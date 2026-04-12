# Hohfeldian Rights Analysis

*Fundamental jural relations from Wesley Newcomb Hohfeld (1913, 1917)*

## Overview

Hohfeld identified eight fundamental legal/normative positions that form the atomic vocabulary for all rights discourse. These divide into two squares of four positions each.

## First-Order Positions (Conduct)

Concern what agents **may, must, or cannot do**.

### The Square

```
    CLAIM ←────correlative────→ DUTY
       ↑                          ↑
    opposite                   opposite
       ↓                          ↓
   NO-RIGHT ←──correlative────→ PRIVILEGE
```

### Definitions

**Claim-right**: X has a claim against Y that Y φ
- Meaning: Y owes X the performance of φ
- Example: "Alice has a claim that Bob repay the loan"
- Constraint type: GOVERNING

**Duty**: Y has a duty to X to φ
- Meaning: Y is bound to perform φ for X's benefit
- Example: "Bob has a duty to Alice to repay the loan"
- Constraint type: GOVERNING

**Privilege** (Liberty): X has a privilege to φ
- Meaning: X has no duty to refrain from φ
- Example: "Alice has a privilege to walk on public land"
- Constraint type: ENABLING

**No-right**: Y has no-right that X not φ
- Meaning: Y cannot demand X refrain from φ
- Example: "Bob has no-right that Alice not walk on public land"
- Constraint type: ENABLING

### Formal Relations

```
Claim(X, Y, φ)  ⟺  Duty(Y, X, φ)           [Correlative]
Claim(X, Y, φ)  ⟺  ¬NoRight(X, Y, φ)       [Opposite]
Privilege(X, φ) ⟺  ¬Duty(X, ¬φ)            [Definition]
Privilege(X, φ) ⟺  NoRight(others, X, φ)   [Correlative]
```

## Second-Order Positions (Normative Change)

Concern who **can change** first-order positions.

### The Square

```
    POWER ←────correlative────→ LIABILITY
       ↑                           ↑
    opposite                    opposite
       ↓                           ↓
  DISABILITY ←─correlative────→ IMMUNITY
```

### Definitions

**Power**: X has power to change Y's normative position
- Meaning: X can perform an act that alters Y's rights/duties
- Example: "The employer has power to terminate employment"
- Constraint type: ENABLING

**Liability**: Y is liable to having position changed by X
- Meaning: Y's position can be altered by X's exercise of power
- Example: "The employee is liable to dismissal"
- Constraint type: GOVERNING

**Immunity**: X is immune from Y changing X's position
- Meaning: Y cannot alter X's normative situation
- Example: "Citizens are immune from ex post facto laws"
- Constraint type: CONSTITUTIVE

**Disability**: Y is disabled from changing X's position
- Meaning: Y lacks power to alter X's normative situation
- Example: "Parliament is disabled from abolishing habeas corpus"
- Constraint type: CONSTITUTIVE

### Formal Relations

```
Power(X, Y, ψ)     ⟺  Liability(Y, X, ψ)      [Correlative]
Power(X, Y, ψ)     ⟺  ¬Disability(X, Y, ψ)    [Opposite]
Immunity(X, Y, ψ)  ⟺  Disability(Y, X, ψ)     [Correlative]
Immunity(X, Y, ψ)  ⟺  ¬Liability(X, Y, ψ)     [Opposite]
```

## Full Opposition Table

| Position A | Opposite | Correlative |
|------------|----------|-------------|
| Claim | No-right | Duty |
| Duty | Privilege | Claim |
| Privilege | Duty | No-right |
| No-right | Claim | Privilege |
| Power | Disability | Liability |
| Liability | Immunity | Power |
| Immunity | Liability | Disability |
| Disability | Power | Immunity |

## Mapping to Deontic Operators

| Hohfeldian | Deontic | Relationship |
|------------|---------|--------------|
| Claim(X,Y,φ) | O_Y(φ) | Y is obligated to φ |
| Duty(Y,X,φ) | O_Y(φ) | Y is obligated to φ |
| Privilege(X,φ) | P(φ) ∧ ¬O(φ) | Permitted but not required |
| No-right(Y,X,φ) | ¬O_X(¬φ) | X not obligated to refrain |
| Power | Meta-operator | Changes deontic state |
| Immunity | I(change) | Impossible to change |

## Compound Rights

Most rights in practice are **molecular**—compounds of atomic positions:

**Property right** (in rem):
```
Property(X, object) = ∀Y≠X. [
    Claim(X, Y, non-interference) ∧
    Privilege(X, use) ∧
    Power(X, transfer) ∧
    Immunity(X, Y, expropriation)
]
```

**Contract right** (in personam):
```
Contract(X, Y, performance) = 
    Claim(X, Y, performance) ∧
    Power(X, waive) ∧
    Power(X, assign)
```

**Constitutional right**:
```
Constitutional(X, right) =
    Immunity(X, state, infringement) ∧
    Claim(X, state, protection)
```

## Incidents and Correlatives Matrix

```
┌─────────────────────────────────────────────────────────┐
│              HOHFELDIAN CORRELATIVE MATRIX              │
├───────────┬───────────┬───────────────┬─────────────────┤
│ Holder    │ Position  │ Correlative   │ Other Party     │
├───────────┼───────────┼───────────────┼─────────────────┤
│ X         │ Claim     │ ←→            │ Y has Duty      │
│ X         │ Privilege │ ←→            │ Y has No-right  │
│ X         │ Power     │ ←→            │ Y has Liability │
│ X         │ Immunity  │ ←→            │ Y has Disability│
└───────────┴───────────┴───────────────┴─────────────────┘
```

## Inference Rules

### Correlative Introduction/Elimination
```
Claim(X, Y, φ)
─────────────── CORR-INTRO
Duty(Y, X, φ)

Duty(Y, X, φ)
─────────────── CORR-ELIM
Claim(X, Y, φ)
```

### Opposite Contradiction
```
Claim(X, Y, φ) ∧ NoRight(X, Y, φ)
─────────────────────────────────── OPP-⊥
⊥
```

### Power Exercise
```
Power(X, Y, ψ)   Act(X, exercise(ψ))
────────────────────────────────────── POWER-EX
NewPosition(Y, ψ)
```

### Immunity Shield
```
Immunity(X, Y, ψ)   Attempts(Y, change(X, ψ))
───────────────────────────────────────────── IMM-SHIELD
¬Changed(X, ψ)
```

## Temporal Dynamics

Positions can change over time:

```
Power(X, Y, ψ) ∧ Exercise(X, ψ, t₀) → 
    ¬Liability(Y, X, ψ)@t₁ ∧ Duty(Y, X, φ)@t₁

(Contract creates new duties upon exercise of power)
```

## Computational Representation

```python
@dataclass
class HohfeldianPosition:
    holder: Agent
    position_type: Literal['claim', 'duty', 'privilege', 'no_right',
                           'power', 'liability', 'immunity', 'disability']
    counterparty: Optional[Agent]  # None for in-rem
    content: Action | State
    
    def correlative(self) -> 'HohfeldianPosition':
        """Return the correlative position."""
        corr_map = {
            'claim': 'duty', 'duty': 'claim',
            'privilege': 'no_right', 'no_right': 'privilege',
            'power': 'liability', 'liability': 'power',
            'immunity': 'disability', 'disability': 'immunity'
        }
        return HohfeldianPosition(
            holder=self.counterparty,
            position_type=corr_map[self.position_type],
            counterparty=self.holder,
            content=self.content
        )
    
    def opposite(self) -> 'HohfeldianPosition':
        """Return the opposite (contradictory) position."""
        opp_map = {
            'claim': 'no_right', 'no_right': 'claim',
            'duty': 'privilege', 'privilege': 'duty',
            'power': 'disability', 'disability': 'power',
            'liability': 'immunity', 'immunity': 'liability'
        }
        return HohfeldianPosition(
            holder=self.holder,
            position_type=opp_map[self.position_type],
            counterparty=self.counterparty,
            content=self.content
        )
```

## Practical Applications

### Access Control
- Privilege = Permission without obligation
- Power = Admin capability to modify permissions
- Immunity = Protected/locked permissions

### Smart Contracts
- Claims and duties map to contractual obligations
- Powers map to callable functions
- Immunities map to immutable state

### Organizational Roles
- Role assignment = Power exercise
- Role authority = Aggregated claims and privileges
- Role protection = Immunities from subordinates

---

**Further reading**: Hohfeld (1913, 1917), Wenar (2005), Kramer et al. (1998), Sumner (1987)
