---
name: manus-intent-router
description: Local ML-based intent classification (GGUF quantized model) and multi-model LLM routing (DeBERTa-v3 ONNX). Routes requests to optimal agents and LLMs by task type and complexity. Use when working on the Manus intent/routing system.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus Intent Router & LLM Routing

ML-powered request classification and routing in `~/manus-chatbot/`.

## Two Routing Systems

### 1. Intent Classification (`agents/intent_classifier_agent.py`)
- **Primary**: Local GGUF model (`models/manus-intent-router-q8_0.gguf`)
- **Fallback**: HuggingFace BART zero-shot classification
- **Accuracy**: 60.9% intent, 63.5% domain (measured)
- Extracts: intent, domain, entities, confidence, conversational signals

### 2. Multi-Model Router (`agents/multi_model_router.py`)
Routes agents to optimal LLMs by AgentType × TaskComplexity:

| AgentType | Simple | Medium | Complex | Premium |
|-----------|--------|--------|---------|---------|
| CODE | phi4 | qwen2.5-coder:14b | deepseek-r1:32b | claude-sonnet |
| REASONING | gemma3:27b | deepseek-r1:32b | qwen3:32b | claude-sonnet |
| RESEARCH | phi4-mini | gemma3:27b | qwen3:32b | claude-sonnet |
| DATA | phi4 | qwen2.5:14b | deepseek-r1:32b | claude-sonnet |
| QUICK | phi4-mini | phi4 | gemma3:27b | - |

### 3. DeBERTa LLM Router (`models/manus-llm-router-onnx/`)
- ONNX-optimized DeBERTa-v3-small for request → LLM classification
- Loaded lazily by `agents/model_manager.py`

## Key Files

- `agents/intent_classifier_agent.py` — Intent classification
- `agents/multi_model_router.py` — Agent→LLM routing
- `agents/model_manager.py` — Unified model interface
- `models/` — GGUF and ONNX model files
- `training_data/` — Training datasets
- `scripts/` — 40+ training/evaluation scripts

## Training

```bash
cd ~/manus-chatbot
python scripts/train_intent_router.py    # Train intent model
python scripts/evaluate_intent_router.py # Evaluate accuracy
python scripts/export_onnx.py            # Export to ONNX
```
