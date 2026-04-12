# Level Construction Guide

Detailed procedures for constructing each RPP level.

## L3: Detail-Graph (Ground Truth)

The foundation layer containing all domain knowledge.

### Extraction Process

```python
def extract_l3(corpus: str, domain: str) -> Graph:
    """
    Extract ground truth detail graph from corpus.
    
    1. Tokenise and segment corpus
    2. Extract entities and relationships
    3. Build initial graph with all nodes
    4. Compute semantic weights for edges
    """
    # Entity extraction
    entities = extract_entities(corpus, domain_ontology=domain)
    
    # Relationship extraction
    relationships = extract_relationships(corpus, entities)
    
    # Build graph
    g = Graph()
    for e in entities:
        g.add_node(e, level=3, atomic=False)
    
    for r in relationships:
        g.add_edge(r.source, r.target, weight=r.semantic_weight)
    
    return g
```

### L3 Properties

- **Completeness**: Contains all extractable domain knowledge
- **No compression**: 100% node coverage
- **Rich edges**: Full relationship network
- **Semantic weights**: Edge weights reflect importance

## L2: Concept-Graph (Composite Concepts)

Emergent composite concepts from L3 clustering.

### Construction from L3

```python
def construct_l2(l3: Graph, pareto_threshold: float = 0.8) -> Graph:
    """
    Construct concept graph via Pareto extraction.
    
    Target: 20% of L3 nodes grounding 80% of content.
    """
    # 1. Compute node importance
    importance = pagerank(l3) * semantic_centrality(l3)
    
    # 2. Cluster related nodes
    clusters = community_detection(l3, resolution=1.0)
    
    # 3. Select cluster representatives by Pareto criterion
    l2_nodes = []
    coverage = 0.0
    
    for cluster in sorted(clusters, key=lambda c: c.total_importance, reverse=True):
        representative = max(cluster.nodes, key=lambda n: importance[n])
        l2_nodes.append(representative)
        coverage += cluster.coverage_contribution
        
        if coverage >= pareto_threshold:
            break
    
    # 4. Build L2 graph with composite relationships
    l2 = Graph()
    for node in l2_nodes:
        l2.add_node(node, level=2, composite=True)
        l2.node[node]['grounded_nodes'] = get_cluster_members(node, clusters)
    
    # 5. Add edges based on inter-cluster relationships
    for n1 in l2_nodes:
        for n2 in l2_nodes:
            if n1 != n2 and has_cross_cluster_edges(n1, n2, l3):
                weight = compute_composite_weight(n1, n2, l3)
                l2.add_edge(n1, n2, weight=weight)
    
    return l2
```

### L2 Properties

- **Composite nodes**: Each represents cluster of L3 nodes
- **Emergent concepts**: Arise from L3 interactions
- **Pareto coverage**: 20% nodes → 80% ground coverage
- **Hyperedge potential**: May form multi-node interactions

### Hyperedge Generation

```python
def generate_l2_hyperedges(l2: Graph, l3: Graph) -> list[Hyperedge]:
    """
    Generate weighted hyperedges for multi-concept interactions.
    """
    hyperedges = []
    
    # Find triads and higher-order cliques
    cliques = find_cliques(l2, min_size=3)
    
    for clique in cliques:
        # Compute hyperedge weight from L3 interactions
        weight = sum(
            l3_interaction_strength(n1, n2)
            for n1, n2 in combinations(clique, 2)
        ) / len(clique)
        
        he = Hyperedge(nodes=clique, weight=weight, level=2)
        hyperedges.append(he)
    
    return hyperedges
```

## L1: Logic-Graph (Atomic Principles)

First principles extracted from L2 via Pareto.

### Construction from L2

```python
def construct_l1(l2: Graph, pareto_threshold: float = 0.8) -> Graph:
    """
    Construct logic graph of atomic first principles.
    
    Target: 4% of original L3 nodes (20% of L2).
    Grounding: 64% of original content.
    """
    # 1. Identify atomic candidates
    # Atomic = cannot be decomposed into simpler concepts
    atomic_candidates = identify_atomics(l2)
    
    # 2. Rank by explanatory power
    explanatory_power = {}
    for node in atomic_candidates:
        # How many L2 concepts does this principle explain?
        explained = count_derived_concepts(node, l2)
        ep = explained / len(l2.nodes)
        explanatory_power[node] = ep
    
    # 3. Select by Pareto criterion
    l1_nodes = []
    coverage = 0.0
    
    for node in sorted(explanatory_power, key=explanatory_power.get, reverse=True):
        l1_nodes.append(node)
        coverage += explanatory_power[node]
        
        if coverage >= pareto_threshold:
            break
    
    # 4. Build L1 graph
    l1 = Graph()
    for node in l1_nodes:
        l1.add_node(node, level=1, atomic=True)
        l1.node[node]['derives'] = get_derived_concepts(node, l2)
    
    # 5. Add edges (principled interactions)
    for n1 in l1_nodes:
        for n2 in l1_nodes:
            if n1 != n2 and principles_interact(n1, n2, l2):
                l1.add_edge(n1, n2, weight=interaction_strength(n1, n2))
    
    return l1
```

### L1 Properties

- **Atomic nodes**: Irreducible first principles
- **Derivation links**: Each principle derives multiple L2 concepts
- **Pareto squared**: 4% nodes → 64% coverage
- **Permutative interactions**: Principles combine to generate composites

### Atomicity Validation

```python
def validate_atomicity(node, l2: Graph) -> bool:
    """
    Verify node is truly atomic (not decomposable).
    """
    # Check if node can be expressed as combination of other L1 candidates
    other_l1 = [n for n in l2.nodes if n != node and is_atomic_candidate(n)]
    
    for subset in powerset(other_l1):
        if len(subset) >= 2:
            combined_coverage = combine_explanatory_power(subset, l2)
            if combined_coverage >= node.explanatory_power:
                return False  # Node is composite of others
    
    return True
```

## L0: Meta-Graph (Schema)

Ultimate schema via abductive generalisation from L1.

### Construction from L1

```python
def construct_l0(l1: Graph, pareto_threshold: float = 0.8) -> Graph:
    """
    Construct meta-graph schema via abductive generalisation.
    
    Target: 0.8% of original L3 nodes.
    Grounding: 51% of original content (Pareto cubed).
    """
    # 1. Abductive generalisation: find patterns across L1 principles
    patterns = abductive_inference(l1)
    
    # 2. Rank patterns by generality
    generality = {}
    for pattern in patterns:
        # How many L1 principles does this pattern explain?
        explained_principles = count_subsumed_principles(pattern, l1)
        generality[pattern] = explained_principles / len(l1.nodes)
    
    # 3. Select by Pareto criterion
    l0_nodes = []
    coverage = 0.0
    
    for pattern in sorted(generality, key=generality.get, reverse=True):
        l0_nodes.append(pattern)
        coverage += generality[pattern]
        
        if coverage >= pareto_threshold:
            break
    
    # 4. Build L0 schema
    l0 = Schema()
    for node in l0_nodes:
        l0.add_node(node, level=0, schema_element=True)
        l0.node[node]['subsumes'] = get_subsumed_principles(node, l1)
    
    # 5. Add structural relationships
    for n1 in l0_nodes:
        for n2 in l0_nodes:
            if n1 != n2:
                rel = infer_schema_relationship(n1, n2, l1)
                if rel:
                    l0.add_edge(n1, n2, relation_type=rel.type, weight=rel.strength)
    
    return l0
```

### L0 Properties

- **Schema elements**: Highest-level abstractions
- **Pareto cubed**: 0.8% nodes → 51% coverage
- **Abductive**: Inferred patterns, not extracted entities
- **Deductively valid**: Must explain L1 principles

### Deductive Validation

```python
def validate_l0_deductively(l0: Schema, l1: Graph) -> ValidationResult:
    """
    Verify L0 schema deductively derives L1 principles.
    """
    errors = []
    
    for principle in l1.nodes:
        # Find L0 elements that should derive this principle
        derivers = [n for n in l0.nodes if principle in n['subsumes']]
        
        if not derivers:
            errors.append(f"L1 principle {principle} not derived from L0")
        else:
            # Verify derivation is logically sound
            for deriver in derivers:
                if not logically_derives(deriver, principle):
                    errors.append(f"Derivation {deriver} → {principle} invalid")
    
    coverage = len([p for p in l1.nodes if any(
        p in n['subsumes'] for n in l0.nodes
    )]) / len(l1.nodes)
    
    return ValidationResult(
        valid=len(errors) == 0 and coverage >= 0.8,
        coverage=coverage,
        errors=errors
    )
```

## Bidirectional Construction

Simultaneous bottom-up and top-down with convergence.

```python
def bidirectional_construct(
    corpus: str,
    initial_schema: Schema = None,
    max_iterations: int = 10
) -> RPPGraph:
    """
    Bidirectional construction with convergence.
    """
    # Initialize
    l3 = extract_l3(corpus)
    l0 = initial_schema or bootstrap_schema(corpus)
    
    prev_l2 = None
    
    for iteration in range(max_iterations):
        # Bottom-up: L3 → L2
        l2_bottom = construct_l2(l3)
        
        # Top-down: L0 → L1 → L2
        l1_top = derive_l1_from_schema(l0)
        l2_top = expand_l1_to_l2(l1_top)
        
        # Merge at L2
        l2_merged = merge_graphs(l2_bottom, l2_top)
        
        # Check convergence
        if prev_l2 and graph_similarity(l2_merged, prev_l2) > 0.95:
            break
        
        prev_l2 = l2_merged
        
        # Update L1 and L0 from merged L2
        l1 = construct_l1(l2_merged)
        l0 = construct_l0(l1)
    
    return RPPGraph(l0=l0, l1=l1, l2=l2_merged, l3=l3)
```

## Generation Constraints

### Children Per Node

Each node generates 2-3 children at the next level:

```python
def validate_generation_constraint(parent_level: Graph, child_level: Graph) -> bool:
    """
    Verify 2-3 children per parent node.
    """
    for parent in parent_level.nodes:
        children = get_children(parent, child_level)
        if not (2 <= len(children) <= 3):
            return False
    return True
```

### Node Ratio Validation

```python
def validate_ratios(l0, l1, l2, l3) -> dict:
    """
    Validate node ratios between levels.
    """
    return {
        'l1_l2': (len(l1) / len(l2), (2, 3)),  # Target 2-3:1
        'l1_l2_alt': (len(l1) / len(l2), (9, 12)),  # Alternative 9-12:1
        'l1_l3': (len(l1) / len(l3), (6, 9)),  # Target 6-9:1
        'valid': all_ratios_valid(...)
    }
```
