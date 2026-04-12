# Integration Patterns

## Table of Contents

1. [Skill-Backed Subagent](#pattern-1-skill-backed-subagent)
2. [Multi-Agent Pipeline](#pattern-2-multi-agent-pipeline)
3. [Supervision Gradient](#pattern-3-supervision-gradient)
4. [Tool Specialization](#pattern-4-tool-specialization)
5. [Skill Composition](#pattern-5-skill-composition)
6. [Validation Checklist](#validation-checklist)

---

## Pattern 1: Skill-Backed Subagent

Agent loads procedural knowledge via skills.

```
skill: code-analysis ──► subagent: analyst ──► command: /analyze
                              │
                         skills: [code-analysis]
```

**Skill:**
```yaml
# .claude/skills/code-analysis/SKILL.md
---
name: code-analysis
description: Static analysis procedures. Trigger when analyzing code quality.
---
```

**Subagent:**
```yaml
# .claude/agents/analyst.md
---
description: Code analyst for architecture review and technical debt.
allowed-tools: [Read, Grep, Glob, LS]
model: sonnet
skills: [code-analysis]
---
```

**Command:**
```yaml
# .claude/commands/analyze.md
---
description: Perform code analysis on target path
allowed-tools: [Agent, Read]
argument-hint: [path]
---

Launch analyst agent on specified path.
```

---

## Pattern 2: Multi-Agent Pipeline

Sequential agent stages for complex workflows.

```
command: /ship
    │
    ├─► Agent[planner] ──► Plan
    ├─► Agent[implementer] ──► Code
    ├─► Agent[reviewer] ──► Review
    └─► Agent[deployer] ──► Deploy
```

**Command:**
```yaml
# .claude/commands/ship.md
---
description: End-to-end feature shipping pipeline
allowed-tools: [Agent, Bash(git:*)]
model: opus
argument-hint: [feature]
---

## Stage 1: Planning
Spawn planner. Await implementation plan.

## Stage 2: Implementation  
Spawn implementer with plan. Await code changes.

## Stage 3: Review
Spawn reviewer. Await approval.

## Stage 4: Deploy
On approval, spawn deployer.
```

**Agents:**
```yaml
# .claude/agents/planner.md
---
description: Decomposes features into milestones. Anticipates risks.
allowed-tools: [Read, Grep]
model: opus
permissionMode: ask
---
```

```yaml
# .claude/agents/implementer.md
---
description: Implements code following conventions. Commits incrementally.
allowed-tools: [Read, Write, Edit, Bash(git:*)]
model: sonnet
permissionMode: allow
---
```

---

## Pattern 3: Supervision Gradient

Same workflow with configurable autonomy.

**Autonomous:**
```yaml
# .claude/styles/autonomous.md
---
name: autonomous
description: Full automation with logging. Minimal prompts.
keep-coding-instructions: true
---

Proceed without confirmation on standard operations.
Document all decisions. Only prompt for genuinely ambiguous situations.
```

**Supervised:**
```yaml
# .claude/styles/supervised.md
---
name: supervised
description: Checkpoint-based with human review at key decisions.
keep-coding-instructions: true
---

Present plan before implementation.
Pause at milestones for approval.
Request confirmation for external operations.
```

**Collaborative:**
```yaml
# .claude/styles/collaborative.md
---
name: collaborative
description: Step-by-step with full human involvement.
keep-coding-instructions: true
---

Explain reasoning at each step.
Present options before choosing.
Seek explicit approval for all changes.
```

---

## Pattern 4: Tool Specialization

Isolate capabilities by agent role.

```yaml
# Reader - no write access
# .claude/agents/reader.md
---
description: Read-only analyst for safe codebase exploration
allowed-tools: [Read, Grep, Glob, LS]
disallowed-tools: [Write, Edit, Bash]
permissionMode: deny
---
```

```yaml
# Writer - controlled access
# .claude/agents/writer.md
---
description: Code author with file modification capabilities
allowed-tools: [Read, Write, Edit]
disallowed-tools: [Bash]
permissionMode: ask
---
```

```yaml
# Executor - full access
# .claude/agents/executor.md
---
description: Operations agent with full system access
allowed-tools: [Read, Write, Edit, Bash(*)]
permissionMode: allow
---
```

---

## Pattern 5: Skill Composition

Agent loads multiple skills for comprehensive expertise.

```yaml
# .claude/agents/fullstack.md
---
description: Full-stack developer proficient across domains
allowed-tools: [Read, Write, Edit, Bash(*)]
model: sonnet
skills:
  - frontend-development
  - backend-development
  - devops-practices
  - security-guidelines
---
```

Each skill provides domain-specific procedures composing into unified expertise.

---

## Validation Checklist

Before packaging, verify:

### Commands
- [ ] No `name` field (filename is command name)
- [ ] Has `description`
- [ ] Tool patterns valid (see syntax.md)
- [ ] No forbidden params: `permissionMode`, `skills`, `keep-coding-instructions`

### Subagents
- [ ] Has `description`
- [ ] `skills` reference existing skill directories
- [ ] `permissionMode` is `ask`, `allow`, or `deny`
- [ ] `model` is `sonnet`, `opus`, or `haiku`

### Skills
- [ ] Has `name` (kebab-case, matches directory)
- [ ] Has `description` (max 1024 chars)
- [ ] SKILL.md under 500 lines
- [ ] No forbidden params

### Styles
- [ ] Has `name` and `description`
- [ ] `keep-coding-instructions` is boolean
- [ ] No tool or model parameters

### Cross-References
- [ ] All skills in `skills:` arrays exist as directories
- [ ] All agents referenced by commands exist
- [ ] No circular dependencies
