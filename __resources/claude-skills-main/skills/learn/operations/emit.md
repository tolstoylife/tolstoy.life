---
name: "emit"
description: "Produce formatted output."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[renormalize](operations/renormalize.md)"
  λ.out: ""
  λ.kin: ""
  τ.goal: "format compliance"
---

# Emit

> synthesized → τ

## Description

Format output according to Φ style rules and pipeline constraints.

## Properties

| Property | Value |
|----------|-------|
| Pure | Yes |
| Signature | `synthesized → τ` |

## Usage

```python
result = operations.emit(input)
```

## Related Operations

See [Operations Index](INDEX.md) for all operations.


## See Also

- [../concepts/scale-invariance](concepts/scale-invariance.md)
- [../meta/routing](meta/routing.md)

## Graph

**λ.in** (requires): [renormalize](operations/renormalize.md)
**τ.goal**: format compliance
