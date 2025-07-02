#!/usr/bin/env python3
"""
Test script to verify GeminiAssessmentAgent works correctly
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.assessment.gemini_agent import assessment_agent

async def test_assessment_agent():
    """Test the GeminiAssessmentAgent"""
    print("🧪 Testing GeminiAssessmentAgent...")
    
    try:
        # Test problem and student response
        problem = "What is 2 + 3?"
        student_response = "I think it's 5"
        
        print(f"📚 Problem: {problem}")
        print(f"👤 Student response: {student_response}")
        
        # Test assessment
        print("🔍 Running assessment...")
        assessment = await assessment_agent.assess_student_response(
            problem=problem,
            student_response=student_response
        )
        
        print(f"✅ Assessment completed:")
        print(f"   - Skill level: {assessment.get('skill_level')}")
        print(f"   - Confidence: {assessment.get('confidence')}")
        print(f"   - Emotional state: {assessment.get('emotional_state')}")
        
        # Test tutoring response
        print("💬 Generating tutoring response...")
        tutoring = await assessment_agent.generate_tutoring_response(
            problem=problem,
            student_response=student_response,
            assessment=assessment
        )
        
        print(f"✅ Tutoring response generated:")
        print(f"   - Message: {tutoring.get('message')}")
        print(f"   - Hint level: {tutoring.get('hint_level')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Assessment agent test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_assessment_agent())
    sys.exit(0 if success else 1)
