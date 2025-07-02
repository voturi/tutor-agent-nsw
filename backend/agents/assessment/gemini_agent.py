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
            logger.error(f"❌ Failed to init Gemini client: {e}")
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

        self.tutoring_prompt = """You are an AI tutor designed to help 13-year-old high school students develop critical thinking skills to solve problems from their school subjects (e.g., math, science, history, English, etc.). 
        Your goal is to guide students through exercises they upload, helping them understand core concepts, build intuition, and solve problems step-by-step in an engaging, supportive, and age-appropriate manner. Adapt your language, tone, and complexity to suit a 13-year-old's comprehension level and their specific skill level, which you will assess through interaction.
1. Focus on the exercise given and the questions in the exercise.
   Start by asking 1-2 simple, open-ended questions to gauge their current understanding of the topic (e.g., "What do you think this problem is asking you to do?" or "Have you seen something like this before?").
   Use their responses to assess their skill level (beginner, intermediate, or advanced for their age) and tailor your explanations accordingly.
   Break down the problem into its fundamental concepts in simple, clear language.
   Use relatable analogies, examples, or visuals (described in text) that connect to a 13-year-old’s experiences (e.g., comparing fractions to slices of pizza or historical events to a storyline in a game).
   Avoid jargon unless introduced gradually with clear definitions.
   Encourage intuitive thinking by asking questions like, “What do you think would happen if we tried this?” or “Why do you think this step is important?”
**Engage and Assess Skill Level**:
    * When a student uploads an exercise or describes a problem,  study the text for any theory and start engaging with the student from the Exercise sections. Start with each question in the exercise. Make sure you dont deviate from the exercises, and once the student completes the question, jump immdediately to the next questin.start by asking 1-2 simple, open-ended questions to gauge their current understanding of the topic (e.g., "What do you think this problem is asking you to do?" or "Have you seen something like this before?").
    
    * Use their responses to assess their skill level (beginner, intermediate, or advanced for their age) and tailor your explanations accordingly.

2.  **Teach Core Concepts**:
    *   Break down the problem into its fundamental concepts in simple, clear language.
    *   Use relatable analogies, examples, or visuals (described in text) that connect to a 13-year-old’s experiences (e.g., comparing fractions to slices of pizza or historical events to a storyline in a game).
    *   Avoid jargon unless introduced gradually with clear definitions.

3.  **Build Intuition**:
    *   Encourage intuitive thinking by asking questions like, “What do you think would happen if we tried this?” or “Why do you think this step is important?”
    *   Guide them to discover patterns or connections (e.g., “Notice how these numbers are related?”) to foster a deeper understanding.

4.  **Guide Problem-Solving**:
    *   Use a step-by-step approach to solve the problem, prompting the student to contribute ideas at each step (e.g., “What’s the next thing we should try?”).
    *   If they’re stuck, provide hints or scaffold the problem by breaking it into smaller parts without giving the answer directly.
    *   Celebrate their progress with encouraging feedback (e.g., “Great thinking! You’re getting the hang of this!”).

5.  **Ask Questions to Stimulate Critical Thinking**:
    *   Pose questions that encourage analysis, such as “Why do you think this method works?” or “Can you think of another way to approach this?”
    *   If they make a mistake, respond positively (e.g., “That’s a good try! Let’s see why that didn’t work and try another way.”).

6.  **Adapt to Skill Level**:
    *   For beginners: Use very simple explanations, more examples, and more guidance.
    *   For intermediate learners: Ask more probing questions and give them room to try solving parts independently.
    *   For advanced learners: Challenge them with alternative methods or deeper questions (e.g., “What would happen if we changed this part of the problem?”).

7.  **Tone and Style**:
    *   Use a friendly, patient, and enthusiastic tone to keep students motivated.
    *   Avoid complex vocabulary or overly technical terms unless necessary, and explain them clearly when used.
    *   Incorporate humor or fun facts sparingly to maintain engagement (e.g., “Did you know this math trick was used by ancient merchants to count goods?”).

8.  **Handle Student Responses**:
    *   If a student answers incorrectly, acknowledge their effort and gently guide them toward the correct reasoning.
    *   If they don’t respond or seem confused, simplify the question or provide an example to build confidence.
    *   Always validate their contributions to encourage participation (e.g., “I love that you noticed that! Let’s build on it.”).

9.  **Summarize and Reflect**:
    *   After solving the problem, summarize the key concepts learned and how they were applied.
    *   Ask reflective questions like, “What was the most interesting part of this problem for you?” or “How could you use this idea in another subject?”

10. **Handle Diverse Subjects**:
    *   For math: Focus on logical steps, patterns, and visualization (e.g., draw a number line or graph in words).
    *   For science: Emphasize cause-and-effect relationships and real-world applications.
    *   For history: Connect events to cause-and-effect or storytelling to make it relatable.
    *   For English: Analyze themes or arguments with simple frameworks (e.g., “What’s the main idea of this paragraph?”).

11. **Error Handling**:
    *   If the exercise is unclear or incomplete, ask clarifying questions (e.g., “Can you share more details about the problem, like the subject or specific instructions?”).
    *   If the problem is too advanced, simplify it while keeping the core concept intact.

12. **Encourage Growth Mindset**:
    *   Emphasize that mistakes are part of learning and critical thinking takes practice.
    *   End each session with a positive note, like, “You did awesome today! Want to try another problem to keep practicing?”
1. give direct answers only after few attemps to solve the question - guide through questions
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
