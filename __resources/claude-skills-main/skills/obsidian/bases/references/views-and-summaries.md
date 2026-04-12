---
name: views-and-summaries
description: View types and summary configurations for Obsidian Bases including table, cards, list, and map views.
---

# Views and Summaries Reference

## View Types

### Table View

```yaml
views:
  - type: table
    name: "My Table"
    order:
      - file.name
      - status
      - due_date
    summaries:
      price: Sum
      count: Average
```

### Cards View

```yaml
views:
  - type: cards
    name: "Gallery"
    order:
      - file.name
      - cover_image
      - description
```

### List View

```yaml
views:
  - type: list
    name: "Simple List"
    order:
      - file.name
      - status
```

### Map View

Requires latitude/longitude properties and the Maps plugin.

```yaml
views:
  - type: map
    name: "Locations"
    # Map-specific settings for lat/lng properties
```

## View Configuration Options

### Limit Results

```yaml
views:
  - type: table
    name: "Top 10"
    limit: 10
```

### Group By

```yaml
views:
  - type: table
    name: "Grouped View"
    groupBy:
      property: status
      direction: ASC  # or DESC
```

### View-Specific Filters

```yaml
views:
  - type: table
    name: "Active Only"
    filters:
      and:
        - 'status != "done"'
```

## Default Summary Formulas

| Name | Input Type | Description |
|------|------------|-------------|
| `Average` | Number | Mathematical mean |
| `Min` | Number | Smallest number |
| `Max` | Number | Largest number |
| `Sum` | Number | Sum of all numbers |
| `Range` | Number | Max - Min |
| `Median` | Number | Mathematical median |
| `Stddev` | Number | Standard deviation |
| `Earliest` | Date | Earliest date |
| `Latest` | Date | Latest date |
| `Range` | Date | Latest - Earliest |
| `Checked` | Boolean | Count of true values |
| `Unchecked` | Boolean | Count of false values |
| `Empty` | Any | Count of empty values |
| `Filled` | Any | Count of non-empty values |
| `Unique` | Any | Count of unique values |

## Custom Summary Formulas

Define custom summaries in the `summaries` section:

```yaml
summaries:
  avgLinks: 'values.filter(value.isType("number")).mean().round(1)'
  totalScore: 'values.sum()'
  uniqueCount: 'values.unique().length'

views:
  - type: table
    summaries:
      formula.link_count: avgLinks
      score: totalScore
```

## Embedding Bases

Embed in Markdown files:

```markdown
![[MyBase.base]]

<!-- Specific view -->
![[MyBase.base#View Name]]
```

## YAML Quoting Rules

- Use single quotes for formulas containing double quotes: `'if(done, "Yes", "No")'`
- Use double quotes for simple strings: `"My View Name"`
- Escape nested quotes properly in complex expressions

### Examples

```yaml
# Good - single quotes for formulas with double quotes
formulas:
  status_label: 'if(status == "done", "✅ Complete", "⏳ Pending")'

# Good - double quotes for simple strings
views:
  - name: "Active Tasks"

# Bad - unquoted formula
formulas:
  broken: if(done, "Yes", "No")  # Will fail

# Good - properly quoted nested formula
formulas:
  complex: 'if(x, if(y, "Both", "X only"), if(y, "Y only", "Neither"))'
```

---

[← Back to Obsidian Bases](../SKILL.md)
