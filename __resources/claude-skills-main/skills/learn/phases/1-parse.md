---
name: "1-parse"
description: "Transform input into processable form."
metadata:
  ο.class: "occurrent"
  ο.mode: "independent"
  λ.in: "[SKILL](SKILL.md)"
  λ.out: "[2-route](phases/2-route.md)"
  λ.kin: "[parse op](operations/parse.md)"
  τ.goal: "information preservation"
---

# Phase 1: Parse

> ο → components — Decompose query into structured representation.

## Input

Raw query ο from user.

## Output

```yaml
intent: string           # What user wants
domain: string           # Which domain applies
complexity: float        # 0-10 score
shared_vertices: list    # Concepts in PKM
```

## Operations

1. **Intent classification**: What type of task?
2. **Domain detection**: Which domain config applies?
3. **Complexity scoring**: How much reasoning needed?
4. **Vertex identification**: What existing concepts connect?

## Complexity Formula

```python
complexity = (
    domains * 2 +      # Multi-domain bonus
    depth * 3 +        # Reasoning depth
    stakes * 1.5 +     # Consequence weight
    novelty * 2        # New territory
)
```

## Next

→ [2-route](phases/2-route.md) — Select execution pipeline


## See Also

- [../concepts/topology-invariants](concepts/topology-invariants.md)
- [../concepts/vertex-sharing](concepts/vertex-sharing.md)

## Graph

**λ.in** (requires): [SKILL](SKILL.md)
**λ.out** (enables): [2-route](phases/2-route.md)
**λ.kin** (related): [parse op](operations/parse.md)
**τ.goal**: information preservation
