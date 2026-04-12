# Extending the Orchestrator Reference

Guide for adding new skills to the orchestration system.

## Overview

The knowledge orchestrator is designed to be extensible. To add coordination for a new skill, you need to:

1. Add keyword catalog for skill detection
2. Define trigger conditions and confidence scoring
3. Map integration points (output transformations)
4. Add validation criteria
5. (Optional) Define new workflow patterns

---

## Step 1: Add Keyword Catalog

Edit SKILL.md, section "1. Semantic Task Analysis" → "Keyword Catalogs"

```markdown
**Keyword Catalogs:**
- **Obsidian**: vault, wikilink, dataview, frontmatter, callout, note, .md, mermaid, templater
- **Reasoning**: analyze, strategic, tactical, decompose, converge, multi-level, planning
- **Graph**: entities, relationships, extract, ontology, schema, knowledge graph, mapping
+ **NewSkill**: keyword1, keyword2, keyword3, feature1, feature2, action1
```

**Guidelines:**
- Include 5-10 highly specific keywords
- Mix feature names, action verbs, and domain terms
- Avoid generic terms that overlap with existing skills
- Test keywords on sample requests to verify discrimination

---

## Step 2: Define Trigger Conditions

Edit `references/decision_logic.md`, add to Rule Set 1 or 2:

```python
# Rule Set 1: Explicit Triggers (0.90-1.0 confidence)

**NewSkill Triggers:**
if count_keywords(request, NEWSKILL_KEYWORDS) >= 3:
    confidence = 0.90
elif "specific_unique_feature" in request:
    confidence = 0.92
elif task_features.requires_newskill_capability:
    confidence = 0.88
```

**Confidence Guidelines:**
- **0.95+**: Unambiguous, unique signals (e.g., file extension, explicit feature mention)
- **0.90-0.94**: Strong multi-keyword presence or clear intent
- **0.85-0.89**: Moderate keyword presence + context support
- **0.70-0.84**: Implicit signals, circumstantial evidence

**Test Cases:**
Create 5-10 example requests and verify confidence scores:

```python
test_cases = [
    {
        "request": "Use newskill to process this data",
        "expected_skill": "newskill",
        "expected_confidence": 0.95
    },
    {
        "request": "I need feature1 and feature2 capabilities",
        "expected_skill": "newskill",
        "expected_confidence": 0.90
    },
    # ... more cases
]
```

---

## Step 3: Map Integration Points

Edit `references/integration_mappings.md`, add new section:

```markdown
## NewSkill → Obsidian-Markdown

### NewSkill Output → Markdown Element

**Transformation:**
```python
def newskill_output_to_markdown(output):
    # Convert newskill's primary output to markdown
    markdown = f"# {output.title}\n\n"
    markdown += f"{output.content}\n\n"

    # Add newskill-specific elements
    for item in output.special_items:
        markdown += f"- {item}\n"

    return markdown
```

**Example:**
```json
Input (NewSkill output):
{
  "title": "Analysis Result",
  "content": "Detailed findings...",
  "special_items": ["Item 1", "Item 2"]
}

Output (Markdown):
```
# Analysis Result

Detailed findings...

- Item 1
- Item 2
```
```

## NewSkill → Knowledge-Graph

### NewSkill Output → Entities/Relationships

**Transformation:**
```python
def newskill_to_entities(output):
    entities = []
    for component in output.components:
        entities.append({
            "id": sanitize_id(component.name),
            "type": "NewSkillComponent",
            "name": component.name,
            "properties": component.properties,
            "confidence": 0.90  # High confidence from structured output
        })
    return entities
```

---

## Step 4: Add Validation Criteria

Edit `references/validation_criteria.md`, add new section:

```markdown
## NewSkill Validation

### Critical Checks (Must Pass)

- [ ] **Output structure valid** - Required fields present
- [ ] **Data types correct** - No type mismatches
- [ ] **No empty results** - Meaningful output generated

### Quality Checks (Affect Score)

- [ ] **Completeness** (0.3 weight)
  - Target: All requested features processed
  - Acceptable: ≥ 80% of features
  - Warning: < 80% completeness

- [ ] **Accuracy** (0.3 weight)
  - Target: ≥ 95% accuracy (if measurable)
  - Acceptable: ≥ 90% accuracy
  - Warning: < 90% accuracy

- [ ] **Performance** (0.2 weight)
  - Target: Completed within expected time
  - Acceptable: ≤ 2x expected time
  - Warning: > 2x expected time

- [ ] **Output quality** (0.2 weight)
  - Target: Well-formatted, usable output
  - Acceptable: Minor formatting issues
  - Warning: Major issues affecting usability

### Scoring Formula

```python
quality_score = 1.0

if not critical_checks_pass():
    return ValidationResult(passed=False, quality_score=0.0)

completeness_points = assess_completeness() * 0.30
accuracy_points = assess_accuracy() * 0.30
performance_points = assess_performance() * 0.20
quality_points = assess_output_quality() * 0.20

quality_score = (
    completeness_points +
    accuracy_points +
    performance_points +
    quality_points
)

return ValidationResult(
    passed=quality_score >= 0.6,
    quality_score=quality_score
)
```
```

---

## Step 5: Define Workflow Patterns (Optional)

If the new skill composes well with existing skills, define workflow patterns.

Edit `references/workflow_patterns.md`, add new pattern:

```yaml
newskill_enhance_document:
  description: "Use NewSkill to enhance existing documentation"
  trigger_conditions:
    - newskill_applicable: true
    - artifact_type: file
    - enhancement_requested: true

  sequence:
    1. newskill:
       purpose: "Analyze and enhance content"
       input: user_request.source_content
       output_binding: enhanced_content

    2. obsidian-markdown:
       purpose: "Format enhanced content"
       input:
         content: enhanced_content
         template: note-template
       output_binding: final_note
```

---

## Integration Checklist

Before deploying new skill integration:

- [ ] Keyword catalog added to SKILL.md
- [ ] Trigger conditions defined in decision_logic.md
- [ ] Integration mappings documented for all applicable skills
- [ ] Validation criteria added to validation_criteria.md
- [ ] (If applicable) Workflow patterns defined
- [ ] Test cases created and verified
- [ ] Edge cases identified and handled
- [ ] Documentation updated in SKILL.md examples

---

## Example: Adding a "Data Visualization" Skill

### 1. Keywords
```
- **DataViz**: visualize, chart, graph, plot, dashboard, heatmap, scatter, bar chart
```

### 2. Triggers
```python
if count_keywords(request, DATAVIZ_KEYWORDS) >= 2:
    confidence = 0.90
elif "visualize" in request or "chart" in request:
    confidence = 0.85
```

### 3. Integration: DataViz → Obsidian

```python
def dataviz_to_markdown(chart_output):
    # Embed chart as image
    markdown = f"![{chart_output.title}]({chart_output.image_path})\n\n"

    # Add chart description
    markdown += f"**Type**: {chart_output.chart_type}\n"
    markdown += f"**Data Points**: {chart_output.data_count}\n\n"

    return markdown
```

### 4. Integration: KG → DataViz

```python
def kg_to_dataviz(graph):
    # Visualize graph as network diagram
    return {
        "chart_type": "network",
        "nodes": graph.entities,
        "edges": graph.relationships,
        "layout": "force-directed"
    }
```

### 5. Workflow: Analyze → Visualize → Document

```yaml
analyze_visualize_document:
  sequence:
    1. hierarchical-reasoning (decompose problem)
    2. data-viz (create visualizations)
    3. obsidian-markdown (combine text + visuals)
```

---

## Advanced: Custom Task Analyzers

For complex skills, you may need custom task feature detection:

```python
# Add to task_classifier.py

def detect_newskill_features(request):
    features = {}

    # Custom detection logic
    if "special_pattern" in request:
        features["newskill_mode"] = "advanced"
    elif complexity_heuristic(request) > 0.8:
        features["newskill_mode"] = "deep_analysis"
    else:
        features["newskill_mode"] = "standard"

    return features
```

Then use in skill selector:

```python
if task_features.newskill_mode == "advanced":
    confidence = 0.95
elif task_features.newskill_mode == "deep_analysis":
    confidence = 0.90
```

---

## Anti-Patterns to Avoid

### ❌ Overlapping Keywords
Don't reuse keywords from existing skills - causes ambiguity

### ❌ Over-Confident Triggers
Don't assign 0.95+ confidence to weak signals

### ❌ Missing Integration Points
Don't skip integration mappings - skills become isolated

### ❌ Incomplete Validation
Don't forget edge cases in validation criteria

### ❌ Workflow Explosion
Don't create workflows for every skill combination - focus on valuable patterns

---

## Testing New Skill Integration

### Unit Tests

```python
def test_newskill_detection():
    request = "I need feature1 to process this"
    features = analyze_task(request)
    selection = select_skills(features)

    assert "newskill" in selection.skills
    assert selection.confidence >= 0.85

def test_newskill_integration():
    newskill_output = mock_newskill_output()
    markdown = newskill_to_markdown(newskill_output)

    assert "# " in markdown  # Has heading
    assert markdown.strip()  # Non-empty
```

### Integration Tests

```python
def test_workflow_with_newskill():
    request = "Use newskill and obsidian to create documentation"
    result = orchestrator.execute(request)

    assert result.skills_used == ["newskill", "obsidian-markdown"]
    assert result.validation.passed
    assert result.quality_score >= 0.7
```

### User Acceptance Tests

Create realistic scenarios and verify orchestrator behavior:

```
Scenario 1: User requests newskill explicitly
  Request: "Apply newskill to analyze this data"
  Expected: newskill selected with 0.95+ confidence

Scenario 2: User requests newskill implicitly
  Request: "I need feature1 and feature2 on this dataset"
  Expected: newskill selected with 0.85+ confidence

Scenario 3: User requests multi-skill workflow
  Request: "Analyze with newskill then create an Obsidian note"
  Expected: workflow pattern detected and executed
```

---

## Deployment

After extending the orchestrator:

1. **Validate**: Run `scripts/validate_workflow.py` if you added patterns
2. **Test**: Execute unit and integration tests
3. **Document**: Update SKILL.md with newskill examples
4. **Package**: Re-run `package_skill.py` to create new distributable
5. **Announce**: Update changelog with new skill support

---

**Core Principle**: New skills should integrate seamlessly, enhancing the orchestrator's capabilities without increasing complexity for users. Clear triggers, well-defined transformations, and thorough validation ensure quality integration.
