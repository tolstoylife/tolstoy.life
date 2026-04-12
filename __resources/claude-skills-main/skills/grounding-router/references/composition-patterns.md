# Composition Patterns — Emergent Behaviors

## Pattern Library

### Pattern 1: Sequential Refinement Pipeline

```
Composition: Σₚ ∘ Σₗ ∘ Σₜ ∘ Σₐ ∘ Δ ∘ Ρ

Flow:
  Personal → Local → Textbook → Authoritative → Synthesis → Response

Emergent Behavior:
  - Personal context seeds search terms
  - Local templates constrain textbook scope
  - Textbook claims validated by authoritative sources
  - Each stage refines the next
```

**Use When**: Deep, thorough grounding required; time not critical

### Pattern 2: Parallel Saturation

```
Composition: (Σₚ ⊗ Σₗ ⊗ Σₜ ⊗ Σₐ) ∘ Δ ∘ Ρ

Flow:
  [Personal | Local | Textbook | Authoritative] → Synthesis → Response

Emergent Behavior:
  - All sources extracted simultaneously
  - Faster execution (parallel)
  - Richer conflict detection in Δ
  - May surface unexpected connections
```

**Use When**: Speed required; comprehensive coverage needed

### Pattern 3: Recursive Deepening

```
Composition: Σ* ∘ Τ* ∘ Δ* ∘ Ρ

Flow:
  Extract(until saturation) → Ground(until coverage) → Synthesize(until resolved) → Respond

Emergent Behavior:
  - Each primitive runs until convergence
  - Σ* expands search on each iteration
  - Τ* finds additional textbook support
  - Δ* resolves deeper antitheses
  - Produces most comprehensive output
```

**Use When**: Academic mode; complex controversial topics

### Pattern 4: Conditional Bypass

```
Composition: (Σ | cache) ∘ (Τ | not_cached) ∘ Δ ∘ Ρ

Flow:
  if cached: Skip source extraction
  if not cached: Full textbook grounding
  Always: Synthesize and respond

Emergent Behavior:
  - Caching dramatically speeds repeat queries
  - Maintains quality through conditional textbook check
  - Adapts to user's session history
```

**Use When**: Repeat queries; time-sensitive responses

### Pattern 5: Conflict-Triggered Expansion

```
Composition: (Σ ∘ Τ ∘ Δ) ⊗ ((Σ ⊗ Τ)* | has_antithesis) ∘ Ρ

Flow:
  Standard pipeline in parallel with:
    If antithesis detected → Recursive source expansion

Emergent Behavior:
  - Normal queries complete quickly
  - Conflicts trigger deeper investigation
  - Automatic escalation without user intervention
```

**Use When**: Unknown topic complexity; adaptive thoroughness

### Pattern 6: Multimodal-Augmented

```
Composition: (Σₛ ⊗ Σₐ) ∘ (Σₜ | has_textbook_match) ∘ Δ ∘ Ρ

Flow:
  [Screen Recordings | Authoritative] → Conditional Textbook → Synthesis → Response

Emergent Behavior:
  - Screen recordings provide experiential context
  - Authoritative sources validate recording claims
  - Textbook grounding if gaps detected
  - Multimodal insights enriched by video/transcript analysis
```

**Use When**: User has recorded related teaching sessions; demos provide context

**CLI Implementation:**
```bash
# Parallel extraction
screenapp files search "{topic}" --semantic --limit 5 --json &
research pex-grounding -t "{topic}" --format json &
wait

# Conditional textbook
pdf-search "{topic}" --limit 10 --tags {specialty}

# Optional: AI insights from top recording
screenapp ask {fileId} "{question}" --mode transcript --json
```

---

## Scenario-Specific Compositions

### Medical SAQ: Pharmacology

```yaml
composition: (Σₜ ⊗ Σₐ) ∘ Δ ∘ Ρₛ
rationale: Textbook + guidelines; personal context less relevant for facts
primitives:
  Σₜ: pdf-search with --tags pharmacology
  Σₐ: research pex-grounding
  Δ: Standard Hegelian
  Ρₛ: SAQ template with drug table
```

### Medical SAQ: Clinical Management

```yaml
composition: Σₐ ∘ (Σₜ | mechanism_needed) ∘ Δ ∘ Ρₛ
rationale: Guidelines primary; textbook only if mechanism required
primitives:
  Σₐ: research pex-grounding with --specialty
  Σₜ: Conditional textbook for mechanisms
  Δ: Emphasis on clinical synthesis
  Ρₛ: SAQ template with management steps
```

### Medical VIVA: Complex Topic

```yaml
composition: Σ* ∘ (Τ ⊗ Δ*) ∘ Ρᵥ*
rationale: Full saturation for examiner depth
primitives:
  Σ*: Recursive all sources until saturation
  Τ ⊗ Δ*: Parallel grounding with recursive synthesis
  Ρᵥ*: Expand until examiner probes exhausted
```

### Quick Fact Check

```yaml
composition: Σₐ ∘ Τᵥ ∘ Ρₛ
rationale: Single authoritative check with verification
primitives:
  Σₐ: research fact-check
  Τᵥ: Verify against textbook
  Ρₛ: Minimal SAQ response
```

---

## Composition Algebra

### Identity Laws

```
Σ ∘ id = Σ          (Right identity)
id ∘ Σ = Σ          (Left identity)
```

### Associativity

```
(Σ ∘ Τ) ∘ Δ = Σ ∘ (Τ ∘ Δ)
```

### Distributivity

```
(Σ ⊗ Τ) ∘ Δ = (Σ ∘ Δ) ⊗ (Τ ∘ Δ)    (Parallel distributes over sequential)
```

### Conditional Collapse

```
(Σ | true) = Σ
(Σ | false) = id
```

### Recursive Fixpoint

```
Σ* = Σ ∘ (Σ* | not_converged) ∪ id | converged
```

---

## Emergent Behavior Catalog

| Composition | Emergent Behavior | Discovery Context |
|-------------|-------------------|-------------------|
| `Σₚ ∘ Σₜ` | Personal trajectory guides textbook search | User learning patterns affect results |
| `Σₜ ⊗ Σₐ` | Cross-validation of textbook vs current | Detects outdated textbook info |
| `Δ* ∘ Ρᵥ` | Recursive synthesis produces examiner probes | Probes emerge from unresolved antitheses |
| `(Τ ⊗ Δ) \| conflict` | On-demand deepening | Resource efficiency |
| `Ρ*` | Response expands with examples | Each iteration adds clinical vignettes |
| `Σₗ ∘ Σₜ` | Template-guided textbook search | Prior SAQs constrain search scope |

---

## Anti-Patterns

### Infinite Recursion

```
BAD: Σ* with no convergence check
FIX: Σ* with depth_limit=5 OR saturation_threshold=0.9
```

### Parallel Explosion

```
BAD: (Σ* ⊗ Τ* ⊗ Δ*) — All recursive in parallel
FIX: Σ* ∘ (Τ ⊗ Δ)* — Sequential saturation, then parallel
```

### Condition Race

```
BAD: (Σ | a) ⊗ (Σ | !a) — Mutually exclusive conditions in parallel
FIX: (Σ | a) ∘ (Σ | !a) — Sequential with condition evaluation
```

### Grounding Skip

```
BAD: Σ ∘ Ρ — Direct response without grounding
FIX: Σ ∘ Τ ∘ Ρ — Always include textbook primitive
```
