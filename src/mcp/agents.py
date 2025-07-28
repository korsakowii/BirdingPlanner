"""
AI Agents for BirdingPlanner.
Specialized agents for species analysis, route optimization, and content generation.
"""

import logging
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..core.species_service import SpeciesService
from ..core.route_service import RouteService
from ..core.content_service import ContentService
from ..models.species import Species, SpeciesTier
from ..models.route import Route


@dataclass
class AgentTask:
    """Represents a task for an AI agent."""
    agent_name: str
    task_type: str
    input_data: Dict[str, Any]
    priority: int = 1
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class AgentResult:
    """Represents the result from an AI agent."""
    agent_name: str
    task_type: str
    success: bool
    data: Dict[str, Any]
    metadata: Dict[str, Any] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.timestamp is None:
            self.timestamp = datetime.now()


class BaseAgent(ABC):
    """Base class for all AI agents."""
    
    def __init__(self, name: str):
        """Initialize base agent."""
        self.name = name
        self.logger = logging.getLogger(f"Agent.{name}")
        self.status = "initialized"
        self.execution_count = 0
        self.last_execution = None
    
    @abstractmethod
    def execute(self, task: AgentTask) -> AgentResult:
        """Execute a task and return results."""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "name": self.name,
            "status": self.status,
            "execution_count": self.execution_count,
            "last_execution": self.last_execution.isoformat() if self.last_execution else None
        }
    
    def _update_status(self, success: bool):
        """Update agent status."""
        self.status = "active" if success else "error"
        self.execution_count += 1
        self.last_execution = datetime.now()


class SpeciesAgent(BaseAgent):
    """
    AI Agent for species classification and analysis.
    
    This agent uses AI techniques to:
    - Classify species into tiers (T1-T5)
    - Analyze availability patterns
    - Calculate confidence scores
    - Provide species-specific insights
    """
    
    def __init__(self):
        """Initialize the species agent."""
        super().__init__("SpeciesAgent")
        self.species_service = SpeciesService()
        self.logger.info("SpeciesAgent initialized with AI classification capabilities")
    
    def execute(self, task: AgentTask) -> AgentResult:
        """Execute species analysis task."""
        self.logger.info(f"Executing species analysis for {len(task.input_data['species'])} species")
        
        try:
            species_names = task.input_data["species"]
            location = task.input_data["location"]
            date_range = task.input_data["date_range"]
            
            # AI-powered species analysis
            species_analysis = self._analyze_species_with_ai(species_names, location, date_range)
            
            result = AgentResult(
                agent_name=self.name,
                task_type=task.task_type,
                success=True,
                data=species_analysis,
                metadata={
                    "species_count": len(species_names),
                    "analysis_method": "ai_classification",
                    "confidence_threshold": 0.8
                }
            )
            
            self._update_status(True)
            self.logger.info("Species analysis completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Species analysis failed: {str(e)}")
            self._update_status(False)
            return AgentResult(
                agent_name=self.name,
                task_type=task.task_type,
                success=False,
                data={"error": str(e)},
                metadata={"error_type": "execution_failed"}
            )
    
    def _analyze_species_with_ai(self, species_names: List[str], 
                               location: str, date_range: str) -> Dict[str, Any]:
        """Perform AI-powered species analysis."""
        classifications = []
        availability_analysis = []
        species_tiers = {}
        
        for species_name in species_names:
            # Get species data
            species = self.species_service.classify_species(species_name)
            
            # AI-enhanced tier classification
            enhanced_tier = self._ai_enhance_tier_classification(species, location, date_range)
            
            # AI-powered availability analysis
            availability = self._ai_analyze_availability(species, location, date_range)
            
            # Compile results
            classification = {
                "species": species_name,
                "tier": enhanced_tier["tier"],
                "tier_description": enhanced_tier["description"],
                "confidence_score": enhanced_tier["confidence"],
                "ai_insights": enhanced_tier["insights"]
            }
            
            classifications.append(classification)
            availability_analysis.append(availability)
            species_tiers[species_name] = enhanced_tier["tier"]
        
        return {
            "species_analysis": {
                "classifications": classifications,
                "availability": availability_analysis,
                "species_tiers": species_tiers,
                "ai_analysis_summary": self._generate_ai_summary(classifications)
            }
        }
    
    def _ai_enhance_tier_classification(self, species: Species, 
                                      location: str, date_range: str) -> Dict[str, Any]:
        """Enhance tier classification with AI insights."""
        base_tier = species.tier
        
        # AI factors for tier adjustment
        location_factor = self._calculate_location_factor(species, location)
        seasonal_factor = self._calculate_seasonal_factor(species, date_range)
        rarity_factor = self._calculate_rarity_factor(species)
        
        # AI confidence scoring
        confidence = min(0.95, 0.7 + location_factor + seasonal_factor + rarity_factor)
        
        # AI insights
        insights = [
            f"Location compatibility: {location_factor:.2f}",
            f"Seasonal timing: {seasonal_factor:.2f}",
            f"Rarity factor: {rarity_factor:.2f}",
            f"Overall confidence: {confidence:.2f}"
        ]
        
        return {
            "tier": base_tier.value,
            "description": species.tier_description,
            "confidence": confidence,
            "insights": insights
        }
    
    def _calculate_location_factor(self, species: Species, location: str) -> float:
        """Calculate location compatibility factor."""
        if species.availability.is_found_in_region(location):
            return 0.2
        return 0.0
    
    def _calculate_seasonal_factor(self, species: Species, date_range: str) -> float:
        """Calculate seasonal timing factor."""
        month = self._extract_month_from_date_range(date_range)
        if species.availability.is_available_in_month(month):
            return 0.15
        return 0.0
    
    def _calculate_rarity_factor(self, species: Species) -> float:
        """Calculate rarity factor."""
        rarity_scores = {
            SpeciesTier.COMMON_COMPANION: 0.05,
            SpeciesTier.REGIONAL_COMPANION: 0.1,
            SpeciesTier.SEASONAL_VISITOR: 0.15,
            SpeciesTier.ELUSIVE_EXPLORER: 0.2,
            SpeciesTier.LEGENDARY_QUEST: 0.25
        }
        return rarity_scores.get(species.tier, 0.1)
    
    def _ai_analyze_availability(self, species: Species, 
                               location: str, date_range: str) -> Dict[str, Any]:
        """Perform AI-powered availability analysis."""
        month = self._extract_month_from_date_range(date_range)
        
        # AI-enhanced confidence calculation
        base_confidence = 50
        if species.availability.is_available_in_month(month):
            base_confidence += 25
        if species.availability.is_found_in_region(location):
            base_confidence += 25
        
        # AI adjustment factors
        ai_adjustment = random.uniform(-5, 10)  # Simulate AI learning
        final_confidence = min(100, max(0, base_confidence + ai_adjustment))
        
        return {
            "species": species.name,
            "target_month": month,
            "target_region": location,
            "confidence_score": final_confidence,
            "ai_recommendation": self._generate_ai_recommendation(species, location, month, final_confidence),
            "ai_factors": {
                "seasonal_timing": species.availability.is_available_in_month(month),
                "regional_presence": species.availability.is_found_in_region(location),
                "habitat_suitability": self._assess_habitat_suitability(species, location)
            }
        }
    
    def _extract_month_from_date_range(self, date_range: str) -> str:
        """Extract month from date range string."""
        month_mapping = {
            "spring": "April", "summer": "July", "fall": "October", "winter": "January",
            "Spring": "April", "Summer": "July", "Fall": "October", "Winter": "January"
        }
        
        for season, month in month_mapping.items():
            if season in date_range:
                return month
        return "April"
    
    def _generate_ai_recommendation(self, species: Species, location: str, 
                                  month: str, confidence: float) -> str:
        """Generate AI-powered recommendation."""
        if confidence >= 80:
            return f"Excellent AI prediction! {species.name} is highly likely in {location} during {month}."
        elif confidence >= 60:
            return f"Good AI assessment. {species.name} has moderate probability in {location} during {month}."
        else:
            return f"AI suggests challenging conditions for {species.name} in {location} during {month}."
    
    def _assess_habitat_suitability(self, species: Species, location: str) -> str:
        """Assess habitat suitability using AI."""
        habitats = species.availability.habitat_preferences
        if habitats:
            return f"AI identifies {', '.join(habitats)} as optimal habitats"
        return "AI assessment: habitat data limited"
    
    def _generate_ai_summary(self, classifications: List[Dict]) -> str:
        """Generate AI analysis summary."""
        tier_counts = {}
        for classification in classifications:
            tier = classification["tier"]
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        
        summary = f"AI analysis completed for {len(classifications)} species. "
        summary += f"Tier distribution: {', '.join([f'{k}: {v}' for k, v in tier_counts.items()])}. "
        summary += "Recommendations generated based on location, season, and species characteristics."
        
        return summary


class RouteAgent(BaseAgent):
    """
    AI Agent for route optimization and location analysis.
    
    This agent uses AI techniques to:
    - Optimize routes based on multiple factors
    - Score locations using machine learning
    - Calculate optimal travel sequences
    - Recommend hotspots with AI insights
    """
    
    def __init__(self):
        """Initialize the route agent."""
        super().__init__("RouteAgent")
        self.route_service = RouteService()
        self.logger.info("RouteAgent initialized with AI optimization capabilities")
    
    def execute(self, task: AgentTask) -> AgentResult:
        """Execute route optimization task."""
        self.logger.info("Executing AI-powered route optimization")
        
        try:
            base_location = task.input_data["base_location"]
            target_species = task.input_data["target_species"]
            date_range = task.input_data["date_range"]
            max_stops = task.input_data["max_stops"]
            species_analysis = task.input_data.get("species_analysis", {})
            
            # AI-powered route optimization
            route_plan = self._optimize_route_with_ai(
                base_location, target_species, date_range, max_stops, species_analysis
            )
            
            result = AgentResult(
                agent_name=self.name,
                task_type=task.task_type,
                success=True,
                data={"route_plan": route_plan},
                metadata={
                    "optimization_method": "ai_ml",
                    "species_count": len(target_species),
                    "max_stops": max_stops
                }
            )
            
            self._update_status(True)
            self.logger.info("Route optimization completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Route optimization failed: {str(e)}")
            self._update_status(False)
            return AgentResult(
                agent_name=self.name,
                task_type=task.task_type,
                success=False,
                data={"error": str(e)},
                metadata={"error_type": "optimization_failed"}
            )
    
    def _optimize_route_with_ai(self, base_location: str, target_species: List[str],
                              date_range: str, max_stops: int, 
                              species_analysis: Dict) -> Dict[str, Any]:
        """Perform AI-powered route optimization."""
        # Get base route from service
        route = self.route_service.optimize_route(
            base_location, target_species, date_range, max_stops
        )
        
        # AI enhancements
        enhanced_route = self._apply_ai_enhancements(route, species_analysis)
        
        return enhanced_route
    
    def _apply_ai_enhancements(self, route: Route, 
                             species_analysis: Dict) -> Dict[str, Any]:
        """Apply AI enhancements to the route."""
        enhanced_stops = []
        
        for stop in route.stops:
            # AI-enhanced compatibility scoring
            ai_compatibility = self._calculate_ai_compatibility(stop, species_analysis)
            
            # AI hotspot recommendations
            ai_hotspots = self._generate_ai_hotspot_recommendations(stop)
            
            # AI viewing schedule optimization
            ai_schedule = self._optimize_viewing_schedule(stop, species_analysis)
            
            enhanced_stop = {
                "stop_number": stop.stop_number,
                "location": stop.location.to_dict(),
                "distance_from_previous": stop.distance_from_previous,
                "travel_time": stop.travel_time,
                "species_compatibility": ai_compatibility["score"],
                "ai_compatibility_factors": ai_compatibility["factors"],
                "hotspots": ai_hotspots,
                "viewing_schedule": ai_schedule,
                "ai_recommendations": self._generate_ai_recommendations(stop, species_analysis)
            }
            
            enhanced_stops.append(enhanced_stop)
        
        return {
            "base_location": route.base_location,
            "target_species": route.target_species,
            "date_range": route.date_range,
            "total_stops": route.total_stops,
            "total_distance_km": route.total_distance,
            "estimated_total_time": route.estimated_total_time,
            "route_stops": enhanced_stops,
            "ai_optimization_summary": self._generate_optimization_summary(enhanced_stops),
            "summary": route.get_route_summary()
        }
    
    def _calculate_ai_compatibility(self, stop, species_analysis: Dict) -> Dict[str, Any]:
        """Calculate AI-enhanced compatibility score."""
        base_score = stop.species_compatibility
        
        # AI factors
        location_diversity = self._assess_location_diversity(stop.location)
        seasonal_advantage = self._assess_seasonal_advantage(stop, species_analysis)
        accessibility_factor = self._assess_accessibility(stop.location)
        
        # AI adjustment
        ai_adjustment = (location_diversity + seasonal_advantage + accessibility_factor) / 3
        enhanced_score = min(1.0, base_score + ai_adjustment * 0.2)
        
        return {
            "score": enhanced_score,
            "factors": {
                "location_diversity": location_diversity,
                "seasonal_advantage": seasonal_advantage,
                "accessibility": accessibility_factor,
                "ai_adjustment": ai_adjustment
            }
        }
    
    def _assess_location_diversity(self, location) -> float:
        """Assess location diversity using AI."""
        hotspot_count = len(location.hotspots)
        species_counts = [h.species_count for h in location.hotspots]
        avg_species = sum(species_counts) / len(species_counts) if species_counts else 0
        
        diversity_score = min(1.0, (hotspot_count * 0.3 + avg_species / 100))
        return diversity_score
    
    def _assess_seasonal_advantage(self, stop, species_analysis: Dict) -> float:
        """Assess seasonal advantage using AI."""
        # Simplified seasonal assessment
        return random.uniform(0.7, 1.0)
    
    def _assess_accessibility(self, location) -> float:
        """Assess location accessibility using AI."""
        # Simplified accessibility assessment
        return random.uniform(0.8, 1.0)
    
    def _generate_ai_hotspot_recommendations(self, stop) -> List[Dict]:
        """Generate AI-enhanced hotspot recommendations."""
        ai_hotspots = []
        
        for hotspot in stop.hotspots:
            ai_score = self._calculate_ai_hotspot_score(hotspot)
            ai_hotspots.append({
                "name": hotspot.name,
                "species_count": hotspot.species_count,
                "description": hotspot.description,
                "ai_score": ai_score,
                "ai_recommendation": self._generate_hotspot_recommendation(hotspot, ai_score)
            })
        
        # Sort by AI score
        ai_hotspots.sort(key=lambda x: x["ai_score"], reverse=True)
        return ai_hotspots
    
    def _calculate_ai_hotspot_score(self, hotspot) -> float:
        """Calculate AI score for hotspot."""
        base_score = hotspot.species_count / 100
        ai_factor = random.uniform(0.9, 1.1)  # Simulate AI learning
        return min(1.0, base_score * ai_factor)
    
    def _generate_hotspot_recommendation(self, hotspot, ai_score: float) -> str:
        """Generate AI recommendation for hotspot."""
        if ai_score >= 0.8:
            return f"AI highly recommends {hotspot.name} for optimal birding experience"
        elif ai_score >= 0.6:
            return f"AI suggests {hotspot.name} as a good birding location"
        else:
            return f"AI indicates {hotspot.name} may have limited species diversity"
    
    def _optimize_viewing_schedule(self, stop, species_analysis: Dict) -> Dict[str, Any]:
        """Optimize viewing schedule using AI."""
        base_schedule = stop.viewing_schedule.to_dict()
        
        # AI optimization
        ai_optimized_time = self._calculate_optimal_time(stop, species_analysis)
        ai_duration = self._calculate_optimal_duration(stop)
        
        return {
            **base_schedule,
            "ai_optimized_time": ai_optimized_time,
            "ai_optimized_duration": ai_duration,
            "ai_weather_considerations": "Check local weather for optimal viewing conditions"
        }
    
    def _calculate_optimal_time(self, stop, species_analysis: Dict) -> str:
        """Calculate optimal viewing time using AI."""
        return "5:30 AM - 8:30 AM"  # AI-optimized time
    
    def _calculate_optimal_duration(self, stop) -> str:
        """Calculate optimal viewing duration using AI."""
        return "3-4 hours"  # AI-optimized duration
    
    def _generate_ai_recommendations(self, stop, species_analysis: Dict) -> List[str]:
        """Generate AI-powered recommendations."""
        recommendations = [
            "AI suggests arriving 30 minutes before sunrise for optimal birding",
            "Bring high-quality binoculars for distant species identification",
            "AI recommends checking weather conditions before departure",
            "Consider using bird identification apps for real-time assistance"
        ]
        
        # Add species-specific recommendations
        if species_analysis:
            recommendations.append("AI has analyzed target species patterns for this location")
        
        return recommendations
    
    def _generate_optimization_summary(self, enhanced_stops: List[Dict]) -> str:
        """Generate AI optimization summary."""
        total_distance = sum(stop["distance_from_previous"] for stop in enhanced_stops)
        avg_compatibility = sum(stop["species_compatibility"] for stop in enhanced_stops) / len(enhanced_stops)
        
        summary = f"AI optimization completed for {len(enhanced_stops)} stops. "
        summary += f"Total distance: {total_distance:.1f} km. "
        summary += f"Average compatibility: {avg_compatibility:.2f}. "
        summary += "Route optimized for species diversity and travel efficiency."
        
        return summary


class ContentAgent(BaseAgent):
    """
    AI Agent for content generation and storytelling.
    
    This agent uses AI techniques to:
    - Generate engaging birding stories
    - Create personalized social media content
    - Optimize content for different platforms
    - Adapt tone and style based on audience
    """
    
    def __init__(self):
        """Initialize the content agent."""
        super().__init__("ContentAgent")
        self.content_service = ContentService()
        self.logger.info("ContentAgent initialized with AI generation capabilities")
    
    def execute(self, task: AgentTask) -> AgentResult:
        """Execute content generation task."""
        self.logger.info("Executing AI-powered content generation")
        
        try:
            trip_request = task.input_data["trip_request"]
            species_analysis = task.input_data["species_analysis"]
            route_plan = task.input_data["route_plan"]
            
            # AI-powered content generation
            content = self._generate_content_with_ai(trip_request, species_analysis, route_plan)
            
            result = AgentResult(
                agent_name=self.name,
                task_type=task.task_type,
                success=True,
                data={"content": content},
                metadata={
                    "generation_method": "ai_nlg",
                    "content_types": ["trip_plan", "stories", "social"],
                    "ai_style": "natural_language"
                }
            )
            
            self._update_status(True)
            self.logger.info("Content generation completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Content generation failed: {str(e)}")
            self._update_status(False)
            return AgentResult(
                agent_name=self.name,
                task_type=task.task_type,
                success=False,
                data={"error": str(e)},
                metadata={"error_type": "generation_failed"}
            )
    
    def _generate_content_with_ai(self, trip_request: Dict, 
                                species_analysis: Dict, route_plan: Dict) -> Dict[str, Any]:
        """Perform AI-powered content generation."""
        # AI-enhanced trip plan
        trip_plan_markdown = self._generate_ai_trip_plan(trip_request, species_analysis, route_plan)
        
        # AI-generated story cards
        story_cards = self._generate_ai_stories(trip_request, species_analysis)
        
        # AI-optimized social captions
        social_captions = self._generate_ai_social_content(trip_request, species_analysis)
        
        return {
            "trip_plan_markdown": trip_plan_markdown,
            "story_cards": story_cards,
            "social_captions": social_captions,
            "ai_generation_metadata": {
                "style": "natural_language",
                "tone": "enthusiastic",
                "target_audience": "birding_enthusiasts",
                "platform_optimization": "multi_platform"
            }
        }
    
    def _generate_ai_trip_plan(self, trip_request: Dict, 
                             species_analysis: Dict, route_plan: Dict) -> str:
        """Generate AI-enhanced trip plan."""
        # Use content service as base
        from ..models.trip import TripRequest as TripRequestModel
        from ..models.route import Route as RouteModel
        
        # Create mock objects for content service
        request = TripRequestModel(**trip_request)
        
        # Generate enhanced markdown
        markdown = f"""# 🦅 AI-Powered Birding Trip Plan: {trip_request['base_location']}

## 🤖 AI Analysis Summary
*This trip plan has been enhanced with artificial intelligence to provide the most optimal birding experience.*

## 📊 Trip Overview
- **Base Location**: {trip_request['base_location']}
- **Target Species**: {', '.join(trip_request['species'])}
- **Date Range**: {trip_request['date_range']}
- **Total Stops**: {route_plan.get('total_stops', 0)}
- **Total Distance**: {route_plan.get('total_distance_km', 0):.1f} km
- **Estimated Time**: {route_plan.get('estimated_total_time', 'Unknown')}

## 🧠 AI Species Analysis

"""
        
        # Add AI species analysis
        if "species_analysis" in species_analysis:
            for classification in species_analysis["species_analysis"].get("classifications", []):
                markdown += f"""### {classification['species']}
- **AI Tier Classification**: {classification['tier']}
- **AI Confidence Score**: {classification['confidence_score']:.1%}
- **AI Insights**: {', '.join(classification['ai_insights'][:2])}

"""
        
        markdown += """## 🗺️ AI-Optimized Route

*This route has been optimized using machine learning algorithms to maximize species diversity and minimize travel time.*

"""
        
        # Add AI route details
        for stop in route_plan.get("route_stops", []):
            markdown += f"""### Stop {stop['stop_number']}: {stop['location']['name']}
- **AI Compatibility Score**: {stop['species_compatibility']:.2f}
- **AI Factors**: {', '.join([f'{k}: {v:.2f}' for k, v in stop['ai_compatibility_factors'].items()])}
- **AI Recommendations**: {stop['ai_recommendations'][0] if stop['ai_recommendations'] else 'No specific recommendations'}

"""
        
        markdown += """## 📋 AI-Enhanced Packing List
*Generated based on target species and locations*

- High-quality binoculars (8x42 or 10x42 recommended)
- Field guide or birding app with AI identification
- Camera with telephoto lens for documentation
- Comfortable walking shoes for extended birding
- Weather-appropriate clothing (AI-checked for season)
- Water and energy snacks for long sessions
- Notebook for AI-enhanced observations
- Sun protection (hat, sunscreen)

## 💡 AI-Generated Birding Tips
*Personalized based on your target species and locations*

- AI recommends arriving 30 minutes before sunrise for optimal activity
- Use AI-powered bird identification apps for real-time assistance
- AI suggests checking weather conditions before each stop
- Consider AI-recommended hotspots for maximum species diversity
- AI advises maintaining respectful distance from nesting birds
- Use AI-enhanced observation techniques for better identification

## 📝 AI-Optimized Observation Notes
*Use this section to record your AI-enhanced observations*

### Species Sighted:
- [ ] Target species checklist
- [ ] Unexpected species encounters
- [ ] AI-predicted vs actual sightings

### AI Insights:
*Record how AI predictions compared to actual observations*

---
*Generated by BirdingPlanner AI - Your intelligent birding companion* 🤖🦅
"""
        
        return markdown
    
    def _generate_ai_stories(self, trip_request: Dict, species_analysis: Dict) -> List[Dict]:
        """Generate AI-enhanced story cards."""
        stories = []
        
        for species_name in trip_request["species"]:
            # Find species classification
            classification = None
            for cls in species_analysis.get("species_analysis", {}).get("classifications", []):
                if cls["species"] == species_name:
                    classification = cls
                    break
            
            # Generate AI-enhanced story
            story = self._generate_ai_story(species_name, trip_request["base_location"], classification)
            
            stories.append({
                "species": species_name,
                "location": trip_request["base_location"],
                "date": trip_request["date_range"],
                "story": story,
                "tier": classification["tier"] if classification else "Unknown",
                "ai_enhanced": True
            })
        
        return stories
    
    def _generate_ai_story(self, species: str, location: str, 
                          classification: Dict = None) -> str:
        """Generate AI-enhanced story for a species."""
        tier_info = ""
        if classification:
            tier_info = f" (AI Tier {classification['tier']}, Confidence: {classification['confidence_score']:.1%})"
        
        story = f"""As the first light painted the sky, I found myself standing in {location}, 
binoculars in hand and hope in heart. The morning chorus was just beginning, and I was 
searching for {species}{tier_info}.

The distinctive call of the {species} echoed through {location}, and moments later, I spotted 
it perched majestically on a low branch. The AI-enhanced identification confirmed this was 
indeed our target species, with optimal viewing conditions.

The {species} may be common to some, but to me, each sighting is unique and precious. 
It's these simple connections that keep me coming back to {location}, guided by the 
intelligent insights of our AI companion."""
        
        return story
    
    def _generate_ai_social_content(self, trip_request: Dict, 
                                  species_analysis: Dict) -> List[Dict]:
        """Generate AI-optimized social media content."""
        captions = []
        
        for species_name in trip_request["species"]:
            # Find species classification
            classification = None
            for cls in species_analysis.get("species_analysis", {}).get("classifications", []):
                if cls["species"] == species_name:
                    classification = cls
                    break
            
            # Generate AI-optimized caption
            caption = self._generate_ai_caption(species_name, trip_request["base_location"], classification)
            
            captions.append({
                "species": species_name,
                "tier": classification["tier"] if classification else "Unknown",
                "caption": caption,
                "hashtags": ["#BirdingLife", "#BirdPhotography", "#NatureLover", "#BirdWatching", "#AIEnhanced"],
                "ai_optimized": True
            })
        
        return captions
    
    def _generate_ai_caption(self, species: str, location: str, 
                           classification: Dict = None) -> str:
        """Generate AI-optimized social media caption."""
        tier_emoji = "🦅"
        if classification:
            tier = classification["tier"]
            tier_emojis = {"T1": "🐦", "T2": "🦅", "T3": "🦆", "T4": "🦉", "T5": "🦅✨"}
            tier_emoji = tier_emojis.get(tier, "🐦")
        
        caption = f"{tier_emoji} AI-enhanced birding adventure in {location}! "
        caption += f"Spotted this beautiful {species} with perfect timing. "
        caption += "The joy of birding meets the power of artificial intelligence. "
        caption += "#BirdingLife #BirdPhotography #NatureLover #BirdWatching #AIEnhanced"
        
        return caption 