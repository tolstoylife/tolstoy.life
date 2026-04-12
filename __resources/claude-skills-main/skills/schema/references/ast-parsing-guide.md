---
created: 2025-01-05
tags: [reference, ast, parsing, layer1]
purpose: Guide for extending AST parsing to new input formats
---

# AST Parsing Guide

Layer 1 structural extraction reference for adding new input adapters.

## Adapter Interface

All input adapters must implement:

```python
class InputAdapter:
    def parse(self, input_data: str) -> Ontology:
        """Parse input and return ontology structure."""
        pass
```

## Existing Adapters

### TextAdapter

**Purpose**: Parse plain text and markdown documents
**Location**: `scripts/adapters/input_text.py`

**Features**:
- Markdown heading detection (`# Header`)
- Hierarchical structure from heading levels
- Paragraph-based fallback for plain text
- Content extraction and truncation

**Usage**:
```python
from scripts.adapters.input_text import TextAdapter

adapter = TextAdapter()
ontology = adapter.parse("# Title\n\nContent here")
```

### JSONAdapter

**Purpose**: Extract structure from JSON data
**Location**: `scripts/adapters.input_json.py`

**Features**:
- Recursive object traversal
- Array handling with indexed children
- Primitive value nodes
- Property relationships

**Usage**:
```python
from scripts.adapters.input_json import JSONAdapter

adapter = JSONAdapter()
ontology = adapter.parse('{"key": "value"}')
```

## Node Creation Patterns

### Structural Node
```python
node = OntologyNode(
    id=f"struct_{counter}",
    label="Element Name",
    node_type="structural",
    depth=level,
    parent_id=parent_id,
    source_location=f"line:{line_number}"
)
```

### Semantic Node
```python
node = OntologyNode(
    id=f"semantic_{counter}",
    label="Concept Name",
    node_type="concept",
    depth=depth,
    stem=extract_stem(label),
    description="Semantic description"
)
```

### Value Node
```python
node = OntologyNode(
    id=f"value_{counter}",
    label=key,
    node_type="value",
    depth=depth,
    description=f"{type(value).__name__}: {value}"
)
node.add_property("value", value)
node.add_property("value_type", type(value).__name__)
```

## Edge Creation Patterns

### Hierarchical Edge
```python
edge = OntologyEdge(
    source_id=parent_id,
    target_id=child_id,
    edge_type="parent_of"
)
```

### Structural Edge
```python
edge = OntologyEdge(
    source_id=prev_id,
    target_id=next_id,
    edge_type="follows",
    properties={"sequence": index}
)
```

## Best Practices

1. **Always set metadata**: Include source type, timestamp
2. **Use consistent IDs**: Prefix with adapter name (`json_`, `text_`)
3. **Preserve source locations**: Track where data came from
4. **Handle errors gracefully**: Catch parse errors, provide fallbacks
5. **Add properties liberally**: Capture useful metadata
6. **Test edge cases**: Empty inputs, malformed data, deep nesting

## Performance Tips

- Limit description field to first 200 characters
- Use iterators for large inputs
- Cache computed values (stems, types)
- Batch edge creation

## Related

- [[semantic-patterns|Semantic Pattern Reference]]
- [[template-syntax|Template Syntax Reference]]
