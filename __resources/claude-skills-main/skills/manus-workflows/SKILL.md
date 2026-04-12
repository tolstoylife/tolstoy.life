---
name: manus-workflows
description: YAML-based multi-agent workflow orchestration with dependency DAGs, scheduling, and real-time monitoring. Define multi-step agent pipelines with conditional routing and error handling.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus Workflow Orchestration

Multi-agent workflows in `~/manus-chatbot/workflows/`.

## Modules

| Module | Purpose |
|--------|---------|
| `orchestrator.py` | Scheduled multi-agent workflow execution from YAML config |
| `manage.py` | CLI for workflow CRUD and control |
| `monitor.py` | Real-time workflow monitoring and analytics |

## Workflow Definition (YAML)

```yaml
name: daily_research
schedule: "0 9 * * *"
steps:
  - agent: research
    task: "Find latest AI policy updates"
    output: research_results
  - agent: data_scientist
    task: "Analyze trends from {{research_results}}"
    depends_on: [research]
  - agent: business_comms
    task: "Draft summary email from {{analysis}}"
    depends_on: [data_scientist]
```

## CLI

```bash
cd ~/manus-chatbot
python -m workflows.manage list              # List workflows
python -m workflows.manage create config.yaml # Create workflow
python -m workflows.manage run <name>         # Execute workflow
python -m workflows.manage status <name>      # Check status
```

## API

```bash
curl http://localhost:8000/api/v1/workflows  # List workflows
```
