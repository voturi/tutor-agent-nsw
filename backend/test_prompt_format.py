#!/usr/bin/env python3
"""
Test tutoring prompt formatting
"""

import sys
from pathlib import Path
import json

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.assessment.gemini_agent import assessment_agent

def test_prompt_format():
    """Test tutoring prompt formatting"""
    print("🔍 Testing tutoring prompt formatting...")
    
    context = {}
    problem = "What is 2 + 3?"
    student_response = "I think it's 5"
    assessment = {"skill_level": "beginner", "confidence": 0.8, "emotional_state": "confident"}
    
    try:
        prompt = assessment_agent.tutoring_prompt.format(
            context=json.dumps(context or {}, indent=2),
            problem=problem,
            student_response=student_response,
            assessment=json.dumps(assessment, indent=2)
        )
        
        print("✅ Prompt formatting successful")
        print(f"📝 Generated prompt:\n{prompt}")
        
    except Exception as e:
        print(f"❌ Prompt formatting failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prompt_format()
