---
name: manus-prompt-pipeline
description: Prompt lifecycle management — register, test (golden/realistic/adversarial), score (9-dimension rubric), version, and promote prompts to production. CLI and Streamlit dashboard included.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus Prompt Pipeline

Prompt engineering lifecycle in `~/manus-chatbot/governance/`.

## Pipeline Stages

```
Register → Test → Score → Review → Promote → Monitor
```

## Testing Methodology (3 tiers)

1. **Golden Path** — Known-good input/output pairs
2. **Realistic** — Production-like scenarios
3. **Edge/Adversarial** — Jailbreak attempts, edge cases, malformed input

## Scoring (9 dimensions, threshold 8.0)

See `/manus-governance` skill for full rubric.

## CLI Commands

```bash
cd ~/manus-chatbot
python -m governance.prompt_cli register <name> <template>
python -m governance.prompt_cli test <name>     # Run 3-tier tests
python -m governance.prompt_cli score <name>    # Score against rubric
python -m governance.prompt_cli promote <name>  # Move to production
python -m governance.prompt_cli rollback <name> # Revert version
python -m governance.prompt_cli list            # Show all prompts
python -m governance.prompt_cli show <name>     # Prompt details + history
```

## Model Registry (`governance/model_registry.py`)

Version control for models and prompts:
- Immutable version history
- Rollback to any previous version
- Metadata tracking (author, date, score, test results)

## Dashboard

```bash
cd ~/manus-chatbot
streamlit run governance/prompt_dashboard.py
```
