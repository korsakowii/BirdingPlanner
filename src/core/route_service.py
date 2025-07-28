"""
Route service for BirdingPlanner.
Handles route optimization and location management.
"""

import math
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
    
    def create_multi_day_plan(self, base_location: str, target_species: List[str], 
                             date_range: str, days: int = 3, max_distance_per_day: float = 50.0) -> Dict:
        """Create a multi-day birding plan optimized for maximum species with minimal walking."""
        print(f"🗺️ Creating {days}-day optimized birding plan...")
        
        # Get all available hotspots in the area
        all_hotspots = self._get_all_hotspots_in_area(base_location, max_distance_per_day * days)
        
        # Analyze species availability at each hotspot
        hotspot_species_analysis = {}
        for hotspot in all_hotspots:
            species_scores = {}
            for species in target_species:
                score = self.get_species_compatibility_score(species, hotspot['name'])
                species_scores[species] = score
            hotspot_species_analysis[hotspot['name']] = {
                'hotspot': hotspot,
                'species_scores': species_scores,
                'total_score': sum(species_scores.values()),
                'unique_species': [s for s, score in species_scores.items() if score > 0.3]
            }
        
        # Sort hotspots by total species score
        sorted_hotspots = sorted(
            hotspot_species_analysis.items(),
            key=lambda x: x[1]['total_score'],
            reverse=True
        )
        
        # Create daily plans
        daily_plans = []
        remaining_hotspots = sorted_hotspots.copy()
        daily_distance_budget = max_distance_per_day
        
        for day in range(1, days + 1):
            print(f"📅 Planning Day {day}...")
            
            day_plan = self._create_optimized_day_plan(
                remaining_hotspots, 
                daily_distance_budget, 
                day, 
                base_location,
                target_species
            )
            
            daily_plans.append(day_plan)
            
            # Remove visited hotspots from remaining list
            visited_hotspots = [h['hotspot']['name'] for h in day_plan['hotspots']]
            remaining_hotspots = [
                (name, data) for name, data in remaining_hotspots 
                if name not in visited_hotspots
            ]
        
        # Calculate overall statistics
        total_species_seen = set()
        total_distance = 0
        total_success_probability = 1.0
        
        for day_plan in daily_plans:
            total_species_seen.update(day_plan['expected_species'])
            total_distance += day_plan['total_distance']
            total_success_probability *= day_plan['day_success_probability']
        
        multi_day_plan = {
            'base_location': base_location,
            'target_species': target_species,
            'date_range': date_range,
            'total_days': days,
            'daily_plans': daily_plans,
            'overall_stats': {
                'total_species_expected': len(total_species_seen),
                'total_distance': total_distance,
                'average_distance_per_day': total_distance / days,
                'overall_success_probability': total_success_probability,
                'species_coverage': len(total_species_seen) / len(target_species),
                'efficiency_score': len(total_species_seen) / (total_distance / 10)  # species per 10km
            }
        }
        
        return multi_day_plan
    
    def _create_optimized_day_plan(self, available_hotspots: List, max_distance: float, 
                                  day_number: int, base_location: str, target_species: List[str]) -> Dict:
        """Create an optimized plan for a single day."""
        if not available_hotspots:
            return self._create_empty_day_plan(day_number, base_location)
        
        # Start with the highest scoring hotspot
        best_hotspot_name, best_hotspot_data = available_hotspots[0]
        best_hotspot = best_hotspot_data['hotspot']
        
        # Find nearby hotspots that complement the best one
        nearby_hotspots = []
        current_distance = 0
        
        for hotspot_name, hotspot_data in available_hotspots[1:]:
            hotspot = hotspot_data['hotspot']
            
            # Calculate distance from current location
            if nearby_hotspots:
                last_hotspot = nearby_hotspots[-1]['hotspot']
                distance = self._calculate_distance(
                    last_hotspot['coordinates'], 
                    hotspot['coordinates']
                )
            else:
                distance = self._calculate_distance(
                    best_hotspot['coordinates'], 
                    hotspot['coordinates']
                )
            
            # Check if adding this hotspot would exceed daily distance limit
            if current_distance + distance <= max_distance:
                # Check if this hotspot adds unique species
                unique_species = [
                    species for species in hotspot_data['unique_species']
                    if species not in [s for h in nearby_hotspots for s in h['unique_species']]
                ]
                
                if unique_species or len(nearby_hotspots) < 2:  # Allow up to 3 hotspots per day
                    nearby_hotspots.append({
                        'hotspot': hotspot,
                        'distance_from_previous': distance,
                        'unique_species': unique_species,
                        'species_scores': hotspot_data['species_scores']
                    })
                    current_distance += distance
        
        # Create day plan
        day_hotspots = [{'hotspot': best_hotspot, 'distance_from_previous': 0, 
                        'unique_species': best_hotspot_data['unique_species'],
                        'species_scores': best_hotspot_data['species_scores']}] + nearby_hotspots
        
        # Calculate day statistics and create detailed route
        expected_species = set()
        day_success_probability = 1.0
        total_distance = sum(h['distance_from_previous'] for h in day_hotspots)
        
        # Create detailed route plan for the day
        route_stops = []
        current_time = "6:00 AM"  # Start early for best birding
        
        for i, hotspot_info in enumerate(day_hotspots):
            hotspot = hotspot_info['hotspot']
            distance = hotspot_info['distance_from_previous']
            unique_species = hotspot_info['unique_species']
            species_scores = hotspot_info['species_scores']
            
            # Calculate travel time
            if distance > 0:
                travel_time = self._calculate_travel_time(distance)
            else:
                travel_time = "0 minutes"
            
            # Determine optimal viewing time for this hotspot
            if i == 0:
                viewing_time = "6:00 AM - 9:00 AM"  # First stop - dawn chorus
            elif i == 1:
                viewing_time = "9:30 AM - 12:00 PM"  # Second stop - mid-morning
            else:
                viewing_time = "12:30 PM - 3:00 PM"  # Later stops - afternoon
            
            # Calculate success probability for this hotspot
            hotspot_prob = sum(species_scores.values()) / len(target_species)
            day_success_probability *= (0.7 + 0.3 * hotspot_prob)
            
            # Get target species for this hotspot (species with high scores)
            target_species_for_hotspot = [
                species for species, score in species_scores.items() 
                if score > 0.3 and species in target_species
            ]
            
            # Add to expected species
            expected_species.update(target_species_for_hotspot)
            
            # Create route stop details
            route_stop = {
                'stop_number': i + 1,
                'hotspot_name': hotspot['name'],
                'coordinates': hotspot['coordinates'],
                'description': hotspot.get('description', ''),
                'distance_from_previous': distance,
                'travel_time': travel_time,
                'viewing_time': viewing_time,
                'target_species': target_species_for_hotspot,
                'species_scores': species_scores,
                'success_probability': hotspot_prob,
                'recommendations': self._generate_hotspot_recommendations(hotspot, target_species_for_hotspot),
                'facilities': self._get_hotspot_facilities(hotspot),
                'best_approach': self._get_best_approach(hotspot, target_species_for_hotspot)
            }
            
            route_stops.append(route_stop)
        
        # Calculate efficiency score
        efficiency_score = len(expected_species) / (total_distance / 10) if total_distance > 0 else len(expected_species)
        
        return {
            'day': day_number,
            'hotspots': day_hotspots,
            'expected_species': list(expected_species),
            'total_distance': total_distance,
            'day_success_probability': day_success_probability,
            'efficiency_score': efficiency_score,
            'route_stops': route_stops,
            'daily_schedule': self._create_daily_schedule(route_stops),
            'daily_summary': self._create_daily_summary(day_number, route_stops, expected_species, total_distance)
        }
    
    def _generate_hotspot_recommendations(self, hotspot: Dict, target_species: List[str]) -> List[str]:
        """Generate specific recommendations for a hotspot."""
        recommendations = []
        
        # General recommendations
        recommendations.append("Arrive early for best birding conditions")
        recommendations.append("Bring binoculars and field guide")
        recommendations.append("Move slowly and quietly to avoid startling birds")
        
        # Species-specific recommendations
        if len(target_species) > 0:
            recommendations.append(f"Focus on: {', '.join(target_species)}")
        
        # Habitat-specific recommendations
        if "park" in hotspot.get('description', '').lower():
            recommendations.append("Check both open areas and wooded sections")
        elif "wetland" in hotspot.get('description', '').lower():
            recommendations.append("Bring waterproof footwear")
            recommendations.append("Check both water edges and marsh areas")
        elif "coastal" in hotspot.get('description', '').lower():
            recommendations.append("Check tide times for optimal viewing")
            recommendations.append("Look for both shorebirds and seabirds")
        
        return recommendations
    
    def _get_hotspot_facilities(self, hotspot: Dict) -> List[str]:
        """Get available facilities at the hotspot."""
        facilities = ["Parking available", "Walking trails"]
        
        # Add facilities based on hotspot type
        if "park" in hotspot.get('description', '').lower():
            facilities.extend(["Restrooms", "Picnic areas", "Information center"])
        elif "refuge" in hotspot.get('description', '').lower():
            facilities.extend(["Visitor center", "Observation platforms", "Educational displays"])
        
        return facilities
    
    def _get_best_approach(self, hotspot: Dict, target_species: List[str]) -> str:
        """Get the best approach strategy for the hotspot."""
        if "park" in hotspot.get('description', '').lower():
            return "Start at the main entrance and work your way through different habitats"
        elif "wetland" in hotspot.get('description', '').lower():
            return "Begin at observation platforms, then walk the perimeter trails"
        elif "coastal" in hotspot.get('description', '').lower():
            return "Check the beach first, then explore inland areas"
        else:
            return "Start at the main viewing area and explore systematically"
    
    def _create_daily_schedule(self, route_stops: List[Dict]) -> List[Dict]:
        """Create a detailed daily schedule."""
        schedule = []
        current_time = "6:00 AM"
        
        for stop in route_stops:
            # Add travel time if not first stop
            if stop['stop_number'] > 1:
                schedule.append({
                    'time': current_time,
                    'activity': f"Travel to {stop['hotspot_name']}",
                    'duration': stop['travel_time'],
                    'type': 'travel'
                })
                # Update current time (simplified)
                current_time = stop['viewing_time'].split(' - ')[0]
            
            # Add birding time
            schedule.append({
                'time': current_time,
                'activity': f"Birding at {stop['hotspot_name']}",
                'duration': "2-3 hours",
                'type': 'birding',
                'target_species': stop['target_species'],
                'recommendations': stop['recommendations'][:2]  # Top 2 recommendations
            })
            
            # Update current time for next stop
            current_time = stop['viewing_time'].split(' - ')[1]
        
        return schedule
    
    def _create_daily_summary(self, day_number: int, route_stops: List[Dict], 
                            expected_species: set, total_distance: float) -> str:
        """Create a summary for the day."""
        summary = f"Day {day_number} focuses on {len(route_stops)} key hotspots "
        summary += f"covering {total_distance:.1f} km. "
        summary += f"Target species include {', '.join(list(expected_species)[:3])}"
        if len(expected_species) > 3:
            summary += f" and {len(expected_species) - 3} more species. "
        else:
            summary += ". "
        
        summary += "The route is optimized for maximum species diversity with minimal travel time. "
        summary += "Each hotspot offers unique habitat and species combinations."
        
        return summary
    
    def _create_empty_day_plan(self, day_number: int, base_location: str) -> Dict:
        """Create an empty day plan when no hotspots are available."""
        return {
            'day': day_number,
            'hotspots': [],
            'expected_species': [],
            'total_distance': 0,
            'day_success_probability': 0.0,
            'efficiency_score': 0.0
        }
    
    def _get_all_hotspots_in_area(self, base_location: str, max_radius: float) -> List[Dict]:
        """Get all hotspots within a certain radius of the base location."""
        base_loc = self.get_location(base_location)
        if not base_loc:
            return []
        
        base_coords = base_loc.coordinates
        all_hotspots = []
        
        # Get hotspots from all available locations
        for location_name, location_data in self._location_database.items():
            distance = self._calculate_distance(base_coords, location_data.coordinates)
            
            if distance <= max_radius:
                # Add the main location as a hotspot
                all_hotspots.append({
                    'name': location_name,
                    'coordinates': location_data.coordinates,
                    'description': location_data.name,
                    'distance_from_base': distance
                })
                
                # Add nearby hotspots (simulated)
                nearby_hotspots = self._generate_nearby_hotspots(location_data.coordinates, location_name)
                all_hotspots.extend(nearby_hotspots)
        
        return all_hotspots
    
    def _generate_nearby_hotspots(self, base_coords: Coordinates, location_name: str) -> List[Dict]:
        """Generate nearby hotspots around a base location."""
        nearby_hotspots = []
        
        # Generate 3-5 nearby hotspots with slight coordinate variations
        for i in range(3, 6):
            # Add small random variations to coordinates
            lat_variation = (i - 2) * 0.01  # ~1km increments
            lng_variation = (i - 2) * 0.01
            
            hotspot_coords = Coordinates(
                latitude=base_coords.latitude + lat_variation,
                longitude=base_coords.longitude + lng_variation
            )
            
            nearby_hotspots.append({
                'name': f"{location_name} Hotspot {i}",
                'coordinates': hotspot_coords,
                'description': f"Secondary birding location near {location_name}",
                'distance_from_base': self._calculate_distance(base_coords, hotspot_coords)
            })
        
        return nearby_hotspots
    
    def _calculate_distance(self, coord1: Coordinates, coord2: Coordinates) -> float:
        """Calculate distance between two geographic coordinates using the Haversine formula."""
        R = 6371.0 # Radius of Earth in km
        lat1, lon1 = coord1.latitude, coord1.longitude
        lat2, lon2 = coord2.latitude, coord2.longitude
        
        d_lat = (lat2 - lat1) * math.pi / 180.0
        d_lon = (lon2 - lon1) * math.pi / 180.0
        
        a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + \
            math.cos(lat1 * math.pi / 180.0) * math.cos(lat2 * math.pi / 180.0) * \
            math.sin(d_lon / 2) * math.sin(d_lon / 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c # Distance in km
        return distance 