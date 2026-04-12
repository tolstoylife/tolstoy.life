---
name: godmode-ollama
description: Chat and generate with local Ollama models via GODMODE MCP. List available models, pull new ones, run inference with configurable temperature and system prompts. Tools — ollama_chat, ollama_generate, ollama_list, ollama_pull.
allowed-tools: Read, Bash
---

# Godmode Ollama Integration

Local LLM inference via GODMODE MCP (`http://127.0.0.1:7865/sse`).

## Tools

| Tool | Args | Description |
|------|------|-------------|
| `ollama_chat` | `model`, `messages[]`, `system?`, `temperature?`, `max_tokens?` | Chat with Ollama model |
| `ollama_generate` | `model`, `prompt`, `system?`, `temperature?`, `format?` (text/json) | Generate text/code |
| `ollama_list` | — | List available models |
| `ollama_pull` | `model` | Download a model (600s timeout) |

## Available Models (18 local)

nemotron-3-nano, llama4:scout, qwen3:32b, deepseek-r1:32b, gemma3:27b, gpt-oss:20b, phi4-reasoning:plus, phi4-reasoning, phi4, qwen2.5:14b, qwen2.5-coder:14b, deepseek-r1:8b, qwen2.5:7b, phi4-mini

## Example

```json
{"tool": "ollama_chat", "arguments": {"model": "qwen3:32b", "messages": [{"role": "user", "content": "Explain CQRS"}], "temperature": 0.7}}
```
