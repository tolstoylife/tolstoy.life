---
name: "parse"
description: "Decompose input into tokens/AST."
metadata:
  ο.class: "occurrent"
  ο.mode: "independent"
  λ.in: ""
  λ.out: "[route](operations/route.md)"
  λ.kin: "[1-parse](phases/1-parse.md)"
  τ.goal: "reversibility"
---

# Parse

> ο → components

## Description

Stateless decomposition of raw query into intent, domain, complexity, and shared vertices.

## Properties

| Property | Value |
|----------|-------|
| Pure | Yes |
| Signature | `ο → components` |

## Usage

```python
result = operations.parse(input)
```

## Related Operations

See [Operations Index](INDEX.md) for all operations.


## See Also

- [../concepts/vertex-sharing](concepts/vertex-sharing.md)
- [../phases/1-parse](phases/1-parse.md)

## Graph

**λ.out** (enables): [route](operations/route.md)
**λ.kin** (related): [1-parse](phases/1-parse.md)
**τ.goal**: reversibility
