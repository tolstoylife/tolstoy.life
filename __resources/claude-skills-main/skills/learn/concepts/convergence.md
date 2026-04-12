---
name: "convergence"
description: "Iterative process reaching stable state."
metadata:
  ο.class: "continuant"
  ο.mode: "dependent"
  λ.in: "[fixed-point](concepts/fixed-point.md)"
  λ.out: "[4-assess](phases/4-assess.md)"
  λ.kin: "[path-optimization](concepts/path-optimization.md)"
  τ.goal: "stable state detection"
---

# Convergence

> When to stop iterating—similarity threshold reached.

## Convergence Criteria

Multi-level similarity check:

```python
weighted_sim = (
    0.5 * similarity(current.strategic, previous.strategic) +
    0.3 * similarity(current.tactical, previous.tactical) +
    0.2 * similarity(current.operational, previous.operational)
)
return weighted_sim > thresholds[pipeline]
```

## Threshold by Pipeline

| Pipeline | Threshold | Rationale |
|----------|-----------|-----------|
| R1 | 0.85 | Simple tasks, quick convergence |
| R2 | 0.92 | Moderate depth, balanced |
| R3 | 0.96 | Deep reasoning, high precision |

## Detection

```python
def is_converged(current, previous, pipeline):
    return weighted_similarity(current, previous) > THRESHOLDS[pipeline]
```

## Graph

**λ.in** (requires): [fixed-point](concepts/fixed-point.md)
**λ.out** (enables): [4-assess](phases/4-assess.md)
**λ.kin** (related): [path-optimization](concepts/path-optimization.md)
**τ.goal**: stable state detection
