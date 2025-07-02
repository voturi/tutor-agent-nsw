"""
Assessment Agent using Google Gemini 2.5 Pro
Handles skill assessment and adaptive tutoring for Year 7 mathematics
"""

import google.generativeai as genai
from typing import Dict, List, Optional, Any
import json
import logging
from core.config import settings

logger = logging.getLogger(__name__)

class GeminiAssessmentAgent:
    """Assessment agent powered by Google Gemini 2.5 Pro"""
    
    def __init__(self):
        """Initialize the Gemini assessment agent"""
        self.model_name = "gemini-1.5-flash-latest"
        self._setup_client()
        self._setup_prompts()
    
    def _setup_client(self):
        """Setup Gemini API client"""
        try:
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY is not set in environment variables")
            
            # Ensure we use API key authentication exclusively
            # Clear any existing auth to prevent OAuth interference
            import os
            os.environ.pop('GOOGLE_APPLICATION_CREDENTIALS', None)
            
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(
                self.model_name,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            logger.info(f"✅ Gemini {self.model_name} client initialized with API key")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini client: {e}")
            raise
    
    def _setup_prompts(self):
        """Setup system prompts for different assessment tasks"""
        self.assessment_prompt = """You are an expert Year 7 mathematics assessment agent. Your role is to:

1. Analyze student responses to identify their skill level
2. Detect knowledge gaps and misconceptions
3. Adapt the tutoring approach based on student performance
4. Provide guidance for the tutoring agent

Student Profile:
- Age: 12-13 years (Year 7)
- Subject: Mathematics (NSW curriculum)
- Context: Homework assistance

Assessment Framework:
- Beginner: Needs step-by-step guidance, struggles with problem identification
- Intermediate: Recognizes patterns but needs support with multi-step problems  
- Advanced: Shows mathematical reasoning, can attempt multiple approaches

IMPORTANT: You must respond with ONLY valid JSON. No other text before or after the JSON object.

Response Format (JSON only):
{{
    "skill_level": "beginner|intermediate|advanced",
    "confidence": 0.0-1.0,
    "knowledge_gaps": ["gap1", "gap2"],
    "strengths": ["strength1", "strength2"],
    "recommended_approach": "detailed strategy",
    "next_question_difficulty": "easier|same|harder",
    "emotional_state": "confident|hesitant|frustrated|engaged",
    "reasoning": "explanation of assessment"
}}"""

        self.tutoring_prompt = """You are a patient, encouraging Year 7 mathematics tutor using the Socratic method. Your goal is to guide students to discover solutions through thoughtful questioning.

Key Principles:
1. NEVER give direct answers - guide through questions
2. Use age-appropriate language (12-13 years old)
3. Be encouraging and patient
4. Break complex problems into smaller steps
5. Celebrate small wins and progress
6. Treat mistakes as learning opportunities

Student Context: {context}
Current Problem: {problem}
Student Response: {student_response}
Assessment: {assessment}

Generate your next tutoring response following these guidelines:
- Ask ONE clear, focused question
- Provide gentle hints without revealing the answer
- Acknowledge what the student did well
- Guide toward the next logical step
- Keep language friendly and encouraging

IMPORTANT: You must respond with ONLY valid JSON. No other text before or after the JSON object.

Response Format (JSON only):
{{
    "message": "Your encouraging tutoring message with a guiding question",
    "hint_level": 1-3,
    "celebrates_progress": true/false,
    "targets_gap": "specific knowledge gap being addressed"
}}"""

    async def assess_student_response(
        self,
        problem: str,
        student_response: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Assess a student's response and provide recommendations
        
        Args:
            problem: The mathematics problem being solved
            student_response: Student's answer or attempt
            context: Additional context about the student's session
            
        Returns:
            Assessment results with skill level, gaps, and recommendations
        """
        try:
            prompt = f"""{self.assessment_prompt}

PROBLEM: {problem}

STUDENT RESPONSE: {student_response}

CONTEXT: {json.dumps(context or {}, indent=2)}

Analyze this response and provide a comprehensive assessment."""

            response = await self._generate_response(prompt)
            
            # Parse JSON response
            assessment = json.loads(response)
            
            # Validate required fields
            required_fields = [
                "skill_level", "confidence", "knowledge_gaps", 
                "strengths", "recommended_approach", "emotional_state"
            ]
            
            for field in required_fields:
                if field not in assessment:
                    logger.warning(f"Missing field in assessment: {field}")
                    assessment[field] = self._get_default_value(field)
            
            logger.info(f"Assessment completed: {assessment['skill_level']}")
            return assessment
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse assessment JSON: {e}")
            logger.error(f"Raw response was: {repr(response[:200])}...")
            return self._get_fallback_assessment()
        except Exception as e:
            logger.error(f"Assessment failed: {e}")
            return self._get_fallback_assessment()

    async def generate_tutoring_response(
        self,
        problem: str,
        student_response: str,
        assessment: Dict[str, Any],
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Generate a Socratic tutoring response based on assessment
        
        Args:
            problem: The mathematics problem
            student_response: Student's latest response
            assessment: Assessment results from assess_student_response
            context: Session context
            
        Returns:
            Tutoring response with message and metadata
        """
        response = None
        try:
            prompt = self.tutoring_prompt.format(
                context=json.dumps(context or {}, indent=2),
                problem=problem,
                student_response=student_response,
                assessment=json.dumps(assessment, indent=2)
            )
            
            response = await self._generate_response(prompt)
            tutoring_response = json.loads(response)
            
            # Add timestamp and assessment reference
            tutoring_response["timestamp"] = context.get("timestamp") if context else None
            tutoring_response["based_on_assessment"] = assessment.get("skill_level")
            
            logger.info(f"Tutoring response generated (hint level: {tutoring_response.get('hint_level', 'unknown')})")
            return tutoring_response
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse tutoring JSON: {e}")
            if response:
                logger.error(f"Raw tutoring response was: {repr(response[:400])}...")
            return self._get_fallback_tutoring_response()
        except Exception as e:
            logger.error(f"Tutoring response generation failed: {e}")
            if response:
                logger.error(f"Raw tutoring response was: {repr(response[:400])}...")
            return self._get_fallback_tutoring_response()

    async def _generate_response(self, prompt: str) -> str:
        """Generate response using Gemini model"""
        try:
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
            
            # Strip markdown JSON formatting if present
            cleaned_text = self._clean_json_response(raw_text)
            return cleaned_text
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise
    
    def _clean_json_response(self, text: str) -> str:
        """Clean JSON response by removing markdown formatting"""
        # Remove markdown JSON code blocks
        if text.startswith('```json'):
            text = text[7:]  # Remove ```json
        elif text.startswith('```'):
            text = text[3:]   # Remove ```
        
        if text.endswith('```'):
            text = text[:-3]  # Remove trailing ```
        
        return text.strip()

    def _get_default_value(self, field: str) -> Any:
        """Get default value for missing assessment fields"""
        defaults = {
            "skill_level": "intermediate",
            "confidence": 0.5,
            "knowledge_gaps": [],
            "strengths": [],
            "recommended_approach": "Continue with guided questioning",
            "emotional_state": "neutral",
            "next_question_difficulty": "same"
        }
        return defaults.get(field, "unknown")

    def _get_fallback_assessment(self) -> Dict[str, Any]:
        """Fallback assessment when AI fails"""
        return {
            "skill_level": "intermediate",
            "confidence": 0.5,
            "knowledge_gaps": ["assessment_unavailable"],
            "strengths": [],
            "recommended_approach": "Continue with standard tutoring approach",
            "next_question_difficulty": "same",
            "emotional_state": "neutral",
            "reasoning": "Fallback assessment due to AI failure"
        }

    def _get_fallback_tutoring_response(self) -> Dict[str, Any]:
        """Fallback tutoring response when AI fails"""
        return {
            "message": "I'm here to help! Can you tell me what you think the first step might be for this problem?",
            "hint_level": 1,
            "celebrates_progress": False,
            "targets_gap": "general_approach"
        }

# Global instance
assessment_agent = GeminiAssessmentAgent()
