---
name: "orchestrator"
description: "Workflow coordination."
metadata:
  ο.class: "occurrent"
  ο.mode: "dependent"
  λ.in: "[skills](integration/skills.md), [patterns](integration/patterns.md)"
  λ.out: ""
  λ.kin: "[routing](meta/routing.md)"
  τ.goal: "deadlock-free"
---

# Orchestrator

> Complex tasks → Coordinated execution

## Responsibilities

1. **Planning**: Decompose complex tasks into steps
2. **Scheduling**: Order steps respecting dependencies
3. **Execution**: Invoke skills/tools per plan
4. **Monitoring**: Track progress, detect issues
5. **Synthesis**: Combine results into coherent output

## R3 Pipeline Flow

```
ο → plan → [step₁, step₂, ..., stepₙ] → parallel/sequential → synthesize → τ
```

## State Management

```python
@dataclass
class OrchestratorState:
    plan: List[Step]
    completed: List[StepResult]
    current: Optional[Step]
    context: Dict
    
def advance(state):
    if all_complete(state):
        return synthesize(state.completed)
    state.current = next_ready(state.plan, state.completed)
    result = execute(state.current, state.context)
    state.completed.append(result)
    return advance(state)
```

## Convergence

Orchestrator terminates when:
- All planned steps complete
- Quality threshold reached
- Max iterations exceeded


## See Also

- [../concepts/convergence](concepts/convergence.md)
- [../concepts/fixed-point](concepts/fixed-point.md)
- [../concepts/topology-invariants](concepts/topology-invariants.md)
- [../phases/3-execute](phases/3-execute.md)
- [../phases/4-assess](phases/4-assess.md)
- [../meta/governance](meta/governance.md)
- [../meta/routing](meta/routing.md)
- [skills](integration/skills.md)
- [tools](integration/tools.md)

## Graph

**λ.in** (requires): [skills](integration/skills.md), [patterns](integration/patterns.md)
**λ.kin** (related): [routing](meta/routing.md)
**τ.goal**: deadlock-free
