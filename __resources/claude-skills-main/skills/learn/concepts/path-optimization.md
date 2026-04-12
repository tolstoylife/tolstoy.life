---
name: "path-optimization"
description: "Finding optimal routes through possibility space."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[convergence](concepts/convergence.md)"
  λ.out: "[5-refactor](phases/5-refactor.md)"
  λ.kin: "[pareto](concepts/pareto-governance.md)"
  τ.goal: "minimum cost route"
---

# Path Optimization

> Finding shortest path through knowledge graph—efficient navigation from current to target state.

## Problem Statement

Given:
- Current state v₀
- Target state vₙ
- Knowledge graph G = (V, E)

Find: Path P = (v₀, v₁, ..., vₙ) minimizing total distance

## Algorithms

```python
def shortest_path(G, source, target):
    # Dijkstra for weighted graphs
    return dijkstra(G, source, target)

def semantic_path(G, source, target, embedding):
    # A* with semantic heuristic
    h = lambda v: cosine_distance(embedding(v), embedding(target))
    return astar(G, source, target, heuristic=h)
```

## Application in Routing

The route phase uses path optimization to select:
1. Which concepts to activate
2. Which operations to sequence
3. Which tools to invoke

## Graph

**λ.in** (requires): [convergence](concepts/convergence.md)
**λ.out** (enables): [5-refactor](phases/5-refactor.md)
**λ.kin** (related): [pareto](concepts/pareto-governance.md)
**τ.goal**: minimum cost route
