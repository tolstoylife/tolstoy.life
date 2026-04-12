# Topology Reference (Γ, χ)

Validation invariants that preserve quality across transformations.

## Density (η)

```
η = |E|/|V| = edges/nodes
```

### Targets by Context

| Context | η Target | Rationale |
|---------|----------|-----------|
| Default | ≥4.0 | Small-world connectivity |
| SAQ | 2.0-2.5 | Word limit constrains nodes |
| Viva | 3.0-4.0 | Progressive disclosure |
| Mechanistic | ≥4.0 | Full causal chains |
| Systems integration | ≥5.5 | Dense interdependencies |

### Theoretical Basis

- **Small-world topology**: High clustering + short path lengths
- **3-connectivity**: Removal of 2 vertices doesn't disconnect
- **Scale-free property**: Power-law degree distribution

### Validation

```python
def validate_topology(G, target=4.0):
    η = len(G.edges) / len(G.nodes)
    if η < target:
        return ValidationFailure(
            current=η,
            target=target,
            deficit=target - η,
            remediation="Add edges or triangulate"
        )
    return Valid(η=η)
```

### Remediation

| Condition | Strategy |
|-----------|----------|
| η < 2.0 (sparse) | Identify orphans, add primary connections |
| 2.0 ≤ η < 3.0 | Triangulate: A-B, B-C → add A-C |
| 3.0 ≤ η < target | Add cross-domain bridges |
| η > 6.0 (dense) | Verify not artificial; may indicate overconnection |

### Preserving η Across Transformations

```haskell
∀G. transform(G) ⊢ η(G') ≥ η(G)  -- Never degrade
```

## KROG Governance (χ)

```
Valid(λ) ⟺ K(λ) ∧ R(λ) ∧ O(λ) ∧ G(λ)
```

### K — Knowable

Effects must be transparent:

| Check | Question |
|-------|----------|
| Predictability | Can the user anticipate outcomes? |
| Traceability | Can reasoning be followed? |
| Explainability | Can the process be described? |

### R — Rights

Authority must be held:

| Check | Question |
|-------|----------|
| Authorization | Is this within permitted scope? |
| Capability | Do I have the skills needed? |
| Resources | Are required tools available? |

### O — Obligations

Duties must be met:

| Check | Question |
|-------|----------|
| Accuracy | Is information correct? |
| Completeness | Are key aspects addressed? |
| Honesty | Are limitations disclosed? |

### G — Governance

Within bounds:

| Check | Question |
|-------|----------|
| Safety | Could this cause harm? |
| Alignment | Does this serve user's intent? |
| Proportionality | Is response appropriately scaled? |

### Quick KROG Check

```
□ K: User can understand what will happen
□ R: I'm authorized and capable for this task
□ O: I'm being accurate, complete, honest
□ G: This is safe, aligned, proportional
```

### KROG Violations

| Violation | Example | Remediation |
|-----------|---------|-------------|
| K-fail | Opaque reasoning | Add explanation |
| R-fail | Beyond expertise | Acknowledge limits |
| O-fail | Incomplete answer | Expand scope |
| G-fail | Potential harm | Refuse or caveat |

## Constraint Types (Deontic)

```haskell
data D = P a    -- Permitted
       | O a    -- Obligated  
       | F a    -- Forbidden
       | I a    -- Impossible
```

### Axioms

```
O a ⊢ P a        -- Ought implies may
P a ⟺ ¬F a       -- Permission = not forbidden
F a ⟺ O (¬a)     -- Forbidden = obligated to not
```

### Constraint Trichotomy

| Type | Effect | Example |
|------|--------|---------|
| Enabling | Expands action space | "You may use web search" |
| Governing | Channels flow | "Cite sources" |
| Constitutive | Defines identity | "Never claim certainty without evidence" |

## Combined Validation

```python
def validate(response, η_target=4.0):
    # Topology check
    G = extract_graph(response)
    η_valid = validate_topology(G, η_target)
    
    # KROG check
    krog_valid = all([
        check_knowable(response),
        check_rights(response),
        check_obligations(response),
        check_governance(response)
    ])
    
    if not η_valid:
        return Remediate("topology", η_valid.deficit)
    if not krog_valid:
        return Remediate("krog", krog_valid.violations)
    
    return Valid(η=G.η, krog=True)
```

## Invariant Preservation

The λ transformation preserves invariants:

```
∀τ ∈ λ(ο,K). 
  η(τ) ≥ target ∧ 
  KROG(τ) ∧ 
  PSR(τ)  -- Principle of Sufficient Reason
```

PSR: Every claim has sufficient grounds (evidence, reasoning, or explicit uncertainty).
