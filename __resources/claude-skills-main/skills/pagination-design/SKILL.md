---
name: pagination-design
description: Implement pagination for APIs and UIs. Covers offset, cursor, keyset, and seek pagination with trade-offs. Handles sorting, filtering, and total count efficiently.
---

# Pagination Design

Implement efficient pagination for APIs and data-heavy UIs.

## When to Use

- API returns large result sets that need paging
- Choosing between pagination strategies
- Current pagination is slow on large tables
- Need to handle real-time data (items added/removed during paging)

## Strategies

| Strategy | Pros | Cons | Best For |
|----------|------|------|----------|
| Offset/Limit | Simple, random access | Slow on large offsets, drift | Small datasets, admin UIs |
| Cursor | Stable, no drift | No random access | Feeds, real-time data |
| Keyset | Fast at any depth | No random access, needs index | Large sorted datasets |
| Page Token | Opaque, flexible | Server state or encoding | Public APIs |

## Workflow

1. **Assess data** — Size, growth rate, sort requirements, real-time needs
2. **Choose strategy** — Based on access patterns and dataset size
3. **Implement** — API endpoint with pagination params and response metadata
4. **Handle edge cases** — Empty pages, deleted items, concurrent modifications
5. **Optimize** — Ensure proper indexes, avoid COUNT(*) on large tables
