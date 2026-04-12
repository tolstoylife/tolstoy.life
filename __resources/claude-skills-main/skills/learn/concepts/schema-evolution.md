---
name: "schema-evolution"
description: "Schema refinement through feedback."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[homoiconicity](concepts/homoiconicity.md)"
  λ.out: "[7-renormalize](phases/7-renormalize.md)"
  λ.kin: "[vertex-sharing](concepts/vertex-sharing.md)"
  τ.goal: "capability expansion"
---

# Schema Evolution

> How Σ changes over time—schema itself improves through learning cycles.

## Evolution Equation

```
Σₙ₊₁ = refactor(assess(Σₙ))
```

## Stages

1. **Assessment**: Evaluate current schema against invariants
2. **Identification**: Find suboptimal patterns
3. **Refactoring**: Apply improvements
4. **Validation**: Ensure invariants preserved
5. **Integration**: Merge into live schema

## Versioning

```python
@dataclass
class SchemaVersion:
    major: int  # Breaking changes
    minor: int  # New features
    patch: int  # Bug fixes
    
def bump_version(current, change_type):
    if change_type == "breaking":
        return SchemaVersion(current.major + 1, 0, 0)
    elif change_type == "feature":
        return SchemaVersion(current.major, current.minor + 1, 0)
    else:
        return SchemaVersion(current.major, current.minor, current.patch + 1)
```

## Convergence

Schema evolution converges when:
- `similarity(Σₙ, Σₙ₊₁) > threshold`
- All invariants satisfied
- No suboptimal patterns detected

## Graph

**λ.in** (requires): [homoiconicity](concepts/homoiconicity.md)
**λ.out** (enables): [7-renormalize](phases/7-renormalize.md)
**λ.kin** (related): [vertex-sharing](concepts/vertex-sharing.md)
**τ.goal**: capability expansion
