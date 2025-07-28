# Birding Planner System Architecture

## Core System Modules

- **MCP Server**: Task orchestration layer
- **Agents**:
    - `bird_info_agent.py`: Fetch seasonal and regional match for target species
    - `tier_classifier.py`: Classify bird species by encounter rhythm
    - `route_planner.py`: Optimize travel based on time, geography, species
    - `content_writer.py`: Generate logs and social content

## Data Flow

User Input → MCP Server → Agent Chain → Output:
  - Birding Route Plan (Markdown / PDF)
  - Bird Encounter Rhythm Chart
  - Storytelling Log & Captions
