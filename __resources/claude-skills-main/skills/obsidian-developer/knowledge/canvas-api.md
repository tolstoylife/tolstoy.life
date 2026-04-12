# Canvas API Reference

Programmatic creation and manipulation of Obsidian Canvas files.

## Overview

Obsidian Canvas is a spatial note-taking feature that stores visual layouts as JSON files (`.canvas`). This reference covers programmatic canvas creation via the obsidian-devtools SDK.

## Canvas File Format

Canvas files are JSON with this structure:

```json
{
  "nodes": [
    {
      "id": "unique-id",
      "type": "text|file|link|group",
      "x": 0,
      "y": 0,
      "width": 400,
      "height": 200,
      // Type-specific properties...
    }
  ],
  "edges": [
    {
      "id": "edge-id",
      "fromNode": "node-id-1",
      "fromSide": "right",
      "toNode": "node-id-2",
      "toSide": "left",
      "color": "1"  // Optional
    }
  ]
}
```

## Node Types

### Text Node

Inline text content rendered as markdown.

```python
text_node = {
    "id": "text-1",
    "type": "text",
    "x": 0,
    "y": 0,
    "width": 400,
    "height": 200,
    "text": "# Heading\n\nMarkdown content here."
}
```

### File Node

Embed an existing vault file.

```python
file_node = {
    "id": "file-1",
    "type": "file",
    "x": 500,
    "y": 0,
    "width": 400,
    "height": 400,
    "file": "Notes/Example.md"  # Vault-relative path
}
```

### Link Node

Embed external web content.

```python
link_node = {
    "id": "link-1",
    "type": "link",
    "x": 1000,
    "y": 0,
    "width": 600,
    "height": 400,
    "url": "https://example.com"
}
```

### Group Node

Visual container for organizing other nodes.

```python
group_node = {
    "id": "group-1",
    "type": "group",
    "x": -50,
    "y": -50,
    "width": 1000,
    "height": 500,
    "label": "Concept Cluster"
}
```

## Edges

Edges connect nodes visually with arrows.

```python
edge = {
    "id": "edge-1",
    "fromNode": "text-1",
    "fromSide": "right",  # left, right, top, bottom
    "toNode": "file-1",
    "toSide": "left",
    "color": "1",         # Optional: 1-6 for preset colors
    "label": "relates to" # Optional: edge label
}
```

### Side Options

| Side | Position |
|------|----------|
| `left` | Left edge of node |
| `right` | Right edge of node |
| `top` | Top edge of node |
| `bottom` | Bottom edge of node |

### Color Presets

| Color | Value | Hex |
|-------|-------|-----|
| Red | `"1"` | #fb464c |
| Orange | `"2"` | #e9973f |
| Yellow | `"3"` | #e0de71 |
| Green | `"4"` | #44cf6e |
| Cyan | `"5"` | #53dfdd |
| Purple | `"6"` | #a882ff |

## SDK Methods

### Creating a Canvas

```python
from obsidian_devtools.sdk import ObsidianClient

# Define nodes
nodes = [
    {
        "id": "concept-1",
        "type": "text",
        "x": 0, "y": 0,
        "width": 300, "height": 150,
        "text": "# Core Concept\n\nMain idea here."
    },
    {
        "id": "related-1",
        "type": "file",
        "x": 400, "y": 0,
        "width": 300, "height": 200,
        "file": "Notes/RelatedTopic.md"
    }
]

# Define edges
edges = [
    {
        "id": "e1",
        "fromNode": "concept-1",
        "fromSide": "right",
        "toNode": "related-1",
        "toSide": "left"
    }
]

# Create canvas
await sdk.create_canvas("Diagrams/MyConcept.canvas", nodes, edges)
```

### Reading a Canvas

```python
canvas_data = await sdk.read_canvas("Diagrams/Existing.canvas")
print(f"Nodes: {len(canvas_data['nodes'])}")
print(f"Edges: {len(canvas_data['edges'])}")
```

### Adding Nodes Dynamically

```python
new_node = {
    "id": f"node-{uuid4()}",
    "type": "text",
    "x": 800, "y": 0,
    "width": 300, "height": 150,
    "text": "# Added Later\n\nDynamic content."
}

await sdk.add_canvas_node("Diagrams/MyConcept.canvas", new_node)
```

## Layout Algorithms

### Grid Layout

```python
def grid_layout(items, cols=3, spacing=50, node_width=300, node_height=200):
    """Arrange items in a grid pattern."""
    nodes = []
    for i, item in enumerate(items):
        row = i // cols
        col = i % cols
        nodes.append({
            "id": f"node-{i}",
            "type": "text",
            "x": col * (node_width + spacing),
            "y": row * (node_height + spacing),
            "width": node_width,
            "height": node_height,
            "text": item
        })
    return nodes
```

### Radial Layout

```python
import math

def radial_layout(center_text, items, radius=400, node_width=250, node_height=150):
    """Arrange items in a circle around a center node."""
    nodes = [{
        "id": "center",
        "type": "text",
        "x": 0, "y": 0,
        "width": node_width, "height": node_height,
        "text": center_text
    }]

    edges = []
    angle_step = 2 * math.pi / len(items)

    for i, item in enumerate(items):
        angle = i * angle_step
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        node_id = f"node-{i}"
        nodes.append({
            "id": node_id,
            "type": "text",
            "x": x, "y": y,
            "width": node_width, "height": node_height,
            "text": item
        })

        edges.append({
            "id": f"edge-{i}",
            "fromNode": "center",
            "fromSide": "right" if x > 0 else "left",
            "toNode": node_id,
            "toSide": "left" if x > 0 else "right"
        })

    return nodes, edges
```

### Hierarchical Layout

```python
def hierarchical_layout(root, children_map, level_height=300, node_spacing=50):
    """Arrange nodes in a tree hierarchy."""
    nodes = []
    edges = []

    def add_node(node_id, text, level, position):
        nodes.append({
            "id": node_id,
            "type": "text",
            "x": position * (300 + node_spacing),
            "y": level * level_height,
            "width": 300,
            "height": 150,
            "text": text
        })

    def traverse(node_id, level=0, position=0):
        add_node(node_id, node_id, level, position)
        children = children_map.get(node_id, [])
        for i, child in enumerate(children):
            child_pos = position + i - len(children) // 2
            traverse(child, level + 1, child_pos)
            edges.append({
                "id": f"e-{node_id}-{child}",
                "fromNode": node_id,
                "fromSide": "bottom",
                "toNode": child,
                "toSide": "top"
            })

    traverse(root)
    return nodes, edges
```

## Use Cases

### Concept Map from Wikilinks

```python
async def create_concept_map(file_path: str, output_canvas: str):
    """Generate a canvas from a file's outgoing links."""
    # Get the source file's links
    links = await sdk.get_links(file_path)

    # Create center node for source
    nodes = [{
        "id": "source",
        "type": "file",
        "x": 0, "y": 0,
        "width": 400, "height": 300,
        "file": file_path
    }]

    edges = []
    angle_step = 2 * math.pi / max(len(links), 1)

    for i, link in enumerate(links):
        angle = i * angle_step
        x = 500 * math.cos(angle)
        y = 500 * math.sin(angle)

        node_id = f"link-{i}"
        nodes.append({
            "id": node_id,
            "type": "file",
            "x": x, "y": y,
            "width": 300, "height": 200,
            "file": f"{link}.md"
        })

        edges.append({
            "id": f"e-{i}",
            "fromNode": "source",
            "fromSide": "right" if x > 0 else "left",
            "toNode": node_id,
            "toSide": "left" if x > 0 else "right"
        })

    await sdk.create_canvas(output_canvas, nodes, edges)
```

### SAQ Visualization

```python
async def visualize_saq(saq_path: str):
    """Create a canvas showing SAQ structure with concepts."""
    fm = await sdk.get_frontmatter(saq_path)

    nodes = [{
        "id": "saq",
        "type": "file",
        "x": 0, "y": 0,
        "width": 500, "height": 400,
        "file": saq_path
    }]

    edges = []
    concepts = fm.get("concept_direct", [])

    for i, concept in enumerate(concepts):
        nodes.append({
            "id": f"concept-{i}",
            "type": "file",
            "x": 600,
            "y": i * 220,
            "width": 300,
            "height": 200,
            "file": f"Concepts/{concept}.md"
        })
        edges.append({
            "id": f"e-{i}",
            "fromNode": "saq",
            "fromSide": "right",
            "toNode": f"concept-{i}",
            "toSide": "left",
            "color": "4"  # Green for concept links
        })

    output = saq_path.replace(".md", "-map.canvas")
    await sdk.create_canvas(output, nodes, edges)
```

## Best Practices

1. **Use unique IDs**: Generate with `uuid4()` or descriptive prefixes
2. **Calculate positions**: Use layout algorithms for clean arrangements
3. **Group related nodes**: Use group nodes for visual organization
4. **Consistent sizing**: Maintain uniform dimensions within groups
5. **Meaningful edges**: Use colors and labels for semantic edges

---

See also:
- [sdk-reference.md](sdk-reference.md) - Full SDK documentation
- [patterns/canvas-generator.js](../patterns/canvas-generator.js) - JavaScript patterns
