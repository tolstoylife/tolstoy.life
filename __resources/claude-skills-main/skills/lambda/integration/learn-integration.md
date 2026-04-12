# Learn Skill Integration

> How λ (lambda-skill) and Learn work together

## Relationship

```
λ(ο,K).τ         ─────────────────>  λ(ο,Κ,Σ).τ'
(lambda-skill)    extends to          (Learn)

Lambda: 6 stages   →   Learn: 7 stages (adds Assess, Refactor, Renormalize)
Lambda: K evolves  →   Learn: K + Σ evolve (schema evolution)
```

## Shared Invariants

| Invariant | Lambda | Learn |
|-----------|--------|-------|
| Topology | η ≥ target (4.0 default) | η ≥ 4 |
| Vertex-sharing | `shared(new, K) ≠ ∅` | `shared_vertices ≠ ∅` |
| K-monotonicity | `K' ⊇ K` | `len(Κ') ≥ len(Κ)` |
| KROG governance | K ∧ R ∧ O ∧ G | Via meta/governance.md |

## When to Use Each

| Scenario | Use | Rationale |
|----------|-----|-----------|
| Query routing | Lambda | R0-R3 complexity classification |
| Response generation | Lambda | Pipeline: parse→route→execute→validate→emit |
| Post-session reflection | Learn | Full 7-phase with Assess→Refactor→Renormalize |
| Skill improvement | Learn | Schema evolution (Σ→Σ') |
| Knowledge crystallization | Either | Both have compound phases |
| Examination mode | Lambda | SAQ/VIVA templates |

## Composition Patterns

### Sequential (λ → Learn)
```haskell
-- Lambda handles query, Learn handles post-processing
response = λ(query, K).τ
(K', Σ') = Learn.renormalize ∘ Learn.compound ∘ Learn.assess $ response
```

### Parallel (λ ⊗ Learn)
```haskell
-- Both active: Lambda for response, Learn for meta-learning
(τ, K_λ) = λ(query, K).τ
(τ', K_L, Σ') = Learn(meta_query, K, Σ).τ'
K_final = K_λ ∪ K_L
```

### Recursive (Learn(λ))
```haskell
-- Learn improves Lambda itself (skill self-improvement)
improved_lambda = Learn("improve λ routing", K, Σ).τ'
```

## Shared Concepts Cross-Reference

| Concept | Lambda Location | Learn Location |
|---------|-----------------|----------------|
| Compound loop | reference/compound.md | phases/6-compound.md |
| Topology validation | reference/topology.md | concepts/topology-invariants.md |
| Vertex-sharing | Vertex-Sharing section | concepts/vertex-sharing.md |
| Convergence | Implicit in compound | concepts/convergence.md |
| Knowledge monotonicity | K' ⊇ K invariant | concepts/knowledge-monotonicity.md |

## Integration Points

### From Lambda to Learn

1. **After compound stage**: Lambda can hand off to Learn for deeper reflection
2. **On R3 queries**: High-complexity queries may benefit from Learn's assessment
3. **Post-examination**: After SAQ/VIVA, Learn captures examination insights

### From Learn to Lambda

1. **Routing decisions**: Learn can inform Lambda's complexity classification
2. **Schema updates**: Learn evolves Σ which affects Lambda's pipeline behavior
3. **Knowledge injection**: Learn's crystallized K feeds into Lambda's execute(K)

## Example: Full Integration Flow

```
User Query: "Explain hypertensive crisis management"
    │
    ▼
┌──────────────────────────────────────────────────┐
│ λ(ο,K).τ                                         │
│   parse → route(R2) → execute(K) → validate → emit│
│   └── Uses K from previous Learn sessions         │
└──────────────────────────────────────────────────┘
    │
    ▼ Response delivered
    │
┌──────────────────────────────────────────────────┐
│ Learn(reflect, K, Σ).τ'                          │
│   assess → refactor → compound → renormalize     │
│   └── Extracts new vertices, updates Σ           │
└──────────────────────────────────────────────────┘
    │
    ▼ K' and Σ' available for next query
```

## Anti-Patterns

| Pattern | Why Harmful | Fix |
|---------|-------------|-----|
| Using Learn for simple queries | Overhead without benefit | Use Lambda R0-R1 |
| Skipping Lambda's validate | Unchecked η, KROG violations | Always include validate |
| Learn without vertex-sharing | Orphan knowledge | Ensure shared_vertices ≠ ∅ |
| Parallel without merge | Fragmented K | Always K_final = K_λ ∪ K_L |
