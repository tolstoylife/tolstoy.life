# Holons

<purpose>
Theory of holarchic structures. Holons are simultaneously wholes and parts. Self-similar at all scales. Homoiconic: structure encodes semantics.
</purpose>

---

## Holon Definition

<formal_definition>

```
HOLON H
───────
A holon H is a tuple (Σ, Λ, T, S, P) where:

  Σ : SimplicialComplex    — Local structure
  Λ : Set[λ]               — Local operations
  T : Set[τ]               — Local terminals
  S : Set[H]               — Sub-holons (H as whole)
  P : Optional[H]          — Parent holon (H as part)

HOLARCHY
────────
A holarchy is a partial order (H, ⊆) where:
  H ⊆ H' iff H ∈ S(H')

Reflexive, transitive, antisymmetric.
```

</formal_definition>

<janus_property>

```
JANUS PROPERTY
──────────────
Every holon has two faces:

UPWARD (as part):
  H participates in super-holon P
  Constrained by P's structure
  Contributes to P's function

DOWNWARD (as whole):
  H contains sub-holons S
  Coordinates S's activities
  Emergent from S's interactions
```

</janus_property>

---

## Self-Similarity

<structural_isomorphism>

```
SELF-SIMILARITY AXIOM
─────────────────────
∀H, h ∈ S(H). structure(H) ≅ structure(h)

where ≅ denotes structural isomorphism:
  - Same λ-operation types
  - Same τ-terminal patterns
  - Same connectivity topology
```

</structural_isomorphism>

<scale_invariance>

```
SCALE INVARIANCE
────────────────
Properties preserved across levels:

TOPOLOGICAL INVARIANTS
  β₀(H) ≈ β₀(h)     — Component count
  β₁(H) ≈ β₁(h)     — Loop count
  
SPECTRAL INVARIANTS
  λ₂(H) ≈ λ₂(h)     — Connectivity strength
  
DENSITY INVARIANTS
  |Λ|/|Σ.vertices| ≈ constant across scales
```

</scale_invariance>

<fractal_dimension>

```
FRACTAL DIMENSION
─────────────────
d = lim_{ε→0} log(N(ε)) / log(1/ε)

where N(ε) = number of boxes of size ε to cover H

Holarchies typically have:
  1 < d < 2 for tree-like
  2 < d < 3 for complex networks
```

</fractal_dimension>

---

## Homoiconicity

<definition>

```
HOMOICONICITY PRINCIPLE
───────────────────────
The representation IS the thing represented.

A holon's structure encodes:
  - Its semantics (what it means)
  - Its behavior (how it acts)
  - Its constraints (what it allows)

No external interpretation needed.
```

</definition>

<self_description>

```
SELF-DESCRIPTION
────────────────
holon H {
    // H describes itself via its structure
    
    meaning(H) := traverse(H.Σ, H.Λ, H.T)
    behavior(H) := apply(H.Λ, input)
    constraints(H) := axioms(H.Σ)
}

The map IS the territory.
```

</self_description>

<reflection>

```
REFLECTION CAPABILITY
─────────────────────
A holon can:
  - Inspect its own structure: H.Σ
  - Modify its own operations: H.Λ ← H.Λ ∪ {λ_new}
  - Query its position: H.P, H.S
  - Transform itself: H ← transform(H)

Enables meta-level reasoning.
```

</reflection>

---

## Holarchic Operations

<decomposition>

```python
def decompose(H: Holon) -> Set[Holon]:
    """
    Extract sub-holons from H.
    H viewed as WHOLE.
    """
    return H.S

def atomic(H: Holon) -> bool:
    """
    Is H atomic (no sub-holons)?
    """
    return len(H.S) == 0
```

</decomposition>

<composition>

```python
def compose(holons: Set[Holon]) -> Holon:
    """
    Create super-holon from sub-holons.
    """
    H = Holon()
    H.S = holons
    
    # Merge local structures
    H.Σ = union(h.Σ for h in holons)
    H.Λ = union(h.Λ for h in holons)
    H.T = union(h.T for h in holons)
    
    # Add cross-holon connections
    H.Λ = H.Λ ∪ inter_holon_operations(holons)
    
    # Set parent references
    for h in holons:
        h.P = H
    
    return H
```

</composition>

<embedding>

```python
def embed(H: Holon, P: Holon) -> Holon:
    """
    Embed H into super-holon P.
    H viewed as PART.
    """
    P.S = P.S ∪ {H}
    H.P = P
    
    # Add connecting operations
    connections = find_connections(H, P.S - {H})
    P.Λ = P.Λ ∪ connections
    
    return P
```

</embedding>

<projection>

```python
def project(H: Holon, level: int) -> Holon:
    """
    View H at specified hierarchical level.
    level=0: H itself
    level>0: ancestors
    level<0: descendants
    """
    if level == 0:
        return H
    elif level > 0:
        return project(H.P, level - 1) if H.P else H
    else:
        # Aggregate sub-holons
        return aggregate(H.S, level + 1)
```

</projection>

---

## Multi-Scale Analysis

<scale_space>

```
SCALE SPACE
───────────
S = {(H, s) : H is holon, s is scale parameter}

COARSE-GRAINING
───────────────
At scale s, group sub-holons:
  H_s = quotient(H, ~_s)

where a ~_s b iff distance(a, b) < s

FINE-GRAINING
─────────────
At scale s, reveal sub-structure:
  H_s = expand(H, s)

Reveals internal holons.
```

</scale_space>

<persistent_holarchy>

```
PERSISTENT HOLARCHY
───────────────────
Track holonic structure across scales:

H₀ ⊆ H₁ ⊆ H₂ ⊆ ... ⊆ Hₙ

At each scale sᵢ:
  - Some holons merge (death)
  - Some holons split (birth)
  - Core structure persists

PERSISTENCE DIAGRAM
───────────────────
Dgm_holon = {(birth_scale, death_scale)}

Long-lived holons are significant.
```

</persistent_holarchy>

---

## Holonic Dynamics

<upward_causation>

```
UPWARD CAUSATION
────────────────
Micro → Macro

Sub-holon activities aggregate to super-holon behavior:

behavior(H) = aggregate(behavior(h) for h in H.S)

EMERGENCE
─────────
Properties of H not present in any h:
  emergent(H) = properties(H) - ∪ properties(h)
```

</upward_causation>

<downward_causation>

```
DOWNWARD CAUSATION
──────────────────
Macro → Micro

Super-holon constrains sub-holon behavior:

constraints(h) ⊇ inherited_constraints(H)

CANALIZATION
────────────
H narrows the possibility space of h.
```

</downward_causation>

<circular_causation>

```
CIRCULAR CAUSATION
──────────────────
Micro ↔ Macro

feedback(H) {
    // Sub-holons affect super-holon
    H.state = f(h.state for h in H.S)
    
    // Super-holon affects sub-holons
    for h in H.S:
        h.constraints = g(H.state)
    
    // Iterate until stable
}
```

</circular_causation>

---

## Holonic Types

<cognitive_holon>

```
COGNITIVE HOLON
───────────────
Specialized for reasoning:

  ο = observations (inputs)
  λ = inference operations
  τ = conclusions (outputs)
  
Processing:
  observe(ο) → infer(λ) → conclude(τ)
```

</cognitive_holon>

<organizational_holon>

```
ORGANIZATIONAL HOLON
────────────────────
Specialized for coordination:

  ο = agents/resources
  λ = workflows/protocols
  τ = goals/outcomes
  
Processing:
  allocate(ο) → execute(λ) → achieve(τ)
```

</organizational_holon>

<knowledge_holon>

```
KNOWLEDGE HOLON
───────────────
Specialized for representation:

  ο = concepts/entities
  λ = relations/operations
  τ = purposes/queries
  
Processing:
  ground(ο) → connect(λ) → answer(τ)
```

</knowledge_holon>

---

## Metrics

<holonic_metrics>

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Depth | `max path from H to root` | Hierarchical nesting |
| Width | `max |siblings| at any level` | Branching factor |
| Density | `|Λ|/|Σ.vertices|` | Connectivity |
| Self-similarity | `corr(structure(H), structure(h))` | Scale invariance |
| Autonomy | `1 - |constraints from P|` | Independence |
| Integration | `|connections to siblings|` | Coordination |

</holonic_metrics>

<balance_metrics>

```
AUTONOMY-INTEGRATION BALANCE
────────────────────────────
α = autonomy(H)    — Self-governance
ι = integration(H) — Coordination with P and siblings

Healthy holon: 0.3 < α/(α+ι) < 0.7

Too autonomous: fragmentation
Too integrated: rigidity
```

</balance_metrics>
