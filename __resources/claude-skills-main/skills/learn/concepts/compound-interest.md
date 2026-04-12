---
name: "compound-interest"
description: "Cumulative gains where outputs become inputs."
metadata:
  ο.class: "continuant"
  ο.mode: "independent"
  λ.in: "[Κ-monotonicity](concepts/knowledge-monotonicity.md)"
  λ.out: "[6-compound](phases/6-compound.md)"
  λ.kin: "[topology](concepts/topology-invariants.md)"
  τ.goal: "cumulative gains"
---

# Compound Interest

> Knowledge grows exponentially when the learning process itself improves.

## Core Insight

| Model | Equation | Behavior |
|-------|----------|----------|
| Linear | y = m·t | Constant progress rate |
| Compound | dy/dt = m·y | Accelerating progress |

Compound learning means *the rate of learning itself increases* with accumulated knowledge.

## Mathematical Foundation

The differential equation `dy/dt = m·y` has solution `y(t) = y₀·e^(m·t)`.

This exponential growth occurs because:
1. More knowledge → better pattern recognition
2. Better patterns → faster acquisition
3. Faster acquisition → more knowledge (loop)

## Implementation

```python
def compound_value(initial, rate, time):
    return initial * math.exp(rate * time)
```

## Graph

**λ.in** (requires): [Κ-monotonicity](concepts/knowledge-monotonicity.md)
**λ.out** (enables): [6-compound](phases/6-compound.md)
**λ.kin** (related): [topology](concepts/topology-invariants.md)
**τ.goal**: cumulative gains
