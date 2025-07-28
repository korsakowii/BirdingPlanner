#!/usr/bin/env python3
"""
Multi-Day Birding Planning Demo
Demonstrates the comprehensive multi-day planning features
"""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config.settings import get_settings
from src.core.birding_planner import BirdingPlanner
from src.core.route_service import RouteService


def demo_multi_day_features():
    """Demonstrate all multi-day planning features"""
    print("🗺️ Multi-Day Birding Planning Demo")
    print("=" * 60)
    
    # Initialize services
    settings = get_settings()
    planner = BirdingPlanner(settings)
    route_service = planner.route_service
    
    print("✅ Services initialized successfully")
    
    # Demo 1: Basic multi-day planning
    print("\n🎯 Demo 1: Basic Multi-Day Planning")
    print("-" * 40)
    
    basic_plan = route_service.create_multi_day_plan(
        base_location="New York",
        target_species=["American Robin", "Northern Cardinal", "Blue Jay"],
        date_range="Spring 2024",
        days=3,
        max_distance_per_day=30.0
    )
    
    print(f"📍 Base Location: {basic_plan['base_location']}")
    print(f"🎯 Target Species: {', '.join(basic_plan['target_species'])}")
    print(f"📅 Total Days: {basic_plan['total_days']}")
    
    overall_stats = basic_plan['overall_stats']
    print(f"📊 Overall Statistics:")
    print(f"   Total Species Expected: {overall_stats['total_species_expected']}")
    print(f"   Total Distance: {overall_stats['total_distance']:.1f} km")
    print(f"   Average Distance per Day: {overall_stats['average_distance_per_day']:.1f} km")
    print(f"   Overall Success Probability: {overall_stats['overall_success_probability']:.1%}")
    print(f"   Species Coverage: {overall_stats['species_coverage']:.1%}")
    print(f"   Efficiency Score: {overall_stats['efficiency_score']:.1f} species per 10km")
    
    # Demo 2: Detailed daily routes
    print("\n🗺️ Demo 2: 每天应该去哪些鸟点 (Daily Hotspot Plan)")
    print("-" * 40)
    
    for day_plan in basic_plan['daily_plans']:
        print(f"\n📅 Day {day_plan['day']}")
        print(f"   计划去的鸟点 (Hotspots to visit):")
        if 'route_stops' in day_plan and day_plan['route_stops']:
            for route_stop in day_plan['route_stops']:
                print(f"     - {route_stop['hotspot_name']} | 时间: {route_stop['viewing_time']} | 目标鸟种: {', '.join(route_stop['target_species'])}")
        else:
            print("     (无推荐鸟点)")
        print(f"   预计可见鸟种: {len(day_plan['expected_species'])}")
        print(f"   总距离: {day_plan['total_distance']:.1f} km")
        print(f"   成功概率: {day_plan['day_success_probability']:.1%}")
        if 'daily_summary' in day_plan:
            print(f"   总结: {day_plan['daily_summary']}")
        print()
    
    # 保留原有详细路线和日程输出
    print("\n🗺️ Demo 2b: 每日详细路线和日程 (Detailed Route & Schedule)")
    print("-" * 40)
    for day_plan in basic_plan['daily_plans']:
        print(f"\n📅 Day {day_plan['day']}")
        if 'route_stops' in day_plan and day_plan['route_stops']:
            print(f"   Detailed Route:")
            for route_stop in day_plan['route_stops']:
                print(f"     Stop {route_stop['stop_number']}: {route_stop['hotspot_name']}")
                print(f"        Time: {route_stop['viewing_time']}")
                print(f"        Distance: {route_stop['distance_from_previous']:.1f} km")
                print(f"        Target Species: {', '.join(route_stop['target_species'])}")
                print(f"        Success Rate: {route_stop['success_probability']:.1%}")
                print(f"        Best Approach: {route_stop['best_approach']}")
                if route_stop['facilities']:
                    print(f"        Facilities: {', '.join(route_stop['facilities'][:2])}")
                if route_stop['recommendations']:
                    print(f"        Tips: {route_stop['recommendations'][0]}")
                print()
        if 'daily_schedule' in day_plan and day_plan['daily_schedule']:
            print(f"   Daily Schedule:")
            for schedule_item in day_plan['daily_schedule']:
                if schedule_item['type'] == 'travel':
                    print(f"     {schedule_item['time']}: {schedule_item['activity']} ({schedule_item['duration']})")
                else:
                    print(f"     {schedule_item['time']}: {schedule_item['activity']} ({schedule_item['duration']})")
                    if schedule_item['target_species']:
                        print(f"        Target: {', '.join(schedule_item['target_species'])}")
        print()
    
    # Demo 3: Different planning scenarios
    print("\n🧪 Demo 3: Different Planning Scenarios")
    print("-" * 40)
    
    scenarios = [
        {
            "name": "Short Trip (2 days, 2 species)",
            "days": 2,
            "species": ["American Robin", "Northern Cardinal"],
            "max_distance": 20.0
        },
        {
            "name": "Medium Trip (3 days, 4 species)",
            "days": 3,
            "species": ["American Robin", "Northern Cardinal", "Blue Jay", "Red-winged Blackbird"],
            "max_distance": 30.0
        },
        {
            "name": "Long Trip (5 days, 7 species)",
            "days": 5,
            "species": ["American Robin", "Northern Cardinal", "Blue Jay", "Red-winged Blackbird", 
                       "Common Grackle", "House Sparrow", "European Starling"],
            "max_distance": 40.0
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 {scenario['name']}")
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
    
    # Demo 4: Save and load plans
    print("\n💾 Demo 4: Save and Load Plans")
    print("-" * 40)
    
    # Save the basic plan
    output_dir = "demo_multi_day"
    os.makedirs(output_dir, exist_ok=True)
    
    import json
    with open(os.path.join(output_dir, 'demo_plan.json'), 'w') as f:
        json.dump(basic_plan, f, indent=2, default=str)
    
    # Generate markdown report
    from src.cli.main import generate_multi_day_markdown
    markdown_content = generate_multi_day_markdown(basic_plan)
    with open(os.path.join(output_dir, 'demo_plan.md'), 'w') as f:
        f.write(markdown_content)
    
    print(f"✅ Demo plan saved to {output_dir}/ directory")
    print(f"📁 Files generated:")
    print(f"   - {output_dir}/demo_plan.md (Complete plan report)")
    print(f"   - {output_dir}/demo_plan.json (Structured data)")
    
    # Demo 5: Feature comparison
    print("\n📊 Demo 5: Feature Comparison")
    print("-" * 40)
    
    print("🎯 Multi-Day Planning Features:")
    print("   ✅ Daily route optimization")
    print("   ✅ Distance-based planning")
    print("   ✅ Success probability analysis")
    print("   ✅ Efficiency scoring")
    print("   ✅ Detailed daily schedules")
    print("   ✅ Hotspot-specific recommendations")
    print("   ✅ Species targeting per hotspot")
    print("   ✅ Travel time calculations")
    print("   ✅ Facility information")
    print("   ✅ Best approach strategies")
    
    print("\n💡 Benefits:")
    print("   • More realistic for extended birding trips")
    print("   • Better resource management")
    print("   • Higher success rates through strategic planning")
    print("   • Reduced fatigue and better enjoyment")
    print("   • Comprehensive trip documentation")
    print("   • Optimized for maximum species diversity")
    print("   • Minimal walking distance")
    print("   • Balanced daily schedules")


def show_usage_examples():
    """Show usage examples for multi-day planning"""
    print("\n📖 Usage Examples")
    print("=" * 60)
    
    print("\n🔧 CLI Usage:")
    print("```bash")
    print("# Basic multi-day planning")
    print("python -m src.cli.main plan \\")
    print("  --species \"American Robin\" \"Northern Cardinal\" \"Blue Jay\" \\")
    print("  --location \"New York\" \\")
    print("  --date \"Spring 2024\" \\")
    print("  --multi-day 3 \\")
    print("  --max-distance-per-day 30 \\")
    print("  --output \"my_trip\"")
    print()
    print("# Optimized efficiency planning")
    print("python -m src.cli.main plan \\")
    print("  --species \"American Robin\" \"Northern Cardinal\" \"Blue Jay\" \\")
    print("  --location \"New York\" \\")
    print("  --date \"Spring 2024\" \\")
    print("  --multi-day 5 \\")
    print("  --max-distance-per-day 25 \\")
    print("  --optimize-efficiency \\")
    print("  --output \"efficient_trip\"")
    print("```")
    
    print("\n🐍 Programmatic Usage:")
    print("```python")
    print("from src.core.route_service import RouteService")
    print("from src.config.settings import get_settings")
    print()
    print("# Initialize service")
    print("settings = get_settings()")
    print("route_service = RouteService()")
    print()
    print("# Create multi-day plan")
    print("plan = route_service.create_multi_day_plan(")
    print("    base_location=\"New York\",")
    print("    target_species=[\"American Robin\", \"Northern Cardinal\", \"Blue Jay\"],")
    print("    date_range=\"Spring 2024\",")
    print("    days=3,")
    print("    max_distance_per_day=30.0")
    print(")")
    print()
    print("# Access plan details")
    print("print(f\"Total species expected: {plan['overall_stats']['total_species_expected']}\")")
    print("print(f\"Total distance: {plan['overall_stats']['total_distance']:.1f} km\")")
    print("print(f\"Success probability: {plan['overall_stats']['overall_success_probability']:.1%}\")")
    print("```")


if __name__ == "__main__":
    print("🗺️ Multi-Day Birding Planning Comprehensive Demo")
    print("=" * 60)
    
    # Run main demo
    demo_multi_day_features()
    
    # Show usage examples
    show_usage_examples()
    
    print("\n🎉 Multi-day planning demo completed!")
    print("   This feature provides comprehensive planning for extended birding trips.")
    print("   Each day includes detailed routes, target species, and optimal timing.") 