---
name: pieces
description: Extract local code context and development history from Pieces LTM. Searches snippets and work history. Usage: /pieces [query]
---

# /pieces Command

Local code context and Long-Term Memory extraction.

## Usage

```
/pieces [query]
```

## Behavior

1. **Parse Query**: Determine if LTM or search needed
2. **Select Mode**: LTM question vs semantic search
3. **Execute**: Run pieces CLI
4. **Return Context**: Code context with history

## Mode Selection

| Query Type | Command |
|------------|---------|
| Implementation question | `pieces ask "{query}" --ltm` |
| Semantic code search | `pieces search --mode ncs "{query}"` |
| Exact text search | `pieces search --mode fts "{query}"` |
| With file context | `pieces ask "{query}" -f {files}` |

## Execution

```bash
# Primary: LTM-enabled question
pieces ask "{query}" --ltm

# Fallback: semantic search
pieces search --mode ncs "{query}"
```

## Example

```
User: /pieces how did I implement error handling before

→ Runs: pieces ask "how did I implement error handling before" --ltm
→ Returns: Past implementations with context
→ Includes: Related projects and patterns
```
