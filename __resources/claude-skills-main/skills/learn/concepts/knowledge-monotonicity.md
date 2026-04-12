---
name: "knowledge-monotonicity"
description: "Knowledge never decreases: len(Κ')≥len(Κ) - delegates to shared operation."
metadata:
  ο.class: "continuant"
  ο.mode: "independent"
  λ.in: "[vertex-sharing](vertex-sharing.md)"
  λ.out: "[6-compound](../phases/6-compound.md), [compound-interest](compound-interest.md)"
  λ.kin: "[topology](topology-invariants.md)"
  τ.goal: "len(Κ')≥len(Κ)"
---

# Knowledge Monotonicity

> Knowledge only grows: len(Κ') ≥ len(Κ).

## Delegated Invariant

This concept delegates to the **shared monotonicity operation** to eliminate redundancy between learn and lambda-skill.

**See**: [`~/.claude/skills/shared/monotonicity.md`](../../shared/monotonicity.md)

The shared monotonicity operation provides the complete implementation of:
- K-monotonicity invariant: `len(K') ≥ len(K)`
- Line count validation across transformations
- Archival strategy instead of deletion
- Knowledge preservation mechanisms (accumulation, refinement, correction)

## Core Invariant

```python
assert len(K_new) >= len(K_old)  # Must always hold
```

## Why This Matters

- Prevents catastrophic forgetting
- Enables rollback to previous states
- Builds institutional memory

## Graph

**λ.in** (requires): [vertex-sharing](vertex-sharing.md)
**λ.out** (enables): [6-compound](../phases/6-compound.md), [compound-interest](compound-interest.md)
**λ.kin** (related): [topology](topology-invariants.md), [shared monotonicity](../../shared/monotonicity.md)
**τ.goal**: len(Κ')≥len(Κ)
