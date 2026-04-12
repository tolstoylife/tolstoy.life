---
name: law5-external-docs
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: (ARCHITECTURE|IMPLEMENTATION|API_REFERENCE|SPECIFICATION)\.md$
---

**LAW 5 Violation: External Documentation Detected**

You're creating external documentation that WILL DRIFT from code.

**The Seven Laws state:** "∀d ∈ AuthoritativeDoc. d ⊂ Codebase"

**Better alternatives:**
- **Types (T1):** Express data shapes as TypeScript interfaces
- **Schemas (T2):** Use Pydantic/Zod for validation documentation
- **Generated specs (T3):** Use OpenAPI auto-generation from code
- **TODOs (T7):** Express plans as in-code TODOs

**If this is intentional:** Add to `.claude/hookify.law5-external-docs.local.md` and set `enabled: false`
