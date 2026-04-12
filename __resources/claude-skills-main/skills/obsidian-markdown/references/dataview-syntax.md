# Dataview Query Syntax Reference

Dataview is a community plugin that enables data indexing and querying over Markdown files.

## Query Structure

```
<QUERY-TYPE> <fields>
FROM <source>
WHERE <condition>
SORT <field> [ASC|DESC]
LIMIT <number>
```

Only the QUERY-TYPE is mandatory.

## Query Types

### LIST Queries

Creates bullet point lists of pages matching the query.

```dataview
LIST
FROM "Projects"
WHERE status = "active"
```

```dataview
LIST file.ctime
FROM #meeting
SORT file.ctime DESC
```

### TABLE Queries

Output page data as tabular view with multiple metadata fields.

```dataview
TABLE started, file.folder, file.etags
FROM #games
SORT rating DESC
```

```dataview
TABLE rating AS "Rating", summary AS "Summary"
FROM #books
WHERE rating >= 4
```

### TASK Queries

Display tasks from matching pages.

```dataview
TASK
FROM "Projects"
WHERE !completed
```

### CALENDAR Queries

Display pages in calendar view.

```dataview
CALENDAR file.ctime
FROM "Daily Notes"
```

## Inline Queries

Inline queries use backticks with `=` prefix to display single values within text.

```markdown
Today is `= date(today)`
File name: `= this.file.name`
Modified: `= this.file.mtime`
Link data: `= [[Note]].property`
```

**Examples in text:**
- "I have `= length(file.tasks)` tasks remaining."
- "Last modified: `= this.file.mtime`"

## Common Fields

### File Properties
- `file.name` - File name without extension
- `file.path` - Full file path
- `file.folder` - Folder containing file
- `file.size` - File size in bytes
- `file.ctime` - Creation time
- `file.mtime` - Last modified time
- `file.tags` - Array of all tags
- `file.etags` - Array of explicit tags
- `file.inlinks` - Array of incoming links
- `file.outlinks` - Array of outgoing links
- `file.tasks` - Array of all tasks

### Custom Properties
Access any YAML frontmatter property directly: `property-name`

## Operators

### Comparison
- `=` or `==` (equal)
- `!=` (not equal)
- `>`, `>=`, `<`, `<=`
- `contains`

### Logical
- `AND` or `and` or `&`
- `OR` or `or` or `|`
- `NOT` or `!`

## Functions

### Date Functions
- `date(text)` - Parse date from text
- `date(today)` - Current date
- `dur(duration)` - Create duration

### List Functions
- `length(list)` - List length
- `sum(list)` - Sum of numbers
- `sort(list)` - Sort list
- `reverse(list)` - Reverse list

### String Functions
- `contains(text, pattern)` - Check if text contains pattern
- `lower(text)` - Convert to lowercase
- `upper(text)` - Convert to uppercase

## Examples

```dataview
LIST
FROM #project
WHERE status = "active" AND priority = "high"
SORT file.mtime DESC
LIMIT 10
```

```dataview
TABLE
  author,
  rating AS "★",
  summary AS "Summary"
FROM #books
WHERE rating >= 4
SORT rating DESC, author ASC
```

```markdown
Total books read: `= length(filter(file.lists.file, (f) => contains(f.tags, "#books")))`
```

## Documentation

Official docs: https://blacksmithgu.github.io/obsidian-dataview/
