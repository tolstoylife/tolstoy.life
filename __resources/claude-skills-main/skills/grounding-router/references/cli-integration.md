# CLI Integration — Complete Feature Matrix & Permutation Pipelines

## CLI Capability Matrix

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         COMPLETE CLI INTEGRATION MATRIX                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  LIMITLESS ─────────────────────────────────────────────────────────────────│
│  │                                                                            │
│  ├── lifelogs                                                                 │
│  │   ├── search "query" --limit N --json    # Semantic lifelog search        │
│  │   ├── list --limit N --json              # Recent lifelogs               │
│  │   ├── get <id> --json                    # Specific lifelog              │
│  │   └── sync                               # Sync to Neo4j graph           │
│  │                                                                            │
│  ├── workflow                                                                 │
│  │   ├── daily YYYY-MM-DD --json            # Full day snapshot             │
│  │   ├── recent --hours N --json            # Time-windowed context         │
│  │   ├── search "query" --json              # Cross-source search           │
│  │   └── export --start --end --json        # Date range export             │
│  │                                                                            │
│  ├── chats                                                                    │
│  │   ├── list --limit N --json              # AI conversation history       │
│  │   └── get <id> --json                    # Specific chat                 │
│  │                                                                            │
│  ├── graph                                                                    │
│  │   ├── query "CYPHER" --json              # Neo4j Cypher execution        │
│  │   ├── stats                              # Graph statistics              │
│  │   └── traverse <type> <id> --depth N     # Relationship traversal        │
│  │                                                                            │
│  └── pipeline                               # DAG PIPELINE ENGINE            │
│      ├── run <template|file> --var k=v      # Execute pipeline              │
│      ├── run --dry-run                      # Validate without execute      │
│      ├── run --verbose                      # Detailed execution logs       │
│      └── list-templates                     # Available pipeline templates   │
│                                                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  RESEARCH ──────────────────────────────────────────────────────────────────│
│  │                                                                            │
│  ├── MODES                                                                    │
│  │   ├── fact-check -t "claim"              # Claim verification            │
│  │   ├── academic -t "topic" -d domain      # Scholarly sources             │
│  │   ├── pex-grounding -t "query" -s spec   # Medical education PEX         │
│  │   ├── docs -t "query" -k framework       # Framework documentation       │
│  │   └── sdk-api -t "query" --sdk name      # SDK/API reference             │
│  │                                                                            │
│  ├── INPUT FLAGS                                                              │
│  │   ├── -t, --text "input"                 # Direct text input             │
│  │   ├── -i, --file <path>                  # Read from file                │
│  │   └── --stdin                            # Read from stdin               │
│  │                                                                            │
│  ├── OUTPUT FLAGS                                                             │
│  │   ├── -f, --format markdown|json|obsidian # Output format               │
│  │   ├── -o, --output <file>                # Write to file                 │
│  │   └── --tui                              # Display with glow             │
│  │                                                                            │
│  ├── GRAPH FLAGS                                                              │
│  │   ├── -g, --graph                        # Build Neo4j + Obsidian        │
│  │   ├── --dry-run                          # Preview graph changes         │
│  │   ├── --no-ner                           # Skip entity extraction        │
│  │   └── --local-ner-only                   # BioBERT only, skip LLM        │
│  │                                                                            │
│  ├── CONFIG FLAGS                                                             │
│  │   ├── -c, --config <path>                # Custom config file            │
│  │   ├── -v, --verbose                      # Debug output                  │
│  │   └── --concurrency N                    # Parallel API requests         │
│  │                                                                            │
│  └── UTILITY                                                                  │
│      ├── health                             # Check API connectivity         │
│      ├── sync --direction <dir>             # Neo4j - Obsidian sync         │
│      └── completions zsh|bash               # Shell completions             │
│                                                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  PIECES ────────────────────────────────────────────────────────────────────│
│  │                                                                            │
│  ├── ask "query"                            # Base query                     │
│  │   ├── --ltm                              # Long-Term Memory context      │
│  │   ├── -f file1.py file2.py               # File context (multi-file)    │
│  │   └── -m 1 2 3                           # Include saved materials       │
│  │                                                                            │
│  ├── search "pattern"                                                         │
│  │   ├── --mode ncs                         # Neural Code Search (semantic) │
│  │   ├── --mode fts                         # Full-Text Search (exact)      │
│  │   └── --mode fuzzy                       # Fuzzy matching (default)      │
│  │                                                                            │
│  ├── materials                                                                │
│  │   ├── list                               # List saved materials          │
│  │   ├── save                               # Save from clipboard           │
│  │   └── create                             # Create new material           │
│  │                                                                            │
│  └── chats                                                                    │
│      ├── chats                              # List all chats                │
│      └── chat                               # Interactive chat select       │
│                                                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  PDF-SEARCH / PDF-BRAIN ────────────────────────────────────────────────────│
│  │                                                                            │
│  ├── pdf-search "query"                     # Primary semantic search        │
│  │   ├── --limit N                          # Result limit                   │
│  │   ├── --tags ANZCA,pharmacology          # Tag filtering                  │
│  │   └── --stats                            # Library statistics             │
│  │                                                                            │
│  └── pdf-brain search "query"               # Alternative semantic search    │
│      ├── --limit N                          # Result limit                   │
│      ├── --tags                             # Tag filtering                  │
│      └── --stats                            # Library statistics             │
│                                                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  SCREENAPP ────────────────────────────────────────────────────────────────  │
│  │                                                                            │
│  ├── files                                                                    │
│  │   ├── list --json                        # List all recordings            │
│  │   ├── get <id> --include transcript --json  # Get with transcript        │
│  │   ├── search "query" --semantic --json   # Semantic transcript search    │
│  │   ├── search "query" --hybrid --json     # Combined search               │
│  │   ├── tag <id> --key K --value V         # Add tag to recording          │
│  │   └── untag <id> --key K                 # Remove tag from recording     │
│  │                                                                            │
│  ├── ask <fileId> "question"                # Multimodal AI query            │
│  │   ├── --mode transcript                  # Transcript-focused             │
│  │   ├── --mode video                       # Video frame analysis           │
│  │   ├── --mode screenshots                 # Screenshot analysis            │
│  │   ├── --start N --end M                  # Time segment (seconds)         │
│  │   └── --json                             # JSON output format             │
│  │                                                                            │
│  ├── sync                                                                     │
│  │   ├── run --full                         # Full resync                    │
│  │   ├── run                                # Incremental sync               │
│  │   ├── status --json                      # Sync status & stats            │
│  │   ├── build-similarity                   # Build recording similarity     │
│  │   └── build-topics                       # Build topic co-occurrence      │
│  │                                                                            │
│  ├── graph                                                                    │
│  │   ├── query "CYPHER" --json              # FalkorDB Cypher execution      │
│  │   ├── stats --json                       # Graph statistics               │
│  │   └── traverse Recording <id> --depth N  # Relationship traversal         │
│  │                                                                            │
│  └── workflow                                                                 │
│      ├── daily YYYY-MM-DD --json            # Daily recordings snapshot      │
│      ├── search "query" --limit N --json    # Cross-recording search         │
│      ├── recent --hours N --json            # Recent activity window         │
│      └── export --start --end --format obs  # Export to Obsidian             │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Primitive to Advanced CLI Mapping

### Σₚ — Personal Context (limitless)

**Basic Extraction:**
```bash
# Semantic search (most common)
limitless lifelogs search "{topic}" --limit 10 --json

# Date-specific context
limitless workflow daily $(date +%Y-%m-%d) --json

# Time-windowed (last N hours)
limitless workflow recent --hours 24 --json
```

**Advanced Operations:**
```bash
# Cross-source unified search
limitless workflow search "{topic}" --json

# Date range export for longitudinal context
limitless workflow export --start 2025-01-01 --end 2025-01-05 --json

# Relationship-based queries via Cypher
limitless graph query "
  MATCH (p:Person)-[:MENTIONED_IN]->(l:Lifelog)
  WHERE l.markdown CONTAINS '{topic}'
  RETURN p.name, l.title, l.startTime
  ORDER BY l.startTime DESC
  LIMIT 10
" --json

# Person-specific context traversal
limitless graph traverse Person "person-uuid" --depth 2

# Topic cluster discovery
limitless graph query "
  MATCH (t:Topic)-[:DISCUSSED_IN]->(l:Lifelog)
  WHERE t.name =~ '(?i).*{topic}.*'
  RETURN t, collect(l) as lifelogs
  LIMIT 5
" --json

# AI chat history for prior explanations
limitless chats list --limit 5 --json
```

**DAG Pipeline Execution:**
```bash
# Execute pre-built context extraction pipeline
limitless pipeline run context-extraction --var query="{topic}" --var depth=3

# Dry-run validation
limitless pipeline run medical-grounding --dry-run

# Verbose execution logging
limitless pipeline run saq-prep --var topic="{topic}" --verbose
```

### Σₗ — Local Context (pieces)

**Basic Extraction:**
```bash
# LTM-enhanced query (always preferred)
echo "" | pieces ask "{topic}" --ltm

# Semantic code search
pieces search --mode ncs "{pattern}"
```

**Advanced Operations:**
```bash
# Multi-file grounded query
echo "" | pieces ask "{topic}" --ltm -f src/auth.py src/middleware.py src/models.py

# Combined materials + LTM + files
echo "" | pieces ask "{topic}" --ltm -m 1 2 3 -f relevant_file.py

# Full-text exact match (for specific code)
pieces search --mode fts "class {ClassName}"

# Fuzzy search (typo-tolerant)
pieces search "authentcation" --mode fuzzy

# List materials for context selection
pieces list | head -20
```

**Conditional Mode Selection:**
```python
def select_pieces_mode(query: str) -> str:
    if is_exact_code_search(query):
        return "fts"  # Full-text for exact matches
    elif has_typos(query):
        return "fuzzy"  # Fuzzy for approximate
    else:
        return "ncs"  # Neural for conceptual
```

### Σₜ — Textbook Context (pdf-search / pdf-brain)

**Basic Extraction:**
```bash
# Primary semantic search
pdf-search "{topic}" --limit 10

# With tag filtering
pdf-search "{topic}" --limit 10 --tags ANZCA,pharmacology,obstetrics
```

**Advanced Operations:**
```bash
# Multi-tag intersection
pdf-search "{topic}" --limit 15 --tags "anesthesia,pharmacology"

# Library statistics check
pdf-search --stats

# Alternative search engine
pdf-brain search "{topic}" --limit 10

# Fallback chain
pdf-search "{topic}" --limit 10 || pdf-brain search "{topic}" --limit 10
```

**Tag-Based Routing:**
```python
def select_textbook_tags(topic: str, specialty: str) -> str:
    tag_map = {
        "anesthesia": "ANZCA,anesthesia",
        "obstetrics": "RANZCOG,obstetrics",
        "pharmacology": "pharmacology,drugs",
        "physiology": "physiology,mechanisms",
        "emergency": "emergency,critical-care"
    }
    return tag_map.get(specialty, "")
```

### Σₐ — Authoritative Context (research)

**Mode Selection:**
```bash
# Medical education (PEX sources)
research pex-grounding -t "{topic}" --specialty {specialty} --format json

# Fact verification with evidence chain
research fact-check -t "{claim}" --format json --graph

# Framework documentation
research docs -t "{query}" -k "{framework}" --format json

# Academic papers
research academic -t "{topic}" --domain pubmed.ncbi.nlm.nih.gov --format json

# SDK/API reference
research sdk-api -t "{query}" --sdk aws --format json
```

**Advanced Operations:**
```bash
# File input for batch processing
research pex-grounding -i claims.txt --format json -o grounded.json

# Stdin pipeline
echo "{claim}" | research fact-check --stdin --format json

# Graph building with dry-run preview
research pex-grounding -t "{topic}" --graph --dry-run

# Local NER only (faster, offline)
research pex-grounding -t "{topic}" --local-ner-only --format json

# High concurrency for speed
research pex-grounding -t "{topic}" --concurrency 10 --format json

# Obsidian vault output
research pex-grounding -t "{topic}" -f obsidian -o ~/vault/grounding/{topic}.md

# Health check before pipeline
research health
```

**Provider-Aware Routing:**
```python
RESEARCH_MODES = {
    "fact_verification": {
        "mode": "fact-check",
        "providers": ["perplexity", "exa"],
        "confidence_threshold": 0.8
    },
    "medical_education": {
        "mode": "pex-grounding",
        "providers": ["perplexity", "exa", "tavily"],
        "sources": ["derangedphysiology.com", "litfl.com", "emcrit.org"]
    },
    "academic": {
        "mode": "academic",
        "providers": ["serp", "perplexity", "tavily"],
        "domains": ["pubmed", "arxiv", "scholar.google"]
    },
    "documentation": {
        "mode": "docs",
        "providers": ["docfork", "context7", "ref"]
    },
    "api_reference": {
        "mode": "sdk-api",
        "providers": ["context7", "ref", "jina"]
    }
}
```

### Σₛ — Screen Context (screenapp)

**Basic Extraction:**
```bash
# Semantic transcript search
screenapp files search "{topic}" --semantic --limit 5 --json

# Daily recordings context
screenapp workflow daily $(date +%Y-%m-%d) --json

# Recent recordings (time-windowed)
screenapp workflow recent --hours 24 --json
```

**Advanced Operations:**
```bash
# Multimodal AI query on specific recording
screenapp ask {fileId} "{question}" --mode transcript --json

# Video frame analysis
screenapp ask {fileId} "{question}" --mode video --json

# Time-segment specific analysis
screenapp ask {fileId} "{question}" --start 60 --end 300 --json

# Cross-recording semantic search
screenapp workflow search "{topic}" --limit 10 --json

# Graph-based queries
screenapp graph query "
  MATCH (r:Recording)-[:COVERS_TOPIC]->(t:Topic)
  WHERE t.name CONTAINS '{topic}'
  RETURN r.name, r.id, t.name
  ORDER BY r.createdAt DESC
  LIMIT 10
" --json

# Find similar recordings
screenapp graph query "
  MATCH (r:Recording {id: '{id}'})-[:SIMILAR_TO]->(s)
  RETURN s.name, s.id
  LIMIT 5
" --json

# Speaker-based queries
screenapp graph query "
  MATCH (r:Recording)-[:FEATURES_SPEAKER]->(sp:Speaker)
  WHERE sp.name CONTAINS '{speaker}'
  RETURN r.name, r.id, sp.name
" --json
```

**Context-Aware Routing:**
```python
SCREENAPP_MODES = {
    "transcript_search": {
        "mode": "semantic",
        "output": "--json",
        "relevance_threshold": 0.7
    },
    "visual_analysis": {
        "mode": "video",
        "output": "--json",
        "requires": "file_id"
    },
    "temporal_context": {
        "mode": "daily|recent",
        "output": "--json",
        "requires": "date|hours"
    },
    "ai_insights": {
        "mode": "ask",
        "output": "--json",
        "requires": "file_id,question"
    }
}
```

---

## Permutation Pipeline Compositions

### Pattern 1: Sequential Refinement with Conditional Branching

```yaml
# Composition: Σₚ ∘ (Σₜ | has_textbook_match) ∘ Σₐ ∘ Δ ∘ Ρ
#
# Personal seeds search -> Conditional textbook -> Authoritative -> Synthesis

pipeline:
  name: sequential-refinement
  nodes:
    personal:
      type: cli
      command: "limitless workflow search '{query}' --json"
      outputs: [personal_context]

    textbook_check:
      type: condition
      depends_on: [personal]
      condition: "personal_context.length > 0"
      branches:
        true: textbook_search
        false: authoritative_only

    textbook_search:
      type: cli
      command: "pdf-search '{extracted_terms}' --limit 10 --tags {specialty}"
      depends_on: [textbook_check]
      outputs: [textbook_chunks]

    authoritative_only:
      type: cli
      command: "research pex-grounding -t '{query}' --format json"
      depends_on: [textbook_check]
      outputs: [authoritative_sources]

    authoritative_full:
      type: cli
      command: "research pex-grounding -t '{query}' --specialty {specialty} --format json"
      depends_on: [textbook_search]
      outputs: [authoritative_sources]

    synthesis:
      type: aggregate
      depends_on: [textbook_search, authoritative_full, authoritative_only]
      merge_strategy: deduplicate_by_hash
```

### Pattern 2: Parallel Saturation with Timeout Fallback

```yaml
# Composition: (Σₚ ⊗ Σₗ ⊗ Σₜ ⊗ Σₐ) ∘ Δ ∘ Ρ
#
# All sources in parallel -> Aggregate -> Synthesize

pipeline:
  name: parallel-saturation
  timeout: 30s
  nodes:
    personal:
      type: cli
      command: "limitless lifelogs search '{query}' --limit 5 --json"
      timeout: 10s
      on_timeout: skip
      outputs: [personal]

    local:
      type: cli
      command: "echo '' | pieces ask '{query}' --ltm"
      timeout: 8s
      on_timeout: skip
      outputs: [local]

    textbook:
      type: cli
      command: "pdf-search '{query}' --limit 10"
      timeout: 5s
      fallback: "pdf-brain search '{query}' --limit 10"
      outputs: [textbook]

    authoritative:
      type: cli
      command: "research pex-grounding -t '{query}' --format json"
      timeout: 15s
      on_timeout: skip
      outputs: [authoritative]

    aggregate:
      type: merge
      depends_on: [personal, local, textbook, authoritative]
      merge_config:
        deduplicate: content_hash
        rank_by: confidence
        min_sources: 2
```

### Pattern 3: Recursive Deepening with Convergence

```yaml
# Composition: Σ* ∘ Τ* ∘ Δ* ∘ Ρ
#
# Recursive extraction until saturation -> Recursive grounding -> Recursive synthesis

pipeline:
  name: recursive-deepening
  max_iterations: 5
  convergence_threshold: 0.9
  nodes:
    extract_loop:
      type: recursive
      initial_command: "limitless lifelogs search '{query}' --limit 5 --json"
      expand_command: "limitless lifelogs search '{expanded_query}' --limit 10 --json"
      convergence_check: |
        (new_results - prev_results) / new_results < 0.1
      max_depth: 5
      outputs: [saturated_sources]

    ground_loop:
      type: recursive
      depends_on: [extract_loop]
      initial_command: "pdf-search '{topic}' --limit 10"
      expand_command: "pdf-search '{related_term}' --limit 5"
      convergence_check: "coverage >= 0.5"
      max_depth: 3
      outputs: [grounded_claims]

    synthesize_loop:
      type: recursive
      depends_on: [ground_loop]
      process: dialectical_synthesis
      convergence_check: "antitheses.length == 0"
      max_depth: 3
      outputs: [resolved_synthesis]
```

### Pattern 4: Conflict-Triggered Expansion

```yaml
# Composition: (Σ ∘ Τ ∘ Δ) ⊗ ((Σ ⊗ Τ)* | has_antithesis) ∘ Ρ
#
# Standard pipeline || Expansion on conflict

pipeline:
  name: conflict-triggered
  nodes:
    standard_extract:
      type: cli
      command: "pdf-search '{query}' --limit 5"
      outputs: [initial_sources]

    standard_ground:
      type: cli
      depends_on: [standard_extract]
      command: "research fact-check -t '{claims}' --format json"
      outputs: [initial_grounding]

    conflict_detect:
      type: analysis
      depends_on: [standard_ground]
      check: "antitheses.length > 0"
      outputs: [has_conflict]

    expansion_branch:
      type: condition
      depends_on: [conflict_detect]
      condition: "has_conflict == true"
      branches:
        true: deep_expansion
        false: direct_synthesis

    deep_expansion:
      type: parallel
      depends_on: [expansion_branch]
      nodes:
        expand_personal:
          command: "limitless graph query 'MATCH ... {conflict_topic}' --json"
        expand_textbook:
          command: "pdf-search '{conflict_topic}' --limit 20"
        expand_research:
          command: "research academic -t '{conflict_topic}' --format json"

    direct_synthesis:
      type: synthesis
      depends_on: [expansion_branch]
      mode: consensus

    conflict_synthesis:
      type: synthesis
      depends_on: [deep_expansion]
      mode: resolve_by_authority
```

### Pattern 5: Graph-Augmented Pipeline

```yaml
# Composition: Σ ∘ (Τ ⊗ graph_build) ∘ Δ ∘ Ρ
#
# Extract -> Parallel textbook + graph building -> Synthesize with graph context

pipeline:
  name: graph-augmented
  nodes:
    extract:
      type: cli
      command: "limitless lifelogs search '{query}' --limit 10 --json"
      outputs: [personal]

    sync_to_graph:
      type: cli
      depends_on: [extract]
      command: "limitless lifelogs sync"
      async: true

    textbook:
      type: cli
      depends_on: [extract]
      command: "pdf-search '{query}' --limit 10"
      outputs: [textbook]

    research_with_graph:
      type: cli
      depends_on: [textbook]
      command: "research pex-grounding -t '{query}' --graph --format json"
      outputs: [authoritative, graph_entities]

    graph_relationships:
      type: cli
      depends_on: [sync_to_graph, research_with_graph]
      command: "limitless graph query 'MATCH (e)-[r]-(related) WHERE e.name IN {entities} RETURN e, r, related'"
      outputs: [relationship_context]

    synthesis:
      type: aggregate
      depends_on: [textbook, authoritative, relationship_context]
      context: "Include graph relationships in synthesis"
```

---

## Conditional Logic Patterns

### Source Availability Routing

```python
def route_by_availability(preflight_result: PreflightResult) -> Composition:
    available = preflight_result.available_clis

    if all(cli in available for cli in ["limitless", "research", "pieces", "pdf-search"]):
        return "(Σₚ ⊗ Σₗ ⊗ Σₜ ⊗ Σₐ) ∘ Δ ∘ Ρ"  # Full parallel
    elif "pdf-search" in available and "research" in available:
        return "(Σₜ ⊗ Σₐ) ∘ Δ ∘ Ρ"  # Textbook + Research only
    elif "research" in available:
        return "Σₐ ∘ Δ ∘ Ρ"  # Research only
    else:
        return "Ρ"  # No grounding possible
```

### Topic Rarity Adaptation

```python
def adapt_by_rarity(initial_results: List[Source]) -> Composition:
    result_count = len(initial_results)

    if result_count >= 10:
        # Common topic: standard pipeline
        return "(Σₜ ⊗ Σₐ) ∘ Δ ∘ Ρ"
    elif result_count >= 3:
        # Moderate topic: add personal context
        return "(Σₚ ⊗ Σₜ ⊗ Σₐ) ∘ Δ ∘ Ρ"
    elif result_count >= 1:
        # Rare topic: recursive expansion
        return "Σ* ∘ Τ* ∘ Δ ∘ Ρ"
    else:
        # Niche topic: require user consent
        return "(Σ* | user_consent) ∘ Τ ∘ Δ ∘ Ρ"
```

### Confidence-Based Escalation

```python
def escalate_by_confidence(
    current_confidence: float,
    iteration: int
) -> Optional[str]:
    if current_confidence >= 0.85:
        return None  # No escalation needed

    if current_confidence >= 0.70:
        # Load additional references
        return "load_references"

    if current_confidence >= 0.50 and iteration < 3:
        # Retry with expanded sources
        return "retry_expanded"

    if current_confidence < 0.50:
        # Execute validation scripts, escalate to user
        return "execute_scripts_and_escalate"

    return None
```

### Mode-Specific Command Selection

```python
def select_commands(mode: Mode, topic: str, specialty: str) -> Dict[str, str]:
    if mode == Mode.SAQ:
        return {
            "personal": f"limitless lifelogs search '{topic}' --limit 5 --json",
            "textbook": f"pdf-search '{topic}' --limit 10 --tags {specialty}",
            "research": f"research pex-grounding -t '{topic}' --specialty {specialty} --format json",
        }
    elif mode == Mode.VIVA:
        return {
            "personal": f"limitless workflow search '{topic}' --json",
            "local": f"echo '' | pieces ask '{topic}' --ltm",
            "textbook": f"pdf-search '{topic}' --limit 20 --tags {specialty}",
            "research": f"research pex-grounding -t '{topic}' --specialty {specialty} --graph --format json",
            "academic": f"research academic -t '{topic}' --domain pubmed.ncbi.nlm.nih.gov --format json",
        }
    elif mode == Mode.ACADEMIC:
        return {
            "personal": f"limitless workflow export --start {week_ago} --end {today} --json",
            "local": f"echo '' | pieces ask '{topic}' --ltm",
            "textbook": f"pdf-search '{topic}' --limit 30",
            "research": f"research pex-grounding -t '{topic}' --graph --format json",
            "academic": f"research academic -t '{topic}' --format json",
            "fact_check": f"research fact-check -t 'synthesized_claims' --format json",
        }
```

---

## Error Handling and Fallback Chains

### Timeout Cascade

```yaml
timeout_config:
  tier_1: 5s   # Fast CLIs (pdf-search, pieces search)
  tier_2: 10s  # Medium CLIs (limitless, pdf-brain)
  tier_3: 15s  # Slow CLIs (research with graph)
  tier_4: 30s  # Complex pipelines

fallback_chains:
  textbook:
    primary: "pdf-search '{query}' --limit 10"
    fallback_1: "pdf-brain search '{query}' --limit 10"
    fallback_2: "research docs -t '{query}' --format json"

  personal:
    primary: "limitless lifelogs search '{query}' --json"
    fallback_1: "limitless workflow recent --hours 48 --json"
    fallback_2: "limitless chats list --limit 10 --json"

  local:
    primary: "echo '' | pieces ask '{query}' --ltm"
    fallback_1: "pieces search --mode ncs '{query}'"
    fallback_2: "pieces search '{query}'"
```

### Graceful Degradation

```python
def extract_with_degradation(
    query: str,
    required_sources: int = 2
) -> ExtractionResult:
    results = {}
    errors = []

    # Try all sources
    for source, command in EXTRACTION_COMMANDS.items():
        try:
            result = execute_with_timeout(command, TIMEOUTS[source])
            results[source] = result
        except TimeoutError:
            errors.append(f"{source}: timeout")
        except CLIError as e:
            errors.append(f"{source}: {e}")

    # Check minimum sources
    if len(results) < required_sources:
        raise InsufficientSourcesError(
            f"Only {len(results)} sources available, need {required_sources}",
            errors=errors
        )

    return ExtractionResult(
        sources=results,
        degraded=len(results) < len(EXTRACTION_COMMANDS),
        errors=errors
    )
```

---

## Output Aggregation and Ranking

### Merge Protocol

```python
def aggregate_sources(
    personal: List[Source],
    local: List[Source],
    textbook: List[Source],
    authoritative: List[Source]
) -> AggregatedContext:

    # Weight by source authority
    AUTHORITY_WEIGHTS = {
        "textbook": 0.95,
        "authoritative": 0.90,
        "local": 0.70,
        "personal": 0.65
    }

    all_sources = []
    for source_list, source_type in [
        (textbook, "textbook"),
        (authoritative, "authoritative"),
        (local, "local"),
        (personal, "personal")
    ]:
        for source in source_list:
            source.authority_weight = AUTHORITY_WEIGHTS[source_type]
            all_sources.append(source)

    # Deduplicate by content hash
    seen_hashes = set()
    unique = []
    for source in all_sources:
        if source.content_hash not in seen_hashes:
            seen_hashes.add(source.content_hash)
            unique.append(source)

    # Rank by weighted confidence
    ranked = sorted(
        unique,
        key=lambda s: s.confidence * s.authority_weight,
        reverse=True
    )

    return AggregatedContext(
        sources=ranked,
        diversity_score=calculate_diversity(ranked),
        confidence=calculate_aggregate_confidence(ranked)
    )
```

---

## Integration with Limitless DAG Engine

### Pipeline Template: SAQ Grounding

```yaml
# ~/.limitless-cli/templates/saq-grounding.yaml
apiVersion: pipeline/v1
kind: Pipeline
metadata:
  name: saq-grounding
  description: Full SAQ grounding pipeline with parallel extraction

spec:
  variables:
    query:
      type: string
      required: true
    specialty:
      type: string
      default: "general"
    mode:
      type: string
      default: "saq"

  nodes:
    preflight:
      type: script
      command: "python3 ~/.claude/skills/routers/grounding-router/scripts/preflight.py --format json"
      outputs: [cli_status]

    textbook:
      type: cli
      command: "pdf-search '${query}' --limit 10 --tags ${specialty}"
      depends_on: [preflight]
      condition: "cli_status.pdf_search.available == true"
      outputs: [textbook_chunks]

    research:
      type: cli
      command: "research pex-grounding -t '${query}' --specialty ${specialty} --format json"
      depends_on: [preflight]
      condition: "cli_status.research.available == true"
      outputs: [authoritative_sources]

    aggregate:
      type: merge
      depends_on: [textbook, research]
      config:
        deduplicate: true
        rank_by: authority
      outputs: [merged_sources]

    validate:
      type: script
      command: "python3 ~/.claude/skills/routers/grounding-router/scripts/validate.py -s ${merged_sources} --format json"
      depends_on: [aggregate]
      outputs: [validation_result]

    final:
      type: output
      depends_on: [validate]
      condition: "validation_result.passed == true"
      outputs: [grounded_context]
```

### Execution Command

```bash
# Run SAQ grounding pipeline
limitless pipeline run saq-grounding \
  --var query="labetalol pharmacology in pregnancy" \
  --var specialty="obstetrics" \
  --verbose

# Dry-run validation
limitless pipeline run saq-grounding \
  --var query="propofol context-sensitive half-time" \
  --dry-run
```

---

## Health Check Integration

```python
async def comprehensive_health_check() -> HealthReport:
    checks = {
        "limitless": {
            "command": "limitless lifelogs list --limit 1 --json",
            "timeout": 10,
            "required": False
        },
        "research": {
            "command": "research health",
            "timeout": 15,
            "required": True  # Core for grounding
        },
        "pieces": {
            "command": "which pieces && echo 'ok'",
            "timeout": 5,
            "required": False
        },
        "pdf-search": {
            "command": "pdf-search --stats | head -1",
            "timeout": 5,
            "required": True  # Core for textbook
        },
        "pdf-brain": {
            "command": "pdf-brain --stats | head -1",
            "timeout": 5,
            "required": False  # Fallback only
        }
    }

    results = await asyncio.gather(*[
        check_cli(name, cfg) for name, cfg in checks.items()
    ])

    required_passed = all(
        r.passed for r, cfg in zip(results, checks.values())
        if cfg["required"]
    )

    return HealthReport(
        checks=results,
        status="HEALTHY" if required_passed else "DEGRADED",
        can_proceed=required_passed
    )
```

---

## Advanced Feature Summary

| CLI | Feature | Use Case | Command Pattern |
|:----|:--------|:---------|:----------------|
| limitless | DAG Pipeline | Complex multi-step workflows | `pipeline run <template> --var k=v` |
| limitless | Graph Query | Relationship-based context | `graph query "CYPHER"` |
| limitless | Workflow Export | Longitudinal context | `workflow export --start --end` |
| research | Graph Building | Persist entities to Neo4j | `--graph` |
| research | Local NER | Offline entity extraction | `--local-ner-only` |
| research | Concurrency | Parallel API calls | `--concurrency N` |
| research | Obsidian Output | Vault integration | `-f obsidian -o file.md` |
| pieces | Multi-file Context | Grounded queries | `-f file1.py file2.py` |
| pieces | Material Combination | Composite context | `-m 1 2 3` |
| pieces | Search Modes | Semantic/Exact/Fuzzy | `--mode ncs|fts|fuzzy` |
| pdf-search | Tag Filtering | Specialty routing | `--tags ANZCA,pharmacology` |
| pdf-brain | Fallback | Alternative search | Used when pdf-search fails |
