---
name: validation-rules
description: Validation requirements for JSON Canvas files including ID generation, required fields, and JSON structure rules.
---

# JSON Canvas Validation Rules

## ID Generation

Node and edge IDs must be unique strings. Obsidian generates 16-character hexadecimal IDs:

```json
"id": "6f0ad84f44ce9c17"
"id": "a3b2c1d0e9f8g7h6"
"id": "1234567890abcdef"
```

This format is a 16-character lowercase hex string (64-bit random value).

## Validation Rules

1. All `id` values must be unique across nodes and edges
2. `fromNode` and `toNode` must reference existing node IDs
3. Required fields must be present for each node type
4. `type` must be one of: `text`, `file`, `link`, `group`
5. `backgroundStyle` must be one of: `cover`, `ratio`, `repeat`
6. `fromSide`, `toSide` must be one of: `top`, `right`, `bottom`, `left`
7. `fromEnd`, `toEnd` must be one of: `none`, `arrow`
8. Color presets must be `"1"` through `"6"` or valid hex color

[← Back to JSON Canvas](../SKILL.md)
