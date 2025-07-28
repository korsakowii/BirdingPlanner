"""
BirdingPlanner - AI-powered birding trip planning system
A comprehensive platform for personalized birdwatching adventures.
"""

__version__ = "1.0.0"
__author__ = "BirdingPlanner Team"
__description__ = "AI-assisted birding trip planning with tier-based species classification"

from .core.birding_planner import BirdingPlanner
from .mcp.server import MCPServer
from .mcp.orchestrator import AgentOrchestrator
from .models.species import Species, SpeciesTier
from .models.route import Route, RouteStop
from .models.trip import TripPlan

__all__ = [
    "BirdingPlanner",
    "MCPServer",
    "AgentOrchestrator",
    "Species",
    "SpeciesTier",
    "Route",
    "RouteStop",
    "TripPlan"
] 