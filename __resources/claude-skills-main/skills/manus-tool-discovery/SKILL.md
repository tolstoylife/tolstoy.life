---
name: manus-tool-discovery
description: Semantic search over 430+ tools using OpenAI embeddings. Discovers tools across native agents, Skills API Hub, GODMODE MCP, ML-Toolkit, and Intelligence servers. Embedding-based similarity matching.
allowed-tools: Read, Bash, Grep, Glob
---

# Manus Semantic Tool Discovery

Find the right tool from 430+ available tools in `~/manus-chatbot/agents/tool_discovery.py`.

## Architecture

- **Embedding model**: OpenAI text-embedding-ada-002
- **Index**: `~/manus-chatbot/tools/embeddings.json` (pre-computed)
- **Sources**: Native agents, Skills API, GODMODE (106 tools), ML-Toolkit (14), Intelligence (14)

## Tool Sources

| Source | Count | Access |
|--------|-------|--------|
| GODMODE MCP | 106 | SSE port 7865 |
| ML-Toolkit MCP | 14 | Streamable HTTP port 7866 |
| Intelligence MCP | 14 | SSE port 7867 |
| Native agents | ~20 | Direct Python |
| Skills API Hub | 177+ | HTTP |
| Claude Code skills | 1,300+ | Filesystem scan |

## Usage

```python
from agents.tool_discovery import ToolDiscovery
discovery = ToolDiscovery()
results = discovery.search("send a slack notification", top_k=5)
# Returns ranked tools with similarity scores
```

## API

```bash
# List all tools (filterable)
curl "http://localhost:8000/api/v1/tools?search=database&source=godmode"

# List skills
curl http://localhost:8000/api/v1/skills

# Force rescan
curl http://localhost:8000/api/v1/skills/scan
```

## MCP Connector (`tools/mcp_connector.py`)

Auto-discovers tools from 3 persistent MCP servers on startup:
- `godmode` → `http://127.0.0.1:7865/sse`
- `ml-toolkit` → `http://127.0.0.1:7866/mcp`
- `intelligence` → `http://127.0.0.1:7867/sse`
