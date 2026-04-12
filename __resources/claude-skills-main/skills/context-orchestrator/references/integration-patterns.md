# Integration Patterns

## Deep-Research Integration (Phase 0)

### When to Augment

```yaml
triggers:
  - User has personal context relevant to research topic
  - Previous implementations exist in pieces LTM
  - Topic was discussed in recent lifelogs

skip_when:
  - Pure technical lookup (no personal/local context)
  - Quick fact-check (speed priority)
  - Explicit "skip context" flag
```

### Phase 0 Pre-Enrichment Flow

```
Deep Research Invoked
    │
    ├── [NEW] Phase 0: Context Gathering
    │   ├── Check if topic has personal context
    │   │   └── limitless search "{topic}" --limit 3
    │   ├── Check if topic has local context
    │   │   └── pieces ask "context for {topic}" --ltm
    │   └── Compile context briefing
    │
    ├── Phase 1: Scoping (with context)
    │   └── Include Phase 0 findings in scope
    │
    └── Continue standard deep-research...
```

### Context Briefing Format

```yaml
context_briefing:
  personal:
    summary: "3 relevant conversations found"
    key_points:
      - "Discussed with John on 2025-01-03"
      - "Decided to use JWT over sessions"
    sources: [lifelog-123, lifelog-456]

  local:
    summary: "Previous implementation found"
    key_points:
      - "Used httpOnly cookies"
      - "Implemented in auth/middleware.ts"
    sources: [material-789]
```

## Parallel Extraction Pattern

### Spawning Subagents

```yaml
parallel_extraction:
  strategy: fan-out → fan-in

  fan_out:
    - Task(limitless-agent, query=$QUERY, timeout=10s)
    - Task(research-agent, query=$QUERY, timeout=15s)
    - Task(pieces-agent, query=$QUERY, timeout=8s)

  fan_in:
    wait: all_settled  # Don't fail if one source fails
    merge: deduplicate_and_rank
```

### Result Merging

```yaml
merge_strategy:
  deduplication:
    method: content_similarity
    threshold: 0.85  # 85% similar = duplicate

  ranking:
    factors:
      - confidence_score (weight: 0.4)
      - recency (weight: 0.3)
      - source_authority (weight: 0.3)

  output:
    max_results: 10
    format: unified_context
```

## Error Handling Patterns

### Graceful Degradation

```yaml
on_cli_failure:
  limitless:
    log: "Limitless unavailable: {error}"
    action: Continue with other sources
    note_to_user: "Personal context unavailable"

  research:
    log: "Research unavailable: {error}"
    action: Continue with other sources
    note_to_user: "Online documentation unavailable"

  pieces:
    log: "Pieces unavailable: {error}"
    action: Continue with other sources
    note_to_user: "Local code context unavailable"
```

### Timeout Handling

```yaml
timeouts:
  limitless: 10s
  research: 15s
  pieces: 8s

on_timeout:
  action: Return partial results
  include_error: true
  message: "Source timed out, showing partial context"
```

### Empty Results

```yaml
on_empty_results:
  single_source:
    action: Report no matches
    suggestion: "Try different keywords or broader query"

  parallel_all_empty:
    action: Report no context found
    suggestion: "This topic may not have existing context"
```

## Caching Integration

### Pre-Check Cache

```python
# Before CLI invocation
cache_key = f"{source}:{hash(query)}"
cached = cache_manager.get(source, query)
if cached and not expired(cached):
    return cached  # Skip CLI call
```

### Post-Store Cache

```python
# After successful extraction
result = execute_cli(source, query)
if result.success:
    cache_manager.set(source, query, result)
```

### Cache Invalidation

```yaml
invalidation_triggers:
  - New session starts
  - Explicit "/context refresh" command
  - TTL expiration (30/60/15 min by source)
  - Manual cache clear
```

## Skill Routing Integration

### From Meta-Router

```yaml
routing_chain:
  meta-router:
    detects: [context, lifelog, research, ltm]
    routes_to: context-router

  context-router:
    classifies: Query domain
    selects: CLI(s) to invoke
    spawns: Subagent(s)
```

### Skill Invocation

```yaml
# Direct skill invocation
Skill(context-orchestrator, args="/context auth best practices")

# Or via slash command
/context auth best practices
```

## Observability Hooks

### Logging Pattern

```yaml
log_events:
  - context_request_received
  - source_selected (source, confidence)
  - cli_invoked (source, command)
  - cli_completed (source, latency, result_count)
  - cache_hit / cache_miss
  - aggregation_completed
  - context_returned
```

### Metrics (Future)

```yaml
metrics:
  - request_count_by_source
  - latency_percentiles
  - cache_hit_rate
  - error_rate_by_source
```
