---
name: performance-profiler
description: Profile and optimize code performance. Identify bottlenecks, suggest optimizations, analyze time/space complexity, and benchmark alternatives. Supports Python, JavaScript, Go, and Rust.
---

# Performance Profiler

Identify and fix performance bottlenecks in code.

## When to Use

- Code is slower than expected
- Need to analyze algorithmic complexity (Big-O)
- Comparing performance of alternative implementations
- Memory usage is too high
- Need to set up profiling tools for a project

## Workflow

1. **Identify hotspot** — Read code, analyze complexity, find likely bottlenecks
2. **Profile** — Set up language-appropriate profiling (cProfile, perf_hooks, pprof)
3. **Analyze** — Interpret profiling output, identify top consumers
4. **Optimize** — Suggest concrete improvements with expected impact
5. **Benchmark** — Write before/after benchmarks to verify improvements

## Optimization Checklist

- Algorithm complexity (O(n^2) → O(n log n))
- Unnecessary allocations and copies
- N+1 query patterns
- Missing caching opportunities
- Blocking I/O that could be async
- Unneeded serialization/deserialization
