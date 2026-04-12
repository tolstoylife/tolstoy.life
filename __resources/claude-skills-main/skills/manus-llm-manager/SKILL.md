---
name: manus-llm-manager
description: Unified multi-provider LLM configuration — auto-discovers and configures OpenAI, Anthropic, Ollama (18 local models), Gemini, Azure, and Moonshot. Cost tracking, fallback chains, and model capability mapping.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus LLM Manager

Unified LLM configuration in `~/manus-chatbot/llm_config.py`.

## Supported Providers

| Provider | Config Source | Models |
|----------|-------------|--------|
| Ollama | Auto-discovery (localhost:11434) | 18 local models (see memory) |
| OpenAI | OPENAI_API_KEY | gpt-4o, gpt-4-turbo, etc. |
| Anthropic | ANTHROPIC_API_KEY | claude-sonnet-4-5, claude-haiku |
| Google Gemini | GOOGLE_API_KEY | gemini-2.0-flash, etc. |
| Azure OpenAI | AZURE_OPENAI_* | Deployment-based |
| Moonshot | MOONSHOT_API_KEY | moonshot-v1 |

## Multi-Model Routing

The `MultiModelRouter` in `agents/multi_model_router.py` maps:
- **AgentType** (CODE, REASONING, RESEARCH, DATA, QUICK, BROWSER, COORDINATION, GENERAL)
- **TaskComplexity** (SIMPLE, MEDIUM, COMPLEX, PREMIUM)

To the optimal local or cloud model with fallback chains.

## Cost Tracking

Each model has token cost metadata. The router tracks cumulative spend per session.

## Usage

```python
from llm_config import LLMManager
manager = LLMManager()
models = manager.get_available_models()  # Auto-discovers all providers
config = manager.get_config_for("code", complexity="complex")
```

## API

```bash
curl http://localhost:8000/api/v1/models  # List all available models
```
