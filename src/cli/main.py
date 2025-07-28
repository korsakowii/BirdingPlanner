"""
Command-line interface for BirdingPlanner.
"""

import argparse
import sys
from pathlib import Path
from typing import List

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.birding_planner import BirdingPlanner
from src.mcp.server import MCPServer
from src.models.trip import TripRequest
from src.config.settings import get_settings


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="BirdingPlanner - AI-powered birding trip planning system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a basic trip plan
  python -m src.cli.main plan --species "American Robin" "Northern Cardinal" --location "New York" --date "Spring 2024"
  
  # Create a trip plan with custom output directory
  python -m src.cli.main plan --species "Cerulean Warbler" --location "Boston" --date "Summer 2024" --output "my_trip"
  
  # Get species information
  python -m src.cli.main species --name "American Robin"
  
  # List all available species
  python -m src.cli.main species --list
  
  # Get application information
  python -m src.cli.main info
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Plan command
    plan_parser = subparsers.add_parser('plan', help='Create a birding trip plan')
    plan_parser.add_argument('--species', nargs='+', required=True, 
                           help='Target bird species')
    plan_parser.add_argument('--location', required=True, 
                           help='Base location for the trip')
    plan_parser.add_argument('--date', required=True, 
                           help='Date range for the trip')
    plan_parser.add_argument('--stops', type=int, default=3, 
                           help='Maximum number of stops (default: 3)')
    plan_parser.add_argument('--output', default='output', 
                           help='Output directory (default: output)')
    plan_parser.add_argument('--verbose', '-v', action='store_true', 
                           help='Verbose output')
    plan_parser.add_argument('--ai', action='store_true', 
                           help='Use AI agents for enhanced planning')
    
    # Species command
    species_parser = subparsers.add_parser('species', help='Species information')
    species_parser.add_argument('--name', help='Species name to look up')
    species_parser.add_argument('--list', action='store_true', 
                              help='List all available species')
    
    # MCP command
    mcp_parser = subparsers.add_parser('mcp', help='MCP Server and AI Agent operations')
    mcp_parser.add_argument('--interactive', '-i', action='store_true', 
                           help='Run MCP server in interactive mode')
    mcp_parser.add_argument('--status', action='store_true', 
                           help='Show MCP server status')
    mcp_parser.add_argument('--health', action='store_true', 
                           help='Perform health check')
    mcp_parser.add_argument('--capabilities', action='store_true', 
                           help='Show agent capabilities')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Application information')
    
    return parser


def plan_command(args, planner: BirdingPlanner, mcp_server: MCPServer = None):
    """Handle the plan command."""
    print("🦅 BirdingPlanner - Creating Your Trip Plan")
    print("=" * 50)
    
    # Create trip request
    request = TripRequest(
        species=args.species,
        base_location=args.location,
        date_range=args.date,
        max_stops=args.stops
    )
    
    print(f"Target Species: {', '.join(request.species)}")
    print(f"Base Location: {request.base_location}")
    print(f"Date Range: {request.date_range}")
    print(f"Max Stops: {request.max_stops}")
    print(f"AI Enhanced: {args.ai}")
    print()
    
    try:
        # Choose planning method
        if args.ai and mcp_server:
            print("🤖 Using AI Agents for enhanced planning...")
            trip_plan = mcp_server.create_trip_plan(
                species=args.species,
                base_location=args.location,
                date_range=args.date,
                max_stops=args.stops,
                output_dir=args.output
            )
        else:
            print("📋 Using standard planning...")
            trip_plan = planner.create_trip_plan(request)
            # Save to files
            save_message = planner.save_trip_plan(trip_plan, args.output)
            print(f"✅ {save_message}")
        
        # Print summary
        print("\n📋 Trip Plan Summary:")
        print(f"   Base Location: {trip_plan.trip_overview.base_location}")
        print(f"   Target Species: {', '.join(trip_plan.trip_overview.target_species)}")
        print(f"   Total Stops: {trip_plan.trip_overview.total_stops}")
        print(f"   Total Distance: {trip_plan.trip_overview.total_distance_km:.1f} km")
        print(f"   Estimated Time: {trip_plan.trip_overview.estimated_time}")
        
        print("\n🎯 Species Tiers:")
        for species, tier in trip_plan.trip_overview.species_tiers.items():
            print(f"   {species}: {tier}")
        
        print("\n📁 Generated Files:")
        print(f"   - {args.output}/trip_plan.md (Complete trip plan)")
        print(f"   - {args.output}/story_cards/ (Individual story cards)")
        print(f"   - {args.output}/social_captions.txt (Social media content)")
        
        if args.verbose:
            print("\n🔍 Detailed Analysis:")
            for availability in trip_plan.species_analysis["availability"]:
                print(f"   {availability['species']}: {availability['confidence_score']}% confidence")
                print(f"      Recommendation: {availability['recommendation']}")
        
        print("\n✨ Your birding adventure awaits! Happy birding!")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def species_command(args, planner: BirdingPlanner):
    """Handle the species command."""
    if args.list:
        print("🦅 Available Species in Database")
        print("=" * 40)
        species_list = planner.get_all_species()
        for species in species_list:
            print(f"   {species.name} ({species.scientific_name}) - {species.tier.value}")
        print(f"\nTotal: {len(species_list)} species")
    
    elif args.name:
        print(f"🦅 Species Information: {args.name}")
        print("=" * 40)
        species = planner.get_species_info(args.name)
        if species:
            print(f"Name: {species.name}")
            print(f"Scientific Name: {species.scientific_name}")
            print(f"Tier: {species.tier.value} - {species.tier_description}")
            print(f"Occurrence Rate: {species.occurrence_rate:.2f}")
            print(f"Region Count: {species.region_count}")
            print(f"Visibility: {species.visibility}")
            print(f"Challenge: {species.tier_challenge}")
            
            if species.availability:
                print(f"\nAvailability:")
                print(f"  Best Months: {', '.join(species.availability.best_months)}")
                print(f"  Regions: {', '.join(species.availability.regions)}")
                print(f"  Peak Activity: {species.availability.peak_activity.value}")
                print(f"  Migration Pattern: {species.availability.migration_pattern.value}")
        else:
            print(f"❌ Species '{args.name}' not found in database")
            print("💡 Use --list to see all available species")
    
    else:
        print("❌ Please specify either --name or --list")
        sys.exit(1)


def info_command(planner: BirdingPlanner):
    """Handle the info command."""
    print("🦅 BirdingPlanner Application Information")
    print("=" * 50)
    
    app_info = planner.get_application_info()
    
    print(f"Name: {app_info['name']}")
    print(f"Version: {app_info['version']}")
    print(f"Description: {app_info['description']}")
    print(f"Environment: {app_info['environment']}")
    print(f"Species in Database: {app_info['species_count']}")
    
    print(f"\nSettings:")
    settings = app_info['settings']
    for key, value in settings.items():
        if key != 'settings':  # Avoid recursive display
            print(f"  {key}: {value}")


def mcp_command(args, mcp_server: MCPServer):
    """Handle the MCP command."""
    if args.interactive:
        mcp_server.run_interactive_mode()
    elif args.status:
        status = mcp_server.get_server_status()
        print("🦅 MCP Server Status")
        print("=" * 30)
        print(f"Server Status: {status['server']['status']}")
        print(f"Uptime: {status['server']['uptime_seconds']:.1f} seconds")
        print(f"Requests: {status['server']['request_count']}")
        print(f"Agents: {status['agents']['total_agents']}")
        print(f"Orchestrator: {status['agents']['orchestrator']}")
    elif args.health:
        health = mcp_server.health_check()
        print("🦅 MCP Server Health Check")
        print("=" * 30)
        print(f"Status: {health['status']}")
        print(f"Agents Healthy: {health['agents_healthy']}")
        print(f"Total Agents: {health['total_agents']}")
        print(f"Uptime: {health['server_uptime']:.1f} seconds")
    elif args.capabilities:
        capabilities = mcp_server.get_agent_capabilities()
        print("🦅 AI Agent Capabilities")
        print("=" * 30)
        for agent, caps in capabilities.items():
            print(f"{agent}:")
            for cap in caps:
                print(f"  - {cap}")
            print()
    else:
        print("❌ Please specify an MCP operation (--interactive, --status, --health, --capabilities)")


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Initialize services
        settings = get_settings()
        planner = BirdingPlanner(settings)
        mcp_server = MCPServer(settings)
        
        # Handle commands
        if args.command == 'plan':
            plan_command(args, planner, mcp_server)
        elif args.command == 'species':
            species_command(args, planner)
        elif args.command == 'mcp':
            mcp_command(args, mcp_server)
        elif args.command == 'info':
            info_command(planner)
        else:
            print(f"❌ Unknown command: {args.command}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 