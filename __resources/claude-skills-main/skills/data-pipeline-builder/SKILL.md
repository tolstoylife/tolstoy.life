---
name: data-pipeline-builder
description: Design data pipelines for ETL/ELT workflows. Build extraction, transformation, and loading stages with error handling, retries, and monitoring for batch and streaming scenarios.
---

# Data Pipeline Builder

Design robust data pipelines for batch and streaming workloads.

## When to Use

- Moving data between systems (DB → warehouse, API → DB)
- Building batch processing jobs
- Setting up streaming data ingestion
- Need error handling and retry logic for data flows

## Patterns

| Pattern | Best For | Tools |
|---------|----------|-------|
| Batch ETL | Daily/hourly imports | Python scripts, Airflow, cron |
| Streaming | Real-time events | Kafka, Redis Streams, SSE |
| CDC | DB replication | Debezium, pg_logical |
| API Polling | External data sync | Scheduled HTTP + upsert |

## Workflow

1. **Map data flow** — Source → transformations → destination
2. **Choose pattern** — Batch vs streaming based on latency needs
3. **Handle failures** — Retries, dead letter queue, idempotent writes
4. **Monitor** — Lag, throughput, error rate, data freshness
5. **Test** — Schema validation, data quality checks, edge cases
