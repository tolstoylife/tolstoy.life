# Validation Criteria Reference

Quality checklists and thresholds for each skill's outputs.

## Obsidian-Markdown Validation

### Critical Checks (Must Pass)

- [ ] **Valid YAML frontmatter** - Opens with `---`, closes with `---`, valid YAML syntax
- [ ] **No tabs in YAML** - Only spaces used for indentation
- [ ] **Proper date format** - Dates use `YYYY-MM-DD` or `YYYY-MM-DDTHH:mm:ss`
- [ ] **Code blocks closed** - All ` ``` ` blocks have closing delimiters
- [ ] **No unescaped pipes in tables** - Use `\|` for literal pipes in table cells

### Quality Checks (Affect Score)

- [ ] **Wikilinks for internal references** (0.3 weight)
  - Internal notes use `[[wikilink]]` not `[markdown](link.md)`
  - Custom display text uses pipe: `[[note|display]]`

- [ ] **Proper callout syntax** (0.2 weight)
  - Callouts use correct format: `> [!type] Title`
  - Type is lowercase: `[!note]` not `[!NOTE]`
  - Continuation lines have `>` prefix

- [ ] **Tables well-formatted** (0.2 weight)
  - Header row present with `---` separators
  - Alignment specified: `:--` (left), `:--:` (center), `--:` (right)
  - Consistent column count across rows

- [ ] **Code blocks have language** (0.1 weight)
  - All ` ```lang ` blocks specify language
  - Only exception: generic text blocks

- [ ] **Appropriate template used** (0.1 weight)
  - Note type matches frontmatter `type` field
  - Structure follows template conventions

- [ ] **Metadata completeness** (0.1 weight)
  - `created` and `modified` dates present
  - `tags` array populated appropriately
  - Custom properties correctly typed

### Scoring Formula

```python
quality_score = 1.0

if not critical_checks_pass():
    return ValidationResult(passed=False, quality_score=0.0)

quality_score -= 0.3 * (1 - wikilinks_ratio)
quality_score -= 0.2 * (1 - callouts_valid_ratio)
quality_score -= 0.2 * (1 - tables_valid_ratio)
quality_score -= 0.1 * (1 - code_blocks_with_lang_ratio)
quality_score -= 0.1 * template_mismatch_penalty
quality_score -= 0.1 * metadata_incompleteness_penalty

return ValidationResult(
    passed=quality_score >= 0.6,
    quality_score=max(0.0, quality_score)
)
```

### Example Validation Output

```
Obsidian-Markdown Validation Results
─────────────────────────────────────
✓ Critical checks passed (5/5)
  ✓ Valid YAML frontmatter
  ✓ No tabs in YAML
  ✓ Proper date formats
  ✓ Code blocks closed
  ✓ Escaped pipes in tables

Quality Assessment:
  Wikilinks: 8/10 internal refs use wikilinks (0.24/0.30)
  Callouts: 3/3 callouts valid syntax (0.20/0.20)
  Tables: 2/2 tables properly formatted (0.20/0.20)
  Code blocks: 5/6 have language tags (0.08/0.10)
  Template: Matches 'note-template' (0.10/0.10)
  Metadata: All required fields present (0.10/0.10)

Overall Quality Score: 0.92/1.00 ✓ PASS (threshold: 0.60)
```

---

## Hierarchical-Reasoning Validation

### Critical Checks (Must Pass)

- [ ] **All three levels present** - Strategic, tactical, operational outputs exist
- [ ] **Structured output format** - Each level has required fields
- [ ] **Non-empty insights** - Each level contains substantive content

### Quality Checks (Affect Score)

- [ ] **Convergence score** (0.4 weight)
  - Target: ≥ 0.85 (good convergence)
  - Acceptable: ≥ 0.75 (moderate convergence)
  - Warning: < 0.75 (poor convergence, may need re-run)

- [ ] **Average confidence** (0.3 weight)
  - Target: ≥ 0.80 (high confidence)
  - Acceptable: ≥ 0.70 (moderate confidence)
  - Warning: < 0.70 (low confidence, validate findings)

- [ ] **Level coherence** (0.2 weight)
  - Strategic goals align with tactical methods
  - Tactical methods supported by operational details
  - Operational details serve strategic goals

- [ ] **Uncertainty quantification** (0.1 weight)
  - Uncertainties explicitly identified
  - Confidence scores provided for claims
  - Known unknowns documented

### Scoring Formula

```python
quality_score = 1.0

if not critical_checks_pass():
    return ValidationResult(passed=False, quality_score=0.0)

# Convergence scoring
if convergence_score >= 0.85:
    convergence_points = 0.40
elif convergence_score >= 0.75:
    convergence_points = 0.30
else:
    convergence_points = 0.20 * (convergence_score / 0.75)

# Confidence scoring
if avg_confidence >= 0.80:
    confidence_points = 0.30
elif avg_confidence >= 0.70:
    confidence_points = 0.25
else:
    confidence_points = 0.15 * (avg_confidence / 0.70)

# Coherence scoring (manual assessment or heuristic)
coherence_points = assess_level_coherence() * 0.20

# Uncertainty scoring
uncertainty_points = assess_uncertainty_quality() * 0.10

quality_score = (
    convergence_points +
    confidence_points +
    coherence_points +
    uncertainty_points
)

return ValidationResult(
    passed=quality_score >= 0.6,
    quality_score=quality_score
)
```

### Example Validation Output

```
Hierarchical-Reasoning Validation Results
──────────────────────────────────────────
✓ Critical checks passed (3/3)
  ✓ All three levels present
  ✓ Structured output format
  ✓ Non-empty insights

Quality Assessment:
  Convergence: 0.92 (excellent) (0.40/0.40)
  Average Confidence: 0.85 (high) (0.30/0.30)
  Level Coherence: Strong alignment (0.18/0.20)
  Uncertainty: Well quantified (0.09/0.10)

Overall Quality Score: 0.97/1.00 ✓ PASS (threshold: 0.60)
```

---

## Knowledge-Graph Validation

### Critical Checks (Must Pass)

- [ ] **Required entity fields** - All entities have `id`, `type`, `name`
- [ ] **Reference integrity** - All relationship endpoints exist as entity IDs
- [ ] **No duplicate IDs** - Entity IDs are unique
- [ ] **Valid JSON structure** - Graph is well-formed JSON

### Quality Checks (Affect Score)

- [ ] **Entity count** (0.2 weight)
  - Target: ≥ 10 entities (rich graph)
  - Acceptable: ≥ 5 entities (moderate graph)
  - Warning: < 5 entities (sparse graph)

- [ ] **Relationship count** (0.2 weight)
  - Target: ≥ entity_count (well-connected)
  - Acceptable: ≥ 0.5 * entity_count (moderate connectivity)
  - Warning: < 0.5 * entity_count (poorly connected)

- [ ] **Isolation rate** (0.2 weight)
  - Target: < 10% isolated entities (highly connected)
  - Acceptable: < 20% isolated (moderately connected)
  - Warning: ≥ 20% isolated (fragmented graph)

- [ ] **Average confidence** (0.2 weight)
  - Target: ≥ 0.80 (high extraction confidence)
  - Acceptable: ≥ 0.70 (moderate confidence)
  - Warning: < 0.70 (low confidence, verify extractions)

- [ ] **Provenance coverage** (0.2 weight)
  - Target: 100% entities have provenance (full traceability)
  - Acceptable: ≥ 80% have provenance (mostly traceable)
  - Warning: < 80% have provenance (poor traceability)

### Scoring Formula

```python
quality_score = 1.0

if not critical_checks_pass():
    return ValidationResult(passed=False, quality_score=0.0)

# Entity count scoring
if entity_count >= 10:
    entity_points = 0.20
elif entity_count >= 5:
    entity_points = 0.15
else:
    entity_points = 0.10 * (entity_count / 5)

# Relationship count scoring
rel_per_entity = relationship_count / entity_count
if rel_per_entity >= 1.0:
    relationship_points = 0.20
elif rel_per_entity >= 0.5:
    relationship_points = 0.15
else:
    relationship_points = 0.10 * (rel_per_entity / 0.5)

# Isolation rate scoring
if isolation_rate < 0.10:
    isolation_points = 0.20
elif isolation_rate < 0.20:
    isolation_points = 0.15
else:
    isolation_points = 0.05 * (1 - isolation_rate)

# Confidence scoring
if avg_confidence >= 0.80:
    confidence_points = 0.20
elif avg_confidence >= 0.70:
    confidence_points = 0.15
else:
    confidence_points = 0.10 * (avg_confidence / 0.70)

# Provenance scoring
provenance_ratio = entities_with_provenance / entity_count
if provenance_ratio >= 1.0:
    provenance_points = 0.20
elif provenance_ratio >= 0.80:
    provenance_points = 0.15
else:
    provenance_points = 0.10 * (provenance_ratio / 0.80)

quality_score = (
    entity_points +
    relationship_points +
    isolation_points +
    confidence_points +
    provenance_points
)

return ValidationResult(
    passed=quality_score >= 0.6,
    quality_score=quality_score
)
```

### Example Validation Output

```
Knowledge-Graph Validation Results
───────────────────────────────────
✓ Critical checks passed (4/4)
  ✓ Required entity fields present
  ✓ Reference integrity maintained
  ✓ No duplicate IDs
  ✓ Valid JSON structure

Quality Assessment:
  Entity Count: 15 entities (rich) (0.20/0.20)
  Relationships: 18 relationships (1.2 per entity) (0.20/0.20)
  Isolation Rate: 6.7% isolated (highly connected) (0.20/0.20)
  Avg Confidence: 0.82 (high) (0.20/0.20)
  Provenance: 100% coverage (0.20/0.20)

Overall Quality Score: 1.00/1.00 ✓ PASS (threshold: 0.60)
```

---

## Orchestrator Meta-Validation

Validate the orchestrator's own decisions:

### Decision Quality Checks

- [ ] **Skill selection confidence** - Selected skill(s) have confidence ≥ 0.70
- [ ] **Workflow pattern match** - If multi-skill, pattern clearly identified
- [ ] **No contradictory selections** - Skills don't have conflicting requirements
- [ ] **User intent alignment** - Selection matches apparent user goal

### Execution Quality Checks

- [ ] **All skills completed** - No mid-workflow failures
- [ ] **Data flow integrity** - Outputs successfully transformed to inputs
- [ ] **Final output coherence** - Combined output makes sense as whole
- [ ] **Quality threshold met** - Final output passes validation for target skill

### Meta-Scoring

```python
meta_quality = (
    0.3 * selection_confidence +
    0.3 * execution_success_rate +
    0.2 * data_flow_integrity +
    0.2 * final_output_quality
)

# If meta-quality < 0.70, provide explanation to user
if meta_quality < 0.70:
    explain_orchestrator_decisions()
    offer_alternative_approaches()
```

---

## Validation Failure Actions

### Obsidian-Markdown Failures
- **Critical failure**: Ask user if they want standard markdown instead
- **Quality < 0.60**: Offer to fix specific issues and re-validate

### Hierarchical-Reasoning Failures
- **Low convergence (<0.75)**: Suggest increasing cycle counts and re-running
- **Low confidence (<0.70)**: Highlight uncertain areas, suggest additional context

### Knowledge-Graph Failures
- **Sparse graph (<5 entities)**: Suggest re-extraction with broader scope
- **High isolation (>20%)**: Trigger refinement analysis, suggest relationship discovery

### Workflow Failures
- **Mid-workflow failure**: Offer to continue from last successful step
- **Low overall quality**: Suggest trying single highest-confidence skill instead
