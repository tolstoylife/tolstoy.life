---
name: manus-crew
description: CrewAI-like multi-agent workflows — sequential, hierarchical, and parallel execution modes. Agent roles/personas, human-in-the-loop checkpoints, Autogen SelectorGroupChat swarms, and inter-agent message bus.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus Crew Workflows

CrewAI-like agent orchestration in `~/manus-chatbot/agents/`.

## Execution Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| Sequential | Agents run one after another | Pipeline processing |
| Hierarchical | Manager delegates to workers | Complex projects |
| Parallel | Agents run simultaneously | Independent tasks |

## Key Modules

| Module | Purpose |
|--------|---------|
| `crew_features.py` | Roles, personas, execution modes, human-in-the-loop |
| `smart_swarm.py` | Autogen SelectorGroupChat with multi-model routing |
| `swarm_team.py` | Collaborative agent swarm with dynamic task routing |
| `multi_agent_coordinator.py` | Inter-agent messaging, handoffs, intent-first routing |
| `agent_message_bus.py` | Priority-based pub/sub for agent-to-agent communication |

## Human-in-the-Loop

```python
from agents.crew_features import CrewWorkflow
workflow = CrewWorkflow(
    agents=[researcher, writer, reviewer],
    mode="sequential",
    human_checkpoints=["after_research", "before_publish"]
)
```

## Message Bus

```python
from agents.agent_message_bus import AgentMessageBus
bus = AgentMessageBus()
bus.publish("research_complete", data=results, priority=1)
bus.subscribe("research_complete", handler=writer_agent.process)
```
