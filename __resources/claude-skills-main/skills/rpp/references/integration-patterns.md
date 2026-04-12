# Integration Patterns

Workflows for composing RPP with other skills.

## Skill Composition Algebra

```haskell
-- Sequential: output of A feeds B
(∘) :: Skill → Skill → Skill
rpp ∘ graph = λx. graph.validate(rpp.generate(x))

-- Parallel: run simultaneously
(⊗) :: Skill → Skill → Skill
rpp ⊗ infranodus = λx. (rpp.generate(x), infranodus.analyze(x))

-- Conditional: route based on predicate
(|) :: Skill → Predicate → Skill → Skill
rpp | complex | mega = λx. if complex(x) then mega.extend(rpp(x)) else rpp(x)

-- Recursive: apply until convergence
fix :: Skill → Skill
fix rpp = λx. let y = rpp(x) in if converged(y) then y else fix(rpp)(y)
```

## Core Integration Patterns

### Pattern 1: RPP + graph (Topology Validation)

```python
# Full workflow with topology validation
def rpp_with_validation(corpus: str, domain: str) -> ValidatedRPP:
    """
    Generate RPP graph with topology validation via graph skill.
    """
    from graph import validate_topology, remediate_topology
    
    # Step 1: Generate RPP structure
    rpp = RPPGenerator(domain=domain)
    rpp_graph = rpp.generate(corpus)
    
    # Step 2: Validate topology
    metrics = validate_topology(
        rpp_graph.unified,
        require_eta=4.0,
        require_clustering=0.3
    )
    
    # Step 3: Remediate if needed
    if not metrics['valid']:
        rpp_graph = remediate_topology(
            rpp_graph,
            target_eta=4.0,
            preserve_levels=True
        )
    
    return ValidatedRPP(graph=rpp_graph, metrics=metrics)
```

### Pattern 2: RPP + abduct (Schema Refactoring)

```python
# Schema optimisation via abductive refactoring
def rpp_with_refactoring(corpus: str, existing_schema: Schema = None) -> RPPGraph:
    """
    Generate RPP with abductive schema refinement.
    """
    from abduct import refactor_schema, detect_patterns
    
    # Step 1: Generate initial RPP
    rpp = RPPGenerator()
    initial = rpp.generate(corpus)
    
    # Step 2: Detect patterns for refactoring
    patterns = detect_patterns(initial.l0)
    
    # Step 3: Refactor schema abductively
    refined_l0 = refactor_schema(
        initial.l0,
        patterns=patterns,
        target_compression=0.8
    )
    
    # Step 4: Propagate changes down hierarchy
    refined = propagate_schema_changes(initial, refined_l0)
    
    return refined
```

### Pattern 3: RPP + mega (SuperHyperGraph Extension)

```python
# Extend to n-SuperHyperGraphs for complex domains
def rpp_with_mega(corpus: str, complexity_threshold: float = 0.8) -> ExtendedRPP:
    """
    Extend RPP to SuperHyperGraph when complexity warrants.
    """
    from mega import extend_to_superhypergraph, assess_complexity
    
    # Step 1: Generate base RPP
    rpp = RPPGenerator()
    base = rpp.generate(corpus)
    
    # Step 2: Assess complexity
    complexity = assess_complexity(base)
    
    # Step 3: Extend if needed
    if complexity > complexity_threshold:
        extended = extend_to_superhypergraph(
            base,
            max_hyperedge_arity=5,
            preserve_pareto=True
        )
        return ExtendedRPP(base=base, extended=extended, is_super=True)
    
    return ExtendedRPP(base=base, extended=None, is_super=False)
```

### Pattern 4: RPP + infranodus (Gap Detection)

```python
# Structural gap detection and bridge suggestion
def rpp_with_gap_analysis(corpus: str) -> EnrichedRPP:
    """
    Generate RPP with structural gap analysis via InfraNodus.
    """
    # Step 1: Generate RPP
    rpp = RPPGenerator()
    graph = rpp.generate(corpus)
    
    # Step 2: Analyze gaps via InfraNodus MCP
    gaps = mcp__infranodus__generateContentGaps(
        text=graph.to_text_representation()
    )
    
    # Step 3: Get bridge suggestions
    advice = mcp__infranodus__getGraphAndAdvice(
        text=graph.to_text_representation(),
        optimize="gaps"
    )
    
    # Step 4: Apply bridge suggestions
    for bridge in advice['suggested_bridges']:
        graph.add_bridge_edge(
            source=bridge['from'],
            target=bridge['to'],
            weight=bridge['strength']
        )
    
    return EnrichedRPP(graph=graph, gaps=gaps, bridges=advice)
```

### Pattern 5: RPP + non-linear (Uncertainty Handling)

```python
# Handle uncertainty in RPP generation
def rpp_with_uncertainty(corpus: str, confidence_threshold: float = 0.7) -> UncertainRPP:
    """
    Generate RPP with uncertainty quantification via non-linear skill.
    """
    from non_linear import NoisyGraph, uncertainty_propagate
    
    # Step 1: Generate base RPP with uncertainty tracking
    rpp = RPPGenerator(track_uncertainty=True)
    base = rpp.generate(corpus)
    
    # Step 2: Wrap in NoisyGraph scaffold
    noisy = NoisyGraph(base.unified)
    
    # Step 3: Propagate uncertainty through levels
    for level in [base.l3, base.l2, base.l1, base.l0]:
        uncertainty_propagate(level, noisy)
    
    # Step 4: Filter low-confidence elements
    confident_graph = noisy.filter(
        confidence_threshold=confidence_threshold
    )
    
    return UncertainRPP(
        graph=confident_graph,
        uncertainty_map=noisy.uncertainty_map,
        confidence_threshold=confidence_threshold
    )
```

## Composite Workflows

### Workflow 1: Full Research Pipeline

```python
def research_pipeline(corpus: str, domain: str) -> ResearchOutput:
    """
    Complete research pipeline:
    RPP → graph validation → gap analysis → refinement
    """
    # Phase 1: Generate RPP
    rpp = RPPGenerator(domain=domain)
    initial = rpp.generate(corpus)
    
    # Phase 2: Validate topology (graph skill)
    from graph import validate_topology
    metrics = validate_topology(initial.unified, require_eta=4.0)
    
    # Phase 3: Gap analysis (infranodus)
    gaps = mcp__infranodus__generateContentGaps(initial.to_text())
    questions = mcp__infranodus__generateResearchQuestions(
        text=initial.to_text(),
        useSeveralGaps=True
    )
    
    # Phase 4: Refine based on gaps (abduct)
    from abduct import refactor_with_gaps
    refined = refactor_with_gaps(initial, gaps)
    
    # Phase 5: Final validation
    final_metrics = validate_topology(refined.unified, require_eta=4.0)
    
    return ResearchOutput(
        graph=refined,
        gaps=gaps,
        research_questions=questions,
        metrics=final_metrics
    )
```

### Workflow 2: Domain Ontology Construction

```python
def ontology_construction(
    corpus: str,
    domain: str,
    existing_ontology: Schema = None
) -> DomainOntology:
    """
    Construct domain ontology via RPP with validation.
    """
    # Phase 1: Extract ground truth (L3)
    rpp = RPPGenerator(domain=domain)
    l3 = rpp.extract_l3(corpus)
    
    # Phase 2: Build levels with validation
    l2 = rpp.construct_l2(l3)
    assert validate_pareto_coverage(l2, l3)
    
    l1 = rpp.construct_l1(l2)
    assert validate_pareto_coverage(l1, l2)
    assert validate_l1_l2_ratio(l1, l2)
    
    # Phase 3: Generate schema (L0)
    if existing_ontology:
        # Integrate with existing
        l0 = rpp.construct_l0(l1, seed_schema=existing_ontology)
    else:
        l0 = rpp.construct_l0(l1)
    
    # Phase 4: Validate complete structure
    from graph import validate_topology
    complete = RPPGraph(l0=l0, l1=l1, l2=l2, l3=l3)
    metrics = validate_topology(complete.unified, require_eta=4.0)
    
    # Phase 5: Export as formal ontology
    ontology = export_as_ontology(complete, format='owl')
    
    return DomainOntology(
        rpp=complete,
        ontology=ontology,
        metrics=metrics
    )
```

### Workflow 3: Iterative Refinement

```python
def iterative_refinement(
    corpus: str,
    max_iterations: int = 5,
    convergence_threshold: float = 0.95
) -> RefinedRPP:
    """
    Iteratively refine RPP until convergence.
    """
    rpp = RPPGenerator()
    current = rpp.generate(corpus)
    
    for i in range(max_iterations):
        # Step 1: Identify weaknesses
        gaps = mcp__infranodus__generateContentGaps(current.to_text())
        
        # Step 2: Refine via abduct
        from abduct import refactor_schema
        refined = refactor_schema(current, gaps=gaps)
        
        # Step 3: Validate topology
        from graph import validate_topology
        metrics = validate_topology(refined.unified)
        
        # Step 4: Check convergence
        similarity = graph_similarity(current, refined)
        if similarity > convergence_threshold and metrics['valid']:
            return RefinedRPP(
                graph=refined,
                iterations=i + 1,
                converged=True,
                metrics=metrics
            )
        
        current = refined
    
    return RefinedRPP(
        graph=current,
        iterations=max_iterations,
        converged=False,
        metrics=metrics
    )
```

## MCP Tool Integration

### InfraNodus MCP Tools

```python
# Available InfraNodus MCP tools for RPP integration

# Generate knowledge graph and analyze
result = mcp__infranodus__generateKnowledgeGraph(
    text=corpus,
    includeGraph=True,
    includeStatements=True
)

# Detect content gaps
gaps = mcp__infranodus__generateContentGaps(
    text=corpus
)

# Generate research questions from gaps
questions = mcp__infranodus__generateResearchQuestions(
    text=corpus,
    useSeveralGaps=True,
    gapDepth=2
)

# Get advice for graph optimization
advice = mcp__infranodus__getGraphAndAdvice(
    text=corpus,
    optimize="gaps"  # or "bridges", "clusters"
)

# Compare two texts
comparison = mcp__infranodus__overlapBetweenTexts(
    contexts=[
        {"text": corpus1},
        {"text": corpus2}
    ]
)

# Find differences
diff = mcp__infranodus__differenceBetweenTexts(
    contexts=[
        {"text": target},
        {"text": reference}
    ]
)
```

## Skill Routing Table

| User Intent | Primary Skill | Supporting Skills |
|-------------|---------------|-------------------|
| "Create schema" | rpp | graph, abduct |
| "Generate ontology" | rpp | graph, mega |
| "Find knowledge gaps" | rpp + infranodus | graph |
| "Validate structure" | graph | rpp |
| "Refactor schema" | abduct | rpp, graph |
| "Handle complexity" | mega | rpp, graph |
| "Quantify uncertainty" | non-linear | rpp |

## Error Handling

```python
def safe_rpp_generation(corpus: str, **kwargs) -> Result:
    """
    RPP generation with comprehensive error handling.
    """
    try:
        # Generate
        rpp = RPPGenerator(**kwargs)
        graph = rpp.generate(corpus)
        
        # Validate
        metrics = validate_topology(graph.unified)
        
        if not metrics['valid']:
            # Attempt remediation
            graph = remediate_topology(graph)
            metrics = validate_topology(graph.unified)
        
        return Result(success=True, graph=graph, metrics=metrics)
    
    except ParetoCoverageError as e:
        # Coverage threshold not achievable
        return Result(
            success=False,
            error="Pareto coverage not achievable",
            suggestion="Lower target_coverage or expand corpus"
        )
    
    except TopologyViolation as e:
        # Graph structure invalid
        return Result(
            success=False,
            error=f"Topology violation: {e}",
            suggestion="Use graph skill for remediation"
        )
    
    except RatioConstraintError as e:
        # Node ratios outside bounds
        return Result(
            success=False,
            error=f"Ratio constraint violated: {e}",
            suggestion="Adjust pareto_threshold parameters"
        )
```
