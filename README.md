# BirdingPlanner 🦅

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

**Enterprise-grade AI-powered birding trip planning system** with tier-based species classification, intelligent route optimization, and comprehensive content generation.

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
- **eBird Trip Reports Integration**: Real-world trip data analysis
- **Community-Driven Insights**: Historical trip patterns and recommendations
- **Success Rate Comparison**: Traditional vs. trip report based predictions
- **Real-time eBird Data Integration**: Live observation data from global birding community
- **Success Rate Prediction**: Historical data-based viewing probability
- **Hotspot Activity Analysis**: Location-specific birding recommendations

### ✍️ Natural Storytelling Content
- Generates engaging birding stories and narratives
- Creates social media captions with hashtags
- Produces detailed observation logs
- Builds comprehensive trip plans in Markdown format

## 🏗️ Architecture

BirdingPlanner采用**混合架构**，结合了AI Agent编排和企业级服务层架构的优势：

### **架构概览**
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

### **AI Agent架构 (MCP Server)**
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

### **数据流架构**
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

### **架构特点**

#### **1. 双模式架构**
- **AI增强模式**: 使用MCP Server和AI Agents进行智能规划
- **标准模式**: 使用传统的服务层架构进行规划
- **自动降级**: AI失败时自动切换到标准模式
- **智能路线选择**: 根据物种稀有程度自动选择本地或长途路线

#### **2. AI Agent层**
- **SpeciesAgent**: AI驱动的物种分类、置信度评分和可用性分析
- **RouteAgent**: 机器学习优化的路线规划、热点推荐和兼容性评分
- **ContentAgent**: 自然语言生成的故事创作、社交媒体内容和Markdown格式化
- **AgentOrchestrator**: 智能任务编排、依赖管理和结果编译

#### **3. 服务层**
- **SpeciesService**: 物种数据管理、分类和可用性分析
- **RouteService**: 智能路线优化、本地/长途判断、距离计算
- **ContentService**: 内容生成、故事创作和格式化
- **BirdingPlanner**: 主应用类，协调所有服务

#### **4. 数据模型层**
- **Species**: 物种信息、分类和可用性数据
- **Route**: 路线、位置和热点数据
- **Trip**: 旅行计划、内容和摘要数据

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

# Option 3: Configure API Keys (optional, for real-time data)
# 方法1: 环境变量
export EBIRD_API_KEY=your_ebird_api_key_here

# 方法2: .env文件 (推荐)
cp env.example .env
# 然后编辑.env文件，填入您的API密钥
# Get your eBird API key from: https://ebird.org/api/keygen
```

### CLI Usage

#### **标准模式 (Service Layer)**
```bash
# 激活虚拟环境
source birding_env/bin/activate

# 创建标准旅行计划
python -m src.cli.main plan \
  --species "American Robin" "Northern Cardinal" \
  --location "New York" \
  --date "Spring 2024" \
  --output "my_trip"

# 获取物种信息
python -m src.cli.main species --name "American Robin"

# 列出所有可用物种
python -m src.cli.main species --list

# 获取应用信息
python -m src.cli.main info
```

#### **AI增强模式 (MCP Server)**
```bash
# 创建AI增强旅行计划
python -m src.cli.main plan \
  --species "American Robin" "Northern Cardinal" \
  --location "New York" \
  --date "Spring 2024" \
  --ai \
  --output "ai_trip"

# MCP Server操作
python -m src.cli.main mcp --status          # 查看服务器状态
python -m src.cli.main mcp --capabilities    # 查看AI Agent能力
python -m src.cli.main mcp --health          # 健康检查
python -m src.cli.main mcp --interactive     # 交互模式
```

#### **高级选项**
```bash
# 详细输出模式
python -m src.cli.main plan \
  --species "American Robin" "Northern Cardinal" \
  --location "New York" \
  --date "Spring 2024" \
  --ai \
  --output "ai_trip" \
  --verbose

# 自定义站点数量
python -m src.cli.main plan \
  --species "American Robin" "Northern Cardinal" "Blue Jay" \
  --location "New York" \
  --date "Spring 2024" \
  --stops 5 \
  --ai \
  --output "custom_trip"
```

#### **eBird集成测试**
```bash
# 测试eBird API集成
python test_ebird_integration.py

# 测试Trip Reports功能
python test_trip_reports.py

# 运行eBird功能演示
python demo_ebird_integration.py

# 查看API密钥配置指南
cat docs/api_keys.md
```

### Programmatic Usage

#### **标准模式 (Service Layer)**
```python
from src.core.birding_planner import BirdingPlanner
from src.models.trip import TripRequest
from src.config.settings import get_settings

# 初始化应用
settings = get_settings()
planner = BirdingPlanner(settings)

# 创建旅行请求
request = TripRequest(
    species=["American Robin", "Northern Cardinal"],
    base_location="New York",
    date_range="Spring 2024",
    max_stops=3
)

# 生成旅行计划
trip_plan = planner.create_trip_plan(request)

# 保存到文件
planner.save_trip_plan(trip_plan, "output")

# 获取物种信息
species_info = planner.get_species_info("American Robin")
all_species = planner.get_all_species()
```

#### **AI增强模式 (MCP Server)**
```python
from src.mcp.server import MCPServer
from src.models.trip import TripRequest
from src.config.settings import get_settings

# 初始化MCP Server
settings = get_settings()
mcp_server = MCPServer(settings)

# 创建AI增强旅行计划
trip_plan = mcp_server.create_trip_plan(
    species=["American Robin", "Northern Cardinal"],
    base_location="New York",
    date_range="Spring 2024",
    max_stops=3,
    output_dir="ai_output"
)

# 检查服务器状态
status = mcp_server.get_server_status()
capabilities = mcp_server.get_agent_capabilities()
health = mcp_server.health_check()

# 执行单个Agent任务
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

#### **直接使用AI Agents**
```python
from src.mcp.agents import SpeciesAgent, RouteAgent, ContentAgent
from src.mcp.agents import AgentTask

# 初始化AI Agents
species_agent = SpeciesAgent()
route_agent = RouteAgent()
content_agent = ContentAgent()

# 物种分析
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

# 路线优化
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

#### **eBird集成使用**
```python
from src.core.ebird_service import EBirdService
from src.mcp.ebird_agent import EBirdAgent, AgentTask
from src.config.settings import get_settings

# 初始化eBird服务
settings = get_settings()
ebird_service = EBirdService(settings.ebird_api_key)
ebird_agent = EBirdAgent(ebird_service)

# 获取实时观察数据
observations = ebird_service.get_recent_observations("New York", days=7)
print(f"Found {len(observations)} recent observations")

# 预测成功率
success_rate = ebird_service.predict_success_rate(
    "American Robin", "New York", "2024-04-15"
)
print(f"Success rate: {success_rate:.1%}")

# AI增强物种分析
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
    analysis = result.data.get('analysis')
    print(f"AI Insights: {analysis.ai_insights}")
    print(f"Best Time: {analysis.best_time}")
    print(f"Success Rate: {analysis.success_rate:.1%}")
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

### **智能本地观鸟 (常见鸟种)**
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

### **长途观鸟规划 (稀有鸟种)**
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

### **AI增强模式输出**
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

This project demonstrates enterprise-level software engineering practices:

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
