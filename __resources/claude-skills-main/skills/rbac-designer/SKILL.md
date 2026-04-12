---
name: rbac-designer
description: Design role-based access control systems. Define roles, permissions, and policies for multi-tenant applications. Covers RBAC, ABAC, and ReBAC patterns with database schema designs.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - WebFetch
  - WebSearch
---

# RBAC Designer

Design access control systems for applications.

## When to Use

- Building user roles and permissions for a new app
- Adding multi-tenant access control
- Migrating from simple role checks to fine-grained permissions
- Designing admin/user/viewer role hierarchies

## Models

| Model | Complexity | Best For |
|-------|-----------|----------|
| RBAC | Low | Fixed roles (admin, editor, viewer) |
| ABAC | Medium | Attribute-based (dept, location, time) |
| ReBAC | High | Relationship-based (owner, member, shared) |

## Workflow

1. **Identify resources** — What entities need protection?
2. **Define actions** — CRUD + custom actions per resource
3. **Design roles** — Role hierarchy with permission inheritance
4. **Schema** — Users ↔ Roles ↔ Permissions tables
5. **Enforce** — Middleware/decorator pattern for authorization checks
6. **Audit** — Log all access decisions for compliance

## Best Practices

- Deny by default, explicitly grant
- Check permissions, not roles (roles can change)
- Cache permission lookups (they're checked on every request)
- Separate authentication (who) from authorization (what)
