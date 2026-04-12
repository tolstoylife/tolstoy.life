---
name: "tools"
description: "External tool integration."
metadata:
  ο.class: "continuant"
  ο.mode: "dependent"
  λ.in: ""
  λ.out: "[3-execute](phases/3-execute.md)"
  λ.kin: "[skills](integration/skills.md), [patterns](integration/patterns.md)"
  τ.goal: "idempotency"
---

# Tool Integrations

> learn + tools → grounded responses

## Available Tools

### Graph Analytics (relate:*)

| Tool | Purpose |
|------|---------|
| relate:generate_knowledge_graph | Extract graph from text |
| relate:generate_content_gaps | Find structural gaps |
| relate:generate_research_questions | Gap-based questions |
| relate:develop_text_tool | Combined analysis |

### Reasoning (think:*)

| Tool | Purpose |
|------|---------|
| think:thoughtbox | Step-by-step reasoning |
| think:mental_models | Access reasoning frameworks |
| think:notebook | Literate programming |

### Memory & Search

| Tool | Purpose |
|------|---------|
| web_search | External information |
| conversation_search | Past context |
| memory_user_edits | Persistent preferences |

## Usage Pattern

```python
# Phase 3 (Execute) tool invocation
if needs_grounding:
    results = await web_search(query)
if needs_structure:
    graph = await relate.generate_knowledge_graph(text)
if needs_reasoning:
    thoughts = await think.thoughtbox(problem)
```


## See Also

- [../concepts/vertex-sharing](concepts/vertex-sharing.md)
- [../concepts/topology-invariants](concepts/topology-invariants.md)
- [../phases/3-execute](phases/3-execute.md)
- [../phases/4-assess](phases/4-assess.md)
- [../meta/routing](meta/routing.md)
- [skills](integration/skills.md)
- [patterns](integration/patterns.md)

## Graph

**λ.out** (enables): [3-execute](phases/3-execute.md)
**λ.kin** (related): [skills](integration/skills.md), [patterns](integration/patterns.md)
**τ.goal**: idempotency
