---
name: "route"
description: "Direct to appropriate handler."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[parse](operations/parse.md)"
  λ.out: "[execute](operations/execute.md)"
  λ.kin: "[2-route](phases/2-route.md)"
  τ.goal: "determinism"
---

# Route

> components → pipeline

## Description

Determine R0/R1/R2/R3 based on complexity score and trigger patterns.

## Properties

| Property | Value |
|----------|-------|
| Pure | Yes |
| Signature | `components → pipeline` |

## Usage

```python
result = operations.route(input)
```

## Related Operations

See [Operations Index](INDEX.md) for all operations.


## See Also

- [../concepts/path-optimization](concepts/path-optimization.md)
- [../phases/2-route](phases/2-route.md)
- [../meta/routing](meta/routing.md)

## Graph

**λ.in** (requires): [parse](operations/parse.md)
**λ.out** (enables): [execute](operations/execute.md)
**λ.kin** (related): [2-route](phases/2-route.md)
**τ.goal**: determinism
