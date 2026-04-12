---
name: healthcheck-endpoint
description: Design health check endpoints for services. Implements liveness, readiness, and startup probes with dependency checks for databases, caches, and external APIs. Kubernetes-compatible.
---

# Health Check Endpoint

Build health check endpoints for application monitoring.

## When to Use

- Setting up Kubernetes liveness/readiness probes
- Load balancer needs a health endpoint
- Monitoring system needs to check service status
- Need to verify database/cache/external API connectivity

## Probe Types

| Probe | Purpose | Should Check |
|-------|---------|-------------|
| Liveness | Is the process alive? | App responds, no deadlock |
| Readiness | Can it serve traffic? | DB connected, cache warm, deps up |
| Startup | Has it finished initializing? | Migrations done, cache loaded |

## Workflow

1. **Identify dependencies** — DB, cache, message queue, external APIs
2. **Design probes** — Separate liveness (simple) from readiness (thorough)
3. **Implement** — GET /health, /ready, /live endpoints
4. **Add timeouts** — Each dependency check gets its own timeout
5. **Configure K8s** — Set proper initialDelaySeconds, periodSeconds, failureThreshold
