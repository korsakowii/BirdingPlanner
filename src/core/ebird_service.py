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
    
    def get_hotspot_activity(self, hotspot_id: str) -> Optional[HotspotActivity]:
        """Get activity information for a hotspot"""
        cache_key = f"hotspot_{hotspot_id}"
        
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key][1]
        
        hotspot_info = self.client.get_hotspot_info(hotspot_id)
        if not hotspot_info:
            return None
        
        # Get recent observations for this hotspot
        recent_obs = self.client.get_recent_observations(hotspot_id, days=7)
        species_count = len(set(obs.get('comName', '') for obs in recent_obs))
        
        activity = HotspotActivity(
            hotspot_id=hotspot_id,
            hotspot_name=hotspot_info.get('name', ''),
            recent_observations=len(recent_obs),
            species_count=species_count,
            last_updated=datetime.now(),
            coordinates=Coordinates(
                latitude=hotspot_info.get('latitude', 0),
                longitude=hotspot_info.get('longitude', 0)
            ) if hotspot_info.get('latitude') and hotspot_info.get('longitude') else None,
            success_rate=self._calculate_success_rate(recent_obs)
        )
        
        self._cache_data(cache_key, activity)
        return activity
    
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