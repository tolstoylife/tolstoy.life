---
name: colors-and-layout
description: Color presets, hex colors, coordinate system, and layout algorithms for JSON Canvas positioning.
---

# JSON Canvas Colors and Layout Reference

## Colors

The `canvasColor` type can be specified in two ways:

### Hex Colors

```json
{
  "color": "#FF0000"
}
```

### Preset Colors

```json
{
  "color": "1"
}
```

| Preset | Color |
|--------|-------|
| `"1"` | Red |
| `"2"` | Orange |
| `"3"` | Yellow |
| `"4"` | Green |
| `"5"` | Cyan |
| `"6"` | Purple |

Note: Specific color values for presets are intentionally undefined, allowing applications to use their own brand colors.

## Layout Guidelines

### Positioning

- Coordinates can be negative (canvas extends infinitely)
- `x` increases to the right
- `y` increases downward
- Position refers to top-left corner of node

### Recommended Sizes

| Node Type | Suggested Width | Suggested Height |
|-----------|-----------------|------------------|
| Small text | 200-300 | 80-150 |
| Medium text | 300-450 | 150-300 |
| Large text | 400-600 | 300-500 |
| File preview | 300-500 | 200-400 |
| Link preview | 250-400 | 100-200 |
| Group | Varies | Varies |

### Spacing

- Leave 20-50px padding inside groups
- Space nodes 50-100px apart for readability
- Align nodes to grid (multiples of 10 or 20) for cleaner layouts

[← Back to JSON Canvas](../SKILL.md)
