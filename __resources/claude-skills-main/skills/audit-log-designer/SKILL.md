---
name: audit-log-designer
description: Design audit logging systems for compliance and debugging. Capture who did what, when, and to what with immutable, queryable audit trails.
---

# Audit Log Designer

Build audit trails for compliance and debugging.

## When to Use

- Compliance requirements (SOC2, HIPAA, GDPR)
- Need to track who changed what and when
- Building admin activity dashboards
- Debugging "who deleted this record?"

## Workflow

1. **Define events** — What actions need auditing? (CRUD, auth, config changes)
2. **Design schema** — actor, action, resource, timestamp, before/after values
3. **Implement capture** — Middleware, database triggers, or application events
4. **Ensure immutability** — Append-only table, no UPDATE/DELETE on audit log
5. **Enable querying** — Indexes on actor, resource, timestamp, action type
6. **Retention** — Archival policy, cold storage for old logs

## Schema Pattern

```sql
CREATE TABLE audit_log (
  id BIGSERIAL PRIMARY KEY,
  actor_id UUID NOT NULL,
  action VARCHAR(50) NOT NULL,
  resource_type VARCHAR(50) NOT NULL,
  resource_id VARCHAR(255) NOT NULL,
  changes JSONB,
  metadata JSONB,
  ip_address INET,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```
