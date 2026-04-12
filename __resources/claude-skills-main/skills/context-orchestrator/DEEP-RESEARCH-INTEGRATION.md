# Deep-Research Phase 0 Integration

## Overview

When deep-research is invoked, optionally gather personal and local context first.

## Phase 0: Context Pre-Enrichment

### Trigger Conditions

Add Phase 0 when:
- Topic likely has personal context (discussed before)
- Topic involves code that exists in local history
- User explicitly requests comprehensive research

Skip Phase 0 when:
- Quick fact lookup (Type A research)
- Pure technical documentation query
- User requests "fast" or "skip context"

### Implementation

Before Phase 1 (Scoping), insert:

```yaml
phase_0:
  name: Context Gathering
  purpose: Enrich research with personal and local knowledge
  duration: 30-60 seconds

  steps:
    1_personal_search:
      condition: Topic may have conversation history
      action: limitless lifelogs search "{topic}" --limit 3 --format json
      extract: Key points, decisions, people involved

    2_local_search:
      condition: Topic may have code history
      action: pieces ask "context for {topic}" --ltm
      extract: Previous implementations, patterns used

    3_compile_briefing:
      format: |
        ## Existing Context

        ### Personal Background
        {personal_findings or "No relevant conversations found"}

        ### Local Code Context
        {local_findings or "No existing implementations found"}

  output:
    inject_into: Phase 1 scoping as background context
```

### Modified Scoping (Phase 1)

With Phase 0 context available:

```yaml
phase_1_with_context:
  inputs:
    - User question (original)
    - Phase 0 briefing (if available)

  scoping_questions:
    - Standard scoping questions
    - "Does the Phase 0 context inform the research scope?"
    - "Are there specific findings to verify or expand?"
```

### Example Flow

```
User: "Deep research on authentication approaches for our API"

Phase 0:
├── limitless search "authentication API" → Found:
│   - "Discussed with John on Jan 3: decided JWT over sessions"
│   - "Security review on Dec 15: noted rate limiting concerns"
│
├── pieces ask "auth implementation context" --ltm → Found:
│   - Previous auth in auth/middleware.ts using httpOnly cookies
│   - Rate limiter in middleware/ratelimit.ts
│
└── Context Briefing compiled

Phase 1 (Scoping):
├── Core question: Best auth approach for our API
├── Context: We previously chose JWT, have cookie implementation
├── Scope: Compare with context, focus on gaps
└── ...continues normal deep-research flow
```

## Integration Points

### How to Enable

Option 1: Automatic (when context-orchestrator hook detects relevance)
Option 2: Explicit flag: `deep research with context: {topic}`
Option 3: Conversation history indicates prior discussion

### Data Flow

```
context-orchestrator Phase 0
         │
         ▼
   Context Briefing
         │
         ▼
 deep-research Phase 1
         │
         ▼
   ...normal phases...
```

### Cache Consideration

Phase 0 results are cached:
- limitless: 30 min TTL
- pieces: 15 min TTL

Subsequent deep-research on same topic reuses cached context.
