---
name: obsidian-bases
description: This skill should be used when the user asks to "create a Base file", "add filters to a Base", "create formulas", "build a table view", "create cards view", or when working with .base files in Obsidian.
user-invocable: false
---

# Obsidian Bases

## Directory Index

**References:**
- [references/schema-and-structure.md](references/schema-and-structure.md)
- [references/filters.md](references/filters.md)
- [references/properties.md](references/properties.md)
- [references/formulas.md](references/formulas.md)
- [references/functions-reference.md](references/functions-reference.md)
- [references/views-and-summaries.md](references/views-and-summaries.md)

**Examples:** [examples/task-tracker.base](examples/task-tracker.base) | [examples/reading-list.base](examples/reading-list.base) | [examples/project-notes.base](examples/project-notes.base) | [examples/daily-notes-index.base](examples/daily-notes-index.base)

**Templates:** [templates/simple-table.base](templates/simple-table.base) | [templates/kanban-groups.base](templates/kanban-groups.base) | [templates/filtered-view.base](templates/filtered-view.base)

---

Create and edit Obsidian `.base` files for database-like views with filters, formulas, and summaries.

## Quick Syntax Reference

| Feature | Syntax | Example |
|---------|--------|---------|
| File format | `.base` (YAML) | `my-tasks.base` |
| Filter by tag | `file.hasTag("tag")` | `file.hasTag("project")` |
| Filter by folder | `file.inFolder("path")` | `file.inFolder("Notes")` |
| Property access | `property_name` | `status`, `due_date` |
| File property | `file.*` | `file.name`, `file.mtime` |
| Formula | `formula.name` | `formula.days_left` |
| View types | `table`, `cards`, `list`, `map` | `type: table` |

## Minimal Schema

```yaml
filters:
  and:
    - file.hasTag("project")

views:
  - type: table
    name: "My View"
    order:
      - file.name
      - status
```

## Core Concepts

### Filters

```yaml
# Single condition
filters: 'status == "done"'

# Multiple conditions (AND)
filters:
  and:
    - file.hasTag("task")
    - 'status != "done"'

# Multiple conditions (OR)
filters:
  or:
    - file.hasTag("book")
    - file.hasTag("article")
```

### Formulas

```yaml
formulas:
  days_until: 'if(due, ((date(due) - today()) / 86400000).round(0), "")'
  is_overdue: 'if(due, date(due) < today(), false)'
  priority_icon: 'if(priority == 1, "🔴", if(priority == 2, "🟡", "🟢"))'
```

### Views with Grouping

```yaml
views:
  - type: table
    name: "Tasks by Status"
    groupBy:
      property: status
      direction: ASC
    order:
      - file.name
      - formula.days_until
    summaries:
      formula.days_until: Average
```

## Detailed Documentation

For comprehensive syntax, see:

- [Schema & Structure](references/schema-and-structure.md) - Complete YAML schema
- [Filters](references/filters.md) - Filter syntax and operators
- [Properties](references/properties.md) - Property types and file properties
- [Formulas](references/formulas.md) - Formula syntax and patterns
- [Functions Reference](references/functions-reference.md) - All 80+ functions
- [Views & Summaries](references/views-and-summaries.md) - View types and summaries

## Examples

Working `.base` files you can copy:

- [Task Tracker](examples/task-tracker.base) - Task management with formulas
- [Reading List](examples/reading-list.base) - Books with cards view
- [Project Notes](examples/project-notes.base) - Project tracking
- [Daily Notes Index](examples/daily-notes-index.base) - Daily notes with regex

## Templates

Starter templates to customize:

- [Simple Table](templates/simple-table.base) - Basic table view
- [Kanban Groups](templates/kanban-groups.base) - Grouped by status
- [Filtered View](templates/filtered-view.base) - Tag/folder filters

## Embedding Bases

```markdown
![[MyBase.base]]
![[MyBase.base#View Name]]
```

## References

- [Obsidian Help - Bases Syntax](https://help.obsidian.md/bases/syntax)
- [Obsidian Help - Functions](https://help.obsidian.md/bases/functions)

## Memory Integration

This subskill contributes to the [Obsidian skill's](../SKILL.md) self-iterative memory:

- **Tracked patterns**: filters, formulas, views, summaries
- **Memory location**: `.claude/obsidian-memory.json`
- **Learning**: Your frequently used patterns inform future suggestions

[← Back to Obsidian Skill](../SKILL.md)
