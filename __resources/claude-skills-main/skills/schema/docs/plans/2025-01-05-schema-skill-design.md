# Schema Skill Design Document

**Date**: 2025-01-05
**Status**: Approved for Implementation
**Author**: Claude Code with User Collaboration

## Purpose

Generate knowledge schemas and ontologies from any input format. Extract semantic structures, relationships, and hierarchies. Represent them as Obsidian-compatible markdown with rich metadata, or export to semantic formats (JSON-LD, RDF, Neo4j Cypher, GraphQL).

## Requirements

### Core Functionality
- **Input Formats**: Plain text, structured data (JSON/YAML/CSV/XML), markdown files, code repositories
- **Primary Output**: Obsidian markdown with YAML frontmatter, wikilinks, tags, callouts, mermaid diagrams
- **Secondary Outputs**: JSON-LD, RDF/OWL, Neo4j Cypher, GraphQL schemas
- **Modes**: Fractal mode (strict hierarchical constraints) + Free mode (flexible generation)
- **Ontology Features**: Property inheritance, multi-dimensional navigation, implicit relationship inference

### Implementation Constraints
- **Sandboxed Python**: Limited to pre-installed libraries (pandas, numpy, spaCy, networkx, etc.)
- **Local Execution**: Can leverage shell scripts, Rust, Node.js, Python when not sandboxed
- **MCP Integration**: Hybrid—works standalone OR orchestrates deepgraph, zen:thinkdeep, deepwiki tools

## Architecture

### Four-Layer Pipeline

**Layer 1: Structural Extraction (AST-First)**
- Parse inputs to Abstract Syntax Tree
- Tools: `markdown-oxide` LSP (markdown), `tree-sitter` (code), `pandas` (tabular data)
- Extract: Headings, lists, code blocks, frontmatter, wikilinks, tags, class/function definitions
- Output: JSON graph with structural nodes and containment edges
- Speed: ~10ms for typical documents

**Layer 2: Semantic Analysis (NLP-Enhanced)**
- Extract entities and relationships using natural language processing
- Tools: `spaCy` (entity/relation extraction), `networkx` (graph analytics)
- Classify: Meronymy (part-of), hypernymy (is-a), antonymy (opposite), causation
- Compute: Centrality metrics, community detection, topology scores
- Output: Semantic ontology with typed entities and classified relationships
- Speed: ~100-500ms

**Layer 3: LLM Enrichment (Optional, Conditional)**
- Trigger: User requests `--deep`, low-confidence relationships, complex multi-domain content
- Standalone: Direct Claude API calls for semantic enrichment
- MCP Orchestration: Coordinate zen:thinkdeep, deepgraph, deepwiki for complex analysis
- Resolve: Ambiguities, inferred relationships, cross-domain links, descriptions
- Output: Enriched ontology with inferred properties
- Speed: ~5-30s

**Layer 4: Output Generation (Template-Driven)**
- Apply Jinja2 templates for each format
- Tools: Jinja2, mq/jq for querying, format-specific validators
- Generate: YAML frontmatter, mermaid diagrams, wikilinks, tables, semantic format exports
- Validate: Syntax, schema, links, constraints (fractal mode), graph connectivity
- Output: Formatted documents with validation report
- Speed: ~50-200ms

### Control Flow

```
Input → Adapter → L1 → L2 → L3 → L4 → Output
         ↓         ↓     ↓     ↓     ↓
      Normalize  AST   NLP  Enrich Format
```

Layers execute sequentially with graceful degradation:
- L1 fails → Plain text fallback
- L2 fails → Heuristic relationships from L1 structure
- L3 fails → Skip enrichment, use L1+L2
- L4 fails → Output raw JSON ontology

## Data Model

```python
@dataclass
class OntologyNode:
    id: str                          # Unique identifier
    label: str                       # Display name
    node_type: str                   # entity, concept, class, property
    stem: Optional[str]              # Lexical stem (fractal mode)
    depth: int                       # Hierarchy level
    properties: Dict[str, Any]       # Node metadata
    inherited_properties: Dict       # From ancestors
    aliases: List[str]               # Alternative names
    description: Optional[str]       # Semantic description
    source_location: Optional[str]   # Origin in input

@dataclass
class OntologyEdge:
    source_id: str
    target_id: str
    edge_type: str                   # parent_of, part_of, opposite_of, causes
    properties: Dict[str, Any]
    strength: float                  # Confidence (0.0-1.0)
    inferred: bool                   # True if L3 generated

@dataclass
class Ontology:
    nodes: Dict[str, OntologyNode]
    edges: List[OntologyEdge]
    metadata: Dict[str, Any]         # Source, timestamp, mode
    dimensions: List[str]            # Navigation axes
```

## Directory Structure

```
schema/
├── SKILL.md
├── config/
│   ├── fractal-mode.yaml
│   ├── free-mode.yaml
│   └── templates/
│       ├── obsidian.md.j2
│       ├── jsonld.json.j2
│       ├── cypher.cypher.j2
│       └── graphql.graphql.j2
├── scripts/
│   ├── core/
│   │   ├── layer1_ast_parser.py
│   │   ├── layer2_semantic.py
│   │   ├── layer3_llm_enrich.py
│   │   └── layer4_generator.py
│   ├── adapters/
│   │   ├── input_text.py
│   │   ├── input_json.py
│   │   ├── input_markdown.py
│   │   └── input_code.py
│   ├── integrations/
│   │   ├── mcp_deepgraph.py
│   │   ├── mcp_zen.py
│   │   └── mcp_orchestra.py
│   └── utils/
│       ├── ontology.py
│       ├── inheritance.py
│       ├── graph_analytics.py
│       └── validation.py
├── references/
│   ├── ast-parsing-guide.md
│   ├── semantic-patterns.md
│   ├── template-syntax.md
│   └── mcp-integration.md
└── examples/
    ├── text-to-schema/
    ├── json-to-schema/
    ├── markdown-to-schema/
    └── code-to-schema/
```

## Breadcrumb-Style Ontology Features

### Property Inheritance
Child nodes automatically inherit properties from ancestors:
```python
def compute_inherited_properties(node, ontology):
    inherited = {}
    current = node
    while current.parent_id:
        parent = ontology.nodes[current.parent_id]
        # Parent properties, but child can override
        for key, value in parent.properties.items():
            if key not in inherited:
                inherited[key] = value
        current = parent
    return inherited
```

### Multi-Dimensional Navigation
Generate alternate edge sets for different navigation axes:
- **Temporal**: Creation order, modification time, lifecycle stages
- **Conceptual**: Domain hierarchies, abstraction levels
- **Spatial**: Physical location, containment, adjacency
- **Functional**: Purpose-based groupings, process flows

### Implicit Relationship Inference
Layer 2 creates edges based on:
- **Co-occurrence**: Entities appearing in same context
- **Tag overlap**: Nodes sharing >50% tags
- **Structural proximity**: Within N hops in hierarchy
- **Semantic similarity**: Embedding distance < threshold

## Mode Switching

### Fractal Mode
- Enforce 2-3 children per non-leaf node
- Require homonymic inheritance (child labels contain parent stem)
- Uniform relation types per parent
- Label length ≤3 words
- Topology score ≥4.0
- Configuration: `config/fractal-mode.yaml`

### Free Mode
- Relaxed constraints
- Optimize for semantic coherence
- Variable branching factor
- Flexible naming
- Configuration: `config/free-mode.yaml`

Mode detection: From config parameter or auto-inferred from input complexity.

## Error Handling

### Graceful Degradation
- **L1 failure**: Fall back to paragraph splitting, create flat ontology
- **L2 failure**: Use heuristic relationships from L1 structure
- **L3 failure**: Skip enrichment, proceed with L1+L2
- **Template failure**: Use fallback template or output raw JSON

### Stagnation Detection
If repair loop produces identical output twice:
- Abort immediately
- Return best-attempt output
- Include diagnostic message
- Suggest: simplify input, change mode, reduce constraints

### Validation
- **Syntax**: Lint markdown/JSON/Cypher
- **Schema**: Verify required fields, type constraints
- **Links**: Ensure wikilinks reference valid nodes
- **Constraints**: Apply fractal-mode rules if enabled
- **Graph**: Check connectivity, no orphaned nodes

Non-critical failures: Log warnings, proceed.
Critical failures: Attempt auto-repair, return output + error report.

## Output Formats

### Obsidian Markdown (Primary)
- YAML frontmatter with tags, aliases, metadata
- Wikilinks for all internal references
- Callouts for important information
- Mermaid diagrams with `internal-link` class
- Tables for properties and relationships
- Breadcrumb-style navigation sections

### JSON-LD
- Standard semantic web format
- `@context` + `@graph` structure
- Compatible with triple stores

### Neo4j Cypher
- CREATE statements for nodes
- CREATE statements for relationships
- Property assignments
- Index creation

### GraphQL Schema
- Type definitions
- Resolver structure
- Relationship fields

## Success Metrics

- **Processing Speed**: L1+L2 < 1s for typical documents
- **Accuracy**: >85% entity extraction precision
- **Topology**: Achieve ≥4.0 score in fractal mode
- **Validation**: >95% outputs pass all validators
- **Degradation**: Always produce usable output, even on failures

## Implementation Phases

1. **Core Pipeline**: Implement L1-L4 with basic adapters
2. **Obsidian Output**: Template development + validation
3. **Mode Support**: Fractal and free mode configurations
4. **Breadcrumb Features**: Inheritance, multi-dimension, inference
5. **MCP Integration**: Deep mode orchestration
6. **Format Export**: JSON-LD, RDF, Cypher, GraphQL
7. **Testing**: Comprehensive test cases across formats
8. **Documentation**: Reference guides, examples

## Dependencies

**Sandboxed Python (Always Available)**:
- pandas, numpy, spaCy, networkx
- python-frontmatter, pyyaml
- Jinja2

**Local Execution (When Available)**:
- markdown-oxide LSP
- tree-sitter
- mq, jq, yq
- ast-grep

**External (Optional)**:
- Claude API (Layer 3 enrichment)
- MCP tools (deepgraph, zen, deepwiki)

## Next Steps

1. Set up git worktree for isolated development
2. Create detailed implementation plan
3. Build L1 parser with input adapters
4. Implement L2 semantic analysis
5. Develop Obsidian template
6. Add mode configuration
7. Test with example inputs
8. Integrate MCP orchestration
9. Add export formats
10. Validate and refine
