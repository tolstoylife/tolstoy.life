# Compound Engineering Reference

The self-improvement loop that makes knowledge recursive.

## Core Principle

**"Each unit of engineering work should make subsequent units easier—not harder."**

```haskell
compound :: Knowledge -> Response -> Knowledge
compound K τ = K ∪ crystallize(assess(τ))

-- K grows monotonically; never loses valid knowledge
-- Crystallization compresses: raw experience -> reusable pattern
```

## The Compound Loop

```
Plan(K) -> Execute -> Assess -> Compound(K->K')
   ↑                              |
   └────────── K' ────────────────┘
```

Each iteration makes the next **easier**, not harder.

## Abductive Learning Protocol

### The OHPT Chain

| Phase | Question | Output |
|-------|----------|--------|
| **O**bservation | What behavior was observed? | Symptom description |
| **H**ypothesis | What best explains O? | Candidate explanation |
| **P**rediction | If H true, what else is true? | Testable prediction |
| **T**est | Does P hold? | Confirmation/refutation |

### Implementation Pattern

```python
def debug_with_abduction(symptom: str) -> Solution:
    """
    Abductive debugging protocol.

    O: symptom (given)
    H: generate_hypotheses(symptom)
    P: for h in H: derive_predictions(h)
    T: for p in P: test_prediction(p)
    """
    # O: Observation
    observation = analyze_symptom(symptom)

    # H: Generate hypotheses (best explanations)
    hypotheses = [
        rank_by_parsimony(h)
        for h in generate_explanations(observation)
    ]

    # P: Derive testable predictions
    for hypothesis in hypotheses:
        predictions = derive_predictions(hypothesis)

        # T: Test predictions
        for prediction in predictions:
            if test_prediction(prediction):
                return Solution(
                    hypothesis=hypothesis,
                    evidence=prediction,
                    confidence=calculate_confidence(prediction)
                )

    return Solution.unknown()
```

## Trigger Detection

Compound when resolution patterns detected:

| Pattern | Example | Action |
|---------|---------|--------|
| Confirmation | "that worked", "correct" | Extract solution |
| Insight | "I see now", "the key is" | Extract principle |
| Prevention | "next time", "to avoid" | Extract guard |
| Connection | "this relates to", "like" | Extract vertex |

## Knowledge Crystallization Schema

```yaml
# Required structure for all compounded learnings
date: 2026-01-14
trigger: "what initiated the learning"
domain: "coding|architecture|debugging|testing|..."

# The OHPT chain
observation: "what was observed (symptom)"
hypothesis: "best explanation"
prediction: "what should be true if H correct"
test: "how prediction was verified"

# Resolution
root_cause: "fundamental cause (not surface)"
solution: "what worked"
why_works: "mechanistic explanation"
prevention: "how to avoid in future"

# Integration
vertices:
  - "[[shared concept 1]]"
  - "[[shared concept 2]]"
related:
  - "link to similar learning"

# Epistemic
confidence: 0.85
evidence_strength: "strong|moderate|weak"
```

## Validation Checklist

Before adding to K:

- [ ] Has >=2 shared vertices with existing K
- [ ] Root cause is fundamental (not surface symptom)
- [ ] Solution is generalizable (not one-off)
- [ ] Prevention is actionable
- [ ] OHPT chain is complete

```python
def validate_learning(learning: Learning, K: Knowledge) -> bool:
    shared = find_shared_vertices(learning, K)
    return (
        len(shared) >= 2 and
        is_fundamental(learning.root_cause) and
        is_generalizable(learning.solution) and
        is_actionable(learning.prevention) and
        is_complete(learning.ohpt_chain)
    )
```

## Integration Protocol

```haskell
integrate :: Learning -> Knowledge -> Knowledge
integrate l K =
  let shared = vertices(l) ∩ concepts(K)
  in case shared of
       []  -> K ∪ bridge(l, analogical_map(l, K))  -- Create bridge
       _   -> K ∪ link(l, shared)                   -- Direct merge
```

### Vertex Sharing (η ≥ 4)

New knowledge must connect to existing knowledge:

```python
def integrate_learning(learning: Learning, K: Knowledge) -> Knowledge:
    shared_vertices = find_shared_vertices(learning, K)

    if len(shared_vertices) == 0:
        # Create analogical bridge
        similar = find_most_similar(learning, K)
        bridge = create_bridge(learning, similar)
        return K.union(learning).union(bridge)
    else:
        # Direct integration via shared vertices
        return K.union(learning).link(shared_vertices)
```

## Decay and Retrieval

### Decay Function

Recent learnings weighted higher:

```python
def decay(date: datetime) -> float:
    days = (datetime.now() - date).days
    return 0.95 ** days  # Half-life ~14 days

def effective_weight(learning: Learning) -> float:
    # High-confidence learnings resist decay
    return learning.confidence + (1 - learning.confidence) * decay(learning.date)
```

### Retrieval Protocol

```python
def retrieve_relevant(query: str, K: Knowledge, limit: int = 5) -> List[Learning]:
    # 1. Extract query concepts
    concepts = parse_concepts(query)

    # 2. Find learnings with shared vertices
    relevant = [l for l in K if shared_vertices(l, concepts)]

    # 3. Rank by relevance × recency × confidence
    ranked = sorted(relevant, key=lambda l:
        similarity(l, query) * decay(l.date) * l.confidence,
        reverse=True
    )

    return ranked[:limit]
```

## Anti-Patterns

| Anti-Pattern | Why Bad | Correct Approach |
|--------------|---------|------------------|
| Raw conversation storage | Not crystallized, no reuse | Extract patterns |
| Surface symptoms as root cause | Will recur | Dig to fundamental cause |
| One-off solutions | Not generalizable | Abstract the principle |
| Orphan learnings | Cannot retrieve | Ensure vertex sharing |
| Overconfident weights | Miscalibration | Match confidence to evidence |
| Deleting knowledge | Monotonicity violation | Supersede or refine |

## Hookify Integration

The following hooks enforce compound engineering:

| Hook | Event | Purpose |
|------|-------|---------|
| `compound-learning` | stop | Prompt crystallization before ending |
| `abductive-hypothesis` | file | Ensure OHPT chain in tests |
| `knowledge-monotonicity` | file | Prevent knowledge deletion |
| `vertex-sharing` | file | Require vertex connections |
| `inference-chain` | file | Complete uncertainty markers |
| `pattern-crystallization` | bash | Prompt extraction on commits |

## Self-Application

This reference applies to itself:
- Reading it triggers learning about compound loops
- The structure IS a compound pattern
- Future invocations will reference this knowledge

```haskell
-- The compound reference is homoiconic
compound_reference :: Learning
compound_reference = Learning {
  observation = "No systematic self-improvement",
  hypothesis = "Need explicit compound loop",
  prediction = "Structured extraction enables reuse",
  test = "Apply protocol, measure knowledge growth",
  solution = "This reference document",
  vertices = ["compound-interest", "homoiconicity", "abduction"]
}
```
