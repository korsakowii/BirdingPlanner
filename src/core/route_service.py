"""
Route service for BirdingPlanner.
Handles route optimization and location management.
"""

import random
from typing import Dict, List, Optional
from ..models.route import Route, RouteStop, Location, Coordinates, Hotspot, ViewingSchedule


class RouteService:
    """Service for managing routes and locations."""
    
    def __init__(self):
        """Initialize the route service with default data."""
        self._location_database = self._initialize_location_database()
        self._species_location_matrix = self._initialize_compatibility_matrix()
    
    def _initialize_location_database(self) -> Dict[str, Location]:
        """Initialize the location database with default data."""
        database = {}
        
        # New York
        ny_coords = Coordinates(latitude=40.7128, longitude=-74.0060)
        ny_hotspots = [
            Hotspot("Central Park", ny_coords, 230, "Urban park with diverse habitats"),
            Hotspot("Prospect Park", ny_coords, 180, "Brooklyn's premier birding location"),
            Hotspot("Jamaica Bay Wildlife Refuge", ny_coords, 320, "Coastal wetland habitat")
        ]
        database["New York"] = Location(
            name="New York",
            region="Northeast",
            coordinates=ny_coords,
            hotspots=ny_hotspots
        )
        
        # Boston
        boston_coords = Coordinates(latitude=42.3601, longitude=-71.0589)
        boston_hotspots = [
            Hotspot("Mount Auburn Cemetery", boston_coords, 200, "Historic cemetery with mature trees"),
            Hotspot("Parker River NWR", boston_coords, 280, "Coastal refuge with diverse species"),
            Hotspot("Boston Common", boston_coords, 150, "Urban park with seasonal migrants")
        ]
        database["Boston"] = Location(
            name="Boston",
            region="Northeast",
            coordinates=boston_coords,
            hotspots=boston_hotspots
        )
        
        # Chicago
        chicago_coords = Coordinates(latitude=41.8781, longitude=-87.6298)
        chicago_hotspots = [
            Hotspot("Montrose Point", chicago_coords, 250, "Lakefront migration hotspot"),
            Hotspot("Jackson Park", chicago_coords, 180, "Urban park with diverse habitats"),
            Hotspot("North Park Village", chicago_coords, 160, "Wooded area with resident species")
        ]
        database["Chicago"] = Location(
            name="Chicago",
            region="Midwest",
            coordinates=chicago_coords,
            hotspots=chicago_hotspots
        )
        
        # Miami
        miami_coords = Coordinates(latitude=25.7617, longitude=-80.1918)
        miami_hotspots = [
            Hotspot("Everglades National Park", miami_coords, 350, "World-famous wetland ecosystem"),
            Hotspot("Bill Baggs Cape Florida", miami_coords, 200, "Coastal park with seabirds"),
            Hotspot("Fairchild Tropical Botanic Garden", miami_coords, 180, "Tropical garden with exotic species")
        ]
        database["Miami"] = Location(
            name="Miami",
            region="Southeast",
            coordinates=miami_coords,
            hotspots=miami_hotspots
        )
        
        # San Francisco
        sf_coords = Coordinates(latitude=37.7749, longitude=-122.4194)
        sf_hotspots = [
            Hotspot("Golden Gate Park", sf_coords, 200, "Urban park with diverse habitats"),
            Hotspot("Point Reyes National Seashore", sf_coords, 450, "Coastal wilderness with seabirds"),
            Hotspot("San Francisco Bay", sf_coords, 300, "Estuary with waterfowl and shorebirds")
        ]
        database["San Francisco"] = Location(
            name="San Francisco",
            region="West Coast",
            coordinates=sf_coords,
            hotspots=sf_hotspots
        )
        
        return database
    
    def _initialize_compatibility_matrix(self) -> Dict[str, Dict[str, float]]:
        """Initialize species-location compatibility matrix."""
        return {
            "American Robin": {
                "New York": 0.9, "Boston": 0.85, "Chicago": 0.8, "Miami": 0.6, "San Francisco": 0.7
            },
            "Northern Cardinal": {
                "New York": 0.8, "Boston": 0.75, "Chicago": 0.85, "Miami": 0.9, "San Francisco": 0.3
            },
            "Blue Jay": {
                "New York": 0.85, "Boston": 0.8, "Chicago": 0.9, "Miami": 0.4, "San Francisco": 0.2
            },
            "Red-tailed Hawk": {
                "New York": 0.7, "Boston": 0.75, "Chicago": 0.8, "Miami": 0.6, "San Francisco": 0.8
            },
            "Baltimore Oriole": {
                "New York": 0.6, "Boston": 0.65, "Chicago": 0.7, "Miami": 0.4, "San Francisco": 0.3
            },
            "Cerulean Warbler": {
                "New York": 0.4, "Boston": 0.35, "Chicago": 0.3, "Miami": 0.2, "San Francisco": 0.1
            }
        }
    
    def get_location(self, name: str) -> Optional[Location]:
        """Get a location by name."""
        return self._location_database.get(name)
    
    def get_all_locations(self) -> List[Location]:
        """Get all locations in the database."""
        return list(self._location_database.values())
    
    def get_species_compatibility_score(self, species: str, location: str) -> float:
        """Get compatibility score between species and location."""
        if species in self._species_location_matrix:
            return self._species_location_matrix[species].get(location, 0.5)
        return 0.5  # Default score for unknown species
    
    def optimize_route(self, base_location: str, target_species: List[str], 
                      date_range: str, max_stops: int = 3) -> Route:
        """Optimize route for given species and location."""
        # Get base location
        base_loc = self.get_location(base_location)
        if not base_loc:
            raise ValueError(f"Unknown location: {base_location}")
        
        # Score all locations
        location_scores = []
        for loc_name, location in self._location_database.items():
            if loc_name == base_location:
                continue
            
            # Calculate combined score
            species_score = sum(
                self.get_species_compatibility_score(species, loc_name)
                for species in target_species
            ) / len(target_species)
            
            # Distance penalty (simplified)
            distance = base_loc.coordinates.distance_to(location.coordinates)
            distance_penalty = min(distance / 1000, 0.3)  # Max 30% penalty
            
            final_score = species_score - distance_penalty
            location_scores.append((loc_name, location, final_score))
        
        # Sort by score and take top locations
        location_scores.sort(key=lambda x: x[2], reverse=True)
        selected_locations = location_scores[:max_stops]
        
        # Create route
        route = Route(
            base_location=base_location,
            target_species=target_species,
            date_range=date_range
        )
        
        # Add stops
        for i, (loc_name, location, score) in enumerate(selected_locations):
            distance = base_loc.coordinates.distance_to(location.coordinates)
            travel_time = f"{int(distance / 60)} hours"
            
            # Get best hotspots
            best_hotspots = location.get_best_hotspots(limit=2)
            
            # Create viewing schedule
            viewing_schedule = ViewingSchedule(
                recommended_time="6:00 AM - 9:00 AM",
                activity_description="Dawn chorus and early morning activity",
                target_species_focus=target_species,
                estimated_duration="2-3 hours"
            )
            
            # Create route stop
            stop = RouteStop(
                stop_number=i + 1,
                location=location,
                distance_from_previous=distance,
                travel_time=travel_time,
                species_compatibility=score,
                hotspots=best_hotspots,
                viewing_schedule=viewing_schedule,
                recommendations=[
                    "Arrive early for best birding",
                    "Bring binoculars and field guide",
                    "Check weather conditions"
                ]
            )
            
            route.add_stop(stop)
        
        # Set estimated time
        total_hours = int(route.total_distance / 60 + len(route.stops) * 2)
        route.estimated_total_time = f"{total_hours} hours"
        
        return route
    
    def get_suggestions(self, base_location: str, target_species: List[str]) -> List[Dict]:
        """Get route suggestions for given parameters."""
        try:
            route = self.optimize_route(base_location, target_species, "Spring 2024")
            return [route.to_dict()]
        except Exception as e:
            return [{"error": str(e)}] 