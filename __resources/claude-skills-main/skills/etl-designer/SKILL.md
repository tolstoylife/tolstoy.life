---
name: etl-designer
description: Design ETL transformations for data warehousing. Build extraction queries, transformation logic, and loading strategies with schema mapping, data quality checks, and incremental processing.
---

# ETL Designer

Design Extract-Transform-Load workflows for data warehousing.

## When to Use

- Moving data from operational DB to analytics warehouse
- Cleaning and normalizing data from multiple sources
- Building incremental load strategies
- Designing star/snowflake schema transformations

## Workflow

1. **Extract** — Source queries, CDC, API calls, file imports
2. **Transform** — Clean, deduplicate, normalize, enrich, aggregate
3. **Load** — Full refresh vs incremental, upsert strategies
4. **Validate** — Row counts, checksums, null checks, referential integrity
5. **Schedule** — Dependency DAGs, SLA monitoring, alerting

## Key Decisions

- Full refresh vs incremental (watermark column, CDC)
- Transform in source (ELT) vs in pipeline (ETL)
- Schema evolution handling (additive only vs breaking changes)
- Idempotency — reruns produce same result
