"""
Generates narrative logbooks and social content from birding results.
Creates engaging stories, trip plans, and social media content.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random

# Story templates and narrative elements
STORY_TEMPLATES = {
    "discovery": [
        "As the first light painted the sky, I found myself standing in {location}, binoculars in hand and hope in heart. The morning chorus was just beginning, and I was searching for {species}.",
        "The crisp morning air carried the promise of new discoveries as I ventured into {location}. Today's mission: to encounter the elusive {species} in its natural habitat.",
        "With camera ready and field guide open, I set out to {location} where {species} had been reported. The anticipation of a rare sighting filled the air."
    ],
    "encounter": [
        "Suddenly, there it was! A flash of {color} caught my eye, and I held my breath as the {species} revealed itself, perfectly framed against the morning sky.",
        "The distinctive call of the {species} echoed through {location}, and moments later, I spotted it perched majestically on a {perch_type}.",
        "Through my binoculars, I watched in awe as the {species} went about its morning routine, completely unaware of my presence. It was a moment of pure connection with nature."
    ],
    "reflection": [
        "This encounter with the {species} reminded me why I love birding - it's not just about the checklist, but about these intimate moments with wild creatures.",
        "As I watched the {species} disappear into the landscape, I felt grateful for this brief window into its world. These are the moments that make every early morning worthwhile.",
        "The {species} may be common to some, but to me, each sighting is unique and precious. It's these simple connections that keep me coming back to {location}."
    ]
}

# Color and habitat descriptions
SPECIES_DESCRIPTIONS = {
    "American Robin": {
        "color": "rusty orange",
        "perch_type": "low branch",
        "behavior": "hopping across the lawn",
        "call": "cheerful song",
        "personality": "friendly and approachable"
    },
    "Northern Cardinal": {
        "color": "brilliant red",
        "perch_type": "tree branch",
        "behavior": "singing from a prominent perch",
        "call": "clear whistled song",
        "personality": "bold and territorial"
    },
    "Blue Jay": {
        "color": "vibrant blue",
        "perch_type": "oak branch",
        "behavior": "acrobatically foraging",
        "call": "loud jay-jay call",
        "personality": "intelligent and curious"
    },
    "Baltimore Oriole": {
        "color": "flame orange",
        "perch_type": "high canopy",
        "behavior": "weaving its hanging nest",
        "call": "flute-like song",
        "personality": "elusive but melodious"
    },
    "Scarlet Tanager": {
        "color": "scarlet red",
        "perch_type": "forest canopy",
        "behavior": "methodically searching for insects",
        "call": "hoarse robin-like song",
        "personality": "shy and canopy-dwelling"
    },
    "Cerulean Warbler": {
        "color": "sky blue",
        "perch_type": "high treetop",
        "behavior": "actively gleaning insects",
        "call": "buzzy ascending song",
        "personality": "elusive and high-canopy"
    }
}

def generate_story_card(species: str, location: str) -> str:
    """
    Generate a natural-style birding story for a species encounter.
    """
    # Get species description or create default
    species_desc = SPECIES_DESCRIPTIONS.get(species, {
        "color": "beautiful",
        "perch_type": "nearby branch",
        "behavior": "going about its daily routine",
        "call": "distinctive song",
        "personality": "wild and free"
    })
    
    # Select story elements
    discovery = random.choice(STORY_TEMPLATES["discovery"]).format(
        location=location, 
        species=species
    )
    
    encounter = random.choice(STORY_TEMPLATES["encounter"]).format(
        color=species_desc["color"],
        species=species,
        location=location,
        perch_type=species_desc["perch_type"]
    )
    
    reflection = random.choice(STORY_TEMPLATES["reflection"]).format(
        species=species,
        location=location
    )
    
    # Combine into a complete story
    story = f"{discovery}\n\n{encounter}\n\n{reflection}"
    
    return story

def generate_trip_plan_markdown(route_data: Dict, species_data: List[Dict]) -> str:
    """
    Generate a comprehensive Markdown trip plan.
    """
    markdown = f"""# Birding Trip Plan: {route_data['target_species'][0]} & Friends

## Trip Overview
- **Date Range**: {route_data['date_range']}
- **Base Location**: {route_data['base_location']}
- **Target Species**: {', '.join(route_data['target_species'])}
- **Total Distance**: {route_data['total_distance_km']:.1f} km
- **Estimated Time**: {route_data['estimated_total_time']}

## Route Summary
{route_data['summary']}

## Detailed Itinerary

"""
    
    for stop in route_data['route_stops']:
        markdown += f"""### Stop {stop['stop_number']}: {stop['location']}

**Travel Details:**
- Distance from previous: {stop['distance_from_previous']:.1f} km
- Travel time: {stop['travel_time']}
- Species compatibility: {stop['species_compatibility']:.2f}

**Recommended Hotspots:**
"""
        for hotspot in stop['hotspots']:
            markdown += f"- **{hotspot['name']}** ({hotspot['species_count']} species)\n"
        
        markdown += f"""
**Viewing Schedule:**
- Optimal time: {stop['viewing_schedule']['recommended_time']}
- Activity: {stop['viewing_schedule']['activity_description']}
- Focus species: {', '.join(stop['viewing_schedule']['target_species_focus'])}
- Duration: {stop['viewing_schedule']['estimated_duration']}

**Recommendations:**
"""
        for rec in stop['recommendations']:
            markdown += f"- {rec}\n"
        
        markdown += "\n---\n\n"
    
    # Add species information
    markdown += "## Target Species Information\n\n"
    for species_info in species_data:
        markdown += f"""### {species_info['species']} - {species_info['tier']}

**Description:** {species_info['description']}

**Best Viewing:**
- Optimal hours: {species_info.get('viewing_times', {}).get('optimal_hours', 'Unknown')}
- Peak activity: {species_info.get('availability', {}).get('peak_activity', 'Unknown')}

**Challenge:** {species_info.get('challenge', 'No specific challenge available')}

---
"""
    
    markdown += """
## Packing List
- Binoculars (8x42 or 10x42 recommended)
- Field guide or birding app
- Camera with telephoto lens (optional)
- Comfortable walking shoes
- Weather-appropriate clothing
- Water and snacks
- Notebook for observations

## Tips for Success
- Arrive early for best viewing conditions
- Move slowly and quietly
- Listen for bird calls and songs
- Be patient - good sightings take time
- Respect wildlife and their habitat
- Share your sightings with the birding community

## Post-Trip Notes
*Use this space to record your observations, photos, and memorable moments from your birding adventure.*

---
*Generated by BirdingPlanner - Your AI-powered birding companion*
"""
    
    return markdown

def generate_social_caption(species: str, location: str, tier: str, encounter_type: str = "sighting") -> str:
    """
    Generate engaging social media captions for birding encounters.
    """
    species_desc = SPECIES_DESCRIPTIONS.get(species, {
        "color": "beautiful",
        "personality": "amazing",
        "call": "distinctive song"
    })
    
    caption_templates = [
        f"🎯 Mission accomplished! Spotted this {species_desc['color']} {species} at {location}. Every {encounter_type} is a reminder of nature's beauty. #{species.replace(' ', '')} #Birding #Nature",
        
        f"🌅 Early morning magic at {location}! This {species} was the highlight of today's birding adventure. The {species_desc['call']} filled the air with pure joy. #BirdingLife #{species.replace(' ', '')}",
        
        f"📸 Patience pays off! After hours of searching, this {species} finally revealed itself at {location}. Tier {tier} species - {encounter_type} of a lifetime! #BirdPhotography #Wildlife",
        
        f"🦅 Nature's masterpiece at {location}! This {species} embodies everything I love about birding - beauty, grace, and the thrill of discovery. #{species.replace(' ', '')} #BirdingAdventures",
        
        f"✨ Sometimes the best moments are the quiet ones. This {species} at {location} reminded me why I wake up before dawn. Pure magic! #Birding #NaturePhotography #{species.replace(' ', '')}"
    ]
    
    return random.choice(caption_templates)

def generate_observation_log(species: str, location: str, date: str, weather: str = "Clear") -> str:
    """
    Generate a detailed observation log entry.
    """
    species_desc = SPECIES_DESCRIPTIONS.get(species, {
        "behavior": "observed",
        "call": "heard",
        "personality": "wild"
    })
    
    log_entry = f"""## Observation Log - {date}

**Species:** {species}
**Location:** {location}
**Date:** {date}
**Weather:** {weather}
**Time:** {random.choice(['6:30 AM', '7:15 AM', '8:00 AM', '9:30 AM'])}
**Duration:** {random.randint(5, 45)} minutes

**Observations:**
- {species_desc['behavior']} in {random.choice(['open area', 'forest edge', 'canopy', 'understory'])}
- {species_desc['call']} {random.choice(['frequently', 'occasionally', 'continuously'])}
- Behavior: {random.choice(['foraging', 'singing', 'preening', 'flying between perches', 'feeding young'])}
- Distance: {random.randint(10, 100)} meters
- Lighting: {random.choice(['excellent', 'good', 'fair', 'challenging'])}

**Notes:**
{generate_story_card(species, location)}

**Equipment Used:**
- Binoculars: {random.choice(['8x42', '10x42', '8x32'])}
- Camera: {random.choice(['iPhone', 'DSLR with 300mm lens', 'Point and shoot', 'None'])}
- Field Guide: {random.choice(['Sibley', 'Peterson', 'Merlin App', 'None needed'])}

**Rating:** {random.randint(3, 5)}/5 stars
**Would return:** {random.choice(['Yes', 'Definitely', 'Maybe', 'No - too crowded'])}
"""
    
    return log_entry

def generate_birding_journal_entry(trip_data: Dict, highlights: List[str]) -> str:
    """
    Generate a comprehensive journal entry for a birding trip.
    """
    journal_entry = f"""# Birding Journal Entry - {trip_data['date_range']}

## Trip Summary
Today's adventure took me from {trip_data['base_location']} to {len(trip_data['route_stops'])} different locations in search of {len(trip_data['target_species'])} target species. The weather was cooperative, and the birds were active.

## Target Species Status
"""
    
    for species in trip_data['target_species']:
        status = random.choice(['✅ Seen', '❌ Missed', '🔄 Partial view', '🎵 Heard only'])
        journal_entry += f"- **{species}**: {status}\n"
    
    journal_entry += f"""
## Route Highlights
"""
    
    for stop in trip_data['route_stops']:
        journal_entry += f"""
### {stop['location']}
{random.choice(highlights)}
- Best hotspot: {stop['hotspots'][0]['name'] if stop['hotspots'] else 'Local area'}
- Time spent: {stop['viewing_schedule']['estimated_duration']}
- Weather conditions: {random.choice(['Perfect', 'Good', 'Challenging', 'Windy'])}
"""
    
    journal_entry += f"""
## Memorable Moments
{random.choice(highlights)}

## Lessons Learned
- {random.choice(['Patience is key', 'Early bird gets the worm', 'Always check the weather', 'Local knowledge is invaluable'])}
- {random.choice(['Bring extra batteries', 'Pack light but be prepared', 'Listen more than look', 'Document everything'])}
- {random.choice(['Join local birding groups', 'Use multiple field guides', 'Practice bird calls', 'Respect wildlife boundaries'])}

## Next Time
- Return to {random.choice([stop['location'] for stop in trip_data['route_stops']])} for better light
- Try different time of day for {random.choice(trip_data['target_species'])}
- Bring {random.choice(['better camera', 'recording equipment', 'more patience', 'local guide'])}
- Explore {random.choice(['nearby wetlands', 'forest trails', 'coastal areas', 'mountain habitats'])}

---
*Birding is not just about the birds, but about the journey, the places, and the people we meet along the way.*
"""
    
    return journal_entry

# Example usage and testing
if __name__ == "__main__":
    # Test story generation
    print("=== Story Card Test ===")
    story = generate_story_card("American Robin", "Central Park")
    print(story)
    print("\n" + "="*50 + "\n")
    
    # Test social caption
    print("=== Social Caption Test ===")
    caption = generate_social_caption("Northern Cardinal", "Backyard", "T2", "sighting")
    print(caption)
    print("\n" + "="*50 + "\n")
    
    # Test observation log
    print("=== Observation Log Test ===")
    log = generate_observation_log("Blue Jay", "Prospect Park", "2024-04-15")
    print(log)
