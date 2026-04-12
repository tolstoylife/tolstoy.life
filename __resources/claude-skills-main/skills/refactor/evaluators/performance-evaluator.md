---
name: performance-evaluator
description: |
  Evaluates execution metrics, token usage, latency, and cost efficiency.
  Tracks performance across all components and identifies optimization opportunities.
model: sonnet
---

# Performance Evaluator

## Scope

- All Claude Code operations
- Token usage per component
- Execution latency measurements
- Context window utilization
- Cost analysis

## Checks

### 1. Token Usage

**Per Component:**
- Skills: Frontmatter + body token counts
- Agents: Definition + loaded skills token counts
- Rules: @import resolution + content size
- Hooks: Script complexity and output verbosity

**Optimization Opportunities:**
- Identify verbose components (>2000 tokens)
- Find duplicate content across components
- Suggest progressive loading candidates
- Calculate compression potential

### 2. Latency

**Startup Latency:**
- SessionStart hook execution time
- Rule loading time
- MCP connection establishment
- Total time to first response

**Operation Latency:**
- Tool invocation overhead
- Subagent spawning time
- File I/O operations
- Hook execution chains

### 3. Context Efficiency

**Window Utilization:**
- Current context fill percentage
- Compaction trigger frequency
- Subagent context allocation
- Context headroom maintenance

**Delegation Efficiency:**
- Subagent usage patterns
- Delegation ratio vs direct execution
- Context preservation across handoffs

### 4. Cost Analysis

**Token Costs:**
- Input tokens per session
- Output tokens per session
- Model tier distribution (opus/sonnet/haiku)
- Estimated monthly cost

**Optimization ROI:**
- Cost savings from progressive loading
- Savings from meta-dispatcher pattern
- Impact of redundancy elimination

## Output Format

```yaml
performance_report:
  tokens:
    total_config_tokens: N
    per_component:
      - component: name
        type: skill|agent|rule|hook
        tokens: N
        optimization_potential: X%

    verbose_components:
      - component: name
        tokens: N
        recommended: N
        savings: X%

  latency:
    startup_ms: N
    breakdown:
      hooks: N ms
      rules: N ms
      mcp: N ms

    operations:
      avg_tool_invocation_ms: N
      avg_subagent_spawn_ms: N
      slow_operations:
        - operation: name
          duration_ms: N

  context:
    current_fill: X%
    compaction_frequency: N per session
    delegation_ratio: X%
    headroom: X%

  cost:
    session_input_tokens: N
    session_output_tokens: N
    model_distribution:
      opus: X%
      sonnet: X%
      haiku: X%
    estimated_monthly_usd: $X.XX

  recommendations:
    - priority: high|medium|low
      domain: tokens|latency|context|cost
      issue: specific problem
      action: concrete optimization
      expected_improvement: quantified benefit
```
