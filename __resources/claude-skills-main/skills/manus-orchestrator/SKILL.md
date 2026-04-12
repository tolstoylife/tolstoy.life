---
name: manus-orchestrator
description: Route tasks to 20+ specialized manus-chatbot agents. Covers 5 orchestration tiers (keyword, LLM-routed, semantic, nuanced quality-tier, workflow DAG). Use when dispatching complex tasks to the right agent in the Manus platform.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus Agent Orchestrator

Route tasks to the right specialized agent in the manus-chatbot platform (`~/manus-chatbot/`).

## Available Agents (20+)

| Agent | Type | Capability |
|-------|------|------------|
| CodeAgent | CODE | Code generation, analysis, refactoring |
| DataScientistAgent | DATA | Pandas, sklearn, visualization, forecasting |
| DatabaseAgent | DATA | SQL execution across SQLite/Postgres/MySQL |
| ResearchAgentImpl | RESEARCH | Web search and knowledge synthesis |
| BrowserAgentImpl | BROWSER | Playwright/Selenium automation |
| DevOpsAgent | CODE | GitHub, Docker, CI/CD integration |
| AzureAgentImpl | CODE | Azure SDK cloud operations |
| CivicAIPolicyAgent | REASONING | Government AI policy, NIST RMF |
| GovernanceAgentImpl | REASONING | Compliance, safety enforcement |
| HealthcareAgent | REASONING | Medical info with disclaimers |
| JobSearchAgent | GENERAL | Multi-board job search |
| CareerAdvisorAgent | GENERAL | Career path planning, skill gaps |
| InterviewCoachAgent | GENERAL | Mock interviews, STAR method |
| ResumeWriterAgent | GENERAL | AI resume creation, ATS optimization |
| CitizenServiceAgent | GENERAL | Government public-facing chatbot |
| SkillsAPIAgent | GENERAL | Access 177+ skills via Skills API Hub |
| BusinessCommsAgent | GENERAL | Professional correspondence via Claude |
| OrchestratorAgentImpl | COORDINATION | Multi-agent task routing |
| IntelliJAgent | CODE | IDE integration, file ops |
| AntigravityAgent | CODE | VS Code IDE integration |

## 5 Orchestration Tiers

1. **AgentOrchestrator** (`agents/orchestrator.py`) — Keyword-based intent detection
2. **SmartOrchestrator** (`agents/smart_orchestrator.py`) — LLM-per-agent-type with fallback chains
3. **SmartOrchestratorV2** (`agents/smart_orchestrator_v2.py`) — Semantic tool discovery routing
4. **NuancedOrchestrator** (`agents/nuanced_orchestrator.py`) — Quality tiers (Quick/Standard/Premium), 13 LLM providers
5. **SimpleOrchestrator** (`agents/simple_orchestrator.py`) — Workflow step chaining with dependency DAG

## How to Use

```bash
# API endpoint for chat routing
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "analyze this CSV data", "user_id": "user1"}'

# List agents
curl http://localhost:8000/api/v1/agents

# System status
curl http://localhost:8000/api/v1/system/status
```

## Key Files

- `~/manus-chatbot/api_server.py` — FastAPI server (16+ endpoints)
- `~/manus-chatbot/agents/registry.py` — Agent CRUD registry
- `~/manus-chatbot/agents/multi_model_router.py` — Routes by AgentType + TaskComplexity
