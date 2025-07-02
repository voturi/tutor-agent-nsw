"""
PDF Chat API endpoints for document-based tutoring
Handles PDF upload, text extraction, and chat sessions with document context
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import uuid
import logging
from datetime import datetime
import json
import os
import tempfile
from pathlib import Path

from agents.assessment.gemini_agent import assessment_agent
from services.redis import redis_client
from core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Request/Response Models
class PDFChatMessage(BaseModel):
    """Individual PDF chat message"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now)
    question_context: Optional[str] = None
    page_reference: Optional[int] = None

class PDFChatRequest(BaseModel):
    """Request to send a message in PDF chat"""
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class PDFUploadResponse(BaseModel):
    """Response from PDF upload"""
    session_id: str
    document_id: str
    filename: str
    file_size: int
    questions_extracted: int
    processing_status: str
    message: str

class PDFChatResponse(BaseModel):
    """Response from PDF chat endpoint"""
    message: PDFChatMessage
    session_id: str
    document_context: Optional[Dict[str, Any]] = None
    assessment: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None

class PDFChatSession(BaseModel):
    """PDF Chat session data"""
    session_id: str
    document_id: Optional[str] = None
    document_name: Optional[str] = None
    extracted_text: Optional[str] = None
    questions_extracted: int = 0
    current_question: int = 1
    messages: List[PDFChatMessage] = []
    student_level: str = "intermediate"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    model_config = {"arbitrary_types_allowed": True}

# Helper Functions
async def extract_text_from_pdf(file_content: bytes, filename: str) -> Dict[str, Any]:
    """Extract text from PDF using PyPDF2 or similar"""
    try:
        import PyPDF2
        import io
        
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        
        extracted_text = ""
        page_count = len(pdf_reader.pages)
        
        # Extract text from each page
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                page_text = page.extract_text()
                if page_text.strip():
                    extracted_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            except Exception as e:
                logger.warning(f"Failed to extract text from page {page_num + 1}: {e}")
        
        # Count potential questions (basic heuristic)
        questions_found = count_math_questions(extracted_text)
        
        return {
            "text": extracted_text,
            "page_count": page_count,
            "questions_found": questions_found,
            "success": True
        }
        
    except ImportError:
        logger.error("PyPDF2 not installed. Installing...")
        # Fallback to basic text extraction
        return {
            "text": "PDF text extraction requires PyPDF2. Please install it to process documents.",
            "page_count": 1,
            "questions_found": 5,  # Default estimate
            "success": False
        }
    except Exception as e:
        logger.error(f"PDF text extraction failed: {e}")
        return {
            "text": f"Could not extract text from {filename}. The PDF might be image-based or corrupted.",
            "page_count": 1,
            "questions_found": 3,
            "success": False
        }

def count_math_questions(text: str) -> int:
    """Count potential math questions in text using heuristics"""
    question_indicators = [
        "?", "find", "calculate", "solve", "what is", "determine",
        "evaluate", "simplify", "factorize", "expand", "graph",
        "plot", "draw", "construct", "prove", "show that"
    ]
    
    lines = text.lower().split('\n')
    question_count = 0
    
    for line in lines:
        line = line.strip()
        if len(line) > 10:  # Ignore very short lines
            # Check for question indicators
            if any(indicator in line for indicator in question_indicators):
                question_count += 1
            # Check for numbered questions (1., 2., a), b), etc.)
            elif any(line.startswith(f"{i}.") or line.startswith(f"{i})") for i in range(1, 51)):
                question_count += 1
            elif any(line.startswith(f"{letter})") for letter in "abcdefghijklm"):
                question_count += 1
    
    # Ensure at least 1 question found
    return max(1, min(question_count, 20))  # Cap at 20 for sanity

async def get_or_create_pdf_session(session_id: Optional[str] = None) -> PDFChatSession:
    """Get existing PDF session or create a new one"""
    if not session_id:
        session_id = str(uuid.uuid4())
        session = PDFChatSession(session_id=session_id)
        await save_pdf_session(session)
        return session
    
    try:
        session_data = await redis_client.get_json(f"pdf_chat_session:{session_id}")
        if session_data:
            return PDFChatSession(**session_data)
    except Exception as e:
        logger.warning(f"Failed to load PDF session {session_id}: {e}")
    
    # Create new session if not found
    session = PDFChatSession(session_id=session_id)
    await save_pdf_session(session)
    return session

async def save_pdf_session(session: PDFChatSession):
    """Save PDF session to Redis"""
    try:
        session.updated_at = datetime.now()
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
            f"pdf_chat_session:{session.session_id}",
            session_dict,
            expire=7200  # 2 hours
        )
    except Exception as e:
        logger.error(f"Failed to save PDF session {session.session_id}: {e}")

# API Routes
@router.post("/upload", response_model=PDFUploadResponse)
async def upload_pdf_document(file: UploadFile = File(...)):
    """
    Upload PDF document and create new chat session
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported for document chat"
            )
        
        # Check file size
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE // 1024 // 1024}MB"
            )
        
        # Generate IDs
        session_id = str(uuid.uuid4())
        document_id = str(uuid.uuid4())
        
        # Extract text from PDF
        extraction_result = await extract_text_from_pdf(content, file.filename)
        
        # Create new session with document
        session = PDFChatSession(
            session_id=session_id,
            document_id=document_id,
            document_name=file.filename,
            extracted_text=extraction_result["text"],
            questions_extracted=extraction_result["questions_found"]
        )
        
        # Add welcome message
        welcome_message = PDFChatMessage(
            role="assistant",
            content=f"""Excellent! I've successfully processed "{file.filename}" and found {extraction_result["questions_found"]} questions. I can see problems covering various Year 7 topics.

I'm here to guide you through each question step by step using the Socratic method. I won't give you direct answers - instead, I'll ask you questions to help you discover the solutions yourself. This builds real understanding!

Let's start with Question 1. Take a look at it and tell me: what type of mathematical problem do you think this is?""",
            question_context="Document uploaded - starting session"
        )
        
        session.messages.append(welcome_message)
        
        # Save session
        await save_pdf_session(session)
        
        logger.info(f"PDF uploaded and processed: {file.filename}, Session: {session_id}")
        
        return PDFUploadResponse(
            session_id=session_id,
            document_id=document_id,
            filename=file.filename,
            file_size=len(content),
            questions_extracted=extraction_result["questions_found"],
            processing_status="completed",
            message="Document processed successfully! Ready to start tutoring."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF upload error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process PDF document")

@router.post("/send", response_model=PDFChatResponse)
async def send_pdf_chat_message(request: PDFChatRequest):
    """
    Send a message in PDF chat context
    """
    try:
        # Get session
        session = await get_or_create_pdf_session(request.session_id)
        
        if not session.document_id:
            raise HTTPException(
                status_code=400,
                detail="No document uploaded. Please upload a PDF first."
            )
        
        # Create user message
        user_message = PDFChatMessage(
            role="user",
            content=request.message,
            question_context=f"Question {session.current_question}"
        )
        
        # Add to session
        session.messages.append(user_message)
        
        # Prepare context for assessment
        document_context = {
            "document_name": session.document_name,
            "extracted_text": session.extracted_text[:2000],  # Limit for context
            "current_question": session.current_question,
            "total_questions": session.questions_extracted,
            "timestamp": datetime.now().isoformat()
        }
        
        # Assess student response with document context
        assessment = await assessment_agent.assess_student_response(
            problem=f"Question {session.current_question} from {session.document_name}",
            student_response=request.message,
            context={**document_context, **(request.context or {})}
        )
        
        # Generate tutoring response with document awareness
        tutoring_response = await assessment_agent.generate_tutoring_response(
            problem=f"Question {session.current_question} from uploaded homework",
            student_response=request.message,
            assessment=assessment,
            context=document_context
        )
        
        # Create assistant message
        assistant_message = PDFChatMessage(
            role="assistant",
            content=tutoring_response.get("message", "Let me help you with that question!"),
            question_context=f"Question {session.current_question}",
            page_reference=1  # Could be enhanced to track actual page numbers
        )
        
        # Add to session
        session.messages.append(assistant_message)
        
        # Update session level based on assessment
        if assessment and "skill_level" in assessment:
            session.student_level = assessment["skill_level"]
        
        # Save session
        await save_pdf_session(session)
        
        # Generate context-aware suggestions
        suggestions = generate_pdf_suggestions(assessment, session.current_question, session.questions_extracted)
        
        return PDFChatResponse(
            message=assistant_message,
            session_id=session.session_id,
            document_context=document_context,
            assessment=assessment,
            suggestions=suggestions
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process message")

@router.get("/session/{session_id}/history")
async def get_pdf_chat_history(session_id: str):
    """Get PDF chat history for a session"""
    try:
        session = await get_or_create_pdf_session(session_id)
        return {
            "session_id": session.session_id,
            "document_name": session.document_name,
            "questions_extracted": session.questions_extracted,
            "current_question": session.current_question,
            "messages": session.messages,
            "student_level": session.student_level
        }
    except Exception as e:
        logger.error(f"Failed to get PDF chat history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chat history")

@router.post("/session/new")
async def create_new_pdf_session():
    """Create a new PDF chat session"""
    try:
        session = await get_or_create_pdf_session()
        return {
            "session_id": session.session_id,
            "message": "New PDF chat session created! Upload your homework to get started."
        }
    except Exception as e:
        logger.error(f"Failed to create new PDF session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create session")

@router.delete("/session/{session_id}")
async def delete_pdf_session(session_id: str):
    """Delete a PDF chat session"""
    try:
        await redis_client.delete(f"pdf_chat_session:{session_id}")
        return {"message": "PDF session deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete PDF session: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete session")

def generate_pdf_suggestions(assessment: Optional[Dict], current_question: int, total_questions: int) -> List[str]:
    """Generate helpful suggestions based on PDF context and assessment"""
    suggestions = []
    
    if not assessment:
        suggestions = [
            f"What do you notice about Question {current_question}?",
            "Can you identify what type of problem this is?",
            "What information does the question give you?"
        ]
    else:
        skill_level = assessment.get("skill_level", "intermediate")
        
        if skill_level == "beginner":
            suggestions = [
                "Let's read the question together step by step",
                f"What is Question {current_question} asking you to find?",
                "Can you identify the key numbers in this problem?"
            ]
        elif skill_level == "advanced":
            suggestions = [
                f"How does Question {current_question} compare to previous ones?",
                "Can you think of multiple ways to approach this?",
                "What patterns do you see in your homework?"
            ]
        else:  # intermediate
            suggestions = [
                f"What's your first step for Question {current_question}?",
                "Which math concept does this problem use?",
                "Can you explain your thinking so far?"
            ]
    
    # Add navigation suggestions
    if current_question < total_questions:
        suggestions.append(f"Ready to move to Question {current_question + 1}?")
    
    return suggestions[:3]  # Limit to 3 suggestions
