# BirdingPlanner 🦅

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

**AI驱动的观鸟旅行规划系统**，具备分级物种分类、智能路线优化和全面内容生成功能。

## 🌟 核心功能

### 🎯 分级物种分类系统 (T1-T5)
- **T1: 常见伙伴** - 非常常见，在大多数地区都容易发现
- **T2: 区域伙伴** - 在特定区域常见，难度适中
- **T3: 季节性访客** - 在特定季节出现，需要把握时机
- **T4: 神秘探索者** - 稀有，需要特定条件和耐心
- **T5: 传奇追寻** - 极其稀有，成为难忘故事的特殊目击

### 🗺️ 智能路线规划
- **智能本地/长途路线选择**: 自动检测物种是否在本地可用
- **距离优化**: 常见物种从3208公里优化到24公里 (如知更鸟、红雀)
- **实用建议**: 针对不同技能水平的上下文感知建议
- **真实旅行时间**: 本地热点间15-35分钟 vs 长途旅行数小时
- **物种兼容性评分**: 基于阈值的智能路线决策
- **哈弗辛距离计算**: 准确的地理距离计算
- **最佳观鸟点推荐**: 每个物种的优化观鸟位置

### 📊 物种可用性分析
- 季节性和区域性可用性匹配
- 物种目击的置信度评分
- 最佳观鸟时间和条件
- 栖息地偏好分析

### ✍️ 自然故事内容生成
- 生成引人入胜的观鸟故事和叙述
- 创建带标签的社交媒体标题
- 制作详细的观察记录
- 构建Markdown格式的全面旅行计划

## 🏗️ 系统架构

BirdingPlanner采用**混合架构**，结合了AI Agent编排和专业服务层架构的优势：

### **架构概览**
```
┌─────────────────────────────────────────────────────────────────┐
│                    用户界面层                                   │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   命令行界面    │   API层         │  网页界面 (未来)            │
└─────────┬───────┴─────────┬───────┴─────────────┬───────────────┘
          │                 │                     │
          └─────────────────┼─────────────────────┘
                            │
                ┌───────────▼───────────┐
                │    规划模式选择       │
                │   选择逻辑           │
                └───────────┬───────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
    ┌─────▼─────┐    ┌──────▼──────┐    ┌────▼────┐
    │  AI模式   │    │  标准模式   │    │  备用   │
    │(MCP服务器)│    │(核心规划器) │    │  模式   │
    └─────┬─────┘    └──────┬──────┘    └────┬────┘
          │                 │                │
          └─────────────────┼────────────────┘
                            │
                ┌───────────▼───────────┐
                │    服务层             │
                │  (业务逻辑)           │
                └───────────┬───────────┘
                            │
                ┌───────────▼───────────┐
                │    数据模型           │
                │  (领域对象)           │
                └───────────────────────┘
```

### **AI Agent架构 (MCP服务器)**
```
┌─────────────────────────────────────────────────────────────┐
│                    MCP服务器                                │
│              (Agent编排器)                                  │
├─────────────────┬─────────────────┬─────────────────────────┤
│  物种Agent      │  路线Agent      │  内容Agent              │
│  (AI分类器)     │  (AI优化器)     │  (AI生成器)             │
└─────────┬───────┴─────────┬───────┴─────────┬───────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                ┌───────────▼───────────┐
                │    核心服务           │
                │  (共享后端)           │
                └───────────────────────┘
```

### **数据流架构**
```
用户请求
     │
     ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   命令行    │───▶│   模式      │───▶│   AI模式    │
│   界面      │    │   选择      │    │(MCP服务器)  │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                 │
                           ▼                 ▼
                    ┌─────────────┐    ┌─────────────┐
                    │   标准      │    │   Agent     │
                    │   模式      │    │   编排器    │
                    │(核心规划器) │    └─────────────┘
                    └─────────────┘            │
                           │                   │
                           └─────────┬─────────┘
                                     │
                                     ▼
                            ┌─────────────┐
                            │   服务      │
                            │   层        │
                            └─────────────┘
                                     │
                                     ▼
                            ┌─────────────┐
                            │   数据      │
                            │   模型      │
                            └─────────────┘
```

### **架构特点**

#### **1. 双模式架构**
- **AI增强模式**: 使用MCP服务器和AI Agents进行智能规划
- **标准模式**: 使用传统的服务层架构进行规划
- **自动备用**: AI失败时自动切换到标准模式
- **智能路线选择**: 根据物种稀有程度自动选择本地或长途路线

#### **2. AI Agent层**
- **SpeciesAgent**: AI驱动的物种分类、置信度评分和可用性分析
- **RouteAgent**: 机器学习路线优化、热点推荐和兼容性评分
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

## 📁 项目结构

```
BirdingPlanner/
├── src/                          # 主要源代码
│   ├── __init__.py              # 包初始化
│   ├── models/                   # 数据模型 (领域对象)
│   │   ├── __init__.py          # 模型聚合
│   │   ├── species.py           # 物种、分级、可用性
│   │   ├── route.py             # 路线、位置、热点
│   │   └── trip.py              # 旅行计划、请求、内容
│   ├── core/                    # 核心服务 (业务逻辑)
│   │   ├── __init__.py          # 服务聚合
│   │   ├── birding_planner.py   # 主应用编排器
│   │   ├── species_service.py   # 物种数据和分类
│   │   ├── route_service.py     # 路线优化和规划
│   │   └── content_service.py   # 内容生成和格式化
│   ├── mcp/                     # AI Agent编排
│   │   ├── __init__.py          # MCP包初始化
│   │   ├── server.py            # MCP服务器和CLI集成
│   │   ├── orchestrator.py      # Agent任务编排
│   │   └── agents.py            # AI Agent实现
│   ├── config/                  # 配置管理
│   │   ├── __init__.py          # 配置聚合
│   │   ├── settings.py          # 应用设置
│   │   ├── database.py          # 数据库配置
│   │   └── logging.py           # 日志配置
│   └── cli/                     # 命令行界面
│       ├── __init__.py          # CLI包初始化
│       └── main.py              # CLI入口点和命令
├── tests/                       # 测试套件
│   ├── __init__.py              # 测试包初始化
│   └── test_models.py           # 数据模型单元测试
├── docs/                        # 文档
├── output/                      # 生成的旅行计划
├── data/                        # 数据文件
├── agents/                      # 遗留Agent模块 (已废弃)
├── mcp_server/                  # 遗留MCP服务器 (已废弃)
├── pyproject.toml              # 现代Python项目配置
├── requirements.txt            # 依赖项
├── Dockerfile                  # 容器配置
├── docker-compose.yml          # 多服务部署
├── setup_env.sh               # 环境设置脚本
├── check_status.py            # 系统状态检查器
├── demo_hybrid_architecture.py # 混合架构演示
├── CHANGELOG.md               # 版本历史和变更
└── README.md                  # 本文件
```

## 🚀 快速开始

### 环境设置
```bash
# 选项1: 使用设置脚本 (推荐)
./setup_env.sh

# 选项2: 手动设置
python3 -m venv birding_env
source birding_env/bin/activate
pip install -r requirements.txt
```

### 命令行使用

#### **标准模式 (服务层)**
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

#### **AI增强模式 (MCP服务器)**
```bash
# 创建AI增强旅行计划
python -m src.cli.main plan \
  --species "American Robin" "Northern Cardinal" \
  --location "New York" \
  --date "Spring 2024" \
  --ai \
  --output "ai_trip"

# MCP服务器操作
python -m src.cli.main mcp --status          # 检查服务器状态
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

### 编程使用

#### **标准模式 (服务层)**
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

#### **AI增强模式 (MCP服务器)**
```python
from src.mcp.server import MCPServer
from src.models.trip import TripRequest
from src.config.settings import get_settings

# 初始化MCP服务器
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

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行覆盖率测试
pytest --cov=src

# 运行特定测试文件
pytest tests/test_models.py

# 运行详细输出
pytest -v
```

## 🐳 Docker部署

```bash
# 使用Docker构建和运行
docker build -t birdingplanner .
docker run -p 8000:8000 birdingplanner

# 或使用Docker Compose
docker-compose up -d
```

## 📋 示例输出

### **智能本地观鸟 (常见物种)**
```
🦅 BirdingPlanner - 创建您的旅行计划
==================================================

目标物种: American Robin, Northern Cardinal, Blue Jay
基础位置: New York
日期范围: Spring 2024
最大站点: 3
AI增强: False

📋 使用标准规划...

✅ 旅行计划已保存到 local_birding/ 目录

📋 旅行计划摘要:
   基础位置: New York
   目标物种: American Robin, Northern Cardinal, Blue Jay
   总站点: 3
   总距离: 24.0 公里
   预计时间: 4-6 小时

🎯 物种分级:
   American Robin: T1
   Northern Cardinal: T1
   Blue Jay: T2

📁 生成文件:
   - local_birding/trip_plan.md (完整旅行计划)
   - local_birding/story_cards/ (个人故事卡片)
   - local_birding/social_captions.txt (社交媒体内容)

💡 智能建议:
   - 完美适合本地观鸟 - 无需长途旅行!
   - 在晨鸣时分访问效果最佳
   - 这些常见物种在本地很容易找到
   - 适合新手或时间有限的观鸟者
```

### **长途观鸟规划 (稀有物种)**
```
🦅 BirdingPlanner - 创建您的旅行计划
==================================================

目标物种: Cerulean Warbler, Baltimore Oriole, Scarlet Tanager
基础位置: New York
日期范围: Spring 2024
最大站点: 3
AI增强: False

📋 使用标准规划...

✅ 旅行计划已保存到 rare_birding/ 目录

📋 旅行计划摘要:
   基础位置: New York
   目标物种: Cerulean Warbler, Baltimore Oriole, Scarlet Tanager
   总站点: 3
   总距离: 3208.4 公里
   预计时间: 59 小时

🎯 物种分级:
   Cerulean Warbler: T4 (神秘探索者)
   Baltimore Oriole: T3 (季节性访客)
   Scarlet Tanager: T4 (神秘探索者)

📁 生成文件:
   - rare_birding/trip_plan.md (完整旅行计划)
   - rare_birding/story_cards/ (个人故事卡片)
   - rare_birding/social_captions.txt (社交媒体内容)

💡 智能建议:
   - 这些稀有物种需要专门旅行
   - 提前到达以获得最佳观鸟机会
   - 携带双筒望远镜和野外指南
   - 旅行前检查天气条件
```

### **AI增强模式输出**
```
🦅 BirdingPlanner - 创建您的旅行计划
==================================================

目标物种: American Robin, Northern Cardinal
基础位置: New York
日期范围: Spring 2024
最大站点: 3
AI增强: True

🤖 使用AI Agents进行增强规划...

📊 AI Agent状态:
   SpeciesAgent: 活跃 (AI分类)
   RouteAgent: 活跃 (ML优化)
   ContentAgent: 活跃 (NLG生成)

📋 AI增强旅行计划摘要:
   基础位置: New York
   目标物种: American Robin, Northern Cardinal
   总站点: 3
   总距离: 24.0 公里 (AI优化)
   预计时间: 4-6 小时 (AI优化)

🎯 AI增强物种分析:
   American Robin: T1 (置信度: 95%)
     - AI建议: 春季观鸟条件极佳
     - 栖息地适宜性: 高 (城市公园和花园)
     - 最佳观鸟时间: 清晨 (6-8 AM)
   
   Northern Cardinal: T1 (置信度: 92%)
     - AI建议: 非常常见，多种观鸟机会
     - 栖息地适宜性: 高 (林地地区和喂食器)
     - 最佳观鸟时间: 黎明和黄昏

🤖 AI生成洞察:
   - AI检测到本地可用性并优化为本地观鸟
   - 生成5个个性化故事卡片，包含位置特定细节
   - 创建3个社交媒体标题，包含热门标签
   - 通过AI置信度评分增强路线建议

📁 生成文件:
   - ai_enhanced/trip_plan.md (AI增强旅行计划)
   - ai_enhanced/story_cards/ (AI生成故事)
   - ai_enhanced/social_captions/ (AI优化标题)
   - ai_enhanced/trip_data.json (完整AI分析数据)
```

### 生成的故事示例
```
物种: American Robin
位置: New York
日期: Spring 2024
分级: T1

==================================================

当第一缕阳光染红天空时，我发现自己站在纽约，手持双筒望远镜，心中满怀希望。
晨鸣合唱刚刚开始，我正在寻找知更鸟。

知更鸟独特的叫声在纽约回荡，片刻之后，我发现它庄严地栖息在低矮的树枝上。

对某些人来说，知更鸟可能很常见，但对我来说，每次目击都是独特而珍贵的。
正是这些简单的联系让我不断回到纽约。
```

## 🎯 分级系统示例

### T1 - 常见伙伴
- **American Robin**: 在48个州发现，85%出现率
- **Northern Cardinal**: 全年居民，非常容易发现
- **Blue Jay**: 分布广泛，高可见性

### T2 - 区域伙伴  
- **Red-tailed Hawk**: 在北美各地发现，难度适中
- **American Goldfinch**: 区域变化，季节性模式

### T3 - 季节性访客
- **Baltimore Oriole**: 春季/夏季候鸟，需要把握时机
- **Scarlet Tanager**: 森林栖息，季节性出现

### T4 - 神秘探索者
- **Cerulean Warbler**: 高冠层专家，低出现率
- **Kirtland's Warbler**: 非常有限的范围，特定栖息地需求

### T5 - 传奇追寻
- **Ivory-billed Woodpecker**: 极其稀有，可能已灭绝
- **特殊稀有物种**: 一生一次的目击

## 🔧 技术细节

### **依赖项**
- **核心**: Python 3.7+, dataclasses, typing, datetime
- **CLI**: argparse, pathlib
- **开发**: pytest, black, flake8, mypy
- **文档**: sphinx, sphinx-rtd-theme
- **容器化**: Docker, docker-compose

### **代码质量**
- **类型提示**: 所有模块的完整类型注解覆盖
- **代码格式化**: Black代码格式化器，风格一致
- **代码检查**: Flake8用于风格检查和代码质量
- **类型检查**: MyPy用于静态分析和类型安全
- **测试**: Pytest，覆盖率报告和全面测试套件

### **配置**
- **基于环境**: 从环境变量加载设置，带默认值
- **灵活**: 易于为不同部署和环境定制
- **日志**: 结构化日志，文件和控制台输出
- **验证**: 全面的输入验证和错误处理

### **AI Agent实现细节**

#### **Agent任务系统**
```python
@dataclass
class AgentTask:
    agent_name: str          # 目标agent (SpeciesAgent, RouteAgent, ContentAgent)
    task_type: str           # 任务类型 (species_classification, route_optimization, 等)
    input_data: Dict[str, Any]  # 输入参数
    priority: int = 1        # 任务优先级 (1-5)
    dependencies: List[str] = None  # 依赖的agents
```

#### **Agent结果系统**
```python
@dataclass
class AgentResult:
    agent_name: str          # 源agent
    task_type: str           # 已完成的任务类型
    success: bool            # 执行成功状态
    data: Dict[str, Any]     # 结果数据
    metadata: Dict[str, Any] = None  # 执行元数据
    timestamp: datetime = None  # 执行时间戳
```

#### **AI增强功能**
- **SpeciesAgent**: 
  - AI驱动的分级分类，带置信度评分
  - 位置特定的可用性分析
  - 季节性模式识别
  - 栖息地适宜性评估

- **RouteAgent**:
  - 机器学习路线优化
  - AI增强热点推荐
  - 物种和位置间的兼容性评分
  - 最佳观鸟时间表生成

- **ContentAgent**:
  - 自然语言故事生成
  - AI优化社交媒体标题
  - 上下文标签生成
  - 带AI洞察的Markdown格式化

#### **备用机制**
- AI agents失败时自动切换到标准服务层
- 优雅备用确保系统可靠性
- 全面的错误日志和监控
- 无论AI可用性如何，都能提供无缝用户体验

## 🚀 未来增强

### 计划功能
- **FastAPI Web API** 用于RESTful端点
- **实时eBird集成** 用于实时物种数据
- **天气集成** 用于最佳观鸟条件
- **移动应用** 带GPS跟踪
- **社区功能** 用于分享目击
- **机器学习** 用于改进预测

### 数据扩展
- **全球物种数据库** 超越北美
- **更详细的栖息地信息**
- **每个物种的摄影技巧**
- **鸟叫音频录音**

## 🤝 贡献

本项目展示了专业软件工程实践：

### 架构模式
- **服务层模式**: 关注点分离
- **仓库模式**: 数据访问抽象
- **工厂模式**: 对象创建管理
- **策略模式**: 算法选择

### 开发实践
- **测试驱动开发**: 全面测试覆盖
- **持续集成**: 自动化测试和部署
- **代码审查**: 同行审查流程
- **文档**: 全面的API和用户文档

### 质量保证
- **静态分析**: 类型检查和代码检查
- **代码覆盖**: 测试覆盖率报告
- **性能监控**: 应用指标
- **安全扫描**: 漏洞评估

## 📄 许可证

本项目是展示AI辅助自然应用技术专业知识和创新能力的作品集的一部分。

---

*BirdingPlanner - 让自然连接更加便捷，一次一只鸟。* 🦅✨ 