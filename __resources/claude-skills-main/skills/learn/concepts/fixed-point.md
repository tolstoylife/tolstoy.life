---
name: "fixed-point"
description: "States unchanged by transformation: f(x)=x."
metadata:
  ο.class: "continuant"
  ο.mode: "independent"
  λ.in: ""
  λ.out: "[convergence](concepts/convergence.md), [homoiconicity](concepts/homoiconicity.md)"
  λ.kin: "[scale-invariance](concepts/scale-invariance.md)"
  τ.goal: "f(x)=x equilibrium"
---

# Fixed Point

> Σ∞ = lim Σₙ — the stable state where further refinement yields no change.

## Definition

A fixed point is a state where applying the transformation yields the same state:

```
λ(Σ∞) = Σ∞
```

In learn skill context: the schema where self-improvement produces no further changes.

## Mathematical Properties

1. **Existence**: Guaranteed by Brouwer's theorem for continuous maps
2. **Uniqueness**: Not guaranteed; multiple fixed points possible
3. **Stability**: Attracting fixed points draw nearby trajectories

## Detection

```python
def at_fixed_point(schema, epsilon=0.001):
    evolved = apply_learning(schema)
    return distance(schema, evolved) < epsilon
```

## Practical Implications

- Fixed point = local optimum of learning process
- Multiple fixed points → path dependency matters
- Perturbation can escape local fixed points

## Graph

**λ.out** (enables): [convergence](concepts/convergence.md), [homoiconicity](concepts/homoiconicity.md)
**λ.kin** (related): [scale-invariance](concepts/scale-invariance.md)
**τ.goal**: f(x)=x equilibrium
