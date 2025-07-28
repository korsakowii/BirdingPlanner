"""
Main controller for Birding Planner MCP Server
Orchestrates all modules to create comprehensive birding trip plans.
"""

import sys
import os
from typing import Dict, List, Optional
from datetime import datetime

# Add the agents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

# Import all agent modules
from bird_info_agent import get_species_planning_summary, get_species_availability
from tier_classifier import classify_species_by_name, get_tier_challenge
from route_planner import optimize_route
from content_writer import generate_trip_plan_markdown, generate_story_card, generate_social_caption

def parse_user_input(user_input: Dict) -> Dict:
    """
    Parse and validate user input for birding trip planning.
    """
    # Extract and validate required fields
    species = user_input.get("species", [])
    base_location = user_input.get("location", "New York")
    date_range = user_input.get("date_range", "Spring 2024")
    
    # Validate species list
    if not species or not isinstance(species, list):
        species = ["American Robin", "Northern Cardinal", "Blue Jay"]
    
    # Validate location
    valid_locations = ["New York", "Boston", "Chicago", "Miami", "San Francisco"]
    if base_location not in valid_locations:
        base_location = "New York"
    
    return {
        "species": species,
        "base_location": base_location,
        "date_range": date_range
    }

def generate_complete_trip_plan(user_input: Dict) -> Dict:
    """
    Generate a complete birding trip plan using all modules.
    """
    # Parse user input
    parsed_input = parse_user_input(user_input)
    
    print(f"Planning birding trip for {parsed_input['species']} from {parsed_input['base_location']}")
    print("=" * 60)
    
    # Step 1: Classify species into tiers
    print("1. Classifying species into tiers...")
    species_data = []
    for species in parsed_input['species']:
        classification = classify_species_by_name(species)
        species_data.append(classification)
        print(f"   {species}: {classification['tier']} - {classification['description']}")
    
    # Step 2: Get species availability and planning data
    print("\n2. Analyzing species availability...")
    species_availability = []
    for species in parsed_input['species']:
        # Extract month from date range for availability check
        month = extract_month_from_date_range(parsed_input['date_range'])
        region = get_region_from_location(parsed_input['base_location'])
        
        availability = get_species_planning_summary(species, month, region)
        species_availability.append(availability)
        print(f"   {species}: {availability['confidence_score']}% confidence in {region} during {month}")
    
    # Step 3: Plan optimized route
    print("\n3. Planning optimized route...")
    route_data = optimize_route(
        parsed_input['base_location'],
        parsed_input['species'],
        parsed_input['date_range']
    )
    
    if "error" in route_data:
        print(f"   Error: {route_data['error']}")
        return {"error": route_data["error"]}
    
    print(f"   Route planned: {route_data['total_stops']} stops, {route_data['total_distance_km']:.1f} km")
    
    # Step 4: Generate content
    print("\n4. Generating trip content...")
    
    # Generate Markdown trip plan
    trip_plan_markdown = generate_trip_plan_markdown(route_data, species_data)
    
    # Generate story cards for each species
    story_cards = []
    for species in parsed_input['species']:
        story = generate_story_card(species, parsed_input['base_location'])
        story_cards.append({
            "species": species,
            "story": story
        })
    
    # Generate social media captions
    social_captions = []
    for species_info in species_data:
        caption = generate_social_caption(
            species_info['species'],
            parsed_input['base_location'],
            species_info['tier']
        )
        social_captions.append({
            "species": species_info['species'],
            "tier": species_info['tier'],
            "caption": caption
        })
    
    print("   Content generated successfully!")
    
    # Step 5: Compile complete plan
    complete_plan = {
        "trip_overview": {
            "base_location": parsed_input['base_location'],
            "target_species": parsed_input['species'],
            "date_range": parsed_input['date_range'],
            "total_stops": route_data['total_stops'],
            "total_distance_km": route_data['total_distance_km'],
            "estimated_time": route_data['estimated_total_time']
        },
        "species_analysis": {
            "classifications": species_data,
            "availability": species_availability
        },
        "route_plan": route_data,
        "content": {
            "trip_plan_markdown": trip_plan_markdown,
            "story_cards": story_cards,
            "social_captions": social_captions
        }
    }
    
    return complete_plan

def extract_month_from_date_range(date_range: str) -> str:
    """
    Extract month from date range string.
    """
    month_mapping = {
        "spring": "April",
        "summer": "July", 
        "fall": "October",
        "winter": "January",
        "Spring": "April",
        "Summer": "July",
        "Fall": "October", 
        "Winter": "January"
    }
    
    for season, month in month_mapping.items():
        if season in date_range:
            return month
    
    # Default to April if no season found
    return "April"

def get_region_from_location(location: str) -> str:
    """
    Map location to region for species availability.
    """
    region_mapping = {
        "New York": "Northeast",
        "Boston": "Northeast", 
        "Chicago": "Midwest",
        "Miami": "Southeast",
        "San Francisco": "West Coast"
    }
    
    return region_mapping.get(location, "Northeast")

def save_trip_plan(complete_plan: Dict, output_dir: str = "output") -> str:
    """
    Save the complete trip plan to files.
    """
    import os
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save main trip plan
    trip_plan_path = os.path.join(output_dir, "trip_plan.md")
    with open(trip_plan_path, 'w', encoding='utf-8') as f:
        f.write(complete_plan['content']['trip_plan_markdown'])
    
    # Save story cards
    story_cards_dir = os.path.join(output_dir, "story_cards")
    os.makedirs(story_cards_dir, exist_ok=True)
    
    for i, story_card in enumerate(complete_plan['content']['story_cards']):
        story_path = os.path.join(story_cards_dir, f"story_{i+1:02d}_{story_card['species'].replace(' ', '_')}.txt")
        with open(story_path, 'w', encoding='utf-8') as f:
            f.write(f"Species: {story_card['species']}\n")
            f.write(f"Location: {complete_plan['trip_overview']['base_location']}\n")
            f.write(f"Date: {complete_plan['trip_overview']['date_range']}\n")
            f.write("\n" + "="*50 + "\n\n")
            f.write(story_card['story'])
    
    # Save social captions
    captions_path = os.path.join(output_dir, "social_captions.txt")
    with open(captions_path, 'w', encoding='utf-8') as f:
        f.write("Social Media Captions\n")
        f.write("=" * 30 + "\n\n")
        for caption_data in complete_plan['content']['social_captions']:
            f.write(f"Species: {caption_data['species']} (Tier {caption_data['tier']})\n")
            f.write(f"Caption: {caption_data['caption']}\n")
            f.write("\n" + "-"*50 + "\n\n")
    
    return f"Trip plan saved to {output_dir}/ directory"

def run_planner():
    """
    Main entry point for the Birding Planner.
    """
    print("🦅 Welcome to BirdingPlanner!")
    print("Your AI-powered birding trip companion")
    print("=" * 50)
    
    # Example user input
    example_input = {
        "species": ["American Robin", "Northern Cardinal", "Blue Jay"],
        "location": "New York",
        "date_range": "Spring 2024"
    }
    
    try:
        # Generate complete trip plan
        complete_plan = generate_complete_trip_plan(example_input)
        
        if "error" in complete_plan:
            print(f"❌ Error: {complete_plan['error']}")
            return
        
        # Save to files
        save_message = save_trip_plan(complete_plan)
        print(f"\n✅ {save_message}")
        
        # Print summary
        print("\n📋 Trip Plan Summary:")
        print(f"   Base Location: {complete_plan['trip_overview']['base_location']}")
        print(f"   Target Species: {', '.join(complete_plan['trip_overview']['target_species'])}")
        print(f"   Total Stops: {complete_plan['trip_overview']['total_stops']}")
        print(f"   Total Distance: {complete_plan['trip_overview']['total_distance_km']:.1f} km")
        print(f"   Estimated Time: {complete_plan['trip_overview']['estimated_time']}")
        
        print("\n🎯 Species Tiers:")
        for species_info in complete_plan['species_analysis']['classifications']:
            print(f"   {species_info['species']}: {species_info['tier']}")
        
        print("\n📁 Generated Files:")
        print("   - output/trip_plan.md (Complete trip plan)")
        print("   - output/story_cards/ (Individual story cards)")
        print("   - output/social_captions.txt (Social media content)")
        
        print("\n✨ Your birding adventure awaits! Happy birding!")
        
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_planner()
