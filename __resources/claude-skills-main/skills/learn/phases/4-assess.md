---
name: "4-assess"
description: "Evaluate against quality criteria."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[3-execute](phases/3-execute.md)"
  λ.out: "[5-refactor](phases/5-refactor.md)"
  λ.kin: "[assess op](operations/assess.md), [convergence](concepts/convergence.md)"
  τ.goal: "honest evaluation"
---

# Phase 4: Assess

> results → evaluation — Evaluate results against quality criteria.

## Input

Results from [3-execute](phases/3-execute.md).

## Output

```yaml
quality_score: float     # 0-1 overall
gaps: list               # Missing elements
strengths: list          # What worked
improvements: list       # Suggested changes
```

## Assessment Lenses

| Lens | Focus | Weight |
|------|-------|--------|
| STRUCTURAL | Coherence, organization | 0.2 |
| EVIDENTIAL | Citations, grounding | 0.25 |
| PRAGMATIC | Usefulness, actionability | 0.25 |
| SCOPE | Completeness, coverage | 0.15 |
| ADVERSARIAL | Edge cases, weaknesses | 0.15 |

## Quality Score

```python
score = sum(lens.score * lens.weight for lens in lenses)
```

## Next

→ [5-refactor](phases/5-refactor.md) — Address identified gaps


## See Also

- [../concepts/topology-invariants](concepts/topology-invariants.md)
- [../concepts/vertex-sharing](concepts/vertex-sharing.md)

## Graph

**λ.in** (requires): [3-execute](phases/3-execute.md)
**λ.out** (enables): [5-refactor](phases/5-refactor.md)
**λ.kin** (related): [assess op](operations/assess.md), [convergence](concepts/convergence.md)
**τ.goal**: honest evaluation
