# Handlebars Template Syntax

## Overview

Handlebars is a logic-less templating language that compiles templates into JavaScript functions. For Obsidian imports, we use it to inject data values into Markdown templates.

## Basic Concepts

### Variable Substitution

**Simple Variables:**
```handlebars
{{FieldName}}
```

Renders the value of `FieldName` from your data.

**CSV Example:**
```csv
Title,Author,Year
Dune,Frank Herbert,1965
```

**Template:**
```handlebars
# {{Title}}
By {{Author}} ({{Year}})
```

**Output:**
```markdown
# Dune
By Frank Herbert (1965)
```

### Nested Properties (JSON)

Access nested object properties with dot notation:

```handlebars
{{object.property}}
{{object.nested.deepProperty}}
```

**JSON Example:**
```json
{
  "book": {
    "title": "Dune",
    "author": {
      "first": "Frank",
      "last": "Herbert"
    }
  }
}
```

**Template:**
```handlebars
# {{book.title}}
By {{book.author.first}} {{book.author.last}}
```

### Array Access

Access array elements by index:

```handlebars
{{array.0}}
{{array.1.property}}
```

**JSON Example:**
```json
{
  "authors": ["Frank Herbert", "Brian Herbert"]
}
```

**Template:**
```handlebars
Primary: {{authors.0}}
Secondary: {{authors.1}}
```

## Conditional Rendering

### #if Helper

Show content only if variable exists and is truthy:

```handlebars
{{#if variable}}
  Content shown if variable exists
{{/if}}
```

**Example:**
```handlebars
{{#if Description}}
## Description
{{Description}}
{{/if}}
```

If `Description` is empty or null, the entire section is omitted.

### #if with else

```handlebars
{{#if variable}}
  Content if true
{{else}}
  Content if false
{{/if}}
```

**Example:**
```handlebars
**Status:** {{#if IsComplete}}✅ Complete{{else}}⏳ In Progress{{/if}}
```

### #unless Helper

Opposite of `#if` - shows content when variable is falsy:

```handlebars
{{#unless variable}}
  Content shown when variable is false/empty
{{/unless}}
```

**Example:**
```handlebars
{{#unless HasNotes}}
_No notes available_
{{/unless}}
```

## Iteration

### #each Helper

Loop through arrays:

```handlebars
{{#each arrayName}}
  {{this}}
{{/each}}
```

**CSV Example with Array:**
```json
{
  "tags": ["project", "urgent", "review"]
}
```

**Template:**
```handlebars
Tags:
{{#each tags}}
- {{this}}
{{/each}}
```

**Output:**
```markdown
Tags:
- project
- urgent
- review
```

### #each with Objects

Access properties of objects in arrays:

```handlebars
{{#each objectArray}}
  {{this.property}}
{{/each}}
```

**JSON Example:**
```json
{
  "tasks": [
    {"name": "Task 1", "status": "Done"},
    {"name": "Task 2", "status": "In Progress"}
  ]
}
```

**Template:**
```handlebars
## Tasks
{{#each tasks}}
- **{{this.name}}**: {{this.status}}
{{/each}}
```

### Special Variables in Loops

**@index** - Zero-based index:
```handlebars
{{#each items}}
  {{@index}}. {{this}}
{{/each}}
```

**@first** - True for first item:
```handlebars
{{#each items}}
  {{#if @first}}**{{this}}**{{else}}{{this}}{{/if}}
{{/each}}
```

**@last** - True for last item:
```handlebars
{{#each items}}
  {{this}}{{#unless @last}}, {{/unless}}
{{/each}}
```

Output: `item1, item2, item3` (no comma after last)

**@key** - Property name in object iteration:
```handlebars
{{#each object}}
  {{@key}}: {{this}}
{{/each}}
```

## Comments

Comments aren't rendered in output:

```handlebars
{{!-- This is a comment --}}
{{! Short comment }}
```

**Use for:**
- Template documentation
- Explaining field purposes
- Noting customization points

**Example:**
```handlebars
---
{{!-- Basic metadata --}}
title: '{{Title}}'

{{!-- Optional field - only included if present --}}
{{#if Description}}
description: '{{Description}}'
{{/if}}
---
```

## Combining Techniques

### Pattern: Optional Sections

```handlebars
{{#if Subtasks}}
## Subtasks
{{#each Subtasks}}
- [ ] {{this}}
{{/each}}
{{/if}}
```

Shows section only if `Subtasks` exists and has items.

### Pattern: Formatted Lists

```handlebars
tags: [{{#each Tags}}'{{this}}'{{#unless @last}}, {{/unless}}{{/each}}]
```

Output: `tags: ['tag1', 'tag2', 'tag3']`

### Pattern: Conditional Metadata

```handlebars
---
title: '{{Title}}'
{{#if DueDate}}
due: '{{DueDate}}'
{{/if}}
{{#if Priority}}
priority: '{{Priority}}'
{{/if}}
---
```

Only includes fields that have values.

### Pattern: Nested Iteration

```handlebars
{{#each Projects}}
## {{this.name}}
{{#each this.tasks}}
- {{this.description}}
{{/each}}
{{/each}}
```

Iterates through projects, then tasks within each project.

## Complete Examples

### Example 1: Task Template

**Data:**
```json
{
  "task": "Review PR",
  "status": "In Progress",
  "priority": "High",
  "assignee": "John",
  "subtasks": ["Check tests", "Review code", "Update docs"],
  "notes": "Focus on security"
}
```

**Template:**
```handlebars
---
title: '{{task}}'
status: '{{status}}'
priority: '{{priority}}'
assigned: '{{assignee}}'
tags: [task, priority/{{priority}}, status/{{status}}]
---

# {{task}}

**Status:** {{status}}  
**Priority:** {{priority}}  
**Assigned to:** [[{{assignee}}]]

{{#if subtasks}}
## Subtasks
{{#each subtasks}}
- [ ] {{this}}
{{/each}}
{{/if}}

{{#if notes}}
## Notes
{{notes}}
{{/if}}
```

### Example 2: Reference Material

**Data:**
```json
{
  "title": "Thinking in Systems",
  "author": {"first": "Donella", "last": "Meadows"},
  "year": 2008,
  "topics": ["systems thinking", "complexity"],
  "summary": "A primer on systems thinking"
}
```

**Template:**
```handlebars
---
title: '{{title}}'
author: '{{author.first}} {{author.last}}'
year: {{year}}
type: book
tags: [book, {{#each topics}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}]
---

# {{title}}

**Author:** [[{{author.first}} {{author.last}}]]  
**Year:** {{year}}

## Topics
{{#each topics}}
- [[{{this}}]]
{{/each}}

{{#if summary}}
## Summary
{{summary}}
{{/if}}

## Notes
[Add your notes here]
```

### Example 3: CSV with Multiple Fields

**CSV:**
```csv
Name,Email,Company,Role,LinkedIn
John Smith,john@example.com,Acme Inc,Engineer,https://linkedin.com/in/john
Jane Doe,jane@example.com,Beta Corp,Manager,https://linkedin.com/in/jane
```

**Template:**
```handlebars
---
name: '{{Name}}'
email: '{{Email}}'
company: '[[{{Company}}]]'
role: '{{Role}}'
type: person
tags: [people, {{Company}}]
---

# {{Name}}

**Role:** {{Role}} at [[{{Company}}]]  
**Email:** {{Email}}

{{#if LinkedIn}}
**LinkedIn:** [Profile]({{LinkedIn}})
{{/if}}

## Interactions
[Document interactions here]

## Related
- [[{{Company}}]]
```

## Best Practices

### 1. Always Use Conditionals for Optional Fields

```handlebars
{{!-- GOOD - won't break if field missing --}}
{{#if OptionalField}}
field: '{{OptionalField}}'
{{/if}}

{{!-- BAD - creates empty field if missing --}}
field: '{{OptionalField}}'
```

### 2. Quote YAML String Values

```handlebars
{{!-- GOOD - YAML safe --}}
title: '{{Title}}'

{{!-- BAD - breaks if Title contains special chars --}}
title: {{Title}}
```

See [yaml-safety.md](yaml-safety.md) for details.

### 3. Use #unless @last for Comma Separation

```handlebars
{{!-- GOOD - no trailing comma --}}
[{{#each items}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}]

{{!-- BAD - trailing comma --}}
[{{#each items}}{{this}}, {{/each}}]
```

### 4. Document Template Intent

```handlebars
{{!-- This template creates task notes with:
     - Status tracking
     - Priority levels
     - Assignee links
     - Optional subtasks
--}}
---
title: '{{TaskName}}'
...
```

### 5. Test with Sample Data

Always preview template with actual data before bulk import.

## Common Patterns

### Pattern: Wikilink Generation

```handlebars
[[{{FieldName}}]]
```

Creates links to other notes.

### Pattern: Tag Formation

```handlebars
tags: [imported, {{Category}}, status/{{Status}}]
```

Hierarchical tags with dynamic values.

### Pattern: Date Handling

```handlebars
created: '{{CreatedDate}}'
modified: '{{ModifiedDate}}'
```

Keep dates as strings for Obsidian compatibility.

### Pattern: URL Links

```handlebars
[Link text]({{URL}})
{{#if URL}}[View Source]({{URL}}){{/if}}
```

Markdown hyperlinks with optional rendering.

### Pattern: Conditional Sections

```handlebars
{{#if SectionData}}
## Section Title
{{SectionData}}
{{/if}}
```

Entire sections disappear if data absent.

## Troubleshooting

### Variables Not Replacing

**Problem:** `{{FieldName}}` appears literally in output

**Causes:**
1. Field name doesn't match data (case-sensitive)
2. JSON path incorrect (missing dots)
3. Data is nested but accessed as flat

**Solutions:**
```handlebars
{{!-- Verify exact field name from data --}}
CSV: Check header row
JSON: Check exact property name

{{!-- For nested JSON, use dot notation --}}
{{object.property}}

{{!-- Check with simple test --}}
{{FieldName}} → If this shows, field exists
```

### Empty Output

**Problem:** Entire section missing when expected

**Cause:** Conditional evaluates to false

**Debug:**
```handlebars
{{!-- Test if field exists --}}
DEBUG: "{{FieldName}}" (shows value or empty)

{{!-- Check conditional --}}
{{#if FieldName}}
  FIELD EXISTS
{{else}}
  FIELD MISSING
{{/if}}
```

### Arrays Not Iterating

**Problem:** `{{#each}}` shows nothing

**Causes:**
1. Field is not actually an array
2. Array is empty
3. Path to array is incorrect

**Solutions:**
```handlebars
{{!-- Verify array exists --}}
{{#if ArrayField}}
  Array exists
  {{#each ArrayField}}
    Item: {{this}}
  {{/each}}
{{else}}
  Array missing
{{/if}}
```

## Related Resources

- **[yaml-safety.md](yaml-safety.md)** - YAML escaping rules
- **[type-mapping.md](type-mapping.md)** - Data type strategies
- **[templates/](../templates/)** - Complete template examples
- **[Handlebars.js Documentation](https://handlebarsjs.com/guide/)** - Official reference

---

**Last Updated:** October 2025  
**Version:** 2.0.0