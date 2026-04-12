---
name: "patterns"
description: "Reusable solution templates."
metadata:
  ο.class: "continuant"
  ο.mode: "independent"
  λ.in: ""
  λ.out: "[orchestrator](integration/orchestrator.md)"
  λ.kin: "[skills](integration/skills.md), [tools](integration/tools.md)"
  τ.goal: "applicability"
---

# Usage Patterns

> Situation → Pattern → Application

## Pattern Catalog

### Simple Learning

**When**: Single concept, moderate depth
**Pipeline**: R1
**Composition**: `learn.parse → learn.execute → learn.emit`

### Research Synthesis

**When**: Multiple sources, integration required
**Pipeline**: R2
**Composition**: `learn ∘ (reason ⊗ graph) ∘ critique`

### Self-Improvement

**When**: Skill/process optimization
**Pipeline**: R3
**Composition**: `learn ∘ learn` (recursive)

### Exam Preparation

**When**: Structured knowledge, retention focus
**Pipeline**: R2
**Domain**: learning
**Composition**: `learn[learning] ∘ assess{EVIDENTIAL}`

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Over-routing | R3 for simple queries | Trust R0/R1 |
| Under-assessment | Skipping assess phase | Always assess |
| Orphan knowledge | No vertex sharing | Force integration |


## See Also

- [../concepts/scale-invariance](concepts/scale-invariance.md)
- [../concepts/pareto-governance](concepts/pareto-governance.md)
- [../concepts/convergence](concepts/convergence.md)
- [../phases/2-route](phases/2-route.md)
- [../meta/routing](meta/routing.md)
- [skills](integration/skills.md)
- [tools](integration/tools.md)
- [orchestrator](integration/orchestrator.md)

## Graph

**λ.out** (enables): [orchestrator](integration/orchestrator.md)
**λ.kin** (related): [skills](integration/skills.md), [tools](integration/tools.md)
**τ.goal**: applicability
