"""Graph analytics and multi-dimensional navigation utilities."""

from typing import List, Dict, Set
from scripts.utils.ontology import Ontology, OntologyNode, OntologyEdge


class GraphNavigator:
    """Multi-dimensional navigation for ontology graphs."""

    def __init__(self, ontology: Ontology):
        """Initialize navigator with an ontology."""
        self.ontology = ontology

    def get_dimensions(self) -> List[str]:
        """Get all unique dimensions in the ontology."""
        dimensions = set()
        for edge in self.ontology.edges:
            if edge.dimension:
                dimensions.add(edge.dimension)
        return sorted(dimensions)

    def filter_by_dimension(self, dimension: str) -> List[OntologyEdge]:
        """Get all edges in a specific dimension."""
        return [e for e in self.ontology.edges if e.dimension == dimension]

    def add_temporal_dimension(self) -> None:
        """Add temporal dimension edges based on node order/sequence."""
        # Find nodes with sequence/index properties
        ordered_nodes = []
        for node in self.ontology.nodes.values():
            if "index" in node.properties or "sequence" in node.properties:
                order = node.properties.get("index", node.properties.get("sequence", 0))
                ordered_nodes.append((order, node))

        # Sort by order
        ordered_nodes.sort(key=lambda x: x[0])

        # Add temporal edges
        for i in range(len(ordered_nodes) - 1):
            current = ordered_nodes[i][1]
            next_node = ordered_nodes[i + 1][1]

            edge = OntologyEdge(
                source_id=current.id,
                target_id=next_node.id,
                edge_type="precedes",
                dimension="temporal",
                inferred=True,
                strength=1.0
            )
            self.ontology.add_edge(edge)

    def add_conceptual_dimension(self) -> None:
        """Add conceptual dimension edges based on abstraction levels."""
        nodes_by_depth = {}
        for node in self.ontology.nodes.values():
            if node.depth not in nodes_by_depth:
                nodes_by_depth[node.depth] = []
            nodes_by_depth[node.depth].append(node)

        # Connect nodes at same depth (peer relationships)
        for depth, nodes in nodes_by_depth.items():
            if depth == 0:  # Skip root
                continue

            for i, node_a in enumerate(nodes):
                for node_b in nodes[i+1:]:
                    # Only connect if they share semantic similarity
                    if self._are_conceptually_related(node_a, node_b):
                        edge = OntologyEdge(
                            source_id=node_a.id,
                            target_id=node_b.id,
                            edge_type="peer_of",
                            dimension="conceptual",
                            inferred=True,
                            strength=0.6
                        )
                        self.ontology.add_edge(edge)

    def add_functional_dimension(self) -> None:
        """Add functional dimension edges based on purpose/role."""
        # Group nodes by entity_type property
        type_groups: Dict[str, List[OntologyNode]] = {}

        for node in self.ontology.nodes.values():
            entity_type = node.properties.get("entity_type")
            if entity_type:
                if entity_type not in type_groups:
                    type_groups[entity_type] = []
                type_groups[entity_type].append(node)

        # Connect nodes within same functional group
        for entity_type, nodes in type_groups.items():
            if len(nodes) < 2:
                continue

            for i, node_a in enumerate(nodes):
                for node_b in nodes[i+1:]:
                    edge = OntologyEdge(
                        source_id=node_a.id,
                        target_id=node_b.id,
                        edge_type="functionally_similar",
                        dimension="functional",
                        inferred=True,
                        strength=0.7
                    )
                    self.ontology.add_edge(edge)

    def _are_conceptually_related(self, node_a: OntologyNode, node_b: OntologyNode) -> bool:
        """Check if nodes are conceptually related (same stem or similar labels)."""
        if node_a.stem and node_b.stem and node_a.stem == node_b.stem:
            return True

        # Check label similarity
        words_a = set(node_a.label.lower().split())
        words_b = set(node_b.label.lower().split())

        if words_a & words_b:  # Any word overlap
            return True

        return False

    def get_navigation_paths(self, start_id: str, end_id: str,
                            dimension: str = None) -> List[List[str]]:
        """Find all paths between two nodes, optionally filtered by dimension.

        Args:
            start_id: Starting node ID
            end_id: Target node ID
            dimension: Optional dimension filter

        Returns:
            List of paths, where each path is a list of node IDs
        """
        if start_id not in self.ontology.nodes or end_id not in self.ontology.nodes:
            return []

        # Build adjacency list
        adj = {}
        for edge in self.ontology.edges:
            if dimension and edge.dimension != dimension:
                continue

            if edge.source_id not in adj:
                adj[edge.source_id] = []
            adj[edge.source_id].append(edge.target_id)

        # DFS to find all paths
        paths = []
        visited = set()

        def dfs(current: str, path: List[str]):
            if current == end_id:
                paths.append(path.copy())
                return

            visited.add(current)

            if current in adj:
                for neighbor in adj[current]:
                    if neighbor not in visited:
                        path.append(neighbor)
                        dfs(neighbor, path)
                        path.pop()

            visited.remove(current)

        dfs(start_id, [start_id])
        return paths

    def get_dimension_summary(self) -> Dict[str, int]:
        """Get count of edges per dimension."""
        summary = {}
        for edge in self.ontology.edges:
            dim = edge.dimension or "hierarchical"
            summary[dim] = summary.get(dim, 0) + 1
        return summary

    def enrich_with_all_dimensions(self) -> None:
        """Add all dimension types to the ontology."""
        self.add_temporal_dimension()
        self.add_conceptual_dimension()
        self.add_functional_dimension()

        # Update ontology dimensions list
        self.ontology.dimensions = self.get_dimensions()


class GraphMetrics:
    """Calculate graph-theoretic metrics for ontologies."""

    @staticmethod
    def calculate_centrality(ontology: Ontology) -> Dict[str, float]:
        """Calculate degree centrality for each node."""
        centrality = {}

        for node_id in ontology.nodes:
            # Count incoming and outgoing edges
            degree = 0
            for edge in ontology.edges:
                if edge.source_id == node_id or edge.target_id == node_id:
                    degree += 1

            # Also count hierarchical children
            node = ontology.nodes[node_id]
            degree += len(node.children)

            centrality[node_id] = degree

        # Normalize
        max_degree = max(centrality.values()) if centrality else 1
        for node_id in centrality:
            centrality[node_id] /= max_degree

        return centrality

    @staticmethod
    def find_clusters(ontology: Ontology, min_cluster_size: int = 2) -> List[Set[str]]:
        """Find clusters of highly connected nodes."""
        # Simple clustering based on shared parent
        clusters = []
        parent_groups = {}

        for node in ontology.nodes.values():
            if node.parent_id:
                if node.parent_id not in parent_groups:
                    parent_groups[node.parent_id] = set()
                parent_groups[node.parent_id].add(node.id)

        for parent_id, children in parent_groups.items():
            if len(children) >= min_cluster_size:
                clusters.append(children)

        return clusters

    @staticmethod
    def calculate_depth_distribution(ontology: Ontology) -> Dict[int, int]:
        """Get distribution of nodes across depth levels."""
        distribution = {}

        for node in ontology.nodes.values():
            distribution[node.depth] = distribution.get(node.depth, 0) + 1

        return distribution
