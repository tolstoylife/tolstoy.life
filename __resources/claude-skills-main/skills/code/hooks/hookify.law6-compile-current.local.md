---
name: law6-compile-current
enabled: true
event: bash
action: warn
pattern: git\s+merge|git\s+rebase|npm\s+run\s+build
---

**LAW 6 Check: Documentation = Compilation**

Verify executable documentation is current before proceeding:

```bash
# TypeScript types
npm run typecheck

# Python types
mypy .

# Schemas
npm run validate:schemas

# Linting (T5)
npm run lint
```

**The Seven Laws state:** "compiles(d) ∨ validates(d) ⟹ current(d)"

If compilation fails, documentation is stale. Fix before proceeding.
