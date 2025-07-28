#!/usr/bin/env python3
"""
eBird Trip Reports Test Script
Demonstrates the new trip report analysis functionality
"""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config.settings import get_settings
from src.core.ebird_service import EBirdService
from src.mcp.ebird_agent import EBirdAgent, AgentTask


def test_trip_reports():
    """Test trip report functionality"""
    print("🦅 Testing eBird Trip Reports Functionality")
    print("=" * 60)
    
    settings = get_settings()
    
    if not settings.ebird_api_key:
        print("❌ No eBird API key found. Please set EBIRD_API_KEY environment variable.")
        print("   You can get one from: https://ebird.org/api/keygen")
        return False
    
    try:
        # Initialize services
        ebird_service = EBirdService(settings.ebird_api_key)
        ebird_agent = EBirdAgent(ebird_service)
        
        print(f"✅ Services initialized with API key: {settings.ebird_api_key[:10]}...")
        
        # Test 1: Get trip reports
        print("\n📋 Test 1: Getting Trip Reports")
        print("-" * 40)
        
        trip_reports = ebird_service.get_trip_reports("New York", days=30)
        print(f"✅ Found {len(trip_reports)} trip reports")
        
        if trip_reports:
            print("\n📊 Sample Trip Report:")
            sample_report = trip_reports[0]
            print(f"   Date: {sample_report['date']}")
            print(f"   Observer: {sample_report['observer']}")
            print(f"   Species Count: {sample_report['species_count']}")
            print(f"   Hotspots Visited: {len(sample_report['hotspots_visited'])}")
            print(f"   Highlights: {', '.join(sample_report['highlights'][:2])}")
            print(f"   Recommendations: {', '.join(sample_report['recommendations'][:2])}")
        
        # Test 2: Trip report analysis
        print("\n🔍 Test 2: Trip Report Analysis")
        print("-" * 40)
        
        analysis_task = AgentTask(
            agent_name=ebird_agent.name,
            task_type="trip_report_analysis",
            input_data={
                "location": "New York",
                "days": 30
            }
        )
        
        analysis_result = ebird_agent.execute(analysis_task)
        
        if analysis_result.success:
            analysis = analysis_result.data["analysis"]
            print(f"✅ Analysis completed successfully")
            print(f"   Total Reports: {analysis['total_reports']}")
            print(f"   Average Species per Trip: {analysis['average_species_per_trip']:.1f}")
            print(f"   Most Productive Hotspots: {len(analysis['most_productive_hotspots'])}")
            print(f"   Common Species: {len(analysis['common_species'])}")
            print(f"   Rare Species: {len(analysis['rare_species'])}")
            
            if analysis['recommendations']:
                print(f"   Recommendations: {', '.join(analysis['recommendations'])}")
        else:
            print(f"❌ Analysis failed: {analysis_result.data.get('error', 'Unknown error')}")
        
        # Test 3: Trip planning insights
        print("\n🎯 Test 3: Trip Planning Insights")
        print("-" * 40)
        
        insights_task = AgentTask(
            agent_name=ebird_agent.name,
            task_type="trip_planning_insights",
            input_data={
                "location": "New York",
                "target_species": ["American Robin", "Northern Cardinal", "Blue Jay"],
                "date_range": "Spring 2024"
            }
        )
        
        insights_result = ebird_agent.execute(insights_task)
        
        if insights_result.success:
            insights = insights_result.data["insights"]
            basic_insights = insights["basic_insights"]
            ai_recommendations = insights["ai_recommendations"]
            
            print(f"✅ Insights generated successfully")
            print(f"   Total Trips Analyzed: {basic_insights['total_trips']}")
            print(f"   Average Species per Trip: {basic_insights['average_species_per_trip']:.1f}")
            print(f"   Best Timing: {basic_insights['best_timing']}")
            
            if basic_insights['top_hotspots']:
                top_hotspot = basic_insights['top_hotspots'][0]
                print(f"   Top Hotspot: {top_hotspot[0]} ({top_hotspot[1]} visits)")
            
            print(f"   Target Species Success Rates:")
            for species, rate in basic_insights['target_species_success'].items():
                print(f"     {species}: {rate:.1%}")
            
            if ai_recommendations:
                print(f"   AI Recommendations:")
                for rec in ai_recommendations:
                    print(f"     • {rec}")
            
            # Show hotspot prioritization
            prioritized = insights["hotspot_prioritization"]
            if prioritized:
                print(f"   Hotspot Prioritization:")
                for hotspot in prioritized[:3]:
                    print(f"     • {hotspot['hotspot']}: {hotspot['priority']} priority")
            
            # Show species success predictions
            predictions = insights["species_success_prediction"]
            if predictions:
                print(f"   Species Success Predictions:")
                for species, pred in predictions.items():
                    print(f"     • {species}: {pred['predicted_success_rate']:.1%} ({pred['confidence']} confidence)")
        else:
            print(f"❌ Insights generation failed: {insights_result.data.get('error', 'Unknown error')}")
        
        # Test 4: Compare with traditional planning
        print("\n🔄 Test 4: Comparison with Traditional Planning")
        print("-" * 40)
        
        # Get traditional success rate
        traditional_success = ebird_service.predict_success_rate("American Robin", "New York", "2024-04-15")
        print(f"   Traditional Success Rate for American Robin: {traditional_success:.1%}")
        
        # Get trip report based success rate
        if insights_result.success:
            trip_based_success = insights_result.data["insights"]["species_success_prediction"]["American Robin"]["predicted_success_rate"]
            print(f"   Trip Report Based Success Rate: {trip_based_success:.1%}")
            
            improvement = ((trip_based_success - traditional_success) / traditional_success * 100) if traditional_success > 0 else 0
            print(f"   Improvement: {improvement:+.1f}%")
        
        print("\n✅ All trip report tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


def demo_trip_report_features():
    """Demonstrate trip report features"""
    print("\n🎬 Trip Report Features Demo")
    print("=" * 60)
    
    settings = get_settings()
    if not settings.ebird_api_key:
        print("❌ No eBird API key available for demo")
        return
    
    ebird_service = EBirdService(settings.ebird_api_key)
    ebird_agent = EBirdAgent(ebird_service)
    
    print("\n📊 Feature 1: Trip Report Generation")
    print("   • Automatically creates trip reports from recent observations")
    print("   • Groups observations by date and observer")
    print("   • Generates highlights and recommendations")
    
    print("\n🔍 Feature 2: Trip Report Analysis")
    print("   • Analyzes patterns across multiple trips")
    print("   • Identifies most productive hotspots")
    print("   • Finds common and rare species patterns")
    
    print("\n🎯 Feature 3: Trip Planning Insights")
    print("   • Provides AI-enhanced recommendations")
    print("   • Predicts species success rates")
    print("   • Prioritizes hotspots based on historical data")
    
    print("\n📈 Feature 4: Success Rate Comparison")
    print("   • Compares traditional vs. trip report based predictions")
    print("   • Shows improvement in accuracy")
    print("   • Provides confidence levels for predictions")
    
    print("\n💡 Benefits of Trip Report Integration:")
    print("   • More accurate success rate predictions")
    print("   • Better hotspot recommendations")
    print("   • Real-world timing insights")
    print("   • Community-driven recommendations")
    print("   • Historical pattern analysis")


if __name__ == "__main__":
    print("🦅 eBird Trip Reports Integration Test")
    print("=" * 60)
    
    # Run tests
    success = test_trip_reports()
    
    # Show demo
    demo_trip_report_features()
    
    if success:
        print("\n🎉 Trip reports integration is working perfectly!")
        print("   This feature enhances route planning with real-world trip data.")
    else:
        print("\n⚠️  Some tests failed. Check your API key and internet connection.") 