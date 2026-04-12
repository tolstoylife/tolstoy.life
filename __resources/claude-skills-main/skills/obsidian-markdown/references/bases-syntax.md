# Obsidian Bases Syntax Reference

Bases is a core plugin (Obsidian 1.9.0+) that turns notes into queryable databases using properties.

## File Format

Bases are saved as `.base` files containing YAML configuration for views, filters, and formulas.

## Creating a Base

1. Create a new base from Command Palette: "Create new base"
2. Or right-click folder → "Create base in folder"
3. Edit via UI or manually edit .base file

## Base Syntax (YAML)

```yaml
views:
  - id: view-1
    name: "Table View"
    type: table
    filter:
      and:
        - property: status
          operator: equals
          value: active
        - property: priority
          operator: in
          value: [high, medium]
    sort:
      - property: due-date
        direction: ascending
    columns:
      - property: title
        width: 300
      - property: status
      - property: due-date
    formulas:
      - id: days-remaining
        name: "Days Left"
        expression: "datediff(due-date, today())"
```

## Filters

### Single Filter (String)
```yaml
filter: "status = 'active'"
```

### Filter Object

#### AND Filter
```yaml
filter:
  and:
    - property: status
      operator: equals
      value: active
    - property: priority
      operator: not-equals
      value: low
```

#### OR Filter
```yaml
filter:
  or:
    - property: type
      operator: equals
      value: project
    - property: type
      operator: equals
      value: task
```

#### NOT Filter
```yaml
filter:
  not:
    property: status
    operator: equals
    value: archived
```

### Filter Operators

- `equals` - Exact match
- `not-equals` - Not equal
- `contains` - Contains text
- `not-contains` - Does not contain
- `starts-with` - Starts with text
- `ends-with` - Ends with text
- `is-empty` - Property is empty
- `is-not-empty` - Property has value
- `greater-than` - Numeric/date comparison
- `less-than` - Numeric/date comparison
- `greater-than-or-equal` - Inclusive comparison
- `less-than-or-equal` - Inclusive comparison
- `in` - Value in list
- `not-in` - Value not in list

## Formulas

Bases support formula properties with basic arithmetic and built-in functions.

### Arithmetic Operators
- `+` - Addition
- `-` - Subtraction
- `*` - Multiplication
- `/` - Division
- `%` - Modulo
- `^` - Exponentiation

### Built-in Functions

#### Date Functions
```yaml
today() # Current date
datediff(date1, date2) # Days between dates
dateadd(date, days) # Add days to date
year(date) # Extract year
month(date) # Extract month
day(date) # Extract day
```

#### String Functions
```yaml
concat(str1, str2, ...) # Concatenate strings
upper(text) # Uppercase
lower(text) # Lowercase
length(text) # String length
substr(text, start, length) # Substring
```

#### Numeric Functions
```yaml
round(number) # Round to integer
ceil(number) # Round up
floor(number) # Round down
abs(number) # Absolute value
min(num1, num2, ...) # Minimum value
max(num1, num2, ...) # Maximum value
sum(list) # Sum of list
average(list) # Average of list
count(list) # Count items
```

#### Logical Functions
```yaml
if(condition, true_value, false_value)
and(condition1, condition2, ...)
or(condition1, condition2, ...)
not(condition)
```

### Formula Examples

```yaml
formulas:
  - id: days-until-due
    name: "Days Until Due"
    expression: "datediff(due-date, today())"

  - id: is-overdue
    name: "Overdue"
    expression: "if(datediff(due-date, today()) < 0, 'Yes', 'No')"

  - id: full-name
    name: "Full Name"
    expression: "concat(first-name, ' ', last-name)"

  - id: completion-rate
    name: "Progress"
    expression: "round((completed / total) * 100)"
```

## View Types

### Table View
```yaml
views:
  - id: table-1
    name: "Project Table"
    type: table
    columns:
      - property: title
        width: 300
      - property: status
      - property: assignee
```

### Board View (Kanban)
```yaml
views:
  - id: board-1
    name: "Task Board"
    type: board
    group-by: status
    card-properties:
      - assignee
      - due-date
```

### Gallery View
```yaml
views:
  - id: gallery-1
    name: "Image Gallery"
    type: gallery
    cover-property: thumbnail
```

### Calendar View
```yaml
views:
  - id: calendar-1
    name: "Timeline"
    type: calendar
    date-property: due-date
```

## Sorting

```yaml
sort:
  - property: priority
    direction: descending
  - property: due-date
    direction: ascending
```

## Complete Example

```yaml
name: "Project Tracker"
description: "Track all active projects"
source:
  folder: "Projects"

views:
  - id: active-projects
    name: "Active Projects"
    type: table
    filter:
      and:
        - property: status
          operator: in
          value: [planning, in-progress, review]
        - property: archived
          operator: not-equals
          value: true
    sort:
      - property: priority
        direction: descending
      - property: due-date
        direction: ascending
    columns:
      - property: title
        width: 300
      - property: status
        width: 120
      - property: assignee
        width: 150
      - property: due-date
        width: 120
      - formula: days-remaining
        width: 100
    formulas:
      - id: days-remaining
        name: "Days Left"
        expression: "datediff(due-date, today())"

  - id: by-status
    name: "Kanban Board"
    type: board
    group-by: status
    card-properties:
      - assignee
      - due-date
      - priority
```

## Working with Bases via Plugin API

Bases API allows plugin developers to extend functionality (planned feature).

### Access Base Data
```javascript
// API access (when available)
const base = app.plugins.getPlugin('bases').getBase('base-id');
const records = base.query(filter);
```

## Best Practices

1. Use descriptive property names in kebab-case
2. Define formulas for calculated fields
3. Create multiple views for different perspectives
4. Use filters to keep views focused
5. Leverage sort for prioritization
6. Group related properties in board views

## References

- Official docs: https://help.obsidian.md/bases/syntax
- Changelog: https://obsidian.md/changelog/2025-05-21-desktop-v1.9.0/
- Format: Valid YAML conforming to Bases schema
