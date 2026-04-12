---
name: "pareto-governance"
description: "80/20 resource allocation and trade-offs."
metadata:
  ο.class: "continuant"
  ο.mode: "independent"
  λ.in: "[governance](meta/governance.md)"
  λ.out: "[2-route](phases/2-route.md)"
  λ.kin: "[path-optimization](concepts/path-optimization.md)"
  τ.goal: "80/20 allocation"
---

# Pareto Governance

> 80/20 rule for resource allocation—focus effort on highest-impact areas.

## Principle

20% of improvements yield 80% of value:

```python
def prioritize_improvements(candidates):
    ranked = sorted(candidates, key=lambda c: c.impact, reverse=True)
    cutoff = int(len(ranked) * 0.2)
    return ranked[:cutoff]  # Focus on top 20%
```

## Application in Learn Skill

| Area | Focus | Rationale |
|------|-------|-----------|
| Phases | 1-parse, 4-assess | Highest leverage |
| Concepts | topology, homoiconicity | Core invariants |
| Operations | route, refactor | Decision points |

## Recursive Pareto

Apply Pareto at each level:
- Top 20% of domains
- Top 20% of files within domain
- Top 20% of content within file

Result: 0.2³ = 0.8% of content captures 51% of value (0.8³)

## Graph

**lambda.in** (requires): [governance](../meta/governance.md)
**lambda.out** (enables): [2-route](../phases/2-route.md), [metasuperhypergraph](metasuperhypergraph.md)
**lambda.kin** (related): [path-optimization](path-optimization.md)
**tau.goal**: 80/20 allocation
