# YAML Safety Rules

## Purpose

YAML (YAML Ain't Markup Language) is sensitive to syntax. Incorrect quoting or unescaped characters cause parsing failures that corrupt imports. This guide ensures error-free template generation.

## Critical Characters

### Must-Quote Characters

| Character | Role | Risk | Solution |
|-----------|------|------|----------|
| `:` | Key-value separator | Breaks parsing if in value | Wrap in quotes: `'value: with colon'` |
| `#` | Comment indicator | Truncates value | Quote: `'Task #123'` |
| `&` | Anchor | YAML interprets | Quote: `'Smith & Co'` |
| `*` | Alias | YAML interprets | Quote: `'2 * 3 = 6'` |
| `@` | Reserved | Can cause issues | Quote: `'email@example.com'` |
| `` ` `` | Reserved | Special in some contexts | Quote: `` '`backticks`' `` |
| `%` | Reserved | Directory indicator | Quote: `'50% complete'` |
| `!` | Type indicator | YAML interprets | Quote: `'Hello!'` |
| `?` | Key indicator | YAML interprets | Quote: `'Why?'` |
| <code>&#124;</code> | Literal block | Format indicator | Quote: `'either | or'` |
| `>` | Folded block | Format indicator | Quote: `'5 > 3'` |
| `[` `]` | List delimiters | Array syntax | Quote if in string: `'[notes]'` |
| `{` `}` | Map delimiters | Object syntax | Quote if in string: `'{info}'` |

### Quote Characters Themselves

| Character | Context | Escape Method |
|-----------|---------|---------------|
| `'` | Inside single quotes | Double it: `'it''s fine'` |
| `"` | Inside double quotes | Backslash: `"say \"hi\""` |

## Quoting Strategies

### Strategy 1: Single Quotes (Default)

**Use for:** Most text values, especially with colons, hashes, or special chars

**Pros:** Simple, doesn't require escaping except for single quotes  
**Cons:** Must escape `'` as `''`

```yaml
title: 'Chapter 1: Introduction'
note: 'Task #123 for Smith & Co'
formula: '2 * 3 = 6'
question: 'Why?'
```

**Escape single quotes:**
```yaml
title: 'It''s a beautiful day'      # Correct
description: 'Author''s note'       # Correct
```

### Strategy 2: Double Quotes

**Use for:** Text containing single quotes, or when you need escape sequences

**Pros:** Can use escape sequences like `\n`, `\t`  
**Cons:** Must escape `"` and `\`

```yaml
title: "It's a beautiful day"
path: "C:\\Users\\Documents"
quote: "She said \"Hello\""
```

### Strategy 3: Literal Block (`|`)

**Use for:** Multi-line content preserving line breaks

```yaml
description: |
  First paragraph with details.
  Second paragraph continues here.
  
  Third paragraph after blank line.
```

**Preserves:** Line breaks, indentation, blank lines  
**Best for:** Descriptions, notes, multi-paragraph content

### Strategy 4: Folded Block (`>`)

**Use for:** Long text that should display as single paragraph

```yaml
summary: >
  This is a very long summary that would
  normally wrap across multiple lines but
  should be displayed as a single flowing
  paragraph when parsed.
```

**Result:** Newlines become spaces, blank lines become paragraph breaks  
**Best for:** Long descriptions, abstracts, summaries

### Strategy 5: No Quotes

**Use for:** Numbers, booleans, dates, simple text without special chars

```yaml
count: 42
price: 19.99
active: true
inactive: false
date: 2025-10-21
simple_title: Task Name
```

**Safe characters:** Letters, numbers, spaces, hyphens, underscores  
**Avoid:** Starting with numbers if it looks like a date

## Decision Tree

```
Does value contain special chars (: # & * @ etc)?
├─ YES → Use single quotes
└─ NO → Check further
    │
    Is it multi-line content?
    ├─ YES → Preserve line breaks?
    │   ├─ YES → Literal block |
    │   └─ NO → Folded block >
    └─ NO → Check further
        │
        Does it contain single quotes (')?
        ├─ YES → Use double quotes
        └─ NO → Check further
            │
            Is it a number, boolean, or date?
            ├─ YES → No quotes
            └─ NO → Single quotes (safest)
```

## Common Patterns

### Pattern: Field with Colon
```yaml
# WRONG - breaks parsing
title: Chapter 1: Introduction

# CORRECT - quoted
title: 'Chapter 1: Introduction'
```

### Pattern: Hash/Pound Sign
```yaml
# WRONG - truncates value
task: Task #123

# CORRECT - quoted
task: 'Task #123'
```

### Pattern: URL
```yaml
# SAFE - no special chars that break YAML
url: https://example.com/page

# SAFER - quoted for consistency
url: 'https://example.com/page'
```

### Pattern: Email
```yaml
# SAFE - @ doesn't break YAML but quote for consistency
email: 'user@example.com'
```

### Pattern: Array Values
```yaml
# Inline array
tags: [project, urgent, 'has:colon']

# Block array
tags:
  - project
  - urgent
  - 'has:colon'
```

### Pattern: Empty/Null Values
```yaml
# Explicitly null
field: null

# Omit if optional (better)
# field: (not included)

# Empty string
field: ''
```

## Handlebars Integration

### Template Syntax for Safe YAML

```handlebars
---
# Always quote string fields from data
title: '{{Title}}'
description: '{{Description}}'

# Numbers can be unquoted if truly numeric
count: {{Count}}

# Booleans unquoted
active: {{IsActive}}

# Dates quoted for safety
date: '{{Date}}'

# Fields that might have special chars - ALWAYS quote
note: '{{Notes}}'
email: '{{Email}}'
url: '{{URL}}'

# Arrays - use #each helper
tags: [{{#each Tags}}'{{this}}'{{#unless @last}}, {{/unless}}{{/each}}]

# Multi-line content - use literal block
content: |
  {{Content}}

# Conditional fields
{{#if OptionalField}}
optional: '{{OptionalField}}'
{{/if}}
---
```

### Automatic Escaping Strategy

**For String Fields:**
```handlebars
field: '{{FieldName}}'  <!-- Single quotes by default -->
```

**For Fields Potentially Containing Both Quote Types:**
```handlebars
field: "{{FieldName}}"  <!-- Use double quotes, ensure data is pre-escaped -->
```

**For Multi-line Fields:**
```handlebars
field: |
  {{FieldName}}
```

## Validation Checklist

Before importing, verify:

- [ ] All string values containing `:` are quoted
- [ ] All values with `#` are quoted
- [ ] Email addresses are quoted
- [ ] Task/issue numbers (e.g., #123) are quoted
- [ ] Formulas or equations are quoted
- [ ] Multi-line content uses `|` or `>`
- [ ] Arrays are properly formatted
- [ ] Single quotes in values are escaped as `''`
- [ ] Empty values are handled (null or omitted)

## Error Patterns & Solutions

### Error: "mapping values are not allowed here"

**Cause:** Unquoted colon in value

```yaml
# WRONG
title: Chapter 1: Introduction

# CORRECT
title: 'Chapter 1: Introduction'
```

### Error: "could not find expected ':'"

**Cause:** Unbalanced quotes or missing colon

```yaml
# WRONG - unclosed quote
title: 'Chapter 1

# CORRECT
title: 'Chapter 1: Introduction'
```

### Error: Value truncated or missing

**Cause:** Unquoted `#` treated as comment

```yaml
# WRONG - everything after # is ignored
task: Review PR #123

# CORRECT
task: 'Review PR #123'
```

### Error: "unknown tag !<...>"

**Cause:** Unquoted `!` interpreted as YAML tag

```yaml
# WRONG
exclamation: Hello!

# CORRECT
exclamation: 'Hello!'
```

## Best Practices

1. **When in doubt, quote** - Single quotes are safest default
2. **Quote all user-generated content** - Can't predict what users will enter
3. **Use literal blocks for descriptions** - Preserve formatting
4. **Test with first row** - Validate before bulk import
5. **Standardize formats** - Dates as ISO 8601, URLs as full paths
6. **Document edge cases** - Note any special handling in template comments

## Examples by Scenario

### Scenario: Task Management
```yaml
---
title: 'Review PR #456'
status: 'In Progress'
priority: 'High'
assigned: 'John Smith'
notes: 'Check security implications & update docs'
due: '2025-10-25'
tags: [project/alpha, status/active, priority/high]
---
```

### Scenario: Bibliography
```yaml
---
title: 'Thinking in Systems: A Primer'
author: 'Donella H. Meadows'
subtitle: 'A Primer'
publisher: 'Chelsea Green Publishing'
isbn: '978-1603580557'
topics: [systems-thinking, complexity, feedback-loops]
summary: >
  A concise and crucial book offering insight for
  problem solving on scales ranging from the personal
  to the global.
---
```

### Scenario: Contact Information
```yaml
---
name: 'Dr. Jane Smith'
title: 'VP of Engineering'
company: 'Smith & Associates, Inc.'
email: 'jane.smith@example.com'
phone: '+1-555-123-4567'
linkedin: 'https://linkedin.com/in/janesmith'
notes: |
  Met at conference 2024.
  Interested in AI/ML collaboration.
  Follow up re: Q1 partnership.
---
```

## Related Resources

- **[handlebars-syntax.md](handlebars-syntax.md)** - Template language reference
- **[type-mapping.md](type-mapping.md)** - Field type strategies
- **[error-resolution.md](error-resolution.md)** - Troubleshooting guide
- **[examples/troubleshooting/10-special-chars-fix/](../examples/troubleshooting/10-special-chars-fix/)** - Worked example

---

**Last Updated:** October 2025  
**Version:** 2.0.0