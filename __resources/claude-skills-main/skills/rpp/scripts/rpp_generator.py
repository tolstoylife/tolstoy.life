#!/usr/bin/env python3
"""
RPP Generator - Core implementation of Recursive Pareto Principle graph generation.

Usage:
    python rpp_generator.py --corpus input.txt --domain "pharmacology" --output rpp_graph.json
"""

import json
import math
import argparse
from dataclasses import dataclass, field
from typing import Optional
from collections import defaultdict


@dataclass
class Node:
    """Graph node with level and metadata."""
    id: str
    level: int
    content: str
    semantic_weight: float = 1.0
    atomic: bool = False
    grounded_nodes: list = field(default_factory=list)
    
    def __hash__(self):
        return hash(self.id)


@dataclass
class Edge:
    """Graph edge with weight and type."""
    source: str
    target: str
    weight: float = 1.0
    edge_type: str = "vertical"  # vertical, horizontal, bridge


@dataclass
class Graph:
    """Simple graph implementation."""
    nodes: dict = field(default_factory=dict)
    edges: list = field(default_factory=list)
    
    def add_node(self, node: Node):
        self.nodes[node.id] = node
    
    def add_edge(self, source: str, target: str, weight: float = 1.0, edge_type: str = "vertical"):
        self.edges.append(Edge(source, target, weight, edge_type))
    
    def get_neighbors(self, node_id: str) -> list:
        neighbors = []
        for e in self.edges:
            if e.source == node_id:
                neighbors.append(e.target)
            elif e.target == node_id:
                neighbors.append(e.source)
        return neighbors
    
    def degree(self, node_id: str) -> int:
        return len(self.get_neighbors(node_id))


@dataclass
class RPPGraph:
    """Complete RPP graph with all four levels."""
    l0: Graph
    l1: Graph
    l2: Graph
    l3: Graph
    domain: str = ""
    
    @property
    def unified(self) -> Graph:
        """Return unified graph combining all levels."""
        unified = Graph()
        for level in [self.l0, self.l1, self.l2, self.l3]:
            for node in level.nodes.values():
                unified.add_node(node)
            for edge in level.edges:
                unified.edges.append(edge)
        return unified


class RPPGenerator:
    """
    Recursive Pareto Principle graph generator.
    
    Generates four-level hierarchical knowledge graphs where each level
    contains 80% fewer nodes while grounding 80% of the derivative content.
    """
    
    def __init__(self, domain: str = "", pareto_threshold: float = 0.8):
        self.domain = domain
        self.pareto_threshold = pareto_threshold
    
    def generate(self, corpus: str) -> RPPGraph:
        """
        Generate complete RPP graph from corpus.
        
        Args:
            corpus: Input text corpus
            
        Returns:
            RPPGraph with L0-L3 levels
        """
        # Extract L3 ground truth
        l3 = self.extract_l3(corpus)
        
        # Build L2 concepts via Pareto extraction
        l2 = self.construct_l2(l3)
        
        # Build L1 atomics via Pareto extraction
        l1 = self.construct_l1(l2)
        
        # Build L0 schema via abductive generalisation
        l0 = self.construct_l0(l1)
        
        # Add cross-level edges
        self._add_cross_level_edges(l0, l1, l2, l3)
        
        return RPPGraph(l0=l0, l1=l1, l2=l2, l3=l3, domain=self.domain)
    
    def extract_l3(self, corpus: str) -> Graph:
        """
        Extract ground truth detail graph from corpus.
        
        This is a simplified implementation - in production, use NLP
        for entity/relationship extraction.
        """
        l3 = Graph()
        
        # Split into statements
        statements = [s.strip() for s in corpus.split('\n') if s.strip()]
        
        # Create node for each statement
        for i, statement in enumerate(statements):
            node = Node(
                id=f"l3_{i}",
                level=3,
                content=statement,
                semantic_weight=1.0 / len(statements),
                atomic=False
            )
            l3.add_node(node)
        
        # Add edges between related statements (simple word overlap)
        for i, n1 in enumerate(l3.nodes.values()):
            for j, n2 in enumerate(l3.nodes.values()):
                if i < j:
                    overlap = self._compute_overlap(n1.content, n2.content)
                    if overlap > 0.2:
                        l3.add_edge(n1.id, n2.id, weight=overlap, edge_type="horizontal")
        
        return l3
    
    def construct_l2(self, l3: Graph) -> Graph:
        """
        Construct L2 concept graph via Pareto extraction.
        
        Target: 20% of L3 nodes grounding 80% of content.
        """
        l2 = Graph()
        
        # Compute importance scores
        importance = self._compute_importance(l3)
        
        # Sort by importance
        sorted_nodes = sorted(
            l3.nodes.values(),
            key=lambda n: importance.get(n.id, 0),
            reverse=True
        )
        
        # Select top nodes by Pareto criterion
        target_count = max(1, int(len(l3.nodes) * 0.2))
        selected = sorted_nodes[:target_count]
        
        # Create L2 nodes
        for i, l3_node in enumerate(selected):
            node = Node(
                id=f"l2_{i}",
                level=2,
                content=f"Concept: {l3_node.content[:50]}...",
                semantic_weight=importance.get(l3_node.id, 0),
                atomic=False,
                grounded_nodes=[l3_node.id]
            )
            l2.add_node(node)
        
        # Add edges between L2 nodes
        l2_list = list(l2.nodes.values())
        for i, n1 in enumerate(l2_list):
            for j, n2 in enumerate(l2_list):
                if i < j:
                    # Edge if grounded L3 nodes are connected
                    if self._are_grounded_connected(n1, n2, l3):
                        l2.add_edge(n1.id, n2.id, weight=0.5, edge_type="horizontal")
        
        return l2
    
    def construct_l1(self, l2: Graph) -> Graph:
        """
        Construct L1 atomic principles via Pareto extraction.
        
        Target: 4% of original L3 (20% of L2).
        """
        l1 = Graph()
        
        # Compute atomic scores
        atomic_scores = {}
        for node in l2.nodes.values():
            # Higher score for nodes with more connections (more explanatory)
            connections = l2.degree(node.id)
            atomic_scores[node.id] = connections * node.semantic_weight
        
        # Select top atomics
        target_count = max(1, int(len(l2.nodes) * 0.2))
        sorted_nodes = sorted(
            l2.nodes.values(),
            key=lambda n: atomic_scores.get(n.id, 0),
            reverse=True
        )
        selected = sorted_nodes[:target_count]
        
        # Create L1 nodes
        for i, l2_node in enumerate(selected):
            node = Node(
                id=f"l1_{i}",
                level=1,
                content=f"Principle: {l2_node.content[:30]}",
                semantic_weight=atomic_scores.get(l2_node.id, 0),
                atomic=True,
                grounded_nodes=[l2_node.id]
            )
            l1.add_node(node)
        
        # Add edges between L1 nodes
        l1_list = list(l1.nodes.values())
        for i, n1 in enumerate(l1_list):
            for j, n2 in enumerate(l1_list):
                if i < j:
                    l1.add_edge(n1.id, n2.id, weight=0.5, edge_type="horizontal")
        
        return l1
    
    def construct_l0(self, l1: Graph) -> Graph:
        """
        Construct L0 schema via abductive generalisation.
        
        Target: 0.8% of original L3 (20% of L1).
        """
        l0 = Graph()
        
        # For small L1, may only have 1 L0 node
        target_count = max(1, int(len(l1.nodes) * 0.2))
        
        # Generalise L1 principles into schema elements
        l1_list = list(l1.nodes.values())
        
        for i in range(target_count):
            # Each L0 node subsumes multiple L1 nodes
            start_idx = i * (len(l1_list) // target_count)
            end_idx = min((i + 1) * (len(l1_list) // target_count), len(l1_list))
            subsumed = l1_list[start_idx:end_idx] if start_idx < len(l1_list) else l1_list
            
            node = Node(
                id=f"l0_{i}",
                level=0,
                content=f"Schema: {self.domain}",
                semantic_weight=1.0 / target_count,
                atomic=False,
                grounded_nodes=[n.id for n in subsumed]
            )
            l0.add_node(node)
        
        return l0
    
    def _add_cross_level_edges(self, l0: Graph, l1: Graph, l2: Graph, l3: Graph):
        """Add vertical edges between levels."""
        # L0 → L1
        for l0_node in l0.nodes.values():
            for l1_id in l0_node.grounded_nodes:
                if l1_id in l1.nodes:
                    l0.add_edge(l0_node.id, l1_id, weight=1.0, edge_type="vertical")
        
        # L1 → L2
        for l1_node in l1.nodes.values():
            for l2_id in l1_node.grounded_nodes:
                if l2_id in l2.nodes:
                    l1.add_edge(l1_node.id, l2_id, weight=1.0, edge_type="vertical")
        
        # L2 → L3
        for l2_node in l2.nodes.values():
            for l3_id in l2_node.grounded_nodes:
                if l3_id in l3.nodes:
                    l2.add_edge(l2_node.id, l3_id, weight=1.0, edge_type="vertical")
    
    def _compute_importance(self, graph: Graph) -> dict:
        """Compute node importance scores (simplified PageRank)."""
        scores = {n: 1.0 / len(graph.nodes) for n in graph.nodes}
        
        # Simple iteration
        for _ in range(10):
            new_scores = {}
            for node_id in graph.nodes:
                neighbors = graph.get_neighbors(node_id)
                if neighbors:
                    new_scores[node_id] = 0.15 / len(graph.nodes) + 0.85 * sum(
                        scores.get(n, 0) / max(1, graph.degree(n))
                        for n in neighbors
                    )
                else:
                    new_scores[node_id] = scores[node_id]
            scores = new_scores
        
        return scores
    
    def _compute_overlap(self, text1: str, text2: str) -> float:
        """Compute word overlap between texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def _are_grounded_connected(self, n1: Node, n2: Node, l3: Graph) -> bool:
        """Check if grounded L3 nodes are connected."""
        for g1 in n1.grounded_nodes:
            for g2 in n2.grounded_nodes:
                if g1 in l3.get_neighbors(g2):
                    return True
        return False


def export_rpp_json(rpp: RPPGraph) -> dict:
    """Export RPP graph to JSON format."""
    def serialize_level(level: Graph, level_name: str) -> dict:
        return {
            "nodes": [
                {
                    "id": n.id,
                    "content": n.content,
                    "semantic_weight": n.semantic_weight,
                    "atomic": n.atomic,
                    "grounded_nodes": n.grounded_nodes
                }
                for n in level.nodes.values()
            ],
            "edges": [
                {
                    "source": e.source,
                    "target": e.target,
                    "weight": e.weight,
                    "type": e.edge_type
                }
                for e in level.edges
            ]
        }
    
    return {
        "metadata": {
            "domain": rpp.domain,
            "pareto_chain": [0.8, 0.64, 0.51],
            "node_counts": {
                "l0": len(rpp.l0.nodes),
                "l1": len(rpp.l1.nodes),
                "l2": len(rpp.l2.nodes),
                "l3": len(rpp.l3.nodes)
            }
        },
        "levels": {
            "l0": serialize_level(rpp.l0, "l0"),
            "l1": serialize_level(rpp.l1, "l1"),
            "l2": serialize_level(rpp.l2, "l2"),
            "l3": serialize_level(rpp.l3, "l3")
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Generate RPP graph from corpus")
    parser.add_argument("--corpus", required=True, help="Input corpus file")
    parser.add_argument("--domain", default="general", help="Domain name")
    parser.add_argument("--output", default="rpp_graph.json", help="Output JSON file")
    parser.add_argument("--pareto", type=float, default=0.8, help="Pareto threshold")
    
    args = parser.parse_args()
    
    # Read corpus
    with open(args.corpus, 'r') as f:
        corpus = f.read()
    
    # Generate RPP
    generator = RPPGenerator(domain=args.domain, pareto_threshold=args.pareto)
    rpp = generator.generate(corpus)
    
    # Export
    output = export_rpp_json(rpp)
    with open(args.output, 'w') as f:
        json.dump(output, f, indent=2)
    
    # Summary
    print(f"Generated RPP graph:")
    print(f"  L0 (schema): {len(rpp.l0.nodes)} nodes")
    print(f"  L1 (atomic): {len(rpp.l1.nodes)} nodes")
    print(f"  L2 (concept): {len(rpp.l2.nodes)} nodes")
    print(f"  L3 (detail): {len(rpp.l3.nodes)} nodes")
    print(f"  Output: {args.output}")


if __name__ == "__main__":
    main()
