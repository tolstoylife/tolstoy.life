# Pareto Algorithms

Mathematical foundations and algorithms for Pareto-optimal extraction in RPP.

## Pareto Principle Chain

The recursive Pareto principle creates exponential compression:

| Level | Pareto Order | Nodes | Coverage | Formula |
|-------|--------------|-------|----------|---------|
| L3 | Base | 100% | 100% | N |
| L2 | Pareto¹ | 20% | 80% | 0.2N |
| L1 | Pareto² | 4% | 64% | 0.2² × N |
| L0 | Pareto³ | 0.8% | 51% | 0.2³ × N |

### Mathematical Foundation

```
Coverage(Ln) = 0.8^(3-n) × 100%
Nodes(Ln) = 0.2^(3-n) × |L3|

Where:
- n ∈ {0, 1, 2, 3} is the level index
- L3 is the ground truth with |L3| nodes
```

## Core Extraction Algorithm

```python
def pareto_extract(
    source: Graph,
    target_coverage: float = 0.8,
    max_nodes_ratio: float = 0.2
) -> Graph:
    """
    Extract Pareto-optimal subgraph.
    
    Guarantees:
    - Output has ≤ max_nodes_ratio × |source| nodes
    - Output grounds ≥ target_coverage of source semantics
    
    Args:
        source: Input graph to compress
        target_coverage: Minimum semantic coverage (default 80%)
        max_nodes_ratio: Maximum node ratio (default 20%)
    
    Returns:
        Pareto-optimal subgraph
    """
    # Step 1: Compute importance scores
    importance = compute_importance_scores(source)
    
    # Step 2: Sort nodes by importance
    sorted_nodes = sorted(
        source.nodes,
        key=lambda n: importance[n],
        reverse=True
    )
    
    # Step 3: Greedy selection until coverage threshold
    selected = []
    cumulative_coverage = 0.0
    max_nodes = int(max_nodes_ratio * len(source.nodes))
    
    for node in sorted_nodes:
        if len(selected) >= max_nodes:
            break
            
        selected.append(node)
        cumulative_coverage += node_coverage_contribution(node, source, selected)
        
        if cumulative_coverage >= target_coverage:
            break
    
    # Step 4: Build output graph
    output = build_induced_subgraph(source, selected)
    
    # Step 5: Validate Pareto property
    assert len(output.nodes) <= max_nodes
    assert cumulative_coverage >= target_coverage
    
    return output
```

## Importance Scoring

### Multi-Factor Importance

```python
def compute_importance_scores(graph: Graph) -> dict[Node, float]:
    """
    Compute node importance via multiple factors.
    
    Factors:
    1. PageRank (structural importance)
    2. Semantic centrality (content importance)
    3. Connectivity (bridge potential)
    4. Information density (compression value)
    """
    scores = {}
    
    # Factor 1: PageRank
    pagerank = nx.pagerank(graph, alpha=0.85)
    
    # Factor 2: Semantic centrality
    semantic = {}
    for node in graph.nodes:
        # TF-IDF style semantic weight
        semantic[node] = node['semantic_weight'] * log(len(graph) / node['frequency'])
    
    # Factor 3: Connectivity (betweenness)
    betweenness = nx.betweenness_centrality(graph)
    
    # Factor 4: Information density
    info_density = {}
    for node in graph.nodes:
        # Bits of information per unit
        info_density[node] = node['entropy'] / node['size']
    
    # Combine with weights
    for node in graph.nodes:
        scores[node] = (
            0.3 * pagerank[node] +
            0.3 * normalise(semantic[node]) +
            0.2 * betweenness[node] +
            0.2 * normalise(info_density[node])
        )
    
    return scores
```

### Coverage Contribution

```python
def node_coverage_contribution(
    node: Node,
    source: Graph,
    already_selected: list[Node]
) -> float:
    """
    Marginal coverage contribution of adding node.
    
    Uses submodular function to avoid redundancy:
    - High contribution if node covers new ground
    - Low contribution if overlaps with selected
    """
    # Nodes grounded by this node
    grounded = set(get_grounded_nodes(node, source))
    
    # Already covered by selected nodes
    already_covered = set()
    for selected in already_selected:
        already_covered |= set(get_grounded_nodes(selected, source))
    
    # Marginal contribution
    new_coverage = grounded - already_covered
    
    # Weighted by semantic importance
    contribution = sum(
        source.nodes[n]['semantic_weight']
        for n in new_coverage
    ) / source.total_semantic_weight
    
    return contribution
```

## Level-Specific Algorithms

### L3 → L2: Concept Clustering

```python
def extract_l2_from_l3(l3: Graph) -> Graph:
    """
    Extract L2 concept graph via clustering and Pareto selection.
    """
    # Step 1: Community detection
    communities = louvain_communities(l3, resolution=1.0)
    
    # Step 2: Compute community importance
    community_importance = {}
    for comm in communities:
        # Sum of member importances
        importance = sum(l3.nodes[n]['importance'] for n in comm)
        # Penalise size (prefer compact communities)
        size_penalty = 1.0 / log(1 + len(comm))
        community_importance[comm] = importance * size_penalty
    
    # Step 3: Select communities by Pareto
    selected_communities = pareto_select_communities(
        communities,
        community_importance,
        target_coverage=0.8
    )
    
    # Step 4: Extract representatives
    l2_nodes = []
    for comm in selected_communities:
        # Representative = highest importance member
        rep = max(comm, key=lambda n: l3.nodes[n]['importance'])
        l2_nodes.append(rep)
    
    # Step 5: Build L2 graph with inter-community edges
    l2 = Graph()
    for node in l2_nodes:
        l2.add_node(node, level=2, composite=True)
    
    for n1, n2 in combinations(l2_nodes, 2):
        # Edge if communities have inter-edges in L3
        comm1 = get_community(n1, communities)
        comm2 = get_community(n2, communities)
        
        inter_edges = count_inter_community_edges(comm1, comm2, l3)
        if inter_edges > 0:
            weight = inter_edges / max(len(comm1), len(comm2))
            l2.add_edge(n1, n2, weight=weight)
    
    return l2
```

### L2 → L1: Atomic Extraction

```python
def extract_l1_from_l2(l2: Graph) -> Graph:
    """
    Extract L1 atomic principles via abstraction and Pareto selection.
    """
    # Step 1: Identify atomic candidates
    # Atomic = high explanatory power, low decomposability
    atomic_scores = {}
    for node in l2.nodes:
        # Explanatory power: how many others depend on this?
        ep = len(get_dependents(node, l2)) / len(l2.nodes)
        
        # Decomposability: can this be expressed as others?
        decomp = decomposability_score(node, l2)
        
        # Atomic score = high EP, low decomp
        atomic_scores[node] = ep * (1 - decomp)
    
    # Step 2: Pareto selection of atomics
    l1_candidates = sorted(
        l2.nodes,
        key=lambda n: atomic_scores[n],
        reverse=True
    )
    
    l1_nodes = []
    coverage = 0.0
    
    for node in l1_candidates:
        l1_nodes.append(node)
        coverage += atomic_coverage_contribution(node, l2, l1_nodes)
        
        if coverage >= 0.8:  # Pareto threshold
            break
    
    # Step 3: Build L1 graph
    l1 = Graph()
    for node in l1_nodes:
        l1.add_node(node, level=1, atomic=True)
    
    # Edges: principled interactions
    for n1, n2 in combinations(l1_nodes, 2):
        if principles_interact(n1, n2, l2):
            l1.add_edge(n1, n2, weight=interaction_strength(n1, n2))
    
    return l1
```

### L1 → L0: Schema Generalisation

```python
def extract_l0_from_l1(l1: Graph) -> Schema:
    """
    Extract L0 schema via abductive generalisation.
    """
    # Step 1: Pattern mining across L1 principles
    patterns = mine_patterns(l1, min_support=0.3)
    
    # Step 2: Abductive inference of generalizations
    generalisations = []
    for pattern in patterns:
        # Infer most general form that explains pattern
        gen = abductive_generalise(pattern, l1)
        generalisations.append(gen)
    
    # Step 3: Rank by explanatory breadth
    gen_scores = {}
    for gen in generalisations:
        # How many L1 principles does this explain?
        explained = count_explained(gen, l1)
        gen_scores[gen] = explained / len(l1.nodes)
    
    # Step 4: Pareto selection
    l0_elements = pareto_select(
        generalisations,
        gen_scores,
        target_coverage=0.8,
        max_ratio=0.2
    )
    
    # Step 5: Build schema
    schema = Schema()
    for elem in l0_elements:
        schema.add_element(elem, level=0)
        schema.elements[elem]['subsumes'] = get_subsumed(elem, l1)
    
    # Step 6: Add structural relationships
    for e1, e2 in combinations(l0_elements, 2):
        rel = infer_relationship(e1, e2, l1)
        if rel:
            schema.add_relationship(e1, e2, rel)
    
    return schema
```

## Hyperedge Weighting

```python
def compute_hyperedge_weights(graph: Graph, hyperedges: list) -> dict:
    """
    Compute semantic weights for hyperedges.
    
    Weight = interaction strength of constituent nodes
    """
    weights = {}
    
    for he in hyperedges:
        nodes = he.nodes
        
        # Pairwise interaction strength
        pairwise = sum(
            graph.edges[n1, n2]['weight']
            for n1, n2 in combinations(nodes, 2)
            if graph.has_edge(n1, n2)
        )
        
        # Normalize by hyperedge size
        max_pairs = len(nodes) * (len(nodes) - 1) / 2
        normalised = pairwise / max_pairs if max_pairs > 0 else 0
        
        # Semantic coherence bonus
        coherence = semantic_coherence(nodes, graph)
        
        weights[he] = normalised * coherence
    
    return weights
```

## Convergence Criteria

```python
def check_pareto_convergence(
    current: Graph,
    previous: Graph,
    threshold: float = 0.95
) -> bool:
    """
    Check if Pareto extraction has converged.
    
    Convergence when:
    - Node overlap > threshold
    - Coverage delta < (1 - threshold)
    """
    # Node overlap
    current_nodes = set(current.nodes)
    prev_nodes = set(previous.nodes)
    overlap = len(current_nodes & prev_nodes) / len(current_nodes | prev_nodes)
    
    if overlap < threshold:
        return False
    
    # Coverage stability
    current_coverage = compute_coverage(current)
    prev_coverage = compute_coverage(previous)
    coverage_delta = abs(current_coverage - prev_coverage)
    
    return coverage_delta < (1 - threshold)
```

## Optimisation Variants

### Greedy Pareto (Default)

```python
# Standard greedy selection by importance
result = pareto_extract(graph, target_coverage=0.8)
```

### Diverse Pareto

```python
def diverse_pareto_extract(graph: Graph, diversity_weight: float = 0.3):
    """
    Pareto extraction with diversity constraint.
    Penalizes selecting nodes too similar to already-selected.
    """
    selected = []
    
    for _ in range(target_count):
        scores = {}
        for node in graph.nodes:
            if node in selected:
                continue
            
            importance = importance_scores[node]
            diversity = min(
                1 - similarity(node, s)
                for s in selected
            ) if selected else 1.0
            
            scores[node] = (1 - diversity_weight) * importance + diversity_weight * diversity
        
        best = max(scores, key=scores.get)
        selected.append(best)
    
    return selected
```

### Constrained Pareto

```python
def constrained_pareto_extract(
    graph: Graph,
    must_include: list[Node] = None,
    must_exclude: list[Node] = None
):
    """
    Pareto extraction with hard constraints.
    """
    must_include = must_include or []
    must_exclude = must_exclude or []
    
    # Start with must-include
    selected = list(must_include)
    
    # Exclude forbidden
    candidates = [n for n in graph.nodes if n not in must_exclude]
    
    # Continue standard extraction
    return pareto_extract_from_candidates(
        graph, candidates, initial_selected=selected
    )
```
