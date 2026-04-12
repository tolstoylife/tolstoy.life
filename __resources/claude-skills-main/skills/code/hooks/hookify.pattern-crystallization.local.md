---
name: pattern-crystallization
enabled: true
event: bash
action: warn
pattern: git\s+commit.*-m.*fix|solve|resolve|implement
---

**Compound Engineering: Pattern Crystallization Opportunity**

Commit message indicates resolution. Consider crystallizing the pattern.

**Crystallization checklist:**

1. **Was this a novel solution?**
   - If solving for first time -> crystallize
   - If applying known pattern -> link to existing

2. **Is it generalizable?**
   - Works in multiple contexts -> crystallize
   - One-off fix -> document inline only

3. **Extraction template:**
```yaml
# ~/.claude/learnings/YYYY-MM-DD-brief-title.md
date: YYYY-MM-DD
trigger: "commit: <commit-message>"
domain: "coding"
symptom: "what was broken"
root_cause: "fundamental cause"
solution: "what fixed it"
why_works: "mechanism"
prevention: "how to avoid"
vertices:
  - "[[error-handling]]"
  - "[[async-patterns]]"
confidence: 0.80
```

4. **Integration:**
```bash
# Add to knowledge base
cp learning.md ~/.claude/learnings/
# Link to related patterns
grep -l "similar-concept" ~/.claude/learnings/
```

**Core insight:** Every fix is a learning; every learning compounds.
