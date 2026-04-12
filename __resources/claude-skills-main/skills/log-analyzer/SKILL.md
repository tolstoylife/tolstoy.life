---
name: log-analyzer
description: Parse, search, and analyze application logs. Extract patterns, identify errors, correlate timestamps, and summarize log files to quickly diagnose issues.
---

# Log Analyzer

Parse and analyze log files to diagnose application issues.

## When to Use

- Application throwing errors and you need to find the root cause
- Need to correlate events across multiple log files
- Want to extract metrics (error rates, response times) from logs
- Analyzing crash dumps or stack traces

## Workflow

1. **Identify format** — JSON, structured, unstructured, syslog, Apache/nginx
2. **Parse and filter** — Extract relevant entries by time range, severity, pattern
3. **Correlate** — Link related events across log files using request IDs, timestamps
4. **Summarize** — Top errors by frequency, error rate over time, first occurrence
5. **Root cause** — Trace the chain of events leading to the failure

## Capabilities

- Parse common log formats (JSON lines, Apache CLF, syslog, Docker logs)
- Time-range filtering with timezone awareness
- Group and count by error type, status code, endpoint
- Identify anomalies (sudden spike in errors, new error types)
- Extract stack traces and deduplicate them
