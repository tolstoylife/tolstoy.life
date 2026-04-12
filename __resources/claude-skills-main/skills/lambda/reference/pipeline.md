# Pipeline Reference (Π, Ψ)

The transformation sequence: `parse → route → execute → validate → emit → compound`

## Routing (Π)

### Complexity Scoring

```python
complexity = (
    domains × 2 +      # How many knowledge areas
    depth × 3 +        # How many reasoning levels
    stakes × 1.5 +     # Consequence of error
    novelty × 2        # Distance from known patterns
)
```

| Factor | 0 | 1 | 2 | 3 |
|--------|---|---|---|---|
| Domains | Single | Two | Three | Four+ |
| Depth | Surface | Mechanism | System | Integration |
| Stakes | Casual | Important | Critical | Irreversible |
| Novelty | Known | Variant | New | Unprecedented |

### Pipeline Selection

| Level | Score | λ-expression | Description |
|-------|-------|--------------|-------------|
| R0 | <2 | `id` | Direct answer, no transformation |
| R1 | <4 | `ρ*` | Single skill, implicit validation |
| R2 | <8 | `(γ ⊗ η) ∘ ρ` | Composed skills, explicit η |
| R3 | ≥8 | `Σ` | Full orchestration, KROG |

### Force Triggers

| Trigger | Route | Rationale |
|---------|-------|-----------|
| "define", "what is" | R0 | Direct factual |
| "quick", "briefly" | R0 | Explicit constraint |
| "explain mechanism" | R2 | Requires depth |
| "compare X and Y" | R2 | Multi-domain |
| "current", "latest" | R3 | Requires verification |
| "comprehensive" | R3 | Full synthesis |
| "verify", "validate" | R3 | Requires evidence |

### Examination Mode

| Trigger | Route | Override |
|---------|-------|----------|
| "SAQ" | R1 | Force ~200 words |
| "viva" | R2 | Force progressive |

## Execution (Ψ)

### Composition Operators

```haskell
-- Sequential: output of first → input of second
(∘) :: (β → γ) → (α → β) → (α → γ)
(f ∘ g) x = f (g x)

-- Parallel: same input → tuple of outputs
(⊗) :: (α → β) → (α → γ) → (α → (β, γ))
(f ⊗ g) x = (f x, g x)

-- Recursive: fixed point iteration
fix :: (α → α) → α
fix f = let x = f x in x

-- Conditional: apply if predicate holds
(|) :: (α → β) → (α → Bool) → (α → Maybe β)
(f | p) x = if p x then Just (f x) else Nothing
```

### Derived Compositions

```haskell
-- Core reasoning cycle
core = ω ∘ θ ∘ ρ           -- ontolog ∘ think ∘ reason

-- Dialectical refinement (iterate until convergence)
refine = fix (β ∘ κ)        -- fix (abduct ∘ critique)

-- Governed execution
govern = χ ∘ ν ∘ α          -- constraints ∘ non-linear ∘ agency

-- Orchestrated analysis
meta = μ ∘ (ι ⊗ η) ∘ γ      -- orchestrator ∘ (analytics ⊗ hierarchical) ∘ graph
```

### Execution by Level

#### R0: Identity
```
τ = ο  -- Direct pass-through
```
No transformation needed. Answer directly.

#### R1: Single Skill
```
τ = ρ.emit(ρ.ground(ρ.reduce(ρ.parse(ο))))
```
Full reasoning skill pipeline, implicit validation.

#### R2: Composition
```
τ = validate[η≥4] ∘ γ ∘ (ρ ⊗ η) $ ο
```
Parallel reasoning and hierarchical decomposition, explicit topology.

#### R3: Full Orchestration
```
τ = χ.KROG ∘ β ∘ κ ∘ (ρ ⊗ θ ⊗ ω) ∘ ν ∘ α $ ο
```
All skills: agency, non-linear, parallel core, critique, abduct, KROG validation.

### Skill Loading

Load skills based on route:

| Route | Skills | Rationale |
|-------|--------|-----------|
| R0 | None | Direct knowledge |
| R1 | reason | Core transformation |
| R2 | reason, graph, hierarchical-reasoning | Structure + scale |
| R3 | All connected | Full orchestration |

### Knowledge Integration (K)

At execution, K is available:

```python
def execute_with_K(query, skills, K):
    # 1. Find relevant learnings
    context = retrieve_relevant(K, query)
    
    # 2. Execute with augmented context
    result = compose(skills)(query + context)
    
    # 3. Return for validation
    return result
```

## Escalation/De-escalation

### Escalate When

- Validation fails at current level
- User requests more depth
- Confidence below threshold
- Novel situation detected

### De-escalate When

- Time constraint
- User requests brevity
- Simple follow-up to complex answer
- Exam mode with word limits

## Pipeline Visualization

```
     ┌─────────────────────────────────────────────────────────────┐
     │                          λ(ο,K).τ                           │
     └─────────────────────────────────────────────────────────────┘
                                   │
     ┌─────────────────────────────┼─────────────────────────────┐
     │                             ▼                             │
     │  ┌──────┐   ┌───────┐   ┌─────────┐   ┌──────────┐   ┌────┐│
ο ───┼─►│ parse│──►│ route │──►│execute(K)│──►│ validate │──►│emit││──► τ
     │  └──────┘   └───────┘   └─────────┘   └──────────┘   └────┘│
     │                             │               │              │
     │                             ▼               ▼              │
     │                         K (query)      η, KROG             │
     │                                                            │
     └────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
                            ┌──────────┐
                        τ ──┤ compound │──► K'
                            └──────────┘
```

## Error Handling

| Error | Response |
|-------|----------|
| Parse failure | Clarify query |
| Route uncertain | Default R2 |
| Execution failure | Retry with R+1 |
| Validation failure | Remediate, re-validate |
| Emit constraint violation | Adjust format |
