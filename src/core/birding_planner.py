"""
Main BirdingPlanner application class.
Orchestrates all services to create comprehensive birding trip plans.
"""

import logging
from typing import Dict, List, Optional
from ..models.trip import TripRequest, TripPlan, TripSummary, TripContent
from ..models.species import Species
from ..models.route import Route
from ..config.settings import get_settings
from .species_service import SpeciesService
from .route_service import RouteService
from .content_service import ContentService


class BirdingPlanner:
    """
    Main application class for BirdingPlanner.
    
    This class orchestrates all the services to create comprehensive
    birding trip plans with species classification, route optimization,
    and content generation.
    """
    
    def __init__(self, settings=None):
        """Initialize the BirdingPlanner application."""
        self.settings = settings or get_settings()
        self.logger = self._setup_logging()
        
        # Initialize services
        self.species_service = SpeciesService()
        self.route_service = RouteService()
        self.content_service = ContentService()
        
        self.logger.info("BirdingPlanner initialized successfully")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup application logging."""
        logger = logging.getLogger("BirdingPlanner")
        logger.setLevel(getattr(logging, self.settings.log_level))
        
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # File handler
            if self.settings.log_file:
                file_handler = logging.FileHandler(self.settings.log_file)
                file_handler.setLevel(logging.DEBUG)
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
                )
                file_handler.setFormatter(file_formatter)
                logger.addHandler(file_handler)
        
        return logger
    
    def create_trip_plan(self, request: TripRequest) -> TripPlan:
        """
        Create a complete birding trip plan.
        
        Args:
            request: TripRequest containing species, location, and date information
            
        Returns:
            TripPlan: Complete trip plan with all components
            
        Raises:
            ValueError: If the request is invalid
        """
        self.logger.info(f"Creating trip plan for {len(request.species)} species from {request.base_location}")
        
        # Validate request
        errors = request.validate()
        if errors:
            error_msg = "; ".join(errors)
            self.logger.error(f"Invalid trip request: {error_msg}")
            raise ValueError(f"Invalid trip request: {error_msg}")
        
        try:
            # Step 1: Classify species into tiers
            self.logger.info("Step 1: Classifying species into tiers...")
            species_data = self._classify_species(request.species)
            
            # Step 2: Analyze species availability
            self.logger.info("Step 2: Analyzing species availability...")
            species_availability = self._analyze_species_availability(
                request.species, request.date_range, request.base_location
            )
            
            # Step 3: Plan optimized route
            self.logger.info("Step 3: Planning optimized route...")
            route_data = self.route_service.optimize_route(
                request.base_location,
                request.species,
                request.date_range,
                max_stops=request.max_stops
            )
            
            # Step 4: Generate content
            self.logger.info("Step 4: Generating trip content...")
            content = self.content_service.generate_trip_content(
                route_data, species_data, request
            )
            
            # Step 5: Create trip summary
            trip_summary = TripSummary(
                base_location=request.base_location,
                target_species=request.species,
                date_range=request.date_range,
                total_stops=route_data.total_stops,
                total_distance_km=route_data.total_distance,
                estimated_time=route_data.estimated_total_time,
                species_tiers={s.name: s.tier.value for s in species_data}
            )
            
            # Step 6: Compile complete plan
            trip_plan = TripPlan(
                trip_overview=trip_summary,
                species_analysis={
                    "classifications": [s.to_dict() for s in species_data],
                    "availability": species_availability
                },
                route_plan=route_data,
                content=content
            )
            
            self.logger.info("Trip plan created successfully")
            return trip_plan
            
        except Exception as e:
            self.logger.error(f"Error creating trip plan: {str(e)}")
            raise
    
    def _classify_species(self, species_names: List[str]) -> List[Species]:
        """Classify species into tiers."""
        species_data = []
        for name in species_names:
            species = self.species_service.classify_species(name)
            species_data.append(species)
            self.logger.debug(f"Classified {name} as {species.tier.value}")
        return species_data
    
    def _analyze_species_availability(self, species_names: List[str], 
                                    date_range: str, base_location: str) -> List[Dict]:
        """Analyze species availability for the given parameters."""
        month = self._extract_month_from_date_range(date_range)
        region = self._get_region_from_location(base_location)
        
        availability_data = []
        for name in species_names:
            availability = self.species_service.get_species_availability(name, month, region)
            availability_data.append(availability)
            self.logger.debug(f"Availability for {name}: {availability['confidence_score']}% confidence")
        return availability_data
    
    def _extract_month_from_date_range(self, date_range: str) -> str:
        """Extract month from date range string."""
        month_mapping = {
            "spring": "April",
            "summer": "July",
            "fall": "October",
            "winter": "January",
            "Spring": "April",
            "Summer": "July",
            "Fall": "October",
            "Winter": "January"
        }
        
        for season, month in month_mapping.items():
            if season in date_range:
                return month
        
        return "April"  # Default
    
    def _get_region_from_location(self, location: str) -> str:
        """Map location to region for species availability."""
        region_mapping = {
            "New York": "Northeast",
            "Boston": "Northeast",
            "Chicago": "Midwest",
            "Miami": "Southeast",
            "San Francisco": "West Coast"
        }
        
        return region_mapping.get(location, "Northeast")
    
    def get_species_info(self, name: str) -> Optional[Species]:
        """Get detailed information about a species."""
        return self.species_service.get_species(name)
    
    def get_all_species(self) -> List[Species]:
        """Get all species in the database."""
        return self.species_service.get_all_species()
    
    def get_route_suggestions(self, base_location: str, 
                            target_species: List[str]) -> List[Dict]:
        """Get route suggestions for given species and location."""
        return self.route_service.get_suggestions(base_location, target_species)
    
    def generate_story(self, species: str, location: str) -> str:
        """Generate a story for a species encounter."""
        return self.content_service.generate_story_card(species, location)
    
    def generate_social_caption(self, species: str, location: str, 
                              tier: str) -> str:
        """Generate a social media caption for a species sighting."""
        return self.content_service.generate_social_caption(species, location, tier)
    
    def save_trip_plan(self, trip_plan: TripPlan, output_dir: str = None) -> str:
        """Save a trip plan to files."""
        if output_dir is None:
            output_dir = str(self.settings.output_dir)
        
        return trip_plan.save_to_files(output_dir)
    
    def get_application_info(self) -> Dict:
        """Get application information and status."""
        return {
            "name": self.settings.app_name,
            "version": self.settings.app_version,
            "description": self.settings.app_description,
            "environment": self.settings.environment,
            "species_count": len(self.species_service.get_all_species()),
            "settings": self.settings.to_dict()
        } 