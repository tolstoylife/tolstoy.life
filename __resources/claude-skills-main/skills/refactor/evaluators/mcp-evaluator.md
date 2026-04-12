---
name: mcp-evaluator
description: |
  Evaluates MCP server connections, lootbox namespaces, availability, response times, and error rates.
  Checks all configured MCP servers and tools.
model: sonnet
---

# MCP Evaluator

## Scope

- Lootbox server: ws://localhost:9742/ws
- Lootbox namespaces: kv, sqlite, memory, graphql, neo4j, deepgraph, perplexity
- GitHub MCP: plugin:github:github
- Context7: plugin:compound-engineering:context7
- Playwright: plugin:compound-engineering:pw

## Checks

### 1. Availability
- Verify server connections (lootbox, MCP servers)
- Test namespace responsiveness
- Check for connection timeouts

### 2. Response Times
- Measure average latency per namespace
- Identify slow operations (>1s)
- Track connection establishment time

### 3. Error Rates
- Count failed operations per namespace
- Identify common error patterns
- Track retry behavior

### 4. Integration Health
- Verify tool invocation syntax
- Check for deprecated MCP methods
- Validate namespace availability matches configuration

## Output Format

```yaml
mcp_report:
  servers:
    - name: lootbox
      status: online|offline|degraded
      uptime_hours: N
      namespaces: N

  namespaces:
    - name: namespace_name
      status: available|unavailable
      avg_latency_ms: N
      error_rate: X%
      operations_tested: N

  performance:
    fastest: {namespace, latency_ms}
    slowest: {namespace, latency_ms}
    unreliable: [namespaces with >5% error rate]

  recommendations:
    - namespace: namespace_name
      issue: slow|unreliable|deprecated
      action: optimize|replace|remove
      impact: performance|reliability
```
