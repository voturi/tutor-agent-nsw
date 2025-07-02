#!/usr/bin/env python3
"""
Test script to verify Gemini API key authentication
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import google.generativeai as genai
from core.config import settings

def test_gemini_auth():
    """Test Gemini API authentication"""
    print("🧪 Testing Gemini API Authentication...")
    
    # Clear any OAuth credentials that might interfere
    os.environ.pop('GOOGLE_APPLICATION_CREDENTIALS', None)
    
    try:
        # Check if API key is available
        if not settings.GEMINI_API_KEY:
            print("❌ GEMINI_API_KEY is not set!")
            print("Please check your .env file or environment variables")
            return False
            
        print(f"✅ API Key found: {settings.GEMINI_API_KEY[:10]}...{settings.GEMINI_API_KEY[-4:]}")
        
        # Configure Gemini with API key
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Create model instance
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        # Test with a simple prompt
        print("🚀 Testing API call...")
        response = model.generate_content("Say 'Hello, I am working correctly!' in exactly those words.")
        
        print(f"✅ Success! Response: {response.text.strip()}")
        return True
        
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini_auth()
    sys.exit(0 if success else 1)
