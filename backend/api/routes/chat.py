"""
Chat API endpoints for the tutoring interface
Handles real-time conversation between student and AI tutor
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import uuid
import logging
from datetime import datetime

from agents.assessment.gemini_agent import tutor_agent
from services.redis import redis_client

logger = logging.getLogger(__name__)

router = APIRouter()

# Request/Response Models
class ChatMessage(BaseModel):
    """Individual chat message"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    """Request to send a chat message"""
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    """Response from the chat endpoint"""
    message: ChatMessage
    session_id: str
    assessment: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None

class ChatSession(BaseModel):
    """Chat session data"""
    session_id: str
    messages: List[ChatMessage] = []
    current_problem: Optional[str] = None
    student_level: str = "intermediate"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    model_config = {"arbitrary_types_allowed": True}

# Session Management
async def get_or_create_session(session_id: Optional[str] = None) -> ChatSession:
    """Get existing session or create a new one"""
    if not session_id:
        session_id = str(uuid.uuid4())
        session = ChatSession(session_id=session_id)
        await save_session(session)
        return session
    
    try:
        session_data = await redis_client.get_json(f"chat_session:{session_id}")
        if session_data:
            return ChatSession(**session_data)
    except Exception as e:
        logger.warning(f"Failed to load session {session_id}: {e}")
    
    # Create new session if not found
    session = ChatSession(session_id=session_id)
    await save_session(session)
    return session

async def save_session(session: ChatSession):
    """Save session to Redis"""
    try:
        session.updated_at = datetime.now()
        # Convert to dict and handle datetime serialization
        session_dict = session.model_dump()
        
        # Convert datetime objects to ISO strings
        for key, value in session_dict.items():
            if isinstance(value, datetime):
                session_dict[key] = value.isoformat()
        
        # Handle nested datetime in messages
        for message in session_dict.get('messages', []):
            if 'timestamp' in message and isinstance(message['timestamp'], datetime):
                message['timestamp'] = message['timestamp'].isoformat()
        
        await redis_client.set_json(
            f"chat_session:{session.session_id}",
            session_dict,
            expire=3600  # 1 hour
        )
    except Exception as e:
        logger.error(f"Failed to save session {session.session_id}: {e}")

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Send a message to the AI tutor and get a response
    """
    try:
        # Get or create session
        session = await get_or_create_session(request.session_id)
        
        # Create user message
        user_message = ChatMessage(
            role="user",
            content=request.message,
            metadata=request.context
        )
        
        # Add to session
        session.messages.append(user_message)
        
        # Determine if this is the start of a new problem or continuation
        is_new_problem = (
            len(session.messages) == 1 or 
            "new problem" in request.message.lower() or
            session.current_problem is None
        )
        
        if is_new_problem:
            # This looks like a new problem - set it as current
            session.current_problem = request.message
            
            # Generate welcoming response for new problem
            assistant_content = await generate_initial_response(request.message)
            assessment = None
        else:
            # This is a continuation - use tutoring approach directly
            # Create temporary file with conversation context
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                # Write problem and student response
                file_content = f"""Current Problem: {session.current_problem or "General math help"}

Student Response: {request.message}

Context: {request.context or {}}"""
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                # Process with tutor agent
                tutoring_response = await tutor_agent.process_file_upload(
                    file_path=temp_file_path,
                    context=request.context
                )
                assistant_content = tutoring_response.get("message", "Let me help you with that!")
                assessment = None  # No longer using assessment
            except ValueError as ve:
                # Handle Gemini API filtering or safety errors
                logger.warning(f"Gemini API filtered response: {ve}")
                assistant_content = "I'm here to help, but let me approach this differently. Can you tell me more about what you're working on?"
                assessment = None
            except Exception as e:
                # Handle other API errors
                logger.error(f"Error processing with tutor agent: {e}")
                assistant_content = "I'm having a technical issue right now, but I still want to help! What specific part of this problem would you like to work on together?"
                assessment = None
            finally:
                # Clean up temporary file
                import os
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
        
        # Create assistant message
        assistant_message = ChatMessage(
            role="assistant",
            content=assistant_content,
            metadata={
                "assessment": assessment,  # Will be None in the new flow
                "problem": session.current_problem
            }
        )
        
        # Add to session
        session.messages.append(assistant_message)
        
        # Update session level based on assessment
        if assessment and "skill_level" in assessment:
            session.student_level = assessment["skill_level"]
        
        # Save session
        await save_session(session)
        
        # Generate helpful suggestions
        suggestions = generate_suggestions(assessment, session.current_problem)
        
        return ChatResponse(
            message=assistant_message,
            session_id=session.session_id,
            assessment=assessment,
            suggestions=suggestions
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process message")

@router.get("/session/{session_id}/history")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    try:
        session = await get_or_create_session(session_id)
        return {
            "session_id": session.session_id,
            "messages": session.messages,
            "current_problem": session.current_problem,
            "student_level": session.student_level
        }
    except Exception as e:
        logger.error(f"Failed to get chat history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chat history")

@router.post("/session/new")
async def create_new_session():
    """Create a new chat session"""
    try:
        session = await get_or_create_session()
        return {
            "session_id": session.session_id,
            "message": "New tutoring session created! What math problem would you like help with?"
        }
    except Exception as e:
        logger.error(f"Failed to create new session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create session")

@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a chat session"""
    try:
        await redis_client.delete(f"chat_session:{session_id}")
        return {"message": "Session deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete session: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete session")

# Helper Functions
async def generate_initial_response(problem: str) -> str:
    """Generate initial welcoming response for a new problem"""
    try:
        # Use tutor agent to generate initial response
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            # Write problem context
            file_content = f"""New Problem: {problem}

Student needs help with this problem."""
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            # Process with tutor agent
            dummy_response = await tutor_agent.process_file_upload(
                file_path=temp_file_path,
                context={"is_initial": True}
            )
            return dummy_response.get("message", "Great! I'm here to help you work through this problem step by step. What do you think might be a good first step?")
        finally:
            # Clean up temporary file
            import os
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    except Exception as e:
        logger.warning(f"Failed to generate initial response: {e}")
        return "Hi! I'm excited to help you with this math problem. Let's work through it together - what do you think we should look at first?"

def generate_suggestions(assessment: Optional[Dict], current_problem: Optional[str]) -> List[str]:
    """Generate helpful suggestions based on assessment"""
    suggestions = []
    
    if not assessment:
        suggestions = [
            "Can you show me your work so far?",
            "What's the first step you would take?",
            "Are there any parts you're unsure about?"
        ]
    else:
        skill_level = assessment.get("skill_level", "intermediate")
        emotional_state = assessment.get("emotional_state", "neutral")
        
        if skill_level == "beginner":
            suggestions = [
                "Let's break this into smaller steps",
                "What information do we have?",
                "Can you identify what we need to find?"
            ]
        elif skill_level == "advanced":
            suggestions = [
                "Are there multiple ways to solve this?",
                "Can you explain your reasoning?",
                "What would happen if we changed one of the numbers?"
            ]
        else:  # intermediate
            suggestions = [
                "What operation might help here?",
                "Can you try the next step?",
                "Does this remind you of similar problems?"
            ]
        
        if emotional_state == "frustrated":
            suggestions = [
                "Take your time - we'll figure this out together",
                "Let's try a different approach",
                "You're doing well - keep going!"
            ]
    
    return suggestions[:3]  # Limit to 3 suggestions
