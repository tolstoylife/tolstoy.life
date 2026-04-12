---
name: docker-compose-builder
description: Generate and optimize docker-compose.yml files. Handles multi-service setups, networking, volumes, health checks, and environment configuration with best practices.
---

# Docker Compose Builder

Generate production-ready docker-compose.yml configurations.

## When to Use

- Setting up a multi-service development environment
- Adding services (databases, caches, queues) to existing compose files
- Optimizing compose files for production vs development
- Debugging networking or volume issues between containers

## Workflow

1. **Identify services** — What the app needs (web, db, cache, worker, etc.)
2. **Generate compose** — Write docker-compose.yml with proper structure
3. **Configure networking** — Service discovery, exposed ports, internal networks
4. **Set up volumes** — Named volumes for persistence, bind mounts for dev
5. **Add health checks** — Proper startup ordering with depends_on + healthcheck
6. **Environment** — Use env_file references, never inline secrets

## Best Practices

- Use specific image tags, never `latest` in production
- Set resource limits (mem_limit, cpus)
- Use multi-stage builds referenced via build context
- Separate dev and prod with docker-compose.override.yml
- Always include restart policies
