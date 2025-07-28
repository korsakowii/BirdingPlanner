"""
Database configuration for BirdingPlanner.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    
    url: Optional[str] = None
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Create database config from environment variables."""
        import os
        return cls(
            url=os.getenv("DATABASE_URL"),
            echo=os.getenv("DATABASE_ECHO", "false").lower() == "true"
        ) 