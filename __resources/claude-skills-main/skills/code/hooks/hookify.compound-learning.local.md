---
name: compound-learning
enabled: true
event: stop
action: warn
pattern: .*
---

**Compound Engineering: Crystallize Before Stopping**

Before ending this session, check if learnings should be compounded:

**Trigger Detection:**
| Signal | Pattern | Action |
|--------|---------|--------|
| Confirmation | "that worked", "fixed" | Extract solution |
| Insight | "the key is", "realized" | Extract principle |
| Prevention | "next time", "avoid" | Extract guard |
| Connection | "relates to", "similar" | Extract vertex |

**If learnings detected, crystallize:**

```yaml
# Learning artifact schema
date: YYYY-MM-DD
trigger: "what initiated learning"
domain: "coding|architecture|debugging|..."
symptom: "observable problem"
root_cause: "fundamental cause (not surface)"
solution: "what worked"
why_works: "mechanistic explanation"
prevention: "how to avoid in future"
vertices:
  - "[[shared concept 1]]"
  - "[[shared concept 2]]"
confidence: 0.85
```

**Validation before adding to K:**
- [ ] Has >=2 shared vertices with existing knowledge
- [ ] Root cause is fundamental (not surface symptom)
- [ ] Solution is generalizable (not one-off)
- [ ] Prevention is actionable

**Core principle:** K' = K ∪ crystallize(assess(τ))
