---
name: formulas
description: Formula syntax for Obsidian Bases including computed properties, expressions, and operators.
---

# Formula Syntax Reference

Formulas compute values from properties. Defined in the `formulas` section.

## Basic Formula Examples

```yaml
formulas:
  # Simple arithmetic
  total: "price * quantity"

  # Conditional logic
  status_icon: 'if(done, "✅", "⏳")'

  # String formatting
  formatted_price: 'if(price, price.toFixed(2) + " dollars")'

  # Date formatting
  created: 'file.ctime.format("YYYY-MM-DD")'

  # Complex expressions
  days_old: '((now() - file.ctime) / 86400000).round(0)'
```

## Referencing Formulas

Once defined in the `formulas` section, use them in views:

```yaml
formulas:
  days_until_due: 'if(due, ((date(due) - today()) / 86400000).round(0), "")'

properties:
  formula.days_until_due:
    displayName: "Days Until Due"

views:
  - type: table
    order:
      - file.name
      - formula.days_until_due
```

## Common Formula Patterns

### Date Calculations

```yaml
formulas:
  # Days from now
  days_until: '((date(due_date) - today()) / 86400000).round(0)'

  # Days old
  age_in_days: '((now() - file.ctime) / 86400000).round(0)'

  # Format date
  pretty_date: 'file.ctime.format("MMMM DD, YYYY")'

  # Extract year
  year_created: 'file.ctime.year'
```

### Conditional Logic

```yaml
formulas:
  # Status icon
  status_icon: 'if(status == "done", "✅", if(status == "in-progress", "🔄", "⏳"))'

  # Priority label
  priority_label: 'if(priority == 1, "🔴 High", if(priority == 2, "🟡 Medium", "🟢 Low"))'

  # Overdue check
  is_overdue: 'if(due, date(due) < today() && status != "done", false)'
```

### String Operations

```yaml
formulas:
  # Concatenation
  full_name: 'first_name + " " + last_name'

  # Uppercase
  title_upper: 'title.upper()'

  # Reading time estimate
  reading_time: 'if(pages, (pages * 2).toString() + " min", "")'
```

### Number Operations

```yaml
formulas:
  # Percentage
  completion: '((completed / total) * 100).round(1) + "%"'

  # Word count estimate
  word_estimate: '(file.size / 5).round(0)'

  # Average
  avg_score: '(score1 + score2 + score3) / 3'
```

### List Operations

```yaml
formulas:
  # Count links
  link_count: 'file.links.length'

  # Count tags
  tag_count: 'file.tags.length'

  # Join list
  tag_list: 'file.tags.join(", ")'
```

## Date Arithmetic

```yaml
# Duration units: y/year/years, M/month/months, d/day/days,
#                 w/week/weeks, h/hour/hours, m/minute/minutes, s/second/seconds

formulas:
  # Add/subtract durations
  tomorrow: 'today() + "1d"'
  next_week: 'now() + "7d"'
  last_month: 'now() - "1M"'

  # Complex duration arithmetic
  two_days_ahead: 'now() + (duration("1d") * 2)'

  # Subtract dates for millisecond difference
  time_since_creation: 'now() - file.ctime'
```

---

[← Back to Obsidian Bases](../SKILL.md)
