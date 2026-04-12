# Pipeline DSL Reference

## YAML Structure

```yaml
apiVersion: limitless.cli/v1
kind: Pipeline
metadata:
  name: string
  version: string
  description: string
spec:
  variables: []        # Runtime overrides
  agents: {}           # Agent definitions
  nodes: {}            # Execution nodes
  edges: []            # Data flow
  config:
    checkpointStrategy: always | on_error | never
    maxParallelism: number
    timeout: string    # e.g., "5m", "1h"
```

## Node Types

### Agent Node
Executes a Claude agent with specified model and prompt.

```yaml
nodes:
  extract_entities:
    type: agent
    agent: entity-extractor
    model: sonnet
    inputs:
      - lifelog_content
    outputs:
      - entities
    config:
      maxTokens: 4096
      temperature: 0.7
```

### Transform Node
Transforms data using JavaScript expressions or jq.

```yaml
nodes:
  filter_topics:
    type: transform
    transform: |
      data.filter(t => t.confidence > 0.5)
    inputs:
      - raw_topics
    outputs:
      - filtered_topics
```

### Conditional Node
Branches based on condition.

```yaml
nodes:
  check_content:
    type: conditional
    condition: "input.length > 1000"
    then: summarize
    else: pass_through
    inputs:
      - content
```

### Parallel Node
Fan-out over array.

```yaml
nodes:
  process_each:
    type: parallel
    over: lifelogs
    node: process_single
    maxConcurrency: 5
    inputs:
      - lifelogs
    outputs:
      - processed_items
```

### Merge Node
Fan-in results.

```yaml
nodes:
  combine_results:
    type: merge
    strategy: concat | reduce | first
    inputs:
      - item_1
      - item_2
      - item_3
    outputs:
      - combined
```

## Edge Definitions

```yaml
edges:
  - from: fetch_lifelogs
    to: extract_entities
    mapping:
      lifelogs: lifelog_content

  - from: extract_entities
    to: filter_topics
    mapping:
      entities.topics: raw_topics
```

## Variables

Runtime variables can be passed via CLI.

```yaml
spec:
  variables:
    - name: date
      type: string
      default: "today"
      description: "Date to process"

    - name: limit
      type: number
      default: 10
      description: "Maximum items to process"
```

**Usage:**
```bash
pipeline run daily-digest --var date=2026-01-04 --var limit=20
```

## Agent Definitions

```yaml
spec:
  agents:
    entity-extractor:
      model: sonnet
      systemPrompt: |
        Extract entities from the provided text.
        Return structured JSON.
      tools:
        - search-lifelogs
        - graph-query

    summarizer:
      model: opus
      systemPrompt: |
        Create a comprehensive summary.
      maxTokens: 8192
```

## Checkpointing

```yaml
spec:
  config:
    checkpointStrategy: on_error  # Save state on failures
    checkpointStorage: falkordb   # Where to store checkpoints
```

**Resume from checkpoint:**
```bash
pipeline resume <execution-id>
```

## Built-in Templates

### daily-digest.yaml
```yaml
# Summarizes a day's lifelogs
nodes:
  - fetch: Get lifelogs for date
  - extract: Extract entities and topics
  - summarize: Generate daily summary
  - store: Save to graph database
```

### hierarchical-extraction.yaml
```yaml
# Full entity extraction with session detection
nodes:
  - fetch: Get lifelogs
  - detect_sessions: Group into sessions
  - extract_per_session: Parallel extraction
  - aggregate: Combine results
  - sync: Store in graph
```

### research.yaml
```yaml
# Combine lifelogs with web research
nodes:
  - fetch_lifelogs: Get relevant lifelogs
  - extract_topics: Identify research topics
  - web_search: Search for each topic
  - synthesize: Combine sources
  - report: Generate research report
```

## Execution

### Run Pipeline
```bash
# From template
bun run src/index.ts pipeline run daily-digest

# From file
bun run src/index.ts pipeline run ./custom-pipeline.yaml

# With variables
bun run src/index.ts pipeline run daily-digest --var date=2026-01-04
```

### Check Status
```bash
bun run src/index.ts pipeline status <execution-id>
```

### Resume Failed
```bash
bun run src/index.ts pipeline resume <execution-id>
```

## Error Handling

```yaml
spec:
  config:
    errorHandling:
      maxRetries: 3
      retryDelay: "1s"
      onFailure: checkpoint | abort | continue
```

## Performance

| Config | Recommended |
|--------|-------------|
| maxParallelism | 5 (default) |
| timeout | 5m per node |
| checkpointStrategy | on_error |

For large datasets, increase parallelism:
```yaml
config:
  maxParallelism: 10
```
