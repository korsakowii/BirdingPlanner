"""
Classifies bird species into tiers based on commonness and visibility.
Tier System:
T1: Common Companion (Very common, easy to spot)
T2: Regional Companion (Common in specific regions)
T3: Seasonal Visitor (Appears during specific seasons)
T4: Elusive Explorer (Rare, requires specific conditions)
T5: Legendary Quest (Very rare, special sightings)
"""

import random
from typing import Dict, List, Tuple

# Mock bird database with occurrence data
BIRD_DATABASE = {
    "American Robin": {
        "occurrence_rate": 0.85,  # 85% chance of sighting
        "region_count": 48,       # Found in 48 states
        "visibility": "high",     # Easy to spot
        "habitat": ["backyards", "parks", "forests"],
        "seasonality": "year-round"
    },
    "Northern Cardinal": {
        "occurrence_rate": 0.78,
        "region_count": 35,
        "visibility": "high",
        "habitat": ["backyards", "woodlands"],
        "seasonality": "year-round"
    },
    "Blue Jay": {
        "occurrence_rate": 0.72,
        "region_count": 42,
        "visibility": "high",
        "habitat": ["forests", "parks"],
        "seasonality": "year-round"
    },
    "Red-tailed Hawk": {
        "occurrence_rate": 0.65,
        "region_count": 50,
        "visibility": "medium",
        "habitat": ["open areas", "highways"],
        "seasonality": "year-round"
    },
    "American Goldfinch": {
        "occurrence_rate": 0.58,
        "region_count": 40,
        "visibility": "medium",
        "habitat": ["meadows", "backyards"],
        "seasonality": "year-round"
    },
    "Baltimore Oriole": {
        "occurrence_rate": 0.45,
        "region_count": 25,
        "visibility": "medium",
        "habitat": ["forests", "parks"],
        "seasonality": "spring-summer"
    },
    "Scarlet Tanager": {
        "occurrence_rate": 0.35,
        "region_count": 30,
        "visibility": "medium",
        "habitat": ["forests"],
        "seasonality": "spring-summer"
    },
    "Cerulean Warbler": {
        "occurrence_rate": 0.25,
        "region_count": 20,
        "visibility": "low",
        "habitat": ["forests"],
        "seasonality": "spring-summer"
    },
    "Kirtland's Warbler": {
        "occurrence_rate": 0.08,
        "region_count": 3,
        "visibility": "low",
        "habitat": ["young jack pine forests"],
        "seasonality": "spring-summer"
    },
    "Ivory-billed Woodpecker": {
        "occurrence_rate": 0.001,
        "region_count": 1,
        "visibility": "very_low",
        "habitat": ["swamps"],
        "seasonality": "unknown"
    }
}

def calculate_tier_score(occurrence_rate: float, region_count: int, visibility: str) -> float:
    """
    Calculate a numerical score for tier classification.
    Higher scores = higher tiers (more common/easy to find)
    """
    # Convert visibility to numerical value
    visibility_scores = {
        "very_low": 0.2,
        "low": 0.4,
        "medium": 0.7,
        "high": 1.0
    }
    
    visibility_score = visibility_scores.get(visibility, 0.5)
    
    # Normalize region count (max 50 states)
    region_score = min(region_count / 50.0, 1.0)
    
    # Weighted combination
    final_score = (occurrence_rate * 0.5) + (region_score * 0.3) + (visibility_score * 0.2)
    return final_score

def classify_species(species_data: Dict) -> str:
    """
    Classify a species into T1-T5 tier based on its data.
    """
    occurrence_rate = species_data.get("occurrence_rate", 0.5)
    region_count = species_data.get("region_count", 25)
    visibility = species_data.get("visibility", "medium")
    
    score = calculate_tier_score(occurrence_rate, region_count, visibility)
    
    # Tier thresholds
    if score >= 0.8:
        return "T1"  # Common Companion
    elif score >= 0.6:
        return "T2"  # Regional Companion
    elif score >= 0.4:
        return "T3"  # Seasonal Visitor
    elif score >= 0.2:
        return "T4"  # Elusive Explorer
    else:
        return "T5"  # Legendary Quest

def get_tier_description(tier: str) -> str:
    """
    Get human-readable description for each tier.
    """
    tier_descriptions = {
        "T1": "Common Companion - Very common, easy to spot in most areas",
        "T2": "Regional Companion - Common in specific regions, moderate difficulty",
        "T3": "Seasonal Visitor - Appears during specific seasons, requires timing",
        "T4": "Elusive Explorer - Rare, requires specific conditions and patience",
        "T5": "Legendary Quest - Very rare, special sightings that become memorable stories"
    }
    return tier_descriptions.get(tier, "Unknown tier")

def classify_species_by_name(species_name: str) -> Dict:
    """
    Classify a species by name using the database.
    """
    if species_name in BIRD_DATABASE:
        species_data = BIRD_DATABASE[species_name]
        tier = classify_species(species_data)
        return {
            "species": species_name,
            "tier": tier,
            "description": get_tier_description(tier),
            "data": species_data
        }
    else:
        # For unknown species, generate mock data
        mock_data = {
            "occurrence_rate": random.uniform(0.1, 0.8),
            "region_count": random.randint(5, 45),
            "visibility": random.choice(["low", "medium", "high"]),
            "habitat": ["unknown"],
            "seasonality": "unknown"
        }
        tier = classify_species(mock_data)
        return {
            "species": species_name,
            "tier": tier,
            "description": get_tier_description(tier),
            "data": mock_data
        }

def get_tier_challenge(tier: str) -> str:
    """
    Get a personalized challenge for each tier level.
    """
    challenges = {
        "T1": "Perfect for beginners! Focus on learning identification features and behavior patterns.",
        "T2": "Great for building confidence! Practice with different lighting conditions and distances.",
        "T3": "Timing is key! Research migration patterns and optimal viewing windows.",
        "T4": "Patience and persistence required! Study habitat preferences and vocalizations.",
        "T5": "The ultimate birding achievement! Document everything and share your story with the community."
    }
    return challenges.get(tier, "Unknown challenge level")

# Example usage and testing
if __name__ == "__main__":
    # Test with known species
    test_species = ["American Robin", "Cerulean Warbler", "Ivory-billed Woodpecker"]
    
    for species in test_species:
        result = classify_species_by_name(species)
        print(f"{species}: {result['tier']} - {result['description']}")
        print(f"Challenge: {get_tier_challenge(result['tier'])}")
        print()
