# JSON Canvas Format Specification

Canvas files (`.canvas`) use the open JSON Canvas format for infinite canvas data.

## File Structure

```json
{
  "nodes": [],
  "edges": []
}
```

## Node Types

### Text Node
```json
{
  "id": "unique-id",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 250,
  "height": 60,
  "text": "Text content with **Markdown** support"
}
```

### File Node
```json
{
  "id": "unique-id",
  "type": "file",
  "file": "path/to/note.md",
  "x": 300,
  "y": 0,
  "width": 400,
  "height": 400
}
```

### Link Node
```json
{
  "id": "unique-id",
  "type": "link",
  "url": "https://example.com",
  "x": 750,
  "y": 0,
  "width": 400,
  "height": 400
}
```

### Group Node
```json
{
  "id": "unique-id",
  "type": "group",
  "x": 0,
  "y": 500,
  "width": 800,
  "height": 600,
  "label": "Group Label",
  "background": "#ffffff",
  "backgroundStyle": "solid"
}
```

## Node Properties

### Required
- `id` (string) - Unique identifier
- `type` (string) - Node type: "text", "file", "link", or "group"
- `x` (number) - X coordinate
- `y` (number) - Y coordinate
- `width` (number) - Width in pixels
- `height` (number) - Height in pixels

### Type-Specific
- **Text nodes:** `text` (string) - Markdown content
- **File nodes:** `file` (string) - Path to file
- **Link nodes:** `url` (string) - URL
- **Group nodes:** `label` (string), `background` (string), `backgroundStyle` (string)

### Optional
- `color` (string) - Node color (#hex format)

## Edges (Connections)

```json
{
  "id": "unique-edge-id",
  "fromNode": "source-node-id",
  "fromSide": "right",
  "fromEnd": "none",
  "toNode": "target-node-id",
  "toSide": "left",
  "toEnd": "arrow",
  "color": "1",
  "label": "Connection Label"
}
```

### Edge Properties

#### Required
- `id` (string) - Unique identifier
- `fromNode` (string) - Source node ID
- `toNode` (string) - Target node ID

#### Optional
- `fromSide` (string) - Side where edge starts: "top", "right", "bottom", "left"
- `toSide` (string) - Side where edge ends
- `fromEnd` (string) - Shape at start: "none" or "arrow"
- `toEnd` (string) - Shape at end: "none" or "arrow" (default: "arrow")
- `color` (string) - Edge color identifier
- `label` (string) - Label text for edge

## Complete Example

```json
{
  "nodes": [
    {
      "id": "text-1",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 250,
      "height": 100,
      "text": "# Main Idea\n\nThis is the central concept."
    },
    {
      "id": "file-1",
      "type": "file",
      "file": "Notes/Related Note.md",
      "x": 300,
      "y": 0,
      "width": 400,
      "height": 400
    },
    {
      "id": "link-1",
      "type": "link",
      "url": "https://jsoncanvas.org",
      "x": 750,
      "y": 0,
      "width": 400,
      "height": 300
    },
    {
      "id": "group-1",
      "type": "group",
      "x": -50,
      "y": -50,
      "width": 1250,
      "height": 500,
      "label": "Project Overview"
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "fromNode": "text-1",
      "fromSide": "right",
      "toNode": "file-1",
      "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "edge-2",
      "fromNode": "file-1",
      "fromSide": "right",
      "toNode": "link-1",
      "toSide": "left",
      "label": "Learn more"
    }
  ]
}
```

## Z-Index Ordering

Nodes are placed in the array in ascending z-index order:
- First node: displayed below all others
- Last node: displayed on top

## Color Values

- Nodes: `color` accepts hex color codes (`#RRGGBB`)
- Edges: `color` accepts string identifiers ("0"-"6")

## Best Practices

1. Use descriptive IDs for nodes and edges
2. Place group nodes first in array for proper layering
3. Use consistent sizing for similar node types
4. Leverage labels for edge annotations
5. Keep related nodes within groups

## References

- Official spec: https://github.com/obsidianmd/jsoncanvas/blob/main/spec/1.0.md
- Website: https://jsoncanvas.org
- License: MIT (open source)
