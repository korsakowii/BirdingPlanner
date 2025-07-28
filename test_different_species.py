#!/usr/bin/env python3
"""
Test script to demonstrate BirdingPlanner with different species combinations.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'mcp_server'))

from mcp_server.main import generate_complete_trip_plan, save_trip_plan

def test_advanced_species():
    """Test with more challenging species to show tier differences."""
    
    print("🦅 Testing BirdingPlanner with Advanced Species")
    print("=" * 60)
    
    # Test with mixed tier species
    advanced_input = {
        "species": ["Cerulean Warbler", "Baltimore Oriole", "Scarlet Tanager"],
        "location": "New York", 
        "date_range": "Spring 2024"
    }
    
    print(f"Target Species: {advanced_input['species']}")
    print(f"Base Location: {advanced_input['location']}")
    print(f"Date Range: {advanced_input['date_range']}")
    print()
    
    try:
        # Generate complete trip plan
        complete_plan = generate_complete_trip_plan(advanced_input)
        
        if "error" in complete_plan:
            print(f"❌ Error: {complete_plan['error']}")
            return
        
        # Save to files
        save_message = save_trip_plan(complete_plan, "output_advanced")
        print(f"✅ {save_message}")
        
        # Print detailed analysis
        print("\n🎯 Species Tier Analysis:")
        for species_info in complete_plan['species_analysis']['classifications']:
            print(f"   {species_info['species']}: {species_info['tier']}")
            print(f"      Description: {species_info['description']}")
            print(f"      Challenge: {species_info.get('challenge', 'No challenge available')}")
            print()
        
        print("📊 Availability Analysis:")
        for availability in complete_plan['species_analysis']['availability']:
            print(f"   {availability['species']}: {availability['confidence_score']}% confidence")
            print(f"      Recommendation: {availability['recommendation']}")
            print()
        
        print("🗺️ Route Analysis:")
        print(f"   Total Stops: {complete_plan['trip_overview']['total_stops']}")
        print(f"   Total Distance: {complete_plan['trip_overview']['total_distance_km']:.1f} km")
        print(f"   Estimated Time: {complete_plan['trip_overview']['estimated_time']}")
        
        print("\n📍 Route Stops:")
        for stop in complete_plan['route_plan']['route_stops']:
            print(f"   Stop {stop['stop_number']}: {stop['location']}")
            print(f"      Species Compatibility: {stop['species_compatibility']:.2f}")
            print(f"      Best Hotspots: {[h['name'] for h in stop['hotspots']]}")
            print()
        
        print("✨ Advanced species test completed successfully!")
        
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

def test_west_coast_species():
    """Test with West Coast species and location."""
    
    print("\n🦅 Testing BirdingPlanner with West Coast Species")
    print("=" * 60)
    
    west_coast_input = {
        "species": ["Red-tailed Hawk", "American Goldfinch", "Blue Jay"],
        "location": "San Francisco",
        "date_range": "Summer 2024"
    }
    
    print(f"Target Species: {west_coast_input['species']}")
    print(f"Base Location: {west_coast_input['location']}")
    print(f"Date Range: {west_coast_input['date_range']}")
    print()
    
    try:
        # Generate complete trip plan
        complete_plan = generate_complete_trip_plan(west_coast_input)
        
        if "error" in complete_plan:
            print(f"❌ Error: {complete_plan['error']}")
            return
        
        # Save to files
        save_message = save_trip_plan(complete_plan, "output_west_coast")
        print(f"✅ {save_message}")
        
        # Print summary
        print("\n📋 West Coast Trip Summary:")
        print(f"   Base Location: {complete_plan['trip_overview']['base_location']}")
        print(f"   Target Species: {', '.join(complete_plan['trip_overview']['target_species'])}")
        print(f"   Total Stops: {complete_plan['trip_overview']['total_stops']}")
        print(f"   Total Distance: {complete_plan['trip_overview']['total_distance_km']:.1f} km")
        
        print("\n🎯 Species Tiers:")
        for species_info in complete_plan['species_analysis']['classifications']:
            print(f"   {species_info['species']}: {species_info['tier']}")
        
        print("\n✨ West Coast species test completed successfully!")
        
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_advanced_species()
    test_west_coast_species() 