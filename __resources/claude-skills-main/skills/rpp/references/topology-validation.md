# Topology Validation

Procedures for validating RPP graph topology, small-world properties, and structural invariants.

## Topology Metrics

### Edge Density (η)

```python
def compute_eta(graph: Graph) -> float:
    """
    Edge density: average edges per node.
    
    Target: η ≥ 4.0
    """
    return len(graph.edges) / len(graph.nodes)
```

### Clustering Coefficient (κ)

```python
def compute_clustering(graph: Graph) -> float:
    """
    Average local clustering coefficient.
    
    Target: κ > 0.3 (small-world property)
    """
    coefficients = []
    for node in graph.nodes:
        neighbors = list(graph.neighbors(node))
        if len(neighbors) < 2:
            coefficients.append(0.0)
            continue
        
        # Count edges between neighbors
        possible_edges = len(neighbors) * (len(neighbors) - 1) / 2
        actual_edges = sum(
            1 for i, n1 in enumerate(neighbors)
            for n2 in neighbors[i+1:]
            if graph.has_edge(n1, n2)
        )
        
        coefficients.append(actual_edges / possible_edges)
    
    return sum(coefficients) / len(coefficients)
```

### Isolation Ratio (φ)

```python
def compute_isolation(graph: Graph) -> float:
    """
    Proportion of orphan/isolated nodes.
    
    Target: φ < 0.2
    """
    isolated = sum(1 for n in graph.nodes if graph.degree(n) == 0)
    return isolated / len(graph.nodes)
```

### Small-World Coefficient (σ)

```python
def compute_small_world(graph: Graph) -> float:
    """
    Small-world coefficient: C/C_random / L/L_random
    
    σ > 1 indicates small-world network.
    """
    # Real metrics
    C_real = compute_clustering(graph)
    L_real = average_path_length(graph)
    
    # Random graph baseline (Erdős-Rényi)
    n = len(graph.nodes)
    p = 2 * len(graph.edges) / (n * (n - 1))
    C_random = p
    L_random = math.log(n) / math.log(n * p) if p > 0 else float('inf')
    
    # Small-world coefficient
    if C_random == 0 or L_real == 0:
        return 0.0
    
    sigma = (C_real / C_random) / (L_real / L_random)
    return sigma
```

## Node Ratio Validation

### L1:L2 Ratio

```python
def validate_l1_l2_ratio(l1: Graph, l2: Graph) -> ValidationResult:
    """
    Atomic to composite ratio.
    
    Target: 2-3:1 (each L2 composite from 2-3 L1 atomics)
    """
    ratio = len(l2.nodes) / len(l1.nodes)
    
    return ValidationResult(
        metric='l1_l2_ratio',
        value=ratio,
        target=(2.0, 3.0),
        valid=2.0 <= ratio <= 3.0,
        message=f"L1:L2 ratio = {ratio:.2f} (target 2-3:1)"
    )
```

### L1:L3 Ratio

```python
def validate_l1_l3_ratio(l1: Graph, l3: Graph) -> ValidationResult:
    """
    Atomic to detail ratio.
    
    Target: 6-9:1 (reflecting Pareto squared compression)
    """
    ratio = len(l3.nodes) / len(l1.nodes)
    
    return ValidationResult(
        metric='l1_l3_ratio',
        value=ratio,
        target=(6.0, 9.0),
        valid=6.0 <= ratio <= 9.0,
        message=f"L1:L3 ratio = {ratio:.2f} (target 6-9:1)"
    )
```

### Coverage Validation

```python
def validate_pareto_coverage(level: Graph, parent_level: Graph) -> ValidationResult:
    """
    Verify Pareto coverage at each level.
    
    Target: 20% nodes → 80% coverage
    """
    # Compute semantic coverage
    total_semantic_weight = sum(n['weight'] for n in parent_level.nodes)
    covered_weight = sum(
        parent_level.nodes[n]['weight']
        for n in parent_level.nodes
        if is_grounded_by(n, level)
    )
    
    coverage = covered_weight / total_semantic_weight
    node_ratio = len(level.nodes) / len(parent_level.nodes)
    
    return ValidationResult(
        metric='pareto_coverage',
        value={'coverage': coverage, 'node_ratio': node_ratio},
        target={'coverage': 0.8, 'node_ratio': 0.2},
        valid=coverage >= 0.8 and node_ratio <= 0.2,
        message=f"{node_ratio:.1%} nodes → {coverage:.1%} coverage"
    )
```

## Structural Validation

### Cross-Level Edges

```python
def validate_cross_level_edges(rpp: RPPGraph) -> ValidationResult:
    """
    Verify proper parent-child relationships across levels.
    """
    errors = []
    
    for level_pair in [(rpp.l0, rpp.l1), (rpp.l1, rpp.l2), (rpp.l2, rpp.l3)]:
        parent_level, child_level = level_pair
        
        # Each parent should have children
        for parent in parent_level.nodes:
            children = get_children(parent, child_level)
            if not children:
                errors.append(f"Node {parent} has no children")
            elif not (2 <= len(children) <= 3):
                errors.append(f"Node {parent} has {len(children)} children (target 2-3)")
        
        # Each child should have parent
        for child in child_level.nodes:
            parents = get_parents(child, parent_level)
            if not parents:
                errors.append(f"Node {child} is orphan (no parent)")
    
    return ValidationResult(
        metric='cross_level_edges',
        valid=len(errors) == 0,
        errors=errors
    )
```

### Bridge Edges

```python
def validate_bridge_edges(rpp: RPPGraph) -> ValidationResult:
    """
    Verify orthogonal cross-hierarchical connections exist.
    """
    bridges = []
    
    for n1 in rpp.all_nodes():
        for n2 in rpp.all_nodes():
            if n1['level'] != n2['level'] and abs(n1['level'] - n2['level']) > 1:
                if rpp.has_edge(n1, n2):
                    bridges.append((n1, n2))
    
    # Should have some bridges for small-world property
    bridge_ratio = len(bridges) / len(rpp.all_edges())
    
    return ValidationResult(
        metric='bridge_edges',
        value=bridge_ratio,
        target=(0.05, 0.15),  # 5-15% of edges should be bridges
        valid=0.05 <= bridge_ratio <= 0.15,
        message=f"Bridge edge ratio: {bridge_ratio:.1%}"
    )
```

### Lattice Structure

```python
def validate_lattice_structure(level: Graph) -> ValidationResult:
    """
    Verify structured lattice interconnections within level.
    """
    # Check for regular patterns
    degree_sequence = [level.degree(n) for n in level.nodes]
    mean_degree = sum(degree_sequence) / len(degree_sequence)
    variance = sum((d - mean_degree)**2 for d in degree_sequence) / len(degree_sequence)
    
    # Low variance indicates lattice-like regularity
    cv = (variance ** 0.5) / mean_degree  # Coefficient of variation
    
    return ValidationResult(
        metric='lattice_structure',
        value=cv,
        target=(0.0, 0.5),  # Low CV indicates regularity
        valid=cv <= 0.5,
        message=f"Degree CV: {cv:.2f} (lower = more lattice-like)"
    )
```

## Comprehensive Validation

```python
def validate_rpp_topology(rpp: RPPGraph) -> TopologyReport:
    """
    Run all topology validations.
    """
    report = TopologyReport()
    
    # Core metrics
    report.add(compute_eta(rpp.unified_graph))
    report.add(compute_clustering(rpp.unified_graph))
    report.add(compute_isolation(rpp.unified_graph))
    report.add(compute_small_world(rpp.unified_graph))
    
    # Node ratios
    report.add(validate_l1_l2_ratio(rpp.l1, rpp.l2))
    report.add(validate_l1_l3_ratio(rpp.l1, rpp.l3))
    
    # Pareto coverage
    report.add(validate_pareto_coverage(rpp.l2, rpp.l3))
    report.add(validate_pareto_coverage(rpp.l1, rpp.l2))
    report.add(validate_pareto_coverage(rpp.l0, rpp.l1))
    
    # Structural
    report.add(validate_cross_level_edges(rpp))
    report.add(validate_bridge_edges(rpp))
    report.add(validate_lattice_structure(rpp.l2))
    
    return report
```

## Remediation Actions

```python
REMEDIATION = {
    'η < 4.0': {
        'action': 'add_edges',
        'procedure': 'Identify high-importance node pairs, add weighted edges',
        'tool': 'infranodus.generateContentGaps()'
    },
    'κ < 0.3': {
        'action': 'triangulate',
        'procedure': 'Find open triads, close with weighted edges',
        'tool': 'graph.triangulate()'
    },
    'φ > 0.2': {
        'action': 'connect_orphans',
        'procedure': 'Link isolated nodes to nearest neighbors by semantic similarity',
        'tool': 'abduct.connect_orphans()'
    },
    'σ < 1.0': {
        'action': 'add_bridges',
        'procedure': 'Add cross-hierarchical shortcuts',
        'tool': 'infranodus.getGraphAndAdvice(optimize="bridges")'
    },
    'ratio_violation': {
        'action': 'rebalance_levels',
        'procedure': 'Adjust Pareto threshold, re-extract levels',
        'tool': 'rpp.reconstruct(pareto_threshold=adjusted)'
    }
}
```

## Integration with graph Skill

```python
# Use graph skill for topology validation
from graph import validate_topology, remediate_topology

# Validate
metrics = validate_topology(rpp.unified_graph, require_eta=4.0)

if not metrics['valid']:
    # Remediate
    remediated = remediate_topology(
        rpp.unified_graph,
        target_eta=4.0,
        target_clustering=0.3
    )
```
