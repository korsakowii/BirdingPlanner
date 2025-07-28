"""
Plans optimal routes for birdwatching based on locations and time.
Optimizes for species diversity, travel efficiency, and viewing conditions.
"""

from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import random
import math

# Mock location database with coordinates and birding hotspots
LOCATION_DATABASE = {
    "New York": {
        "coordinates": (40.7128, -74.0060),
        "region": "Northeast",
        "hotspots": [
            {"name": "Central Park", "coordinates": (40.7829, -73.9654), "species_count": 230},
            {"name": "Jamaica Bay Wildlife Refuge", "coordinates": (40.6157, -73.8257), "species_count": 325},
            {"name": "Prospect Park", "coordinates": (40.6602, -73.9690), "species_count": 200}
        ]
    },
    "Boston": {
        "coordinates": (42.3601, -71.0589),
        "region": "Northeast", 
        "hotspots": [
            {"name": "Mount Auburn Cemetery", "coordinates": (42.3704, -71.1445), "species_count": 180},
            {"name": "Parker River NWR", "coordinates": (42.7483, -70.8167), "species_count": 300},
            {"name": "Boston Common", "coordinates": (42.3554, -71.0655), "species_count": 120}
        ]
    },
    "Chicago": {
        "coordinates": (41.8781, -87.6298),
        "region": "Midwest",
        "hotspots": [
            {"name": "Montrose Point", "coordinates": (41.9664, -87.6328), "species_count": 280},
            {"name": "Jackson Park", "coordinates": (41.7833, -87.5767), "species_count": 200},
            {"name": "North Park Village", "coordinates": (41.9833, -87.7167), "species_count": 150}
        ]
    },
    "Miami": {
        "coordinates": (25.7617, -80.1918),
        "region": "Southeast",
        "hotspots": [
            {"name": "Everglades National Park", "coordinates": (25.2867, -80.9000), "species_count": 350},
            {"name": "Bill Baggs Cape Florida", "coordinates": (25.6658, -80.1589), "species_count": 180},
            {"name": "Matheson Hammock Park", "coordinates": (25.6733, -80.2583), "species_count": 120}
        ]
    },
    "San Francisco": {
        "coordinates": (37.7749, -122.4194),
        "region": "West Coast",
        "hotspots": [
            {"name": "Golden Gate Park", "coordinates": (37.7694, -122.4862), "species_count": 200},
            {"name": "Point Reyes", "coordinates": (38.0697, -122.8069), "species_count": 450},
            {"name": "Crissy Field", "coordinates": (37.8063, -122.4650), "species_count": 150}
        ]
    }
}

# Mock species-location compatibility matrix
SPECIES_LOCATION_MATRIX = {
    "American Robin": {
        "New York": 0.9, "Boston": 0.85, "Chicago": 0.8, "Miami": 0.3, "San Francisco": 0.7
    },
    "Northern Cardinal": {
        "New York": 0.8, "Boston": 0.75, "Chicago": 0.85, "Miami": 0.9, "San Francisco": 0.1
    },
    "Blue Jay": {
        "New York": 0.9, "Boston": 0.85, "Chicago": 0.8, "Miami": 0.2, "San Francisco": 0.1
    },
    "Baltimore Oriole": {
        "New York": 0.7, "Boston": 0.65, "Chicago": 0.8, "Miami": 0.4, "San Francisco": 0.1
    },
    "Scarlet Tanager": {
        "New York": 0.6, "Boston": 0.55, "Chicago": 0.7, "Miami": 0.3, "San Francisco": 0.1
    },
    "Cerulean Warbler": {
        "New York": 0.4, "Boston": 0.35, "Chicago": 0.5, "Miami": 0.2, "San Francisco": 0.1
    }
}

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates using Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def get_species_compatibility_score(species: str, location: str) -> float:
    """
    Get compatibility score between a species and location (0-1).
    """
    if species in SPECIES_LOCATION_MATRIX and location in SPECIES_LOCATION_MATRIX[species]:
        return SPECIES_LOCATION_MATRIX[species][location]
    else:
        # Default score for unknown combinations
        return random.uniform(0.3, 0.7)

def optimize_route(base_location: str, target_species: List[str], date_range: str, max_stops: int = 3) -> Dict:
    """
    Plan an optimized route for birdwatching.
    
    Args:
        base_location: Starting location
        target_species: List of target bird species
        date_range: Date range for the trip
        max_stops: Maximum number of stops (default 3)
    
    Returns:
        Dictionary with optimized route information
    """
    
    if base_location not in LOCATION_DATABASE:
        return {"error": f"Location '{base_location}' not found in database"}
    
    base_coords = LOCATION_DATABASE[base_location]["coordinates"]
    available_locations = list(LOCATION_DATABASE.keys())
    
    # Score each potential location based on species compatibility and distance
    location_scores = []
    
    for location in available_locations:
        if location == base_location:
            continue
            
        location_coords = LOCATION_DATABASE[location]["coordinates"]
        distance = calculate_distance(base_coords[0], base_coords[1], 
                                   location_coords[0], location_coords[1])
        
        # Calculate species compatibility score
        species_scores = []
        for species in target_species:
            compatibility = get_species_compatibility_score(species, location)
            species_scores.append(compatibility)
        
        avg_species_score = sum(species_scores) / len(species_scores) if species_scores else 0
        
        # Combine distance and species compatibility
        # Prefer closer locations with good species compatibility
        distance_penalty = min(distance / 1000, 1.0)  # Normalize distance penalty
        combined_score = avg_species_score * (1 - distance_penalty * 0.3)
        
        location_scores.append({
            "location": location,
            "distance_km": distance,
            "species_compatibility": avg_species_score,
            "combined_score": combined_score,
            "hotspots": LOCATION_DATABASE[location]["hotspots"]
        })
    
    # Sort by combined score and select top locations
    location_scores.sort(key=lambda x: x["combined_score"], reverse=True)
    selected_locations = location_scores[:max_stops]
    
    # Generate route with timing and recommendations
    route = generate_detailed_route(base_location, selected_locations, target_species, date_range)
    
    return route

def generate_detailed_route(base_location: str, selected_locations: List[Dict], 
                          target_species: List[str], date_range: str) -> Dict:
    """
    Generate detailed route with timing, hotspots, and recommendations.
    """
    
    route_stops = []
    total_distance = 0
    previous_location = base_location
    
    for i, location_data in enumerate(selected_locations):
        location = location_data["location"]
        
        # Calculate travel time (assuming 60 km/h average speed)
        travel_time_hours = location_data["distance_km"] / 60
        travel_time_minutes = int(travel_time_hours * 60)
        
        # Select best hotspots for target species
        best_hotspots = select_best_hotspots(location, target_species)
        
        # Generate viewing schedule
        viewing_schedule = generate_viewing_schedule(location, target_species, i + 1)
        
        stop_info = {
            "stop_number": i + 1,
            "location": location,
            "distance_from_previous": location_data["distance_km"],
            "travel_time": f"{travel_time_minutes} minutes",
            "hotspots": best_hotspots,
            "viewing_schedule": viewing_schedule,
            "species_compatibility": location_data["species_compatibility"],
            "recommendations": generate_stop_recommendations(location, target_species)
        }
        
        route_stops.append(stop_info)
        total_distance += location_data["distance_km"]
        previous_location = location
    
    return {
        "base_location": base_location,
        "target_species": target_species,
        "date_range": date_range,
        "total_stops": len(route_stops),
        "total_distance_km": total_distance,
        "estimated_total_time": f"{int(total_distance / 60 + len(route_stops) * 2)} hours",
        "route_stops": route_stops,
        "summary": generate_route_summary(route_stops, target_species)
    }

def select_best_hotspots(location: str, target_species: List[str]) -> List[Dict]:
    """
    Select the best hotspots for target species in a location.
    """
    if location not in LOCATION_DATABASE:
        return []
    
    hotspots = LOCATION_DATABASE[location]["hotspots"]
    
    # Score hotspots based on species count and proximity
    scored_hotspots = []
    for hotspot in hotspots:
        # Simple scoring: higher species count = better hotspot
        score = hotspot["species_count"] / 500  # Normalize to 0-1
        
        scored_hotspots.append({
            "name": hotspot["name"],
            "species_count": hotspot["species_count"],
            "score": score,
            "coordinates": hotspot["coordinates"]
        })
    
    # Return top 2 hotspots
    scored_hotspots.sort(key=lambda x: x["score"], reverse=True)
    return scored_hotspots[:2]

def generate_viewing_schedule(location: str, target_species: List[str], stop_number: int) -> Dict:
    """
    Generate optimal viewing schedule for a location.
    """
    # Mock optimal viewing times based on stop number (simulating different times of day)
    time_slots = [
        {"time": "6:00 AM - 9:00 AM", "activity": "Dawn chorus and early morning activity"},
        {"time": "9:00 AM - 12:00 PM", "activity": "Mid-morning feeding and territorial behavior"},
        {"time": "12:00 PM - 3:00 PM", "activity": "Midday rest period, focus on raptors"},
        {"time": "3:00 PM - 6:00 PM", "activity": "Afternoon feeding and pre-roosting activity"}
    ]
    
    # Select time slot based on stop number
    selected_slot = time_slots[(stop_number - 1) % len(time_slots)]
    
    return {
        "recommended_time": selected_slot["time"],
        "activity_description": selected_slot["activity"],
        "target_species_focus": target_species[:2] if len(target_species) >= 2 else target_species,
        "estimated_duration": "2-3 hours"
    }

def generate_stop_recommendations(location: str, target_species: List[str]) -> List[str]:
    """
    Generate specific recommendations for each stop.
    """
    recommendations = [
        f"Arrive early at {location} for best viewing conditions",
        "Bring binoculars and field guide for species identification",
        "Check local weather conditions before departure",
        "Consider hiring a local guide for rare species"
    ]
    
    # Add species-specific recommendations
    if len(target_species) > 0:
        recommendations.append(f"Focus on {target_species[0]} at this location")
    
    return recommendations

def generate_route_summary(route_stops: List[Dict], target_species: List[str]) -> str:
    """
    Generate a human-readable route summary.
    """
    total_stops = len(route_stops)
    total_distance = sum(stop["distance_from_previous"] for stop in route_stops)
    
    summary = f"This {total_stops}-stop route covers {total_distance:.1f} km and targets {len(target_species)} species: {', '.join(target_species)}. "
    summary += "The route is optimized for species diversity and travel efficiency. "
    summary += f"Estimated total time including travel and birding: {int(total_distance / 60 + total_stops * 2)} hours."
    
    return summary

def plan_route(base_location: str, targets: List[str]) -> List[str]:
    """
    Legacy function for backward compatibility.
    """
    result = optimize_route(base_location, targets, "Spring 2024")
    if "error" in result:
        return ["Error: " + result["error"]]
    
    return [stop["location"] for stop in result["route_stops"]]

# Example usage and testing
if __name__ == "__main__":
    # Test the route planner
    base_location = "New York"
    target_species = ["American Robin", "Northern Cardinal", "Blue Jay"]
    date_range = "April 15-20, 2024"
    
    print(f"Planning route from {base_location} for {target_species}:")
    print("-" * 60)
    
    route = optimize_route(base_location, target_species, date_range)
    
    print(f"Route Summary: {route['summary']}")
    print(f"Total Distance: {route['total_distance_km']:.1f} km")
    print(f"Estimated Time: {route['estimated_total_time']}")
    print("\nDetailed Stops:")
    
    for stop in route['route_stops']:
        print(f"\nStop {stop['stop_number']}: {stop['location']}")
        print(f"  Distance: {stop['distance_from_previous']:.1f} km")
        print(f"  Travel Time: {stop['travel_time']}")
        print(f"  Hotspots: {[h['name'] for h in stop['hotspots']]}")
        print(f"  Viewing Time: {stop['viewing_schedule']['recommended_time']}")
        print(f"  Species Compatibility: {stop['species_compatibility']:.2f}")
