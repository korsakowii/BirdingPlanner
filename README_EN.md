# BirdingPlanner 🦅

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

**AI-powered birding trip planning system** with tier-based species classification, intelligent route optimization, and comprehensive content generation.

## 🌟 Features

### 🎯 Tier-Based Species Classification (T1-T5)
- **T1: Common Companion** - Very common, easy to spot in most areas
- **T2: Regional Companion** - Common in specific regions, moderate difficulty  
- **T3: Seasonal Visitor** - Appears during specific seasons, requires timing
- **T4: Elusive Explorer** - Rare, requires specific conditions and patience
- **T5: Legendary Quest** - Very rare, special sightings that become memorable stories

### 🗺️ Intelligent Route Planning
- **Smart Local vs. Long-Distance Routing**: Automatically detects when species are available locally
- **Distance Optimization**: 3208km → 24km for common species (American Robin, Northern Cardinal)
- **Practical Recommendations**: Context-aware suggestions for different skill levels
- **Realistic Travel Times**: 15-35 minutes between local hotspots vs. hours for long-distance travel
- **Species Compatibility Scoring**: Intelligent threshold-based routing decisions
- **Haversine Distance Calculation**: Accurate geographic distance computation
- **Best Hotspot Recommendations**: Optimized viewing locations for each species

### 📊 Species Availability Analysis
- Seasonal and regional availability matching
- Confidence scoring for species sightings
- Optimal viewing times and conditions
- Habitat preference analysis

### ✍️ Natural Storytelling Content
- Generates engaging birding stories and narratives
- Creates social media captions with hashtags
- Produces detailed observation logs
- Builds comprehensive trip plans in Markdown format

## 🏗️ Architecture

BirdingPlanner adopts a **hybrid architecture** that combines the advantages of AI Agent orchestration and service layer architecture:

### **Architecture Overview**
```
┌─────────────────────────────────────────────────────────────────┐
│                    User Interface Layer                         │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   CLI Interface │   API Layer     │  Web Interface (Future)     │
└─────────┬───────┴─────────┬───────┴─────────────┬───────────────┘
          │                 │                     │
          └─────────────────┼─────────────────────┘
                            │
                ┌───────────▼───────────┐
                │    Planning Mode      │
                │   Selection Logic     │
                └───────────┬───────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
    ┌─────▼─────┐    ┌──────▼──────┐    ┌────▼────┐
    │   AI Mode │    │Standard Mode│    │Fallback │
    │(MCP Server)│    │(Core Planner)│    │  Mode   │
    └─────┬─────┘    └──────┬──────┘    └────┬────┘
          │                 │                │
          └─────────────────┼────────────────┘
                            │
                ┌───────────▼───────────┐
                │   Service Layer       │
                │  (Business Logic)     │
                └───────────┬───────────┘
                            │
                ┌───────────▼───────────┐
                │   Data Models         │
                │  (Domain Objects)     │
                └───────────────────────┘
```

### **AI Agent Architecture (MCP Server)**
```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server                               │
│              (Agent Orchestrator)                           │
├─────────────────┬─────────────────┬─────────────────────────┤
│  Species Agent  │  Route Agent    │  Content Agent          │
│  (AI Classifier)│  (AI Optimizer) │  (AI Generator)         │
└─────────┬───────┴─────────┬───────┴─────────┬───────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                ┌───────────▼───────────┐
                │   Core Services       │
                │  (Shared Backend)     │
                └───────────────────────┘
```

### **Data Flow Architecture**
```
User Request
     │
     ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   CLI       │───▶│   Mode      │───▶│   AI Mode   │
│  Interface  │    │ Selection   │    │(MCP Server) │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                 │
                           ▼                 ▼
                    ┌─────────────┐    ┌─────────────┐
                    │ Standard    │    │ Agent       │
                    │ Mode        │    │ Orchestrator│
                    │(Core Planner)│    └─────────────┘
                    └─────────────┘            │
                           │                   │
                           └─────────┬─────────┘
                                     │
                                     ▼
                            ┌─────────────┐
                            │   Service   │
                            │   Layer     │
                            └─────────────┘
                                     │
                                     ▼
                            ┌─────────────┐
                            │   Data      │
                            │  Models     │
                            └─────────────┘
```

### **Architecture Features**

#### **1. Dual-Mode Architecture**
- **AI-Enhanced Mode**: Uses MCP Server and AI Agents for intelligent planning
- **Standard Mode**: Uses traditional service layer architecture for planning
- **Automatic Fallback**: Graceful degradation from AI to standard planning
- **Smart Route Selection**: Automatically chooses local or long-distance routes based on species rarity

#### **2. AI Agent Layer**
- **SpeciesAgent**: AI-driven species classification, confidence scoring, and availability analysis
- **RouteAgent**: Machine learning route optimization, hotspot recommendations, and compatibility scoring
- **ContentAgent**: Natural language generation for stories, social media content, and Markdown formatting
- **AgentOrchestrator**: Intelligent task orchestration, dependency management, and result compilation

#### **3. Service Layer**
- **SpeciesService**: Species data management, classification, and availability analysis
- **RouteService**: Intelligent route optimization, local/long-distance decision making, distance calculation
- **ContentService**: Content generation, story creation, and formatting
- **BirdingPlanner**: Main application class that orchestrates all services

#### **4. Data Model Layer**
- **Species**: Species information, classification, and availability data
- **Route**: Route, location, and hotspot data
- **Trip**: Trip planning, content, and summary data

## 📁 Project Structure

```
BirdingPlanner/
├── src/                          # Main source code
│   ├── __init__.py              # Package initialization
│   ├── models/                   # Data models (Domain Objects)
│   │   ├── __init__.py          # Model aggregations
│   │   ├── species.py           # Species, tiers, availability
│   │   ├── route.py             # Routes, locations, hotspots
│   │   └── trip.py              # Trip plans, requests, content
│   ├── core/                    # Core services (Business Logic)
│   │   ├── __init__.py          # Service aggregations
│   │   ├── birding_planner.py   # Main application orchestrator
│   │   ├── species_service.py   # Species data & classification
│   │   ├── route_service.py     # Route optimization & planning
│   │   └── content_service.py   # Content generation & formatting
│   ├── mcp/                     # AI Agent orchestration
│   │   ├── __init__.py          # MCP package initialization
│   │   ├── server.py            # MCP Server & CLI integration
│   │   ├── orchestrator.py      # Agent task orchestration
│   │   └── agents.py            # AI Agent implementations
│   ├── config/                  # Configuration management
│   │   ├── __init__.py          # Config aggregations
│   │   ├── settings.py          # Application settings
│   │   ├── database.py          # Database configuration
│   │   └── logging.py           # Logging configuration
│   └── cli/                     # Command-line interface
│       ├── __init__.py          # CLI package initialization
│       └── main.py              # CLI entry point & commands
├── tests/                       # Test suite
│   ├── __init__.py              # Test package initialization
│   └── test_models.py           # Data model unit tests
├── docs/                        # Documentation
├── output/                      # Generated trip plans
├── data/                        # Data files
├── agents/                      # Legacy agent modules (deprecated)
├── mcp_server/                  # Legacy MCP server (deprecated)
├── pyproject.toml              # Modern Python project config
├── requirements.txt            # Dependencies
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # Multi-service deployment
├── setup_env.sh               # Environment setup script
├── check_status.py            # System status checker
├── demo_hybrid_architecture.py # Hybrid architecture demo
├── CHANGELOG.md               # Version history and changes
└── README.md                  # This file
```

## 🚀 Quick Start

### Environment Setup
```bash
# Option 1: Use the setup script (recommended)
./setup_env.sh

# Option 2: Manual setup
python3 -m venv birding_env
source birding_env/bin/activate
pip install -r requirements.txt
```

### CLI Usage

#### **Standard Mode (Service Layer)**
```bash
# Activate virtual environment
source birding_env/bin/activate

# Create standard trip plan
python -m src.cli.main plan \
  --species "American Robin" "Northern Cardinal" \
  --location "New York" \
  --date "Spring 2024" \
  --output "my_trip"

# Get species information
python -m src.cli.main species --name "American Robin"

# List all available species
python -m src.cli.main species --list

# Get application information
python -m src.cli.main info
```

#### **AI-Enhanced Mode (MCP Server)**
```bash
# Create AI-enhanced trip plan
python -m src.cli.main plan \
  --species "American Robin" "Northern Cardinal" \
  --location "New York" \
  --date "Spring 2024" \
  --ai \
  --output "ai_trip"

# MCP Server operations
python -m src.cli.main mcp --status          # Check server status
python -m src.cli.main mcp --capabilities    # View AI Agent capabilities
python -m src.cli.main mcp --health          # Health check
python -m src.cli.main mcp --interactive     # Interactive mode
```

#### **Advanced Options**
```bash
# Verbose output mode
python -m src.cli.main plan \
  --species "American Robin" "Northern Cardinal" \
  --location "New York" \
  --date "Spring 2024" \
  --ai \
  --output "ai_trip" \
  --verbose

# Custom number of stops
python -m src.cli.main plan \
  --species "American Robin" "Northern Cardinal" "Blue Jay" \
  --location "New York" \
  --date "Spring 2024" \
  --stops 5 \
  --ai \
  --output "custom_trip"
```

### Programmatic Usage

#### **Standard Mode (Service Layer)**
```python
from src.core.birding_planner import BirdingPlanner
from src.models.trip import TripRequest
from src.config.settings import get_settings

# Initialize application
settings = get_settings()
planner = BirdingPlanner(settings)

# Create trip request
request = TripRequest(
    species=["American Robin", "Northern Cardinal"],
    base_location="New York",
    date_range="Spring 2024",
    max_stops=3
)

# Generate trip plan
trip_plan = planner.create_trip_plan(request)

# Save to files
planner.save_trip_plan(trip_plan, "output")

# Get species information
species_info = planner.get_species_info("American Robin")
all_species = planner.get_all_species()
```

#### **AI-Enhanced Mode (MCP Server)**
```python
from src.mcp.server import MCPServer
from src.models.trip import TripRequest
from src.config.settings import get_settings

# Initialize MCP Server
settings = get_settings()
mcp_server = MCPServer(settings)

# Create AI-enhanced trip plan
trip_plan = mcp_server.create_trip_plan(
    species=["American Robin", "Northern Cardinal"],
    base_location="New York",
    date_range="Spring 2024",
    max_stops=3,
    output_dir="ai_output"
)

# Check server status
status = mcp_server.get_server_status()
capabilities = mcp_server.get_agent_capabilities()
health = mcp_server.health_check()

# Execute individual agent task
from src.mcp.agents import AgentTask
task = AgentTask(
    agent_name="SpeciesAgent",
    task_type="species_classification",
    input_data={
        "species": ["American Robin"],
        "location": "New York",
        "date_range": "Spring 2024"
    }
)
result = mcp_server.execute_agent_task(task)
```

#### **Direct AI Agent Usage**
```python
from src.mcp.agents import SpeciesAgent, RouteAgent, ContentAgent
from src.mcp.agents import AgentTask

# Initialize AI Agents
species_agent = SpeciesAgent()
route_agent = RouteAgent()
content_agent = ContentAgent()

# Species analysis
species_task = AgentTask(
    agent_name="SpeciesAgent",
    task_type="species_classification",
    input_data={
        "species": ["American Robin", "Northern Cardinal"],
        "location": "New York",
        "date_range": "Spring 2024"
    }
)
species_result = species_agent.execute(species_task)

# Route optimization
route_task = AgentTask(
    agent_name="RouteAgent",
    task_type="route_optimization",
    input_data={
        "base_location": "New York",
        "target_species": ["American Robin", "Northern Cardinal"],
        "date_range": "Spring 2024",
        "max_stops": 3,
        "species_analysis": species_result.data
    }
)
route_result = route_agent.execute(route_task)
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker
docker build -t birdingplanner .
docker run -p 8000:8000 birdingplanner

# Or use Docker Compose
docker-compose up -d
```

## 📋 Example Output

### **Smart Local Birding (Common Species)**
```
🦅 BirdingPlanner - Creating Your Trip Plan
==================================================

Target Species: American Robin, Northern Cardinal, Blue Jay
Base Location: New York
Date Range: Spring 2024
Max Stops: 3
AI Enhanced: False

📋 Using standard planning...

✅ Trip plan saved to local_birding/ directory

📋 Trip Plan Summary:
   Base Location: New York
   Target Species: American Robin, Northern Cardinal, Blue Jay
   Total Stops: 3
   Total Distance: 24.0 km
   Estimated Time: 4-6 hours

🎯 Species Tiers:
   American Robin: T1
   Northern Cardinal: T1
   Blue Jay: T2

📁 Generated Files:
   - local_birding/trip_plan.md (Complete trip plan)
   - local_birding/story_cards/ (Individual story cards)
   - local_birding/social_captions.txt (Social media content)

💡 Smart Recommendations:
   - Perfect for local birding - no long travel needed!
   - Visit during dawn chorus for best results
   - These common species are easily found locally
   - Great for beginners or time-limited birders
```

### **Long-Distance Birding (Rare Species)**
```
🦅 BirdingPlanner - Creating Your Trip Plan
==================================================

Target Species: Cerulean Warbler, Baltimore Oriole, Scarlet Tanager
Base Location: New York
Date Range: Spring 2024
Max Stops: 3
AI Enhanced: False

📋 Using standard planning...

✅ Trip plan saved to rare_birding/ directory

📋 Trip Plan Summary:
   Base Location: New York
   Target Species: Cerulean Warbler, Baltimore Oriole, Scarlet Tanager
   Total Stops: 3
   Total Distance: 3208.4 km
   Estimated Time: 59 hours

🎯 Species Tiers:
   Cerulean Warbler: T4 (Elusive Explorer)
   Baltimore Oriole: T3 (Seasonal Visitor)
   Scarlet Tanager: T4 (Elusive Explorer)

📁 Generated Files:
   - rare_birding/trip_plan.md (Complete trip plan)
   - rare_birding/story_cards/ (Individual story cards)
   - rare_birding/social_captions.txt (Social media content)

💡 Smart Recommendations:
   - These rare species require specialized travel
   - Arrive early for best birding opportunities
   - Bring binoculars and field guide
   - Check weather conditions before travel
```

### **AI-Enhanced Mode Output**
```
🦅 BirdingPlanner - Creating Your Trip Plan
==================================================

Target Species: American Robin, Northern Cardinal
Base Location: New York
Date Range: Spring 2024
Max Stops: 3
AI Enhanced: True

🤖 Using AI Agents for enhanced planning...

📊 AI Agent Status:
   SpeciesAgent: Active (AI Classification)
   RouteAgent: Active (ML Optimization)
   ContentAgent: Active (NLG Generation)

📋 AI-Enhanced Trip Plan Summary:
   Base Location: New York
   Target Species: American Robin, Northern Cardinal
   Total Stops: 3
   Total Distance: 24.0 km (AI Optimized)
   Estimated Time: 4-6 hours (AI Optimized)

🎯 AI-Enhanced Species Analysis:
   American Robin: T1 (Confidence: 95%)
     - AI Recommendation: Excellent viewing conditions in Spring
     - Habitat Suitability: High (Urban parks and gardens)
     - Optimal Viewing: Early morning (6-8 AM)
   
   Northern Cardinal: T1 (Confidence: 92%)
     - AI Recommendation: Very common, multiple viewing opportunities
     - Habitat Suitability: High (Wooded areas and feeders)
     - Optimal Viewing: Dawn and dusk

🤖 AI-Generated Insights:
   - AI detected local availability and optimized for local birding
   - Generated 5 personalized story cards with location-specific details
   - Created 3 social media captions with trending hashtags
   - Enhanced route recommendations with AI confidence scoring

📁 Generated Files:
   - ai_enhanced/trip_plan.md (AI-enhanced trip plan)
   - ai_enhanced/story_cards/ (AI-generated stories)
   - ai_enhanced/social_captions/ (AI-optimized captions)
   - ai_enhanced/trip_data.json (Complete AI analysis data)
```

### Generated Story Example
```
Species: American Robin
Location: New York
Date: Spring 2024
Tier: T1

==================================================

As the first light painted the sky, I found myself standing in New York, 
binoculars in hand and hope in heart. The morning chorus was just beginning, 
and I was searching for American Robin.

The distinctive call of the American Robin echoed through New York, and moments 
later, I spotted it perched majestically on a low branch.

The American Robin may be common to some, but to me, each sighting is unique 
and precious. It's these simple connections that keep me coming back to New York.
```

## 🎯 Tier System Examples

### T1 - Common Companion
- **American Robin**: Found in 48 states, 85% occurrence rate
- **Northern Cardinal**: Year-round resident, very easy to spot
- **Blue Jay**: Widespread, high visibility

### T2 - Regional Companion  
- **Red-tailed Hawk**: Found across North America, moderate difficulty
- **American Goldfinch**: Regional variations, seasonal patterns

### T3 - Seasonal Visitor
- **Baltimore Oriole**: Spring/Summer migrant, specific timing required
- **Scarlet Tanager**: Forest-dwelling, seasonal appearance

### T4 - Elusive Explorer
- **Cerulean Warbler**: High-canopy specialist, low occurrence rate
- **Kirtland's Warbler**: Very limited range, specific habitat needs

### T5 - Legendary Quest
- **Ivory-billed Woodpecker**: Extremely rare, possibly extinct
- **Special rarities**: Once-in-a-lifetime sightings

## 🔧 Technical Details

### **Dependencies**
- **Core**: Python 3.7+, dataclasses, typing, datetime
- **CLI**: argparse, pathlib
- **Development**: pytest, black, flake8, mypy
- **Documentation**: sphinx, sphinx-rtd-theme
- **Containerization**: Docker, docker-compose

### **Code Quality**
- **Type Hints**: Full type annotation coverage across all modules
- **Code Formatting**: Black code formatter with consistent style
- **Linting**: Flake8 for style checking and code quality
- **Type Checking**: MyPy for static analysis and type safety
- **Testing**: Pytest with coverage reporting and comprehensive test suite

### **Configuration**
- **Environment-based**: Settings from environment variables with defaults
- **Flexible**: Easy to customize for different deployments and environments
- **Logging**: Structured logging with file and console output
- **Validation**: Comprehensive input validation and error handling

### **AI Agent Implementation Details**

#### **Agent Task System**
```python
@dataclass
class AgentTask:
    agent_name: str          # Target agent (SpeciesAgent, RouteAgent, ContentAgent)
    task_type: str           # Task type (species_classification, route_optimization, etc.)
    input_data: Dict[str, Any]  # Input parameters
    priority: int = 1        # Task priority (1-5)
    dependencies: List[str] = None  # Dependent agents
```

#### **Agent Result System**
```python
@dataclass
class AgentResult:
    agent_name: str          # Source agent
    task_type: str           # Completed task type
    success: bool            # Execution success status
    data: Dict[str, Any]     # Result data
    metadata: Dict[str, Any] = None  # Execution metadata
    timestamp: datetime = None  # Execution timestamp
```

#### **AI Enhancement Features**
- **SpeciesAgent**: 
  - AI-powered tier classification with confidence scoring
  - Location-specific availability analysis
  - Seasonal pattern recognition
  - Habitat suitability assessment

- **RouteAgent**:
  - Machine learning route optimization
  - AI-enhanced hotspot recommendations
  - Compatibility scoring between species and locations
  - Optimal viewing schedule generation

- **ContentAgent**:
  - Natural language story generation
  - AI-optimized social media captions
  - Contextual hashtag generation
  - Markdown formatting with AI insights

#### **Fallback Mechanism**
- Automatic fallback to standard service layer if AI agents fail
- Graceful degradation ensures system reliability
- Comprehensive error logging and monitoring
- Seamless user experience regardless of AI availability

## 🚀 Future Enhancements

### Planned Features
- **FastAPI Web API** for RESTful endpoints
- **Real-time eBird integration** for live species data
- **Weather integration** for optimal viewing conditions
- **Mobile app** with GPS tracking
- **Community features** for sharing sightings
- **Machine learning** for improved predictions

### Data Expansion
- **Global species database** beyond North America
- **More detailed habitat information**
- **Photography tips** for each species
- **Audio recordings** of bird calls

## 🤝 Contributing

This project demonstrates professional software engineering practices:

### Architecture Patterns
- **Service Layer Pattern**: Clean separation of concerns
- **Repository Pattern**: Data access abstraction
- **Factory Pattern**: Object creation management
- **Strategy Pattern**: Algorithm selection

### Development Practices
- **Test-Driven Development**: Comprehensive test coverage
- **Continuous Integration**: Automated testing and deployment
- **Code Review**: Peer review processes
- **Documentation**: Comprehensive API and user documentation

### Quality Assurance
- **Static Analysis**: Type checking and linting
- **Code Coverage**: Test coverage reporting
- **Performance Monitoring**: Application metrics
- **Security Scanning**: Vulnerability assessment

## 📄 License

This project is part of a portfolio demonstrating technical expertise and innovation in AI-assisted nature applications.

---

*BirdingPlanner - Making nature connection more accessible, one bird at a time.* 🦅✨ 