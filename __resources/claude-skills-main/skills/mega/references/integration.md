# MEGA v2.0 Integration Reference
## Skill Composition and Tool Connectivity

<overview>
MEGA v2.0 integrates with the broader skill ecosystem through well-defined interfaces. This reference specifies how MEGA composes with other skills (γ, ω, η, ν, ι, β) and external tools (InfraNodus, Obsidian, MCP servers).
</overview>

---

## 1. SKILL COMPOSITION MAP

<composition_diagram>
```
MEGA SKILL COMPOSITION
══════════════════════

                    ┌──────────────────────┐
                    │   μ (orchestrator)   │
                    │   Route queries      │
                    └──────────┬───────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
            ▼                  ▼                  ▼
    ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
    │  ι (infranodus)│  │   MEGA Core   │  │  β (abduct)   │
    │  Gap detection │  │   Structure   │  │  Refactoring  │
    └───────┬───────┘  └───────┬───────┘  └───────┬───────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
            ▼                  ▼                  ▼
    ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
    │  γ (graph)    │  │  ω (ontolog)  │  │  η (hier.)    │
    │  Compression  │  │  Encoding     │  │  Levels       │
    └───────────────┘  └───────────────┘  └───────────────┘
                               │
                               ▼
                    ┌───────────────────┐
                    │  ν (non-linear)   │
                    │  Uncertainty prop │
                    └───────────────────┘
```
</composition_diagram>

---

## 2. SKILL INTERFACE SPECIFICATIONS

<graph_skill>
```python
# γ (graph) — Compression and extraction
# MEGA provides: structure to compress
# γ provides: quotient algorithms, η validation

from typing import Protocol

class GraphSkillInterface(Protocol):
    def extract(self, text: str) -> 'nSHG':
        """Extract graph from text."""
        ...
    
    def compress(self, graph: 'nSHG', quotient_type: str = 'bisimulation') -> 'nSHG':
        """Apply structural compression."""
        ...
    
    def validate_eta(self, graph: 'nSHG') -> tuple[float, bool]:
        """Check edge density invariant."""
        ...

# MEGA ↔ γ composition
def mega_with_graph(text: str, query: str) -> 'MEGAHolon':
    """
    Compose MEGA with graph extraction/compression.
    """
    # γ extracts initial structure
    initial = graph_skill.extract(text)
    
    # MEGA adds levels, uncertainty, correlations
    mega = build_n_shg(initial, n=determine_level(initial))
    mega = add_uncertainty_attributes(mega)
    
    # γ compresses if needed
    if mega.eta > 6:  # Over-connected, compress
        mega = graph_skill.compress(mega)
    
    # MEGA decohere for query
    return decohere(mega, query)
```
</graph_skill>

<ontolog_skill>
```python
# ω (ontolog) — Simplicial complex encoding
# MEGA provides: n-SHG structure
# ω provides: Σ-complex representation, persistent homology

class OntologSkillInterface(Protocol):
    def encode_simplicial(self, graph: 'nSHG') -> 'SimplicialComplex':
        """Encode graph as simplicial complex."""
        ...
    
    def compute_homology(self, K: 'SimplicialComplex') -> list[int]:
        """Compute Betti numbers."""
        ...
    
    def detect_holes(self, K: 'SimplicialComplex') -> list['Hole']:
        """Identify topological holes (missing structure)."""
        ...

# MEGA ↔ ω composition
def mega_with_ontolog(mega: 'nSHG') -> 'EnrichedMEGA':
    """
    Enrich MEGA with topological features from ontolog.
    """
    # ω encodes as simplicial complex
    K = ontolog_skill.encode_simplicial(mega)
    
    # Level mapping: MEGA levels → simplicial dimension
    # L0 → 0-simplices (vertices)
    # L1 → 1-simplices (edges)  
    # L2 → 2-simplices (triangles/faces)
    # L3 → 3-simplices (tetrahedra)
    
    # Detect holes = missing relationships
    holes = ontolog_skill.detect_holes(K)
    
    # Map holes back to MEGA bridging opportunities
    for hole in holes:
        mega.suggested_bridges.append(hole.boundary_nodes)
    
    return mega
```
</ontolog_skill>

<hierarchical_skill>
```python
# η (hierarchical) — Strategic/tactical/operational decomposition
# MEGA provides: n-level structure
# η provides: S→T→O reasoning pattern

class HierarchicalSkillInterface(Protocol):
    def strategic_reason(self, context: 'nSHG', query: str) -> 'StrategicPlan':
        """Why: high-level goals and constraints."""
        ...
    
    def tactical_plan(self, strategy: 'StrategicPlan') -> 'TacticalApproach':
        """How: approaches and trade-offs."""
        ...
    
    def operational_execute(self, tactics: 'TacticalApproach') -> 'OperationalSteps':
        """What: concrete actions."""
        ...

# MEGA ↔ η composition
def mega_with_hierarchical(mega: 'nSHG', query: str) -> 'MEGAHolon':
    """
    Apply hierarchical reasoning to MEGA structure.
    
    Key insight: MEGA levels ≈ reasoning levels
      L3 (paradigm) ↔ Strategic
      L2 (schema)   ↔ Tactical  
      L1 (grouping) ↔ Operational
      L0 (entity)   ↔ Execution
    """
    # Strategic: operate on L2-L3 nodes
    strategic_view = mega.subgraph(levels={2, 3})
    strategy = hierarchical_skill.strategic_reason(strategic_view, query)
    
    # Tactical: operate on L1-L2 nodes
    tactical_view = mega.subgraph(levels={1, 2})
    tactics = hierarchical_skill.tactical_plan(strategy)
    
    # Operational: operate on L0-L1 nodes
    operational_view = mega.subgraph(levels={0, 1})
    steps = hierarchical_skill.operational_execute(tactics)
    
    return MEGAHolon(
        graph=mega,
        strategic_summary=strategy.summary,
        tactical_approach=tactics.approach,
        operational_steps=steps.actions
    )
```
</hierarchical_skill>

<nonlinear_skill>
```python
# ν (non-linear) — Uncertainty propagation, convergence
# MEGA provides: plithogenic attributes, correlation matrix
# ν provides: propagation algorithms, convergence detection

class NonLinearSkillInterface(Protocol):
    def propagate_uncertainty(
        self, 
        graph: 'nSHG', 
        changed_node: str, 
        delta: 'UncertaintyTuple'
    ) -> dict[str, 'UncertaintyTuple']:
        """Propagate uncertainty change through graph."""
        ...
    
    def detect_convergence(
        self,
        states: list['nSHG'],
        threshold: float = 0.05
    ) -> tuple[bool, float]:
        """Check if iteration has converged."""
        ...

# MEGA ↔ ν composition
def mega_with_nonlinear(mega: 'nSHG', update: 'NodeUpdate') -> 'nSHG':
    """
    Apply non-linear uncertainty propagation.
    
    When a node's uncertainty changes, propagate via:
    1. Correlation matrix (Ψ): direct structural influence
    2. Plithogenic composition: attribute-level effects
    """
    # Get propagation targets from correlation matrix
    targets = []
    for (a, b), corr in mega.correlations.items():
        if a == update.node_id:
            targets.append((b, corr))
        elif b == update.node_id:
            targets.append((a, corr))
    
    # Propagate uncertainty changes
    changes = nonlinear_skill.propagate_uncertainty(
        mega, update.node_id, update.delta
    )
    
    # Apply changes
    for node_id, new_uncertainty in changes.items():
        mega.nodes[node_id].attributes['_propagated'] = new_uncertainty
    
    return mega
```
</nonlinear_skill>

<infranodus_skill>
```python
# ι (infranodus) — Gap detection, research questions, bridging
# MEGA provides: structure to analyze
# ι provides: topological gap analysis, AI-powered suggestions

class InfraNodeusSkillInterface(Protocol):
    async def get_graph_and_advice(
        self,
        text: str,
        optimize: str = 'gaps',
        gap_depth: int = 2
    ) -> 'InfraNodeusResult':
        """Analyze text for structural gaps and advice."""
        ...
    
    async def generate_research_questions(
        self,
        text: str,
        use_several_gaps: bool = True
    ) -> list[str]:
        """Generate questions to fill knowledge gaps."""
        ...

# MEGA ↔ ι composition
async def mega_with_infranodus(mega: 'nSHG') -> 'MEGAWithGaps':
    """
    Enrich MEGA with InfraNodus gap analysis.
    
    This is the primary R1 (bridge_gaps) implementation.
    """
    # Convert MEGA to text representation
    text = mega_to_text(mega)
    
    # Get gap analysis from InfraNodus
    result = await infranodus_skill.get_graph_and_advice(
        text=text,
        optimize='gaps',
        gap_depth=2
    )
    
    # Map InfraNodus gaps to MEGA structure
    mega_gaps = []
    for gap in result.gaps:
        # Find corresponding MEGA nodes
        cluster_a_nodes = find_mega_nodes(mega, gap.cluster_a)
        cluster_b_nodes = find_mega_nodes(mega, gap.cluster_b)
        
        mega_gaps.append(MEGAGap(
            cluster_a=cluster_a_nodes,
            cluster_b=cluster_b_nodes,
            suggested_bridge=gap.bridging_concept,
            eta_impact=estimate_eta_impact(mega, gap)
        ))
    
    # Generate research questions for critical gaps
    critical_gaps = [g for g in mega_gaps if g.eta_impact > 0.5]
    if critical_gaps:
        questions = await infranodus_skill.generate_research_questions(
            text=text,
            use_several_gaps=True
        )
        mega.research_questions = questions
    
    mega.gaps = mega_gaps
    return mega

def mega_to_text(mega: 'nSHG') -> str:
    """Convert MEGA structure to text for InfraNodus analysis."""
    lines = []
    
    # Nodes as concepts
    for node in mega.nodes.values():
        lines.append(f"{node.id}: L{node.level} node")
        if node.content:
            lines.append(f"  contains: {', '.join(node.content)}")
    
    # Edges as relationships
    for edge in mega.edges.values():
        lines.append(f"{edge.source} --[{edge.label}]--> {edge.target}")
    
    return "\n".join(lines)
```
</infranodus_skill>

<abduct_skill>
```python
# β (abduct) — Schema refactoring, topology optimization
# MEGA provides: structure to refactor
# β provides: pattern detection, schema induction

class AbductSkillInterface(Protocol):
    def detect_patterns(self, graph: 'nSHG') -> list['Pattern']:
        """Detect recurring structural patterns."""
        ...
    
    def induce_schema(self, patterns: list['Pattern']) -> 'nSHG':
        """Create meta-level schema from patterns."""
        ...
    
    def refactor(self, graph: 'nSHG', pattern: 'Pattern') -> 'nSHG':
        """Refactor graph to extract pattern as meta-node."""
        ...

# MEGA ↔ β composition  
def mega_with_abduct(mega: 'nSHG') -> 'nSHG':
    """
    Apply abductive refactoring to MEGA structure.
    
    This is the primary R2 (compress) and R3 (expand) implementation.
    """
    # Detect patterns at current level
    patterns = abduct_skill.detect_patterns(mega)
    
    # For frequent patterns, create meta-nodes (R3)
    for pattern in patterns:
        if pattern.frequency >= 3:  # Occurs 3+ times
            # Extract pattern instances as meta-node
            mega = abduct_skill.refactor(mega, pattern)
            
            # New node at level n+1
            if mega.max_level < 3:  # Respect depth bound
                mega.add_node(Node(
                    id=f"schema_{pattern.name}",
                    level=Level(mega.max_level + 1),
                    content=frozenset(pattern.instance_ids)
                ))
    
    # For redundant nodes, merge (R2)
    redundant = find_redundant_nodes(mega)
    for group in redundant:
        if len(group) > 1:
            keep = group[0]
            for remove in group[1:]:
                merge_nodes(mega, keep, remove)
    
    return mega
```
</abduct_skill>

---

## 3. EXTERNAL TOOL INTEGRATION

<obsidian_integration>
```python
# Obsidian PKM Integration
# MEGA → Obsidian vault export
# Obsidian → MEGA import (via batch processing)

from pathlib import Path

def export_mega_to_obsidian(mega: 'nSHG', vault_path: Path) -> None:
    """
    Export MEGA structure to Obsidian-flavored markdown.
    
    Structure:
      vault/
        L0-entities/
          node1.md
          node2.md
          _MOC.md
        L1-groupings/
          group1.md
          _MOC.md
        L2-schemas/
          schema1.md
          _MOC.md
        _MEGA_MOC.md
    """
    
    for level in range(mega.max_level + 1):
        level_dir = vault_path / f"L{level}-{LEVEL_NAMES[level]}"
        level_dir.mkdir(parents=True, exist_ok=True)
        
        nodes = mega.nodes_at_level(Level(level))
        
        for node in nodes:
            note_content = generate_obsidian_note(node, mega)
            note_path = level_dir / f"{sanitize_filename(node.id)}.md"
            note_path.write_text(note_content)
        
        # Generate level MOC
        moc_content = generate_level_moc(nodes, mega, level)
        (level_dir / "_MOC.md").write_text(moc_content)
    
    # Generate master MOC
    master_moc = generate_master_moc(mega)
    (vault_path / "_MEGA_MOC.md").write_text(master_moc)

def generate_obsidian_note(node: 'Node', mega: 'nSHG') -> str:
    """Generate Obsidian-flavored markdown for a MEGA node."""
    lines = [
        "---",
        f"id: {node.id}",
        f"level: {node.level}",
        f"created: {datetime.now().isoformat()}",
        "tags:",
        f"  - mega/L{node.level}",
    ]
    
    # Add uncertainty metadata
    if node.attributes:
        lines.append("uncertainty:")
        for attr, val in node.attributes.items():
            lines.append(f"  {attr}:")
            lines.append(f"    confidence: {val.confidence:.2f}")
            lines.append(f"    coverage: {val.coverage:.2f}")
            lines.append(f"    source_quality: {val.source_quality:.2f}")
    
    lines.append("---")
    lines.append("")
    lines.append(f"# {node.id}")
    lines.append("")
    
    # Containment (for meta-nodes)
    if node.content:
        lines.append("## Contains")
        for child_id in node.content:
            lines.append(f"- [[{child_id}]]")
        lines.append("")
    
    # Relationships
    outgoing = [e for e in mega.edges.values() if e.source == node.id]
    incoming = [e for e in mega.edges.values() if e.target == node.id]
    
    if outgoing:
        lines.append("## Relationships (outgoing)")
        for edge in outgoing:
            lines.append(f"- {edge.label} → [[{edge.target}]]")
        lines.append("")
    
    if incoming:
        lines.append("## Relationships (incoming)")
        for edge in incoming:
            lines.append(f"- [[{edge.source}]] → {edge.label}")
        lines.append("")
    
    # Correlations
    correlated = [
        (other, corr) 
        for (a, b), corr in mega.correlations.items()
        if a == node.id or b == node.id
        for other in [b if a == node.id else a]
    ]
    if correlated:
        lines.append("## Correlated Nodes")
        for other, corr in correlated:
            lines.append(f"- [[{other}]] (Ψ={corr:.2f})")
    
    return "\n".join(lines)

LEVEL_NAMES = {
    0: "entities",
    1: "groupings", 
    2: "schemas",
    3: "paradigms"
}
```
</obsidian_integration>

<mcp_integration>
```python
# MCP Server Integration
# For tools: InfraNodus, Exa, Scholar Gateway, etc.

async def mega_mcp_workflow(
    query: str,
    initial_context: str,
    mcp_tools: list[str]
) -> 'MEGAHolon':
    """
    MEGA workflow with MCP tool integration.
    """
    
    # 1. Initial extraction (may use Exa for web search)
    if 'exa' in mcp_tools:
        search_results = await mcp_call(
            'exa:web_search_exa',
            query=query,
            numResults=5
        )
        initial_context += "\n" + search_results.context
    
    # 2. Build initial graph
    mega = build_n_shg_from_text(initial_context)
    
    # 3. Gap analysis via InfraNodus MCP
    if 'infranodus' in mcp_tools:
        gap_result = await mcp_call(
            'infranodus:getGraphAndAdvice',
            name="mega_analysis",
            text=mega_to_text(mega),
            optimize="gaps",
            extendedGraphSummary=True
        )
        
        # Apply gap suggestions
        for gap in gap_result.gaps:
            suggested_edge = Edge(
                source=gap.cluster_a_representative,
                target=gap.cluster_b_representative,
                label="bridges_gap",
                weight=0.5
            )
            mega.add_edge(suggested_edge)
    
    # 4. Academic grounding via Scholar Gateway
    if 'scholar-gateway' in mcp_tools:
        # Find nodes needing evidence
        low_confidence = [
            n for n in mega.nodes.values()
            if n.attributes and 
            any(a.source_quality < 0.6 for a in n.attributes.values())
        ]
        
        for node in low_confidence[:3]:  # Limit API calls
            papers = await mcp_call(
                'Scholar Gateway:search_papers',
                query=node.id,
                limit=3
            )
            if papers:
                # Update source quality
                for attr in node.attributes.values():
                    attr.source_quality = min(attr.source_quality + 0.2, 0.9)
    
    # 5. Validate and return
    validation = validate_mega(mega)
    if not validation.valid:
        mega = autopoietic_refine(mega)
    
    return decohere(mega, query)
```
</mcp_integration>

---

## 4. COMPOSITION PATTERNS

<sequential_composition>
```python
# Sequential: λ₁ ∘ λ₂ (output of λ₂ feeds λ₁)

# Pattern: Extract → Enrich → Refine → Validate
mega_pipeline = (
    validate_mega ∘ 
    autopoietic_refine ∘ 
    mega_with_infranodus ∘ 
    mega_with_ontolog ∘ 
    graph_skill.extract
)

result = mega_pipeline(input_text)
```
</sequential_composition>

<parallel_composition>
```python
# Parallel: λ₁ ⊗ λ₂ (both operate on same input)

# Pattern: Multi-perspective analysis
def parallel_analysis(mega: 'nSHG') -> dict:
    results = {}
    
    # Run in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(infranodus_gaps, mega): "gaps",
            executor.submit(ontolog_homology, mega): "topology",
            executor.submit(hierarchical_decompose, mega): "hierarchy",
        }
        
        for future in as_completed(futures):
            key = futures[future]
            results[key] = future.result()
    
    return results
```
</parallel_composition>

<recursive_composition>
```python
# Recursive: λ* = fix(λ) (iterate until convergence)

# Pattern: Autopoietic refinement loop
def converge_mega(mega: 'nSHG', max_iterations: int = 10) -> 'nSHG':
    for i in range(max_iterations):
        violations = validate_mega(mega).violations
        
        if not violations:
            break
        
        # Apply refinement
        mega = apply_refinement(mega, violations[0])
        
        # Check convergence
        if i > 0:
            delta = compute_delta(mega, prev_mega)
            if delta < 0.05:
                break
        
        prev_mega = mega
    
    return mega
```
</recursive_composition>

---

## 5. QUICK REFERENCE

```
MEGA v2.0 INTEGRATION
═════════════════════

SKILL INTERFACES
  γ (graph)       extract(), compress(), validate_eta()
  ω (ontolog)     encode_simplicial(), compute_homology(), detect_holes()
  η (hierarchical) strategic_reason(), tactical_plan(), operational_execute()
  ν (non-linear)  propagate_uncertainty(), detect_convergence()
  ι (infranodus)  get_graph_and_advice(), generate_research_questions()
  β (abduct)      detect_patterns(), induce_schema(), refactor()

EXTERNAL TOOLS
  InfraNodus      Gap detection, research questions (MCP)
  Obsidian        PKM export/import (file-based)
  Exa             Web search for context (MCP)
  Scholar Gateway Academic grounding (MCP)

COMPOSITION OPERATORS
  ∘  Sequential   f ∘ g = f(g(x))
  ⊗  Parallel     f ⊗ g = (f(x), g(x))
  *  Recursive    f* = fix(f), iterate until convergence

LEVEL ↔ REASONING MAPPING
  L3 (paradigm)   ↔ Strategic (Why)
  L2 (schema)     ↔ Tactical (How)
  L1 (grouping)   ↔ Operational (What)
  L0 (entity)     ↔ Execution (Do)
```
