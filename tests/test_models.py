"""
Tests for BirdingPlanner data models.
"""

import pytest
from datetime import datetime
from src.models.species import Species, SpeciesTier, SpeciesAvailability, ActivityTime, MigrationPattern
from src.models.route import Coordinates, Location, Hotspot, Route, RouteStop
from src.models.trip import TripRequest, TripPlan, TripSummary


class TestSpecies:
    """Test Species model."""
    
    def test_species_creation(self):
        """Test basic species creation."""
        species = Species(
            name="Test Bird",
            scientific_name="Testus birdus",
            tier=SpeciesTier.COMMON_COMPANION
        )
        
        assert species.name == "Test Bird"
        assert species.scientific_name == "Testus birdus"
        assert species.tier == SpeciesTier.COMMON_COMPANION
        assert species.availability is not None
    
    def test_tier_description(self):
        """Test tier description generation."""
        species = Species(name="Test", tier=SpeciesTier.COMMON_COMPANION)
        assert "Common Companion" in species.tier_description
    
    def test_tier_challenge(self):
        """Test tier challenge generation."""
        species = Species(name="Test", tier=SpeciesTier.ELUSIVE_EXPLORER)
        assert "Patience and persistence" in species.tier_challenge
    
    def test_to_dict(self):
        """Test dictionary conversion."""
        species = Species(
            name="Test Bird",
            tier=SpeciesTier.REGIONAL_COMPANION,
            occurrence_rate=0.6
        )
        
        data = species.to_dict()
        assert data["name"] == "Test Bird"
        assert data["tier"] == "T2"
        assert data["occurrence_rate"] == 0.6
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "name": "Test Bird",
            "tier": "T3",
            "occurrence_rate": 0.4,
            "availability": {
                "best_months": ["April", "May"],
                "regions": ["Northeast"],
                "peak_activity": "morning",
                "migration_pattern": "long_distance"
            }
        }
        
        species = Species.from_dict(data)
        assert species.name == "Test Bird"
        assert species.tier == SpeciesTier.SEASONAL_VISITOR
        assert species.occurrence_rate == 0.4


class TestSpeciesAvailability:
    """Test SpeciesAvailability model."""
    
    def test_availability_creation(self):
        """Test basic availability creation."""
        availability = SpeciesAvailability(
            best_months=["April", "May"],
            regions=["Northeast"],
            peak_activity=ActivityTime.MORNING
        )
        
        assert "April" in availability.best_months
        assert "Northeast" in availability.regions
        assert availability.peak_activity == ActivityTime.MORNING
    
    def test_is_available_in_month(self):
        """Test month availability check."""
        availability = SpeciesAvailability(best_months=["April", "May"])
        assert availability.is_available_in_month("April") is True
        assert availability.is_available_in_month("December") is False
    
    def test_is_found_in_region(self):
        """Test region availability check."""
        availability = SpeciesAvailability(regions=["Northeast", "Midwest"])
        assert availability.is_found_in_region("Northeast") is True
        assert availability.is_found_in_region("West Coast") is False


class TestCoordinates:
    """Test Coordinates model."""
    
    def test_distance_calculation(self):
        """Test distance calculation between coordinates."""
        coord1 = Coordinates(latitude=40.7128, longitude=-74.0060)  # New York
        coord2 = Coordinates(latitude=34.0522, longitude=-118.2437)  # Los Angeles
        
        distance = coord1.distance_to(coord2)
        assert distance > 3000  # Should be roughly 4000+ km
        assert distance < 5000


class TestLocation:
    """Test Location model."""
    
    def test_location_creation(self):
        """Test basic location creation."""
        coords = Coordinates(latitude=40.7128, longitude=-74.0060)
        location = Location(
            name="New York",
            region="Northeast",
            coordinates=coords
        )
        
        assert location.name == "New York"
        assert location.region == "Northeast"
        assert location.coordinates == coords
    
    def test_get_best_hotspots(self):
        """Test hotspot sorting."""
        coords = Coordinates(latitude=40.7128, longitude=-74.0060)
        hotspot1 = Hotspot("Park A", coords, species_count=50)
        hotspot2 = Hotspot("Park B", coords, species_count=100)
        hotspot3 = Hotspot("Park C", coords, species_count=25)
        
        location = Location(
            name="Test City",
            region="Test Region",
            coordinates=coords,
            hotspots=[hotspot1, hotspot2, hotspot3]
        )
        
        best_hotspots = location.get_best_hotspots(limit=2)
        assert len(best_hotspots) == 2
        assert best_hotspots[0].species_count == 100
        assert best_hotspots[1].species_count == 50


class TestTripRequest:
    """Test TripRequest model."""
    
    def test_valid_request(self):
        """Test valid trip request."""
        request = TripRequest(
            species=["American Robin", "Northern Cardinal"],
            base_location="New York",
            date_range="Spring 2024"
        )
        
        errors = request.validate()
        assert len(errors) == 0
    
    def test_invalid_request(self):
        """Test invalid trip request."""
        request = TripRequest(
            species=[],  # Empty species list
            base_location="",  # Empty location
            date_range="",  # Empty date range
            max_stops=0  # Invalid stops
        )
        
        errors = request.validate()
        assert len(errors) == 4
        assert "At least one target species must be specified" in errors
        assert "Base location must be specified" in errors
        assert "Date range must be specified" in errors
        assert "Maximum stops must be at least 1" in errors


class TestTripSummary:
    """Test TripSummary model."""
    
    def test_trip_summary_creation(self):
        """Test basic trip summary creation."""
        summary = TripSummary(
            base_location="New York",
            target_species=["American Robin"],
            date_range="Spring 2024",
            total_stops=3,
            total_distance_km=1500.0,
            estimated_time="48 hours"
        )
        
        assert summary.base_location == "New York"
        assert len(summary.target_species) == 1
        assert summary.total_stops == 3
        assert summary.total_distance_km == 1500.0
    
    def test_to_dict(self):
        """Test dictionary conversion."""
        summary = TripSummary(
            base_location="Test",
            target_species=["Bird"],
            date_range="Test 2024",
            total_stops=1,
            total_distance_km=100.0,
            estimated_time="2 hours"
        )
        
        data = summary.to_dict()
        assert data["base_location"] == "Test"
        assert data["total_stops"] == 1
        assert data["total_distance_km"] == 100.0 