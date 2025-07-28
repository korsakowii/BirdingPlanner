"""
Application settings and configuration management.
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Settings:
    """Application settings."""
    
    # Application metadata
    app_name: str = "BirdingPlanner"
    app_version: str = "1.0.0"
    app_description: str = "AI-powered birding trip planning system"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # File paths
    base_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent)
    output_dir: Path = field(default_factory=lambda: Path("output"))
    data_dir: Path = field(default_factory=lambda: Path("data"))
    
    # Database settings
    database_url: Optional[str] = None
    database_echo: bool = False
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[Path] = None
    
    # API settings
    api_host: str = "localhost"
    api_port: int = 8000
    api_reload: bool = True
    
    # Content generation
    max_story_length: int = 500
    max_caption_length: int = 280
    default_language: str = "en"
    
    # Route planning
    max_route_stops: int = 5
    default_travel_speed: float = 60.0  # km/h
    max_route_distance: float = 5000.0  # km
    
    # Species classification
    tier_weights: Dict[str, float] = field(default_factory=lambda: {
        "occurrence_rate": 0.5,
        "region_count": 0.3,
        "visibility": 0.2
    })
    
    # External services
    weather_api_key: Optional[str] = None
    ebird_api_key: Optional[str] = None
    
    def __post_init__(self):
        """Post-initialization setup."""
        # Create directories if they don't exist
        self.output_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        
        # Set log file path
        if self.log_file is None:
            self.log_file = self.output_dir / "birdingplanner.log"
    
    @classmethod
    def from_env(cls) -> 'Settings':
        """Create settings from environment variables."""
        return cls(
            environment=os.getenv("ENVIRONMENT", "development"),
            debug=os.getenv("DEBUG", "true").lower() == "true",
            database_url=os.getenv("DATABASE_URL"),
            database_echo=os.getenv("DATABASE_ECHO", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            api_host=os.getenv("API_HOST", "localhost"),
            api_port=int(os.getenv("API_PORT", "8000")),
            weather_api_key=os.getenv("WEATHER_API_KEY"),
            ebird_api_key=os.getenv("EBIRD_API_KEY")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "environment": self.environment,
            "debug": self.debug,
            "base_dir": str(self.base_dir),
            "output_dir": str(self.output_dir),
            "data_dir": str(self.data_dir),
            "log_level": self.log_level,
            "api_host": self.api_host,
            "api_port": self.api_port,
            "max_route_stops": self.max_route_stops,
            "default_travel_speed": self.default_travel_speed,
            "max_route_distance": self.max_route_distance
        }


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings


def update_settings(**kwargs) -> Settings:
    """Update settings with new values."""
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    
    for key, value in kwargs.items():
        if hasattr(_settings, key):
            setattr(_settings, key, value)
    
    return _settings 