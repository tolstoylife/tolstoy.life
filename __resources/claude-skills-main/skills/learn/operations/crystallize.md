---
name: "crystallize"
description: "Solidify fluid knowledge into patterns."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[compound](operations/compound.md)"
  λ.out: "[integrate](operations/integrate.md)"
  λ.kin: ""
  τ.goal: "fidelity"
---

# Crystallize

> experience → patterns

## Description

Identify reusable patterns from accumulated experience.

## Properties

| Property | Value |
|----------|-------|
| Pure | Yes |
| Signature | `experience → patterns` |

## Usage

```python
result = operations.crystallize(input)
```

## Related Operations

See [Operations Index](INDEX.md) for all operations.


## See Also

- [../concepts/knowledge-monotonicity](concepts/knowledge-monotonicity.md)
- [../concepts/fixed-point](concepts/fixed-point.md)

## Graph

**λ.in** (requires): [compound](operations/compound.md)
**λ.out** (enables): [integrate](operations/integrate.md)
**τ.goal**: fidelity
