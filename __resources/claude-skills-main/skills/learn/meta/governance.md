---
name: "governance"
description: "Constraint enforcement (KROG)."
metadata:
  ο.class: "continuant"
  ο.mode: "independent"
  λ.in: "[topology](concepts/topology-invariants.md), [meta domain](domains/meta.md)"
  λ.out: "[routing](meta/routing.md)"
  λ.kin: "[pareto](concepts/pareto-governance.md)"
  τ.goal: "KROG compliance"
---

# Governance

> action → valid | invalid

## KROG Validation

Every action must satisfy:

| Criterion | Description | Check |
|-----------|-------------|-------|
| **K**nowable | Effects are transparent | Can predict outcome? |
| **R**ights | Authority to act | Have permission? |
| **O**bligations | Duties fulfilled | Responsibilities met? |
| **G**overnance | Within bounds | Policy compliant? |

```python
def validate_action(action):
    return (
        is_knowable(action) and
        has_rights(action) and
        meets_obligations(action) and
        within_governance(action)
    )
```

## Topology Invariants

| Invariant | Expression | Enforcement |
|-----------|------------|-------------|
| Density | η ≥ 4 | Reject if violated |
| Isolation | φ < 0.2 | Auto-connect orphans |
| Monotonicity | len(Κ') ≥ len(Κ) | Never delete knowledge |

## Deontic Modalities

```haskell
data D = P a | O a | F a | I a
-- P: Permitted, O: Obligated, F: Forbidden, I: Impossible

O a ⊢ P a          -- Ought implies may
P a ⟺ ¬F a         -- Permission = ¬Prohibition
```

## Constraint Trichotomy

| Type | Effect | Example |
|------|--------|---------|
| Enabling | Expands action space | Tool permissions |
| Governing | Channels behavior | Routing rules |
| Constitutive | Defines identity | Core invariants |


## See Also

- [../concepts/topology-invariants](concepts/topology-invariants.md)
- [../concepts/knowledge-monotonicity](concepts/knowledge-monotonicity.md)
- [../concepts/homoiconicity](concepts/homoiconicity.md)
- [../concepts/vertex-sharing](concepts/vertex-sharing.md)
- [../concepts/fixed-point](concepts/fixed-point.md)
- [../phases/4-assess](phases/4-assess.md)
- [../phases/7-renormalize](phases/7-renormalize.md)
- [../operations/refactor](operations/refactor.md)
- [../integration/orchestrator](integration/orchestrator.md)
- [routing](meta/routing.md)

## Graph

**λ.in** (requires): [topology](concepts/topology-invariants.md), [meta domain](domains/meta.md)
**λ.out** (enables): [routing](meta/routing.md)
**λ.kin** (related): [pareto](concepts/pareto-governance.md)
**τ.goal**: KROG compliance
