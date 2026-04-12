---
name: "topology-invariants"
description: "Graph quality constraints: η≥4, isolation<20% - delegates to shared operation."
metadata:
  ο.class: "continuant"
  ο.mode: "independent"
  λ.in: ""
  λ.out: "[governance](../meta/governance.md)"
  λ.kin: "[metagraph](metagraph.md), [Κ-monotonicity](knowledge-monotonicity.md)"
  τ.goal: "η≥4, isolation<20%"
---

# Topology Invariants

> Structural constraints: η ≥ 4, isolation < 20%, small-world properties.

## Delegated Invariant

This concept delegates to the **shared topology operation** to eliminate redundancy between learn and lambda-skill.

**See**: [`~/.claude/skills/shared/topology.md`](../../shared/topology.md)

The shared topology operation provides the complete implementation of:
- Entropy validation: `η ≥ 4` (minimum 4 bits)
- Shannon entropy calculation: `H = -Σ(p * log2(p))`
- Graph metrics: density, clustering, diameter, isolation
- Remediation strategies for violations

## Core Metrics

| Metric | Symbol | Constraint | Meaning |
|--------|--------|------------|---------|
| Edge density | η | ≥ 4.0 | Rich connectivity |
| Isolation | φ | < 0.2 | No orphan nodes |
| Clustering | κ | > 0.3 | Small-world property |
| Diameter | δ | < log(n) | Short paths |

## Graph

**lambda.out** (enables): [governance](../meta/governance.md)
**lambda.kin** (related): [metagraph](metagraph.md), [metasuperhypergraph](metasuperhypergraph.md), [K-monotonicity](knowledge-monotonicity.md), [shared topology](../../shared/topology.md)
**tau.goal**: eta>=4, isolation<20%
