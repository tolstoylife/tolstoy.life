---
name: "homoiconicity"
description: "Schema can process itself: Σ.process(Σ)."
metadata:
  ο.class: "continuant"
  ο.mode: "independent"
  λ.in: "[fixed-point](concepts/fixed-point.md), [scale-invariance](concepts/scale-invariance.md)"
  λ.out: "[7-renormalize](phases/7-renormalize.md), [meta domain](domains/meta.md)"
  λ.kin: "[schema-evolution](concepts/schema-evolution.md), [metagraph](concepts/metagraph.md)"
  τ.goal: "Σ.process(Σ)"
---

# Homoiconicity

> Schema can process itself—Σ.can_process(Σ) = True.

## Definition

A system is homoiconic when its structure can be manipulated by its own operations:

```python
assert learn_skill.can_process(learn_skill.schema) == True
```

## Properties

1. **Self-reference**: Structure can reference itself
2. **Self-modification**: Can change own behavior
3. **Closure**: Operations on schema produce valid schema

## Implementation Test

```python
def test_homoiconicity():
    skill = load_skill("learn")
    # Skill can analyze its own structure
    analysis = skill.analyze(skill.schema)
    # Skill can improve its own structure
    improved = skill.improve(skill.schema)
    # Result is still valid skill schema
    assert validate_schema(improved)
```

## Significance

Homoiconicity enables:
- Recursive self-improvement
- Meta-learning (learning how to learn)
- Schema evolution without external intervention

## Graph

**lambda.in** (requires): [fixed-point](fixed-point.md), [scale-invariance](scale-invariance.md), [metasuperhypergraph](metasuperhypergraph.md)
**lambda.out** (enables): [7-renormalize](../phases/7-renormalize.md), [meta domain](../domains/meta.md)
**lambda.kin** (related): [schema-evolution](schema-evolution.md), [metagraph](metagraph.md)
**tau.goal**: Sigma.process(Sigma)
