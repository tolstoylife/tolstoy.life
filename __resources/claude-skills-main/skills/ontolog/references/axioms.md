# Axioms

<purpose>
Lex-style formal constraint system for holarchic structures. Axioms constrain valid configurations. Inference materializes derived facts. Validation ensures consistency.
</purpose>

---

## Type System

<core_types>

```
TYPE HIERARCHY
──────────────
Type ::= NodeType | EdgeType | PropertyType

NodeType    ::= ο | τ | H          — Bases, terminals, holons
EdgeType    ::= λ | ⊆ | ≅          — Operations, containment, isomorphism
PropertyType ::= π                  — Arbitrary properties
```

</core_types>

<type_constraints>

| Constraint | Syntax | Semantics |
|------------|--------|-----------|
| Domain | `λ : ο → τ` | Operation signature |
| Range | `π : T` | Property type |
| Cardinality | `π[1..*]` | Required multiplicity |
| Uniqueness | `π!` | Unique value |
| Optionality | `π?` | Optional property |

</type_constraints>

<syntax>
```lex
type Base extends Node {
    id: String!
    properties: Map<String, Value>?
}

type Operation extends Edge {
    domain: Base!
    codomain: Base | Terminal!
    confidence: Float[0..1] = 1.0
}

type Terminal extends Node {
    id: String!
    persistence: Float[0..1]!
}
```
</syntax>

---

## Structural Axioms

<transitivity>

```lex
axiom Transitivity[λ: Operation] {
    constraint: λ.transitive = true
    rule: λ(a, b) ∧ λ(b, c) ⟹ λ(a, c)
}
```

**Application**: Reachability, ancestry, containment.

</transitivity>

<symmetry>

```lex
axiom Symmetry[λ: Operation] {
    constraint: λ.symmetric = true
    rule: λ(a, b) ⟹ λ(b, a)
}
```

**Application**: Similarity, equivalence.

</symmetry>

<reflexivity>

```lex
axiom Reflexivity[λ: Operation] {
    constraint: λ.reflexive = true
    rule: ∀a. λ(a, a)
}
```

**Application**: Identity, self-reference.

</reflexivity>

<acyclicity>

```lex
axiom Acyclicity[λ: Operation] {
    constraint: λ.acyclic = true
    rule: ¬∃path. λ*(a, a)
    
    // Equivalent: no cycles in λ-reachability
}
```

**Application**: Hierarchies, DAGs, partial orders.

</acyclicity>

<existential>

```lex
axiom ExistentialRequirement[ο: Base] {
    rule: ∃λ. domain(λ) = ο
    
    // Every base must participate in some operation
}
```

**Application**: Groundedness constraint.

</existential>

---

## Property Axioms

<propagation>

```lex
axiom PropertyPropagation[π: Property, λ: Operation] {
    constraint: π.propagates_along = λ
    rule: λ(a, b) ∧ π(a) = v ⟹ π(b) = v
}
```

**Application**: Attribute inheritance along edges.

</propagation>

<inheritance>

```lex
axiom PropertyInheritance[π: Property, λ: Operation] {
    constraint: π.inherits_via = λ
    rule: λ(a, b) ⟹ π(b) ⊇ π(a)
    
    // Subsets inherit, may extend
}
```

**Application**: Type inheritance, role accumulation.

</inheritance>

<value_constraints>

```lex
axiom ValueConstraint[π: Property] {
    range: Float[0..1]              // Numeric range
    pattern: /^[A-Z][a-z]+$/        // String pattern
    enum: [Low, Medium, High]       // Enumeration
    unique: true                     // Uniqueness
}
```

**Application**: Data validation, schema enforcement.

</value_constraints>

---

## Path Logic

<reachability>

```lex
path Reachability[λ: Operation] {
    // Can reach b from a in n steps
    reach(a, b, n) := ∃λ₁...λₙ. λₙ(...λ₁(a)...) = b
    
    // Shortest path
    shortest(a, b) := min{n : reach(a, b, n)}
    
    // All paths
    all_paths(a, b) := {p : p connects a to b via λ}
}
```

</reachability>

<cycle_prevention>

```lex
path CyclePrevention[λ: Operation] {
    constraint: acyclic(λ)
    
    rule: ¬∃a. reach(a, a, n) for any n > 0
    
    on_violation: reject | break_weakest_edge
}
```

</cycle_prevention>

<connectivity>

```lex
path Connectivity[Σ: Complex] {
    // Connected: single component
    connected(Σ) := β₀(Σ) = 1
    
    // Strongly connected: all pairs reachable
    strongly_connected(Σ) := ∀a,b. reach(a, b, _)
    
    // k-connected: survives k-1 vertex removals
    k_connected(Σ, k) := min_cut(Σ) ≥ k
}
```

</connectivity>

<aggregation>

```lex
path Aggregation[π: Property, λ: Operation] {
    // Sum along paths
    sum_path(a, b, π) := Σ π(v) for v in path(a, b)
    
    // Max along paths
    max_path(a, b, π) := max π(v) for v in path(a, b)
    
    // Min (bottleneck) along paths
    min_path(a, b, π) := min π(v) for v in path(a, b)
}
```

</aggregation>

---

## World Assumptions

<open_world>

```lex
@world(open)
type Knowledge {
    // Absence of fact ≠ negation of fact
    // Unknown is possible
}
```

**Semantics**: Missing information is unknown, not false.

</open_world>

<closed_world>

```lex
@world(closed)
type Configuration {
    // Absence of fact = negation of fact
    // Complete information assumed
}
```

**Semantics**: If not stated, then false.

</closed_world>

<local_closed>

```lex
@world(open)
type Entity {
    @world(closed)
    status: Enum[Active, Inactive, Pending]
    
    // status is closed-world (must be one of enum)
    // other properties are open-world
}
```

**Semantics**: Mixed assumptions per property.

</local_closed>

---

## Inference Rules

<materialized>

```lex
inference MaterializedInference {
    // Compute and store derived facts at write time
    
    trigger: on_write
    strategy: eager
    
    rule TransitiveClosure[λ] {
        when: λ.transitive ∧ insert(λ(a, b))
        then: ∀c. λ(b, c) ⟹ insert(λ(a, c))
    }
}
```

**Trade-off**: Fast reads, slower writes, storage overhead.

</materialized>

<virtual>

```lex
inference VirtualInference {
    // Compute derived facts at query time
    
    trigger: on_read
    strategy: lazy
    
    rule TransitiveClosure[λ] {
        when: query(reach(a, b))
        then: compute_closure(a, b)
    }
}
```

**Trade-off**: Fast writes, slower reads, no storage overhead.

</virtual>

<hybrid>

```lex
inference HybridInference {
    // Materialize frequently-accessed paths
    // Compute rare paths on demand
    
    strategy: adaptive
    
    materialize_threshold: access_frequency > 100/day
    cache_ttl: 1 hour
}
```

</hybrid>

---

## Validation

<write_time>

```lex
validation WriteTimeValidation {
    // Check constraints before accepting writes
    
    @validate(before_write)
    rule TypeCheck {
        ∀π. typeof(π.value) matches π.type
    }
    
    @validate(before_write)
    rule RangeCheck {
        ∀π. π.value ∈ π.range
    }
    
    @validate(before_write)
    rule CardinalityCheck {
        ∀π. |π.values| ∈ π.cardinality
    }
}
```

</write_time>

<consistency>

```lex
validation ConsistencyValidation {
    // Verify structural consistency
    
    @validate(periodic: 1 hour)
    rule AcyclicityCheck {
        ∀λ. λ.acyclic ⟹ ¬has_cycles(λ_graph)
    }
    
    @validate(periodic: 1 day)
    rule GroundednessCheck {
        ∀ο. ∃λ. domain(λ) = ο
    }
}
```

</consistency>

---

## Probabilistic Axioms

<confidence>

```lex
axiom ConfidenceScoring[λ: Operation] {
    property: confidence: Float[0..1]
    
    // Composition rule
    compose_confidence(λ₁, λ₂) := λ₁.confidence × λ₂.confidence
    
    // Path confidence
    path_confidence(p) := Π λᵢ.confidence for λᵢ in p
}
```

</confidence>

<boost>

```lex
axiom BoostFunction[λ: Operation] {
    // Increase confidence based on evidence
    
    boost(λ, evidence) := min(1.0, λ.confidence + Δ(evidence))
    
    where Δ(evidence) = log(1 + |evidence|) / 10
}
```

</boost>

<uncertainty>

```lex
axiom UncertaintyPropagation {
    // Track uncertainty through inference
    
    uncertainty(derived) := 1 - Π confidence(premise) for premise in derivation
    
    threshold: uncertainty < 0.3 for materialization
}
```

</uncertainty>
