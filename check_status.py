#!/usr/bin/env python3
"""
BirdingPlanner Status Check Script
Verifies the integrity and functionality of the BirdingPlanner system.
"""

import os
import sys
import importlib
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 7:
        print("   ✅ Python version is compatible")
        return True
    else:
        print("   ❌ Python 3.7+ is required")
        return False

def check_virtual_environment():
    """Check if virtual environment is active."""
    print("\n🔧 Checking virtual environment...")
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("   ✅ Virtual environment is active")
        return True
    else:
        print("   ⚠️  Virtual environment not detected")
        print("   💡 Run: source birding_env/bin/activate")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    print("\n📚 Checking dependencies...")
    
    required_packages = [
        'pytest',
        'black', 
        'flake8',
        'sphinx'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   💡 Install missing packages: pip install {' '.join(missing_packages)}")
        return False
    else:
        print("   ✅ All dependencies are installed")
        return True

def check_project_structure():
    """Check if project files and directories exist."""
    print("\n📁 Checking project structure...")
    
    required_files = [
        'mcp_server/main.py',
        'agents/bird_info_agent.py',
        'agents/tier_classifier.py', 
        'agents/route_planner.py',
        'agents/content_writer.py',
        'requirements.txt',
        'README.md',
        'test_different_species.py'
    ]
    
    required_dirs = [
        'mcp_server',
        'agents',
        'output'
    ]
    
    missing_items = []
    
    # Check files
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (missing)")
            missing_items.append(file_path)
    
    # Check directories
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ❌ {dir_path}/ (missing)")
            missing_items.append(dir_path)
    
    if missing_items:
        print(f"\n   ❌ Missing {len(missing_items)} items")
        return False
    else:
        print("   ✅ Project structure is complete")
        return True

def check_output_files():
    """Check if output files have been generated."""
    print("\n📄 Checking output files...")
    
    output_files = [
        'output/trip_plan.md',
        'output/social_captions.txt',
        'output/story_cards/'
    ]
    
    generated_files = []
    
    for file_path in output_files:
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                print(f"   ✅ {file_path} ({size} bytes)")
            else:
                print(f"   ✅ {file_path} (directory)")
            generated_files.append(file_path)
        else:
            print(f"   ❌ {file_path} (not generated)")
    
    if generated_files:
        print(f"   ✅ {len(generated_files)} output files found")
        return True
    else:
        print("   ❌ No output files found")
        print("   💡 Run: python mcp_server/main.py")
        return False

def run_basic_test():
    """Run a basic functionality test."""
    print("\n🧪 Running basic functionality test...")
    
    try:
        # Add the mcp_server directory to the path
        sys.path.append('mcp_server')
        
        # Import the main module
        from main import generate_complete_trip_plan
        
        # Test with minimal input
        test_input = {
            "species": ["American Robin"],
            "location": "New York",
            "date_range": "Spring 2024"
        }
        
        result = generate_complete_trip_plan(test_input)
        
        if "error" in result:
            print(f"   ❌ Test failed: {result['error']}")
            return False
        else:
            print("   ✅ Basic functionality test passed")
            return True
            
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

def main():
    """Main status check function."""
    print("🦅 BirdingPlanner Status Check")
    print("=" * 40)
    
    checks = [
        check_python_version,
        check_virtual_environment,
        check_dependencies,
        check_project_structure,
        check_output_files,
        run_basic_test
    ]
    
    results = []
    
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Check failed: {str(e)}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Status Summary")
    print("=" * 40)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All checks passed! BirdingPlanner is ready to use.")
        print("\n🚀 Next steps:")
        print("   python mcp_server/main.py")
        print("   python test_different_species.py")
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. Please address the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 