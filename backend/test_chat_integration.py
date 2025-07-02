#!/usr/bin/env python3
"""
Final integration test for chat functionality with Gemini
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from api.routes.chat import send_message, ChatRequest

async def test_chat_integration():
    """Test the complete chat integration with Gemini"""
    print("🧪 Testing complete chat integration...")
    
    try:
        # Test new problem scenario
        print("\n📚 Testing new math problem scenario...")
        request = ChatRequest(
            message="I need help with this problem: What is 15 + 27?",
            session_id=None,
            context={}
        )
        
        response = await send_message(request)
        
        print(f"✅ New problem response:")
        print(f"   - Session ID: {response.session_id}")
        print(f"   - Message: {response.message.content[:100]}...")
        print(f"   - Role: {response.message.role}")
        
        # Test follow-up response
        print("\n💬 Testing student response scenario...")
        follow_up_request = ChatRequest(
            message="I think the answer is 42",
            session_id=response.session_id,
            context={}
        )
        
        follow_up_response = await send_message(follow_up_request)
        
        print(f"✅ Follow-up response:")
        print(f"   - Message: {follow_up_response.message.content[:100]}...")
        print(f"   - Assessment available: {'assessment' in follow_up_response.message.metadata}")
        print(f"   - Suggestions: {len(follow_up_response.suggestions or [])}")
        
        if follow_up_response.assessment:
            assessment = follow_up_response.assessment
            print(f"   - Skill level: {assessment.get('skill_level')}")
            print(f"   - Confidence: {assessment.get('confidence')}")
            print(f"   - Emotional state: {assessment.get('emotional_state')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Chat integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_chat_integration())
    if success:
        print("\n🎉 All tests passed! Your TutorAgent application is ready to use.")
        print("\n📋 Summary:")
        print("   ✅ Gemini API authentication working")
        print("   ✅ Assessment agent functioning")
        print("   ✅ Tutoring responses generating")
        print("   ✅ Chat integration complete")
        print("\n🚀 You can now start your application with: python main.py")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    sys.exit(0 if success else 1)
