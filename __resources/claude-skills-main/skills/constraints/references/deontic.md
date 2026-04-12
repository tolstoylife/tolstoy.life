# Deontic Logic Reference

*Formal semantics for normative reasoning*

## Standard Deontic Logic (SDL)

### Primitive Operators

| Operator | Symbol | Reading | Semantics |
|----------|--------|---------|-----------|
| Obligation | O(φ) | "It ought to be that φ" | φ holds in all deontically ideal worlds |
| Permission | P(φ) | "It is permitted that φ" | φ holds in some deontically ideal world |
| Prohibition | F(φ) | "It is forbidden that φ" | φ fails in all deontically ideal worlds |

### Interdefinitions

```
P(φ) ≡ ¬O(¬φ)     Permission = not obligated to refrain
F(φ) ≡ O(¬φ)      Prohibition = obligated to refrain
F(φ) ≡ ¬P(φ)      Prohibition = not permitted
```

### Axiom Schemas

**D-axiom** (consistency of obligations):
```
O(φ) → P(φ)       Ought implies may
¬O(⊥)             Obligations are consistent
```

**K-axiom** (distribution):
```
O(φ → ψ) → (O(φ) → O(ψ))
```

**Necessitation** (for tautologies):
```
If ⊢ φ then ⊢ O(φ)
```

### Kripke Semantics

A deontic frame is a tuple ⟨W, R, V⟩ where:
- W = set of possible worlds
- R ⊆ W × W = deontic accessibility relation
- V : Prop → P(W) = valuation function

**Satisfaction conditions**:
```
w ⊨ O(φ) iff ∀v. (wRv → v ⊨ φ)
w ⊨ P(φ) iff ∃v. (wRv ∧ v ⊨ φ)
w ⊨ F(φ) iff ∀v. (wRv → v ⊭ φ)
```

### Resolution Matrix Semantics (RMS)

Alternative semantic foundation using normative values:

| Value | Symbol | Meaning |
|-------|--------|---------|
| Mandatory | m | Must occur |
| Indifferent | i | May or may not occur |
| Forbidden | b | Must not occur |

**Resolution ordering**: m > i > b

## Multi-Agent Deontic Logic

Subscripted operators for agent-relative norms:

```
Oᵢ(φ)     Agent aᵢ is obligated to φ
Pᵢ(φ)     Agent aᵢ is permitted to φ
Fᵢ(φ)     Agent aᵢ is forbidden from φ
```

**Directed obligations**:
```
O(i,j,φ)  Agent i is obligated toward j to φ
```

## Dynamic Deontic Logic

Actions that change normative states:

```
[α]O(φ)   After action α, φ is obligated
⟨α⟩P(φ)   Action α can lead to φ being permitted
```

## Temporal Deontic Logic

Combining temporal and deontic modalities:

```
□O(φ)     Always obligated to φ (standing obligation)
◇P(φ)     Eventually permitted to φ
O(φ) U ψ  Obligated to φ until ψ occurs
```

## Common Paradoxes and Solutions

### Ross's Paradox
From O(mail-letter) we can derive O(mail-letter ∨ burn-letter).

**Solution**: Distinguish between strong and weak obligation.

### Contrary-to-Duty Obligations
"If you steal, you ought to repay" creates issues with O(¬steal).

**Solution**: Preference-based or dyadic deontic logic:
```
O(repay | steal)    Conditional obligation
```

### Free Choice Permission
From P(tea ∨ coffee), can we infer P(tea)?

**Solution**: Strong permission as explicit granting vs weak permission as absence of prohibition.

## Dyadic Deontic Logic

Conditional obligations with explicit contexts:

```
O(φ | ψ)    φ is obligated given condition ψ
P(φ | ψ)    φ is permitted given condition ψ
```

**Semantics**: In all ψ-worlds that are deontically ideal, φ holds.

## Connection to Alethic Modality

| Deontic | Alethic | Relationship |
|---------|---------|--------------|
| O(φ) | □φ | Normative necessity vs logical necessity |
| P(φ) | ◇φ | Normative possibility vs logical possibility |
| F(φ) | ¬◇φ | Normative impossibility |
| I(φ) | ¬◇φ | Absolute impossibility |

**Key difference**: Deontic ideality ≠ logical necessity. What ought to be is not what must be.

## Inference Rules

```
O(φ) ∧ O(ψ)  ⊢  O(φ ∧ ψ)         Agglomeration
O(φ → ψ) ∧ O(φ)  ⊢  O(ψ)         Detachment
P(φ) ∧ (φ → ψ)  ⊢  P(ψ)          Permission closure (controversial)
```

## Deontic Logic Programs

For computational implementation:

```prolog
% Obligation inference
obligated(Agent, Action) :- 
    duty(Agent, Action),
    not exempted(Agent, Action).

% Permission check
permitted(Agent, Action) :-
    not forbidden(Agent, Action).

% Prohibition inference
forbidden(Agent, Action) :-
    rule(prohibits, _, Action),
    applies_to(Agent, rule).
```

---

**Further reading**: von Wright (1951), Chellas (1980), Makinson (1999), Governatori (2015)
