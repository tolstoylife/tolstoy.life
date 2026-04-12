---
name: context
description: Multi-source context extraction. Invokes all three CLI tools (limitless, research, pieces) in parallel to gather comprehensive context. Usage: /context [query]
---

# /context Command

Multi-source context extraction from all available CLIs.

## Usage

```
/context [query]
```

## Behavior

1. **Parallel Extraction**: Spawns subagents for all three CLIs
2. **Merge Results**: Collects and deduplicates results
3. **Return Context**: Unified context from all sources

## Execution

When this command is invoked:

```yaml
mode: parallel

actions:
  limitless:
    command: limitless workflow search "{query}" --format json
    timeout: 10s

  research:
    command: research docs -t "{query}" --format json
    timeout: 15s

  pieces:
    command: pieces ask "{query}" --ltm
    timeout: 8s

aggregation:
  - Collect all results
  - Deduplicate by content similarity
  - Rank by relevance/confidence
  - Return unified context
```

## Example

```
User: /context authentication best practices

→ Limitless: Recent conversations about auth
→ Research: Documentation on auth patterns
→ Pieces: Previous auth implementations
→ Merged: Comprehensive auth context
```
