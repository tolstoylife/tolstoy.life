---
created: 2025-01-05
tags: [reference, semantics, nlp, layer2]
purpose: Common semantic patterns for ontology enrichment
---

# Semantic Pattern Reference

Layer 2 semantic analysis patterns for relationship classification and entity extraction.

## Relationship Types

### Hierarchical Relationships

**Parent-Of** (`parent_of`)
- Description: Direct hierarchical containment
- Example: "Database" parent_of "Tables"
- Properties: Transitive, antisymmetric
- Use: Tree structures, organizational charts

**Part-Of** (Meronymy) (`part_of`)
- Description: Component or aspect relationship
- Example: "Engine" part_of "Car"
- Properties: Transitive
- Use: Physical components, functional aspects

**Instance-Of** (Hypernymy) (`instance_of`)
- Description: Type-instance relationship
- Example: "Fido" instance_of "Dog"
- Properties: Transitive
- Use: Classification hierarchies

### Oppositional Relationships

**Opposite-Of** (Antonymy) (`opposite_of`)
- Description: Semantic opposition or contrast
- Example: "Hot" opposite_of "Cold"
- Properties: Symmetric
- Use: Binary contrasts, antonym pairs

**Contrasts-With** (`contrasts_with`)
- Description: Weaker opposition, different perspectives
- Example: "Hardware" contrasts_with "Software"
- Properties: Symmetric
- Use: Complementary concepts

### Causal Relationships

**Causes** (`causes`)
- Description: Direct causation
- Example: "Rain" causes "Wet Ground"
- Properties: Asymmetric, temporal
- Use: Process flows, cause-effect chains

**Enables** (`enables`)
- Description: Prerequisite or facilitator
- Example: "Authentication" enables "Access"
- Properties: Asymmetric
- Use: Dependencies, requirements

### Associative Relationships

**Related-To** (`related_to`)
- Description: Generic association
- Example: "Machine Learning" related_to "Statistics"
- Properties: Symmetric
- Use: Weak connections, topic associations

**Similar-To** (`similar_to`)
- Description: Semantic similarity
- Example: "Automobile" similar_to "Vehicle"
- Properties: Symmetric, transitive (weak)
- Use: Synonyms, analogies

## Entity Types

### Conceptual Entities

**Concept** (`concept`)
- Abstract idea or category
- Examples: "Democracy", "Photosynthesis", "Algorithm"
- Properties: Usually at higher hierarchy levels

**Class** (`class`)
- Formal type definition
- Examples: "User", "Product", "Transaction"
- Properties: Can have instances

**Property** (`property`)
- Attribute or characteristic
- Examples: "Color", "Size", "Temperature"
- Properties: Usually leaf nodes

### Concrete Entities

**Entity** (`entity`)
- Concrete object or instance
- Examples: "John Smith", "Tesla Model 3", "New York"
- Properties: Specific, identifiable

**Event** (`event`)
- Occurrence or action
- Examples: "Click", "Purchase", "Earthquake"
- Properties: Temporal, often has participants

**Document** (`document`)
- Information container
- Examples: "Report", "Article", "Specification"
- Properties: Has content, author, date

## Extraction Patterns

### Named Entity Patterns

**Person Names**
```regex
\b[A-Z][a-z]+ [A-Z][a-z]+\b
```
- Extract as: `entity` type
- Add property: `entity_type: "person"`

**Organizations**
```regex
\b[A-Z][A-Za-z]+ (?:Inc|Corp|LLC|Ltd)\b
```
- Extract as: `entity` type
- Add property: `entity_type: "organization"`

### Relationship Patterns

**"X is a Y"** → `instance_of`
```
"A dog is an animal" → (Dog, instance_of, Animal)
```

**"X consists of Y"** → `part_of`
```
"Water consists of H2O" → (H2O, part_of, Water)
```

**"X causes Y"** → `causes`
```
"Heat causes expansion" → (Heat, causes, Expansion)
```

**"X versus Y"** → `opposite_of`
```
"Pros versus cons" → (Pros, opposite_of, Cons)
```

## Multi-Dimensional Navigation

### Temporal Dimension

Create edges with `dimension="temporal"`:
- **Precedence**: "X precedes Y"
- **Sequence**: "X follows Y"
- **Concurrency**: "X concurrent Y"

### Spatial Dimension

Create edges with `dimension="spatial"`:
- **Containment**: "X contains Y"
- **Adjacency**: "X adjacent Y"
- **Proximity**: "X near Y"

### Conceptual Dimension

Create edges with `dimension="conceptual"`:
- **Abstraction**: "X abstraction_of Y"
- **Specialization**: "X specializes Y"
- **Generalization**: "X generalizes Y"

## Implicit Relationship Inference

### Co-occurrence Based

```python
if entities_appear_in_same_paragraph(A, B):
    confidence = calculate_proximity_score(A, B)
    edge = OntologyEdge(
        source_id=A.id,
        target_id=B.id,
        edge_type="related_to",
        inferred=True,
        strength=confidence
    )
```

### Tag Overlap Based

```python
def infer_from_tags(node_a, node_b):
    tags_a = set(node_a.properties.get("tags", []))
    tags_b = set(node_b.properties.get("tags", []))

    overlap = len(tags_a & tags_b) / len(tags_a | tags_b)

    if overlap > 0.5:
        return OntologyEdge(
            source_id=node_a.id,
            target_id=node_b.id,
            edge_type="similar_to",
            inferred=True,
            strength=overlap
        )
```

### Structural Proximity Based

```python
def infer_from_structure(node_a, node_b, ontology):
    distance = shortest_path_length(node_a, node_b, ontology)

    if 2 <= distance <= 3:
        return OntologyEdge(
            source_id=node_a.id,
            target_id=node_b.id,
            edge_type="related_to",
            inferred=True,
            strength=1.0 / distance
        )
```

## Related

- [[ast-parsing-guide|AST Parsing Guide]]
- [[template-syntax|Template Syntax Reference]]
