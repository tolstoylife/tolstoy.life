---
name: orm-query-optimizer
description: Optimize ORM queries to eliminate N+1 problems, unnecessary joins, and inefficient patterns. Supports SQLAlchemy, Django ORM, Prisma, TypeORM, and ActiveRecord.
---

# ORM Query Optimizer

Fix slow ORM queries and eliminate common anti-patterns.

## When to Use

- Database queries are slow
- Suspect N+1 query problem
- ORM generates inefficient SQL
- Need to add proper eager loading or query optimization

## Common Problems

- **N+1 queries** — Lazy loading in a loop
- **Over-fetching** — SELECT * when you need 2 columns
- **Missing indexes** — Full table scans on filtered columns
- **Cartesian products** — Multiple eager loads creating cross joins
- **Unnecessary joins** — Subquery would be faster

## Workflow

1. **Identify slow query** — Enable query logging, find the bottleneck
2. **Show generated SQL** — Display what the ORM actually sends to the database
3. **Analyze** — EXPLAIN the query, identify missing indexes or bad plans
4. **Optimize** — Rewrite using proper eager loading, select_related, includes, etc.
5. **Verify** — Compare query count and execution time before/after
