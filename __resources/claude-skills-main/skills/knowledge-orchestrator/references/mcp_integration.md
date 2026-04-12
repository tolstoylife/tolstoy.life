# MCP Integration Reference

MCP tool usage patterns and best practices for context enrichment.

## Hybrid MCP Approach

The orchestrator uses a **hybrid approach** to MCP integration:

1. **Pre-delegation enrichment**: Gather context before invoking skills
2. **Skill-specific preparation**: Load relevant schemas, examples, templates
3. **Minimal overhead**: Use 1-3 MCP tools per enrichment cycle
4. **Delegate intensive work**: Skills handle their own deep MCP usage

This balances context quality with token efficiency.

---

## Obsidian-Markdown Enrichment

### Use Cases
- User creating notes without specifying template type
- Vault conventions unknown or need refreshing
- User requests Obsidian-specific features

### MCP Tools

**1. mcp__obsidian-dev__search-docs**
```python
# Search for feature documentation
mcp__obsidian-dev__search-docs(
    query="wikilink syntax embedding"
)

# Get plugin integration examples
mcp__obsidian-dev__search-docs(
    query="dataview query examples"
)
```

**Use when:**
- User mentions unfamiliar Obsidian feature
- Need to verify syntax for advanced features
- Clarifying plugin capabilities

**2. Read (vault files)**
```python
# Analyze vault conventions
vault_files = glob("~/.obsidian/vault/**/*.md")
sample_notes = vault_files[:5]  # Sample for pattern analysis

for note in sample_notes:
    content = Read(note)
    analyze_frontmatter_patterns(content)
    analyze_tag_usage(content)
    analyze_linking_patterns(content)
```

**Use when:**
- User has existing vault with established conventions
- Need to match existing note structure
- Template selection requires context

**3. Template Selection Logic**
```python
def select_template(note_type, complexity):
    if note_type == "moc" or complexity > 0.7:
        return Read("obsidian-markdown/assets/templates/moc-template.md")
    elif note_type == "daily":
        return Read("obsidian-markdown/assets/templates/daily-note-template.md")
    else:
        return Read("obsidian-markdown/assets/templates/note-template.md")
```

### Enrichment Output

```python
{
    "vault_conventions": {
        "tag_pattern": "hierarchical (e.g., #concept/database)",
        "wikilink_style": "with_display_text",
        "frontmatter_properties": ["created", "modified", "tags", "status"]
    },
    "selected_template": "moc-template",
    "reference_docs": {
        "dataview_syntax": "<loaded_content>",
        "mermaid_diagrams": "<loaded_content>"
    }
}
```

---

## Hierarchical-Reasoning Enrichment

### Use Cases
- Complex problem requiring constraint identification
- Unfamiliar domain needing success criteria
- Convergence parameter optimization

### MCP Tools

**1. WebSearch (domain research)**
```python
# Research domain-specific approaches
WebSearch(query=f"{domain} best practices methodology 2024")

# Find example problem decompositions
WebSearch(query=f"{problem_type} strategic analysis framework")
```

**Use when:**
- Domain is specialized or unfamiliar
- Need to set appropriate success criteria
- Looking for established methodologies

**2. Constraint Identification**
```python
def identify_constraints(task_features):
    constraints = []

    # Technical constraints
    if task_features.domain == "software":
        constraints.extend([
            "Maintainability",
            "Performance",
            "Scalability"
        ])

    # Resource constraints (infer from complexity)
    if task_features.complexity_score > 0.8:
        constraints.append("Time-bounded analysis")

    # Domain-specific (from MCP)
    domain_constraints = WebSearch(
        query=f"{task_features.domain} common constraints"
    )
    constraints.extend(extract_constraints(domain_constraints))

    return constraints
```

**3. Success Criteria Definition**
```python
def define_success_metrics(complexity, domain):
    base_criteria = {
        "convergence_threshold": 0.95 if complexity > 0.8 else 0.90,
        "min_confidence": 0.80,
        "strategic_depth": "comprehensive" if complexity > 0.7 else "focused"
    }

    # Domain-specific criteria from MCP
    domain_criteria = WebSearch(
        query=f"{domain} analysis quality metrics"
    )
    base_criteria.update(extract_metrics(domain_criteria))

    return base_criteria
```

### Enrichment Output

```python
{
    "constraints": [
        "System must scale to 100k users",
        "Budget limited to $50k",
        "Maintainability is priority"
    ],
    "success_criteria": {
        "convergence_threshold": 0.95,
        "min_confidence": 0.80,
        "covers_all_constraints": true
    },
    "convergence_parameters": {
        "max_strategic_cycles": 5,  # Higher for complex problems
        "max_tactical_cycles": 7,
        "max_operational_cycles": 10
    },
    "domain_examples": "<relevant_problem_decompositions>"
}
```

---

## Knowledge-Graph Enrichment

### Use Cases
- Extracting from unfamiliar domain
- Need domain-specific ontology
- Looking for extraction examples

### MCP Tools

**1. Read (schema files)**
```python
# Load appropriate ontology
if domain == "software" or domain == "coding":
    ontology = Read("knowledge-graph/schemas/coding_domain.md")
else:
    ontology = Read("knowledge-graph/schemas/core_ontology.md")

# Parse entity types and relationship types
entity_types = extract_entity_types(ontology)
relationship_types = extract_relationship_types(ontology)
```

**2. WebSearch (example extractions)**
```python
# Find similar extraction tasks
examples = WebSearch(
    query=f"{domain} knowledge graph entity extraction examples"
)

# Get domain-specific relationship patterns
rel_patterns = WebSearch(
    query=f"{domain} common entity relationships taxonomy"
)
```

**3. Confidence Threshold Tuning**
```python
def set_confidence_threshold(complexity, domain_familiarity):
    # Higher complexity → lower threshold (accept more uncertainty)
    # Unfamiliar domain → higher threshold (be conservative)

    base_threshold = 0.70

    if complexity > 0.8:
        base_threshold -= 0.10  # 0.60 for very complex

    if domain_familiarity == "low":
        base_threshold += 0.10  # 0.80 for unfamiliar

    return max(0.50, min(0.90, base_threshold))
```

### Enrichment Output

```python
{
    "ontology": {
        "entity_types": ["Person", "Organization", "Concept", "Technology"],
        "relationship_types": ["WORKS_FOR", "USES", "IMPLEMENTS", "RELATED_TO"]
    },
    "extraction_examples": [
        {
            "source": "Similar domain extraction",
            "entities_found": 12,
            "avg_confidence": 0.85,
            "patterns": ["CamelCase terms", "Proper nouns", "Technical jargon"]
        }
    ],
    "confidence_threshold": 0.70,
    "focus_areas": ["Key algorithms", "System components", "Architectural patterns"]
}
```

---

## MCP Tool Selection Matrix

| Enrichment Need | Primary Tool | Secondary Tool | Fallback |
|---|---|---|---|
| Obsidian syntax | mcp__obsidian-dev__search-docs | Read (references) | WebSearch |
| Vault conventions | Read (vault files) | Glob (pattern detection) | None (use defaults) |
| Domain research | WebSearch | mcp__exa__web_search_exa | None |
| Code analysis | mcp__deepgraph__* | Grep (codebase) | Read (files) |
| Schema loading | Read (skill files) | None | Use core_ontology |
| Examples | WebSearch | mcp__exa__web_search_exa | Pre-loaded examples |

---

## MCP Usage Best Practices

### 1. Minimize Tool Calls

**DON'T:**
```python
# Too many calls for simple enrichment
ontology = mcp_search_docs("entity types")
relationships = mcp_search_docs("relationship types")
examples = mcp_search_docs("extraction examples")
best_practices = mcp_search_docs("extraction tips")
# 4 MCP calls for knowledge-graph enrichment
```

**DO:**
```python
# Single call to load complete schema
ontology = Read("knowledge-graph/schemas/core_ontology.md")
# Contains entity types, relationships, examples, best practices
# 1 Read call replaces 4 MCP calls
```

### 2. Cache MCP Results

```python
class MCPCache:
    def __init__(self):
        self._cache = {}

    def get_or_fetch(self, key, fetch_fn):
        if key not in self._cache:
            self._cache[key] = fetch_fn()
        return self._cache[key]

# Usage
cache = MCPCache()
ontology = cache.get_or_fetch(
    "core_ontology",
    lambda: Read("knowledge-graph/schemas/core_ontology.md")
)
```

### 3. Prefer Local Resources

**Priority Order:**
1. Skill bundled resources (Read from skill directories)
2. User's local files (Read from vault/repo)
3. MCP tools (WebSearch, mcp__obsidian-dev__search-docs)
4. Defaults (hardcoded fallbacks)

### 4. Fail Gracefully

```python
try:
    vault_conventions = analyze_vault_files()
except FileNotFoundError:
    vault_conventions = DEFAULT_CONVENTIONS

try:
    domain_examples = WebSearch(f"{domain} examples")
except MCPError:
    domain_examples = BUILTIN_EXAMPLES
```

### 5. Time-Box MCP Usage

```python
# Limit enrichment to max 3 MCP tools
max_mcp_calls = 3
calls_made = 0

if calls_made < max_mcp_calls:
    ontology = Read("schema.md")
    calls_made += 1

if calls_made < max_mcp_calls and domain_unfamiliar:
    examples = WebSearch(f"{domain} examples")
    calls_made += 1

# If we hit limit, proceed with what we have
```

---

## Context Enrichment Workflow

```
1. Analyze Task Features
   ↓
2. Determine Enrichment Needs
   ├─ Obsidian: Template + conventions?
   ├─ H-Reasoning: Constraints + criteria?
   └─ KG: Ontology + examples?
   ↓
3. Check Local Resources First
   ├─ Skill bundled files (Read)
   ├─ User vault/repo (Read/Glob)
   └─ Cached results
   ↓
4. Use MCP Tools If Needed (max 3)
   ├─ WebSearch for domain research
   ├─ mcp__*__search-docs for technical docs
   └─ mcp__deepgraph for code analysis
   ↓
5. Prepare Enriched Context
   ├─ Combine local + MCP results
   ├─ Format for skill input
   └─ Set parameters (thresholds, cycles, etc.)
   ↓
6. Delegate to Skill(s)
```

---

## Example Enrichment Scenarios

### Scenario 1: Creating Technical Note

```python
# Minimal enrichment - local resources sufficient
context = {
    "template": Read("obsidian-markdown/assets/templates/note-template.md"),
    "vault_conventions": analyze_local_vault(),  # 1 Glob + 3 Reads
    "reference": None  # Not needed for basic note
}
# Total: 4 file operations, 0 MCP calls
```

### Scenario 2: Complex Domain Analysis

```python
# Moderate enrichment - need domain context
context = {
    "constraints": identify_from_request(),  # No MCP
    "success_criteria": DEFAULTS,  # No MCP
    "domain_background": WebSearch(f"{domain} overview"),  # 1 MCP call
    "examples": WebSearch(f"{domain} analysis examples")  # 1 MCP call
}
# Total: 2 MCP calls (under limit)
```

### Scenario 3: Unfamiliar Domain Extraction

```python
# Full enrichment - need everything
context = {
    "ontology": Read("knowledge-graph/schemas/core_ontology.md"),  # 1 Read
    "domain_examples": WebSearch(f"{domain} entity extraction"),  # 1 MCP
    "relationship_patterns": WebSearch(f"{domain} relationships"),  # 1 MCP
    "focus_areas": derive_from_request()  # No MCP
}
# Total: 1 Read, 2 MCP calls (efficient)
```

---

## MCP Integration Anti-Patterns

### ❌ Over-Fetching
Don't fetch information you won't use.

### ❌ Duplicate Fetching
Don't fetch the same resource multiple times - cache it.

### ❌ Synchronous Waterfall
Don't wait for MCP call 1 to complete before starting MCP call 2 if they're independent.

### ❌ Ignoring Failures
Don't halt entire workflow if MCP enrichment fails - use defaults.

### ❌ MCP for Everything
Don't use MCP tools when local resources contain the answer.

---

**Core Principle**: MCP enrichment should enhance skill execution, not become a bottleneck. Prioritize local resources, limit MCP calls, cache results, and fail gracefully.
