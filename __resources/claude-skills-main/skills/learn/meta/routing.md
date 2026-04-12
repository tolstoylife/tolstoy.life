---
name: "routing"
description: "Complexity-based pipeline selection."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[governance](meta/governance.md)"
  λ.out: "[2-route](phases/2-route.md)"
  λ.kin: "[orchestrator](integration/orchestrator.md)"
  τ.goal: "coverage"
---

# Routing

> complexity → pipeline

## Complexity Scoring

```python
complexity = (
    domains * 2 +      # Multi-domain: 0-4
    depth * 3 +        # Reasoning depth: 0-6
    stakes * 1.5 +     # Consequences: 0-3
    novelty * 2        # New territory: 0-4
)
# Range: 0-17
```

## Pipeline Selection

| Score | Pipeline | Description |
|-------|----------|-------------|
| < 2 | R0 | Direct lookup |
| < 4 | R1 | Single skill |
| < 8 | R2 | Composition |
| ≥ 8 | R3 | Full orchestration |

## Escalation Triggers

Auto-escalate to R3 if query contains:
- "current", "latest", "2025" → Needs verification
- "verify", "confirm" → Explicit check
- Multiple domains mentioned → Complex integration

## Pipeline Characteristics

| Pipeline | Tools | Skills | Iterations |
|----------|-------|--------|------------|
| R0 | 0 | 0 | 1 |
| R1 | 0-2 | 1 | 1-2 |
| R2 | 2-5 | 2-3 | 2-3 |
| R3 | 5+ | 3+ | 3-5 |

## De-escalation

If intermediate results are sufficient:
```python
if quality_score >= threshold and iteration > 0:
    return early  # Don't over-process
```


## See Also

- [../concepts/path-optimization](concepts/path-optimization.md)
- [../concepts/pareto-governance](concepts/pareto-governance.md)
- [../concepts/convergence](concepts/convergence.md)
- [../concepts/scale-invariance](concepts/scale-invariance.md)
- [../phases/2-route](phases/2-route.md)
- [../phases/1-parse](phases/1-parse.md)
- [../operations/route](operations/route.md)
- [../integration/patterns](integration/patterns.md)
- [governance](meta/governance.md)

## Graph

**λ.in** (requires): [governance](meta/governance.md)
**λ.out** (enables): [2-route](phases/2-route.md)
**λ.kin** (related): [orchestrator](integration/orchestrator.md)
**τ.goal**: coverage
