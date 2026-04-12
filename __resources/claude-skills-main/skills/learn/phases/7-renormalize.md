---
name: "7-renormalize"
description: "Update schema from learnings."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[6-compound](phases/6-compound.md)"
  λ.out: "[SKILL](SKILL.md)"
  λ.kin: "[renormalize op](operations/renormalize.md), [homoiconicity](concepts/homoiconicity.md)"
  τ.goal: "schema evolution"
---

# Phase 7: Renormalize

> Κ' → Σ' — Update schema if structural changes warranted.

## Input

Updated knowledge Κ' from [6-compound](phases/6-compound.md).

## Output

Potentially updated schema Σ' (or unchanged Σ).

## Convergence Check

```python
similarity = weighted_similarity(Σ_new, Σ_old)
if similarity > thresholds[pipeline]:
    return Σ_old  # Converged, no change
else:
    return validate_and_apply(Σ_new)
```

## Schema Update Criteria

1. **Invariant violation** detected → Must update
2. **New pattern** identified → May update
3. **Optimization** possible → Consider update

## Version Bump

| Change Type | Version Bump |
|-------------|--------------|
| Breaking | Major (X.0.0) |
| Feature | Minor (0.X.0) |
| Fix | Patch (0.0.X) |

## Homoiconic Closure

This phase enables [../concepts/homoiconicity](concepts/homoiconicity.md) — the skill can improve itself.

## Cycle Complete

→ Return to [1-parse](phases/1-parse.md) for next query, now with improved Κ and potentially Σ.


## See Also

- [../concepts/topology-invariants](concepts/topology-invariants.md)
- [../concepts/vertex-sharing](concepts/vertex-sharing.md)

## Graph

**λ.in** (requires): [6-compound](phases/6-compound.md)
**λ.out** (enables): [SKILL](SKILL.md)
**λ.kin** (related): [renormalize op](operations/renormalize.md), [homoiconicity](concepts/homoiconicity.md)
**τ.goal**: schema evolution
