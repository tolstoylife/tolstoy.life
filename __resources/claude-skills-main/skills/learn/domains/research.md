---
name: "research"
description: "Discovery and validation."
metadata:
  ο.class: "continuant"
  ο.mode: "independent"
  λ.in: "[learning](domains/learning.md)"
  λ.out: "[writing](domains/writing.md)"
  λ.kin: "[coding](domains/coding.md)"
  τ.goal: "rigor"
---

# Research Domain

> Literature synthesis, hypothesis generation, evidence evaluation.

## Configuration

| Parameter | Value |
|-----------|-------|
| Primary Lenses | EVIDENTIAL,SCOPE |
| Emphasis | rigor,comprehensiveness |
| Example Trigger | "synthesize findings on X" |

## Lens Weighting

```yaml
lenses:
  STRUCTURAL: 0.15
  EVIDENTIAL: 0.3
  PRAGMATIC: 0.2
  SCOPE: 0.3
  ADVERSARIAL: 0.15
```

## Usage

This domain activates when queries match patterns related to research.

## Customization

Override defaults by specifying in query or context.


## See Also

- [../concepts/vertex-sharing](concepts/vertex-sharing.md)
- [../concepts/metagraph](concepts/metagraph.md)
- [../integration/skills](integration/skills.md)

## Graph

**λ.in** (requires): [learning](domains/learning.md)
**λ.out** (enables): [writing](domains/writing.md)
**λ.kin** (related): [coding](domains/coding.md)
**τ.goal**: rigor
