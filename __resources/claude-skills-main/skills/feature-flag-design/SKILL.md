---
name: feature-flag-design
description: Design and implement feature flags for gradual rollouts, A/B testing, and kill switches. Covers flag types, targeting rules, and cleanup strategies without external dependencies.
---

# Feature Flag Design

Implement feature flags for controlled rollouts.

## When to Use

- Need gradual rollout of a new feature (1% → 10% → 100%)
- Want a kill switch for risky changes
- A/B testing different implementations
- Feature needs to be enabled per-tenant or per-user

## Flag Types

| Type | Example | Lifecycle |
|------|---------|-----------|
| Release | New checkout flow | Temporary, remove after 100% |
| Experiment | Button color A/B test | Temporary, remove after decision |
| Ops | Maintenance mode | Permanent, toggle as needed |
| Permission | Premium features | Permanent, per-plan |

## Workflow

1. **Define flag** — Name, type, default value, targeting rules
2. **Implement** — Simple if/else with flag check (start simple, no framework needed)
3. **Target** — User ID, percentage, tenant, environment
4. **Monitor** — Track flag evaluation metrics
5. **Clean up** — Remove flag and dead code path after full rollout
