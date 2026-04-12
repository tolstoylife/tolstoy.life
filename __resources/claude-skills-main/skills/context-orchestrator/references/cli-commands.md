# Context Orchestrator CLI Quick Reference

## Limitless CLI

> **Note**: Requires API key configuration: `limitless config set api.key YOUR_KEY`

### Lifelogs
```bash
# Search lifelogs
limitless lifelogs search "query" --limit 10 --json

# List recent
limitless lifelogs list --limit 10 --json

# Get specific
limitless lifelogs get <id> --json

# Filter by date
limitless lifelogs list --date 2025-01-05 --json
```

### Workflows
```bash
# Cross-source search (lifelogs + chats)
limitless workflow search "query"

# Daily snapshot (requires date argument)
limitless workflow daily 2025-01-05

# Export (if available)
limitless workflow export --start 2025-01-01 --end 2025-01-05
```

### Knowledge Graph
```bash
# Cypher query
limitless graph query "MATCH (p:Person)-[:SPOKE_IN]->(l) RETURN p, l LIMIT 10"

# Stats
limitless graph stats

# Sync
limitless graph sync
```

---

## Research CLI

### Documentation
```bash
# General docs
research docs -t "query" --format json

# With framework
research docs -t "query" -k "bun" --format json
```

### Verification
```bash
# Fact check
research fact-check -t "claim" --format json

# With graph
research fact-check -t "claim" --graph
```

### SDK/API
```bash
research sdk-api -t "api question" --format json
```

### Academic
```bash
research academic -t "topic" --format json
```

### Medical/PEX
```bash
research pex-grounding -t "medical query" --format json
```

---

## Pieces CLI

### Ask (with LTM)
```bash
# LTM question
pieces ask "query" --ltm

# With file context
pieces ask "query" -f file1.py file2.py

# With materials
pieces ask "query" -m 1 2 3
```

### Search
```bash
# Neural code search
pieces search --mode ncs "pattern"

# Full-text search
pieces search --mode fts "exact text"

# Fuzzy search
pieces search "approximate"
```

### Materials
```bash
# List
pieces list

# Save
pieces save

# Create
pieces create
```

---

## Common Patterns

### Daily Context
```bash
# Today's limitless snapshot
limitless workflow daily $(date +%Y-%m-%d) --format json

# Recent pieces activity
pieces ask "what was I working on today" --ltm
```

### Topic Research
```bash
# Personal context
limitless lifelogs search "auth implementation" --limit 5 --format json

# Online docs
research docs -t "authentication best practices" --format json

# Local patterns
pieces ask "how did I implement auth" --ltm
```

### Verification
```bash
# Fact check
research fact-check -t "claim to verify" --format json
```
