#!/usr/bin/env python3
"""
Test script to check if all imports work correctly
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test all the main imports"""
    try:
        print("🔍 Testing imports...")
        
        # Test core imports
        print("  ✓ Testing core imports...")
        from core.config import settings
        from core.logging import setup_logging
        print("    ✅ Core imports successful")
        
        # Test database import
        print("  ✓ Testing database imports...")
        from services.database import database
        print("    ✅ Database imports successful")
        
        # Test redis import
        print("  ✓ Testing redis imports...")
        from services.redis import redis_client
        print("    ✅ Redis imports successful")
        
        # Test route imports
        print("  ✓ Testing route imports...")
        from api.routes import health, upload, session, agents
        print("    ✅ Route imports successful")
        
        print("🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
