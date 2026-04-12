---
name: "metagraph"
description: "Graphs of graphs for hierarchical representation."
metadata:
  ο.class: "continuant"
  ο.mode: "dependent"
  λ.in: "[scale-invariance](concepts/scale-invariance.md)"
  λ.out: "[homoiconicity](concepts/homoiconicity.md)"
  λ.kin: "[topology](concepts/topology-invariants.md)"
  τ.goal: "multi-scale representation"
---

# Metagraph

> Graph of graphs—hierarchical structure where nodes are themselves graphs.

## Definition

A metagraph has nodes that are themselves graphs:

```
G_meta = (V_meta, E_meta) where each v ∈ V_meta is a graph
```

## Properties

1. **Hierarchical**: Can nest arbitrarily deep
2. **Scale-invariant**: Same operations at every level
3. **Compositional**: Combine graphs via meta-edges

## Learn Skill as Metagraph

```
Level 0: Entire skill (1 graph)
Level 1: Domains (7 subgraphs)
Level 2: Files (45 nodes per domain)
Level 3: Sections within files
```

## Operations

```python
def lift(op, G_meta):
    "Apply operation to all subgraphs."
    return {v: op(v) for v in G_meta.nodes}

def project(G_meta, level):
    "Flatten to specific level."
    return merge([project(v, level-1) for v in G_meta.nodes])
```

## Graph

**lambda.in** (requires): [scale-invariance](scale-invariance.md)
**lambda.out** (enables): [homoiconicity](homoiconicity.md), [metasuperhypergraph](metasuperhypergraph.md)
**lambda.kin** (related): [topology](topology-invariants.md)
**tau.goal**: multi-scale representation
