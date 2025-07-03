#!/usr/bin/env python3
"""
Test script to verify Gemini API error handling improvements
"""

import asyncio
import logging
import tempfile
import os
from agents.assessment.gemini_agent import tutor_agent

# Set up logging to see all the debug information
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_normal_content():
    """Test with normal content that should work"""
    print("\n=== Testing Normal Content ===")
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            content = """
Math Problem: What is 2 + 2?

Student's answer: I think it's 4, but I'm not sure.
"""
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        response = await tutor_agent.process_file_upload(temp_file_path)
        print(f"✅ Normal content response: {response}")
        
    except Exception as e:
        print(f"❌ Normal content failed: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

async def test_potentially_filtered_content():
    """Test with content that might trigger safety filters"""
    print("\n=== Testing Potentially Filtered Content ===")
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            # Create content that might trigger safety filters
            content = """
Problem: Calculate the blast radius of an explosive device.

This is a math problem for educational purposes only, but it might trigger safety filters.
"""
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        response = await tutor_agent.process_file_upload(temp_file_path)
        print(f"✅ Potentially filtered content response: {response}")
        
    except ValueError as ve:
        print(f"⚠️ Content was filtered (expected): {ve}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

async def test_empty_content():
    """Test with empty content"""
    print("\n=== Testing Empty Content ===")
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write("")
            temp_file_path = temp_file.name
        
        response = await tutor_agent.process_file_upload(temp_file_path)
        print(f"✅ Empty content response: {response}")
        
    except Exception as e:
        print(f"❌ Empty content failed: {e}")
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

async def main():
    """Run all tests"""
    print("🧪 Testing Gemini API Error Handling")
    print("="*50)
    
    await test_normal_content()
    await test_potentially_filtered_content()
    await test_empty_content()
    
    print("\n" + "="*50)
    print("✅ Error handling tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
