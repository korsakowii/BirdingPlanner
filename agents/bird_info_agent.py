"""
Agent to match bird species to regions and seasons.
Provides comprehensive availability data for birding planning.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random

# Mock eBird-style database with seasonal and regional data
SPECIES_DATABASE = {
    "American Robin": {
        "best_months": ["March", "April", "May", "September", "October"],
        "regions": ["Northeast", "Midwest", "West Coast", "Southeast"],
        "habitat_preferences": ["backyards", "parks", "forests", "meadows"],
        "peak_activity": "dawn",
        "migration_pattern": "partial_migrator",
        "breeding_range": ["Canada", "Northern US"],
        "wintering_range": ["Southern US", "Mexico"],
        "abundance_rating": 5,  # 1-5 scale
        "ease_of_finding": "very_easy"
    },
    "Northern Cardinal": {
        "best_months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "regions": ["Southeast", "Midwest", "Northeast"],
        "habitat_preferences": ["backyards", "woodlands", "thickets"],
        "peak_activity": "dawn_dusk",
        "migration_pattern": "resident",
        "breeding_range": ["Eastern US"],
        "wintering_range": ["Eastern US"],
        "abundance_rating": 5,
        "ease_of_finding": "very_easy"
    },
    "Blue Jay": {
        "best_months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "regions": ["Northeast", "Midwest", "Southeast"],
        "habitat_preferences": ["forests", "parks", "suburban_areas"],
        "peak_activity": "morning",
        "migration_pattern": "partial_migrator",
        "breeding_range": ["Eastern US", "Canada"],
        "wintering_range": ["Eastern US"],
        "abundance_rating": 4,
        "ease_of_finding": "easy"
    },
    "Baltimore Oriole": {
        "best_months": ["April", "May", "June", "July", "August", "September"],
        "regions": ["Northeast", "Midwest", "Southeast"],
        "habitat_preferences": ["forests", "parks", "riversides"],
        "peak_activity": "morning",
        "migration_pattern": "long_distance",
        "breeding_range": ["Eastern US", "Canada"],
        "wintering_range": ["Central America", "Northern South America"],
        "abundance_rating": 3,
        "ease_of_finding": "moderate"
    },
    "Scarlet Tanager": {
        "best_months": ["April", "May", "June", "July", "August", "September"],
        "regions": ["Northeast", "Midwest", "Southeast"],
        "habitat_preferences": ["forests", "woodlands"],
        "peak_activity": "morning",
        "migration_pattern": "long_distance",
        "breeding_range": ["Eastern US", "Canada"],
        "wintering_range": ["South America"],
        "abundance_rating": 2,
        "ease_of_finding": "difficult"
    },
    "Cerulean Warbler": {
        "best_months": ["April", "May", "June", "July", "August", "September"],
        "regions": ["Northeast", "Midwest", "Southeast"],
        "habitat_preferences": ["forests", "canopy"],
        "peak_activity": "morning",
        "migration_pattern": "long_distance",
        "breeding_range": ["Eastern US"],
        "wintering_range": ["South America"],
        "abundance_rating": 1,
        "ease_of_finding": "very_difficult"
    },
    "Red-tailed Hawk": {
        "best_months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "regions": ["All Regions"],
        "habitat_preferences": ["open_areas", "highways", "fields"],
        "peak_activity": "daytime",
        "migration_pattern": "partial_migrator",
        "breeding_range": ["North America"],
        "wintering_range": ["North America"],
        "abundance_rating": 4,
        "ease_of_finding": "easy"
    },
    "American Goldfinch": {
        "best_months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "regions": ["Northeast", "Midwest", "West Coast"],
        "habitat_preferences": ["meadows", "backyards", "fields"],
        "peak_activity": "morning",
        "migration_pattern": "short_distance",
        "breeding_range": ["Northern US", "Canada"],
        "wintering_range": ["Southern US"],
        "abundance_rating": 3,
        "ease_of_finding": "moderate"
    }
}

def get_species_availability(species_name: str) -> Dict:
    """
    Get comprehensive availability data for a species.
    Returns best months, regions, and additional planning information.
    """
    if species_name in SPECIES_DATABASE:
        return SPECIES_DATABASE[species_name]
    else:
        # Generate mock data for unknown species
        return generate_mock_species_data(species_name)

def generate_mock_species_data(species_name: str) -> Dict:
    """
    Generate realistic mock data for species not in the database.
    """
    # Random seasonal patterns
    seasonal_patterns = [
        ["March", "April", "May", "June", "July", "August", "September"],  # Spring/Summer
        ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],  # Year-round
        ["September", "October", "November", "December", "January", "February"],  # Fall/Winter
        ["April", "May", "June", "July", "August"]  # Summer only
    ]
    
    regions = ["Northeast", "Midwest", "Southeast", "West Coast", "Southwest"]
    habitats = ["forests", "meadows", "wetlands", "backyards", "parks", "coastal"]
    
    return {
        "best_months": random.choice(seasonal_patterns),
        "regions": random.sample(regions, random.randint(1, 3)),
        "habitat_preferences": random.sample(habitats, random.randint(1, 3)),
        "peak_activity": random.choice(["dawn", "morning", "afternoon", "dusk", "night"]),
        "migration_pattern": random.choice(["resident", "short_distance", "long_distance", "partial_migrator"]),
        "breeding_range": ["Mock Range"],
        "wintering_range": ["Mock Range"],
        "abundance_rating": random.randint(1, 5),
        "ease_of_finding": random.choice(["very_easy", "easy", "moderate", "difficult", "very_difficult"])
    }

def get_optimal_viewing_times(species_name: str, month: str) -> Dict:
    """
    Get optimal viewing times for a species in a specific month.
    """
    species_data = get_species_availability(species_name)
    
    if month in species_data["best_months"]:
        peak_activity = species_data["peak_activity"]
        
        # Convert activity time to specific hours
        time_mappings = {
            "dawn": "5:00 AM - 7:00 AM",
            "morning": "6:00 AM - 10:00 AM", 
            "afternoon": "10:00 AM - 4:00 PM",
            "dusk": "5:00 PM - 7:00 PM",
            "night": "8:00 PM - 11:00 PM"
        }
        
        return {
            "optimal_hours": time_mappings.get(peak_activity, "6:00 AM - 10:00 AM"),
            "peak_activity": peak_activity,
            "recommendation": f"Best viewed during {peak_activity} hours in {month}"
        }
    else:
        return {
            "optimal_hours": "Not typically seen in this month",
            "peak_activity": "unknown",
            "recommendation": f"{species_name} is not typically active in {month}"
        }

def get_regional_hotspots(species_name: str, region: str) -> List[str]:
    """
    Get recommended hotspots for a species in a specific region.
    """
    species_data = get_species_availability(species_name)
    
    if region not in species_data["regions"]:
        return [f"No specific hotspots known for {species_name} in {region}"]
    
    # Mock hotspot database
    hotspot_database = {
        "Northeast": ["Central Park, NY", "Acadia National Park, ME", "Cape May, NJ"],
        "Midwest": ["Point Pelee, ON", "Horicon Marsh, WI", "Crane Trust, NE"],
        "Southeast": ["Everglades NP, FL", "Great Smoky Mountains, TN", "Okefenokee Swamp, GA"],
        "West Coast": ["Point Reyes, CA", "Malheur NWR, OR", "Skagit Valley, WA"],
        "Southwest": ["Bosque del Apache, NM", "Big Bend NP, TX", "Saguaro NP, AZ"]
    }
    
    return hotspot_database.get(region, ["Local parks and natural areas"])

def get_species_planning_summary(species_name: str, target_month: str, target_region: str) -> Dict:
    """
    Get a comprehensive planning summary for a species.
    """
    availability = get_species_availability(species_name)
    viewing_times = get_optimal_viewing_times(species_name, target_month)
    hotspots = get_regional_hotspots(species_name, target_region)
    
    # Determine if this is a good time/place for the species
    is_good_time = target_month in availability["best_months"]
    is_good_region = target_region in availability["regions"]
    
    confidence_score = 0
    if is_good_time:
        confidence_score += 50
    if is_good_region:
        confidence_score += 50
    
    return {
        "species": species_name,
        "target_month": target_month,
        "target_region": target_region,
        "availability": availability,
        "viewing_times": viewing_times,
        "hotspots": hotspots,
        "confidence_score": confidence_score,
        "recommendation": generate_recommendation(is_good_time, is_good_region, species_name, target_month, target_region)
    }

def generate_recommendation(is_good_time: bool, is_good_region: bool, species: str, month: str, region: str) -> str:
    """
    Generate a human-readable recommendation.
    """
    if is_good_time and is_good_region:
        return f"Excellent timing! {species} is commonly found in {region} during {month}. Plan your trip with confidence."
    elif is_good_time and not is_good_region:
        return f"Good timing but challenging location. {species} is active in {month} but less common in {region}. Consider nearby regions."
    elif not is_good_time and is_good_region:
        return f"Good location but poor timing. {species} is found in {region} but rarely seen in {month}. Consider different months."
    else:
        return f"Challenging combination. {species} is not typically found in {region} during {month}. Consider alternative species or locations."

# Example usage and testing
if __name__ == "__main__":
    # Test the functions
    test_species = "American Robin"
    test_month = "April"
    test_region = "Northeast"
    
    print(f"Testing {test_species} in {test_region} during {test_month}:")
    print("-" * 50)
    
    summary = get_species_planning_summary(test_species, test_month, test_region)
    
    print(f"Availability: {summary['availability']['best_months']}")
    print(f"Regions: {summary['availability']['regions']}")
    print(f"Optimal Hours: {summary['viewing_times']['optimal_hours']}")
    print(f"Hotspots: {summary['hotspots']}")
    print(f"Confidence Score: {summary['confidence_score']}%")
    print(f"Recommendation: {summary['recommendation']}")
