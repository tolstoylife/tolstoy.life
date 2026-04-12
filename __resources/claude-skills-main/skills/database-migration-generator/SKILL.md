---
name: database-migration-generator
description: Generate safe database migration scripts. Handles schema changes, data migrations, rollbacks, and zero-downtime patterns for PostgreSQL, MySQL, and SQLite using common ORMs.
---

# Database Migration Generator

Generate safe, reversible database migrations.

## When to Use

- Adding/modifying tables, columns, or indexes
- Need zero-downtime schema changes in production
- Data migration between schema versions
- Setting up migration tooling for a project (Alembic, Knex, Prisma, etc.)

## Workflow

1. **Understand change** — What schema change is needed and why
2. **Assess risk** — Table size, lock implications, data loss potential
3. **Generate migration** — Forward and rollback scripts
4. **Zero-downtime pattern** — For production: expand-contract, backfill, then cleanup
5. **Test** — Verify on copy of production data

## Safety Rules

- NEVER drop columns/tables without explicit user confirmation
- Always generate rollback (down) migration
- Large table ALTER: use pt-online-schema-change or pg_repack patterns
- Add columns as nullable first, backfill, then add NOT NULL
- Create indexes CONCURRENTLY on PostgreSQL
- Test migrations against production-size data
