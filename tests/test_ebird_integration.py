#!/usr/bin/env python3
"""
eBird Integration Test Script
Tests the eBird API integration and EBirdAgent functionality
"""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config.settings import get_settings
from src.core.ebird_service import EBirdService
from src.mcp.ebird_agent import EBirdAgent, AgentTask


def test_ebird_api_connection():
    """Test basic eBird API connection"""
    print("🦅 Testing eBird API Connection")
    print("=" * 50)
    
    settings = get_settings()
    
    if not settings.ebird_api_key:
        print("❌ No eBird API key found. Please set EBIRD_API_KEY environment variable.")
        print("   You can get one from: https://ebird.org/api/keygen")
        return False
    
    try:
        # Initialize eBird service
        ebird_service = EBirdService(settings.ebird_api_key)
        print(f"✅ eBird service initialized with API key: {settings.ebird_api_key[:10]}...")
        
        # Test basic API call
        print("\n📡 Testing API connection...")
        observations = ebird_service.get_recent_observations("New York", days=1)
        print(f"✅ API connection successful! Found {len(observations)} recent observations")
        
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False


def test_ebird_agent():
    """Test EBirdAgent functionality"""
    print("\n🤖 Testing EBirdAgent")
    print("=" * 50)
    
    settings = get_settings()
    
    if not settings.ebird_api_key:
        print("❌ No eBird API key found. Skipping agent test.")
        return False
    
    try:
        # Initialize services
        ebird_service = EBirdService(settings.ebird_api_key)
        ebird_agent = EBirdAgent(ebird_service)
        
        print(f"✅ EBirdAgent initialized with capabilities: {ebird_agent.capabilities}")
        
        # Test species analysis
        print("\n🔍 Testing species analysis...")
        species_task = AgentTask(
            agent_name=ebird_agent.name,
            task_type="species_analysis",
            input_data={
                "species": "American Robin",
                "location": "New York",
                "date_range": "Spring 2024"
            }
        )
        
        result = ebird_agent.execute(species_task)
        
        if result.success:
            print("✅ Species analysis successful!")
            data = result.data
            print(f"   - Success rate: {data.get('success_rate', 0):.2f}")
            print(f"   - Observations: {data.get('observations_count', 0)}")
            print(f"   - AI insights: {len(data.get('ai_insights', []))}")
        else:
            print(f"❌ Species analysis failed: {result.data.get('error', 'Unknown error')}")
        
        # Test success prediction
        print("\n🎯 Testing success prediction...")
        prediction_task = AgentTask(
            agent_name=ebird_agent.name,
            task_type="success_prediction",
            input_data={
                "species": ["American Robin", "Northern Cardinal"],
                "location": "New York",
                "date_range": "Spring 2024"
            }
        )
        
        pred_result = ebird_agent.execute(prediction_task)
        
        if pred_result.success:
            print("✅ Success prediction successful!")
            data = pred_result.data
            print(f"   - Overall success rate: {data.get('overall_success_rate', 0):.2f}")
            print(f"   - Individual predictions: {data.get('predictions', {})}")
            print(f"   - Recommendations: {len(data.get('recommendations', []))}")
        else:
            print(f"❌ Success prediction failed: {pred_result.data.get('error', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ EBirdAgent test failed: {e}")
        return False


def test_real_time_data():
    """Test real-time data functionality"""
    print("\n📊 Testing Real-time Data")
    print("=" * 50)
    
    settings = get_settings()
    
    if not settings.ebird_api_key:
        print("❌ No eBird API key found. Skipping real-time data test.")
        return False
    
    try:
        ebird_service = EBirdService(settings.ebird_api_key)
        
        # Test recent observations
        print("📡 Fetching recent observations...")
        observations = ebird_service.get_recent_observations("New York", days=7)
        
        print(f"✅ Found {len(observations)} recent observations")
        
        if observations:
            print("\n📋 Sample observations:")
            for i, obs in enumerate(observations[:3]):  # Show first 3
                print(f"   {i+1}. {obs.species} at {obs.location}")
                print(f"      Time: {obs.timestamp}")
                print(f"      Observer: {obs.observer}")
                print()
        
        # Test success rate prediction
        print("🎯 Testing success rate prediction...")
        success_rate = ebird_service.predict_success_rate(
            "American Robin", "New York", "2024-04-15"
        )
        print(f"✅ Success rate for American Robin: {success_rate:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Real-time data test failed: {e}")
        return False


def main():
    """Main test function"""
    print("🦅 BirdingPlanner eBird Integration Test")
    print("=" * 60)
    print(f"Test started at: {datetime.now()}")
    print()
    
    # Run tests
    tests = [
        ("eBird API Connection", test_ebird_api_connection),
        ("EBirdAgent Functionality", test_ebird_agent),
        ("Real-time Data", test_real_time_data)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! eBird integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the configuration and API key.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 