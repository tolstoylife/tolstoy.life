# Syntax Reference

## Table of Contents

1. [Commands](#commands)
2. [Subagents](#subagents)
3. [Skills](#skills)
4. [Output Styles](#output-styles)
5. [Spawn Parameters](#spawn-parameters)
6. [Tool Patterns](#tool-patterns)

---

## Commands

**Location:** `.claude/commands/<name>.md` → `/name`

```yaml
---
# REQUIRED
description: string          # Imperative action description

# OPTIONAL
allowed-tools: [Tool, ...]   # Tool access patterns
model: sonnet|opus|haiku     # Default: sonnet
argument-hint: <placeholder> # CLI hint shown in /help
disable-model-invocation: bool # Pure script mode (no LLM)
---

[Markdown: procedural instructions, subagent spawning]
```

**Forbidden:** `name`, `permissionMode`, `skills`, `keep-coding-instructions`

---

## Subagents

**Location:** `.claude/agents/<name>.md`

```yaml
---
# REQUIRED
description: string          # Role identity + expertise + traits

# OPTIONAL
allowed-tools: [Tool, ...]   # Permitted tools
disallowed-tools: [Tool, ...] # Explicit denials
model: sonnet|opus|haiku     # Default reasoning model
permissionMode: ask|allow|deny # Autonomy level
skills: [skill-a, skill-b]   # Auto-loaded procedural knowledge
---

[Markdown: persona definition, decision heuristics]
```

**Forbidden:** `argument-hint`, `disable-model-invocation`, `keep-coding-instructions`

**permissionMode values:**
- `ask` — Prompt before sensitive operations (default)
- `allow` — Execute without prompting (trusted automation)
- `deny` — Read-only mode, no modifications

---

## Skills

**Location:** `.claude/skills/<name>/SKILL.md`

```yaml
---
# REQUIRED
name: string                 # Kebab-case, matches directory
description: string          # What + when + triggers (≤1024 chars)

# OPTIONAL
allowed-tools: [Tool, ...]   # Tool restrictions when active
---

[Markdown: procedural instructions, workflow steps]
```

**Forbidden:** `model`, `argument-hint`, `disable-model-invocation`, `permissionMode`, `skills`, `keep-coding-instructions`

**Constraints:**
- `name`: kebab-case, max 64 chars, no leading/trailing/consecutive hyphens
- `description`: max 1024 chars, no angle brackets

---

## Output Styles

**Location:** `.claude/styles/<name>.md` or via SessionStart hooks

```yaml
---
# REQUIRED
name: string                 # Style identifier
description: string          # Interaction mode description

# OPTIONAL
keep-coding-instructions: bool # Preserve coding behavior (default: true)
---

[Markdown: behavioral modifications, output format]
```

**Forbidden:** `allowed-tools`, `model`, `argument-hint`, `disable-model-invocation`, `permissionMode`, `skills`

### Hook-Based Implementation (Modern)

```
style-plugin/
├── .claude-plugin/plugin.json
├── hooks/hooks.json
└── hooks-handlers/session-start.sh
```

**hooks.json:**
```json
{"hooks": [{"name": "style", "event": "SessionStart", 
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks-handlers/session-start.sh"}]}
```

**session-start.sh:**
```bash
#!/bin/bash
cat << 'EOF'
{"additionalContext": "Style instructions here..."}
EOF
```

---

## Spawn Parameters

When spawning subagents via `Agent` tool:

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent_id` | string | Reference to `.claude/agents/*.md` |
| `systemMessage` | string | Additional context for spawn |
| `model` | string | Override agent's default model |
| `allowed_tools` | string[] | Override tool access |
| `disallowed_tools` | string[] | Additional restrictions |
| `permissionMode` | string | Override autonomy level |
| `plan_mode_required` | bool | Force plan approval |

---

## Tool Patterns

### Basic Tools

| Tool | Description |
|------|-------------|
| `Read` | File reading |
| `Write` | File writing |
| `Edit` | File editing |
| `Glob` | File globbing |
| `Grep` | Text search |
| `LS` | Directory listing |
| `Agent` | Subagent spawning |
| `WebFetch` | URL fetching |

### Bash Patterns

```yaml
Bash(git status)        # Exact command
Bash(git:*)             # All git subcommands
Bash(npm run:*)         # All npm run scripts
Bash(gh pr:*)           # All GitHub PR commands
```

### MCP Tools

```yaml
mcp__server__tool       # Specific tool
mcp__github__*          # All tools from server
```

### Combined Example

```yaml
allowed-tools:
  - Read
  - Write
  - Bash(git:*)
  - Bash(npm:*)
  - Agent
  - mcp__github__create_pr
```
