---
name: "learning"
description: "Knowledge acquisition and skill development."
metadata:
  ο.class: "continuant"
  ο.mode: "independent"
  λ.in: ""
  λ.out: "[research](domains/research.md), [meta](domains/meta.md)"
  λ.kin: "[coding](domains/coding.md), [writing](domains/writing.md)"
  τ.goal: "progressive mastery"
---

# Learning Domain

> Exam preparation, concept acquisition, structured knowledge building.

## Configuration

| Parameter | Value |
|-----------|-------|
| Primary Lenses | EVIDENTIAL,STRUCTURAL |
| Emphasis | retention,accuracy |
| Example Trigger | "explain cardiac output" |

## Lens Weighting

```yaml
lenses:
  STRUCTURAL: 0.3
  EVIDENTIAL: 0.3
  PRAGMATIC: 0.2
  SCOPE: 0.15
  ADVERSARIAL: 0.15
```

## Usage

This domain activates when queries match patterns related to learning.

## Customization

Override defaults by specifying in query or context.


## See Also

- [../concepts/knowledge-monotonicity](concepts/knowledge-monotonicity.md)
- [../concepts/compound-interest](concepts/compound-interest.md)
- [../integration/patterns](integration/patterns.md)

## Graph

**λ.out** (enables): [research](domains/research.md), [meta](domains/meta.md)
**λ.kin** (related): [coding](domains/coding.md), [writing](domains/writing.md)
**τ.goal**: progressive mastery
