---
name: limitless
description: Extract personal life context from Limitless pendant recordings. Searches lifelogs and chats. Usage: /limitless [query]
---

# /limitless Command

Personal life context extraction from Limitless pendant.

## Usage

```
/limitless [query]
```

## Behavior

1. **Parse Query**: Extract topic, people, time references
2. **Select Command**: Choose appropriate limitless subcommand
3. **Execute**: Run limitless CLI
4. **Return Context**: Personal life context

## Command Selection

| Query Type | Command |
|------------|---------|
| Topic search | `lifelogs search "{query}" --limit 10 --format json` |
| Date-specific | `workflow daily {date} --format json` |
| Recent activity | `workflow recent --hours 24 --format json` |
| Cross-source | `workflow search "{query}" --format json` |

## Execution

```bash
# Primary: semantic search
limitless lifelogs search "{query}" --limit 10 --format json

# Fallback: workflow search
limitless workflow search "{query}" --format json
```

## Example

```
User: /limitless what did John say about the deadline

→ Searches lifelogs for "John deadline"
→ Returns relevant transcript excerpts
→ Includes speaker attribution and timestamps
```
