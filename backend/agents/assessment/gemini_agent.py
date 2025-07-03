"""
Tutor Agent using Google Gemini 2.5 Pro
Handles tutoring workflow for high school students with file uploads
"""

import google.generativeai as genai
from typing import Dict, List, Optional, Any
import json
import logging
from core.config import settings

logger = logging.getLogger(__name__)

class GeminiTutorAgent:
    """Tutor agent powered by Google Gemini 2.5 Pro for file-based tutoring"""
    
    def __init__(self):
        """Initialize the Gemini assessment agent"""
        self.model_name = "gemini-2.5-pro"
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
            
            # Configure safety settings for educational content
            import google.generativeai.types as genai_types
            safety_settings = {
                genai_types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai_types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                genai_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai_types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                genai_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai_types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                genai_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai_types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            }
            
            self.model = genai.GenerativeModel(
                self.model_name,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                },
                safety_settings=safety_settings
            )
            logger.info(f"✅ Gemini {self.model_name} client initialized with API key")
        except Exception as e:
            logger.error(f"❌ Failed to init Gemini client: {e}")
            raise
    
    def _setup_prompts(self):
        """Setup system prompt for tutoring tasks"""
        self.tutoring_prompt = """{
  "system_prompt": "You are a friendly, intelligent AI math tutor for high school students aged 12–13. Your mission is to help them develop critical thinking, build intuition, and solve problems in mathematics step-by-step. You support file inputs (PDF, DOCX, images) and dynamically adapt your teaching based on student interaction. You're encouraging, age-appropriate, and use plain language suited to a 12-year-old. Track their skill level and use it to adjust the depth of explanations.",
  "behavior_design": [
    "If a file is uploaded:",
    "- Read and summarize the main topic in 3–5 sentences.",
    "- Ask the student if they’d like to go over the summary or jump to exercises.",
    "- If an 'Exercises' section exists, ask if they want to start with the first question.",
    
    "For each exercise:",
    "- Present one question clearly.",
    "- Ask one focused question to get them thinking.",
    "- Wait for an attempt. If the response is:",
    "  - Correct: Acknowledge with varied praise. Move to next.",
    "  - Partially correct or incorrect: Give hints. Ask guiding questions.",
    "  - No response or confusion after 2 cycles: Explain the answer kindly, then move on.",
    
    "Track the student's level (beginner, intermediate, advanced) based on their responses and tailor your explanations accordingly.",
    
    "General teaching rules:",
    "- Never repeat encouragement phrases.",
    "- Celebrate effort and mistakes as learning.",
    "- If the student skips or jumps, follow their lead.",
    "- Max 4–5 minutes per question."
  ],
  "response_schema": {
    "message": "A single friendly, focused response for the student",
    "student_context_parameters": {
      "context": "Short summary of topic/problem being worked on",
      "problem": "Current math problem/question being attempted",
      "student_response": "Student's latest input/attempt",
      "assessment": "Skill-level assessment (beginner/intermediate/advanced), updated dynamically"
    },
    "response_generation_guidelines": [
      "Ask ONE focused question at a time.",
      "Provide gentle hints, not full answers immediately.",
      "Acknowledge effort, even partial or incorrect.",
      "Guide to the next logical step.",
      "Adapt phrasing based on engagement, tone, and past responses.",
      "If stuck after 2 cycles, explain the solution clearly and encourage them to try the next."
    ]
  }
}
"""


    async def process_file_upload(
        self,
        file_path: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Process an uploaded file and apply the tutoring workflow.
        
        Args:
            file_path: Path to the uploaded file
            context: Additional context for the session
            
        Returns:
            Tutoring response based solely on the file content
        """
        try:
            # Extract content from the uploaded file
            with open(file_path, 'r') as file:
                content = file.read()

            # Using the content to create a tutoring scenario
            prompt = f"""Based on the following tutoring guidelines, generate a response:

{self.tutoring_prompt}

CONTENT:
{content}

Use this content to guide your tutoring response. Respond with ONLY a JSON object in this format:
{{
    "message": "Your encouraging tutoring message with a guiding question"
}}"""

            # Generate and process response using the tutoring prompt
            response = await self._generate_response(prompt)
            tutoring_response = json.loads(response)
            
            logger.info(f"Tutoring response generated from file content.")
            return tutoring_response
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse tutoring JSON from file: {e}")
            return self._get_fallback_tutoring_response()
        except Exception as e:
            logger.error(f"File processing for tutoring failed: {e}")
            return self._get_fallback_tutoring_response()

    async def _generate_response(self, prompt: str) -> str:
        """Generate response using Gemini model"""
        try:
            response = self.model.generate_content(prompt)
            
            # Log the full response for debugging
            logger.info(f"Full Gemini API response: {response}")
            
            # Check if response has valid candidates
            if not hasattr(response, 'candidates') or not response.candidates:
                logger.error("No valid candidates in Gemini response")
                # Try to get finish_reason from prompt_feedback if available
                if hasattr(response, 'prompt_feedback'):
                    logger.error(f"Prompt feedback: {response.prompt_feedback}")
                raise ValueError("No valid response candidates from Gemini API")
            
            # Check if any candidate was blocked or filtered
            for i, candidate in enumerate(response.candidates):
                logger.info(f"Candidate {i} finish_reason: {getattr(candidate, 'finish_reason', 'unknown')}")
                if hasattr(candidate, 'safety_ratings'):
                    logger.info(f"Candidate {i} safety_ratings: {candidate.safety_ratings}")
            
            # Try to get text from response
            try:
                raw_text = response.text.strip()
                if not raw_text:
                    logger.error("Empty text in Gemini response")
                    raise ValueError("Empty response text from Gemini API")
                
                # Strip markdown JSON formatting if present
                cleaned_text = self._clean_json_response(raw_text)
                logger.info(f"Successfully processed Gemini response: {cleaned_text[:100]}...")
                return cleaned_text
                
            except ValueError as text_error:
                logger.error(f"Failed to extract text from Gemini response: {text_error}")
                # Log individual candidate parts for debugging
                for i, candidate in enumerate(response.candidates):
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        logger.error(f"Candidate {i} parts: {candidate.content.parts}")
                        for j, part in enumerate(candidate.content.parts):
                            logger.error(f"Part {j}: {part}")
                raise ValueError(f"Unable to extract text from Gemini response: {text_error}")
                
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            logger.error(f"Exception type: {type(e).__name__}")
            
            # Provide more specific error handling
            if "finish_reason" in str(e).lower() or "safety" in str(e).lower():
                logger.error("Response may have been filtered due to safety concerns or other policy violations")
                raise ValueError("Response was filtered by Gemini's safety systems")
            
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



    def _get_fallback_tutoring_response(self) -> Dict[str, Any]:
        """Fallback tutoring response when AI fails"""
        return {
            "message": "I'm here to help! Can you tell me what you think the first step might be for this problem?",
            "hint_level": 1,
            "celebrates_progress": False,
            "targets_gap": "general_approach"
        }

# Global instance
tutor_agent = GeminiTutorAgent()
