## Architectural Patterns

### Pattern 1: Supervisor/Orchestrator

The supervisor pattern places a central agent in control, delegating to specialists and synthesizing results. The supervisor maintains global state and trajectory, decomposes user objectives into subtasks, and routes to appropriate workers.

```
User Request -> Supervisor -> [Specialist A, Specialist B, Specialist C] -> Aggregation -> Final Output
```

**When to use:** Complex tasks with clear decomposition, tasks requiring coordination across domains, tasks where human oversight is important.

**Advantages:** Strict control over workflow, easier to implement human-in-the-loop interventions, ensures adherence to predefined plans.

**Disadvantages:** Supervisor context becomes bottleneck, supervisor failures cascade to all workers, "telephone game" problem where supervisors paraphrase sub-agent responses incorrectly.

**Claude Code Implementation:** Create a main command that orchestrates by calling specialized subagents using the Task tool. The supervisor command contains the coordination logic and calls subagents for specialized work.

```markdown
<!-- Example supervisor command structure -->
1. Analyze the user request and decompose into subtasks
2. For each subtask, dispatch to appropriate specialist:
   - Use Task tool to spawn subagent with focused context
   - Pass only relevant context to each subagent
3. Collect and synthesize results from all subagents
4. Return unified response to user
```

**The Telephone Game Problem:** Supervisor architectures can perform worse when supervisors paraphrase sub-agent responses incorrectly, losing fidelity. The fix: allow sub-agents to pass responses directly when synthesis would lose important details. In Claude Code, this means letting subagents write directly to shared files or return their output verbatim rather than having the supervisor rewrite everything.

### Pattern 2: Peer-to-Peer/Swarm

The peer-to-peer pattern removes central control, allowing agents to communicate directly based on predefined protocols. Any agent can transfer control to any other through explicit handoff mechanisms.

**When to use:** Tasks requiring flexible exploration, tasks where rigid planning is counterproductive, tasks with emergent requirements that defy upfront decomposition.

**Advantages:** No single point of failure, scales effectively for breadth-first exploration, enables emergent problem-solving behaviors.

**Disadvantages:** Coordination complexity increases with agent count, risk of divergence without central state keeper, requires robust convergence constraints.

**Claude Code Implementation:** Create commands that can invoke other commands based on discovered needs. Use shared files (like task lists or state files) as the coordination mechanism.

```markdown
<!-- Example peer handoff structure -->
1. Analyze current state from shared context file
2. Determine if this agent can complete the task
3. If specialized help needed:
   - Write current findings to shared state
   - Invoke appropriate peer command/skill
4. Continue until task complete or hand off
```

### Pattern 3: Hierarchical

Hierarchical structures organize agents into layers of abstraction: strategic, planning, and execution layers. Strategy layer agents define goals and constraints; planning layer agents break goals into actionable plans; execution layer agents perform atomic tasks.

```
Strategy Layer (Goal Definition) -> Planning Layer (Task Decomposition) -> Execution Layer (Atomic Tasks)
```

**When to use:** Large-scale projects with clear hierarchical structure, enterprise workflows with management layers, tasks requiring both high-level planning and detailed execution.

**Advantages:** Mirrors organizational structures, clear separation of concerns, enables different context structures at different levels.

**Disadvantages:** Coordination overhead between layers, potential for misalignment between strategy and execution, complex error propagation.

**Claude Code Implementation:** Structure your plugin with commands at different abstraction levels. High-level commands focus on strategy and call mid-level planning commands, which in turn call atomic execution commands.

## Context Isolation as Design Principle

The primary purpose of multi-agent architectures is context isolation. Each sub-agent operates in a clean context window focused on its subtask without carrying accumulated context from other subtasks.

### Isolation Mechanisms

**Instruction passing:** For simple, well-defined subtasks, the coordinator creates focused instructions. The sub-agent receives only the instructions needed for its specific task. In Claude Code, this means passing minimal, targeted prompts to subagents via the Task tool.

**File system memory:** For complex tasks requiring shared state, agents read and write to persistent storage. The file system serves as the coordination mechanism, avoiding context bloat from shared state passing. This is the most natural pattern for Claude Code—agents communicate through markdown files, JSON state files, or structured documents.

**Full context delegation:** For complex tasks where the sub-agent needs complete understanding, the coordinator shares its entire context. The sub-agent has its own tools and instructions but receives full context for its decisions. Use sparingly as it defeats the purpose of context isolation.

### Isolation Trade-offs

Full context delegation provides maximum capability but defeats the purpose of sub-agents. Instruction passing maintains isolation but limits sub-agent flexibility. File system memory enables shared state without context passing but introduces consistency challenges.

The right choice depends on task complexity, coordination needs, and the nature of the work.

## Consensus and Coordination

### The Voting Problem

Simple majority voting treats hallucinations from weak reasoning as equal to sound reasoning. Without intervention, multi-agent discussions can devolve into consensus on false premises due to inherent bias toward agreement.

### Weighted Contributions

Weight agent contributions by confidence or expertise. Agents with higher confidence or domain expertise carry more weight in final decisions.

### Debate Protocols

Debate protocols require agents to critique each other's outputs over multiple rounds. Adversarial critique often yields higher accuracy on complex reasoning than collaborative consensus.

**Claude Code Implementation:** Create a review stage where one agent critiques another's output. Structure this as separate commands: one for initial work, one for critique, and optionally one for revision based on critique.

### Trigger-Based Intervention

Monitor multi-agent interactions for specific behavioral markers:
- **Stall triggers:** Activate when discussions make no progress
- **Sycophancy triggers:** Detect when agents mimic each other's answers without unique reasoning
- **Divergence triggers:** Detect when agents are moving away from the original objective

## Failure Modes and Mitigations

### Failure: Supervisor Bottleneck

The supervisor accumulates context from all workers, becoming susceptible to saturation and degradation.

**Mitigation:** Implement output constraints so workers return only distilled summaries. Use file-based checkpointing to persist state without carrying full history in context.

### Failure: Coordination Overhead

Agent communication consumes tokens and introduces latency. Complex coordination can negate parallelization benefits.

**Mitigation:** Minimize communication through clear handoff protocols. Use structured file formats for inter-agent communication. Batch results where possible.

### Failure: Divergence

Agents pursuing different goals without central coordination can drift from intended objectives.

**Mitigation:** Define clear objective boundaries for each agent. Implement convergence checks that verify progress toward shared goals. Use iteration limits on agent execution.

### Failure: Error Propagation

Errors in one agent's output propagate to downstream agents that consume that output.

**Mitigation:** Validate agent outputs before passing to consumers. Implement retry logic. Design for graceful degradation when components fail.

## Applying Patterns in Claude Code

### Command as Supervisor

Create a main command that:
1. Analyzes the task and creates a plan
2. Dispatches subagents via Task tool for specialized work
3. Collects results (via return values or shared files)
4. Synthesizes final output

### Subagents as Specialists

Define Subagents for specialized domains:
- Each Subagents focuses on one area of expertise
- Subagents receive focused context relevant to their specialty
- Subagents return structured outputs that coordinators can aggregate

### Files as Shared Memory

Use the file system for inter-agent coordination:
- State files track progress across agents
- Output files collect results from parallel work
- Task lists coordinate remaining work

### Example: Code Review Multi-Agent

```
Supervisor Command: review-code
├── Subagent: security-review (security specialist)
├── Subagent: performance-review (performance specialist)
├── Subagent: style-review (style/conventions specialist)
└── Aggregation: combine findings, deduplicate, prioritize
```

Each subagent receives only the code to review and their specialty focus. The supervisor aggregates all findings into a unified review.

## Guidelines

1. Design for context isolation as the primary benefit of multi-agent systems
2. Choose architecture pattern based on coordination needs, not organizational metaphor
3. Use file-based communication as the default for Claude Code multi-agent patterns
4. Implement explicit handoff protocols with clear state passing
5. Use critique/debate patterns for consensus rather than simple agreement
6. Monitor for supervisor bottlenecks and implement checkpointing via files
7. Validate outputs before passing between agents
8. Set iteration limits to prevent infinite loops
9. Test failure scenarios explicitly
10. Start simple—add multi-agent complexity only when single-agent approaches fail

## Memory and State Management

For tasks spanning multiple sessions or requiring persistent state, use file-based memory:

### Working Memory

The context window itself. Provides immediate access but vanishes when sessions end. Keep only active information; summarize completed work.

### Session Memory

Files created during a session that track progress:
- Task lists (what's done, what remains)
- Intermediate results
- Decision logs

### Long-Term Memory

Persistent files that survive across sessions:
- CLAUDE.md for project-level context
- Memory files in designated directories
- Structured knowledge bases in markdown or JSON

### Memory Patterns for Multi-Agent

- **Handoff files:** Agent A writes state, Agent B reads and continues
- **Result aggregation:** Multiple agents write to separate files, supervisor reads all
- **Progress tracking:** Shared task list updated by all agents
- **Knowledge accumulation:** Agents append findings to shared knowledge files

Choose the simplest memory mechanism that meets your needs. File-based memory is transparent, debuggable, and requires no infrastructure.
