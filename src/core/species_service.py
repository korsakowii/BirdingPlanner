"""
Species service for BirdingPlanner.
Handles species classification, availability analysis, and data management.
"""

import random
from typing import Dict, List, Optional
from ..models.species import Species, SpeciesTier, SpeciesAvailability, ActivityTime, MigrationPattern


class SpeciesService:
    """Service for managing bird species data and operations."""
    
    def __init__(self):
        """Initialize the species service with default data."""
        self._species_database = self._initialize_species_database()
    
    def _initialize_species_database(self) -> Dict[str, Species]:
        """Initialize the species database with default data."""
        database = {}
        
        # T1 - Common Companion species
        database["American Robin"] = Species(
            name="American Robin",
            scientific_name="Turdus migratorius",
            tier=SpeciesTier.COMMON_COMPANION,
            occurrence_rate=0.85,
            region_count=48,
            visibility="high",
            availability=SpeciesAvailability(
                best_months=["March", "April", "May", "September", "October"],
                regions=["Northeast", "Midwest", "West Coast", "Southeast"],
                habitat_preferences=["backyards", "parks", "forests", "meadows"],
                peak_activity=ActivityTime.DAWN,
                migration_pattern=MigrationPattern.PARTIAL_MIGRATOR,
                abundance_rating=5,
                ease_of_finding="very_easy"
            )
        )
        
        database["Northern Cardinal"] = Species(
            name="Northern Cardinal",
            scientific_name="Cardinalis cardinalis",
            tier=SpeciesTier.COMMON_COMPANION,
            occurrence_rate=0.78,
            region_count=35,
            visibility="high",
            availability=SpeciesAvailability(
                best_months=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                regions=["Southeast", "Midwest", "Northeast"],
                habitat_preferences=["backyards", "woodlands", "thickets"],
                peak_activity=ActivityTime.MORNING,
                migration_pattern=MigrationPattern.RESIDENT,
                abundance_rating=5,
                ease_of_finding="very_easy"
            )
        )
        
        # T2 - Regional Companion species
        database["Red-tailed Hawk"] = Species(
            name="Red-tailed Hawk",
            scientific_name="Buteo jamaicensis",
            tier=SpeciesTier.REGIONAL_COMPANION,
            occurrence_rate=0.65,
            region_count=50,
            visibility="medium",
            availability=SpeciesAvailability(
                best_months=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                regions=["All Regions"],
                habitat_preferences=["open_areas", "highways", "fields"],
                peak_activity=ActivityTime.DAYTIME,
                migration_pattern=MigrationPattern.PARTIAL_MIGRATOR,
                abundance_rating=4,
                ease_of_finding="easy"
            )
        )
        
        # T3 - Seasonal Visitor species
        database["Baltimore Oriole"] = Species(
            name="Baltimore Oriole",
            scientific_name="Icterus galbula",
            tier=SpeciesTier.SEASONAL_VISITOR,
            occurrence_rate=0.45,
            region_count=25,
            visibility="medium",
            availability=SpeciesAvailability(
                best_months=["April", "May", "June", "July", "August", "September"],
                regions=["Northeast", "Midwest", "Southeast"],
                habitat_preferences=["forests", "parks", "riversides"],
                peak_activity=ActivityTime.MORNING,
                migration_pattern=MigrationPattern.LONG_DISTANCE,
                abundance_rating=3,
                ease_of_finding="moderate"
            )
        )
        
        # T4 - Elusive Explorer species
        database["Cerulean Warbler"] = Species(
            name="Cerulean Warbler",
            scientific_name="Setophaga cerulea",
            tier=SpeciesTier.ELUSIVE_EXPLORER,
            occurrence_rate=0.25,
            region_count=20,
            visibility="low",
            availability=SpeciesAvailability(
                best_months=["April", "May", "June", "July", "August", "September"],
                regions=["Northeast", "Midwest", "Southeast"],
                habitat_preferences=["forests", "canopy"],
                peak_activity=ActivityTime.MORNING,
                migration_pattern=MigrationPattern.LONG_DISTANCE,
                abundance_rating=1,
                ease_of_finding="very_difficult"
            )
        )
        
        return database
    
    def get_species(self, name: str) -> Optional[Species]:
        """Get a species by name."""
        return self._species_database.get(name)
    
    def get_all_species(self) -> List[Species]:
        """Get all species in the database."""
        return list(self._species_database.values())
    
    def classify_species(self, name: str) -> Species:
        """Classify a species by name, creating mock data if not found."""
        if name in self._species_database:
            return self._species_database[name]
        
        # Generate mock data for unknown species
        return self._generate_mock_species(name)
    
    def _generate_mock_species(self, name: str) -> Species:
        """Generate mock species data for unknown species."""
        # Random tier assignment
        tiers = list(SpeciesTier)
        tier = random.choice(tiers)
        
        # Random occurrence rate based on tier
        tier_occurrence_ranges = {
            SpeciesTier.COMMON_COMPANION: (0.7, 0.9),
            SpeciesTier.REGIONAL_COMPANION: (0.5, 0.7),
            SpeciesTier.SEASONAL_VISITOR: (0.3, 0.5),
            SpeciesTier.ELUSIVE_EXPLORER: (0.1, 0.3),
            SpeciesTier.LEGENDARY_QUEST: (0.001, 0.1)
        }
        
        occurrence_range = tier_occurrence_ranges.get(tier, (0.3, 0.7))
        occurrence_rate = random.uniform(*occurrence_range)
        
        # Random region count
        region_count = random.randint(5, 45)
        
        # Random visibility
        visibility_options = ["low", "medium", "high"]
        visibility = random.choice(visibility_options)
        
        # Generate availability data
        seasonal_patterns = [
            ["March", "April", "May", "June", "July", "August", "September"],
            ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            ["September", "October", "November", "December", "January", "February"],
            ["April", "May", "June", "July", "August"]
        ]
        
        regions = ["Northeast", "Midwest", "Southeast", "West Coast", "Southwest"]
        habitats = ["forests", "meadows", "wetlands", "backyards", "parks", "coastal"]
        
        availability = SpeciesAvailability(
            best_months=random.choice(seasonal_patterns),
            regions=random.sample(regions, random.randint(1, 3)),
            habitat_preferences=random.sample(habitats, random.randint(1, 3)),
            peak_activity=random.choice(list(ActivityTime)),
            migration_pattern=random.choice(list(MigrationPattern)),
            abundance_rating=random.randint(1, 5),
            ease_of_finding=random.choice(["very_easy", "easy", "moderate", "difficult", "very_difficult"])
        )
        
        return Species(
            name=name,
            tier=tier,
            occurrence_rate=occurrence_rate,
            region_count=region_count,
            visibility=visibility,
            availability=availability
        )
    
    def get_species_availability(self, name: str, month: str, region: str) -> Dict:
        """Get availability information for a species in a specific month and region."""
        species = self.classify_species(name)
        
        is_good_time = species.availability.is_available_in_month(month)
        is_good_region = species.availability.is_found_in_region(region)
        
        confidence_score = 0
        if is_good_time:
            confidence_score += 50
        if is_good_region:
            confidence_score += 50
        
        recommendation = self._generate_recommendation(is_good_time, is_good_region, name, month, region)
        
        return {
            "species": name,
            "target_month": month,
            "target_region": region,
            "availability": species.availability,
            "confidence_score": confidence_score,
            "recommendation": recommendation
        }
    
    def _generate_recommendation(self, is_good_time: bool, is_good_region: bool, 
                               species: str, month: str, region: str) -> str:
        """Generate a human-readable recommendation."""
        if is_good_time and is_good_region:
            return f"Excellent timing! {species} is commonly found in {region} during {month}. Plan your trip with confidence."
        elif is_good_time and not is_good_region:
            return f"Good timing but challenging location. {species} is active in {month} but less common in {region}. Consider nearby regions."
        elif not is_good_time and is_good_region:
            return f"Good location but poor timing. {species} is found in {region} but rarely seen in {month}. Consider different months."
        else:
            return f"Challenging combination. {species} is not typically found in {region} during {month}. Consider alternative species or locations."
    
    def get_optimal_viewing_times(self, name: str, month: str) -> Dict:
        """Get optimal viewing times for a species in a specific month."""
        species = self.classify_species(name)
        
        if species.availability.is_available_in_month(month):
            peak_activity = species.availability.peak_activity
            
            time_mappings = {
                ActivityTime.DAWN: "5:00 AM - 7:00 AM",
                ActivityTime.MORNING: "6:00 AM - 10:00 AM",
                ActivityTime.AFTERNOON: "10:00 AM - 4:00 PM",
                ActivityTime.DUSK: "5:00 PM - 7:00 PM",
                ActivityTime.NIGHT: "8:00 PM - 11:00 PM",
                ActivityTime.DAYTIME: "6:00 AM - 6:00 PM"
            }
            
            return {
                "optimal_hours": time_mappings.get(peak_activity, "6:00 AM - 10:00 AM"),
                "peak_activity": peak_activity.value,
                "recommendation": f"Best viewed during {peak_activity.value} hours in {month}"
            }
        else:
            return {
                "optimal_hours": "Not typically seen in this month",
                "peak_activity": "unknown",
                "recommendation": f"{name} is not typically active in {month}"
            } 