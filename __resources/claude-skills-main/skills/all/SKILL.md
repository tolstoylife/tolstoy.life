---
name: all
description: Full-stack task execution pipeline — discovers tools via semantic search, routes to the right agent, then executes via GODMODE. Chains manus-tool-discovery → manus-orchestrator → godmode-system in sequence.
allowed-tools: Read, Bash, Grep, Glob
---

# /all — Full Pipeline Execution

Three-step sequential pipeline that discovers, routes, and executes any task.

## Pipeline

```
Step 1: /manus-tool-discovery  →  finds what tools/agents to use
Step 2: /manus-orchestrator    →  routes to the right agent
Step 3: /godmode-system        →  executes anything the agent can't
```

## Step 1: Discover (manus-tool-discovery)

Search 430+ tools across all sources using semantic similarity.

1. Analyze the user's request to extract intent and required capabilities
2. Query the tool discovery system for the best matches:
   ```bash
   # API search
   curl -s "http://localhost:8000/api/v1/tools?search=USER_INTENT" | python3 -m json.tool
   # Or list skills
   curl -s http://localhost:8000/api/v1/skills
   ```
3. Sources searched: GODMODE MCP (106 tools, port 7865), ML-Toolkit (14 tools, port 7866), Intelligence (14 tools, port 7867), native agents (~20), Skills API Hub (177+), Claude Code skills (1,300+)
4. Rank results by relevance — pick the top tool(s) and agent(s)

**Output of Step 1:** A ranked list of tools/agents that can handle the request.

## Step 2: Route (manus-orchestrator)

Route the task to the right specialized agent from 20+ available.

1. Using the discovery results from Step 1, determine the best agent:
   - CODE tasks → CodeAgent, DevOpsAgent, AzureAgentImpl, IntelliJAgent
   - DATA tasks → DataScientistAgent, DatabaseAgent
   - RESEARCH tasks → ResearchAgentImpl, BrowserAgentImpl
   - REASONING tasks → CivicAIPolicyAgent, GovernanceAgentImpl, HealthcareAgent
   - GENERAL tasks → JobSearchAgent, CareerAdvisorAgent, CitizenServiceAgent, SkillsAPIAgent
   - COORDINATION → OrchestratorAgentImpl (multi-agent)
2. Select the appropriate orchestration tier:
   - **Tier 1** (AgentOrchestrator) — Simple keyword match
   - **Tier 2** (SmartOrchestrator) — LLM-per-agent with fallback
   - **Tier 3** (SmartOrchestratorV2) — Semantic routing
   - **Tier 4** (NuancedOrchestrator) — Quality tiers (Quick/Standard/Premium)
   - **Tier 5** (SimpleOrchestrator) — Workflow DAG chaining
3. Dispatch via API:
   ```bash
   curl -X POST http://localhost:8000/api/v1/chat/message \
     -H "Content-Type: application/json" \
     -d '{"message": "THE_TASK", "user_id": "user1"}'
   ```

**Output of Step 2:** The agent's response, or identification of what still needs direct execution.

## Step 3: Execute (godmode-system)

For anything the agent can't handle directly, use GODMODE MCP (port 7865).

1. If the agent response is complete → deliver to user, done
2. If execution is needed (shell commands, process management, system ops, batch jobs):
   ```bash
   # Single command
   curl -X POST http://127.0.0.1:7865/sse -d '{"tool": "shell_exec", "arguments": {"command": "COMMAND_HERE"}}'

   # Batch execution
   curl -X POST http://127.0.0.1:7865/sse -d '{"tool": "batch_exec", "arguments": {"commands": ["cmd1", "cmd2"], "stop_on_error": true}}'

   # System info
   curl -X POST http://127.0.0.1:7865/sse -d '{"tool": "system_info", "arguments": {}}'

   # Process management
   curl -X POST http://127.0.0.1:7865/sse -d '{"tool": "process_list", "arguments": {"sort_by": "cpu"}}'
   ```
3. GODMODE tools: `shell_exec`, `process_list`, `process_kill`, `system_info`, `batch_exec`

**Output of Step 3:** Final execution results delivered to user.

## Decision Flow

```
User Request
    │
    ▼
[DISCOVER] What tools exist for this?
    │
    ├─ Found agent match → [ROUTE] to agent → agent handles it → done
    │                                │
    │                                └─ agent needs execution help → [EXECUTE] via GODMODE
    │
    └─ No agent match, but GODMODE can do it → [EXECUTE] directly
```

## Key Principle

**Never skip steps.** Always discover first (you might find a better tool than you assumed), then route (the orchestrator knows agent capabilities), then execute (GODMODE is the fallback for anything requiring direct system access).

## Key Files

- `~/manus-chatbot/agents/tool_discovery.py` — Semantic tool search
- `~/manus-chatbot/agents/orchestrator.py` — Tier 1 routing
- `~/manus-chatbot/agents/smart_orchestrator_v2.py` — Tier 3 semantic routing
- `~/manus-chatbot/api_server.py` — FastAPI server (16+ endpoints)
- `~/mcp-godmode/godmode_sse.py` — GODMODE MCP server (106 tools)
