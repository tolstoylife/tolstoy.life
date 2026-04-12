---
name: law7-required-todos
enabled: true
event: bash
action: warn
pattern: git\s+commit|git\s+push
---

**LAW 7 Check: TODO Plans**

Before committing, verify required TODOs are resolved:

```bash
grep -rn "TODO(.*required" --include="*.py" --include="*.ts" --include="*.js" src/
```

**The Seven Laws state:** "∀plan ∈ Plans. expressed_as_todos(plan) ∧ in_code(plan)"

Required TODOs (`TODO(id,required)`) block merge. Complete them or remove the `required` flag.
