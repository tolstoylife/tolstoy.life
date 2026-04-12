# Workflow Patterns Reference

Canonical multi-skill workflow patterns with customization options.

## Pattern 1: Research → Structure → Document

**Use Case:** Complex topic research that needs structured documentation

**Trigger Conditions:**
- `complexity_score > 0.7`
- `artifact_type == file`
- `requires_decomposition == true`
- All three skills (hierarchical-reasoning, knowledge-graph, obsidian-markdown) are candidates

**Workflow Sequence:**

```yaml
1. hierarchical-reasoning:
   purpose: "Strategic decomposition of topic into levels"
   input_from: user_request
   parameters:
     max_strategic_cycles: 3
     max_tactical_cycles: 5
     max_operational_cycles: 7
     convergence_threshold: 0.95
   output_bindings:
     - strategic_insights → strategic analysis
     - tactical_approaches → methodology breakdown
     - operational_details → concrete examples and evidence

2. knowledge-graph:
   purpose: "Extract entities and relationships from reasoning output"
   input_from: hierarchical-reasoning.operational_output
   parameters:
     schema: auto-detect domain
     min_confidence: 0.7
     extraction_focus: hierarchical-reasoning.strategic_insights.key_concepts
   output_bindings:
     - entities → extracted concepts, patterns, technologies
     - relationships → connections between entities
     - ontology → domain structure

3. obsidian-markdown:
   purpose: "Format as Map of Content note"
   input_from: knowledge-graph
   parameters:
     template: moc-template
     frontmatter:
       type: moc
       tags: knowledge-graph.entity_types
       related: knowledge-graph.entity_names
       complexity: hierarchical-reasoning.convergence_score
   transformations:
     - entities → wikilinks
     - relationships → mermaid diagram
     - strategic_insights → H2 sections
     - tactical_approaches → H3 subsections
     - operational_details → detailed content
   output: comprehensive_note.md
```

**Customization Options:**
```yaml
# Adjust reasoning depth
hierarchical_reasoning_depth: standard | deep | quick
  standard: cycles (3,5,7)
  deep: cycles (5,7,10)
  quick: cycles (2,3,5)

# Control extraction granularity
extraction_granularity: coarse | balanced | fine
  coarse: min 5 entities, relationships optional
  balanced: min 8 entities, min 3 relationships
  fine: exhaustive extraction, nested relationships

# Template selection
output_template: moc | concept | project | learning
```

---

## Pattern 2: Extract → Validate → Format

**Use Case:** Processing unstructured text into validated, well-formatted knowledge

**Trigger Conditions:**
- `artifact_type == file`
- `requires_extraction == true`
- `content_type == prose`
- knowledge-graph and obsidian-markdown are candidates

**Workflow Sequence:**

```yaml
1. knowledge-graph:
   purpose: "Extract entities, relationships, and structure"
   input_from: user_request.source_text
   parameters:
     schema: core_ontology OR coding_domain (auto-detect)
     include_provenance: true
     confidence_threshold: 0.6
   output_bindings:
     - raw_graph → initial extraction
     - entity_count → quality metric
     - relationship_count → connectivity metric
     - isolation_rate → gap indicator

2. hierarchical-reasoning:
   purpose: "Validate graph coherence, completeness, and quality"
   input_from: raw_graph
   parameters:
     problem: "Assess quality of extracted knowledge graph. Identify gaps, inconsistencies, and refinement opportunities."
     context:
       graph: knowledge-graph.raw_graph
       metrics:
         entity_count: knowledge-graph.entity_count
         isolation_rate: knowledge-graph.isolation_rate
     success_criteria:
       - Entities cover main concepts
       - Relationships show connectivity
       - No major gaps in coverage
   output_bindings:
     - strategic_assessment → overall quality evaluation
     - tactical_gaps → specific missing elements
     - operational_recommendations → refinement actions

3. obsidian-markdown:
   purpose: "Create structured note with validated knowledge"
   input_from: knowledge-graph + hierarchical-reasoning
   parameters:
     template: note-template
     frontmatter:
       extracted-from: knowledge-graph.provenance.source
       entity-count: knowledge-graph.entity_count
       confidence: knowledge-graph.average_confidence
       quality-score: hierarchical-reasoning.strategic_assessment.score
   transformations:
     - entities → wikilinks with confidence annotations
     - relationships → mermaid graph + prose descriptions
     - validation_gaps → callout warnings
     - recommendations → action items
   output: validated_knowledge_note.md
```

**Customization Options:**
```yaml
# Validation strictness
validation_mode: lenient | standard | strict
  lenient: Accept graphs with gaps, flag for user review
  standard: Require minimum connectivity, highlight gaps
  strict: Enforce quality thresholds, reject if criteria not met

# Extraction refinement
enable_iterative_refinement: true | false
  true: If validation fails, re-extract with focused guidance
  false: Single-pass extraction, report issues

# Output format
include_quality_metrics: true | false
  true: Show confidence scores, coverage metrics in note
  false: Clean output without diagnostic info
```

---

## Pattern 3: Analyze → Graph → Visualize

**Use Case:** Understanding complex systems through decomposition and visualization

**Trigger Conditions:**
- `complexity_score > 0.6`
- `requires_decomposition == true`
- `requires_extraction == true` OR visualization keywords present

**Workflow Sequence:**

```yaml
1. hierarchical-reasoning:
   purpose: "Decompose system into components and relationships"
   input_from: user_request
   parameters:
     focus: system_architecture
     emphasis: tactical_level (how components interact)
   output_bindings:
     - system_components → identified parts
     - interaction_patterns → how components relate
     - hierarchical_structure → levels and dependencies

2. knowledge-graph:
   purpose: "Map components as formal graph structure"
   input_from: hierarchical-reasoning
   parameters:
     schema: custom_system_ontology
     entity_types: hierarchical-reasoning.system_components
     relationship_types: hierarchical-reasoning.interaction_patterns
     preserve_hierarchy: true
   output_bindings:
     - system_graph → formal graph representation
     - component_nodes → entities with properties
     - interaction_edges → relationships with metadata

3. obsidian-markdown:
   purpose: "Visualize system with Mermaid diagrams"
   input_from: knowledge-graph
   parameters:
     template: note-template
     diagram_type: mermaid_graph | mermaid_flowchart
     frontmatter:
       type: system-analysis
       components: knowledge-graph.component_count
       analyzed: timestamp
   transformations:
     - system_graph → mermaid diagram code
     - components → wikilinks to component details
     - hierarchical_structure → nested diagram sections
     - strategic_insights → overview section
   output: system_visualization.md
```

**Customization Options:**
```yaml
# Diagram complexity
diagram_detail: overview | balanced | comprehensive
  overview: Top-level components only
  balanced: Main components + key relationships
  comprehensive: All components + all relationships

# Visualization style
mermaid_type: graph | flowchart | sequence | class
  Auto-selected based on system type, or user can specify

# Interactive elements
make_nodes_clickable: true | false
  true: Mermaid nodes link to component notes
  false: Static diagram
```

---

## Custom Pattern Definition

Users can define custom workflow patterns:

```yaml
custom_pattern:
  name: "custom_workflow_name"
  description: "What this workflow accomplishes"

  trigger_conditions:
    - condition_1: "expression"
    - condition_2: "expression"
    - keyword_present: "specific_word"

  sequence:
    - skill: skill_name
      purpose: "what this step does"
      input: "where input comes from"
      parameters:
        param1: value1
        param2: value2
      output_binding: "variable_name"

    - skill: next_skill
      purpose: "next step purpose"
      input: "previous_output_binding"
      parameters:
        param: value
      output_binding: "next_variable"

  final_output: "last_output_binding"
```

**Custom Pattern Location:**
- Save to: `~/.claude/skills/knowledge-orchestrator/custom_patterns/`
- File format: YAML
- Naming: `pattern_name.yaml`

**Validation:**
Use `scripts/validate_workflow.py` to check custom pattern validity before deployment.

---

## Workflow Selection Logic

```python
def select_workflow(candidates, features):
    # Check canonical patterns first
    if matches_research_structure_document(candidates, features):
        return "research_structure_document"

    if matches_extract_validate_format(candidates, features):
        return "extract_validate_format"

    if matches_analyze_graph_visualize(candidates, features):
        return "analyze_graph_visualize"

    # Check custom patterns
    for pattern in load_custom_patterns():
        if pattern.matches(candidates, features):
            return pattern

    # No pattern match - execute highest confidence single skill
    return None
```

## Workflow Execution Best Practices

1. **Data Flow Validation**: Ensure each step's output matches next step's expected input
2. **Error Handling**: If middle step fails, notify user with context about workflow state
3. **Partial Success**: Allow user to accept partial workflow completion
4. **Transparency**: Show which step is currently executing in multi-step workflows
5. **Optimization**: Cache intermediate results for potential re-runs with different parameters
