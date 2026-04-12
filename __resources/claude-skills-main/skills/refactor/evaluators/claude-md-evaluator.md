---
name: claude-md-evaluator
description: |
  Evaluates ~/.claude/CLAUDE.md for syntax, import resolution, redundancy, and token efficiency.
  Use when refactor-agent needs to analyze the main configuration file.
model: sonnet
---

# Claude MD Evaluator

## Scope

- Main file: ~/.claude/CLAUDE.md
- Imported rules: @rules/core/*.md, @rules/tools/*.md, @rules/infrastructure/*.md

## Checks

### 1. Syntax Validation
- YAML frontmatter validity
- Markdown structure integrity
- @import statement syntax

### 2. Import Resolution
- Verify all @import paths resolve
- Check for circular dependencies
- Identify missing referenced files

### 3. Redundancy Detection
- Find duplicate configuration blocks
- Identify conflicting settings
- Flag redundant @import statements

### 4. Token Efficiency
- Calculate total token count
- Identify verbose sections
- Suggest compression opportunities

## Output Format

```yaml
claude_md_report:
  syntax:
    valid: true|false
    errors: [list of syntax errors]

  imports:
    total: N
    resolved: N
    missing: [list of unresolved paths]
    circular: [list of circular dependency chains]

  redundancy:
    duplicates: [list of duplicate blocks]
    conflicts: [list of conflicting settings]

  efficiency:
    total_tokens: N
    verbose_sections: [list with token counts]
    optimization_potential: X%

  recommendations:
    - priority: high|medium|low
      issue: description
      action: specific fix
```
