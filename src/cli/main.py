"""
Command-line interface for BirdingPlanner.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict
import os

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
  
  # Use minimum stops for high success probability
  python -m src.cli.main plan --species "American Robin" "Northern Cardinal" --location "New York" --date "Spring 2024" --min-stops --verbose
  
  # Target specific success rate
  python -m src.cli.main plan --species "Cerulean Warbler" --location "New York" --date "Spring 2024" --success-rate 0.8
  
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
    plan_parser.add_argument('--min-stops', action='store_true',
                           help='Use minimum stops for high success probability')
    plan_parser.add_argument('--success-rate', type=float, 
                           help='Target success rate (0.0-1.0) for species sightings')
    plan_parser.add_argument('--output', default='output', 
                           help='Output directory (default: output)')
    plan_parser.add_argument('--ai', action='store_true', 
                           help='Use AI-enhanced planning with MCP server')
    plan_parser.add_argument('--verbose', action='store_true',
                           help='Show detailed output')
    
    # Add multi-day planning arguments
    plan_parser.add_argument('--multi-day', type=int, metavar='DAYS',
                           help='Create multi-day plan (specify number of days)')
    plan_parser.add_argument('--max-distance-per-day', type=float, default=50.0,
                           help='Maximum walking distance per day in km (default: 50.0)')
    plan_parser.add_argument('--optimize-efficiency', action='store_true',
                           help='Optimize for maximum species per distance walked')
    
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
    
    # Get route service for success probability calculations
    route_service = planner.route_service
    
    # Show success probability analysis if requested
    if args.min_stops or args.success_rate:
        print("📊 Success Probability Analysis")
        print("-" * 30)
        
        min_stops_info = route_service.calculate_success_probability(args.location, args.species, 1)
        if "error" not in min_stops_info:
            recommended_stops = min_stops_info.get("recommended_min_stops", {}).get("recommended_stops", 1)
            reasoning = min_stops_info.get("recommended_min_stops", {}).get("reasoning", "Unknown")
            
            print(f"Recommended minimum stops: {recommended_stops}")
            print(f"Reasoning: {reasoning}")
            print()
            
            print("Success probabilities by stop count:")
            for stops in range(1, 6):
                success_info = route_service.calculate_success_probability(args.location, args.species, stops)
                if "error" not in success_info:
                    print(f"   {stops} stop(s): {success_info['overall_success_rate']:.1%} overall success rate")
    
    # Handle multi-day planning
    if args.multi_day:
        print(f"🗺️ Creating {args.multi_day}-day optimized birding plan...")
        print(f"📍 Base Location: {args.location}")
        print(f"🎯 Target Species: {', '.join(args.species)}")
        print(f"📅 Date Range: {args.date}")
        print(f"🚶 Max Distance per Day: {args.max_distance_per_day} km")
        print()
        
        # Create multi-day plan
        multi_day_plan = route_service.create_multi_day_plan(
            base_location=args.location,
            target_species=args.species,
            date_range=args.date,
            days=args.multi_day,
            max_distance_per_day=args.max_distance_per_day
        )
        
        # Display multi-day plan
        print("📋 Multi-Day Birding Plan Summary")
        print("=" * 50)
        
        overall_stats = multi_day_plan['overall_stats']
        print(f"🎯 Overall Statistics:")
        print(f"   Total Species Expected: {overall_stats['total_species_expected']}")
        print(f"   Total Distance: {overall_stats['total_distance']:.1f} km")
        print(f"   Average Distance per Day: {overall_stats['average_distance_per_day']:.1f} km")
        print(f"   Overall Success Probability: {overall_stats['overall_success_probability']:.1%}")
        print(f"   Species Coverage: {overall_stats['species_coverage']:.1%}")
        print(f"   Efficiency Score: {overall_stats['efficiency_score']:.1f} species per 10km")
        print()
        
        # Display daily plans with detailed routes
        for day_plan in multi_day_plan['daily_plans']:
            print(f"📅 Day {day_plan['day']}")
            print(f"   Expected Species: {len(day_plan['expected_species'])}")
            print(f"   Total Distance: {day_plan['total_distance']:.1f} km")
            print(f"   Success Probability: {day_plan['day_success_probability']:.1%}")
            print(f"   Efficiency Score: {day_plan['efficiency_score']:.1f}")
            
            # Show daily summary
            if 'daily_summary' in day_plan:
                print(f"   Summary: {day_plan['daily_summary']}")
            
            # Show detailed route stops
            if 'route_stops' in day_plan and day_plan['route_stops']:
                print(f"   Detailed Route:")
                for route_stop in day_plan['route_stops']:
                    print(f"     Stop {route_stop['stop_number']}: {route_stop['hotspot_name']}")
                    print(f"        Time: {route_stop['viewing_time']}")
                    print(f"        Distance: {route_stop['distance_from_previous']:.1f} km")
                    print(f"        Target Species: {', '.join(route_stop['target_species'])}")
                    print(f"        Success Rate: {route_stop['success_probability']:.1%}")
                    if route_stop['recommendations']:
                        print(f"        Tips: {route_stop['recommendations'][0]}")
                    print()
            
            # Show daily schedule
            if 'daily_schedule' in day_plan and day_plan['daily_schedule']:
                print(f"   Daily Schedule:")
                for schedule_item in day_plan['daily_schedule']:
                    if schedule_item['type'] == 'travel':
                        print(f"     {schedule_item['time']}: {schedule_item['activity']} ({schedule_item['duration']})")
                    else:
                        print(f"     {schedule_item['time']}: {schedule_item['activity']} ({schedule_item['duration']})")
                        if schedule_item['target_species']:
                            print(f"        Target: {', '.join(schedule_item['target_species'])}")
            print()
        
        # Save multi-day plan
        output_dir = args.output
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as JSON for programmatic access
        import json
        with open(os.path.join(output_dir, 'multi_day_plan.json'), 'w') as f:
            json.dump(multi_day_plan, f, indent=2, default=str)
        
        # Generate markdown report
        markdown_content = generate_multi_day_markdown(multi_day_plan)
        with open(os.path.join(output_dir, 'multi_day_plan.md'), 'w') as f:
            f.write(markdown_content)
        
        print(f"✅ Multi-day plan saved to {output_dir}/ directory")
        print(f"📁 Files generated:")
        print(f"   - {output_dir}/multi_day_plan.md (Complete plan report)")
        print(f"   - {output_dir}/multi_day_plan.json (Structured data)")
        
        return
    
    optimal_stops = args.stops
    if args.success_rate:
        # Logic to find minimum stops that meet target success rate
        for stops in range(1, 6):
            success_info = route_service.calculate_success_probability(args.location, args.species, stops)
            if "error" not in success_info and success_info["overall_success_rate"] >= args.success_rate:
                optimal_stops = stops
                break
        else:
            optimal_stops = 5  # Use maximum if target can't be met
    elif args.min_stops:
        optimal_stops = min_stops_info.get("recommended_min_stops", {}).get("recommended_stops", 1)
    
    # Create trip request
    request = TripRequest(
        species=args.species,
        base_location=args.location,
        date_range=args.date,
        max_stops=optimal_stops
    )
    
    print(f"Target Species: {', '.join(request.species)}")
    print(f"Base Location: {request.base_location}")
    print(f"Date Range: {request.date_range}")
    print(f"Optimal Stops: {optimal_stops}")
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
        
        # Show success probability for this plan
        success_info = route_service.calculate_success_probability(
            args.location, args.species, trip_plan.trip_overview.total_stops
        )
        if "error" not in success_info:
            print(f"   Success Rate: {success_info['overall_success_rate']:.1%}")
        
        print("\n🎯 Species Tiers:")
        for species, tier in trip_plan.trip_overview.species_tiers.items():
            print(f"   {species}: {tier}")
            if "error" not in success_info and species in success_info["species_probabilities"]:
                prob = success_info["species_probabilities"][species]
                print(f"     (Success probability: {prob:.1%})")
        
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


def generate_multi_day_markdown(multi_day_plan: Dict) -> str:
    """Generate markdown report for multi-day birding plan."""
    base_location = multi_day_plan['base_location']
    target_species = multi_day_plan['target_species']
    date_range = multi_day_plan['date_range']
    total_days = multi_day_plan['total_days']
    overall_stats = multi_day_plan['overall_stats']
    daily_plans = multi_day_plan['daily_plans']
    
    markdown = f"""# Multi-Day Birding Plan: {base_location}

## 🦅 Plan Overview
- **Base Location**: {base_location}
- **Target Species**: {', '.join(target_species)}
- **Date Range**: {date_range}
- **Total Days**: {total_days}
- **Total Species Expected**: {overall_stats['total_species_expected']}
- **Total Distance**: {overall_stats['total_distance']:.1f} km
- **Average Distance per Day**: {overall_stats['average_distance_per_day']:.1f} km
- **Overall Success Probability**: {overall_stats['overall_success_probability']:.1%}
- **Species Coverage**: {overall_stats['species_coverage']:.1%}
- **Efficiency Score**: {overall_stats['efficiency_score']:.1f} species per 10km

## 🎯 Optimization Strategy
This plan is optimized for:
- **Maximum species diversity** with minimal walking distance
- **Efficient route planning** to minimize travel time between hotspots
- **High success probability** based on species availability and habitat compatibility
- **Balanced daily schedules** to avoid fatigue while maximizing sightings

## 📅 Daily Plans

"""
    
    for day_plan in daily_plans:
        day_num = day_plan['day']
        expected_species = day_plan['expected_species']
        total_distance = day_plan['total_distance']
        success_prob = day_plan['day_success_probability']
        efficiency = day_plan['efficiency_score']
        hotspots = day_plan['hotspots']
        
        markdown += f"""### Day {day_num}

**Daily Statistics:**
- **Expected Species**: {len(expected_species)}
- **Total Distance**: {total_distance:.1f} km
- **Success Probability**: {success_prob:.1%}
- **Efficiency Score**: {efficiency:.1f}

**Target Species for Today:**
"""
        
        for species in expected_species:
            markdown += f"- {species}\n"
        
        markdown += "\n**Hotspots to Visit:**\n"
        
        for i, hotspot_info in enumerate(hotspots, 1):
            hotspot = hotspot_info['hotspot']
            distance = hotspot_info['distance_from_previous']
            unique_species = hotspot_info['unique_species']
            
            markdown += f"\n#### {i}. {hotspot['name']}\n"
            if distance > 0:
                markdown += f"- **Distance from previous**: {distance:.1f} km\n"
            if unique_species:
                markdown += f"- **Key species**: {', '.join(unique_species)}\n"
            if hotspot.get('description'):
                markdown += f"- **Description**: {hotspot['description']}\n"
        
        markdown += "\n**Daily Tips:**\n"
        markdown += "- Start early for best birding conditions\n"
        markdown += "- Take breaks between hotspots to rest and observe\n"
        markdown += "- Keep detailed notes of species seen\n"
        markdown += "- Check weather conditions before starting\n\n"
    
    markdown += """## 📋 Packing List
- Binoculars (8x42 or 10x42 recommended)
- Field guide or birding app
- Camera with telephoto lens
- Comfortable walking shoes
- Weather-appropriate clothing
- Water and energy snacks
- Notebook for observations
- Sun protection (hat, sunscreen)
- First aid kit
- Mobile phone with GPS

## 💡 Multi-Day Birding Tips
- **Pace yourself**: Don't try to see everything on the first day
- **Keep records**: Document species seen each day to track progress
- **Be flexible**: Adjust plans based on weather and conditions
- **Rest properly**: Get adequate sleep between birding days
- **Stay hydrated**: Drink plenty of water during long days
- **Share experiences**: Connect with other birders in the area

## 📊 Success Tracking
Use this section to track your progress:

### Species Checklist
"""
    
    for species in target_species:
        markdown += f"- [ ] {species}\n"
    
    markdown += """
### Daily Notes
*Use this space to record your observations, photos taken, and memorable moments.*

---
*Generated by BirdingPlanner - Your AI-powered birding companion* 🦅
"""
    
    return markdown


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