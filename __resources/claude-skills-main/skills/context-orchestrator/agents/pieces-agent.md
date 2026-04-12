---
name: pieces-agent
description: Retrieve local code context and Long-Term Memory (LTM) from Pieces
parent_skill: context-orchestrator
type: general-purpose
model: haiku
timeout: 8s
tools: [Bash, Read]
---

# Pieces Context Agent

## Purpose

Retrieve local code context, development history, and Long-Term Memory (LTM) from Pieces.

## CLI Reference

**Binary**: `/opt/homebrew/bin/pieces`

### Core Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `ask --ltm` | Query with LTM | `ask "question" --ltm` |
| `search --mode ncs` | Semantic search | `search --mode ncs "pattern"` |
| `search --mode fts` | Full-text search | `search --mode fts "text"` |
| `list` | List materials | `list` |
| `ask -f` | With file context | `ask "question" -f file.py` |

## Execution Protocol

### 1. Query Analysis

Parse the query to determine:
- **Type**: Question vs search vs history lookup
- **Mode**: LTM needed? File context? Semantic search?
- **Scope**: Specific files? General codebase?

### 2. Command Selection

```yaml
query_type_mapping:
  ltm_question:
    condition: "what was I working on", "my implementation", "previous solution"
    command: pieces ask "{query}" --ltm

  semantic_search:
    condition: Pattern or concept search
    command: pieces search --mode ncs "{pattern}"

  exact_search:
    condition: Exact text search
    command: pieces search --mode fts "{text}"

  file_context:
    condition: Specific file(s) mentioned
    command: pieces ask "{query}" -f {files}

  material_lookup:
    condition: Need saved snippets
    command: pieces list
```

### 3. LTM Usage Guidelines

**When to use --ltm**:
- Questions about past work patterns
- "How did I implement X before?"
- "What projects have I worked on?"
- Implementation guidance from history

**When to skip --ltm**:
- Simple snippet search
- Current file questions
- No historical context needed

### 4. Execute and Parse

```bash
# With LTM
pieces ask "How should I implement error handling?" --ltm

# Semantic code search
pieces search --mode ncs "async retry pattern"

# With file context
pieces ask "What does this function do?" -f src/utils/parser.py
```

### 5. Return Structured Result

```json
{
  "source": "pieces",
  "query": "original query",
  "mode": "ltm|ncs|fts|file_context",
  "results": [
    {
      "type": "material|ltm_response|search_result",
      "title": "Error Retry Pattern",
      "language": "typescript",
      "content": "async function withRetry...",
      "confidence": 0.87,
      "relevance": "high"
    }
  ],
  "ltm_context": {
    "enabled": true,
    "related_projects": ["project-a", "project-b"],
    "time_range": "Last 3 months"
  },
  "latency_ms": 2345
}
```

## Search Mode Selection

| Mode | Use Case | Example Query |
|------|----------|---------------|
| `ncs` | Conceptual/semantic | "error handling with retry logic" |
| `fts` | Exact text | "class AuthService" |
| `fuzzy` | Typo-tolerant | "authentcation" |

## Error Handling

```yaml
timeout:
  action: Return empty result
  message: "Pieces query timed out after 8s"

ltm_unavailable:
  action: Fallback to regular search
  message: "LTM not available, using standard search"

no_materials:
  action: Return empty result
  message: "No matching materials found"
```

## Best Practices

1. **Always use --ltm** for implementation questions
2. **Include relevant files** with `-f` for precision
3. **Neural search (ncs)** for conceptual queries
4. **Full-text (fts)** for exact code
5. **Combine with limitless** for full context
6. **Note LTM coverage** (typically 3+ months)

## Known Limitations

### Non-Interactive Terminal Issues

The Pieces CLI (v1.19.0) has issues in non-interactive terminals:
```
Warning: Input is not a terminal (fd=0).
UNKNOWN EXCEPTION
[Errno 22] Invalid argument
```

**Workaround Options**:

1. **Use Pieces MCP** (Recommended):
   - Check status: `pieces mcp status` (look for "LTM running")
   - If Claude Code MCP needs repair: `pieces mcp repair --ide claude_code`
   - MCP provides same LTM capabilities without terminal issues

2. **Use Interactive Terminal**:
   - Run commands in a proper terminal session
   - Works for manual testing and exploration

3. **Graceful Degradation**:
   - When pieces fails, context-orchestrator falls back to other sources
   - Research and limitless (when configured) remain available

### API Configuration

Pieces requires PiecesOS to be running. Check status via:
```bash
pieces mcp status  # Shows "LTM running" if operational
```
