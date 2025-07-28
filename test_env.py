#!/usr/bin/env python3
"""
Test environment variable loading
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_env_loading():
    """Test if .env file is loaded correctly."""
    print("🔍 Testing Environment Variable Loading")
    print("=" * 50)
    
    # Test 1: Direct environment variable
    print(f"1. Direct EBIRD_API_KEY: {os.getenv('EBIRD_API_KEY', 'NOT_FOUND')}")
    
    # Test 2: Load .env file manually
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print(f"2. After load_dotenv(): {os.getenv('EBIRD_API_KEY', 'NOT_FOUND')}")
    except ImportError:
        print("2. python-dotenv not available")
    
    # Test 3: Test settings loading
    try:
        from src.config.settings import get_settings
        settings = get_settings()
        print(f"3. Settings EBIRD_API_KEY: {settings.ebird_api_key or 'NOT_FOUND'}")
    except Exception as e:
        print(f"3. Settings loading failed: {e}")
    
    # Test 4: Check .env file content
    env_file = Path('.env')
    if env_file.exists():
        print(f"4. .env file exists: {env_file.absolute()}")
        with open(env_file, 'r') as f:
            content = f.read()
            if 'EBIRD_API_KEY' in content:
                print("   ✅ EBIRD_API_KEY found in .env file")
            else:
                print("   ❌ EBIRD_API_KEY not found in .env file")
    else:
        print("4. .env file does not exist")

if __name__ == "__main__":
    test_env_loading() 