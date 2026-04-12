---
name: "compound"
description: "Combine parts into whole - delegates to shared compound operation."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[refactor](operations/refactor.md)"
  λ.out: "[crystallize](operations/crystallize.md)"
  λ.kin: "[6-compound](phases/6-compound.md)"
  τ.goal: "coherence"
---

# Compound

> improvements → Κ'

## Delegated Operation

This operation delegates to the **shared compound operation** to eliminate redundancy between learn and lambda-skill.

**See**: [`~/.claude/skills/shared/compound.md`](../../shared/compound.md)

The shared compound operation provides the complete implementation of:
- Knowledge accumulation formula: `K' = K ∪ crystallize(assess(τ))`
- Jaccard similarity-based deduplication (threshold 0.85)
- K-monotonicity preservation
- Integration with vertex-sharing invariant

## Properties

| Property | Value |
|----------|-------|
| Pure | No |
| Signature | `improvements → Κ'` |

## Usage

```python
# See shared/compound.md for full implementation
result = operations.compound(input)
```

## Related Operations

See [Operations INDEX](INDEX.md) for all operations.

## See Also

- [Shared Compound Operation](../../shared/compound.md) — Full implementation
- [../concepts/compound-interest](../concepts/compound-interest.md)
- [../phases/6-compound](../phases/6-compound.md)

## Graph

**λ.in** (requires): [refactor](refactor.md)
**λ.out** (enables): [crystallize](crystallize.md)
**λ.kin** (related): [6-compound](../phases/6-compound.md), [shared compound](../../shared/compound.md)
**τ.goal**: coherence
