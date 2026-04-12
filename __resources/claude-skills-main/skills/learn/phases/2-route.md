---
name: "2-route"
description: "Select appropriate processing depth."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[1-parse](phases/1-parse.md)"
  λ.out: "[3-execute](phases/3-execute.md)"
  λ.kin: "[route op](operations/route.md), [routing](meta/routing.md)"
  τ.goal: "appropriate depth selection"
---

# Phase 2: Route

> components → pipeline — Select execution pipeline based on complexity.

## Input

Parsed components from [1-parse](phases/1-parse.md).

## Output

Pipeline selection: R0, R1, R2, or R3.

## Routing Logic

| Complexity | Pipeline | Description |
|------------|----------|-------------|
| < 2 | R0 | Direct response |
| < 4 | R1 | Single-skill |
| < 8 | R2 | Composition |
| ≥ 8 | R3 | Full orchestration |

## Decision Tree

```python
def route(components):
    c = components.complexity
    
    # Force escalation triggers
    if any(t in components.text for t in ["current", "latest", "verify"]):
        return R3
    
    if c < 2: return R0
    if c < 4: return R1
    if c < 8: return R2
    return R3
```

## Next

→ [3-execute](phases/3-execute.md) — Run selected pipeline


## See Also

- [../concepts/topology-invariants](concepts/topology-invariants.md)
- [../concepts/vertex-sharing](concepts/vertex-sharing.md)

## Graph

**λ.in** (requires): [1-parse](phases/1-parse.md)
**λ.out** (enables): [3-execute](phases/3-execute.md)
**λ.kin** (related): [route op](operations/route.md), [routing](meta/routing.md)
**τ.goal**: appropriate depth selection
