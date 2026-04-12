---
name: "assess"
description: "Measure quality against criteria."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[execute](operations/execute.md)"
  λ.out: "[refactor](operations/refactor.md)"
  λ.kin: "[4-assess](phases/4-assess.md)"
  τ.goal: "consistency"
---

# Assess

> results → evaluation

## Description

Apply multi-lens assessment (STRUCTURAL, EVIDENTIAL, PRAGMATIC, SCOPE, ADVERSARIAL).

## Properties

| Property | Value |
|----------|-------|
| Pure | Yes |
| Signature | `results → evaluation` |

## Usage

```python
result = operations.assess(input)
```

## Related Operations

See [Operations Index](INDEX.md) for all operations.


## See Also

- [../concepts/topology-invariants](concepts/topology-invariants.md)
- [../phases/4-assess](phases/4-assess.md)

## Graph

**λ.in** (requires): [execute](operations/execute.md)
**λ.out** (enables): [refactor](operations/refactor.md)
**λ.kin** (related): [4-assess](phases/4-assess.md)
**τ.goal**: consistency
