# Templater Plugin Syntax Reference

Templater is a community plugin providing advanced templating capabilities beyond core Templates plugin.

## Basic Syntax

### Simple Commands
```markdown
<% tp.function() %>
```

### JavaScript Execution Commands
```markdown
<%* JavaScript code here %>
```

### Display Commands
```markdown
<%= expression %>
```

## Command Delimiters

- `<%` and `%>` - Simple syntax commands
- `<%*` and `%>` - Complex JavaScript code blocks
- `<%=` and `%>` - Expression display (outputs result)

## Core Functions (tp object)

All Templater functions are available under the `tp` object.

### Date Functions

```markdown
<% tp.date.now("YYYY-MM-DD") %>
<% tp.date.now("HH:mm") %>
<% tp.date.tomorrow("YYYY-MM-DD") %>
<% tp.date.yesterday("YYYY-MM-DD") %>
<% tp.date.weekday("YYYY-MM-DD", 0) %>
```

**Format tokens:** Moment.js format (YYYY, MM, DD, HH, mm, ss, etc.)

### File Functions

```markdown
<% tp.file.title %>
<% tp.file.content %>
<% tp.file.creation_date("YYYY-MM-DD") %>
<% tp.file.last_modified_date("YYYY-MM-DD") %>
<% tp.file.folder() %>
<% tp.file.path() %>
<% tp.file.tags %>
```

### File Operations

```markdown
<%* await tp.file.create_new("Note Name", "folder/path") %>
<%* await tp.file.move("new/path") %>
<%* await tp.file.rename("New Name") %>
```

### Web Functions

```markdown
<% tp.web.daily_quote() %>
<% tp.web.random_picture() %>
```

### System Functions

```markdown
<% tp.system.clipboard() %>
<% tp.system.prompt("Enter value") %>
<% tp.system.suggester(["Option 1", "Option 2"], ["value1", "value2"]) %>
```

### Frontmatter Functions

```markdown
<% tp.frontmatter.property_name %>
<%* tp.frontmatter["property-with-dashes"] %>
```

### Config Functions

```markdown
<% tp.config.active_file %>
<% tp.config.target_file %>
<% tp.config.run_mode %>
```

## Examples

### Daily Note Template
```markdown
---
created: <% tp.file.creation_date("YYYY-MM-DD") %>
tags: daily-note
---

# <% tp.date.now("dddd, MMMM DD, YYYY") %>

## Tasks
- [ ]

## Notes

## References
- [[<% tp.date.yesterday("YYYY-MM-DD") %>]] ← Yesterday
- [[<% tp.date.tomorrow("YYYY-MM-DD") %>]] → Tomorrow
```

### Meeting Note Template
```markdown
---
type: meeting
date: <% tp.date.now("YYYY-MM-DD") %>
attendees: <% await tp.system.prompt("Attendees (comma-separated)") %>
---

# Meeting: <% tp.file.title %>

**Date:** <% tp.date.now("YYYY-MM-DD HH:mm") %>
**Attendees:** <% tp.frontmatter.attendees %>

## Agenda

## Notes

## Action Items
- [ ]
```

### Book Note Template
```markdown
---
type: book
title: <% await tp.system.prompt("Book title") %>
author: <% await tp.system.prompt("Author") %>
status: reading
rating:
---

# <% tp.frontmatter.title %>

**Author:** <% tp.frontmatter.author %>
**Status:** <% tp.frontmatter.status %>

## Summary

## Key Takeaways

## Quotes

## Notes
```

### JavaScript Execution
```markdown
<%*
const files = app.vault.getMarkdownFiles();
const recent = files
    .sort((a, b) => b.stat.mtime - a.stat.mtime)
    .slice(0, 5);

for (let file of recent) {
    tR += `- [[${file.basename}]]\n`;
}
%>
```

### Conditional Logic
```markdown
<%*
const status = tp.frontmatter.status;
if (status === "completed") {
    tR += "✅ Task completed!";
} else {
    tR += "⏳ In progress...";
}
%>
```

## User Functions

Create custom functions in Templater settings under "User Script Functions":

```javascript
// In user script file
function customGreeting(name) {
    return `Hello, ${name}!`;
}

module.exports = customGreeting;
```

```markdown
<% tp.user.customGreeting("World") %>
```

## Execution Commands

```markdown
<%* tp.file.cursor() %> // Set cursor position
<%* tp.file.cursor_append("text") %> // Append at cursor
```

## Documentation

Official docs: https://silentvoid13.github.io/Templater/
GitHub: https://github.com/SilentVoid13/Templater
