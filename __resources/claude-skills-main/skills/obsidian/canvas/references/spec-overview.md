---
name: spec-overview
description: JSON Canvas 1.0 specification overview including file structure, top-level properties, and format requirements.
---

# JSON Canvas Specification Overview

## Overview

JSON Canvas is an open file format for infinite canvas data. Canvas files use the `.canvas` extension and contain valid JSON following the [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/).

## File Structure

A canvas file contains two top-level arrays:

```json
{
  "nodes": [],
  "edges": []
}
```

- `nodes` (optional): Array of node objects
- `edges` (optional): Array of edge objects connecting nodes

## Node Types

There are four node types in JSON Canvas:

- `text` - Text content with Markdown
- `file` - Reference to files/attachments
- `link` - External URL
- `group` - Visual container for other nodes

## References

- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/)
- [JSON Canvas GitHub](https://github.com/obsidianmd/jsoncanvas)

[← Back to JSON Canvas](../SKILL.md)
