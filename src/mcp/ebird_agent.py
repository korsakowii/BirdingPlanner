"""
eBird Agent for BirdingPlanner
Provides AI-enhanced eBird data analysis and recommendations
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from src.mcp.agents import BaseAgent, AgentTask, AgentResult
from src.core.ebird_service import EBirdService, EBirdObservation, HotspotActivity

logger = logging.getLogger(__name__)


@dataclass
class EBirdAnalysis:
    """eBird data analysis result"""
    species: str
    location: str
    success_rate: float
    recent_observations: int
    best_time: str
    hotspot_recommendations: List[str]
    seasonal_trend: str
    confidence_score: float
    ai_insights: List[str]


class EBirdAgent(BaseAgent):
    """AI-enhanced eBird data analysis agent"""
    
    def __init__(self, ebird_service: EBirdService):
        super().__init__("EBirdAgent")
        self.ebird_service = ebird_service
        self.capabilities = [
            "real_time_data_analysis",
            "success_rate_prediction", 
            "hotspot_recommendation",
            "seasonal_analysis",
            "rare_species_detection"
        ]
    
    def execute(self, task: AgentTask) -> AgentResult:
        """Execute the given task."""
        try:
            if task.task_type == "species_analysis":
                return self._analyze_species(task.input_data)
            elif task.task_type == "hotspot_analysis":
                return self._analyze_hotspot(task.input_data)
            elif task.task_type == "success_prediction":
                return self._predict_success(task.input_data)
            elif task.task_type == "rare_species_alert":
                return self._detect_rare_species(task.input_data)
            elif task.task_type == "trip_report_analysis":
                return self._analyze_trip_reports(task.input_data)
            elif task.task_type == "trip_planning_insights":
                return self._get_trip_planning_insights(task.input_data)
            else:
                return AgentResult(
                    agent_name=self.name,
                    task_type=task.task_type,
                    success=False,
                    data={"error": f"Unknown task type: {task.task_type}"}
                )
        except Exception as e:
            logger.error(f"EBirdAgent execution failed: {e}")
            return AgentResult(
                agent_name=self.name,
                task_type=task.task_type,
                success=False,
                data={"error": str(e)}
            )
    
    def _analyze_species(self, input_data: Dict[str, Any]) -> AgentResult:
        """Analyze species data and provide AI insights"""
        species = input_data.get("species")
        location = input_data.get("location")
        date_range = input_data.get("date_range", "Spring 2024")
        
        if not species or not location:
            return AgentResult(
                agent_name=self.agent_name,
                task_type="species_analysis",
                success=False,
                data={"error": "Missing species or location"}
            )
        
        # Get recent observations
        observations = self.ebird_service.get_recent_observations(
            location, species, days=30
        )
        
        # Calculate success rate
        success_rate = self.ebird_service.predict_success_rate(
            species, location, "2024-04-15"  # Example date
        )
        
        # Analyze patterns
        best_time = self._analyze_best_time(observations)
        seasonal_trend = self._analyze_seasonal_trend(observations, date_range)
        ai_insights = self._generate_ai_insights(observations, success_rate)
        
        analysis = EBirdAnalysis(
            species=species,
            location=location,
            success_rate=success_rate,
            recent_observations=len(observations),
            best_time=best_time,
            hotspot_recommendations=self._get_hotspot_recommendations(observations),
            seasonal_trend=seasonal_trend,
            confidence_score=self._calculate_confidence(observations),
            ai_insights=ai_insights
        )
        
        return AgentResult(
            agent_name=self.name,
            task_type="species_analysis",
            success=True,
            data={
                "analysis": analysis,
                "observations_count": len(observations),
                "success_rate": success_rate,
                "ai_insights": ai_insights
            }
        )
    
    def _analyze_hotspot(self, input_data: Dict[str, Any]) -> AgentResult:
        """Analyze hotspot activity and provide recommendations"""
        hotspot_id = input_data.get("hotspot_id")
        location = input_data.get("location")
        
        if not hotspot_id and not location:
                    return AgentResult(
            agent_name=self.name,
            task_type="hotspot_analysis",
            success=False,
            data={"error": "Missing hotspot_id or location"}
        )
        
        # Get hotspot activity
        if hotspot_id:
            activity = self.ebird_service.get_hotspot_activity(hotspot_id)
        else:
            # For location-based analysis, get recent observations
            observations = self.ebird_service.get_recent_observations(location, days=7)
            activity = self._create_location_activity(location, observations)
        
        if not activity:
                    return AgentResult(
            agent_name=self.name,
            task_type="hotspot_analysis",
            success=False,
            data={"error": "No hotspot data available"}
        )
        
        # Generate AI insights
        insights = self._generate_hotspot_insights(activity)
        
        return AgentResult(
            agent_name=self.name,
            task_type="hotspot_analysis",
            success=True,
            data={
                "hotspot_activity": activity,
                "ai_insights": insights,
                "recommendation_score": activity.success_rate
            }
        )
    
    def _predict_success(self, input_data: Dict[str, Any]) -> AgentResult:
        """Predict success rate for birding trip"""
        species_list = input_data.get("species", [])
        location = input_data.get("location")
        date_range = input_data.get("date_range")
        
        if not species_list or not location:
                    return AgentResult(
            agent_name=self.name,
            task_type="success_prediction",
            success=False,
            data={"error": "Missing species list or location"}
        )
        
        predictions = {}
        overall_success_rate = 0.0
        
        for species in species_list:
            success_rate = self.ebird_service.predict_success_rate(
                species, location, "2024-04-15"  # Example date
            )
            predictions[species] = success_rate
            overall_success_rate += success_rate
        
        overall_success_rate /= len(species_list)
        
        # Generate AI recommendations
        recommendations = self._generate_success_recommendations(
            predictions, overall_success_rate
        )
        
        return AgentResult(
            agent_name=self.name,
            task_type="success_prediction",
            success=True,
            data={
                "predictions": predictions,
                "overall_success_rate": overall_success_rate,
                "recommendations": recommendations,
                "confidence": self._calculate_prediction_confidence(predictions)
            }
        )
    
    def _detect_rare_species(self, input_data: Dict) -> AgentResult:
        """Detect rare species alerts."""
        location = input_data.get("location", "New York")
        days = input_data.get("days", 7)
        
        alerts = self.ebird_service.get_rare_species_alerts(location, days)
        
        return AgentResult(
            agent_name=self.name,
            task_type="rare_species_alert",
            success=True,
            data={
                "alerts": alerts,
                "alert_count": len(alerts),
                "location": location,
                "timeframe": f"{days} days"
            }
        )
    
    def _analyze_trip_reports(self, input_data: Dict) -> AgentResult:
        """Analyze trip reports for insights."""
        location = input_data.get("location", "New York")
        days = input_data.get("days", 30)
        
        trip_reports = self.ebird_service.get_trip_reports(location, days)
        
        # Analyze trip reports
        analysis = {
            "total_reports": len(trip_reports),
            "average_species_per_trip": 0,
            "most_productive_hotspots": [],
            "best_timing": "Unknown",
            "common_species": [],
            "rare_species": [],
            "trip_duration_patterns": {},
            "recommendations": []
        }
        
        if trip_reports:
            # Calculate averages
            total_species = sum(report["species_count"] for report in trip_reports)
            analysis["average_species_per_trip"] = total_species / len(trip_reports)
            
            # Find most productive hotspots
            hotspot_counts = {}
            for report in trip_reports:
                for hotspot in report["hotspots_visited"]:
                    hotspot_counts[hotspot] = hotspot_counts.get(hotspot, 0) + 1
            
            analysis["most_productive_hotspots"] = sorted(
                hotspot_counts.items(), key=lambda x: x[1], reverse=True
            )[:5]
            
            # Find common and rare species
            species_counts = {}
            for report in trip_reports:
                for species in report["species_list"]:
                    species_counts[species] = species_counts.get(species, 0) + 1
            
            total_reports = len(trip_reports)
            common_species = [s for s, c in species_counts.items() if c >= total_reports * 0.3]
            rare_species = [s for s, c in species_counts.items() if c <= 2]
            
            analysis["common_species"] = common_species[:10]
            analysis["rare_species"] = rare_species[:10]
            
            # Generate recommendations
            if analysis["average_species_per_trip"] < 10:
                analysis["recommendations"].append("Consider visiting during peak migration periods")
            
            if len(analysis["most_productive_hotspots"]) > 0:
                top_hotspot = analysis["most_productive_hotspots"][0][0]
                analysis["recommendations"].append(f"Focus on {top_hotspot} for best results")
        
        return AgentResult(
            agent_name=self.name,
            task_type="trip_report_analysis",
            success=True,
            data={
                "analysis": analysis,
                "trip_reports": trip_reports[:5],  # Return first 5 reports
                "location": location,
                "timeframe": f"{days} days"
            }
        )
    
    def _get_trip_planning_insights(self, input_data: Dict) -> AgentResult:
        """Get insights for trip planning based on trip reports."""
        location = input_data.get("location", "New York")
        target_species = input_data.get("target_species", [])
        date_range = input_data.get("date_range", "Spring 2024")
        
        insights = self.ebird_service.get_trip_insights(location, target_species, date_range)
        
        # Enhance insights with AI analysis
        enhanced_insights = {
            "basic_insights": insights,
            "ai_recommendations": self._generate_ai_recommendations(insights, target_species),
            "optimal_timing": self._analyze_optimal_timing(insights),
            "hotspot_prioritization": self._prioritize_hotspots(insights),
            "species_success_prediction": self._predict_species_success(insights, target_species)
        }
        
        return AgentResult(
            agent_name=self.name,
            task_type="trip_planning_insights",
            success=True,
            data={
                "insights": enhanced_insights,
                "location": location,
                "target_species": target_species,
                "date_range": date_range
            }
        )
    
    def _generate_ai_recommendations(self, insights: Dict, target_species: List[str]) -> List[str]:
        """Generate AI-powered recommendations based on insights."""
        recommendations = []
        
        # Analyze trip frequency
        if insights["total_trips"] < 5:
            recommendations.append("Limited trip data available - consider expanding search area")
        
        # Analyze species success rates
        low_success_species = [
            species for species, rate in insights["target_species_success"].items() 
            if rate < 0.3
        ]
        if low_success_species:
            recommendations.append(f"Low success rate for: {', '.join(low_success_species)} - consider alternative locations")
        
        # Analyze timing
        if insights["best_timing"] != "Unknown":
            recommendations.append(f"Optimal timing: {insights['best_timing']}")
        
        # Analyze hotspots
        if insights["top_hotspots"]:
            top_hotspot = insights["top_hotspots"][0][0]
            recommendations.append(f"Most productive hotspot: {top_hotspot}")
        
        return recommendations
    
    def _analyze_optimal_timing(self, insights: Dict) -> Dict:
        """Analyze optimal timing for birding trips."""
        return {
            "best_time_of_day": insights.get("best_timing", "Early morning (6-10 AM)"),
            "recommended_duration": "2-4 hours",
            "seasonal_factors": "Consider migration periods",
            "weather_considerations": "Check weather forecasts before planning"
        }
    
    def _prioritize_hotspots(self, insights: Dict) -> List[Dict]:
        """Prioritize hotspots based on insights."""
        prioritized = []
        for hotspot, count in insights.get("top_hotspots", []):
            priority = "High" if count >= 5 else "Medium" if count >= 3 else "Low"
            prioritized.append({
                "hotspot": hotspot,
                "visit_count": count,
                "priority": priority,
                "recommended_duration": "2-3 hours" if priority == "High" else "1-2 hours"
            })
        return prioritized
    
    def _predict_species_success(self, insights: Dict, target_species: List[str]) -> Dict:
        """Predict success rates for target species."""
        predictions = {}
        for species in target_species:
            success_rate = insights["target_species_success"].get(species, 0.0)
            confidence = "High" if success_rate > 0.7 else "Medium" if success_rate > 0.4 else "Low"
            predictions[species] = {
                "predicted_success_rate": success_rate,
                "confidence": confidence,
                "recommendation": self._get_species_recommendation(success_rate)
            }
        return predictions
    
    def _get_species_recommendation(self, success_rate: float) -> str:
        """Get recommendation based on success rate."""
        if success_rate > 0.7:
            return "High chance of success - plan with confidence"
        elif success_rate > 0.4:
            return "Moderate chance - consider multiple locations"
        else:
            return "Low chance - consider alternative species or locations"
    
    def _analyze_best_time(self, observations: List[EBirdObservation]) -> str:
        """Analyze best time for birding based on observations"""
        if not observations:
            return "No recent observations available"
        
        # Group observations by hour
        hour_counts = {}
        for obs in observations:
            hour = obs.timestamp.hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        if not hour_counts:
            return "Dawn and dusk (6-8 AM, 5-7 PM)"
        
        # Find peak hours
        peak_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
        
        if peak_hours[0][0] < 12:
            return f"Early morning ({peak_hours[0][0]}:00 AM)"
        else:
            return f"Afternoon ({peak_hours[0][0]}:00 PM)"
    
    def _analyze_seasonal_trend(self, observations: List[EBirdObservation], 
                               date_range: str) -> str:
        """Analyze seasonal trends"""
        if not observations:
            return "No seasonal data available"
        
        # Simple seasonal analysis
        spring_count = sum(1 for obs in observations 
                          if 3 <= obs.timestamp.month <= 5)
        summer_count = sum(1 for obs in observations 
                          if 6 <= obs.timestamp.month <= 8)
        fall_count = sum(1 for obs in observations 
                        if 9 <= obs.timestamp.month <= 11)
        winter_count = sum(1 for obs in observations 
                          if obs.timestamp.month in [12, 1, 2])
        
        season_counts = [
            ("Spring", spring_count),
            ("Summer", summer_count),
            ("Fall", fall_count),
            ("Winter", winter_count)
        ]
        
        best_season = max(season_counts, key=lambda x: x[1])
        return f"Best in {best_season[0]} ({best_season[1]} observations)"
    
    def _generate_ai_insights(self, observations: List[EBirdObservation], 
                             success_rate: float) -> List[str]:
        """Generate AI insights based on data"""
        insights = []
        
        if success_rate > 0.8:
            insights.append("Excellent viewing conditions - high success rate expected")
        elif success_rate > 0.5:
            insights.append("Good viewing conditions - moderate success rate")
        else:
            insights.append("Challenging conditions - consider alternative locations")
        
        if len(observations) > 20:
            insights.append("Frequently observed species - reliable sightings")
        elif len(observations) > 5:
            insights.append("Occasionally observed - patience may be required")
        else:
            insights.append("Rare sightings - consider expert guidance")
        
        # Add time-based insights
        if observations:
            recent_obs = [obs for obs in observations 
                         if obs.timestamp > datetime.now() - timedelta(days=7)]
            if recent_obs:
                insights.append(f"Recent activity detected - {len(recent_obs)} sightings this week")
        
        return insights
    
    def _get_hotspot_recommendations(self, observations: List[EBirdObservation]) -> List[str]:
        """Get hotspot recommendations based on observations"""
        if not observations:
            return ["No hotspot data available"]
        
        # Extract unique locations
        locations = list(set(obs.location for obs in observations))
        return locations[:5]  # Return top 5 locations
    
    def _calculate_confidence(self, observations: List[EBirdObservation]) -> float:
        """Calculate confidence score for analysis"""
        if not observations:
            return 0.0
        
        # Base confidence on number of observations
        base_confidence = min(1.0, len(observations) / 50.0)
        
        # Adjust for recency
        recent_obs = [obs for obs in observations 
                     if obs.timestamp > datetime.now() - timedelta(days=7)]
        recency_factor = min(1.0, len(recent_obs) / 10.0)
        
        return (base_confidence + recency_factor) / 2.0
    
    def _create_location_activity(self, location: str, 
                                 observations: List[EBirdObservation]) -> HotspotActivity:
        """Create hotspot activity for a location"""
        species_count = len(set(obs.species for obs in observations))
        
        return HotspotActivity(
            hotspot_id=location,
            hotspot_name=location,
            recent_observations=len(observations),
            species_count=species_count,
            last_updated=datetime.now(),
            coordinates=None,
            success_rate=len(observations) / 7.0  # Simple calculation
        )
    
    def _generate_hotspot_insights(self, activity: HotspotActivity) -> List[str]:
        """Generate insights for hotspot activity"""
        insights = []
        
        if activity.success_rate > 0.7:
            insights.append("Highly active hotspot - excellent birding location")
        elif activity.success_rate > 0.4:
            insights.append("Moderately active - good birding opportunities")
        else:
            insights.append("Low activity - consider timing or alternative locations")
        
        if activity.species_count > 20:
            insights.append(f"High species diversity - {activity.species_count} species observed")
        elif activity.species_count > 10:
            insights.append(f"Moderate diversity - {activity.species_count} species observed")
        else:
            insights.append("Limited species diversity")
        
        return insights
    
    def _generate_success_recommendations(self, predictions: Dict[str, float], 
                                        overall_rate: float) -> List[str]:
        """Generate recommendations based on success predictions"""
        recommendations = []
        
        if overall_rate > 0.8:
            recommendations.append("Excellent trip conditions - high success expected")
        elif overall_rate > 0.6:
            recommendations.append("Good conditions - moderate success likely")
        else:
            recommendations.append("Challenging conditions - consider rescheduling")
        
        # Species-specific recommendations
        low_success_species = [species for species, rate in predictions.items() if rate < 0.3]
        if low_success_species:
            recommendations.append(f"Consider alternatives for: {', '.join(low_success_species)}")
        
        return recommendations
    
    def _calculate_prediction_confidence(self, predictions: Dict[str, float]) -> float:
        """Calculate confidence in predictions"""
        if not predictions:
            return 0.0
        
        # Higher confidence with more species and consistent rates
        rates = list(predictions.values())
        variance = sum((rate - sum(rates)/len(rates))**2 for rate in rates) / len(rates)
        
        # Lower variance = higher confidence
        confidence = max(0.0, 1.0 - variance)
        return confidence
    
    def _filter_rare_species(self, observations: List[EBirdObservation]) -> List[EBirdObservation]:
        """Filter for potentially rare species"""
        # Simplified rarity detection
        rare_species = [
            "Cerulean Warbler", "Kirtland's Warbler", "Ivory-billed Woodpecker",
            "California Condor", "Whooping Crane"
        ]
        
        return [obs for obs in observations if obs.species in rare_species]
    
    def _calculate_rarity_score(self, species: str) -> float:
        """Calculate rarity score for a species"""
        # Simplified rarity scoring
        rarity_scores = {
            "Cerulean Warbler": 0.8,
            "Kirtland's Warbler": 0.9,
            "Ivory-billed Woodpecker": 1.0,
            "California Condor": 0.9,
            "Whooping Crane": 0.8
        }
        
        return rarity_scores.get(species, 0.3)  # Default rarity score 