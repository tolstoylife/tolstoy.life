---
type: moc
created: {{date:YYYY-MM-DD}}
modified: {{date:YYYY-MM-DD}}
tags:
  - moc
  - index
aliases:
  -
cssclasses:
  -
---

# 🗺️ {{title}}

> [!abstract] Map of Content
> This note serves as an index and navigation hub for the {{title}} domain.

## Overview

Brief description of this domain or topic area.

## Core Concepts

```dataview
LIST
FROM "folder/path"
WHERE type = "concept"
SORT file.name ASC
```

### Key Topics

| Topic | Description | Status |
|-------|-------------|--------|
| [[Topic 1]] | Brief description | ✅ |
| [[Topic 2]] | Brief description | 🔄 |
| [[Topic 3]] | Brief description | 📝 |

## Structure

```mermaid
graph TD
    A[{{title}}]
    A --> B[Subtopic 1]
    A --> C[Subtopic 2]
    A --> D[Subtopic 3]
    B --> E[Detail 1]
    B --> F[Detail 2]
    C --> G[Detail 3]

    class A,B,C,D,E,F,G internal-link;
```

## Resources

### Notes
- [[Note 1]]
- [[Note 2]]
- [[Note 3]]

### External Resources
- [Resource 1](https://example.com)
- [Resource 2](https://example.com)

## Related MOCs

- [[Related MOC 1]]
- [[Related MOC 2]]

## Statistics

```dataview
TABLE
  count(rows) AS "Notes",
  count(rows.file.tasks) AS "Tasks"
FROM "folder/path"
GROUP BY type
```

---

**Last Updated:** {{date:YYYY-MM-DD}}
**Total Notes:** `= length(file.inlinks)`
