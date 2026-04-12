---
name: law1-e2e-deploy
enabled: true
event: bash
action: warn
pattern: npm\s+run\s+deploy|git\s+push.*prod|deploy.*prod
---

**LAW 1 Check: E2E Verification Required**

**Before deploying to production:**

1. Run E2E tests: `npm run test:e2e` or `pytest tests/e2e/`
2. Verify all critical paths pass
3. Check observability (LAW 2): logs and traces configured

**The Seven Laws state:** "∀f ∈ Features. deployed(f) ⟹ e2e_verified(f)"

**Trust hierarchy:**
- E2E tests: 0.90
- Unit tests: 0.30 (insufficient alone)
