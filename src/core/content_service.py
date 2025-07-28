"""
Content service for BirdingPlanner.
Handles story generation and content creation.
"""

import random
from typing import Dict, List
from ..models.trip import TripContent, StoryCard, SocialCaption
from ..models.species import Species


class ContentService:
    """Service for generating content and stories."""
    
    def __init__(self):
        """Initialize the content service."""
        self._story_templates = self._initialize_story_templates()
        self._species_descriptions = self._initialize_species_descriptions()
    
    def _initialize_story_templates(self) -> Dict[str, List[str]]:
        """Initialize story templates."""
        return {
            "discovery": [
                "As the first light painted the sky, I found myself standing in {location}, binoculars in hand and hope in heart. The morning chorus was just beginning, and I was searching for {species}.",
                "The crisp morning air carried the promise of new discoveries as I ventured into {location}. My target today was the elusive {species}, a bird I had been hoping to encounter.",
                "With camera ready and field guide in hand, I set out in {location} with one goal: to find and observe the {species} in its natural habitat."
            ],
            "encounter": [
                "The distinctive call of the {species} echoed through {location}, and moments later, I spotted it perched majestically on a low branch.",
                "Suddenly, there it was! The {species} appeared before me in {location}, its vibrant colors catching the morning light perfectly.",
                "After hours of patient waiting, my persistence paid off when the {species} finally revealed itself in {location}, a moment I'll never forget."
            ],
            "reflection": [
                "The {species} may be common to some, but to me, each sighting is unique and precious. It's these simple connections that keep me coming back to {location}.",
                "Watching the {species} in {location} reminded me why I love birding - every encounter tells a story, every moment is a gift from nature.",
                "As I observed the {species} in {location}, I felt a deep connection to the natural world, a reminder of the beauty that surrounds us."
            ]
        }
    
    def _initialize_species_descriptions(self) -> Dict[str, Dict[str, str]]:
        """Initialize species-specific descriptions."""
        return {
            "American Robin": {
                "appearance": "rusty-orange breast and dark gray back",
                "behavior": "hops along the ground searching for worms",
                "call": "cheerful, musical song",
                "habitat": "lawns, gardens, and open woodlands"
            },
            "Northern Cardinal": {
                "appearance": "bright red plumage with a distinctive crest",
                "behavior": "sings from high perches to defend territory",
                "call": "clear, whistled song",
                "habitat": "thickets, hedges, and backyard feeders"
            },
            "Blue Jay": {
                "appearance": "blue crest and wings with white underparts",
                "behavior": "bold and intelligent, often mimics other birds",
                "call": "loud, harsh calls and whistles",
                "habitat": "forests, parks, and suburban areas"
            },
            "Red-tailed Hawk": {
                "appearance": "large raptor with reddish tail",
                "behavior": "soars high above open areas",
                "call": "high-pitched scream",
                "habitat": "open fields, highways, and woodlands"
            },
            "Baltimore Oriole": {
                "appearance": "bright orange and black plumage",
                "behavior": "weaves intricate hanging nests",
                "call": "flute-like whistles",
                "habitat": "trees, especially near water"
            },
            "Cerulean Warbler": {
                "appearance": "sky-blue upperparts and white underparts",
                "behavior": "forages high in the canopy",
                "call": "high-pitched buzzy song",
                "habitat": "mature deciduous forests"
            }
        }
    
    def generate_story_card(self, species: str, location: str) -> str:
        """Generate a story card for a species encounter."""
        # Get species description
        species_desc = self._species_descriptions.get(species, {
            "appearance": "beautiful plumage",
            "behavior": "graceful movements",
            "call": "melodious song",
            "habitat": "natural surroundings"
        })
        
        # Generate story using templates
        discovery = random.choice(self._story_templates["discovery"]).format(
            species=species, location=location
        )
        
        encounter = random.choice(self._story_templates["encounter"]).format(
            species=species, location=location
        )
        
        reflection = random.choice(self._story_templates["reflection"]).format(
            species=species, location=location
        )
        
        # Combine into full story
        story = f"{discovery}\n\n{encounter}\n\n{reflection}"
        
        return story
    
    def generate_social_caption(self, species: str, location: str, tier: str) -> str:
        """Generate a social media caption for a species sighting."""
        tier_emojis = {
            "T1": "🐦",
            "T2": "🦅", 
            "T3": "🦆",
            "T4": "🦉",
            "T5": "🦅✨"
        }
        
        tier_messages = {
            "T1": "A wonderful encounter with this common companion!",
            "T2": "Great find! This regional beauty never disappoints.",
            "T3": "Perfect timing for this seasonal visitor!",
            "T4": "Incredible luck spotting this elusive explorer!",
            "T5": "A once-in-a-lifetime sighting! Feeling blessed!"
        }
        
        emoji = tier_emojis.get(tier, "🐦")
        message = tier_messages.get(tier, "Amazing birding moment!")
        
        caption = f"{emoji} {message} Spotted this beautiful {species} in {location}. "
        caption += "The joy of birding is in these precious moments of connection with nature. "
        caption += "#BirdingLife #BirdPhotography #NatureLover #BirdWatching"
        
        return caption
    
    def generate_trip_plan_markdown(self, route_data, species_data: List[Species], request) -> str:
        """Generate a comprehensive trip plan in Markdown format."""
        markdown = f"""# Birding Trip Plan: {request.base_location}

## 🦅 Trip Overview
- **Base Location**: {request.base_location}
- **Target Species**: {', '.join(request.species)}
- **Date Range**: {request.date_range}
- **Total Stops**: {route_data.total_stops}
- **Total Distance**: {route_data.total_distance:.1f} km
- **Estimated Time**: {route_data.estimated_total_time}

## 🎯 Target Species Analysis

"""
        
        for species in species_data:
            markdown += f"""### {species.name} ({species.scientific_name})
- **Tier**: {species.tier.value} - {species.tier_description}
- **Occurrence Rate**: {species.occurrence_rate:.1%}
- **Visibility**: {species.visibility}
- **Challenge**: {species.tier_challenge}

"""
        
        markdown += """## 🗺️ Route Details

"""
        
        for stop in route_data.stops:
            markdown += f"""### Stop {stop.stop_number}: {stop.location.name}
- **Distance**: {stop.distance_from_previous:.1f} km
- **Travel Time**: {stop.travel_time}
- **Species Compatibility**: {stop.species_compatibility:.2f}

#### Recommended Hotspots:
"""
            for hotspot in stop.hotspots:
                markdown += f"- **{hotspot.name}**: {hotspot.species_count} species - {hotspot.description}\n"
            
            markdown += f"""
#### Viewing Schedule:
- **Best Time**: {stop.viewing_schedule.recommended_time}
- **Activity**: {stop.viewing_schedule.activity_description}
- **Duration**: {stop.viewing_schedule.estimated_duration}

#### Recommendations:
"""
            for rec in stop.recommendations:
                markdown += f"- {rec}\n"
            
            markdown += "\n"
        
        markdown += """## 📋 Packing List
- Binoculars (8x42 or 10x42 recommended)
- Field guide or birding app
- Camera with telephoto lens
- Comfortable walking shoes
- Weather-appropriate clothing
- Water and snacks
- Notebook for observations
- Sun protection (hat, sunscreen)

## 💡 Birding Tips
- Arrive early for the best birding (dawn to mid-morning)
- Move slowly and quietly to avoid startling birds
- Listen for bird calls and songs
- Use the sun at your back for better lighting
- Keep a respectful distance from nesting birds
- Record your observations for future reference

## 📝 Post-Trip Notes
*Use this section to record your observations, photos taken, and memorable moments.*

### Species Sighted:
- [ ] American Robin
- [ ] Northern Cardinal
- [ ] Blue Jay

### Photos Taken:
- [ ] Species photos
- [ ] Habitat shots
- [ ] Landscape views

### Memorable Moments:
*Record any special encounters or observations here*

---
*Generated by BirdingPlanner - Your AI-powered birding companion* 🦅
"""
        
        return markdown
    
    def generate_trip_content(self, route_data, species_data: List[Species], request) -> TripContent:
        """Generate complete trip content."""
        # Generate trip plan markdown
        trip_plan_markdown = self.generate_trip_plan_markdown(route_data, species_data, request)
        
        # Generate story cards
        story_cards = []
        for species in species_data:
            story = self.generate_story_card(species.name, request.base_location)
            story_card = StoryCard(
                species=species.name,
                location=request.base_location,
                date=request.date_range,
                story=story,
                tier=species.tier.value
            )
            story_cards.append(story_card)
        
        # Generate social captions
        social_captions = []
        for species in species_data:
            caption = self.generate_social_caption(species.name, request.base_location, species.tier.value)
            social_caption = SocialCaption(
                species=species.name,
                tier=species.tier.value,
                caption=caption,
                hashtags=["#BirdingLife", "#BirdPhotography", "#NatureLover", "#BirdWatching"]
            )
            social_captions.append(social_caption)
        
        return TripContent(
            trip_plan_markdown=trip_plan_markdown,
            story_cards=story_cards,
            social_captions=social_captions
        ) 