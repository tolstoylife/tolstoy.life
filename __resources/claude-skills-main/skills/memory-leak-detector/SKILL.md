---
name: memory-leak-detector
description: Detect and fix memory leaks in applications. Analyze heap snapshots, identify retained objects, find unclosed resources, and fix common leak patterns in Python, JavaScript, and Go.
---

# Memory Leak Detector

Find and fix memory leaks in applications.

## When to Use

- Application memory usage grows over time
- OOM kills in production
- Need to analyze heap dumps or memory profiles
- Suspect resource leaks (file handles, connections, event listeners)

## Common Leak Patterns

- **JavaScript**: Detached DOM nodes, closures capturing large scopes, forgotten timers/intervals, event listener accumulation
- **Python**: Circular references with __del__, global caches without eviction, threading.local() accumulation
- **Go**: Goroutine leaks, forgotten context cancellation, unbounded channel buffers

## Workflow

1. **Reproduce** — Identify the operation that causes growth
2. **Instrument** — Add memory tracking (process.memoryUsage, tracemalloc, runtime.MemStats)
3. **Snapshot** — Take before/after heap snapshots
4. **Diff** — Compare snapshots to find growing object types
5. **Trace** — Find the allocation site and retention path
6. **Fix** — Apply fix and verify memory stabilizes
