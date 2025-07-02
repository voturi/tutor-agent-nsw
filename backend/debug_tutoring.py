#!/usr/bin/env python3
"""
Debug script to see raw tutoring response from Gemini
"""

import os
import sys
from pathlib import Path
import json

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import google.generativeai as genai
from core.config import settings

def debug_tutoring_response():
    """Debug tutoring response"""
    print("🔍 Testing raw tutoring response...")
    
    # Clear any OAuth credentials that might interfere
    os.environ.pop('GOOGLE_APPLICATION_CREDENTIALS', None)
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        prompt = """You are a patient, encouraging Year 7 mathematics tutor using the Socratic method. Your goal is to guide students to discover solutions through thoughtful questioning.

IMPORTANT: You must respond with ONLY valid JSON. No other text before or after the JSON object.

Response Format (JSON only):
{
    "message": "Your encouraging tutoring message with a guiding question",
    "hint_level": 1-3,
    "celebrates_progress": true/false,
    "targets_gap": "specific knowledge gap being addressed"
}

Student Context: {}
Current Problem: What is 2 + 3?
Student Response: I think it's 5
Assessment: {"skill_level": "beginner", "confidence": 0.8, "emotional_state": "confident"}

Generate your next tutoring response following these guidelines:
- Ask ONE clear, focused question
- Provide gentle hints without revealing the answer
- Acknowledge what the student did well
- Guide toward the next logical step
- Keep language friendly and encouraging"""
        
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        
        print(f"📝 Raw response: {repr(raw_text)}")
        print(f"📝 Raw response (formatted):\n{raw_text}")
        
        # Try to clean and parse
        if raw_text.startswith('```json'):
            cleaned = raw_text[7:]
        elif raw_text.startswith('```'):
            cleaned = raw_text[3:]
        else:
            cleaned = raw_text
            
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
            
        cleaned = cleaned.strip()
        print(f"🧹 Cleaned response: {repr(cleaned)}")
        
        try:
            parsed = json.loads(cleaned)
            print(f"✅ Successfully parsed JSON: {parsed}")
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_tutoring_response()
