---
name: stop-checklist
enabled: true
event: stop
action: warn
pattern: .*
---

**Seven Laws Completion Checklist**

Before stopping, verify:

| Law | Check | Command |
|-----|-------|---------|
| **LAW 1** | E2E tests run | `npm run test:e2e` |
| **LAW 2** | Logging added | Check handlers for logger calls |
| **LAW 3** | Linting passes | `npm run lint` |
| **LAW 4** | Ready for review | Changes documented in PR |
| **LAW 5** | No external docs | Code is the documentation |
| **LAW 6** | Types compile | `npm run typecheck` |
| **LAW 7** | TODOs resolved | `grep -rn "TODO(.*required" src/` |

**Quick validation:**
```bash
python scripts/preflight.py
```
