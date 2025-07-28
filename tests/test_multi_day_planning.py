#!/usr/bin/env python3
"""
Multi-Day Birding Planning Test Script
Demonstrates the new multi-day optimized birding planning functionality
"""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config.settings import get_settings
from src.core.birding_planner import BirdingPlanner
from src.core.route_service import RouteService


def test_multi_day_planning():
    """Test multi-day birding planning functionality"""
    print("🗺️ Testing Multi-Day Birding Planning")
    print("=" * 60)
    
    try:
        # Initialize services
        settings = get_settings()
        planner = BirdingPlanner(settings)
        route_service = planner.route_service
        
        print("✅ Services initialized successfully")
        
        # Test parameters
        base_location = "New York"
        target_species = ["American Robin", "Northern Cardinal", "Blue Jay", "Red-winged Blackbird", "Common Grackle"]
        date_range = "Spring 2024"
        days = 3
        max_distance_per_day = 30.0  # 30km per day for walking
        
        print(f"\n📋 Test Parameters:")
        print(f"   Base Location: {base_location}")
        print(f"   Target Species: {', '.join(target_species)}")
        print(f"   Date Range: {date_range}")
        print(f"   Days: {days}")
        print(f"   Max Distance per Day: {max_distance_per_day} km")
        print()
        
        # Create multi-day plan
        print("🗺️ Creating multi-day plan...")
        multi_day_plan = route_service.create_multi_day_plan(
            base_location=base_location,
            target_species=target_species,
            date_range=date_range,
            days=days,
            max_distance_per_day=max_distance_per_day
        )
        
        # Display results
        print("\n📊 Multi-Day Plan Results")
        print("=" * 50)
        
        overall_stats = multi_day_plan['overall_stats']
        print(f"🎯 Overall Statistics:")
        print(f"   Total Species Expected: {overall_stats['total_species_expected']}")
        print(f"   Total Distance: {overall_stats['total_distance']:.1f} km")
        print(f"   Average Distance per Day: {overall_stats['average_distance_per_day']:.1f} km")
        print(f"   Overall Success Probability: {overall_stats['overall_success_probability']:.1%}")
        print(f"   Species Coverage: {overall_stats['species_coverage']:.1%}")
        print(f"   Efficiency Score: {overall_stats['efficiency_score']:.1f} species per 10km")
        print()
        
        # Display daily plans
        print("📅 Daily Plans:")
        for day_plan in multi_day_plan['daily_plans']:
            print(f"\n   Day {day_plan['day']}:")
            print(f"     Expected Species: {len(day_plan['expected_species'])}")
            print(f"     Total Distance: {day_plan['total_distance']:.1f} km")
            print(f"     Success Probability: {day_plan['day_success_probability']:.1%}")
            print(f"     Efficiency Score: {day_plan['efficiency_score']:.1f}")
            
            if day_plan['hotspots']:
                print(f"     Hotspots:")
                for i, hotspot_info in enumerate(day_plan['hotspots'], 1):
                    hotspot = hotspot_info['hotspot']
                    distance = hotspot_info['distance_from_previous']
                    unique_species = hotspot_info['unique_species']
                    
                    print(f"       {i}. {hotspot['name']}")
                    if distance > 0:
                        print(f"          Distance: {distance:.1f} km")
                    if unique_species:
                        print(f"          Key species: {', '.join(unique_species[:2])}")
                        if len(unique_species) > 2:
                            print(f"          ... and {len(unique_species) - 2} more")
        
        # Save plan to files
        output_dir = "test_multi_day"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as JSON
        import json
        with open(os.path.join(output_dir, 'multi_day_plan.json'), 'w') as f:
            json.dump(multi_day_plan, f, indent=2, default=str)
        
        # Generate and save markdown
        from src.cli.main import generate_multi_day_markdown
        markdown_content = generate_multi_day_markdown(multi_day_plan)
        with open(os.path.join(output_dir, 'multi_day_plan.md'), 'w') as f:
            f.write(markdown_content)
        
        print(f"\n✅ Multi-day plan saved to {output_dir}/ directory")
        print(f"📁 Files generated:")
        print(f"   - {output_dir}/multi_day_plan.md (Complete plan report)")
        print(f"   - {output_dir}/multi_day_plan.json (Structured data)")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_multi_day_features():
    """Demonstrate multi-day planning features"""
    print("\n🎬 Multi-Day Planning Features Demo")
    print("=" * 60)
    
    print("\n📊 Feature 1: Multi-Day Optimization")
    print("   • Optimizes routes across multiple days")
    print("   • Minimizes total walking distance")
    print("   • Maximizes species diversity")
    print("   • Balances daily schedules")
    
    print("\n🗺️ Feature 2: Distance-Based Planning")
    print("   • Sets maximum walking distance per day")
    print("   • Calculates optimal routes between hotspots")
    print("   • Considers travel time and fatigue")
    print("   • Provides realistic daily schedules")
    
    print("\n🎯 Feature 3: Success Probability Analysis")
    print("   • Calculates daily success probabilities")
    print("   • Shows overall trip success rate")
    print("   • Provides species-specific predictions")
    print("   • Includes confidence levels")
    
    print("\n📈 Feature 4: Efficiency Scoring")
    print("   • Measures species per distance walked")
    print("   • Compares different planning strategies")
    print("   • Optimizes for maximum efficiency")
    print("   • Provides actionable recommendations")
    
    print("\n💡 Benefits of Multi-Day Planning:")
    print("   • More realistic for extended birding trips")
    print("   • Better resource management")
    print("   • Higher success rates through strategic planning")
    print("   • Reduced fatigue and better enjoyment")
    print("   • Comprehensive trip documentation")


def test_different_scenarios():
    """Test different multi-day planning scenarios"""
    print("\n🧪 Testing Different Scenarios")
    print("=" * 60)
    
    settings = get_settings()
    planner = BirdingPlanner(settings)
    route_service = planner.route_service
    
    scenarios = [
        {
            "name": "Short Trip (2 days)",
            "days": 2,
            "species": ["American Robin", "Northern Cardinal"],
            "max_distance": 20.0
        },
        {
            "name": "Medium Trip (3 days)",
            "days": 3,
            "species": ["American Robin", "Northern Cardinal", "Blue Jay", "Red-winged Blackbird"],
            "max_distance": 30.0
        },
        {
            "name": "Long Trip (5 days)",
            "days": 5,
            "species": ["American Robin", "Northern Cardinal", "Blue Jay", "Red-winged Blackbird", 
                       "Common Grackle", "House Sparrow", "European Starling"],
            "max_distance": 40.0
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 Testing: {scenario['name']}")
        print(f"   Days: {scenario['days']}")
        print(f"   Species: {len(scenario['species'])}")
        print(f"   Max Distance: {scenario['max_distance']} km/day")
        
        try:
            plan = route_service.create_multi_day_plan(
                base_location="New York",
                target_species=scenario['species'],
                date_range="Spring 2024",
                days=scenario['days'],
                max_distance_per_day=scenario['max_distance']
            )
            
            stats = plan['overall_stats']
            print(f"   ✅ Results:")
            print(f"      Total Species: {stats['total_species_expected']}")
            print(f"      Total Distance: {stats['total_distance']:.1f} km")
            print(f"      Success Rate: {stats['overall_success_probability']:.1%}")
            print(f"      Efficiency: {stats['efficiency_score']:.1f}")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")


if __name__ == "__main__":
    print("🗺️ Multi-Day Birding Planning Test")
    print("=" * 60)
    
    # Run main test
    success = test_multi_day_planning()
    
    # Show demo
    demo_multi_day_features()
    
    # Test different scenarios
    test_different_scenarios()
    
    if success:
        print("\n🎉 Multi-day planning is working perfectly!")
        print("   This feature optimizes your birding trips for maximum efficiency.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.") 