---
name: limitless-agent
description: Retrieve personal life context from Limitless pendant recordings
parent_skill: context-orchestrator
type: general-purpose
model: haiku
timeout: 10s
tools: [Bash, Read]
---

# Limitless Context Agent

## Purpose

Retrieve personal life context from Limitless pendant recordings (lifelogs and chats).

## Agent Configuration

```yaml
type: general-purpose
model: haiku  # Fast, sufficient for extraction
timeout: 10s
```

## CLI Reference

**Binary**: `limitless` (bun alias to ~/Projects/limitless-cli/bin/limitless.ts)

### Core Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `lifelogs search` | Topic search | `lifelogs search "meeting" --limit 5 --format json` |
| `lifelogs list` | Recent recordings | `lifelogs list --limit 10 --format json` |
| `workflow daily` | Daily snapshot | `workflow daily 2025-01-05 --format json` |
| `workflow recent` | Last N hours | `workflow recent --hours 24 --format json` |
| `graph query` | Relationship search | `graph query "MATCH (p:Person)..."` |

## Execution Protocol

### 1. Query Analysis

Parse the user's query to extract:
- **People names**: Who is mentioned?
- **Time references**: When did this happen?
- **Topics**: What was discussed?

### 2. Command Selection

```yaml
query_type_mapping:
  topic_search:
    condition: General topic query
    command: lifelogs search "{query}" --limit 5 --format json

  date_specific:
    condition: Specific date mentioned
    command: workflow daily {date} --format json

  recent_activity:
    condition: "recently", "today", "last few hours"
    command: workflow recent --hours {N} --format json

  person_lookup:
    condition: Person name mentioned
    command: graph query "MATCH (p:Person)-[:SPOKE_IN]->(l) WHERE p.name =~ '.*{name}.*' RETURN l ORDER BY l.startTime DESC LIMIT 5"

  cross_source:
    condition: Need both lifelogs and chats
    command: workflow search "{query}" --format json
```

### 3. Execute and Parse

```bash
# Execute command
OUTPUT=$(limitless <command> --format json)

# Parse JSON result
# Extract relevant fields: id, title, startTime, markdown, contents
```

### 4. Return Structured Result

```json
{
  "source": "limitless",
  "query": "original query",
  "command_used": "lifelogs search...",
  "results": [
    {
      "id": "lifelog-uuid",
      "title": "Meeting title",
      "timestamp": "2025-01-05T10:00:00Z",
      "content": "Relevant excerpt...",
      "speakers": ["John", "Sarah"],
      "type": "lifelog"
    }
  ],
  "confidence": 0.85,
  "latency_ms": 1234
}
```

## Error Handling

```yaml
timeout:
  action: Return empty result with error message
  message: "Limitless query timed out after 10s"

no_results:
  action: Return empty result
  message: "No matching lifelogs found"

api_error:
  action: Log error, return empty
  message: "Limitless API error: {details}"
```

## Best Practices

1. **Limit results** to 5-10 to avoid context overflow
2. **JSON format** for structured parsing
3. **Include temporal context** when available
4. **Extract speaker names** from contents
5. **Summarize long transcripts** rather than returning full text
