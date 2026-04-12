---
created: 2025-01-05
tags: [reference, templates, jinja2, layer4]
purpose: Template variable and filter reference for output generation
---

# Template Syntax Reference

Jinja2 template variables and filters for custom output formats.

## Available Variables

### Ontology Metadata

```jinja2
{{ metadata.timestamp }}        # ISO 8601 timestamp
{{ metadata.mode }}             # "fractal" or "free"
{{ metadata.source_type }}      # "text", "json", "markdown", etc.
{{ metadata.source_file }}      # Input file path
{{ metadata.topology_score }}   # Edge-to-node ratio (float)
{{ metadata.processing_time }}  # Processing time in ms
```

### Root Node

```jinja2
{{ root.id }}           # Root node ID
{{ root.label }}        # Root node label
{{ root.description }}  # Root description
{{ root.aliases }}      # List of aliases
{{ root.properties }}   # Dictionary of properties
```

### Node Collections

```jinja2
{{ nodes }}             # Dictionary: node_id -> OntologyNode
{{ nodes_sorted }}      # List of nodes sorted by depth, label
{{ edges }}             # List of OntologyEdge objects
{{ hierarchical_edges }}  # Edges with type "parent_of", "contains", "has_property"
```

### Computed Data

```jinja2
{{ tags }}              # Sorted list of unique tags
{{ node_relationships }}  # Dict: node_id -> list of outgoing edges
{{ dimensions }}        # List of navigation dimensions
```

## Jinja2 Filters

### Built-in Filters

```jinja2
{{ items | length }}              # Count items
{{ items | join(', ') }}          # Join list with separator
{{ items | sort }}                # Sort items
{{ items | first }}               # First item
{{ items | last }}                # Last item
{{ "%.2f" | format(value) }}      # Format float to 2 decimals
```

### Custom Filters

```jinja2
{{ edge.edge_type | replace('_', ' ') }}  # "part_of" → "part of"
```

## Control Flow

### Loops

```jinja2
{% for node in nodes_sorted %}
### {{ node.label }}

{{ node.description }}

{% endfor %}
```

### Conditionals

```jinja2
{% if node.description %}
> [!info] Description
> {{ node.description }}
{% endif %}

{% if node.properties %}
**Properties:**
{% for key, value in node.properties.items() %}
- `{{ key }}`: {{ value }}
{% endfor %}
{% endif %}
```

## Template Blocks

### YAML Frontmatter

```jinja2
---
created: {{ metadata.timestamp }}
{% if tags %}tags: [{{ tags | join(', ') }}]{% endif %}
ontology_type: {{ metadata.mode }}
{% if root.aliases %}aliases: [{{ root.aliases | join(', ') }}]{% endif %}
---
```

### Mermaid Diagram

```jinja2
```mermaid
graph TD
{% for edge in hierarchical_edges %}
    {{ edge.source_id }}["{{ nodes[edge.source_id].label }}"]
    {{ edge.target_id }}["{{ nodes[edge.target_id].label }}"]
    {{ edge.source_id }} --> {{ edge.target_id }}
    class {{ edge.source_id }},{{ edge.target_id }} internal-link
{% endfor %}
```
```

### Property Table

```jinja2
| Property | Value |
|----------|-------|
{% for key, value in node.properties.items() %}
| {{ key }} | {{ value }} |
{% endfor %}
```

### Inherited Properties

```jinja2
{% if node.inherited_properties %}
**Inherited:**
{% for key, info in node.inherited_properties.items() %}
- `{{ key }}`: {{ info.value }} (from [[{{ nodes[info.from].label }}]])
{% endfor %}
{% endif %}
```

## Creating New Templates

### JSON-LD Template Example

Create `config/templates/jsonld.json.j2`:

```jinja2
{
  "@context": {
    "@vocab": "http://schema.org/",
    "ontology": "http://example.org/ontology#"
  },
  "@graph": [
{% for node in nodes_sorted %}
    {
      "@id": "ontology:{{ node.id }}",
      "@type": "{{ node.node_type | title }}",
      "name": "{{ node.label }}",
      {% if node.description %}"description": "{{ node.description }}",{% endif %}
      {% if node.parent_id %}"partOf": {"@id": "ontology:{{ node.parent_id }}"},{% endif %}
      "properties": {{ node.properties | tojson }}
    }{% if not loop.last %},{% endif %}
{% endfor %}
  ]
}
```

### Cypher Template Example

Create `config/templates/cypher.cypher.j2`:

```jinja2
// Create nodes
{% for node in nodes_sorted %}
CREATE ({{ node.id }}:{{ node.node_type | title }} {
    id: "{{ node.id }}",
    label: "{{ node.label }}",
    depth: {{ node.depth }}
    {% if node.description %}, description: "{{ node.description }}"{% endif %}
})
{% endfor %}

// Create relationships
{% for edge in edges %}
MATCH (src {id: "{{ edge.source_id }}"}), (tgt {id: "{{ edge.target_id }}"})
CREATE (src)-[:{{ edge.edge_type | upper }}]->(tgt)
{% endfor %}
```

## Related

- [[ast-parsing-guide|AST Parsing Guide]]
- [[semantic-patterns|Semantic Patterns]]
