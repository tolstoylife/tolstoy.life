---
name: edges
description: Edge syntax for JSON Canvas including connection attributes, sides, arrow types, and labels.
---

# JSON Canvas Edges Reference

Edges are lines connecting nodes.

## Basic Edge Example

```json
{
  "id": "f67890123456789a",
  "fromNode": "6f0ad84f44ce9c17",
  "toNode": "a1b2c3d4e5f67890"
}
```

## Full Edge Example

```json
{
  "id": "0123456789abcdef",
  "fromNode": "6f0ad84f44ce9c17",
  "fromSide": "right",
  "fromEnd": "none",
  "toNode": "b2c3d4e5f6789012",
  "toSide": "left",
  "toEnd": "arrow",
  "color": "1",
  "label": "leads to"
}
```

## Edge Attributes

| Attribute | Required | Type | Default | Description |
|-----------|----------|------|---------|-------------|
| `id` | Yes | string | - | Unique identifier for the edge |
| `fromNode` | Yes | string | - | Node ID where connection starts |
| `fromSide` | No | string | - | Side where edge starts |
| `fromEnd` | No | string | `none` | Shape at edge start |
| `toNode` | Yes | string | - | Node ID where connection ends |
| `toSide` | No | string | - | Side where edge ends |
| `toEnd` | No | string | `arrow` | Shape at edge end |
| `color` | No | canvasColor | - | Line color |
| `label` | No | string | - | Text label for the edge |

## Side Values

| Value | Description |
|-------|-------------|
| `top` | Top edge of node |
| `right` | Right edge of node |
| `bottom` | Bottom edge of node |
| `left` | Left edge of node |

## End Shapes

| Value | Description |
|-------|-------------|
| `none` | No endpoint shape |
| `arrow` | Arrow endpoint |

[← Back to JSON Canvas](../SKILL.md)
