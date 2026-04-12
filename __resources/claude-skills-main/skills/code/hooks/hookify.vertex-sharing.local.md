---
name: vertex-sharing-check
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: learnings?/.*\.md$|patterns?/.*\.md$
  - field: new_text
    operator: not_contains
    pattern: "vertices:"
---

**Vertex Sharing Required**

New learning/pattern detected without vertex connections.

**Integration requirement:**
```haskell
integrate :: Learning -> Knowledge -> Knowledge
integrate l K =
  let shared = vertices(l) ∩ concepts(K)
  in case shared of
       []  -> K ∪ bridge(l, analogical_map(l, K))  -- Create bridge
       _   -> K ∪ link(l, shared)                   -- Direct merge
```

**Add vertices section:**
```yaml
vertices:
  - "[[concept-1]]"  # Must exist in knowledge base
  - "[[concept-2]]"  # At least 2 shared vertices required
related:
  - "[[similar-learning]]"
```

**Why this matters:**
- Orphan learnings cannot be retrieved
- Vertex-sharing enables compound growth (η ≥ 4)
- Connected knowledge compounds; isolated knowledge decays

**Quick check:**
```bash
# Find concepts in existing knowledge base
grep -rh "^\s*-.*\[\[" ~/.claude/skills/learn/concepts/ | sort -u
```
