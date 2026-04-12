# Examination Templates

Constrained τ patterns for CICM/ANZCA Primary.

## Quick Navigation

| Resource | Purpose |
|----------|---------|
| [reference/examination-mode.md](../reference/examination-mode.md) | Comprehensive exam mode guide |
| [examples/saq-cardio.md](../examples/saq-cardio.md) | Full SAQ worked example |
| [examples/viva-pharmacology.md](../examples/viva-pharmacology.md) | Full viva worked example |

## SAQ Mode

### Constraints

| Parameter | Value |
|-----------|-------|
| Words | ~200 (8-min handwritten) |
| Nodes | ≤15 |
| η | 2.0-2.5 |
| Route | R1 forced |
| Format | Prose only |
| Headers | None |
| Bullets | None |

### Structure

```
[Definition: 1-2 sentences, precise]

[Mechanism: Core pathway, A → B → C]

[Clinical relevance: Application or implication]

(A diagram showing X would be appropriate)  [if applicable]
```

### Mark Allocation Pattern

| Component | Marks | Focus |
|-----------|-------|-------|
| Definition | 20-30% | Precision, completeness |
| Mechanism | 40-50% | Causal chain, quantitative |
| Clinical | 20-30% | Application, relevance |

### Example: Propofol Hypotension SAQ

> Propofol produces hypotension primarily through reduction in systemic vascular resistance (SVR), with a smaller contribution from decreased myocardial contractility. The drug potentiates GABA-A receptors centrally, reducing sympathetic nervous system outflow. This leads to decreased noradrenaline release at vascular smooth muscle, causing both arterial vasodilation and venodilation. The resulting drop in SVR is the dominant mechanism. Direct myocardial depression occurs through calcium channel effects but is usually modest in healthy patients. Blood pressure typically falls 15-40% post-induction, with heart rate relatively unchanged or slightly increased reflexly. Factors increasing susceptibility include hypovolaemia, advanced age, and pre-existing cardiac dysfunction. Mitigation strategies include slow injection, co-induction with opioids, and ensuring adequate preload.

**Word count**: 120 | **η**: ~2.3 | **Nodes**: 12

### Question Type Patterns

| Type | Focus | Example |
|------|-------|---------|
| "Describe the mechanism..." | Causal chain emphasis | 50% mechanism, 30% clinical |
| "What factors affect..." | Enumeration with explanation | List factors, explain each |
| "Compare X and Y" | Structured comparison | State dimension, compare both |
| "Outline the management..." | Sequential steps | Priorities, rationale |

### Examiner Patterns

From accumulated K:
- Expect **contextualization** (why it matters)
- Expect **comparison** (not isolated facts)
- Penalize pure regurgitation
- Reward mechanistic understanding
- Reward quantitative precision ("15-40%", "~1 MAC")

## Viva Mode

### Constraints

| Parameter | Value |
|-----------|-------|
| Duration | ~10 minutes |
| Nodes | ≤30 |
| η | 3.0-4.0 |
| Route | R2 forced |
| Format | Progressive disclosure |

### Time Structure

| Phase | Time | Focus |
|-------|------|-------|
| Opening | 30s | Crisp definition |
| First layer | 2min | Core mechanism |
| Second layer | 3min | Depth/complexity |
| Extensions | 3min | Breadth/variations |
| Clinical | 2min | Application |

### Opening Card Template

```
TOPIC: [X]

DEFINITION (30s):
[Precise, examinable definition]

FIRST PROMPT LIKELY:
"Tell me about X" or "What is X?"

KEY POINTS TO HIT:
1. [Essential concept 1]
2. [Essential concept 2]
3. [Essential concept 3]
```

### Depth Card Template

```
TOPIC: [X] - DEPTH

MECHANISM:
[A → B → C → D]

QUANTITATIVE:
- [Parameter 1]: [Value/range]
- [Parameter 2]: [Value/range]

ANTICIPATE:
- "What happens if..." → [Response]
- "Why is that..." → [Response]
- "What about..." → [Response]
```

### Example: Propofol Viva

**Opening (30s)**:
> "Propofol is an intravenous anaesthetic agent that acts primarily on GABA-A receptors to produce rapid onset, short-duration anaesthesia with a favourable recovery profile."

**First layer (2min)**:
> "Its cardiovascular effects are characterized by hypotension, predominantly from SVR reduction through central sympatholysis and direct vascular smooth muscle relaxation. The mechanism involves GABA-A potentiation centrally, reducing sympathetic outflow, plus direct effects on vascular calcium channels..."

**Anticipated follow-ups**:
- "How does this compare to thiopentone?" → Both reduce SVR, thiopentone more tachycardia
- "What about the myocardial effects?" → Direct depression via calcium handling, usually modest
- "In a patient with aortic stenosis?" → High risk, need slow titration, maintain preload

### Common Traps

| Trap | Avoidance |
|------|-----------|
| Going too deep too fast | Layered disclosure |
| Missing the obvious | Start with definition |
| Saying "I don't know" | Bridge to related knowledge |
| Arguing with examiner | Accept cue, redirect |

## Detection Triggers

| Trigger | Mode | Override |
|---------|------|----------|
| "SAQ" | SAQ | Force R1, ~200 words |
| "Short answer" | SAQ | Force R1, ~200 words |
| "Viva" | Viva | Force R2, progressive |
| "Oral" | Viva | Force R2, progressive |
| None | Normal | Per routing |

## Validation

### SAQ Checklist
- [ ] ~200 words (±20%)
- [ ] No headers
- [ ] No bullets
- [ ] Definition present
- [ ] Mechanism with causation
- [ ] Clinical relevance
- [ ] η ∈ [2.0, 2.5]

### Viva Checklist
- [ ] Opening ≤30s readable
- [ ] Progressive structure
- [ ] Anticipated follow-ups included
- [ ] Quantitative where appropriate
- [ ] η ∈ [3.0, 4.0]
