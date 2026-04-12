---
name: "5-refactor"
description: "Improve structure, preserve semantics."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[4-assess](phases/4-assess.md)"
  λ.out: "[6-compound](phases/6-compound.md)"
  λ.kin: "[refactor op](operations/refactor.md), [path-optimization](concepts/path-optimization.md)"
  τ.goal: "semantic equivalence"
---

# Phase 5: Refactor

> evaluation → improvements — Address gaps, apply improvements.

## Input

Evaluation from [4-assess](phases/4-assess.md).

## Output

Improved results, applied changes.

## Refactoring Strategies

| Gap Type | Strategy |
|----------|----------|
| Missing info | Web search, tool call |
| Poor structure | Reorganize |
| Weak evidence | Add citations |
| Low clarity | Simplify language |

## Iteration Control

```python
max_iterations = 3
for i in range(max_iterations):
    if quality_score >= threshold:
        break
    apply_improvements()
    reassess()
```

## Pareto Principle

Focus on top 20% of improvements yielding 80% of value.
See [../concepts/pareto-governance](concepts/pareto-governance.md).

## Next

→ [6-compound](phases/6-compound.md) — Crystallize learnings


## See Also

- [../concepts/topology-invariants](concepts/topology-invariants.md)
- [../concepts/vertex-sharing](concepts/vertex-sharing.md)

## Graph

**λ.in** (requires): [4-assess](phases/4-assess.md)
**λ.out** (enables): [6-compound](phases/6-compound.md)
**λ.kin** (related): [refactor op](operations/refactor.md), [path-optimization](concepts/path-optimization.md)
**τ.goal**: semantic equivalence
