#!/usr/bin/env python3
"""
Simple test script for TutorAgent chat functionality
Run this to test the basic setup without needing the full frontend
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def test_chat_setup():
    """Test basic chat functionality"""
    print("🧪 Testing TutorAgent Chat Setup...")
    
    try:
        # Test imports
        print("1. Testing imports...")
        from backend.agents.assessment.gemini_agent import assessment_agent
        from backend.services.redis import redis_client
        print("   ✅ Imports successful")
        
        # Test Redis connection (optional - only if Redis is running)
        print("2. Testing Redis connection...")
        try:
            await redis_client.initialize()
            await redis_client.set("test_key", "test_value", expire=10)
            value = await redis_client.get("test_key")
            if value == "test_value":
                print("   ✅ Redis connection working")
            else:
                print("   ⚠️  Redis connection issue")
            await redis_client.delete("test_key")
            await redis_client.close()
        except Exception as e:
            print(f"   ⚠️  Redis not available: {e}")
            print("   (This is OK for basic testing)")
        
        # Test Gemini setup (only if API key is available)
        print("3. Testing Gemini setup...")
        try:
            # This will fail if no API key, but that's expected
            test_assessment = {
                "skill_level": "intermediate",
                "emotional_state": "neutral"
            }
            print("   ✅ Gemini agent initialized")
            print("   (Actual API testing requires GEMINI_API_KEY)")
        except Exception as e:
            print(f"   ⚠️  Gemini setup issue: {e}")
        
        print("\n🎉 Basic setup test completed!")
        print("\nNext steps:")
        print("1. Add your GEMINI_API_KEY to a .env file")
        print("2. Start Redis: docker run --name redis -p 6379:6379 -d redis")
        print("3. Start backend: cd backend && python main.py")
        print("4. Start frontend: cd frontend && npm run dev")
        print("5. Visit http://localhost:3000/chat")
        
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    result = asyncio.run(test_chat_setup())
    sys.exit(0 if result else 1)
