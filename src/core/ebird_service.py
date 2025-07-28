"""
eBird API Service for BirdingPlanner
Provides real-time bird observation data and hotspot information
"""

import requests
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from src.models.route import Coordinates

logger = logging.getLogger(__name__)


@dataclass
class EBirdObservation:
    """eBird observation data model"""
    species: str
    location: str
    timestamp: datetime
    observer: str
    coordinates: Optional[Coordinates]
    checklist_url: Optional[str]
    observation_count: Optional[int]
    location_name: str
    region_code: str


@dataclass
class HotspotActivity:
    """eBird hotspot activity data model"""
    hotspot_id: str
    hotspot_name: str
    recent_observations: int
    species_count: int
    last_updated: datetime
    coordinates: Optional[Coordinates]
    success_rate: float


class EBirdAPIClient:
    """eBird API client for making HTTP requests"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.ebird.org/v2"
        self.headers = {
            "X-eBirdApiToken": api_key,
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request with error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"eBird API request failed: {e}")
            return {}
    
    def get_recent_observations(self, region_code: str, species_code: str = None, 
                               days: int = 7) -> List[Dict]:
        """Get recent observations for a region"""
        endpoint = f"data/obs/{region_code}/recent"
        if species_code:
            endpoint += f"/{species_code}"
        
        params = {"back": days} if days else {}
        return self._make_request(endpoint, params)
    
    def get_hotspots(self, region_code: str) -> List[Dict]:
        """Get hotspots for a region"""
        endpoint = f"ref/hotspot/{region_code}"
        return self._make_request(endpoint)
    
    def get_species_observations(self, species_code: str, region_code: str, 
                                days: int = 30) -> List[Dict]:
        """Get observations for a specific species"""
        endpoint = f"data/obs/{region_code}/recent/{species_code}"
        params = {"back": days}
        return self._make_request(endpoint, params)
    
    def get_hotspot_info(self, hotspot_id: str) -> Dict:
        """Get detailed information for a hotspot"""
        endpoint = f"ref/hotspot/info/{hotspot_id}"
        return self._make_request(endpoint)


class EBirdService:
    """Main eBird service for BirdingPlanner"""
    
    def __init__(self, api_key: str):
        self.client = EBirdAPIClient(api_key)
        self.cache = {}  # Simple in-memory cache
        self.cache_ttl = 300  # 5 minutes cache TTL
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        cache_time, _ = self.cache[key]
        return datetime.now() - cache_time < timedelta(seconds=self.cache_ttl)
    
    def _cache_data(self, key: str, data: Any):
        """Cache data with timestamp"""
        self.cache[key] = (datetime.now(), data)
    
    def get_recent_observations(self, location: str, species: str = None, 
                               days: int = 7) -> List[EBirdObservation]:
        """Get recent observations for a location"""
        cache_key = f"obs_{location}_{species}_{days}"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key][1]
        
        # Convert location to region code (simplified mapping)
        region_code = self._location_to_region_code(location)
        if not region_code:
            logger.warning(f"Unknown location: {location}")
            return []
        
        species_code = self._species_to_ebird_code(species) if species else None
        raw_data = self.client.get_recent_observations(region_code, species_code, days)
        
        observations = []
        for obs in raw_data:
            try:
                observation = EBirdObservation(
                    species=obs.get('comName', ''),
                    location=obs.get('locName', ''),
                    timestamp=datetime.fromisoformat(obs.get('obsDt', '').replace('Z', '+00:00')),
                    observer=obs.get('userDisplayName', ''),
                    coordinates=Coordinates(
                        latitude=obs.get('lat', 0),
                        longitude=obs.get('lng', 0)
                    ) if obs.get('lat') and obs.get('lng') else None,
                    checklist_url=obs.get('subId', ''),
                    observation_count=obs.get('howMany', 1),
                    location_name=obs.get('locName', ''),
                    region_code=obs.get('subnational2Code', '')
                )
                observations.append(observation)
            except Exception as e:
                logger.error(f"Error parsing observation: {e}")
                continue
        
        self._cache_data(cache_key, observations)
        return observations
    
    def get_hotspot_activity(self, location: str, days: int = 7) -> List[HotspotActivity]:
        """Get hotspot activity for a location."""
        cache_key = f"hotspot_{location}_{days}"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key][1]

        region_code = self._location_to_region_code(location)
        if not region_code:
            logger.warning(f"Unknown location: {location}")
            return []

        raw_data = self.client.get_hotspots(region_code)
        
        activities = []
        for hotspot in raw_data[:5]:  # Limit to top 5 hotspots
            try:
                # Get recent observations for this hotspot
                hotspot_id = hotspot.get('locId', '')
                if hotspot_id:
                    observations = self.client.get_recent_observations(hotspot_id, days=days)
                    
                    activity = HotspotActivity(
                        hotspot_id=hotspot_id,
                        hotspot_name=hotspot.get('name', ''),
                        recent_observations=len(observations),
                        species_count=len(set(obs.get('comName', '') for obs in observations)),
                        last_updated=datetime.now(),
                        coordinates=Coordinates(
                            latitude=hotspot.get('lat', 0),
                            longitude=hotspot.get('lng', 0)
                        ) if hotspot.get('lat') and hotspot.get('lng') else None,
                        success_rate=len(observations) / 70.0  # Rough estimate
                    )
                    activities.append(activity)
            except Exception as e:
                logger.error(f"Error processing hotspot {hotspot.get('name', '')}: {e}")
                continue

        self._cache_data(cache_key, activities)
        return activities
    
    def get_trip_reports(self, location: str, days: int = 30) -> List[Dict]:
        """Get trip reports for a location (simulated based on recent observations)."""
        cache_key = f"trip_reports_{location}_{days}"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key][1]

        # Get recent observations to simulate trip reports
        observations = self.get_recent_observations(location, days=days)
        
        # Group observations by date and observer to create trip reports
        trip_reports = []
        date_groups = {}
        
        for obs in observations:
            date_key = obs.timestamp.strftime('%Y-%m-%d')
            if date_key not in date_groups:
                date_groups[date_key] = []
            date_groups[date_key].append(obs)
        
        # Create trip reports from grouped observations
        for date, day_observations in date_groups.items():
            if len(day_observations) >= 3:  # Only create reports for days with multiple observations
                # Group by observer
                observer_groups = {}
                for obs in day_observations:
                    observer = obs.observer or "Anonymous"
                    if observer not in observer_groups:
                        observer_groups[observer] = []
                    observer_groups[observer].append(obs)
                
                for observer, obs_list in observer_groups.items():
                    if len(obs_list) >= 2:  # Minimum 2 species for a trip report
                        trip_report = {
                            "date": date,
                            "observer": observer,
                            "location": location,
                            "species_count": len(set(obs.species for obs in obs_list)),
                            "total_observations": len(obs_list),
                            "species_list": list(set(obs.species for obs in obs_list)),
                            "hotspots_visited": list(set(obs.location for obs in obs_list)),
                            "trip_duration": "2-4 hours",  # Estimated
                            "weather_conditions": "Good",  # Placeholder
                            "highlights": self._generate_trip_highlights(obs_list),
                            "recommendations": self._generate_trip_recommendations(obs_list)
                        }
                        trip_reports.append(trip_report)
        
        self._cache_data(cache_key, trip_reports)
        return trip_reports
    
    def _generate_trip_highlights(self, observations: List[EBirdObservation]) -> List[str]:
        """Generate trip highlights from observations."""
        highlights = []
        
        # Find rare species (less than 5 observations)
        species_counts = {}
        for obs in observations:
            species_counts[obs.species] = species_counts.get(obs.species, 0) + 1
        
        rare_species = [species for species, count in species_counts.items() if count <= 2]
        if rare_species:
            highlights.append(f"Rare sightings: {', '.join(rare_species[:3])}")
        
        # Find high count observations
        high_counts = [obs for obs in observations if obs.observation_count and obs.observation_count > 10]
        if high_counts:
            highlights.append(f"Large flocks observed: {len(high_counts)} species")
        
        # Add general highlights
        highlights.append(f"Total species: {len(set(obs.species for obs in observations))}")
        highlights.append(f"Multiple hotspots visited: {len(set(obs.location for obs in observations))}")
        
        return highlights[:5]  # Limit to 5 highlights
    
    def _generate_trip_recommendations(self, observations: List[EBirdObservation]) -> List[str]:
        """Generate recommendations based on trip observations."""
        recommendations = []
        
        # Analyze timing
        morning_obs = [obs for obs in observations if 6 <= obs.timestamp.hour <= 10]
        if len(morning_obs) > len(observations) * 0.6:
            recommendations.append("Early morning birding was very productive")
        
        # Analyze locations
        locations = set(obs.location for obs in observations)
        if len(locations) >= 3:
            recommendations.append("Consider visiting fewer locations for longer periods")
        elif len(locations) == 1:
            recommendations.append("Good focus on single location - consider expanding to nearby hotspots")
        
        # Analyze species diversity
        species_count = len(set(obs.species for obs in observations))
        if species_count >= 15:
            recommendations.append("Excellent species diversity - consider returning during migration")
        elif species_count <= 5:
            recommendations.append("Low species count - try different habitats or seasons")
        
        return recommendations[:3]  # Limit to 3 recommendations
    
    def get_trip_insights(self, location: str, target_species: List[str], date_range: str) -> Dict:
        """Get insights from trip reports for planning."""
        trip_reports = self.get_trip_reports(location, days=30)
        
        insights = {
            "total_trips": len(trip_reports),
            "average_species_per_trip": 0,
            "best_timing": "Unknown",
            "top_hotspots": [],
            "target_species_success": {},
            "seasonal_patterns": {},
            "recommendations": []
        }
        
        if not trip_reports:
            return insights
        
        # Calculate averages
        total_species = sum(report["species_count"] for report in trip_reports)
        insights["average_species_per_trip"] = total_species / len(trip_reports)
        
        # Analyze timing
        morning_trips = [r for r in trip_reports if any("morning" in highlight.lower() for highlight in r["highlights"])]
        if len(morning_trips) > len(trip_reports) * 0.6:
            insights["best_timing"] = "Early morning (6-10 AM)"
        
        # Analyze hotspots
        hotspot_counts = {}
        for report in trip_reports:
            for hotspot in report["hotspots_visited"]:
                hotspot_counts[hotspot] = hotspot_counts.get(hotspot, 0) + 1
        
        insights["top_hotspots"] = sorted(hotspot_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Analyze target species success
        for species in target_species:
            success_count = 0
            for report in trip_reports:
                if species in report["species_list"]:
                    success_count += 1
            insights["target_species_success"][species] = success_count / len(trip_reports)
        
        # Generate recommendations
        if insights["average_species_per_trip"] < 10:
            insights["recommendations"].append("Consider visiting during peak migration periods")
        
        if len(insights["top_hotspots"]) > 0:
            insights["recommendations"].append(f"Focus on {insights['top_hotspots'][0][0]} for best results")
        
        return insights
    
    def predict_success_rate(self, species: str, location: str, date: str) -> float:
        """Predict success rate for seeing a species at a location"""
        # Get recent observations for the species
        observations = self.get_recent_observations(location, species, days=30)
        
        if not observations:
            return 0.0
        
        # Calculate success rate based on recent observations
        total_days = 30
        days_with_observations = len(set(
            obs.timestamp.date() for obs in observations
        ))
        
        success_rate = days_with_observations / total_days
        
        # Adjust based on seasonal patterns
        seasonal_factor = self._get_seasonal_factor(species, date)
        
        return min(1.0, success_rate * seasonal_factor)
    
    def get_rare_species_alerts(self, location: str, days: int = 1) -> List[EBirdObservation]:
        """Get alerts for rare species sightings"""
        # This would need to be enhanced with rarity data
        # For now, return recent observations
        return self.get_recent_observations(location, days=days)
    
    def _location_to_region_code(self, location: str) -> str:
        """Convert location name to eBird region code"""
        # Simplified mapping - in production, this would be more comprehensive
        location_mapping = {
            "New York": "US-NY",
            "California": "US-CA",
            "Texas": "US-TX",
            "Florida": "US-FL",
            "Alaska": "US-AK",
            "Hawaii": "US-HI"
        }
        return location_mapping.get(location, "US")
    
    def _species_to_ebird_code(self, species: str) -> str:
        """Convert species name to eBird species code"""
        # Simplified mapping - in production, this would use eBird's species API
        species_mapping = {
            "American Robin": "amerob",
            "Northern Cardinal": "norcar",
            "Blue Jay": "blujay",
            "Red-tailed Hawk": "rethaw",
            "American Goldfinch": "amegfi",
            "Baltimore Oriole": "balori",
            "Scarlet Tanager": "scatan",
            "Cerulean Warbler": "cerwar"
        }
        return species_mapping.get(species, species.lower().replace(" ", ""))
    
    def _calculate_success_rate(self, observations: List[Dict]) -> float:
        """Calculate success rate based on observations"""
        if not observations:
            return 0.0
        
        # Simple calculation: percentage of days with observations
        unique_dates = set(obs.get('obsDt', '')[:10] for obs in observations)
        return len(unique_dates) / 7.0  # 7 days period
    
    def _get_seasonal_factor(self, species: str, date: str) -> float:
        """Get seasonal factor for species availability"""
        # Simplified seasonal adjustment
        # In production, this would use detailed seasonal data
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d")
            month = target_date.month
            
            # Spring migration (March-May)
            if 3 <= month <= 5:
                return 1.2
            # Fall migration (September-November)
            elif 9 <= month <= 11:
                return 1.1
            # Winter (December-February)
            elif month in [12, 1, 2]:
                return 0.8
            # Summer (June-August)
            else:
                return 1.0
        except:
            return 1.0 