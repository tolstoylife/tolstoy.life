# Synthesis Protocol

## Hegelian Abductive Synthesis

### Phase 1: Thesis Clustering

```
FOR each unique topic_aspect:
    cluster = {T_i | T_i.claim_type = aspect AND T_i.topic = topic}

    IF |cluster| >= 3:
        consensus_check(cluster)
    ELSE:
        flag_sparse_evidence(cluster)
```

### Phase 2: Consensus Detection

```python
def consensus_check(cluster: list[Thesis]) -> ConsensusResult:
    """
    Identify consensus claims requiring ≥80% source agreement.
    """
    claim_variants = extract_claim_variants(cluster)

    for variant in claim_variants:
        supporters = [t for t in cluster if semantically_similar(t.claim, variant)]
        agreement_rate = len(supporters) / len(cluster)

        if agreement_rate >= 0.80:
            yield ConsensusResult(
                claim=variant,
                type="consensus",
                supporting_sources=[t.source for t in supporters],
                confidence=mean([t.confidence for t in supporters])
            )
        elif agreement_rate >= 0.40:
            yield ConsensusResult(
                claim=variant,
                type="contested",
                supporting_sources=[t.source for t in supporters],
                opposing_sources=[t.source for t in cluster if t not in supporters],
                resolution_required=True
            )
```

### Phase 3: Tension Resolution

**Resolution Hierarchy:**

1. **Authority**: Higher source quality wins
   - Examiner reports > Textbooks > Reviews > Primary research > Web

2. **Recency**: More recent evidence wins
   - Edition year comparison
   - Research publication date

3. **Specificity**: More specific claim wins
   - "Re < 2000 in smooth circular pipes" > "Re < 2000"

4. **Consensus**: More sources wins
   - Simple majority when other factors equal

```python
def resolve_tension(antithesis: Antithesis) -> Resolution:
    t1, t2 = antithesis.thesis_1, antithesis.thesis_2

    # Authority check
    if source_quality(t1) - source_quality(t2) > 0.15:
        return Resolution(winner=t1, method="authority")

    # Recency check
    if publication_year(t1) - publication_year(t2) > 3:
        return Resolution(winner=t1, method="recency")

    # Specificity check
    if specificity_score(t1) > specificity_score(t2):
        return Resolution(winner=t1, method="specificity")

    # Consensus check
    if len(antithesis.t1_supporters) > len(antithesis.t2_supporters):
        return Resolution(winner=t1, method="consensus")

    # Unresolved: both valid in different contexts
    return Resolution(
        winner=None,
        method="context_dependent",
        synthesis=f"Both valid: {t1.context} vs {t2.context}"
    )
```

### Phase 4: Principle Composition

**Parsimony Constraint:**
```
|S| ≤ min(|⋃T_i|/2, 10)
```

The synthesis must be SMALLER than the input theses.

**Coverage Constraint:**
```
∀T_i. ∃s ∈ S. subsumes(s, T_i)
```

Every input thesis must be subsumed by at least one synthesis principle.

**Composition Logic:**
```python
def compose_synthesis(consensus: list, resolved: list, unique: list) -> Synthesis:
    principles = []

    # Layer 1: Universal (from consensus)
    for c in consensus:
        principles.append(Principle(
            id=f"S_{len(principles)+1:02d}",
            claim=c.claim,
            type="universal",
            sources=c.supporting_sources,
            confidence=c.confidence
        ))

    # Layer 2: Conditional (from resolved tensions)
    for r in resolved:
        if r.method == "context_dependent":
            principles.append(Principle(
                id=f"S_{len(principles)+1:02d}",
                claim=r.synthesis,
                type="conditional",
                sources=r.all_sources,
                conditions=r.context_conditions,
                confidence=0.75  # Reduced for conditional
            ))
        else:
            # Winner incorporated, loser acknowledged
            principles.append(Principle(
                id=f"S_{len(principles)+1:02d}",
                claim=r.winner.claim,
                type="resolved",
                sources=[r.winner.source],
                caveat=f"cf. {r.loser.source} for alternative",
                confidence=r.winner.confidence * 0.9
            ))

    # Layer 3: Extensions (from unique high-confidence)
    for u in unique:
        if u.confidence > 0.80:
            principles.append(Principle(
                id=f"S_{len(principles)+1:02d}",
                claim=u.claim,
                type="extension",
                sources=[u.source],
                confidence=u.confidence * 0.85  # Reduced for single-source
            ))

    # Validate parsimony
    if len(principles) > 10:
        principles = prioritize_and_trim(principles, max_count=10)

    return Synthesis(principles=principles)
```

### Phase 5: Validation

```python
def validate_synthesis(S: Synthesis, theses: list[Thesis]) -> ValidationResult:
    # Coverage check
    uncovered = []
    for t in theses:
        if not any(subsumes(s, t) for s in S.principles):
            uncovered.append(t)

    if uncovered:
        return ValidationResult(
            valid=False,
            issue="COVERAGE_FAILURE",
            uncovered=uncovered,
            remediation="Add principles or broaden existing"
        )

    # Parsimony check
    if len(S.principles) > len(theses) / 2:
        return ValidationResult(
            valid=False,
            issue="PARSIMONY_FAILURE",
            current=len(S.principles),
            target=len(theses) // 2,
            remediation="Consolidate principles"
        )

    # Confidence floor
    low_conf = [p for p in S.principles if p.confidence < 0.60]
    if low_conf:
        return ValidationResult(
            valid=False,
            issue="CONFIDENCE_FAILURE",
            low_confidence=low_conf,
            remediation="Strengthen evidence or demote to caveat"
        )

    return ValidationResult(valid=True)
```

## Quick Reference

```
SYNTHESIS = f(consensus ∪ resolved ∪ extensions)

WHERE:
  consensus  = claims with ≥80% source agreement
  resolved   = tensions adjudicated by hierarchy
  extensions = unique claims with >80% confidence

SUBJECT TO:
  |S| ≤ min(|T|/2, 10)           # Parsimony
  ∀T. ∃s ∈ S. subsumes(s, T)     # Coverage
  ∀s ∈ S. confidence(s) ≥ 0.60   # Quality floor
```
