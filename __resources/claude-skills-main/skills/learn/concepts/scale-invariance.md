---
name: "scale-invariance"
description: "Same patterns at all scales."
metadata:
  ο.class: "continuant"
  ο.mode: "independent"
  λ.in: ""
  λ.out: "[homoiconicity](concepts/homoiconicity.md), [metagraph](concepts/metagraph.md)"
  λ.kin: "[fixed-point](concepts/fixed-point.md)"
  τ.goal: "universal patterns"
---

# Scale Invariance

> Same structure and operations at every level—micro, meso, macro all follow λο.τ pattern.

## Definition

A system is scale-invariant when zooming in or out reveals the same structure:

```
structure(skill) ≅ structure(domain) ≅ structure(file) ≅ structure(section)
```

## Manifestation in Learn Skill

| Level | λ | ο | τ |
|-------|---|---|---|
| Skill | 7-phase loop | Query | Response |
| Domain | Domain config | Domain query | Domain response |
| File | File operations | File content | Updated file |
| Section | Section ops | Section text | Updated text |

## Implementation

```python
class Holon:
    "Scale-invariant unit."
    def __init__(self, λ, children=None):
        self.λ = λ
        self.children = children or []
    
    def process(self, ο):
        # Same operation at every level
        return self.λ(ο, [c.process(ο) for c in self.children])
```

## Benefits

- Predictable behavior at any scale
- Reusable patterns
- Compositional reasoning

## Graph

**lambda.out** (enables): [homoiconicity](homoiconicity.md), [metagraph](metagraph.md), [metasuperhypergraph](metasuperhypergraph.md)
**lambda.kin** (related): [fixed-point](fixed-point.md)
**tau.goal**: universal patterns
