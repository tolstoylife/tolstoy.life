---
name: "skills"
description: "Skill composition and orchestration."
metadata:
  ο.class: "continuant"
  ο.mode: "dependent"
  λ.in: ""
  λ.out: "[orchestrator](integration/orchestrator.md)"
  λ.kin: "[tools](integration/tools.md), [patterns](integration/patterns.md)"
  τ.goal: "interface compatibility"
---

# Skill Integrations

> learn ⊗ skills → enhanced capability

## Integrated Skills

| Skill | Composition | Use When |
|-------|-------------|----------|
| reason | learn ∘ reason | Deep decomposition needed |
| think | learn ⊗ think | Mental models useful |
| critique | learn ∘ critique | Validation required |
| graph | learn ∘ graph | Structure extraction |

## Composition Operators

```haskell
(∘) :: sequential composition
(⊗) :: parallel composition  
fix :: recursive application
(|) :: conditional activation
```

## Example: Research Pipeline

```
research_query 
  |> learn.parse
  |> (reason ⊗ think)      -- Parallel reasoning
  |> critique              -- Dialectical validation
  |> graph                 -- Structure extraction
  |> learn.compound        -- Knowledge integration
```


## See Also

- [../concepts/homoiconicity](concepts/homoiconicity.md)
- [../concepts/scale-invariance](concepts/scale-invariance.md)
- [../concepts/metagraph](concepts/metagraph.md)
- [../phases/3-execute](phases/3-execute.md)
- [../meta/governance](meta/governance.md)
- [tools](integration/tools.md)
- [patterns](integration/patterns.md)
- [orchestrator](integration/orchestrator.md)

## Graph

**λ.out** (enables): [orchestrator](integration/orchestrator.md)
**λ.kin** (related): [tools](integration/tools.md), [patterns](integration/patterns.md)
**τ.goal**: interface compatibility
