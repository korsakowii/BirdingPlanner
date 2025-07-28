#!/usr/bin/env python3
"""
eBird Integration Demo Script
Demonstrates the eBird API integration and EBirdAgent capabilities
"""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config.settings import get_settings
from src.core.ebird_service import EBirdService
from src.mcp.ebird_agent import EBirdAgent, AgentTask


def demo_ebird_api_features():
    """Demonstrate eBird API features"""
    print("🦅 eBird API Integration Demo")
    print("=" * 60)
    print(f"Demo started at: {datetime.now()}")
    print()
    
    settings = get_settings()
    
    if not settings.ebird_api_key:
        print("❌ No eBird API key found. Please set EBIRD_API_KEY environment variable.")
        return
    
    try:
        # Initialize services
        ebird_service = EBirdService(settings.ebird_api_key)
        ebird_agent = EBirdAgent(ebird_service)
        
        print("✅ Services initialized successfully!")
        print()
        
        # Demo 1: Real-time observations
        print("📊 Demo 1: Real-time Observations")
        print("-" * 40)
        
        observations = ebird_service.get_recent_observations("New York", days=1)
        print(f"Found {len(observations)} recent observations in New York")
        
        if observations:
            print("\nRecent sightings:")
            for i, obs in enumerate(observations[:5]):
                print(f"  {i+1}. {obs.species} at {obs.location}")
                print(f"     Time: {obs.timestamp.strftime('%Y-%m-%d %H:%M')}")
                print(f"     Observer: {obs.observer or 'Anonymous'}")
                if obs.coordinates:
                    print(f"     Location: ({obs.coordinates.latitude:.3f}, {obs.coordinates.longitude:.3f})")
                print()
        
        # Demo 2: Success rate prediction
        print("🎯 Demo 2: Success Rate Prediction")
        print("-" * 40)
        
        target_species = ["American Robin", "Northern Cardinal", "Blue Jay"]
        
        for species in target_species:
            success_rate = ebird_service.predict_success_rate(
                species, "New York", "2024-04-15"
            )
            print(f"  {species}: {success_rate:.1%} success rate")
        
        print()
        
        # Demo 3: AI-enhanced species analysis
        print("🤖 Demo 3: AI-Enhanced Species Analysis")
        print("-" * 40)
        
        species_task = AgentTask(
            agent_name=ebird_agent.name,
            task_type="species_analysis",
            input_data={
                "species": "American Robin",
                "location": "New York",
                "date_range": "Spring 2024"
            }
        )
        
        result = ebird_agent.execute(species_task)
        
        if result.success:
            data = result.data
            analysis = data.get('analysis')
            
            print(f"Species: {analysis.species}")
            print(f"Location: {analysis.location}")
            print(f"Success Rate: {analysis.success_rate:.1%}")
            print(f"Recent Observations: {analysis.recent_observations}")
            print(f"Best Time: {analysis.best_time}")
            print(f"Seasonal Trend: {analysis.seasonal_trend}")
            print(f"Confidence Score: {analysis.confidence_score:.1%}")
            
            print("\nAI Insights:")
            for insight in analysis.ai_insights:
                print(f"  • {insight}")
            
            print(f"\nHotspot Recommendations:")
            for hotspot in analysis.hotspot_recommendations[:3]:
                print(f"  • {hotspot}")
        
        print()
        
        # Demo 4: Success prediction for multiple species
        print("🎯 Demo 4: Multi-Species Success Prediction")
        print("-" * 40)
        
        prediction_task = AgentTask(
            agent_name=ebird_agent.name,
            task_type="success_prediction",
            input_data={
                "species": ["American Robin", "Northern Cardinal", "Blue Jay", "Red-tailed Hawk"],
                "location": "New York",
                "date_range": "Spring 2024"
            }
        )
        
        pred_result = ebird_agent.execute(prediction_task)
        
        if pred_result.success:
            data = pred_result.data
            print(f"Overall Success Rate: {data.get('overall_success_rate', 0):.1%}")
            print(f"Confidence: {data.get('confidence', 0):.1%}")
            
            print("\nIndividual Predictions:")
            predictions = data.get('predictions', {})
            for species, rate in predictions.items():
                print(f"  {species}: {rate:.1%}")
            
            print("\nAI Recommendations:")
            recommendations = data.get('recommendations', [])
            for rec in recommendations:
                print(f"  • {rec}")
        
        print()
        
        # Demo 5: Rare species alerts
        print("🚨 Demo 5: Rare Species Alerts")
        print("-" * 40)
        
        alert_task = AgentTask(
            agent_name=ebird_agent.name,
            task_type="rare_species_alert",
            input_data={
                "location": "New York",
                "days": 7
            }
        )
        
        alert_result = ebird_agent.execute(alert_task)
        
        if alert_result.success:
            data = alert_result.data
            alerts = data.get('alerts', [])
            
            if alerts:
                print(f"Found {len(alerts)} rare species alerts:")
                for alert in alerts:
                    print(f"  • {alert['species']} at {alert['location']}")
                    print(f"    Rarity Score: {alert['rarity_score']:.1%}")
                    print(f"    Time: {alert['timestamp']}")
                    print(f"    Recommendation: {alert['recommendation']}")
                    print()
            else:
                print("No rare species alerts found in the last 7 days.")
        
        print()
        
        # Demo 6: Hotspot analysis
        print("📍 Demo 6: Hotspot Activity Analysis")
        print("-" * 40)
        
        # Use a sample hotspot ID (in real usage, this would come from eBird data)
        sample_hotspots = ["L123456", "L789012"]  # Example hotspot IDs
        
        for hotspot_id in sample_hotspots:
            activity = ebird_service.get_hotspot_activity(hotspot_id)
            if activity:
                print(f"Hotspot: {activity.hotspot_name}")
                print(f"Recent Observations: {activity.recent_observations}")
                print(f"Species Count: {activity.species_count}")
                print(f"Success Rate: {activity.success_rate:.1%}")
                print(f"Last Updated: {activity.last_updated}")
                print()
            else:
                print(f"No data available for hotspot {hotspot_id}")
        
        print("🎉 Demo completed successfully!")
        print("\nKey Features Demonstrated:")
        print("  ✅ Real-time observation data")
        print("  ✅ Success rate prediction")
        print("  ✅ AI-enhanced species analysis")
        print("  ✅ Multi-species success prediction")
        print("  ✅ Rare species alerts")
        print("  ✅ Hotspot activity analysis")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    demo_ebird_api_features() 