# Graph View API Reference

Programmatic access to Obsidian's Graph View for visualization and analysis.

## Overview

The Graph View in Obsidian visualizes connections between notes. While primarily a UI feature, we can interact with it programmatically via CDP for automation, customization, and data extraction.

## Accessing the Graph

### Opening Graph View

```javascript
// Open global graph
app.commands.executeCommandById('graph:open')

// Open local graph for current file
app.commands.executeCommandById('graph:open-local')
```

### Via SDK

```python
# Open global graph
await client.evaluate("app.commands.executeCommandById('graph:open')")

# Wait for graph to load
await asyncio.sleep(0.5)
```

## Graph Data Extraction

### Getting Graph Nodes

```javascript
// Access the graph view
const graphLeaf = app.workspace.getLeavesOfType('graph')[0];
const graphView = graphLeaf?.view;

if (graphView) {
    // Get rendered nodes
    const renderer = graphView.renderer;
    const nodes = Object.values(renderer.nodes);

    return nodes.map(n => ({
        id: n.id,
        x: n.x,
        y: n.y,
        links: n.links?.length || 0
    }));
}
```

### Getting Link Data

```javascript
// Extract all links from metadata cache
const links = [];
const files = app.vault.getMarkdownFiles();

for (const file of files) {
    const cache = app.metadataCache.getFileCache(file);
    if (cache?.links) {
        for (const link of cache.links) {
            links.push({
                source: file.path,
                target: link.link,
                displayText: link.displayText
            });
        }
    }
}

return links;
```

### Full Graph Export

```python
async def export_graph_data(sdk):
    """Export complete graph structure."""
    result = await client.evaluate("""
    (() => {
        const files = app.vault.getMarkdownFiles();
        const nodes = files.map(f => ({
            id: f.path,
            name: f.basename,
            folder: f.parent?.path || ''
        }));

        const edges = [];
        for (const file of files) {
            const cache = app.metadataCache.getFileCache(file);
            if (cache?.links) {
                for (const link of cache.links) {
                    const target = app.metadataCache.getFirstLinkpathDest(
                        link.link, file.path
                    );
                    if (target) {
                        edges.push({
                            source: file.path,
                            target: target.path
                        });
                    }
                }
            }
        }

        return { nodes, edges };
    })()
    """)
    return result
```

## Graph Configuration

### Reading Current Settings

```javascript
// Access graph settings
const graphLeaf = app.workspace.getLeavesOfType('graph')[0];
const settings = graphLeaf?.view?.dataEngine?.options;

return {
    showOrphans: settings?.showOrphans,
    showTags: settings?.showTags,
    showAttachments: settings?.showAttachments,
    colorGroups: settings?.colorGroups
};
```

### Modifying Display Options

```javascript
// Toggle orphan visibility
const graphLeaf = app.workspace.getLeavesOfType('graph')[0];
if (graphLeaf?.view?.dataEngine) {
    graphLeaf.view.dataEngine.options.showOrphans = false;
    graphLeaf.view.dataEngine.render();
}
```

## Graph Zoom Control

### Via MCP Tool

```python
# Use the built-in MCP tool
await mcp.obsidian_graph_zoom(level=1.5)  # 150% zoom
```

### Via SDK

```javascript
// Programmatic zoom
const graphLeaf = app.workspace.getLeavesOfType('graph')[0];
if (graphLeaf?.view?.renderer) {
    graphLeaf.view.renderer.zoomTo(1.0);  // 100%
}
```

## Color Groups

### Reading Color Groups

```javascript
const graphLeaf = app.workspace.getLeavesOfType('graph')[0];
const colorGroups = graphLeaf?.view?.dataEngine?.options?.colorGroups || [];

return colorGroups.map(g => ({
    query: g.query,
    color: g.color?.rgb
}));
```

### Setting Color Groups

```javascript
// Define color groups programmatically
const colorGroups = [
    { query: 'path:SAQ', color: { r: 255, g: 100, b: 100 } },
    { query: 'path:LO', color: { r: 100, g: 255, b: 100 } },
    { query: 'tag:#concept', color: { r: 100, g: 100, b: 255 } }
];

const graphLeaf = app.workspace.getLeavesOfType('graph')[0];
if (graphLeaf?.view?.dataEngine) {
    graphLeaf.view.dataEngine.options.colorGroups = colorGroups;
    graphLeaf.view.dataEngine.render();
}
```

## Network Analysis

### Calculating Degree Centrality

```python
async def calculate_degree_centrality(sdk):
    """Find most connected notes."""
    graph_data = await export_graph_data(sdk)

    # Count incoming and outgoing links
    degree = {}
    for edge in graph_data['edges']:
        degree[edge['source']] = degree.get(edge['source'], 0) + 1
        degree[edge['target']] = degree.get(edge['target'], 0) + 1

    # Sort by degree
    ranked = sorted(degree.items(), key=lambda x: x[1], reverse=True)
    return ranked[:20]  # Top 20
```

### Finding Orphan Notes

```python
async def find_orphans(sdk):
    """Find notes with no connections."""
    graph_data = await export_graph_data(sdk)

    connected = set()
    for edge in graph_data['edges']:
        connected.add(edge['source'])
        connected.add(edge['target'])

    all_nodes = {n['id'] for n in graph_data['nodes']}
    orphans = all_nodes - connected

    return list(orphans)
```

### Detecting Clusters

```python
async def detect_clusters(sdk, min_connections=3):
    """Find tightly connected note clusters."""
    graph_data = await export_graph_data(sdk)

    # Build adjacency list
    adj = {}
    for edge in graph_data['edges']:
        adj.setdefault(edge['source'], set()).add(edge['target'])
        adj.setdefault(edge['target'], set()).add(edge['source'])

    # Find nodes with high local connectivity
    clusters = []
    visited = set()

    for node in adj:
        if node in visited:
            continue
        if len(adj[node]) >= min_connections:
            cluster = {node}
            queue = list(adj[node])
            while queue:
                neighbor = queue.pop()
                if neighbor not in visited and len(adj.get(neighbor, [])) >= 2:
                    cluster.add(neighbor)
                    visited.add(neighbor)
            if len(cluster) >= 3:
                clusters.append(cluster)

    return clusters
```

## Integration with Breadcrumbs

### Overlaying Breadcrumbs Edges

```javascript
// Get breadcrumbs hierarchy data
const bc = app.plugins.plugins['breadcrumbs'];
if (bc) {
    const hierarchy = bc.mainG;  // Main graph
    const edges = [];

    for (const [source, targets] of hierarchy.entries()) {
        for (const [type, nodes] of Object.entries(targets)) {
            for (const target of nodes) {
                edges.push({
                    source: source,
                    target: target,
                    type: type  // e.g., 'parent', 'child', 'same'
                });
            }
        }
    }

    return edges;
}
```

## Export Formats

### GraphML Export

```python
async def export_graphml(sdk, output_path):
    """Export graph in GraphML format."""
    data = await export_graph_data(sdk)

    graphml = ['<?xml version="1.0" encoding="UTF-8"?>']
    graphml.append('<graphml xmlns="http://graphml.graphdrawing.org/xmlns">')
    graphml.append('<graph id="G" edgedefault="directed">')

    for node in data['nodes']:
        graphml.append(f'  <node id="{node["id"]}"/>')

    for i, edge in enumerate(data['edges']):
        graphml.append(
            f'  <edge id="e{i}" source="{edge["source"]}" target="{edge["target"]}"/>'
        )

    graphml.append('</graph>')
    graphml.append('</graphml>')

    with open(output_path, 'w') as f:
        f.write('\n'.join(graphml))
```

### JSON Export for Neo4j

```python
async def export_for_neo4j(sdk):
    """Export in format suitable for Neo4j import."""
    data = await export_graph_data(sdk)

    nodes_csv = ["id:ID,name,folder,:LABEL"]
    for n in data['nodes']:
        nodes_csv.append(f'"{n["id"]}","{n["name"]}","{n["folder"]}",Note')

    edges_csv = [":START_ID,:END_ID,:TYPE"]
    for e in data['edges']:
        edges_csv.append(f'"{e["source"]}","{e["target"]}",LINKS_TO')

    return {
        'nodes': '\n'.join(nodes_csv),
        'edges': '\n'.join(edges_csv)
    }
```

## Best Practices

1. **Wait for rendering**: Graph operations may need delays for UI updates
2. **Check for graph leaf**: Always verify graph view exists before operations
3. **Use metadata cache**: Faster than parsing files for link extraction
4. **Batch operations**: Export full graph data once, analyze locally
5. **Respect performance**: Large vaults may have slow graph operations

---

See also:
- [sdk-reference.md](sdk-reference.md) - Full SDK documentation
- [canvas-api.md](canvas-api.md) - Canvas creation
- [api-basics.md](api-basics.md) - Core API reference
