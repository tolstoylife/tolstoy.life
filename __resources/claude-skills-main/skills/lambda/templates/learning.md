# Learning Crystallization Template

Schema for compounding knowledge: K → K'

## Trigger Detection

Crystallize when these patterns detected:

| Signal | Example |
|--------|---------|
| Resolution | "that worked", "fixed", "correct" |
| Insight | "I see", "the key is", "realized" |
| Prevention | "next time", "to avoid", "watch for" |
| Connection | "this is like", "relates to", "similar" |

## Full Schema

```yaml
---
# Metadata
id: "λ-YYYYMMDD-NNN"
date: 2026-01-07
source: "conversation|document|experience"
confidence: 0.85  # 0.0-1.0

# Classification
domain: "physiology|pharmacology|physics|reasoning|examination|meta"
category: "mechanism|pattern|error|insight|bridge"
tags:
  - "tag1"
  - "tag2"

# Content
trigger: "What initiated the learning"
symptom: "Observable problem or question"
investigation: "What was tried, what didn't work"
root_cause: "Fundamental cause (not surface symptom)"
solution: "What worked"
why_works: "Mechanistic explanation (A → B → C)"
prevention: "How to avoid recurrence"

# Integration
vertices:
  - "[[shared concept 1]]"
  - "[[shared concept 2]]"
related:
  - "[[similar learning]]"
supersedes: "[[older learning if this replaces it]]"

# Validation
validated: true
η_contribution: 0.2  # How much this adds to graph density
---
```

## Minimal Schema (Quick Capture)

```yaml
---
date: 2026-01-07
domain: physiology
trigger: "Understanding propofol hypotension"
insight: "SVR reduction dominates over cardiac depression"
vertices: ["[[propofol]]", "[[SVR]]", "[[GABA-A]]"]
confidence: 0.8
---
```

## Content Template

```markdown
# [Descriptive Title]

## Symptom
[What was the question/problem?]

## Investigation
[What was tried? What didn't work?]

## Root Cause
[Fundamental reason - not surface symptom]

## Solution
[What resolved it - generalizable pattern]

## Why It Works
[Mechanistic explanation]
A → B → C → resolution

## Prevention
[How to avoid this class of problem in future]

## Related
- [[Similar pattern 1]]
- [[Related concept]]
```

## Examples

### Type: Mechanism Learning

```yaml
---
date: 2026-01-07
domain: pharmacology
category: mechanism
trigger: "Asked about propofol cardiovascular effects"
symptom: "Needed to explain hypotension mechanism"
root_cause: "SVR reduction dominates, cardiac depression secondary"
solution: "Explain via sympathetic inhibition → vascular relaxation pathway"
why_works: "GABA-A → central sympatholysis → ↓noradrenaline → vasodilation"
prevention: "Always distinguish primary (SVR) from secondary (cardiac) effects"
vertices: ["[[propofol]]", "[[SVR]]", "[[GABA-A]]", "[[sympathetic]]"]
confidence: 0.85
---
```

### Type: Error Prevention

```yaml
---
date: 2026-01-07
domain: reasoning
category: error
trigger: "Gave surface explanation, examiner probed deeper"
symptom: "Answer lacked mechanistic depth"
root_cause: "Started with WHAT instead of WHY"
solution: "Apply teleology-first structure"
why_works: "Why → How → What mirrors examiner's expectation"
prevention: "Check: Does answer start with purpose/teleology?"
vertices: ["[[teleology]]", "[[examination]]", "[[mechanism]]"]
confidence: 0.9
---
```

### Type: Bridge Connection

```yaml
---
date: 2026-01-07
domain: physiology
category: bridge
trigger: "Noticed analogy between lung and kidney"
insight: "Fick principle applies to both: Flow = Clearance = (C_in - C_out) × Q"
vertices: ["[[Fick principle]]", "[[renal clearance]]", "[[pulmonary VO2]]"]
confidence: 0.95
---
```

## Validation Checklist

Before adding to K:

- [ ] Root cause is fundamental (not symptom restated)
- [ ] Solution is generalizable (not one-off fix)
- [ ] ≥2 vertices shared with existing K
- [ ] Confidence is calibrated (not overconfident)
- [ ] Why_works includes causal chain (→)
- [ ] Prevention is actionable

## Storage Location

```
learnings/
├── [domain]/
│   ├── mechanisms/
│   ├── patterns/
│   ├── errors/
│   ├── insights/
│   └── bridges/
└── meta/  # Learnings about learning
```

## Decay and Relevance

```python
# Recent learnings weighted higher
decay(l) = 0.95 ** days_since(l.date)

# But high-confidence resists decay
effective_weight(l) = l.confidence + (1 - l.confidence) * decay(l)

# Relevance to query
relevance(l, query) = similarity(l.vertices, query.concepts) * effective_weight(l)
```

## Self-Application

This template itself can be crystallized:

```yaml
---
date: 2026-01-07
domain: meta
category: pattern
trigger: "Designing λ skill compound mechanism"
insight: "Structured schema enables queryable knowledge"
vertices: ["[[compound engineering]]", "[[knowledge crystallization]]", "[[λ]]"]
confidence: 0.9
---
```
