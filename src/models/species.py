"""
Species data models for BirdingPlanner.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Set
from datetime import datetime


class SpeciesTier(Enum):
    """Tier classification for bird species difficulty."""
    COMMON_COMPANION = "T1"      # Very common, easy to spot
    REGIONAL_COMPANION = "T2"    # Common in specific regions
    SEASONAL_VISITOR = "T3"      # Appears during specific seasons
    ELUSIVE_EXPLORER = "T4"      # Rare, requires specific conditions
    LEGENDARY_QUEST = "T5"       # Very rare, special sightings


class MigrationPattern(Enum):
    """Migration patterns for bird species."""
    RESIDENT = "resident"
    SHORT_DISTANCE = "short_distance"
    LONG_DISTANCE = "long_distance"
    PARTIAL_MIGRATOR = "partial_migrator"


class ActivityTime(Enum):
    """Optimal activity times for bird species."""
    DAWN = "dawn"
    MORNING = "morning"
    AFTERNOON = "afternoon"
    DUSK = "dusk"
    NIGHT = "night"
    DAYTIME = "daytime"


@dataclass
class SpeciesAvailability:
    """Availability information for a species."""
    best_months: List[str] = field(default_factory=list)
    regions: List[str] = field(default_factory=list)
    habitat_preferences: List[str] = field(default_factory=list)
    peak_activity: ActivityTime = ActivityTime.MORNING
    migration_pattern: MigrationPattern = MigrationPattern.RESIDENT
    breeding_range: List[str] = field(default_factory=list)
    wintering_range: List[str] = field(default_factory=list)
    abundance_rating: int = 3  # 1-5 scale
    ease_of_finding: str = "moderate"
    
    def is_available_in_month(self, month: str) -> bool:
        """Check if species is available in given month."""
        return month in self.best_months
    
    def is_found_in_region(self, region: str) -> bool:
        """Check if species is found in given region."""
        return region in self.regions


@dataclass
class Species:
    """Bird species data model."""
    name: str
    scientific_name: Optional[str] = None
    tier: SpeciesTier = SpeciesTier.REGIONAL_COMPANION
    occurrence_rate: float = 0.5  # 0.0 to 1.0
    region_count: int = 25
    visibility: str = "medium"
    availability: Optional[SpeciesAvailability] = None
    description: str = ""
    challenge: str = ""
    
    def __post_init__(self):
        """Initialize availability if not provided."""
        if self.availability is None:
            self.availability = SpeciesAvailability()
    
    @property
    def tier_description(self) -> str:
        """Get human-readable tier description."""
        descriptions = {
            SpeciesTier.COMMON_COMPANION: "Common Companion - Very common, easy to spot in most areas",
            SpeciesTier.REGIONAL_COMPANION: "Regional Companion - Common in specific regions, moderate difficulty",
            SpeciesTier.SEASONAL_VISITOR: "Seasonal Visitor - Appears during specific seasons, requires timing",
            SpeciesTier.ELUSIVE_EXPLORER: "Elusive Explorer - Rare, requires specific conditions and patience",
            SpeciesTier.LEGENDARY_QUEST: "Legendary Quest - Very rare, special sightings that become memorable stories"
        }
        return descriptions.get(self.tier, "Unknown tier")
    
    @property
    def tier_challenge(self) -> str:
        """Get personalized challenge for the tier level."""
        challenges = {
            SpeciesTier.COMMON_COMPANION: "Perfect for beginners! Focus on learning identification features and behavior patterns.",
            SpeciesTier.REGIONAL_COMPANION: "Great for building confidence! Practice with different lighting conditions and distances.",
            SpeciesTier.SEASONAL_VISITOR: "Timing is key! Research migration patterns and optimal viewing windows.",
            SpeciesTier.ELUSIVE_EXPLORER: "Patience and persistence required! Study habitat preferences and vocalizations.",
            SpeciesTier.LEGENDARY_QUEST: "The ultimate birding achievement! Document everything and share your story with the community."
        }
        return challenges.get(self.tier, "Unknown challenge level")
    
    def to_dict(self) -> Dict:
        """Convert species to dictionary representation."""
        return {
            "name": self.name,
            "scientific_name": self.scientific_name,
            "tier": self.tier.value,
            "tier_description": self.tier_description,
            "occurrence_rate": self.occurrence_rate,
            "region_count": self.region_count,
            "visibility": self.visibility,
            "availability": {
                "best_months": self.availability.best_months,
                "regions": self.availability.regions,
                "habitat_preferences": self.availability.habitat_preferences,
                "peak_activity": self.availability.peak_activity.value,
                "migration_pattern": self.availability.migration_pattern.value,
                "abundance_rating": self.availability.abundance_rating,
                "ease_of_finding": self.availability.ease_of_finding
            },
            "description": self.description,
            "challenge": self.tier_challenge
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Species':
        """Create species from dictionary representation."""
        availability_data = data.get("availability", {})
        availability = SpeciesAvailability(
            best_months=availability_data.get("best_months", []),
            regions=availability_data.get("regions", []),
            habitat_preferences=availability_data.get("habitat_preferences", []),
            peak_activity=ActivityTime(availability_data.get("peak_activity", "morning")),
            migration_pattern=MigrationPattern(availability_data.get("migration_pattern", "resident")),
            abundance_rating=availability_data.get("abundance_rating", 3),
            ease_of_finding=availability_data.get("ease_of_finding", "moderate")
        )
        
        return cls(
            name=data["name"],
            scientific_name=data.get("scientific_name"),
            tier=SpeciesTier(data.get("tier", "T2")),
            occurrence_rate=data.get("occurrence_rate", 0.5),
            region_count=data.get("region_count", 25),
            visibility=data.get("visibility", "medium"),
            availability=availability,
            description=data.get("description", ""),
            challenge=data.get("challenge", "")
        ) 