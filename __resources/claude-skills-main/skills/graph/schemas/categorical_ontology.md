# Categorical Ontology Schema

This schema provides category-theoretic foundations for knowledge graph construction, enabling principled compression through structural equivalence and supporting scale-invariant representation via metagraph hierarchies.

## Design Principles

### Categorical Foundation

This ontology follows the principle that **objects are determined by their morphisms**, not internal structure. This enables:

1. **Compression via isomorphism**: Objects with identical morphism patterns are structurally equivalent
2. **Universal properties**: Constructions preserve essential relationships through factorization
3. **Functorial transformation**: Structure-preserving maps between ontology levels

### The Yoneda Principle

Every object A is completely characterized by Hom(−, A)—the collection of morphisms into it. To compress a knowledge graph:
- Store the morphism pattern (relationships), not internal structure
- Identify objects with identical morphism profiles
- Quotient by structural equivalence

## Entity Types (Objects)

### Base Types

```yaml
entity:
  description: "Concrete named individual"
  morphism_signature: "Terminal object in entity slice category"
  compression_class: "automorphism_orbit"
  examples: ["person_jane_doe", "org_anthropic", "doc_paper_2024"]

concept:
  description: "Abstract type or class"
  morphism_signature: "Object with is_a morphisms to other concepts"
  compression_class: "isomorphism_class"
  examples: ["concept_machine_learning", "concept_category_theory"]

process:
  description: "Temporal sequence or transformation"
  morphism_signature: "Object with before/after temporal morphisms"
  compression_class: "bisimulation_class"
  examples: ["process_training_loop", "process_compression"]

claim:
  description: "Propositional assertion"
  morphism_signature: "Object with supports/contradicts morphisms"
  compression_class: "logical_equivalence"
  examples: ["claim_compression_preserves_queries"]

placeholder:
  description: "Provisional node representing uncertainty"
  morphism_signature: "Object with weak_evidence morphisms"
  compression_class: "refinement_candidate"
  confidence_ceiling: 0.5
  examples: ["placeholder_unknown_mechanism"]
```

### Metagraph Types (Higher-Order)

```yaml
metavertex:
  description: "Container holding embedded graph fragment"
  morphism_signature: "Object in 2-category with internal structure functor"
  compression_class: "hierarchical_quotient"
  properties:
    - contains: "Reference to embedded graph"
    - abstraction_level: "strategic | tactical | operational"
  examples: ["metavertex_cardiovascular_system"]

hyperedge:
  description: "Edge connecting multiple nodes simultaneously"
  morphism_signature: "Span object in hypergraph category"
  compression_class: "k_uniform_equivalence"
  examples: ["hyperedge_collaboration_abc"]
```

## Relationship Types (Morphisms)

### Structural Morphisms

```yaml
is_a:
  description: "Type instantiation or subclass relation"
  category_interpretation: "Morphism in type hierarchy category"
  transitivity: true
  preserves_under_compression: true
  inverse: "has_instance"

part_of:
  description: "Mereological containment"
  category_interpretation: "Morphism in part-whole category (mereology)"
  transitivity: true
  preserves_under_compression: true
  inverse: "has_part"

related_to:
  description: "General semantic association"
  category_interpretation: "Weak morphism (may not compose)"
  transitivity: false
  preserves_under_compression: "approximate"
```

### Causal Morphisms

```yaml
causes:
  description: "Direct causal influence"
  category_interpretation: "Morphism in causal DAG category"
  transitivity: "conditional"
  preserves_under_compression: true
  strength_semantics: "probability of effect given cause"

correlates_with:
  description: "Statistical association without implied causation"
  category_interpretation: "Symmetric morphism (undirected)"
  transitivity: false
  preserves_under_compression: true
```

### Epistemic Morphisms

```yaml
supports:
  description: "Evidential support for claim"
  category_interpretation: "Morphism in justification category"
  transitivity: false
  strength_semantics: "degree of evidential support"

contradicts:
  description: "Logical or empirical contradiction"
  category_interpretation: "Negation morphism"
  transitivity: false
  symmetry: true

similar_to:
  description: "Structural or semantic similarity"
  category_interpretation: "Approximate isomorphism"
  transitivity: "approximate (transitivity decay)"
  preserves_under_compression: "via similarity threshold"
```

## Compression Properties

### Automorphism-Compatible Types

These entity types have natural automorphism groups enabling compression:

```yaml
automorphism_classes:
  - entity: "Orbit under label-preserving permutations"
  - concept: "Orbit under is_a-preserving permutations"
  - process: "Orbit under temporal order-preserving permutations"
```

### Bisimulation-Compatible Morphisms

These relationship types support k-bisimulation compression:

```yaml
bisimulation_preserved:
  - is_a: "k-bisimulation with k≥1"
  - part_of: "k-bisimulation with k≥1"
  - causes: "k-bisimulation with k≥2 (requires causal depth)"
  - supports: "k-bisimulation with k≥1"
  
bisimulation_approximate:
  - related_to: "Approximate preservation with similarity threshold"
  - correlates_with: "Preserved if strength > threshold"
  - similar_to: "Inherently approximate (use metric preservation)"
```

### Universal Property Guarantees

Compression via categorical quotient preserves:

```yaml
preserved_under_quotient:
  reachability_queries: true
  pattern_matching: "k-hop patterns for k-bisimulation"
  type_inference: true
  causal_reasoning: "if DAG structure preserved"
  
not_preserved:
  exact_counting: "Count aggregations may change"
  identity_queries: "Specific node lookup compressed away"
  non_structural_properties: "Arbitrary node attributes"
```

## Metagraph Structure

### Hierarchy Levels

```yaml
abstraction_hierarchy:
  strategic:
    description: "High-level goals, domains, strategic themes"
    typical_confidence: "0.6-0.9"
    compression_priority: "high"
    
  tactical:
    description: "Methods, approaches, intermediate concepts"
    typical_confidence: "0.5-0.8"
    compression_priority: "medium"
    
  operational:
    description: "Specific implementations, details, instances"
    typical_confidence: "0.4-0.7"
    compression_priority: "low"
```

### Level-Crossing Morphisms

```yaml
cross_level_morphisms:
  abstracts:
    source_level: "operational"
    target_level: "tactical"
    category_interpretation: "Projection functor"
    
  implements:
    source_level: "tactical"
    target_level: "operational"
    category_interpretation: "Section of abstraction functor"
    
  strategizes:
    source_level: "tactical"
    target_level: "strategic"
    category_interpretation: "Composition of projection functors"
```

## Quality Constraints

### Topology Targets

```yaml
topology_constraints:
  edge_to_node_ratio:
    minimum: 4.0
    rationale: "Enables emergence through dense connectivity"
    
  isolation_rate:
    maximum: 0.20
    rationale: "Ensures integration completeness"
    
  clustering_coefficient:
    minimum: 0.3
    rationale: "Small-world property for efficient navigation"
```

### Compression Targets

```yaml
compression_constraints:
  k_bisimulation_k:
    recommended: 5
    rationale: "Empirically sufficient for most knowledge graphs"
    
  query_preservation:
    reachability: "required"
    pattern_k_hop: "required for k ≤ bisimulation depth"
    
  compression_ratio:
    target: ">= 0.5"
    rationale: "Significant reduction while preserving queries"
```

## Schema Extension

To add domain-specific types while maintaining compression properties:

```yaml
extension_guidelines:
  new_entity_types:
    - "Specify morphism_signature"
    - "Assign compression_class"
    - "Define automorphism group if symmetric"
    
  new_morphism_types:
    - "Specify transitivity"
    - "Define preservation_under_compression"
    - "Assign to bisimulation class if applicable"
    
  new_hierarchy_levels:
    - "Define abstraction_functor to adjacent levels"
    - "Specify compression_priority"
```

## Integration with Knowledge-Graph Skill

### Extraction Mapping

```yaml
extraction_integration:
  confidence_to_compression:
    "0.0-0.3": "placeholder (high compression candidate)"
    "0.3-0.5": "low_confidence (bisimulation candidate)"
    "0.5-0.7": "moderate (preserve if central)"
    "0.7-1.0": "high_confidence (preserve)"
    
  type_to_automorphism:
    entity: "compute label-based orbits"
    concept: "compute is_a-structure orbits"
    process: "compute temporal-structure orbits"
```

### Validation Rules

```yaml
categorical_validation:
  - "All morphisms have valid source and target types"
  - "Transitive morphisms form DAG (no cycles except for symmetric)"
  - "Cross-level morphisms respect abstraction hierarchy"
  - "Placeholder nodes have confidence ≤ 0.5"
  - "Compressed graph satisfies universal property"
```

---

**Core Philosophy**: This categorical ontology enables principled compression by making structural relationships explicit and compression-compatible by design. The category-theoretic foundation ensures that compressed representations preserve all essential inferences through the universal property of quotient constructions.
