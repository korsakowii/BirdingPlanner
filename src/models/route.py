"""
Route and location data models for BirdingPlanner.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import math


@dataclass
class Coordinates:
    """Geographic coordinates."""
    latitude: float
    longitude: float
    
    def distance_to(self, other: 'Coordinates') -> float:
        """Calculate distance to another coordinate using Haversine formula."""
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other.latitude), math.radians(other.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c


@dataclass
class Hotspot:
    """Birding hotspot information."""
    name: str
    coordinates: Coordinates
    species_count: int
    description: str = ""
    facilities: List[str] = field(default_factory=list)
    best_season: str = ""
    accessibility: str = "moderate"
    
    def to_dict(self) -> Dict:
        """Convert hotspot to dictionary representation."""
        return {
            "name": self.name,
            "coordinates": {
                "latitude": self.coordinates.latitude,
                "longitude": self.coordinates.longitude
            },
            "species_count": self.species_count,
            "description": self.description,
            "facilities": self.facilities,
            "best_season": self.best_season,
            "accessibility": self.accessibility
        }


@dataclass
class Location:
    """Geographic location with birding information."""
    name: str
    region: str
    coordinates: Coordinates
    hotspots: List[Hotspot] = field(default_factory=list)
    climate: str = "temperate"
    elevation: Optional[int] = None
    
    def get_best_hotspots(self, limit: int = 3) -> List[Hotspot]:
        """Get the best hotspots sorted by species count."""
        sorted_hotspots = sorted(self.hotspots, key=lambda h: h.species_count, reverse=True)
        return sorted_hotspots[:limit]
    
    def to_dict(self) -> Dict:
        """Convert location to dictionary representation."""
        return {
            "name": self.name,
            "region": self.region,
            "coordinates": {
                "latitude": self.coordinates.latitude,
                "longitude": self.coordinates.longitude
            },
            "hotspots": [hotspot.to_dict() for hotspot in self.hotspots],
            "climate": self.climate,
            "elevation": self.elevation
        }


@dataclass
class ViewingSchedule:
    """Optimal viewing schedule for a location."""
    recommended_time: str
    activity_description: str
    target_species_focus: List[str] = field(default_factory=list)
    estimated_duration: str = "2-3 hours"
    weather_considerations: str = ""
    
    def to_dict(self) -> Dict:
        """Convert viewing schedule to dictionary representation."""
        return {
            "recommended_time": self.recommended_time,
            "activity_description": self.activity_description,
            "target_species_focus": self.target_species_focus,
            "estimated_duration": self.estimated_duration,
            "weather_considerations": self.weather_considerations
        }


@dataclass
class RouteStop:
    """A stop on a birding route."""
    stop_number: int
    location: Location
    distance_from_previous: float
    travel_time: str
    species_compatibility: float
    hotspots: List[Hotspot] = field(default_factory=list)
    viewing_schedule: Optional[ViewingSchedule] = None
    recommendations: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize viewing schedule if not provided."""
        if self.viewing_schedule is None:
            self.viewing_schedule = ViewingSchedule(
                recommended_time="6:00 AM - 9:00 AM",
                activity_description="Dawn chorus and early morning activity"
            )
    
    def to_dict(self) -> Dict:
        """Convert route stop to dictionary representation."""
        return {
            "stop_number": self.stop_number,
            "location": self.location.to_dict(),
            "distance_from_previous": self.distance_from_previous,
            "travel_time": self.travel_time,
            "species_compatibility": self.species_compatibility,
            "hotspots": [hotspot.to_dict() for hotspot in self.hotspots],
            "viewing_schedule": self.viewing_schedule.to_dict() if self.viewing_schedule else None,
            "recommendations": self.recommendations
        }


@dataclass
class Route:
    """Complete birding route."""
    base_location: str
    target_species: List[str]
    date_range: str
    stops: List[RouteStop] = field(default_factory=list)
    total_distance: float = 0.0
    estimated_total_time: str = ""
    summary: str = ""
    
    @property
    def total_stops(self) -> int:
        """Get total number of stops."""
        return len(self.stops)
    
    def add_stop(self, stop: RouteStop):
        """Add a stop to the route."""
        self.stops.append(stop)
        self.total_distance += stop.distance_from_previous
    
    def get_route_summary(self) -> str:
        """Generate a human-readable route summary."""
        if not self.stops:
            return "No stops planned."
        
        summary = f"This {self.total_stops}-stop route covers {self.total_distance:.1f} km "
        summary += f"and targets {len(self.target_species)} species: {', '.join(self.target_species)}. "
        summary += "The route is optimized for species diversity and travel efficiency. "
        
        total_hours = int(self.total_distance / 60 + self.total_stops * 2)
        summary += f"Estimated total time including travel and birding: {total_hours} hours."
        
        return summary
    
    def to_dict(self) -> Dict:
        """Convert route to dictionary representation."""
        return {
            "base_location": self.base_location,
            "target_species": self.target_species,
            "date_range": self.date_range,
            "total_stops": self.total_stops,
            "total_distance_km": self.total_distance,
            "estimated_total_time": self.estimated_total_time,
            "route_stops": [stop.to_dict() for stop in self.stops],
            "summary": self.get_route_summary()
        } 