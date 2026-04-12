---
name: "execute"
description: "Perform atomic action."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[route](operations/route.md)"
  λ.out: "[assess](operations/assess.md)"
  λ.kin: "[3-execute](phases/3-execute.md)"
  τ.goal: "atomicity"
---

# Execute

> pipeline → results

## Description

Side-effectful execution of selected pipeline, invoking tools and skills as needed.

## Properties

| Property | Value |
|----------|-------|
| Pure | No |
| Signature | `pipeline → results` |

## Usage

```python
result = operations.execute(input)
```

## Related Operations

See [Operations Index](INDEX.md) for all operations.


## See Also

- [../concepts/scale-invariance](concepts/scale-invariance.md)
- [../phases/3-execute](phases/3-execute.md)
- [../integration/tools](integration/tools.md)

## Graph

**λ.in** (requires): [route](operations/route.md)
**λ.out** (enables): [assess](operations/assess.md)
**λ.kin** (related): [3-execute](phases/3-execute.md)
**τ.goal**: atomicity
