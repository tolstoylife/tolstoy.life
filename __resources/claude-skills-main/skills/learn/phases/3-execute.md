---
name: "3-execute"
description: "Perform the work, generate artifacts."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[2-route](phases/2-route.md)"
  λ.out: "[4-assess](phases/4-assess.md)"
  λ.kin: "[execute op](operations/execute.md), [tools](integration/tools.md)"
  τ.goal: "termination guarantee"
---

# Phase 3: Execute

> pipeline → results — Run selected pipeline with appropriate tools.

## Input

Pipeline from [2-route](phases/2-route.md), components from [1-parse](phases/1-parse.md).

## Output

Raw results from execution.

## Pipeline Implementations

### R0: Direct
```python
return knowledge_base.lookup(query)
```

### R1: Single Skill
```python
return selected_skill.process(query)
```

### R2: Composition
```python
results = parallel_execute([skill_a, skill_b], query)
return merge(results)
```

### R3: Full Orchestration
```python
plan = strategize(query)
for step in plan:
    results.append(execute_step(step))
return synthesize(results)
```

## Tool Invocation

Tools invoked based on pipeline needs:
- [../integration/tools](integration/tools.md) — Available MCP tools
- [../integration/skills](integration/skills.md) — Composable skills

## Next

→ [4-assess](phases/4-assess.md) — Evaluate results


## See Also

- [../concepts/topology-invariants](concepts/topology-invariants.md)
- [../concepts/vertex-sharing](concepts/vertex-sharing.md)

## Graph

**λ.in** (requires): [2-route](phases/2-route.md)
**λ.out** (enables): [4-assess](phases/4-assess.md)
**λ.kin** (related): [execute op](operations/execute.md), [tools](integration/tools.md)
**τ.goal**: termination guarantee
