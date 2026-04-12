# Quality Gates — Validation Checkpoints

## Gate Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    QUALITY GATE PIPELINE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  G₀: PREFLIGHT ─────────────────────────────────────────────── │
│      ├─ CLI health checks                                       │
│      ├─ API quota verification                                  │
│      └─ PDF library stats                                       │
│                                                                  │
│  G₁: SOURCE ────────────────────────────────────────────────── │
│      ├─ Minimum sources extracted                               │
│      ├─ Source diversity check                                  │
│      └─ Timeout compliance                                      │
│                                                                  │
│  G₂: TEXTBOOK ──────────────────────────────────────────────── │
│      ├─ Textbook coverage threshold                             │
│      ├─ Citation completeness                                   │
│      └─ Page reference validity                                 │
│                                                                  │
│  G₃: SYNTHESIS ─────────────────────────────────────────────── │
│      ├─ Thesis subsumption check                                │
│      ├─ Antithesis resolution verification                      │
│      └─ Parsimony constraint                                    │
│                                                                  │
│  G₄: HALLUCINATION ─────────────────────────────────────────── │
│      ├─ Citation presence check                                 │
│      ├─ Semantic entailment verification                        │
│      └─ LLM-as-judge validation                                 │
│                                                                  │
│  G₅: OUTPUT ────────────────────────────────────────────────── │
│      ├─ Word count compliance                                   │
│      ├─ Format validation                                       │
│      └─ Final confidence calculation                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## G₀: Preflight Gate

### CLI Health Checks

```python
def preflight_check() -> PreflightResult:
    checks = {
        "limitless": check_cli("limitless config show"),
        "pieces": check_cli("which pieces"),
        "pdf-search": check_cli("pdf-search --stats"),
        "research": check_cli("research --version"),
        "screenapp": check_cli("screenapp config validate")  # Optional - degraded if missing
    }

    # Core CLIs (required for critical functionality)
    core_checks = {k: v for k, v in checks.items() if k != "screenapp"}
    core_available = sum(1 for v in core_checks.values() if v)

    # Optional CLIs (enhance but not required)
    optional_available = checks.get("screenapp", False)

    if core_available == 4:
        status = "FULL" if optional_available else "FULL_LIMITED"
        return PreflightResult(status=status, degraded=False)
    elif core_available >= 2:
        return PreflightResult(status="DEGRADED", degraded=True, missing=[k for k,v in checks.items() if not v])
    else:
        return PreflightResult(status="CRITICAL", degraded=True, abort=True)
```

### Thresholds

| Condition | Action | Confidence Impact |
|-----------|--------|-------------------|
| 5/5 CLIs available | Proceed (full multimodal) | +0.05 |
| 4/5 CLIs available | Proceed (limited multimodal) | +0.0 |
| 3/5 CLIs available | Proceed with warning | -0.05 |
| 2/5 CLIs available | Require user consent | -0.15 |
| 1/5 CLIs available | Abort | N/A |

## G₁: Source Gate

### Minimum Sources

```yaml
adaptive_thresholds:
  common_topic:
    min_sources: 3
    min_per_primitive: {Σₜ: 2, Σₐ: 1}

  moderate_topic:
    min_sources: 2
    min_per_primitive: {Σₜ: 1, Σₐ: 1}

  rare_topic:
    min_sources: 2
    min_per_primitive: {Σₜ: 1, Σₐ: 0}
    warning: "Limited evidence base"

  niche_topic:
    min_sources: 1
    user_consent_required: true
```

### Source Diversity

```python
def check_diversity(sources: List[Source]) -> bool:
    types = set(s.source_type for s in sources)

    # Require at least 2 different source types
    if len(types) < 2:
        return False

    # Require at least one textbook source
    if "textbook" not in types and "pex" not in types:
        return False

    return True
```

## G₂: Textbook Gate

### Coverage Threshold

```yaml
textbook_coverage:
  saq_mode:
    min_claims_grounded: 0.50  # 50% of claims from textbooks
    min_page_citations: 3

  viva_mode:
    min_claims_grounded: 0.40  # More flexibility for clinical
    min_page_citations: 5

  academic_mode:
    min_claims_grounded: 0.60  # Higher bar for scholarly
    min_page_citations: 15
```

### Citation Completeness

```python
def validate_citations(claims: List[Claim]) -> ValidationResult:
    uncited = [c for c in claims if not c.citation]
    incomplete = [c for c in claims if c.citation and not c.citation.page]

    if len(uncited) > 0:
        return ValidationResult(
            passed=False,
            action="REMOVE_UNCITED",
            claims_affected=uncited
        )

    if len(incomplete) / len(claims) > 0.20:
        return ValidationResult(
            passed=False,
            action="WARN_INCOMPLETE",
            claims_affected=incomplete
        )

    return ValidationResult(passed=True)
```

## G₃: Synthesis Gate

### Thesis Subsumption

```python
def check_subsumption(theses: List[Thesis], syntheses: List[Synthesis]) -> bool:
    """
    Verify: ∀T_i. ∃s ∈ S. subsumes(s, T_i) OR addresses(s, T_i)
    """
    for thesis in theses:
        subsumed = any(
            subsumes(s, thesis) or addresses(s, thesis)
            for s in syntheses
        )
        if not subsumed:
            return False
    return True
```

### Antithesis Resolution

```python
def check_resolution(antitheses: List[Antithesis], syntheses: List[Synthesis]) -> ValidationResult:
    unresolved = []

    for antithesis in antitheses:
        resolved = any(
            s.addresses_antithesis(antithesis)
            for s in syntheses
        )
        if not resolved:
            unresolved.append(antithesis)

    if len(unresolved) > 0:
        # Check if explicitly acknowledged
        acknowledged = [a for a in unresolved if a.acknowledged]
        if len(acknowledged) < len(unresolved):
            return ValidationResult(
                passed=False,
                action="RESOLVE_OR_ACKNOWLEDGE",
                antitheses_affected=[a for a in unresolved if not a.acknowledged]
            )

    return ValidationResult(passed=True)
```

### Parsimony Constraint

```python
def check_parsimony(theses: List[Thesis], syntheses: List[Synthesis]) -> bool:
    """
    Constraint: |S| ≤ |T|/2
    Syntheses should consolidate, not duplicate
    """
    return len(syntheses) <= len(theses) / 2
```

## G₄: Hallucination Gate

### Three-Stage Pipeline

```yaml
stage_1_citation_presence:
  method: regex_check
  pattern: '\[\^?\d+\]|\[.+?\d{4}.+?\]'
  action: Flag sentences without citation markers
  severity: CRITICAL

stage_2_semantic_entailment:
  method: embedding_similarity
  threshold: 0.75
  action: Flag claims with max_similarity < threshold
  severity: HIGH

stage_3_llm_verification:
  method: llm_as_judge
  prompt: "Does claim appear in sources?"
  action: Remove claims judged as hallucination
  severity: CRITICAL
```

### Cascade Behavior

| Stage 1 | Stage 2 | Stage 3 | Action |
|---------|---------|---------|--------|
| PASS | PASS | PASS | Include claim |
| FAIL | - | - | Remove claim |
| PASS | FAIL | - | Flag as low confidence |
| PASS | PASS | FAIL | Remove claim, log |

## G₅: Output Gate

### Word Count Compliance

```python
def check_word_count(response: str, mode: Mode) -> ValidationResult:
    word_count = count_prose_words(response)  # Excludes tables

    ranges = {
        Mode.SAQ: (180, 220),
        Mode.VIVA: (500, 800),
        Mode.ACADEMIC: (1000, 2000)
    }

    min_words, max_words = ranges[mode]

    if word_count < min_words:
        return ValidationResult(
            passed=False,
            action="EXPAND",
            current=word_count,
            target=min_words
        )
    elif word_count > max_words:
        return ValidationResult(
            passed=False,
            action="COMPRESS",
            current=word_count,
            target=max_words
        )

    return ValidationResult(passed=True)
```

### Final Confidence Calculation

```python
def calculate_confidence(
    sources: List[Source],
    textbook_coverage: float,
    synthesis_parsimony: float,
    citation_density: float,
    hallucination_pass_rate: float
) -> float:

    source_authority = weighted_mean([s.authority for s in sources])

    confidence = (
        0.30 * source_authority +
        0.25 * textbook_coverage +
        0.20 * synthesis_parsimony +
        0.15 * citation_density +
        0.10 * hallucination_pass_rate
    )

    # Apply penalties
    if len(sources) < 3:
        confidence -= 0.15  # Single source penalty
    if degraded_mode:
        confidence -= 0.10

    return max(0.0, min(1.0, confidence))
```

### Confidence Thresholds

| Confidence | Tier | Action |
|------------|------|--------|
| ≥ 0.85 | HIGH | Emit response |
| 0.70-0.84 | MEDIUM | Emit with warning |
| 0.50-0.69 | LOW | Load references/, retry Δ |
| < 0.50 | CRITICAL | Execute scripts/, escalate to user |

## Recovery Protocols

### G₁ Recovery: Source Expansion

```python
if not gate_1_passed:
    # Expand search
    expanded_query = broaden_query(original_query)

    # Try alternative sources
    if Σₜ.failed:
        Σₐ.priority = HIGH
    if Σₐ.failed:
        Σₜ.priority = HIGH

    # Retry with expansion
    sources = extract_with_expansion(expanded_query)
```

### G₄ Recovery: Hallucination Removal

```python
if not gate_4_passed:
    # Remove flagged claims
    clean_response = remove_hallucinations(response, flagged_claims)

    # Regenerate if too much removed
    if word_count(clean_response) < min_words:
        response = regenerate_with_constraints(
            must_include=[c for c in claims if c.verified],
            must_cite=[s for s in sources if s.authority > 0.8]
        )
```

### G₅ Recovery: Format Adjustment

```python
if not gate_5_passed:
    if action == "EXPAND":
        response = add_clinical_examples(response)
        response = add_mechanism_detail(response)
    elif action == "COMPRESS":
        response = remove_redundancy(response)
        response = convert_prose_to_bullets(response)
```
