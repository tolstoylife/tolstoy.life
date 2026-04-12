---
name: rate-limiter-design
description: Design and implement rate limiting for APIs. Covers token bucket, sliding window, and fixed window algorithms with Redis, in-memory, and distributed implementations.
---

# Rate Limiter Design

Design and implement rate limiting for APIs and services.

## When to Use

- API needs protection from abuse or overload
- Implementing per-user or per-IP rate limits
- Choosing between rate limiting algorithms
- Setting up distributed rate limiting with Redis

## Algorithms

| Algorithm | Pros | Cons | Best For |
|-----------|------|------|----------|
| Token Bucket | Smooth, allows bursts | Memory per key | API rate limiting |
| Sliding Window | Accurate, no boundary spikes | More complex | Strict rate enforcement |
| Fixed Window | Simple, low memory | Boundary spike problem | Simple use cases |
| Leaky Bucket | Smooth output rate | No burst allowance | Queue processing |

## Workflow

1. **Define limits** — Requests per second/minute/hour, per user/IP/API key
2. **Choose algorithm** — Based on burst tolerance and accuracy needs
3. **Choose storage** — In-memory (single server), Redis (distributed), DB (persistent)
4. **Implement** — Middleware with proper headers (X-RateLimit-Limit, Remaining, Reset)
5. **Handle exceeded** — 429 status, Retry-After header, clear error message
