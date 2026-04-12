---
name: properties
description: Property types for Obsidian Bases including note properties, file properties, and formula properties.
---

# Properties Reference

## Three Types of Properties

1. **Note properties** - From frontmatter: `note.author` or just `author`
2. **File properties** - File metadata: `file.name`, `file.mtime`, etc.
3. **Formula properties** - Computed values: `formula.my_formula`

## File Properties Reference

| Property | Type | Description |
|----------|------|-------------|
| `file.name` | String | File name |
| `file.basename` | String | File name without extension |
| `file.path` | String | Full path to file |
| `file.folder` | String | Parent folder path |
| `file.ext` | String | File extension |
| `file.size` | Number | File size in bytes |
| `file.ctime` | Date | Created time |
| `file.mtime` | Date | Modified time |
| `file.tags` | List | All tags in file |
| `file.links` | List | Internal links in file |
| `file.backlinks` | List | Files linking to this file |
| `file.embeds` | List | Embeds in the note |
| `file.properties` | Object | All frontmatter properties |

## The `this` Keyword

- In main content area: refers to the base file itself
- When embedded: refers to the embedding file
- In sidebar: refers to the active file in main content

## Property Configuration

Configure display names and settings for properties in the `properties` section:

```yaml
properties:
  # Regular property
  status:
    displayName: Status

  # Formula property
  formula.days_until_due:
    displayName: "Days Until Due"

  # File property
  file.ext:
    displayName: "Extension"
```

---

[← Back to Obsidian Bases](../SKILL.md)
