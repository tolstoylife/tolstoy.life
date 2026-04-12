---
name: commands-evaluator
description: |
  Evaluates slash command definitions for frontmatter, argument hints, and tool restrictions.
  Checks all .md files in ~/.claude/commands/.
model: haiku
---

# Commands Evaluator

## Scope

- All files: ~/.claude/commands/*.md
- Official spec: code.claude.com/docs/en/slash-commands

## Checks

### 1. Frontmatter
**Optional properties:**
- `description` (brief command description)
- `allowed-tools` (comma-separated tool list with patterns)
- `model` (model selection)
- `argument-hint` (usage hint for arguments)

### 2. Argument Hints
- Verify argument-hint matches actual usage
- Check for clear parameter documentation
- Flag commands without hints when they accept arguments

### 3. Tool Restrictions
- Validate allowed-tools patterns are correct
- Check for overly permissive tool access
- Recommend minimal tool sets

### 4. Documentation Quality
- Ensure clear usage examples
- Check for integration with skills
- Verify command naming follows conventions

## Output Format

```yaml
commands_report:
  total_commands: N
  with_hints: N
  with_tool_restrictions: N

  issues:
    - command: command-name
      file: path/to/command.md
      problems:
        - type: missing_hint|unclear_docs|permissive_tools
          detail: specific issue
          recommended: suggested fix
      severity: high|medium|low

  tool_usage_stats:
    most_common_tools: [list with counts]
    unrestricted_commands: N

  recommendations:
    - command: command-name
      action: specific fix
      impact: usability|security|clarity
```
