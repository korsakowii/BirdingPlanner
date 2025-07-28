"""
Trip planning data models for BirdingPlanner.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from .species import Species
from .route import Route


@dataclass
class TripRequest:
    """Request for a birding trip plan."""
    species: List[str]
    base_location: str
    date_range: str
    max_stops: int = 3
    preferences: Dict[str, any] = field(default_factory=dict)
    
    def validate(self) -> List[str]:
        """Validate the trip request and return any errors."""
        errors = []
        
        if not self.species:
            errors.append("At least one target species must be specified")
        
        if not self.base_location:
            errors.append("Base location must be specified")
        
        if not self.date_range:
            errors.append("Date range must be specified")
        
        if self.max_stops < 1:
            errors.append("Maximum stops must be at least 1")
        
        return errors
    
    def to_dict(self) -> Dict:
        """Convert trip request to dictionary representation."""
        return {
            "species": self.species,
            "base_location": self.base_location,
            "date_range": self.date_range,
            "max_stops": self.max_stops,
            "preferences": self.preferences
        }


@dataclass
class TripSummary:
    """Summary of a birding trip."""
    base_location: str
    target_species: List[str]
    date_range: str
    total_stops: int
    total_distance_km: float
    estimated_time: str
    species_tiers: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert trip summary to dictionary representation."""
        return {
            "base_location": self.base_location,
            "target_species": self.target_species,
            "date_range": self.date_range,
            "total_stops": self.total_stops,
            "total_distance_km": self.total_distance_km,
            "estimated_time": self.estimated_time,
            "species_tiers": self.species_tiers
        }


@dataclass
class StoryCard:
    """Story card for a species encounter."""
    species: str
    location: str
    date: str
    story: str
    tier: str = ""
    
    def to_dict(self) -> Dict:
        """Convert story card to dictionary representation."""
        return {
            "species": self.species,
            "location": self.location,
            "date": self.date,
            "story": self.story,
            "tier": self.tier
        }


@dataclass
class SocialCaption:
    """Social media caption for a species sighting."""
    species: str
    tier: str
    caption: str
    hashtags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert social caption to dictionary representation."""
        return {
            "species": self.species,
            "tier": self.tier,
            "caption": self.caption,
            "hashtags": self.hashtags
        }


@dataclass
class TripContent:
    """Content generated for a birding trip."""
    trip_plan_markdown: str
    story_cards: List[StoryCard] = field(default_factory=list)
    social_captions: List[SocialCaption] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert trip content to dictionary representation."""
        return {
            "trip_plan_markdown": self.trip_plan_markdown,
            "story_cards": [card.to_dict() for card in self.story_cards],
            "social_captions": [caption.to_dict() for caption in self.social_captions]
        }


@dataclass
class TripPlan:
    """Complete birding trip plan."""
    trip_overview: TripSummary
    species_analysis: Dict[str, any]
    route_plan: Any  # Can be Route object or dict
    content: TripContent
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """Convert trip plan to dictionary representation."""
        route_plan_dict = self.route_plan.to_dict() if hasattr(self.route_plan, 'to_dict') else self.route_plan
        return {
            "trip_overview": self.trip_overview.to_dict(),
            "species_analysis": self.species_analysis,
            "route_plan": route_plan_dict,
            "content": self.content.to_dict(),
            "generated_at": self.generated_at.isoformat()
        }
    
    def save_to_files(self, output_dir: str = "output"):
        """Save trip plan to files."""
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save main trip plan
        trip_plan_path = os.path.join(output_dir, "trip_plan.md")
        with open(trip_plan_path, 'w', encoding='utf-8') as f:
            f.write(self.content.trip_plan_markdown)
        
        # Save story cards
        story_cards_dir = os.path.join(output_dir, "story_cards")
        os.makedirs(story_cards_dir, exist_ok=True)
        
        for i, story_card in enumerate(self.content.story_cards):
            story_path = os.path.join(story_cards_dir, f"story_{i+1:02d}_{story_card.species.replace(' ', '_')}.txt")
            with open(story_path, 'w', encoding='utf-8') as f:
                f.write(f"Species: {story_card.species}\n")
                f.write(f"Location: {story_card.location}\n")
                f.write(f"Date: {story_card.date}\n")
                f.write(f"Tier: {story_card.tier}\n")
                f.write("\n" + "="*50 + "\n\n")
                f.write(story_card.story)
        
        # Save social captions
        captions_path = os.path.join(output_dir, "social_captions.txt")
        with open(captions_path, 'w', encoding='utf-8') as f:
            f.write("Social Media Captions\n")
            f.write("=" * 30 + "\n\n")
            for caption_data in self.content.social_captions:
                f.write(f"Species: {caption_data.species} (Tier {caption_data.tier})\n")
                f.write(f"Caption: {caption_data.caption}\n")
                if caption_data.hashtags:
                    f.write(f"Hashtags: {' '.join(caption_data.hashtags)}\n")
                f.write("\n" + "-"*50 + "\n\n")
        
        return f"Trip plan saved to {output_dir}/ directory" 