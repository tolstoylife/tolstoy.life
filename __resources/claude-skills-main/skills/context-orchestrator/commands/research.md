---
name: research
description: Extract online documentation and research context. Searches docs, verifies facts, finds academic papers. Usage: /research [query]
---

# /research Command

Online documentation and research context extraction.

## Usage

```
/research [query]
```

## Behavior

1. **Classify Query**: Determine research mode (docs, fact-check, academic, sdk, pex)
2. **Detect Framework**: Identify technology context if applicable
3. **Execute**: Run research CLI
4. **Return Context**: Documentation with citations

## Mode Selection

| Query Pattern | Mode | Command |
|---------------|------|---------|
| "how to", "documentation" | docs | `research docs -t "{query}" -k "{framework}"` |
| "verify", "is it true" | fact-check | `research fact-check -t "{query}"` |
| "api", "sdk" | sdk-api | `research sdk-api -t "{query}"` |
| "paper", "research" | academic | `research academic -t "{query}"` |
| "medical", "pex" | pex-grounding | `research pex-grounding -t "{query}"` |

## Execution

```bash
# Primary: documentation search
research docs -t "{query}" --format json

# With framework detection
research docs -t "{query}" -k "{detected_framework}" --format json
```

## Example

```
User: /research how to implement WebSocket in Bun

→ Detects framework: bun
→ Runs: research docs -t "WebSocket implementation" -k "bun" --format json
→ Returns documentation with code examples
```
