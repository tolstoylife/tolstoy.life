# Decision Logic Reference

Complete specification of skill selection rules, confidence scoring, and edge case handling.

## Confidence-Weighted Decision Rules

### Rule Set 1: Explicit Triggers (0.90-1.0)

**Obsidian-Markdown Triggers:**
```python
if creates_md_file or ".md" in request:
    confidence = 0.95
elif count_keywords(request, OBSIDIAN_KEYWORDS) >= 3:
    confidence = 0.92
elif "vault" in request or "wikilink" in request:
    confidence = 0.90
```

**Knowledge-Graph Triggers:**
```python
if requires_extraction and content_type != "code":
    confidence = 0.90
elif count_keywords(request, GRAPH_KEYWORDS) >= 2:
    confidence = 0.88
elif "ontology" in request or "schema" in request:
    confidence = 0.90
```

**Hierarchical-Reasoning Triggers:**
```python
if complexity_score > 0.7 and requires_decomposition:
    confidence = 0.90
elif count_keywords(request, REASONING_KEYWORDS) >= 3:
    confidence = 0.88
elif "strategic" in request or "analyze" in request:
    confidence = 0.85
```

### Rule Set 2: Implicit Triggers (0.70-0.89)

**Context-Based Inference:**
```python
# Knowledge artifact without explicit extraction request
if artifact_type == "knowledge" and "knowledge-graph" not in explicit_triggers:
    confidence = 0.75

# Complex analysis without explicit reasoning request
if complexity_score > 0.5 and artifact_type == "analysis":
    confidence = 0.72

# File creation with prose content
if artifact_type == "file" and content_type == "prose":
    confidence = 0.70
```

### Rule Set 3: Workflow Pattern Detection

When multiple skills are candidates, check for workflow patterns:

```python
def detect_workflow(candidates, features):
    # Research → Structure → Document
    if all(skill in candidates for skill in ["hierarchical-reasoning", "knowledge-graph", "obsidian-markdown"]):
        if features.complexity_score > 0.7 and features.creates_md_file:
            return "research_structure_document"

    # Extract → Validate → Format
    if all(skill in candidates for skill in ["knowledge-graph", "hierarchical-reasoning", "obsidian-markdown"]):
        if features.requires_extraction and features.artifact_type == "file":
            return "extract_validate_format"

    # Analyze → Graph → Visualize
    if all(skill in candidates for skill in ["hierarchical-reasoning", "knowledge-graph", "obsidian-markdown"]):
        if features.complexity_score > 0.6 and "visualiz" in request:
            return "analyze_graph_visualize"

    return None
```

## Edge Cases

### No Skill Matches (confidence < 0.50)

**Action**: Ask user for clarification

**Template Response:**
```
I analyzed your request but couldn't confidently determine which specialized skill would be most helpful.

Could you clarify:
- Are you creating a file/note? (→ obsidian-markdown)
- Do you need entity/relationship extraction? (→ knowledge-graph)
- Does this require strategic decomposition? (→ hierarchical-reasoning)

Or specify directly: "Use [skill-name] for this task"
```

### Multiple High-Confidence Candidates (no workflow match)

**Action**: Select highest confidence, mention alternatives

**Template Response:**
```
I'm using [highest-confidence-skill] for this task (confidence: 0.XX).

Alternative approaches:
- [skill-2]: confidence 0.YY - better for [use case]
- [skill-3]: confidence 0.ZZ - better for [use case]

Override with: "Actually, use [skill-name] instead"
```

### Borderline Confidence (0.50-0.69)

**Action**: Present options to user

**Template Response:**
```
I have moderate confidence about the best approach:

Option 1: [skill-name] (confidence: 0.XX)
  Pros: [benefits]
  Cons: [limitations]

Option 2: [skill-name] (confidence: 0.YY)
  Pros: [benefits]
  Cons: [limitations]

Which would you prefer, or should I choose based on [deciding factor]?
```

### User Override Detection

**Patterns that disable orchestrator:**
- "Don't use the orchestrator"
- "Just [simple action without skill name]"
- "Use [specific-skill-name] only"
- "Skip skill selection"

**Patterns that specify skill:**
- "Use hierarchical-reasoning for this"
- "Apply knowledge-graph to extract..."
- "Format with obsidian-markdown"

## Decision Examples

### Example 1: Clear Single-Skill

```
Request: "Create a meeting note for today"

Analysis:
  creates_md_file: true ("note")
  obsidian_signals: 1 ("note")
  complexity_score: 0.2 (simple structure)

Selection:
  obsidian-markdown: 0.95 (explicit trigger)

Action: Execute obsidian-markdown immediately
```

### Example 2: Multi-Skill Workflow

```
Request: "Research microservices patterns and create a comprehensive guide with architecture diagrams"

Analysis:
  complexity_score: 0.85 (research + structure + visualization)
  requires_decomposition: true ("patterns", "architecture")
  requires_extraction: true (implied by "comprehensive")
  creates_md_file: true ("guide")

Selection:
  hierarchical-reasoning: 0.90 (complexity + decomposition)
  knowledge-graph: 0.75 (implied extraction)
  obsidian-markdown: 0.95 (creates file)

Workflow Detection: research_structure_document (all three present, complexity > 0.7)

Action: Execute 3-skill workflow
```

### Example 3: Ambiguous Request

```
Request: "Help me understand this topic"

Analysis:
  complexity_score: 0.4 (unclear scope)
  artifact_type: unclear
  no clear skill signals

Selection:
  No candidates above 0.50 threshold

Action: Ask user to clarify scope and desired output
```

### Example 4: User Override

```
Request: "Use hierarchical-reasoning only to decompose this problem: [problem]"

Detection:
  User specified "Use hierarchical-reasoning only"
  Override pattern detected

Action: Skip orchestrator, delegate directly to hierarchical-reasoning
```

## Debugging Decision Logic

To explain orchestrator decisions, provide:

1. **Task Features Extracted:**
```
Content Type: prose
Artifact Type: file
Complexity Score: 0.75
Creates MD File: true
Requires Extraction: true
Obsidian Signals: 1
Graph Signals: 2
Reasoning Signals: 1
```

2. **Confidence Scores:**
```
obsidian-markdown: 0.95 (explicit: creates_md_file)
knowledge-graph: 0.88 (explicit: graph_signals >= 2)
hierarchical-reasoning: 0.72 (implicit: complexity > 0.5)
```

3. **Decision Path:**
```
Multiple candidates detected (3 skills)
Checking workflow patterns...
Match found: research_structure_document
Confidence: min(0.95, 0.88, 0.72) = 0.72 (medium-high)
Action: Execute workflow with confidence notification
```

4. **Alternatives Considered:**
```
Could execute single skill: obsidian-markdown (0.95)
  Pros: Simpler, less overhead
  Cons: Misses strategic decomposition and entity extraction

Selected workflow provides higher quality through skill composition
```
