---
name: obsidian-canvas
description: This skill should be used when the user asks to "create a canvas file", "add nodes to canvas", "create a mind map", "build a flowchart", "create visual diagrams", or when working with .canvas files.
user-invocable: false
---

# JSON Canvas

## Directory Index

**References:**
- [references/spec-overview.md](references/spec-overview.md)
- [references/nodes.md](references/nodes.md)
- [references/edges.md](references/edges.md)
- [references/colors-and-layout.md](references/colors-and-layout.md)
- [references/validation-rules.md](references/validation-rules.md)

**Examples:** [examples/simple-mindmap.canvas](examples/simple-mindmap.canvas) | [examples/project-board.canvas](examples/project-board.canvas) | [examples/research-canvas.canvas](examples/research-canvas.canvas) | [examples/flowchart.canvas](examples/flowchart.canvas)

**Templates:** [templates/blank-canvas.canvas](templates/blank-canvas.canvas) | [templates/brainstorm.canvas](templates/brainstorm.canvas) | [templates/meeting-canvas.canvas](templates/meeting-canvas.canvas)

---

Create and edit Obsidian `.canvas` files following JSON Canvas Spec 1.0.

## Quick Reference

| Feature | Description |
|---------|-------------|
| File format | `.canvas` (JSON) |
| Structure | `{ "nodes": [], "edges": [] }` |
| Node types | `text`, `file`, `link`, `group` |
| Edge ends | `none`, `arrow` |
| Colors | `"1"`-`"6"` or hex `"#FF0000"` |

## Minimal Structure

```json
{
  "nodes": [
    {
      "id": "a1b2c3d4e5f67890",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 300,
      "height": 150,
      "text": "# Hello World"
    }
  ],
  "edges": []
}
```

## Node Types

### Text Node
```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "text",
  "x": 0, "y": 0,
  "width": 300, "height": 150,
  "text": "# Markdown content"
}
```

### File Node
```json
{
  "id": "b2c3d4e5f6789012",
  "type": "file",
  "x": 400, "y": 0,
  "width": 300, "height": 200,
  "file": "Notes/My Note.md",
  "subpath": "#Section"
}
```

### Link Node
```json
{
  "id": "c3d4e5f678901234",
  "type": "link",
  "x": 800, "y": 0,
  "width": 300, "height": 150,
  "url": "https://example.com"
}
```

### Group Node
```json
{
  "id": "d4e5f6789012345a",
  "type": "group",
  "x": -50, "y": -50,
  "width": 500, "height": 400,
  "label": "My Group",
  "color": "4"
}
```

## Edges

```json
{
  "id": "e5f67890123456ab",
  "fromNode": "a1b2c3d4e5f67890",
  "fromSide": "right",
  "toNode": "b2c3d4e5f6789012",
  "toSide": "left",
  "toEnd": "arrow",
  "label": "connects to"
}
```

**Sides**: `top`, `right`, `bottom`, `left`
**Ends**: `none` (default for fromEnd), `arrow` (default for toEnd)

## Colors

| Preset | Color |
|--------|-------|
| `"1"` | Red |
| `"2"` | Orange |
| `"3"` | Yellow |
| `"4"` | Green |
| `"5"` | Cyan |
| `"6"` | Purple |

Or use hex: `"#FF5733"`

## Detailed Documentation

For comprehensive syntax, see:

- [Spec Overview](references/spec-overview.md) - File structure and concepts
- [Nodes](references/nodes.md) - All node types and attributes
- [Edges](references/edges.md) - Edge attributes and sides
- [Colors & Layout](references/colors-and-layout.md) - Positioning and sizing
- [Validation Rules](references/validation-rules.md) - ID format and rules

## Examples

Working `.canvas` files you can copy:

- [Simple Mindmap](examples/simple-mindmap.canvas) - Text nodes with connections
- [Project Board](examples/project-board.canvas) - Groups as kanban columns
- [Research Canvas](examples/research-canvas.canvas) - Files, links, and notes
- [Flowchart](examples/flowchart.canvas) - Decision flow with branches

## Templates

Starter templates to customize:

- [Blank Canvas](templates/blank-canvas.canvas) - Empty starting point
- [Brainstorm](templates/brainstorm.canvas) - Central idea with branches
- [Meeting Canvas](templates/meeting-canvas.canvas) - Meeting planning layout

## References

- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/)
- [JSON Canvas GitHub](https://github.com/obsidianmd/jsoncanvas)

## Memory Integration

This subskill contributes to the [Obsidian skill's](../SKILL.md) self-iterative memory:

- **Tracked patterns**: textNodes, fileNodes, linkNodes, groupNodes, edges
- **Memory location**: `.claude/obsidian-memory.json`
- **Learning**: Your frequently used patterns inform future suggestions

[← Back to Obsidian Skill](../SKILL.md)
