# Primitives

<purpose>
Type definitions for λ-calculus over simplicial complexes. All structures are holarchic—simultaneously wholes and parts.
</purpose>

---

## Lambda Calculus Core

<lambda_types>

```
TYPE HIERARCHY
──────────────
Term ::= Variable | Abstraction | Application

Variable    ::= ο                    — Base/grounding
Abstraction ::= λο.τ                 — Operation binding base to terminal
Application ::= (λ τ)                — Applying operation to argument

NOTATION
────────
ο (omicron) : Base variable
τ (tau)     : Terminal variable
λ (lambda)  : Operation/abstraction
Σ (sigma)   : Simplicial complex
H (eta)     : Holon
```

</lambda_types>

<reduction_rules>

```
β-REDUCTION
───────────
(λο.τ) a → τ[ο := a]

Substitute base with argument, yielding terminal.

η-REDUCTION
───────────
λο.(λ ο) → λ   (when ο not free in λ)

Extensional equivalence.

COMPOSITION
───────────
(λ₁ ∘ λ₂) = λο.λ₁(λ₂(ο))

Sequential application.
```

</reduction_rules>

---

## Base Type ο

<definition>
The grounded entity. Input to operations. Vertex in simplicial complex.
</definition>

<schema>

| Field | Type | Semantics |
|-------|------|-----------|
| `id` | String | Unique identifier |
| `σ_membership` | Set[Simplex] | Containing simplices |
| `properties` | Map[String, Value] | Lex property values |

</schema>

<identity_criterion>
```
ο₁ = ο₂ iff σ_membership(ο₁) = σ_membership(ο₂)
```
Identity through structural position, not intrinsic properties.
</identity_criterion>

<syntax>
```
base ο₁
base ο₂ : TypeLabel
base ο₃ { property: value }
```
</syntax>

---

## Terminal Type τ

<definition>
The target purpose. Output of operations. Attractor in dynamical system.
</definition>

<schema>

| Field | Type | Semantics |
|-------|------|-----------|
| `id` | String | Unique identifier |
| `reachable_from` | Set[ο] | Bases that can reach this terminal |
| `persistence` | Float | Topological significance |

</schema>

<reachability>
```
reach(ο, τ) iff ∃λ₁...λₙ. λₙ(...λ₁(ο)...) = τ
```
</reachability>

<syntax>
```
terminal τ₁
terminal τ₂ : Purpose
terminal τ₃ { persistence: 0.95 }
```
</syntax>

---

## Operation Type λ

<definition>
The transformation. Edge in simplicial complex. Maps bases toward terminals.
</definition>

<schema>

| Field | Type | Semantics |
|-------|------|-----------|
| `id` | String | Unique identifier |
| `domain` | Set[ο] | Valid inputs |
| `codomain` | Set[ο ∪ τ] | Possible outputs |
| `path` | List[ο] | Intermediate vertices |
| `confidence` | Float[0,1] | Operational certainty |

</schema>

<properties>

| Property | Formalization |
|----------|---------------|
| Composable | `λ₁ ∘ λ₂` is defined when `codomain(λ₂) ⊆ domain(λ₁)` |
| Typed | `λ : ο → τ` specifies signature |
| Weighted | `weight(λ) = confidence × persistence` |

</properties>

<syntax>
```
lambda λ₁ : ο₁ → τ₁
lambda λ₂ : ο₂ → ο₃ → τ₂ { confidence: 0.9 }
lambda λ₃ = compose(λ₁, λ₂)
```
</syntax>

---

## Simplicial Complex Σ

<definition>
The ambient space. Collection of simplices closed under taking faces.
</definition>

<schema>

| Field | Type | Semantics |
|-------|------|-----------|
| `vertices` | Set[ο] | 0-simplices |
| `simplices` | Set[Simplex] | All k-simplices |
| `boundary` | Map[σ, Set[σ]] | Boundary operator |

</schema>

<simplex_definition>
```
k-SIMPLEX σₖ
────────────
σₖ = [v₀, v₁, ..., vₖ]

Ordered set of k+1 vertices.

FACE CONDITION
──────────────
σ ∈ Σ ⟹ ∀ face f of σ. f ∈ Σ

BOUNDARY OPERATOR
─────────────────
∂ₖ(σₖ) = Σᵢ (-1)ⁱ [v₀, ..., v̂ᵢ, ..., vₖ]

where v̂ᵢ means omit vᵢ.
```
</simplex_definition>

<chain_complex>
```
... →∂ₙ₊₁ Cₙ →∂ₙ Cₙ₋₁ →∂ₙ₋₁ ... →∂₁ C₀ → 0

where:
  Cₖ = free abelian group on k-simplices
  ∂ₖ = boundary operator
  ∂ₖ ∘ ∂ₖ₊₁ = 0  (boundary of boundary is empty)
```
</chain_complex>

---

## Holon Type H

<definition>
Self-similar structure. Simultaneously whole and part. Recursive composition.
</definition>

<schema>

| Field | Type | Semantics |
|-------|------|-----------|
| `id` | String | Unique identifier |
| `sub_holons` | Set[H] | Contained holons (as whole) |
| `super_holon` | Optional[H] | Containing holon (as part) |
| `complex` | Σ | Local simplicial structure |
| `operations` | Set[λ] | Local transformations |
| `terminals` | Set[τ] | Local purposes |

</schema>

<holarchic_laws>
```
COMPOSITION LAW
───────────────
H = ⊕ᵢ hᵢ  (holon is sum of sub-holons)

EMBEDDING LAW
─────────────
H ↪ H'     (holon embeds in super-holon)

SELF-SIMILARITY
───────────────
structure(H) ≅ structure(hᵢ)

Same structural patterns at every scale.
```
</holarchic_laws>

<syntax>
```
holon H₁ {
    sub_holons: [h₁, h₂, h₃]
    operations: [λ₁, λ₂]
    terminals: [τ₁]
}

holon H₂ extends H₁ {
    super_holon: H_parent
}
```
</syntax>

---

## Persistence Diagram

<definition>
Multi-scale topological summary. Captures birth-death of features across filtration.
</definition>

<schema>

| Field | Type | Semantics |
|-------|------|-----------|
| `dimension` | Int | Homology dimension (0, 1, 2, ...) |
| `points` | Set[(birth, death)] | Feature lifespans |
| `persistence` | Float | Maximum lifespan |

</schema>

<interpretation>
```
DIMENSION 0 (H₀)
────────────────
Connected components.
Birth: component appears
Death: components merge

DIMENSION 1 (H₁)
────────────────
Loops/cycles.
Birth: loop forms
Death: loop fills in

DIMENSION 2 (H₂)
────────────────
Voids/cavities.
Birth: void forms
Death: void fills in
```
</interpretation>

---

## Built-in Functions

<core_operations>

| Function | Signature | Semantics |
|----------|-----------|-----------|
| `apply` | λ × ο → ο ∪ τ | Apply operation to base |
| `compose` | λ × λ → λ | Sequential composition |
| `parallel` | λ × λ → λ | Parallel composition |
| `fix` | λ → λ | Recursive fixpoint |

</core_operations>

<topological_operations>

| Function | Signature | Semantics |
|----------|-----------|-----------|
| `boundary` | σₖ → Chain[σₖ₋₁] | Boundary operator |
| `homology` | Σ × k → Hₖ | k-th homology group |
| `persistence` | Σ × Filtration → Diagram | Persistence diagram |
| `betti` | Σ × k → Int | k-th Betti number |

</topological_operations>

<holonic_operations>

| Function | Signature | Semantics |
|----------|-----------|-----------|
| `decompose` | H → Set[H] | Extract sub-holons |
| `embed` | H × H → H | Embed in super-holon |
| `scale` | H × Int → H | View at scale level |
| `similarity` | H × H → Float | Structural similarity |

</holonic_operations>
