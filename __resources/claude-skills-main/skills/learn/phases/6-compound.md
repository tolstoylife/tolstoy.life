---
name: "6-compound"
description: "Crystallize learnings into knowledge base with compound-engineering constraints."
---

# Phase 6: Compound

> improvements → Κ' — Crystallize learnings into knowledge base.

## Core Principle (Compound Engineering)

**"Each unit of engineering work should make subsequent units easier—not harder."**

```haskell
compound :: Knowledge → Response → Knowledge
compound K τ = K ∪ crystallize(assess(τ))

-- K grows monotonically; never loses valid knowledge
-- Crystallization compresses: raw experience → reusable pattern
```

## The Compound Loop

```
Plan(K) → Execute → Assess → Compound(K→K')
   ↑                              |
   └────────── K' ────────────────┘
```

## Input

Improvements from [5-refactor](5-refactor.md).

## Output

Updated knowledge base Κ'.

## Trigger Detection

Compound when resolution patterns detected:

| Pattern | Example | Action |
|---------|---------|--------|
| Confirmation | "that worked", "correct" | Extract solution |
| Insight | "I see now", "the key is" | Extract principle |
| Prevention | "next time", "to avoid" | Extract guard |
| Connection | "this relates to", "like" | Extract vertex |

## Learning Artifact Schema

```yaml
# Required structure for all compounded learnings
date: 2026-01-14
trigger: "what initiated the learning"
domain: "area of knowledge (physiology|pharmacology|reasoning|...)"
symptom: "observable problem"
root_cause: "fundamental cause (not surface)"
solution: "what worked"
why_works: "mechanistic explanation"
prevention: "how to avoid in future"
vertices:
  - "[[shared concept 1]]"
  - "[[shared concept 2]]"
related:
  - "link to similar learning"
confidence: 0.85  # epistemic weight
```

## Validation Before Adding to K

- [ ] Has ≥2 shared vertices with existing K
- [ ] Root cause is fundamental (not surface symptom)
- [ ] Solution is generalizable (not one-off)
- [ ] Prevention is actionable

```python
assert find_shared_vertices(new_knowledge, existing_K) != []
```

## Knowledge Types

| Type | Storage | Example |
|------|---------|---------|
| Facts | Κ.facts | "η must be ≥ 4" |
| Patterns | Κ.patterns | "Route before execute" |
| Heuristics | Κ.heuristics | "Prefer parsimony" |
| Solutions | Κ.solutions | "What works" |
| Antipatterns | Κ.antipatterns | "What fails" |
| Bridges | Κ.bridges | "Cross-domain connections" |

## Anti-Patterns (NEVER)

❌ Storing raw conversation (not crystallized)
❌ Surface symptoms as root cause
❌ One-off solutions (not generalizable)
❌ Orphan learnings (no shared vertices)
❌ Overconfident weights (confidence > evidence)

## Integration Requirement

See [../concepts/vertex-sharing](../concepts/vertex-sharing.md) — new knowledge must connect.

```haskell
integrate :: Learning → Knowledge → Knowledge
integrate l K =
  let shared = vertices(l) ∩ concepts(K)
  in case shared of
       []  → K ∪ bridge(l, analogical_map(l, K))  -- Create bridge
       _   → K ∪ link(l, shared)                   -- Direct merge
```

## Next

→ [7-renormalize](7-renormalize.md) — Update schema if needed

## Graph

**λ.in** (requires): [5-refactor](5-refactor.md)
**λ.out** (enables): [7-renormalize](7-renormalize.md)
**λ.kin** (related): [compound op](../operations/compound.md), [Κ-monotonicity](../concepts/knowledge-monotonicity.md)
**τ.goal**: Κ-monotonicity
