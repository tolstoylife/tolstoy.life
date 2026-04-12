# Atomic Primitives — Full Specification

## Σ (SOURCE) — Complete Sub-Primitive Matrix

### Σₚ — Personal Context (limitless)

**λο.τ Form**: `Query(ο) → Lifelog-Search(λ) → Personal-Context(τ)`

| Sub-Attribute | Symbol | T | F | I | C | Function |
|--------------|--------|---|---|---|---|----------|
| Trajectory Extraction | Σₚ₁ | 0.8 | 0.2 | 0.3 | 0.4 | Extract learning path |
| Prior Explanation | Σₚ₂ | 0.7 | 0.3 | 0.4 | 0.3 | Retrieve past teachings |
| Temporal Context | Σₚ₃ | 0.9 | 0.1 | 0.2 | 0.2 | Date-based filtering |
| Speaker Attribution | Σₚ₄ | 0.6 | 0.4 | 0.5 | 0.5 | Who said what |

**CLI Pattern**:
```bash
limitless lifelogs search "{topic}" --limit 5 --json
limitless workflow daily {date} --json
```

**Output Schema**:
```typescript
interface PersonalContext {
  id: string;
  title: string;
  markdown: string;
  startTime: string;
  speakers: { name: string; content: string }[];
  relevance_score: number;
}
```

### Σₗ — Local Context (pieces)

**λο.τ Form**: `Query(ο) → LTM-Search(λ) → Local-Context(τ)`

| Sub-Attribute | Symbol | T | F | I | C | Function |
|--------------|--------|---|---|---|---|----------|
| LTM Retrieval | Σₗ₁ | 0.85 | 0.15 | 0.2 | 0.3 | Long-term memory |
| Template Match | Σₗ₂ | 0.9 | 0.1 | 0.1 | 0.2 | Prior SAQ patterns |
| Code History | Σₗ₃ | 0.7 | 0.3 | 0.4 | 0.4 | Implementation patterns |
| Snippet Recall | Σₗ₄ | 0.8 | 0.2 | 0.3 | 0.3 | Saved materials |

**CLI Pattern**:
```bash
echo "" | pieces ask "{topic}" --ltm
pieces search "{topic}" --mode ncs
```

**Output Schema**:
```typescript
interface LocalContext {
  title: string;
  content: string;
  source_files: string[];
  ltm_references: string[];
  confidence: number;
}
```

### Σₜ — Textbook Context (pdf-search)

**λο.τ Form**: `Query(ο) → Semantic-Search(λ) → Textbook-Chunks(τ)`

| Sub-Attribute | Symbol | T | F | I | C | Function |
|--------------|--------|---|---|---|---|----------|
| Semantic Match | Σₜ₁ | 0.95 | 0.05 | 0.1 | 0.1 | Embedding similarity |
| Tag Filtering | Σₜ₂ | 0.9 | 0.1 | 0.1 | 0.2 | Exam/topic filter |
| Page Citation | Σₜ₃ | 1.0 | 0.0 | 0.0 | 0.0 | Exact page reference |
| Chunk Ranking | Σₜ₄ | 0.85 | 0.15 | 0.2 | 0.3 | Relevance ordering |

**CLI Pattern**:
```bash
pdf-search "{topic}" --limit 10 --tags ANZCA,pharmacology
pdf-brain search "{topic}" --limit 10
```

**Output Schema**:
```typescript
interface TextbookChunk {
  document: string;
  page: number;
  content: string;
  score: number;
  tags: string[];
  citation: string;  // Formatted citation
}
```

### Σₐ — Authoritative Context (research)

**λο.τ Form**: `Query(ο) → PEX-Grounding(λ) → Authoritative-Sources(τ)`

| Sub-Attribute | Symbol | T | F | I | C | Function |
|--------------|--------|---|---|---|---|----------|
| PEX Sources | Σₐ₁ | 0.9 | 0.1 | 0.2 | 0.2 | Medical education sites |
| Guideline Match | Σₐ₂ | 0.95 | 0.05 | 0.1 | 0.1 | ACOG/NICE/WHO |
| Evidence Grade | Σₐ₃ | 0.8 | 0.2 | 0.3 | 0.4 | RCT/meta-analysis/expert |
| Citation Format | Σₐ₄ | 1.0 | 0.0 | 0.0 | 0.0 | Proper academic format |

**CLI Pattern**:
```bash
research pex-grounding -t "{topic}" --specialty {specialty} --format json
research fact-check -t "{claim}" --format json
```

**Output Schema**:
```typescript
interface AuthoritativeSource {
  title: string;
  url: string;
  content: string;
  source_type: "guideline" | "journal" | "pex" | "textbook";
  authority_score: number;
  publication_date: string;
}
```

### Σₛ — Screen Context (screenapp)

**λο.τ Form**: `Query(ο) → Multimodal-Search(λ) → Screen-Context(τ)`

| Sub-Attribute | Symbol | T | F | I | C | Function |
|--------------|--------|---|---|---|---|----------|
| Transcript Search | Σₛ₁ | 0.90 | 0.10 | 0.15 | 0.2 | Semantic transcript search |
| Visual Query | Σₛ₂ | 0.85 | 0.15 | 0.20 | 0.3 | Screenshot/video frame analysis |
| Temporal Context | Σₛ₃ | 0.80 | 0.20 | 0.25 | 0.2 | Date-based recording filter |
| AI Insights | Σₛ₄ | 0.88 | 0.12 | 0.18 | 0.3 | Multimodal AI query results |

**CLI Pattern**:
```bash
screenapp files search "{topic}" --semantic --limit 5 --json
screenapp ask {fileId} "{question}" --mode transcript --json
screenapp workflow daily {date} --json
```

**Output Schema**:
```typescript
interface ScreenContext {
  id: string;
  name: string;
  duration: number;
  transcript?: {
    text: string;
    segments: { start: number; end: number; text: string; speaker?: string }[];
  };
  topics: string[];
  speakers: string[];
  aiInsights?: string;
  relevance_score: number;
}
```

---

## Τ (TEXTBOOK) — Grounding Sub-Primitives

### Τᵥ — Verified Claims

**Rule**: Claim + Textbook Page + Author

| Verification | Weight | Requirement |
|--------------|--------|-------------|
| Direct quote | 1.0 | Exact text match |
| Paraphrase | 0.9 | Semantic similarity > 0.85 |
| Inference | 0.7 | Logical derivation documented |

### Τₑ — Evidence Claims

**Rule**: Claim + Journal/Guideline + Year

| Evidence Level | Weight | Requirement |
|----------------|--------|-------------|
| Systematic review | 0.95 | Cochrane/meta-analysis |
| RCT | 0.90 | Published controlled trial |
| Cohort | 0.80 | Observational study |
| Expert opinion | 0.65 | Guideline without RCT |

### Τₓ — Templated Claims

**Rule**: Claim matches prior validated template

| Template Match | Weight | Requirement |
|----------------|--------|-------------|
| Exact pattern | 0.85 | Identical structure |
| Variant pattern | 0.75 | Modified but validated |
| New pattern | 0.50 | Requires Τᵥ or Τₑ validation |

---

## Δ (DIALECTICAL) — Synthesis Sub-Primitives

### Δₜ — Thesis Extraction

**Algorithm**:
```python
def extract_theses(sources: List[Source]) -> List[Thesis]:
    theses = []
    for source in sources:
        for claim in extract_claims(source):
            thesis = Thesis(
                claim=claim.text,
                citation=format_citation(source),
                confidence=claim.confidence,
                claim_type=classify_claim(claim)  # definitional|mechanistic|quantitative|clinical
            )
            theses.append(thesis)
    return deduplicate(theses, threshold=0.85)
```

### Δₐ — Antithesis Detection

**Algorithm**:
```python
def detect_antitheses(theses: List[Thesis]) -> List[Antithesis]:
    antitheses = []
    for t1, t2 in combinations(theses, 2):
        if contradicts(t1, t2):
            antithesis = Antithesis(
                thesis_a=t1,
                thesis_b=t2,
                conflict_type=classify_conflict(t1, t2),  # contradiction|refinement|context-dependent
                resolution_priority=calculate_priority(t1, t2)
            )
            antitheses.append(antithesis)
    return sorted(antitheses, key=lambda a: a.resolution_priority, reverse=True)
```

### Δₛ — Synthesis Generation

**Algorithm**:
```python
def synthesize(theses: List[Thesis], antitheses: List[Antithesis]) -> List[Synthesis]:
    syntheses = []

    # Consensus claims (no antithesis)
    for thesis in theses:
        if not has_antithesis(thesis, antitheses):
            syntheses.append(Synthesis(claim=thesis.claim, type="consensus"))

    # Resolved conflicts
    for antithesis in antitheses:
        resolution = resolve_by_authority(antithesis)
        syntheses.append(Synthesis(
            claim=resolution.unified_claim,
            type="resolved",
            resolution_method=resolution.method,
            acknowledged_variation=resolution.alternative
        ))

    return syntheses
```

---

## Ρ (RESPONSE) — Output Sub-Primitives

### Ρₛ — SAQ Mode

**Constraints**:
- Word count: 180-220 (prose only, tables excluded)
- Citations: 5-10 inline
- Structure: Dot points, symbols permitted
- Tables: Max 1, encouraged for comparisons

**Template**:
```markdown
{Opening statement with key definition}

**{Category 1}**:
- {Point 1.1} [{Citation 1}]
- {Point 1.2} [{Citation 2}]

**{Category 2}**:
| {Header 1} | {Header 2} | {Header 3} |
|------------|------------|------------|
| {Data} | {Data} | {Data} [{Citation}] |

**{Closing synthesis}** [{Citation}].
```

### Ρᵥ — VIVA Mode

**Constraints**:
- Word count: 500-800
- Citations: 15-25 with deep references
- Structure: Extended prose with examiner probes
- Includes: Edge cases, clinical vignettes, anticipated questions

**Template**:
```markdown
## Core Response
{Extended explanation with mechanism depth}

## Clinical Application
{Practical scenarios with dosing/monitoring}

## Edge Cases
- {Edge case 1}: {Management}
- {Edge case 2}: {Management}

## Anticipated Examiner Questions
1. **"Why not {alternative}?"** — {Response}
2. **"What if {complication}?"** — {Response}
3. **"How does this differ from {comparison}?"** — {Response}
```

### Ρₐ — Academic Mode

**Constraints**:
- Word count: 1000-2000
- Citations: 30-50 bibliography style
- Structure: Full scholarly format
- Includes: Abstract, methodology acknowledgment, limitations

---

## Composition Operator Semantics

### Sequential (∘) — Formal Definition

```haskell
(∘) :: Primitive → Primitive → Primitive
(f ∘ g) x = f (g x)

-- Example: Σ ∘ Τ
-- First extract sources (Σ), then ground in textbooks (Τ)
```

### Parallel (⊗) — Formal Definition

```haskell
(⊗) :: Primitive → Primitive → Primitive
(f ⊗ g) x = merge (f x) (g x)

-- Example: Σₚ ⊗ Σₜ
-- Extract personal AND textbook simultaneously, merge results
```

### Recursive (*) — Formal Definition

```haskell
(*) :: Primitive → Primitive
f* x = fix (λr. f r) x
     = f (f (f ... x)) until convergence

-- Convergence criteria:
--   |output_{n} - output_{n-1}| < ε
--   depth > max_depth
--   user_patience_threshold exceeded
```

### Conditional (|) — Formal Definition

```haskell
(|) :: Primitive → Condition → Primitive
(f | c) x = if c x then Just (f x) else Nothing

-- Example: Σₚ | has_pendant
-- Only extract personal context if pendant available
```
