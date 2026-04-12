# Category-Theoretic Constraint Composition

*Constraints as functors and their algebraic structure*

## Constraints as Functors

A constraint C is a functor between categories:

```
C : 𝒞_context × 𝒞_action → 𝒞_deontic
```

Where:
- 𝒞_context = Category of structural contexts (simplicial complexes)
- 𝒞_action = Category of actions/states
- 𝒞_deontic = Category of deontic modalities

### Functor Laws

For C to be a valid constraint functor:

```
C(id_σ, id_a) = id_δ                     [Identity]
C(f ∘ g, h ∘ k) = C(f,h) ∘ C(g,k)        [Composition]
```

### Objects and Morphisms

**In 𝒞_context**:
- Objects: Simplicial complexes Σ representing structural context
- Morphisms: Structure-preserving maps (simplicial maps)

**In 𝒞_action**:
- Objects: Actions or states a ∈ A
- Morphisms: Action refinements or state transitions

**In 𝒞_deontic**:
- Objects: Deontic statuses {P, O, F, I, ?}
- Morphisms: Deontic entailments (O → P, etc.)

## Constraint Categories

### The Category **Constr**

- **Objects**: Constraints C : (Σ × A) → Δ
- **Morphisms**: Constraint transformations τ : C₁ ⇒ C₂
- **Identity**: Trivial transformation id_C
- **Composition**: Vertical composition of transformations

A morphism τ : C₁ ⇒ C₂ is a natural transformation satisfying:
```
∀σ,a. τ_σ,a : C₁(σ,a) → C₂(σ,a)
```

### Constraint Monad

Constraints form a monad (C, η, μ) where:

```
η : Id → C        [Unit: trivial permission]
μ : C ∘ C → C     [Multiplication: constraint composition]
```

**Monad laws**:
```
μ ∘ (η ∘ C) = id_C       [Left identity]
μ ∘ (C ∘ η) = id_C       [Right identity]
μ ∘ (μ ∘ C) = μ ∘ (C ∘ μ) [Associativity]
```

## Composition Operations

### Sequential Composition (;)

Apply constraints in sequence:

```
C₁ ; C₂ = λσ.λa. compose(C₁(σ,a), C₂(σ,a))

Where compose(δ₁, δ₂) follows lattice ordering:
  F > O > P > ?
  I overrides all
```

**Semantics**: Both constraints must be satisfied.

### Parallel Composition (⊗)

Apply independent constraints:

```
C₁ ⊗ C₂ = λσ.λ(a₁,a₂). (C₁(σ,a₁), C₂(σ,a₂))
```

**Semantics**: Constraints apply to different action components.

### Choice Composition (+)

Alternative constraints (coproduct):

```
C₁ + C₂ = λσ.λa. C₁(σ,a) ∨ C₂(σ,a)
```

**Semantics**: Satisfying either constraint is sufficient.

### Conditional Composition (→)

Implication between constraints:

```
C₁ → C₂ = λσ.λa. C₁(σ,a) implies C₂(σ,a)
```

**Semantics**: If C₁ permits, then C₂ must permit.

## Constraint Algebra

Constraints form a **Heyting algebra** under:

```
Top (⊤):    λσ.λa. P(a)      [Universal permission]
Bottom (⊥): λσ.λa. F(a)      [Universal prohibition]
Meet (∧):   C₁ ∧ C₂ = C₁ ; C₂
Join (∨):   C₁ ∨ C₂ = C₁ + C₂
Implication (→): As defined above
```

### Lattice Properties

```
C ∧ ⊤ = C           [Top identity]
C ∨ ⊥ = C           [Bottom identity]
C ∧ C = C           [Idempotence]
C ∧ (C ∨ D) = C     [Absorption]
```

## Polymorphisms and CSP

Constraints relate to Constraint Satisfaction Problems (CSP) via polymorphisms.

A **polymorphism** of constraint C is an operation f such that:
```
∀a₁,...,aₙ ∈ domain(C). C(f(a₁,...,aₙ)) follows from C(a₁),...,C(aₙ)
```

**Dichotomy theorem**: CSP(C) is either polynomial-time or NP-complete, determined by polymorphism structure.

## Right Kan Extension

Constraints can be extended along functors via Kan extension:

```
Ran_F(C) = ∫_c [𝒞(Fc, -), C(c)]
```

This allows extending a constraint defined on a subcategory to the full category.

## Sheaf-Theoretic View

Constraints form a **presheaf** on the context category:

```
C : 𝒞_context^op → Set
C(σ) = {a | C(σ,a) ∈ {P,O}}  [Permitted actions in context σ]
```

For restriction maps:
```
C(f)(a) = a|_σ'   where f : σ' → σ
```

The **sheaf condition** ensures local-to-global consistency:
```
If ∀σᵢ. C(σᵢ,a|_σᵢ) = P, then C(⋃σᵢ, a) = P
```

## Constraint Diagrams

### Commutative Squares

A constraint respects structural morphisms:

```
     σ ──f──→ σ'
     │         │
  C  ↓         ↓ C
     │         │
  C(σ)──→ C(σ')
```

### Pullback Constraints

Combine constraints via pullback:

```
       C₁ ×_D C₂
        ╱    ╲
    π₁ ↙      ↘ π₂
      C₁        C₂
        ╲    ╱
         ↘  ↙
          D
```

The pullback constraint requires both C₁ and C₂ to agree on shared deontic outcomes.

## Implementation Patterns

### Functor Pattern (Haskell-style)

```haskell
class ConstraintFunctor c where
  cmap :: (a -> b) -> c a -> c b
  
instance ConstraintFunctor DeonticConstraint where
  cmap f (Permit a) = Permit (f a)
  cmap f (Oblige a) = Oblige (f a)
  cmap f (Forbid a) = Forbid (f a)
```

### Monad Pattern

```haskell
instance Monad ConstraintMonad where
  return a = Permit a  -- η
  (Permit a) >>= f = f a
  (Oblige a) >>= f = strengthen (f a)
  (Forbid a) >>= f = Forbid a
```

### Applicative Composition

```haskell
(<*>) :: Constraint (a -> b) -> Constraint a -> Constraint b
(Permit f) <*> (Permit a) = Permit (f a)
(Oblige f) <*> ca = Oblige (f <$> ca)
(Forbid _) <*> _ = Forbid ()
```

## Type-Level Constraints

In dependently-typed systems:

```
Constraint : Context → Action → Deontic → Type

-- A proof that action a is permitted in context σ
data Permitted (σ : Context) (a : Action) where
  MkPermit : C(σ,a) = P → Permitted σ a

-- Composition preserves well-typing
compose : Permitted σ a → Permitted σ b → Permitted σ (a ∧ b)
```

## Categorical Products of Constraints

The product of constraint categories:

```
C₁ × C₂ : (Σ × A) → (Δ × Δ)

With projections:
  π₁ : (C₁ × C₂) → C₁
  π₂ : (C₁ × C₂) → C₂
```

And exponentials:

```
C^D : (Σ × A) → (Δ^Δ)

(C^D)(σ,a)(d) = C(σ, a | D(σ,a) = d)
```

## Grothendieck Construction

Constraints as fibrations:

```
∫C → 𝒞_context

Where ∫C has:
  Objects: (σ, a) with C(σ,a) ∈ {P,O}
  Morphisms: (f,g) : (σ,a) → (σ',a') with constraint-respecting maps
```

This construction integrates context variation with constraint satisfaction.

---

**Further reading**: Mac Lane (1971), Awodey (2010), Borceux (1994), Zhuk (2020)
