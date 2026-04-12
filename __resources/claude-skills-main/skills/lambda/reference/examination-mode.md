# Examination Mode Reference

Comprehensive guide to λ-skill examination constraints for CICM/ANZCA Primary.

## Mode Detection

| Trigger | Mode | η Target | Route |
|---------|------|----------|-------|
| "SAQ", "short answer", "written" | SAQ | 2.0-2.5 | R1 |
| "viva", "oral", "examiner" | Viva | 3.0-4.0 | R2 |
| "explain briefly" | Quick | 1.5-2.0 | R0-R1 |
| "comprehensive", "detailed" | Deep | 4.0+ | R2-R3 |

## SAQ Mode

### Constraints

```yaml
word_limit: 150-250
paragraphs: 1-3
format: prose_only
η_target: [2.0, 2.5]
route: R1
time: 10 minutes writing
```

### Structure Pattern

```
¶1: Primary concept (definition + mechanism)
¶2: Secondary concept (or elaboration)
¶3: Clinical relevance (if space permits)
```

### Density Management

SAQ requires **selective density**—fewer nodes, well-connected:

```python
def saq_optimize(concepts, word_limit=200):
    # Select highest-yield concepts
    core = select_by_mark_weight(concepts, n=5)

    # Ensure interconnection
    edges = generate_edges(core, min_per_node=2)

    # Validate density
    η = len(edges) / len(core)
    assert 2.0 <= η <= 2.5, f"η={η} outside SAQ range"

    return format_prose(core, edges, word_limit)
```

### Mark Allocation Heuristic

| Marks | Words | Core Concepts | η |
|-------|-------|---------------|---|
| 5 | ~100 | 3-4 | 2.0 |
| 10 | ~200 | 5-6 | 2.25 |
| 15 | ~300 | 7-8 | 2.5 |
| 20 | ~400 | 9-10 | 2.5 |

### Common SAQ Patterns

| Question Type | Structure |
|---------------|-----------|
| "Describe factors..." | Categorise → List → Explain top 3 |
| "Compare and contrast..." | Table mental model → Prose synthesis |
| "Outline the mechanism..." | Trigger → Pathway → Effect |
| "What are the effects of..." | System-by-system OR dose-dependent |
| "Classify..." | Framework → Categories → Examples |

## Viva Mode

### Constraints

```yaml
response_time: 30-60 seconds per answer
format: verbal (prose)
η_target: [3.0, 4.0]
route: R2
style: progressive_disclosure
follow_ups: anticipate 2-3 levels
```

### Progressive Disclosure Pattern

```
Level 0 (Opening): Core definition + primary mechanism
         ↓ "Tell me more about..."
Level 1 (Expand): Secondary mechanisms + properties
         ↓ "What about complications?"
Level 2 (Depth): Complications + management
         ↓ "How does this compare to..."
Level 3 (Mastery): Comparisons + edge cases
```

### Viva Response Structure

**30-Second Template:**
```
[Drug/Concept] is a [class] that [primary action].
It works by [mechanism], resulting in [effects].
Clinically, this is relevant because [application].
```

**60-Second Expansion:**
```
[30-second core]
The [secondary property] means [implication].
Compared to [alternative], it differs in [key distinction].
Important considerations include [safety/monitoring].
```

### Anticipating Follow-ups

| Your Statement | Likely Follow-up |
|----------------|------------------|
| "causes hypotension" | "How would you manage that?" |
| "is metabolised hepatically" | "What about in liver failure?" |
| "has a narrow therapeutic index" | "How do you monitor?" |
| "is contraindicated in..." | "What would you use instead?" |

### Recovery Strategies

| Situation | Strategy |
|-----------|----------|
| Don't know | "I'm not certain, but my understanding is..." |
| Wrong direction | "Let me reconsider—the key point is..." |
| Too brief | "To expand on that..." |
| Too detailed | "In summary, the main point is..." |

## Style Constraints (Φ)

### Prose Primacy

```
❌ Avoid:
- Bullet points
- Numbered lists
- Tables (in response)

✓ Use:
- Complete sentences
- Flowing paragraphs
- Transitional phrases
```

### Teleology First

```
❌ "Propofol binds to GABA-A receptors..."
✓ "Propofol produces hypnosis by enhancing GABA-A activity..."
```

Start with **what it achieves**, then explain **how**.

### Mechanistic Chains

```
Trigger → Pathway → Effect → Clinical Relevance

Example:
Hypoxia → HIF activation → EPO transcription →
Erythropoiesis → Improved O₂ carrying capacity
```

## Validation Checklist

### Pre-Submit (SAQ)

```
□ Word count within limit
□ η ∈ [2.0, 2.5]
□ Prose format (no bullets)
□ Core concepts addressed
□ Mark allocation covered
```

### Pre-Speak (Viva)

```
□ Opening prepared (30s)
□ 2-3 expansion levels ready
□ Comparisons anticipated
□ Complications known
□ Recovery phrases ready
```

## Integration with λ Pipeline

```haskell
λ_exam :: ExamMode -> Query -> Response
λ_exam mode q =
  let constraints = case mode of
        SAQ  -> (η ∈ [2,2.5], R1, prose, ~200 words)
        Viva -> (η ∈ [3,4], R2, progressive, 30-60s)

      τ = emit ∘ validate(constraints) ∘
          compose ∘ execute ∘ route ∘ parse $ q
  in τ
```

## Quick Reference Card

```
┌─────────────────────────────────────────────┐
│ SAQ: η=2.25  R1  prose  ~200w  10min       │
│ Viva: η=3.5  R2  progressive  30-60s       │
├─────────────────────────────────────────────┤
│ Φ: Teleology → Mechanism → Clinical        │
│ KROG: Knowable, Rights, Obligations, Gov   │
├─────────────────────────────────────────────┤
│ SAQ structure: ¶1=core ¶2=expand ¶3=clinic │
│ Viva flow: open→expand→complicate→compare  │
└─────────────────────────────────────────────┘
```

---

See also:
- [examples/saq-cardio.md](../examples/saq-cardio.md)
- [examples/viva-pharmacology.md](../examples/viva-pharmacology.md)
- [templates/exam.md](../templates/exam.md)
