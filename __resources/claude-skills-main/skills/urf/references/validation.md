# URF Quality Assurance Systems

## Severity-Based Validation Levels

### L1-3: Minimal Validation (LOW severity)
```yaml
scope:
  coverage: basic_sanity_checks
  depth: surface_level
  time_budget: <10ms
  confidence_target: >0.7

checks:
  input:
    - null_check: input != null
    - type_check: isinstance(input, expected_type)
    - range_check: min <= value <= max
    
  output:
    - structure: has_required_fields
    - coherence: no_internal_contradictions
    - completeness: all_questions_answered
```

### L4-6: Standard Validation (MEDIUM severity)
```yaml
scope:
  coverage: comprehensive_checking
  depth: detailed_analysis
  time_budget: <100ms
  confidence_target: >0.85

checks:
  data_quality:
    - completeness: missing_value_analysis
    - consistency: cross_field_validation
    - accuracy: reference_data_comparison
    
  logic:
    - correctness: algorithm_verification
    - coherence: reasoning_chain_valid
    - assumptions: explicitly_tested
    - edge_cases: comprehensively_covered
    
  integration:
    - interfaces: contract_compliance
    - dependencies: version_compatibility
    - state: consistency_maintained
```

### L7-9: High-Stakes Validation (HIGH severity)
```yaml
scope:
  coverage: exhaustive_verification
  depth: formal_proof_level
  time_budget: <1000ms
  confidence_target: >0.95

checks:
  formal_methods:
    - specification: TLA+ | Alloy
    - verification: model_checking | theorem_proving
    
  statistical:
    - hypothesis_testing: null_rejection
    - confidence_intervals: parameter_bounds
    - power_analysis: sample_adequacy
    
  simulation:
    - monte_carlo: uncertainty_propagation
    - stress_testing: extreme_conditions
    - chaos_engineering: failure_injection
```

### L10: Critical Validation
```yaml
scope:
  coverage: absolute_certainty_required
  depth: mathematical_proof
  time_budget: unlimited_if_needed
  confidence_target: >0.99

checks:
  theorem_proving:
    systems: [Coq, Isabelle, Lean]
    techniques: [induction, coinduction, contradiction]
    
  safety_critical:
    standards: [DO-178C, ISO-26262, IEC-61508]
    
  failure_analysis:
    - FMEA: failure_modes_effects
    - FTA: fault_tree
    - HAZOP: hazard_operability
```

---

## Γ-Topology Invariants

### η-Density (≥4)
```python
def validate_density(graph):
    """Knowledge graph must have |E|/|V| ≥ 4."""
    ratio = len(graph.edges) / len(graph.nodes)
    if ratio < 4.0:
        return ValidationFailure(
            metric="η",
            value=ratio,
            target=4.0,
            remediation="invoke infranodus:getGraphAndAdvice with optimize='gaps'"
        )
    return ValidationSuccess(metric="η", value=ratio)
```

### ζ-Acyclicity (=0)
```python
def validate_acyclic(graph):
    """DAG structure required for reasoning graphs."""
    cycles = find_cycles(graph)
    if cycles:
        return ValidationFailure(
            metric="ζ",
            value=len(cycles),
            target=0,
            remediation="invoke abduct.refactor with cycle_breaking=True"
        )
    return ValidationSuccess(metric="ζ", value=0)
```

### κ-Clustering (>0.3)
```python
def validate_clustering(graph):
    """Small-world property for emergent reasoning."""
    coeff = clustering_coefficient(graph)
    if coeff <= 0.3:
        return ValidationFailure(
            metric="κ",
            value=coeff,
            target=0.3,
            remediation="invoke graph.add_triangulation"
        )
    return ValidationSuccess(metric="κ", value=coeff)
```

### φ-Connectivity (<0.2)
```python
def validate_connectivity(graph):
    """Maximum 20% isolated nodes."""
    isolated = len([n for n in graph.nodes if graph.degree(n) == 0])
    ratio = isolated / len(graph.nodes)
    if ratio >= 0.2:
        return ValidationFailure(
            metric="φ",
            value=ratio,
            target=0.2,
            remediation="invoke graph.connect_orphans"
        )
    return ValidationSuccess(metric="φ", value=ratio)
```

---

## χ-KROG Constraint Validation

```python
def validate_krog(action):
    """
    Valid(λ) ⟺ K(λ) ∧ R(λ) ∧ O(λ) ∧ G(λ)
    """
    results = {}
    
    # K: Knowable - Effects must be transparent and auditable
    results["K"] = (
        action.effects_visible and 
        action.auditable and
        action.side_effects_documented
    )
    
    # R: Rights - Agent has authority over domain
    results["R"] = (
        action.agent.has_privilege(action.domain) and
        action.agent.has_power(action.scope)
    )
    
    # O: Obligations - All duties satisfied
    results["O"] = all(
        not duty.violated 
        for duty in action.active_duties
    )
    
    # G: Governance - Within meta-bounds
    results["G"] = (
        action in action.governance_boundary and
        not action.violates_constitutive_constraints
    )
    
    valid = all(results.values())
    return KROGResult(valid=valid, components=results)
```

---

## Evidence Hierarchies

| Level | Certainty | Definition | Validation |
|-------|-----------|------------|------------|
| 10 | AXIOMATIC | True by definition, logical necessity | Formal verification |
| 8-9 | EMPIRICAL | Observable, measurable, reproducible | Statistical significance |
| 5-7 | THEORETICAL | Model-based, internally consistent | Consistency + prediction |
| 2-4 | HEURISTIC | Experience-based, practically useful | Success rate tracking |
| 0-1 | SPECULATIVE | Hypothetical, exploratory | Internal consistency only |

---

## Validation Gates

### Entry Criteria
```python
def check_entry(context):
    return {
        "prerequisites_met": all_dependencies_ready(context),
        "resources_available": check_resources(context),
        "configuration_valid": validate_params(context),
    }
```

### Exit Criteria
```python
def check_exit(result):
    return {
        "tests_passed": result.success_rate == 1.0,
        "performance_met": result.latency <= target,
        "quality_achieved": result.accuracy >= threshold,
        "documented": result.has_rationale,
    }
```

### Approval Process
```python
APPROVAL_MATRIX = {
    "routine": "automated_approval",
    "standard": "delegated_authority",
    "exceptional": "escalated_decision",
    "critical": "committee_consensus",
}
```

---

## Convergence Detection

```python
def check_convergence(state, previous, pipeline):
    """Multi-level stability detection."""
    
    weights = {
        "strategic": 0.5,
        "tactical": 0.3,
        "operational": 0.2
    }
    
    similarity = sum(
        w * cosine_similarity(
            getattr(state, level),
            getattr(previous, level)
        )
        for level, w in weights.items()
    )
    
    thresholds = {
        "R1": 0.85,
        "R2": 0.92,
        "R3": 0.96
    }
    
    return ConvergenceResult(
        converged=similarity > thresholds[pipeline],
        score=similarity,
        threshold=thresholds[pipeline]
    )
```
