---
name: knowledge-monotonicity
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.(md|txt|rst)$
  - field: new_text
    operator: regex_match
    pattern: (DELETE|REMOVE|OBSOLETE|DEPRECATED).*learning|knowledge|pattern
---

**Knowledge Monotonicity Violation**

Detected attempt to remove knowledge. K grows monotonically.

**The compound principle states:**
```haskell
compound :: Knowledge -> Response -> Knowledge
compound K τ = K ∪ crystallize(assess(τ))
-- K NEVER shrinks; only grows or refines
```

**Instead of deleting:**

1. **Supersede**: Mark as superseded by newer knowledge
   ```yaml
   status: superseded
   superseded_by: "[[newer-pattern]]"
   reason: "More accurate understanding"
   ```

2. **Refine**: Update with more precise understanding
   ```yaml
   refinement:
     previous: "old understanding"
     current: "refined understanding"
     evidence: "what changed our understanding"
   ```

3. **Contextualize**: Limit scope rather than delete
   ```yaml
   scope:
     valid_for: ["specific-context"]
     not_valid_for: ["general-case"]
   ```

**Anti-patterns (NEVER):**
- Deleting learnings because they seem wrong
- Removing patterns without replacement
- Losing historical context
