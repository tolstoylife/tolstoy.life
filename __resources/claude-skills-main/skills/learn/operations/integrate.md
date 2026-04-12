---
name: "integrate"
description: "Connect new to existing graph."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[crystallize](operations/crystallize.md), [vertex-sharing](concepts/vertex-sharing.md)"
  λ.out: "[renormalize](operations/renormalize.md)"
  λ.kin: ""
  τ.goal: "vertex-sharing"
---

# Integrate

> new → PKM'

## Description

Find shared vertices, create bridges, maintain topology invariants.

## Properties

| Property | Value |
|----------|-------|
| Pure | No |
| Signature | `new → PKM'` |

## Usage

```python
result = operations.integrate(input)
```

## Related Operations

See [Operations Index](INDEX.md) for all operations.


## See Also

- [../concepts/vertex-sharing](concepts/vertex-sharing.md)
- [../concepts/metagraph](concepts/metagraph.md)

## Graph

**λ.in** (requires): [crystallize](operations/crystallize.md), [vertex-sharing](concepts/vertex-sharing.md)
**λ.out** (enables): [renormalize](operations/renormalize.md)
**τ.goal**: vertex-sharing
