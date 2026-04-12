# YAML Frontmatter Properties Reference

YAML frontmatter provides structured metadata for Obsidian notes.

## Basic Structure

```markdown
---
property-name: value
another-property: another value
---

# Note content starts here
```

## Property Types

### Text
```yaml
title: My Note Title
author: John Doe
description: A brief description of the note
```

### Number
```yaml
rating: 5
page-count: 342
version: 1.0
```

### Date
```yaml
created: 2025-01-15
modified: 2025-01-20
due-date: 2025-02-01
published: 2025-01-15T10:30:00
```

**Formats:**
- `YYYY-MM-DD` - Date only
- `YYYY-MM-DDTHH:mm:ss` - Date and time (ISO 8601)
- `YYYY-MM-DD HH:mm` - Alternative format

### Checkbox (Boolean)
```yaml
completed: true
archived: false
public: true
```

### List (Array)
```yaml
tags:
  - project
  - work
  - urgent

authors:
  - Alice
  - Bob

related-links:
  - "[[Note 1]]"
  - "[[Note 2]]"
```

**Inline list format:**
```yaml
tags: [project, work, urgent]
```

### Aliases
```yaml
aliases:
  - Alternative Name
  - Shorthand
  - Abbreviation
```

Aliases allow the note to be found/linked via alternative names.

### cssclasses
```yaml
cssclasses:
  - custom-style
  - wide-page
  - no-header
```

Applies CSS classes to the note for custom styling.

## Common Properties

### Standard Metadata
```yaml
---
title: Note Title
created: 2025-01-15
modified: 2025-01-20
author: Author Name
tags: [tag1, tag2, tag3]
aliases: [Alternative Name]
---
```

### Project Tracking
```yaml
---
type: project
status: in-progress
priority: high
assignee: John Doe
due-date: 2025-02-15
progress: 45
---
```

### Book Notes
```yaml
---
type: book
title: Book Title
author: Author Name
isbn: 978-0-123456-78-9
published: 2024
rating: 4
status: reading
started: 2025-01-10
finished:
pages: 342
genres:
  - fiction
  - science-fiction
---
```

### Meeting Notes
```yaml
---
type: meeting
date: 2025-01-15
time: "14:00"
duration: 60
attendees:
  - Alice
  - Bob
  - Charlie
location: Conference Room A
recording: "[[recordings/meeting-2025-01-15.mp3]]"
---
```

### Person/Contact
```yaml
---
type: person
name: John Doe
email: john@example.com
phone: "+1-555-0123"
company: Acme Corp
role: Senior Engineer
linkedin: https://linkedin.com/in/johndoe
tags: [colleague, engineering]
---
```

### Daily Note
```yaml
---
type: daily-note
date: 2025-01-15
day: Monday
weather: Sunny
mood: productive
tags: [daily]
---
```

### Research Paper
```yaml
---
type: research-paper
title: Paper Title
authors:
  - First Author
  - Second Author
published: 2024-06-15
journal: Nature
doi: 10.1000/example
url: https://doi.org/10.1000/example
keywords:
  - machine-learning
  - neural-networks
status: read
rating: 5
notes-file: "[[Literature Notes/Paper-2024]]"
---
```

## Multi-line Values

Use pipe `|` for multi-line text:

```yaml
---
description: |
  This is a multi-line description.
  It preserves line breaks.
  Each line appears on a new line.

summary: >
  This is also multi-line,
  but lines are joined with spaces
  into a single paragraph.
---
```

## Special Characters

Enclose values with special characters in quotes:

```yaml
---
title: "Note: With Special Characters"
tag-with-space: "multi word tag"
quoted: "Value with \"quotes\" inside"
---
```

## Property Inheritance (Templates)

When using templates, properties merge:

**Template:**
```yaml
---
type: meeting
template: true
version: 1.0
---
```

**New Note:**
```yaml
---
type: meeting
template: true
version: 1.0
date: 2025-01-15
attendees: [Alice, Bob]
---
```

## Dataview Integration

All frontmatter properties are queryable via Dataview:

```dataview
TABLE author, rating, published
FROM #books
WHERE rating >= 4
SORT published DESC
```

## Bases Integration

All frontmatter properties become columns in Bases:

```yaml
# In .base file
columns:
  - property: status
  - property: priority
  - property: due-date
```

## Property Validation

### Date Properties
- Use ISO 8601 format for consistency
- Date properties auto-link to daily notes (if plugin enabled)

### List Properties
- Use consistent formatting (array or inline)
- Avoid mixing types in same property across notes

### Reserved Properties
- `tags` - Special handling for tag indexing
- `aliases` - Used for alternative linking
- `cssclasses` - Applied to note styling
- `publish` - Controls Obsidian Publish visibility
- `permalink` - Custom URL for Publish sites

## Best Practices

1. **Consistency**: Use same property names across similar note types
2. **Naming**: Use kebab-case for multi-word properties
3. **Types**: Keep property types consistent (don't mix text and numbers)
4. **Required**: Define required properties for each note type
5. **Defaults**: Use template defaults for common properties
6. **Documentation**: Document custom properties in MOC notes

## Property Suggestions

Obsidian auto-suggests property names from existing notes. Type-ahead appears when adding properties in Properties view or frontmatter.

## Accessing Properties

### Via Templater
```markdown
<% tp.frontmatter.property-name %>
<% tp.frontmatter["property-with-dashes"] %>
```

### Via Dataview
```markdown
`= this.property-name`
`= this["property with spaces"]`
```

### Via JavaScript
```javascript
const file = app.vault.getAbstractFileByPath("path/to/note.md");
const cache = app.metadataCache.getFileCache(file);
const frontmatter = cache?.frontmatter;
const propertyValue = frontmatter?.["property-name"];
```

## References

- Properties docs: https://help.obsidian.md/properties
- YAML spec: https://yaml.org/spec/
- Property types: https://help.obsidian.md/properties#Property%20types
