"""
Logging configuration for BirdingPlanner.
"""

from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class LoggingConfig:
    """Logging configuration settings."""
    
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[Path] = None
    console_output: bool = True
    file_output: bool = False
    
    @classmethod
    def from_env(cls) -> 'LoggingConfig':
        """Create logging config from environment variables."""
        import os
        return cls(
            level=os.getenv("LOG_LEVEL", "INFO"),
            file_output=os.getenv("LOG_FILE", "").lower() == "true"
        ) 