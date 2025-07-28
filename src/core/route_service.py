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
        
        # Check if all species can be found locally
        local_scores = []
        for species in target_species:
            local_score = self.get_species_compatibility_score(species, base_location)
            local_scores.append(local_score)
        
        avg_local_score = sum(local_scores) / len(local_scores)
        
        # If all species have high local availability (>0.7), suggest local birding
        if avg_local_score > 0.7 and all(score > 0.6 for score in local_scores):
            return self._create_local_route(base_location, target_species, date_range)
        
        # Otherwise, optimize for multi-location route with distance-based selection
        location_scores = []
        for loc_name, location in self._location_database.items():
            if loc_name == base_location:
                continue
            
            # Calculate combined score
            species_score = sum(
                self.get_species_compatibility_score(species, loc_name)
                for species in target_species
            ) / len(target_species)
            
            # Calculate distance and apply distance-based scoring
            distance = base_loc.coordinates.distance_to(location.coordinates)
            
            # Distance scoring: closer locations get higher scores
            if distance <= 50:  # Within 50km - very close
                distance_score = 1.0
            elif distance <= 150:  # Within 150km - close
                distance_score = 0.8
            elif distance <= 300:  # Within 300km - moderate
                distance_score = 0.6
            elif distance <= 500:  # Within 500km - far
                distance_score = 0.4
            else:  # Very far
                distance_score = 0.2
            
            # Combine species score and distance score
            final_score = (species_score * 0.7) + (distance_score * 0.3)
            
            location_scores.append((loc_name, location, final_score, distance))
        
        # Sort by score (highest first) and distance (closest first for same scores)
        location_scores.sort(key=lambda x: (x[2], -x[3]), reverse=True)
        
        # Dynamic selection: choose optimal number of stops based on scores and distances
        selected_locations = self._select_optimal_locations(location_scores, max_stops)
        
        # Create route
        route = Route(
            base_location=base_location,
            target_species=target_species,
            date_range=date_range
        )
        
        # Add stops
        for i, (loc_name, location, score, distance) in enumerate(selected_locations):
            travel_time = self._calculate_travel_time(distance)
            
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
        total_hours = self._calculate_total_time(route)
        route.estimated_total_time = f"{total_hours} hours"
        
        return route
    
    def _create_local_route(self, base_location: str, target_species: List[str], 
                           date_range: str) -> Route:
        """Create a local birding route when species are available nearby."""
        base_loc = self.get_location(base_location)
        
        # Create route with local focus
        route = Route(
            base_location=base_location,
            target_species=target_species,
            date_range=date_range
        )
        
        # Get local hotspots and select optimal number
        all_local_hotspots = base_loc.get_best_hotspots(limit=5)  # Get more options
        
        # Select optimal number of hotspots (1-3 based on species and availability)
        if len(target_species) == 1:
            # Single species - 1-2 hotspots usually sufficient
            selected_hotspots = all_local_hotspots[:min(2, len(all_local_hotspots))]
        elif len(target_species) <= 2:
            # 2 species - 2-3 hotspots for variety
            selected_hotspots = all_local_hotspots[:min(3, len(all_local_hotspots))]
        else:
            # 3+ species - up to 3 hotspots
            selected_hotspots = all_local_hotspots[:min(3, len(all_local_hotspots))]
        
        # Create local stops (different hotspots in the same city)
        for i, hotspot in enumerate(selected_hotspots):
            # Calculate local travel time (within city)
            local_travel_time = f"{15 + i * 10} minutes"  # 15-35 minutes between spots
            
            # Create viewing schedule
            viewing_schedule = ViewingSchedule(
                recommended_time="6:00 AM - 9:00 AM",
                activity_description="Local birding at prime hotspots",
                target_species_focus=target_species,
                estimated_duration="1-2 hours"
            )
            
            # Create route stop
            stop = RouteStop(
                stop_number=i + 1,
                location=base_loc,
                distance_from_previous=5 + i * 3,  # 5-11 km between local spots
                travel_time=local_travel_time,
                species_compatibility=0.9,  # High local compatibility
                hotspots=[hotspot],
                viewing_schedule=viewing_schedule,
                recommendations=[
                    "Perfect for local birding - no long travel needed!",
                    "Visit during dawn chorus for best results",
                    "These common species are easily found locally",
                    "Great for beginners or time-limited birders"
                ]
            )
            
            route.add_stop(stop)
        
        # Set estimated time (much shorter for local birding)
        total_hours = 2 + len(selected_hotspots)  # 2 hours base + 1 hour per hotspot
        route.estimated_total_time = f"{total_hours}-{total_hours + 2} hours"
        
        return route
    
    def _select_optimal_locations(self, location_scores: List[tuple], max_stops: int) -> List[tuple]:
        """Select optimal number of locations based on scores and distances."""
        if not location_scores:
            return []
        
        # Simply take the top max_stops locations
        # The caller (CLI) has already determined the optimal number of stops
        return location_scores[:max_stops]
    
    def _calculate_travel_time(self, distance: float) -> str:
        """Calculate travel time based on distance."""
        if distance <= 50:
            return f"{int(distance / 30)} hours"  # Local travel
        elif distance <= 150:
            return f"{int(distance / 60)} hours"  # Regional travel
        else:
            return f"{int(distance / 80)} hours"  # Long distance travel
    
    def _calculate_total_time(self, route: 'Route') -> int:
        """Calculate total trip time including travel and birding."""
        travel_time = route.total_distance / 80  # Average 80km/h
        birding_time = len(route.stops) * 2  # 2 hours per stop
        return int(travel_time + birding_time)
    
    def get_suggestions(self, base_location: str, target_species: List[str]) -> List[Dict]:
        """Get route suggestions for given parameters."""
        try:
            route = self.optimize_route(base_location, target_species, "Spring 2024")
            return [route.to_dict()]
        except Exception as e:
            return [{"error": str(e)}]
    
    def calculate_success_probability(self, base_location: str, target_species: List[str], 
                                    num_stops: int) -> Dict[str, float]:
        """Calculate success probability for seeing target species with given number of stops."""
        base_loc = self.get_location(base_location)
        if not base_loc:
            return {"error": f"Unknown location: {base_location}"}
        
        # Calculate individual species probabilities
        species_probabilities = {}
        for species in target_species:
            local_score = self.get_species_compatibility_score(species, base_location)
            
            # Base probability from local availability
            base_prob = local_score
            
            # Probability increases with more stops (diminishing returns)
            if num_stops == 1:
                prob = base_prob
            elif num_stops == 2:
                prob = base_prob + (1 - base_prob) * 0.3  # 30% additional chance
            elif num_stops == 3:
                prob = base_prob + (1 - base_prob) * 0.5  # 50% additional chance
            else:
                prob = base_prob + (1 - base_prob) * 0.6  # Max 60% additional chance
            
            species_probabilities[species] = min(prob, 0.95)  # Cap at 95%
        
        # Calculate overall success probability (probability of seeing ALL species)
        overall_prob = 1.0
        for prob in species_probabilities.values():
            overall_prob *= prob
        
        return {
            "overall_success_rate": overall_prob,
            "species_probabilities": species_probabilities,
            "recommended_min_stops": self._get_recommended_min_stops(target_species, base_location)
        }
    
    def _get_recommended_min_stops(self, target_species: List[str], base_location: str) -> Dict[str, int]:
        """Get recommended minimum stops for high success probability."""
        base_loc = self.get_location(base_location)
        if not base_loc:
            return {"error": f"Unknown location: {base_location}"}
        
        # Calculate average local availability
        local_scores = []
        for species in target_species:
            local_score = self.get_species_compatibility_score(species, base_location)
            local_scores.append(local_score)
        
        avg_local_score = sum(local_scores) / len(local_scores)
        min_local_score = min(local_scores)
        
        # Determine recommended stops based on availability
        if avg_local_score > 0.8 and min_local_score > 0.7:
            # High local availability - 1-2 stops sufficient
            recommended_stops = 1 if len(target_species) == 1 else 2
        elif avg_local_score > 0.6 and min_local_score > 0.5:
            # Moderate local availability - 2-3 stops recommended
            recommended_stops = 2 if len(target_species) <= 2 else 3
        else:
            # Low local availability - 3+ stops needed
            recommended_stops = 3
        
        # Adjust based on species count
        if len(target_species) == 1:
            recommended_stops = max(1, recommended_stops - 1)
        elif len(target_species) >= 3:
            recommended_stops = min(5, recommended_stops + 1)
        
        return {
            "recommended_stops": recommended_stops,
            "reasoning": self._get_recommendation_reasoning(avg_local_score, min_local_score, len(target_species))
        }
    
    def _get_recommendation_reasoning(self, avg_score: float, min_score: float, species_count: int) -> str:
        """Get reasoning for recommended stop count."""
        if avg_score > 0.8 and min_score > 0.7:
            if species_count == 1:
                return "High local availability - 1 stop should be sufficient"
            else:
                return "High local availability - 2 stops for variety"
        elif avg_score > 0.6 and min_score > 0.5:
            if species_count <= 2:
                return "Moderate local availability - 2 stops recommended"
            else:
                return "Moderate local availability - 3 stops for better coverage"
        else:
            if species_count <= 2:
                return "Low local availability - 3 stops needed for success"
            else:
                return "Low local availability - 3+ stops recommended for multiple species"
    
    def optimize_route_with_success_target(self, base_location: str, target_species: List[str], 
                                         date_range: str, target_success_rate: float = 0.8) -> Route:
        """Optimize route to achieve target success rate."""
        # Start with minimum recommended stops
        min_stops_info = self._get_recommended_min_stops(target_species, base_location)
        min_stops = min_stops_info["recommended_stops"]
        
        # Try different numbers of stops to find the minimum that meets target
        for num_stops in range(min_stops, 6):  # Try up to 5 stops
            success_info = self.calculate_success_probability(base_location, target_species, num_stops)
            if success_info["overall_success_rate"] >= target_success_rate:
                # Found minimum stops that meet target
                return self.optimize_route(base_location, target_species, date_range, num_stops)
        
        # If we can't meet target with 5 stops, return best possible
        return self.optimize_route(base_location, target_species, date_range, 5) 