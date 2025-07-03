#!/usr/bin/env python3
"""
Test script to verify GeminiTutorAgent works correctly
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.assessment.gemini_agent import tutor_agent

async def test_tutor_agent():
    """Test the GeminiTutorAgent"""
    print("🧪 Testing GeminiTutorAgent...")
    
    try:
        # Create a test file with problem and student response
        import tempfile
        import os
        
        problem = "What is 2 + 3?"
        student_response = "I think it's 5"
        
        print(f"📚 Problem: {problem}")
        print(f"👤 Student response: {student_response}")
        
        # Create temporary file with content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            file_content = f"""Problem: {problem}
            
Student Response: {student_response}
            
This is a test of the tutoring functionality."""
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            # Test tutoring response generation
            print("💬 Processing file with tutor agent...")
            tutoring = await tutor_agent.process_file_upload(
                file_path=temp_file_path,
                context={"test": True}
            )
            
            print(f"✅ Tutoring response generated:")
            print(f"   - Message: {tutoring.get('message')}")
            
            return True
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
    except Exception as e:
        print(f"❌ Tutor agent test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_tutor_agent())
    sys.exit(0 if success else 1)
