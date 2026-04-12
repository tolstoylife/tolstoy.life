# Compound Reference (Κ)

The self-improvement loop that makes λ recursive.

## Core Transformation

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

Each iteration makes the next **easier**, not harder. This is the fundamental insight from compound engineering.

## Trigger Detection

Compound when resolution patterns detected:

| Pattern | Example | Action |
|---------|---------|--------|
| Confirmation | "that worked", "correct" | Extract solution |
| Insight | "I see now", "the key is" | Extract principle |
| Prevention | "next time", "to avoid" | Extract guard |
| Connection | "this relates to", "like" | Extract vertex |

## Extraction Protocol

### 1. Context Gathering

Extract from conversation:
- **Symptom**: What triggered the inquiry
- **Investigation**: Steps taken, what didn't work
- **Root cause**: Fundamental reason (not surface)
- **Solution**: What resolved it
- **Prevention**: How to avoid recurrence

### 2. Knowledge Crystallization

```yaml
# learning artifact schema
date: 2026-01-07
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

### 3. Validation

Before adding to K:
- [ ] Has ≥2 shared vertices with existing K
- [ ] Root cause is fundamental (not surface symptom)
- [ ] Solution is generalizable (not one-off)
- [ ] Prevention is actionable

### 4. Integration

```haskell
integrate :: Learning → Knowledge → Knowledge
integrate l K = 
  let shared = vertices(l) ∩ concepts(K)
  in case shared of
       []  → K ∪ bridge(l, analogical_map(l, K))  -- Create bridge
       _   → K ∪ link(l, shared)                   -- Direct merge
```

## Parallel Extraction Agents

For comprehensive capture, spawn parallel extractors:

| Agent | Focus | Output |
|-------|-------|--------|
| context-analyzer | Problem type, component, symptoms | YAML skeleton |
| solution-extractor | Root cause, working fix | Solution block |
| prevention-strategist | Future avoidance | Prevention rules |
| vertex-finder | Shared concepts with PKM | Vertex list |
| cross-referencer | Similar patterns in K | Related links |

Synthesize outputs into single crystallized learning.

## Storage Patterns

### By Domain (for retrieval)
```
learnings/
├── physiology/
├── pharmacology/
├── reasoning/
├── examination/
└── meta/           # Learnings about learning
```

### By Type (for application)
```
patterns/
├── solutions/      # What works
├── antipatterns/   # What fails
├── principles/     # Generalizable rules
└── bridges/        # Cross-domain connections
```

## Retrieval Protocol

Future queries access K:

```python
def plan_with_knowledge(query, K):
    # 1. Extract query concepts
    concepts = parse_concepts(query)
    
    # 2. Find relevant learnings
    relevant = [l for l in K if shared_vertices(l, concepts)]
    
    # 3. Rank by relevance × recency × confidence
    ranked = sorted(relevant, key=lambda l: 
        similarity(l, query) * decay(l.date) * l.confidence)
    
    # 4. Include top learnings in context
    return plan(query, context=ranked[:5])
```

## Decay Function

Recent learnings weighted higher:

```python
decay(date) = 0.95 ** days_since(date)  # λ=0.95 half-life ~14 days
```

But high-confidence learnings resist decay:

```python
effective_weight(l) = l.confidence + (1 - l.confidence) * decay(l.date)
```

## Self-Application

This reference applies to itself:
- Reading it triggers learning about compound loops
- The structure IS a compound pattern (problem: no self-improvement → solution: compound loop)
- Future λ invocations will reference this knowledge

## Connection to λο.τ

```haskell
-- Standard λ
λο.τ = emit ∘ validate ∘ compose ∘ execute ∘ route ∘ parse

-- With compounding
λ(ο,K).τ = 
  let τ = (emit ∘ validate ∘ compose ∘ execute(K) ∘ route ∘ parse) ο
      K' = compound K τ
  in (τ, K')
```

The compound step **after** emit ensures:
1. Response quality doesn't degrade
2. Learning is based on validated output
3. K grows only with assessed knowledge

## Renormalization Analogy

Like physical renormalization groups:
- Filter irrelevant details (noise)
- Compress redundant patterns (crystallize)
- Preserve essential structure (invariants)
- Apply across scales (fractal self-similarity)

```
K' = RG(K ∪ new_experience)

where RG preserves:
- Vertex connectivity (η)
- Governance compliance (KROG)
- Style constraints (Φ)
```

## Anti-Patterns

❌ Storing raw conversation (not crystallized)
❌ Surface symptoms as root cause
❌ One-off solutions (not generalizable)
❌ Orphan learnings (no shared vertices)
❌ Overconfident weights (confidence > evidence)

✓ Crystallized principles
✓ Fundamental root causes
✓ Generalizable patterns
✓ Vertex-linked integration
✓ Calibrated confidence
