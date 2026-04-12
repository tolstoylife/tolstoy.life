---
name: "coding"
description: "Software creation and automation."
metadata:
  ο.class: "continuant"
  ο.mode: "independent"
  λ.in: ""
  λ.out: ""
  λ.kin: "[writing](domains/writing.md), [research](domains/research.md)"
  τ.goal: "correctness"
---

# Coding Domain

> Software development, debugging, architecture design.

## Configuration

| Parameter | Value |
|-----------|-------|
| Primary Lenses | STRUCTURAL,PRAGMATIC |
| Emphasis | correctness,maintainability |
| Example Trigger | "implement rate limiter" |

## Lens Weighting

```yaml
lenses:
  STRUCTURAL: 0.3
  EVIDENTIAL: 0.2
  PRAGMATIC: 0.3
  SCOPE: 0.15
  ADVERSARIAL: 0.15
```

## Usage

This domain activates when queries match patterns related to coding.

## Customization

Override defaults by specifying in query or context.


## See Also

- [../concepts/topology-invariants](concepts/topology-invariants.md)
- [../concepts/path-optimization](concepts/path-optimization.md)
- [../integration/tools](integration/tools.md)

## Graph

**λ.kin** (related): [writing](domains/writing.md), [research](domains/research.md)
**τ.goal**: correctness
