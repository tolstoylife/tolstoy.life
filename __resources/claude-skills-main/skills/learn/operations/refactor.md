---
name: "refactor"
description: "Restructure without behavior change."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[assess](operations/assess.md)"
  λ.out: "[compound](operations/compound.md)"
  λ.kin: "[5-refactor](phases/5-refactor.md)"
  τ.goal: "semantics preserved"
---

# Refactor

> evaluation → improvements

## Description

Iteratively improve results based on assessment, applying Pareto governance.

## Properties

| Property | Value |
|----------|-------|
| Pure | No |
| Signature | `evaluation → improvements` |

## Usage

```python
result = operations.refactor(input)
```

## Related Operations

See [Operations Index](INDEX.md) for all operations.


## See Also

- [../concepts/pareto-governance](concepts/pareto-governance.md)
- [../phases/5-refactor](phases/5-refactor.md)

## Graph

**λ.in** (requires): [assess](operations/assess.md)
**λ.out** (enables): [compound](operations/compound.md)
**λ.kin** (related): [5-refactor](phases/5-refactor.md)
**τ.goal**: semantics preserved
