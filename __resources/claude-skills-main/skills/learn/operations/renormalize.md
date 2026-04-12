---
name: "renormalize"
description: "Update meta-level from changes."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[integrate](operations/integrate.md)"
  λ.out: "[emit](operations/emit.md)"
  λ.kin: "[7-renormalize](phases/7-renormalize.md)"
  τ.goal: "compatibility"
---

# Renormalize

> Κ' → Σ'

## Description

Check convergence, apply schema updates, bump version if needed.

## Properties

| Property | Value |
|----------|-------|
| Pure | No |
| Signature | `Κ' → Σ'` |

## Usage

```python
result = operations.renormalize(input)
```

## Related Operations

See [Operations Index](INDEX.md) for all operations.


## See Also

- [../concepts/schema-evolution](concepts/schema-evolution.md)
- [../phases/7-renormalize](phases/7-renormalize.md)

## Graph

**λ.in** (requires): [integrate](operations/integrate.md)
**λ.out** (enables): [emit](operations/emit.md)
**λ.kin** (related): [7-renormalize](phases/7-renormalize.md)
**τ.goal**: compatibility
