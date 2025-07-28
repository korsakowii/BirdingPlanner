#!/usr/bin/env python3
"""
BirdingPlanner Hybrid Architecture Demo
Demonstrates the combination of AI Agents and Service Layer architecture.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.birding_planner import BirdingPlanner
from src.mcp.server import MCPServer
from src.models.trip import TripRequest
from src.config.settings import get_settings


def demo_standard_planning():
    """Demonstrate standard service layer planning."""
    print("🦅 Standard Service Layer Planning")
    print("=" * 50)
    
    # Initialize standard planner
    settings = get_settings()
    planner = BirdingPlanner(settings)
    
    # Create trip request
    request = TripRequest(
        species=["American Robin", "Northern Cardinal", "Blue Jay"],
        base_location="New York",
        date_range="Spring 2024",
        max_stops=3
    )
    
    print(f"Target Species: {', '.join(request.species)}")
    print(f"Base Location: {request.base_location}")
    print(f"Date Range: {request.date_range}")
    print()
    
    # Generate trip plan
    trip_plan = planner.create_trip_plan(request)
    
    print("📋 Standard Trip Plan Summary:")
    print(f"   Total Stops: {trip_plan.trip_overview.total_stops}")
    print(f"   Total Distance: {trip_plan.trip_overview.total_distance_km:.1f} km")
    print(f"   Estimated Time: {trip_plan.trip_overview.estimated_time}")
    print()
    
    return trip_plan


def demo_ai_enhanced_planning():
    """Demonstrate AI agent enhanced planning."""
    print("🤖 AI Agent Enhanced Planning")
    print("=" * 50)
    
    # Initialize MCP Server
    settings = get_settings()
    mcp_server = MCPServer(settings)
    
    # Show agent capabilities
    print("AI Agent Capabilities:")
    capabilities = mcp_server.get_agent_capabilities()
    for agent, caps in capabilities.items():
        print(f"  {agent}: {', '.join(caps)}")
    print()
    
    # Create AI-enhanced trip plan
    trip_plan = mcp_server.create_trip_plan(
        species=["American Robin", "Northern Cardinal", "Blue Jay"],
        base_location="New York",
        date_range="Spring 2024",
        max_stops=3,
        output_dir="demo_ai_output"
    )
    
    print("📋 AI-Enhanced Trip Plan Summary:")
    print(f"   Total Stops: {trip_plan.trip_overview.total_stops}")
    print(f"   Total Distance: {trip_plan.trip_overview.total_distance_km:.1f} km")
    print(f"   Estimated Time: {trip_plan.trip_overview.estimated_time}")
    print()
    
    return trip_plan


def demo_agent_status():
    """Demonstrate agent status monitoring."""
    print("📊 AI Agent Status Monitoring")
    print("=" * 50)
    
    # Initialize MCP Server
    settings = get_settings()
    mcp_server = MCPServer(settings)
    
    # Get server status
    status = mcp_server.get_server_status()
    print(f"Server Status: {status['server']['status']}")
    print(f"Uptime: {status['server']['uptime_seconds']:.1f} seconds")
    print(f"Requests: {status['server']['request_count']}")
    print(f"Total Agents: {status['agents']['total_agents']}")
    print()
    
    # Get health check
    health = mcp_server.health_check()
    print(f"Health Status: {health['status']}")
    print(f"Agents Healthy: {health['agents_healthy']}")
    print(f"Total Agents: {health['total_agents']}")
    print()


def demo_agent_task_execution():
    """Demonstrate individual agent task execution."""
    print("⚙️ Individual Agent Task Execution")
    print("=" * 50)
    
    # Initialize MCP Server
    settings = get_settings()
    mcp_server = MCPServer(settings)
    
    # Execute species analysis task
    print("Executing SpeciesAgent task...")
    species_result = mcp_server.execute_agent_task(
        agent_name="SpeciesAgent",
        task_type="species_classification",
        input_data={
            "species": ["American Robin"],
            "location": "New York",
            "date_range": "Spring 2024"
        }
    )
    
    print(f"SpeciesAgent Success: {species_result['success']}")
    if species_result['success']:
        species_data = species_result['data']
        classifications = species_data.get('species_analysis', {}).get('classifications', [])
        for classification in classifications:
            print(f"  {classification['species']}: Tier {classification['tier']} "
                  f"(Confidence: {classification['confidence_score']:.1%})")
    print()


def main():
    """Run the hybrid architecture demo."""
    print("🦅 BirdingPlanner Hybrid Architecture Demo")
    print("=" * 60)
    print("This demo showcases the combination of:")
    print("  • Standard Service Layer Architecture")
    print("  • AI Agent Orchestration")
    print("  • MCP Server Implementation")
    print("  • Intelligent Task Management")
    print()
    
    try:
        # Demo 1: Standard Planning
        demo_standard_planning()
        
        # Demo 2: AI Enhanced Planning
        demo_ai_enhanced_planning()
        
        # Demo 3: Agent Status
        demo_agent_status()
        
        # Demo 4: Individual Agent Tasks
        demo_agent_task_execution()
        
        print("✅ Demo completed successfully!")
        print()
        print("📁 Generated Files:")
        print("  - demo_ai_output/trip_plan.md (AI-enhanced trip plan)")
        print("  - demo_ai_output/story_cards/ (AI-generated stories)")
        print("  - demo_ai_output/social_captions/ (AI-optimized captions)")
        print()
        print("🎯 Key Features Demonstrated:")
        print("  • AI-powered species classification with confidence scoring")
        print("  • Machine learning route optimization")
        print("  • Natural language content generation")
        print("  • Intelligent agent orchestration")
        print("  • Fallback to standard planning if AI fails")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 