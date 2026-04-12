---
name: "custom"
description: "Domain adaptation and specialization."
metadata:
  ο.class: "continuant"
  ο.mode: "dependent"
  λ.in: ""
  λ.out: ""
  λ.kin: "[meta](domains/meta.md)"
  τ.goal: "extensibility"
---

# Custom Domain

> User-defined domain with configurable parameters.

## Configuration

| Parameter | Value |
|-----------|-------|
| Primary Lenses | configurable |
| Emphasis | user-defined |
| Example Trigger | "configure for domain Z" |

## Lens Weighting

```yaml
lenses:
  STRUCTURAL: 0.15
  EVIDENTIAL: 0.2
  PRAGMATIC: 0.2
  SCOPE: 0.15
  ADVERSARIAL: 0.15
```

## Usage

This domain activates when queries match patterns related to custom.

## Customization

Override defaults by specifying in query or context.


## See Also

- [../meta/governance](meta/governance.md)
- [../integration/patterns](integration/patterns.md)
- [../schema.yaml](schema.yaml)

## Graph

**λ.kin** (related): [meta](domains/meta.md)
**τ.goal**: extensibility
