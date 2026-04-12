---
name: cache-strategy
description: Design caching strategies for applications. Choose between cache-aside, write-through, write-behind patterns. Handle invalidation, TTLs, and cache stampede prevention with Redis or in-memory caches.
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

# Cache Strategy

Design effective caching for applications.

## When to Use

- Application has slow database queries or API calls
- Need to choose a caching layer (Redis, Memcached, in-memory)
- Cache invalidation is causing stale data issues
- High traffic causing cache stampedes

## Patterns

| Pattern | How | Best For |
|---------|-----|----------|
| Cache-Aside | App checks cache, falls back to DB | Read-heavy, tolerates staleness |
| Write-Through | Write to cache and DB together | Consistency critical |
| Write-Behind | Write to cache, async flush to DB | Write-heavy, can tolerate lag |
| Read-Through | Cache fetches from DB on miss | Simplifies app code |

## Workflow

1. **Identify hotspot** — What data is accessed frequently and expensive to compute?
2. **Choose pattern** — Based on read/write ratio and consistency needs
3. **Set TTL** — Balance freshness vs hit rate
4. **Handle invalidation** — Event-based, TTL-based, or versioned keys
5. **Prevent stampede** — Mutex/lock, stale-while-revalidate, pre-warming

## Key Decisions

- Cache key design (namespaced, versioned, deterministic)
- Serialization format (JSON, msgpack, protobuf)
- Eviction policy (LRU, LFU, TTL)
- Monitoring (hit rate, miss rate, eviction rate)
