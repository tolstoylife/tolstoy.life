# Examples and Templates

Concrete examples of RPP application across domains.

## Example 1: Medical Pharmacology

### Domain: Drug Interactions

```python
# L3: Ground Truth (100% of nodes)
l3_details = """
Warfarin inhibits VKORC1 enzyme
VKORC1 reduces vitamin K epoxide to vitamin K
Vitamin K is cofactor for clotting factor synthesis
Clotting factors II, VII, IX, X require carboxylation
Carboxylation requires vitamin K as cofactor
CYP2C9 metabolizes warfarin
CYP2C9 polymorphisms affect warfarin clearance
NSAIDS inhibit COX enzymes
COX inhibition reduces platelet aggregation
Aspirin irreversibly inhibits COX-1
Warfarin + Aspirin increases bleeding risk
Vitamin K reverses warfarin effect
FFP provides clotting factors directly
Prothrombin complex concentrate contains factors
INR measures anticoagulation effect
Target INR 2-3 for atrial fibrillation
Target INR 2.5-3.5 for mechanical valves
"""

# L2: Concept Graph (20% nodes → 80% coverage)
l2_concepts = {
    "Warfarin_Mechanism": ["VKORC1", "vitamin_K", "clotting_factors"],
    "Drug_Metabolism": ["CYP2C9", "polymorphisms", "clearance"],
    "Bleeding_Risk": ["NSAIDS", "aspirin", "COX"],
    "Reversal_Agents": ["vitamin_K", "FFP", "PCC"],
    "Monitoring": ["INR", "target_ranges"]
}

# L1: Atomic Principles (4% nodes → 64% coverage)
l1_atomics = {
    "Vitamin_K_Antagonism": "Block vitamin K cycle → reduce clotting factors",
    "CYP_Metabolism": "Drug clearance depends on enzyme activity",
    "Additive_Bleeding": "Multiple anticoagulants compound risk"
}

# L0: Schema (0.8% nodes → 51% coverage)
l0_schema = {
    "Anticoagulation_Control": {
        "subsumes": ["Vitamin_K_Antagonism", "CYP_Metabolism", "Additive_Bleeding"],
        "principle": "Balance clotting inhibition against bleeding risk"
    }
}
```

### Generated RPP Structure

```
L0: Anticoagulation_Control
    ├── L1: Vitamin_K_Antagonism
    │   ├── L2: Warfarin_Mechanism
    │   │   ├── L3: Warfarin inhibits VKORC1
    │   │   ├── L3: VKORC1 reduces vitamin K epoxide
    │   │   └── L3: Vitamin K cofactor for synthesis
    │   └── L2: Reversal_Agents
    │       ├── L3: Vitamin K reverses warfarin
    │       ├── L3: FFP provides factors
    │       └── L3: PCC contains factors
    ├── L1: CYP_Metabolism
    │   └── L2: Drug_Metabolism
    │       ├── L3: CYP2C9 metabolizes warfarin
    │       └── L3: Polymorphisms affect clearance
    └── L1: Additive_Bleeding
        ├── L2: Bleeding_Risk
        │   ├── L3: NSAIDS inhibit COX
        │   ├── L3: Aspirin inhibits COX-1
        │   └── L3: Warfarin + Aspirin increases risk
        └── L2: Monitoring
            ├── L3: INR measures effect
            ├── L3: Target 2-3 for AF
            └── L3: Target 2.5-3.5 for valves
```

### Node Ratios

| Ratio | Value | Target | Valid |
|-------|-------|--------|-------|
| L3 nodes | 17 | - | - |
| L2 nodes | 5 | 3-4 | ✓ |
| L1 nodes | 3 | 2-3 | ✓ |
| L0 nodes | 1 | 1-2 | ✓ |
| L1:L2 | 1.67 | 2-3 | ✓ |
| L1:L3 | 5.67 | 6-9 | ✓ |

## Example 2: Software Architecture

### Domain: Microservices Patterns

```python
# L3: Ground Truth
l3_details = """
Services communicate via REST APIs
REST uses HTTP methods GET POST PUT DELETE
Message queues enable async communication
RabbitMQ implements AMQP protocol
Kafka provides durable message streams
Service discovery locates service instances
Consul provides service registry
Load balancers distribute traffic
Circuit breakers prevent cascade failures
Hystrix implements circuit breaker pattern
Retry logic handles transient failures
Exponential backoff prevents thundering herd
API gateways provide single entry point
Kong implements API gateway
Rate limiting prevents overload
Authentication validates identity
OAuth2 provides authorization framework
JWT tokens carry claims
Service mesh manages inter-service traffic
Istio implements service mesh
Sidecars proxy service communication
"""

# L2: Concepts (20%)
l2_concepts = {
    "Communication_Patterns": ["REST", "queues", "async"],
    "Resilience_Patterns": ["circuit_breakers", "retry", "backoff"],
    "Traffic_Management": ["discovery", "load_balancing", "gateway"],
    "Security_Patterns": ["auth", "OAuth2", "JWT"],
    "Infrastructure": ["service_mesh", "sidecars"]
}

# L1: Atomics (4%)
l1_atomics = {
    "Loose_Coupling": "Services communicate through well-defined interfaces",
    "Fault_Isolation": "Failures in one service don't cascade",
    "Observability": "All traffic is monitored and controllable"
}

# L0: Schema (0.8%)
l0_schema = {
    "Distributed_System_Design": {
        "subsumes": ["Loose_Coupling", "Fault_Isolation", "Observability"],
        "principle": "Independent services with resilient communication"
    }
}
```

## Example 3: Machine Learning

### Domain: Neural Network Optimization

```python
# L3: Ground Truth
l3_details = """
Gradient descent minimizes loss function
Learning rate controls step size
High learning rate causes oscillation
Low learning rate slows convergence
Momentum accumulates gradient history
Adam combines momentum and RMSprop
RMSprop adapts per-parameter learning rate
Batch normalization normalizes layer inputs
Dropout randomly zeros activations
Weight decay penalizes large weights
L2 regularization equivalent to weight decay
Early stopping prevents overfitting
Validation loss monitors generalization
Cross-validation estimates performance
Learning rate scheduling adjusts rate
Warmup starts with low learning rate
Cosine annealing oscillates learning rate
Gradient clipping prevents exploding gradients
"""

# L2: Concepts (20%)
l2_concepts = {
    "Optimization_Algorithms": ["gradient_descent", "momentum", "Adam"],
    "Regularization": ["dropout", "weight_decay", "early_stopping"],
    "Learning_Rate_Control": ["scheduling", "warmup", "annealing"],
    "Stability_Techniques": ["batch_norm", "gradient_clipping"]
}

# L1: Atomics (4%)
l1_atomics = {
    "Loss_Minimization": "Iteratively reduce error via gradients",
    "Generalization": "Prevent memorization of training data",
    "Stability": "Maintain bounded activations and gradients"
}

# L0: Schema (0.8%)
l0_schema = {
    "Neural_Network_Training": {
        "subsumes": ["Loss_Minimization", "Generalization", "Stability"],
        "principle": "Optimize parameters while maintaining trainability"
    }
}
```

## Template: RPP Generation

```python
def generate_rpp_from_domain(
    corpus: str,
    domain: str,
    pareto_threshold: float = 0.8
) -> RPPGraph:
    """
    Template for generating RPP from domain corpus.
    """
    # Initialize
    rpp = RPPGenerator(domain=domain)
    
    # Phase 1: Extract L3 (ground truth)
    print("Extracting L3 detail graph...")
    l3 = rpp.extract_l3(corpus)
    print(f"  L3 nodes: {len(l3.nodes)}")
    
    # Phase 2: Construct L2 (concepts)
    print("Constructing L2 concept graph...")
    l2 = rpp.construct_l2(l3, pareto_threshold=pareto_threshold)
    print(f"  L2 nodes: {len(l2.nodes)} ({len(l2.nodes)/len(l3.nodes):.1%} of L3)")
    
    # Validate L2
    coverage = compute_coverage(l2, l3)
    print(f"  L2 coverage: {coverage:.1%}")
    assert coverage >= pareto_threshold, f"L2 coverage {coverage} < {pareto_threshold}"
    
    # Phase 3: Construct L1 (atomics)
    print("Constructing L1 atomic graph...")
    l1 = rpp.construct_l1(l2, pareto_threshold=pareto_threshold)
    print(f"  L1 nodes: {len(l1.nodes)} ({len(l1.nodes)/len(l3.nodes):.1%} of L3)")
    
    # Validate L1
    coverage = compute_coverage(l1, l2)
    print(f"  L1 coverage of L2: {coverage:.1%}")
    
    # Validate ratio
    ratio = len(l2.nodes) / len(l1.nodes)
    print(f"  L1:L2 ratio: {ratio:.2f} (target 2-3)")
    assert 2.0 <= ratio <= 3.0, f"L1:L2 ratio {ratio} outside [2,3]"
    
    # Phase 4: Construct L0 (schema)
    print("Constructing L0 schema...")
    l0 = rpp.construct_l0(l1, pareto_threshold=pareto_threshold)
    print(f"  L0 nodes: {len(l0.nodes)} ({len(l0.nodes)/len(l3.nodes):.2%} of L3)")
    
    # Validate L0
    coverage = compute_coverage(l0, l1)
    print(f"  L0 coverage of L1: {coverage:.1%}")
    
    # Phase 5: Validate complete structure
    print("Validating topology...")
    complete = RPPGraph(l0=l0, l1=l1, l2=l2, l3=l3)
    metrics = validate_topology(complete.unified)
    
    print(f"  η (density): {metrics['eta']:.2f} (target ≥4.0)")
    print(f"  κ (clustering): {metrics['clustering']:.2f} (target >0.3)")
    print(f"  σ (small-world): {metrics['sigma']:.2f} (target >1.0)")
    
    return complete
```

## Output Formats

### JSON Export

```python
def export_rpp_json(rpp: RPPGraph) -> dict:
    """Export RPP to JSON format."""
    return {
        "metadata": {
            "domain": rpp.domain,
            "pareto_chain": [0.8, 0.64, 0.51],
            "node_counts": {
                "l0": len(rpp.l0.nodes),
                "l1": len(rpp.l1.nodes),
                "l2": len(rpp.l2.nodes),
                "l3": len(rpp.l3.nodes)
            }
        },
        "levels": {
            "l0": serialize_level(rpp.l0),
            "l1": serialize_level(rpp.l1),
            "l2": serialize_level(rpp.l2),
            "l3": serialize_level(rpp.l3)
        },
        "edges": serialize_edges(rpp),
        "topology": {
            "eta": compute_eta(rpp.unified),
            "clustering": compute_clustering(rpp.unified),
            "small_world": compute_small_world(rpp.unified)
        }
    }
```

### OWL Ontology Export

```python
def export_rpp_owl(rpp: RPPGraph, namespace: str) -> str:
    """Export RPP to OWL ontology format."""
    owl = OWLOntology(namespace=namespace)
    
    # L0 as top-level classes
    for node in rpp.l0.nodes:
        owl.add_class(node, parent="owl:Thing")
    
    # L1 as subclasses of L0
    for node in rpp.l1.nodes:
        parent = get_parent(node, rpp.l0)
        owl.add_class(node, parent=parent)
    
    # L2 as subclasses of L1
    for node in rpp.l2.nodes:
        parent = get_parent(node, rpp.l1)
        owl.add_class(node, parent=parent)
    
    # L3 as individuals
    for node in rpp.l3.nodes:
        parent = get_parent(node, rpp.l2)
        owl.add_individual(node, class_type=parent)
    
    return owl.serialize(format="xml")
```

### Mermaid Diagram Export

```python
def export_rpp_mermaid(rpp: RPPGraph) -> str:
    """Export RPP to Mermaid diagram."""
    lines = ["graph TD"]
    
    # Style levels differently
    lines.append("  classDef l0 fill:#f9f,stroke:#333")
    lines.append("  classDef l1 fill:#bbf,stroke:#333")
    lines.append("  classDef l2 fill:#bfb,stroke:#333")
    lines.append("  classDef l3 fill:#fff,stroke:#333")
    
    # Add nodes with levels
    for level, level_class in [
        (rpp.l0, "l0"),
        (rpp.l1, "l1"),
        (rpp.l2, "l2"),
        (rpp.l3, "l3")
    ]:
        for node in level.nodes:
            lines.append(f"  {node}:::{level_class}")
    
    # Add edges
    for u, v in rpp.all_edges():
        lines.append(f"  {u} --> {v}")
    
    return "\n".join(lines)
```

## Validation Checklist

### Before Generation
- [ ] Corpus is domain-relevant and comprehensive
- [ ] Domain keyword specified
- [ ] Pareto threshold set (default 0.8)

### After L3 Extraction
- [ ] Entities extracted correctly
- [ ] Relationships identified
- [ ] Semantic weights computed

### After L2 Construction
- [ ] Node count ≈ 20% of L3
- [ ] Coverage ≥ 80% of L3
- [ ] Clusters are semantically coherent

### After L1 Construction
- [ ] Node count ≈ 4% of L3
- [ ] Coverage ≥ 64% of L3
- [ ] Principles are truly atomic
- [ ] L1:L2 ratio ∈ [2, 3]

### After L0 Construction
- [ ] Node count ≈ 0.8% of L3
- [ ] Coverage ≥ 51% of L3
- [ ] Schema is coherent
- [ ] Deductive validation passes

### Final Validation
- [ ] η (density) ≥ 4.0
- [ ] κ (clustering) > 0.3
- [ ] σ (small-world) > 1.0
- [ ] No orphan nodes
- [ ] Bridge edges present
