# Official Claude Code Component Specifications

> Last verified: 2026-01-14
> Sources: code.claude.com/docs/en/skills, code.claude.com/docs/en/sub-agents

## SKILL.md Frontmatter

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Skill name (lowercase, hyphens, max 64 chars) |
| `description` | string | What skill does and when to use (max 1024 chars) |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `allowed-tools` | string/array | Tools without permission prompts |
| `model` | string | Model to use (`haiku`, `sonnet`, `opus`, or full ID) |
| `context` | string | Set to `fork` for forked sub-agent context |
| `agent` | string | Agent type when context: fork |
| `hooks` | object | Lifecycle hooks (PreToolUse, PostToolUse, Stop) |
| `user-invocable` | boolean | Controls slash menu visibility (default true) |
| `disable-model-invocation` | boolean | Blocks Skill tool programmatic invocation |

### NOT Official (Move to Body)

- `version`
- `triggers`
- `metadata`
- `integrates`
- `progressive_loading`
- `architecture`

## Agent File Frontmatter

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier (lowercase, hyphens) |
| `description` | string | When Claude should delegate to this subagent |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `tools` | array | Tools the subagent can use (inherits all if omitted) |
| `disallowedTools` | array | Tools to deny |
| `model` | string | `sonnet`, `opus`, `haiku`, or `inherit` (default: sonnet) |
| `permissionMode` | string | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `skills` | array | Skills to load at startup |
| `hooks` | object | Lifecycle hooks scoped to this subagent |

## Command File Frontmatter

All fields optional:

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Brief description |
| `allowed-tools` | string | Comma-separated tool list |
| `model` | string | Model selection |
| `argument-hint` | string | Usage hint for arguments |

## Plugin.json

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ Yes | Plugin identifier |
| `description` | ✅ Yes | Plugin description |
| `author` | No | `{name, email}` object |

## Hooks (hooks.json)

```json
{
  "description": "Optional explanation",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {"type": "command", "command": "./script.sh"}
        ]
      }
    ],
    "PostToolUse": [],
    "Stop": [],
    "SessionStart": [],
    "SessionEnd": []
  }
}
```

## Model Selection Guide

| Complexity | Model | Use Cases |
|------------|-------|-----------|
| High | opus | Architecture, debugging, multi-domain reasoning |
| Medium | sonnet | Implementation, refactoring, moderate analysis |
| Low | haiku | Searches, lookups, simple transforms |
| Inherited | inherit | When parent context model is appropriate |

## Permission Mode Guide

| Mode | Use When |
|------|----------|
| plan | Complex multi-step tasks requiring human feedback before implementation |
| acceptEdits | Potential edge cases need user confirmation on edits |
| bypassPermissions | Clear requirements, preplanned, or promise completion |
| default | Normal permission checking with prompts |
| dontAsk | Auto-deny risky prompts, allow explicit tools only |

## Architecture Pattern: One Skill = One Agent

For every active skill:
1. Set `context: fork` in SKILL.md
2. Create designated agent at `~/.claude/agents/{skill-name}-agent.md`
3. Configure agent with appropriate model and permissionMode
4. Add complementary skills to agent's `skills` array
5. Define scoped hooks for lifecycle management
