#!/usr/bin/env python3
"""
Graph Topology Metrics for Knowledge Graph Quality Assessment

Computes structural metrics indicating:
- Graph density and connectivity (|E|/|V| ratio)
- Small-world properties (clustering coefficient, path length)
- Scale-invariance indicators (fractal dimension approximation)
- Compression potential (automorphism orbit count)

Target metrics for high-quality knowledge graphs:
- Edge-to-Node Ratio: ≥4:1 (enables emergence through dense connectivity)
- Isolation Rate: <20% (measures integration completeness)
- Clustering Coefficient: >0.3 (small-world property indicator)
- Average Path Length: Low relative to graph size

Usage:
    python topology_metrics.py graph.json --report
    python topology_metrics.py graph.json --compression-potential
"""

import json
import argparse
import math
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Any, Optional
from dataclasses import dataclass


@dataclass
class TopologyReport:
    """Comprehensive topology analysis results."""
    # Basic counts
    num_nodes: int
    num_edges: int
    
    # Density metrics
    edge_to_node_ratio: float
    density: float  # actual edges / possible edges
    
    # Connectivity metrics
    num_components: int
    largest_component_size: int
    isolated_nodes: int
    isolation_rate: float
    
    # Degree distribution
    avg_in_degree: float
    avg_out_degree: float
    max_in_degree: int
    max_out_degree: int
    degree_variance: float
    
    # Small-world properties
    avg_clustering_coefficient: float
    avg_path_length: Optional[float]  # None if disconnected
    
    # Scale-invariance indicators
    fractal_dimension_estimate: Optional[float]
    hierarchy_depth: int
    
    # Compression potential
    estimated_orbits: int
    compression_potential: float  # 1 - (orbits/nodes)
    
    # Quality assessment
    quality_score: float
    issues: List[str]
    recommendations: List[str]


class TopologyAnalyzer:
    """
    Analyzes knowledge graph topology for quality and compression potential.
    
    Key metrics derived from research on scale-invariant compression:
    
    1. Edge-to-Node Ratio (|E|/|V|):
       - Target ≥4:1 for emergence-enabling density
       - Information-theoretic justification: dense graphs have more redundancy
       
    2. Clustering Coefficient:
       - Measures local triangle density
       - High clustering → small-world property → better navigation
       - Target >0.3 for knowledge graphs
       
    3. Isolation Rate:
       - Orphan nodes represent integration failures
       - Target <20% for complete knowledge coverage
       
    4. Compression Potential:
       - Based on approximate automorphism orbit count
       - Higher symmetry → more compressible
    """
    
    def __init__(self, graph_data: Dict[str, Any]):
        """Initialize with graph JSON data."""
        self.nodes = {}
        self.edges = []
        self.adjacency_out = defaultdict(list)  # node -> [(neighbor, edge_type)]
        self.adjacency_in = defaultdict(list)
        
        self._load_graph(graph_data)
        
    def _load_graph(self, data: Dict[str, Any]):
        """Parse graph data from JSON."""
        graph = data.get('graph', data)
        
        for node in graph.get('nodes', []):
            node_id = node['id']
            self.nodes[node_id] = node
            
        for edge in graph.get('edges', []):
            self.edges.append(edge)
            self.adjacency_out[edge['source']].append((edge['target'], edge.get('type', 'related')))
            self.adjacency_in[edge['target']].append((edge['source'], edge.get('type', 'related')))
    
    def compute_basic_metrics(self) -> Dict[str, Any]:
        """Compute fundamental graph metrics."""
        n = len(self.nodes)
        m = len(self.edges)
        
        # Edge-to-node ratio
        ratio = m / n if n > 0 else 0
        
        # Density (for directed graph: m / (n*(n-1)))
        max_edges = n * (n - 1) if n > 1 else 1
        density = m / max_edges if max_edges > 0 else 0
        
        return {
            'num_nodes': n,
            'num_edges': m,
            'edge_to_node_ratio': round(ratio, 4),
            'density': round(density, 6)
        }
    
    def compute_degree_distribution(self) -> Dict[str, Any]:
        """Analyze degree distribution."""
        in_degrees = []
        out_degrees = []
        
        for node_id in self.nodes:
            in_deg = len(self.adjacency_in[node_id])
            out_deg = len(self.adjacency_out[node_id])
            in_degrees.append(in_deg)
            out_degrees.append(out_deg)
        
        n = len(self.nodes)
        if n == 0:
            return {
                'avg_in_degree': 0,
                'avg_out_degree': 0,
                'max_in_degree': 0,
                'max_out_degree': 0,
                'degree_variance': 0
            }
        
        avg_in = sum(in_degrees) / n
        avg_out = sum(out_degrees) / n
        
        # Variance of total degree
        total_degrees = [i + o for i, o in zip(in_degrees, out_degrees)]
        avg_total = sum(total_degrees) / n
        variance = sum((d - avg_total) ** 2 for d in total_degrees) / n
        
        return {
            'avg_in_degree': round(avg_in, 4),
            'avg_out_degree': round(avg_out, 4),
            'max_in_degree': max(in_degrees) if in_degrees else 0,
            'max_out_degree': max(out_degrees) if out_degrees else 0,
            'degree_variance': round(variance, 4)
        }
    
    def find_connected_components(self) -> Tuple[int, int, List[Set[str]]]:
        """Find weakly connected components."""
        visited = set()
        components = []
        
        # Build undirected adjacency for weak connectivity
        undirected = defaultdict(set)
        for node_id in self.nodes:
            for neighbor, _ in self.adjacency_out[node_id]:
                undirected[node_id].add(neighbor)
                undirected[neighbor].add(node_id)
            for neighbor, _ in self.adjacency_in[node_id]:
                undirected[node_id].add(neighbor)
                undirected[neighbor].add(node_id)
        
        def dfs(start: str) -> Set[str]:
            component = set()
            stack = [start]
            while stack:
                node = stack.pop()
                if node in visited:
                    continue
                visited.add(node)
                component.add(node)
                for neighbor in undirected[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
            return component
        
        for node_id in self.nodes:
            if node_id not in visited:
                comp = dfs(node_id)
                components.append(comp)
        
        largest = max(len(c) for c in components) if components else 0
        return len(components), largest, components
    
    def compute_connectivity_metrics(self) -> Dict[str, Any]:
        """Analyze connectivity and isolation."""
        num_components, largest_size, components = self.find_connected_components()
        
        # Isolated nodes (no edges)
        isolated = 0
        for node_id in self.nodes:
            if not self.adjacency_out[node_id] and not self.adjacency_in[node_id]:
                isolated += 1
        
        n = len(self.nodes)
        isolation_rate = isolated / n if n > 0 else 0
        
        return {
            'num_components': num_components,
            'largest_component_size': largest_size,
            'isolated_nodes': isolated,
            'isolation_rate': round(isolation_rate, 4)
        }
    
    def compute_local_clustering(self, node_id: str) -> float:
        """
        Compute local clustering coefficient for a node.
        
        C(v) = (triangles containing v) / (possible triangles)
        
        For directed graphs, we consider both in and out neighbors.
        """
        # Get all neighbors (undirected view)
        neighbors = set()
        for neighbor, _ in self.adjacency_out[node_id]:
            neighbors.add(neighbor)
        for neighbor, _ in self.adjacency_in[node_id]:
            neighbors.add(neighbor)
        
        k = len(neighbors)
        if k < 2:
            return 0.0
        
        # Count edges among neighbors
        neighbor_edges = 0
        neighbor_list = list(neighbors)
        for i, n1 in enumerate(neighbor_list):
            for n2 in neighbor_list[i+1:]:
                # Check if edge exists in either direction
                out_neighbors = {t for t, _ in self.adjacency_out[n1]}
                in_neighbors = {s for s, _ in self.adjacency_in[n1]}
                if n2 in out_neighbors or n2 in in_neighbors:
                    neighbor_edges += 1
        
        # Possible edges among k neighbors
        possible = k * (k - 1) / 2
        
        return neighbor_edges / possible if possible > 0 else 0.0
    
    def compute_clustering_coefficient(self) -> float:
        """Compute average clustering coefficient."""
        if not self.nodes:
            return 0.0
        
        coefficients = [self.compute_local_clustering(nid) for nid in self.nodes]
        return sum(coefficients) / len(coefficients)
    
    def compute_average_path_length(self, sample_size: int = 100) -> Optional[float]:
        """
        Estimate average shortest path length via sampling.
        
        Uses BFS from sample of nodes. Returns None if graph is disconnected.
        """
        if len(self.nodes) < 2:
            return None
        
        # Sample nodes
        node_list = list(self.nodes.keys())
        import random
        random.seed(42)
        sample = random.sample(node_list, min(sample_size, len(node_list)))
        
        total_distance = 0
        pair_count = 0
        
        for source in sample:
            # BFS
            distances = {source: 0}
            queue = [source]
            idx = 0
            
            while idx < len(queue):
                current = queue[idx]
                idx += 1
                current_dist = distances[current]
                
                for neighbor, _ in self.adjacency_out[current]:
                    if neighbor not in distances:
                        distances[neighbor] = current_dist + 1
                        queue.append(neighbor)
            
            # Sum distances to all reachable nodes
            for target, dist in distances.items():
                if target != source:
                    total_distance += dist
                    pair_count += 1
        
        return total_distance / pair_count if pair_count > 0 else None
    
    def estimate_fractal_dimension(self) -> Optional[float]:
        """
        Estimate fractal dimension using box-covering approximation.
        
        Self-similar networks satisfy: N_B(l_B) ~ l_B^(-d_B)
        where N_B is boxes needed to cover network at scale l_B.
        
        This is a simplified estimation suitable for knowledge graphs.
        """
        if len(self.nodes) < 10:
            return None
        
        # Use degree distribution power-law exponent as proxy
        # (Scale-free networks have fractal properties)
        degrees = []
        for node_id in self.nodes:
            deg = len(self.adjacency_out[node_id]) + len(self.adjacency_in[node_id])
            if deg > 0:
                degrees.append(deg)
        
        if len(degrees) < 5:
            return None
        
        degrees.sort(reverse=True)
        
        # Fit log-log slope (simplified power-law estimate)
        log_ranks = [math.log(i + 1) for i in range(len(degrees))]
        log_degrees = [math.log(d) for d in degrees]
        
        # Linear regression for slope
        n = len(log_ranks)
        sum_x = sum(log_ranks)
        sum_y = sum(log_degrees)
        sum_xy = sum(x * y for x, y in zip(log_ranks, log_degrees))
        sum_xx = sum(x * x for x in log_ranks)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
        
        # Fractal dimension related to degree exponent
        # d_B ≈ 1 / (gamma - 1) for scale-free networks
        gamma = -slope
        if gamma > 1:
            d_B = 1 / (gamma - 1)
            return min(round(d_B, 2), 10.0)  # Cap at 10
        
        return None
    
    def compute_hierarchy_depth(self) -> int:
        """
        Estimate hierarchy depth from longest path in DAG component.
        
        For knowledge graphs with type hierarchies, this indicates
        abstraction levels.
        """
        max_depth = 0
        
        # Find nodes with no incoming edges (roots)
        roots = [nid for nid in self.nodes if not self.adjacency_in[nid]]
        
        for root in roots:
            # DFS with depth tracking
            stack = [(root, 1)]
            visited = set()
            
            while stack:
                node, depth = stack.pop()
                if node in visited:
                    continue
                visited.add(node)
                max_depth = max(max_depth, depth)
                
                for neighbor, _ in self.adjacency_out[node]:
                    if neighbor not in visited:
                        stack.append((neighbor, depth + 1))
        
        return max_depth
    
    def estimate_compression_potential(self) -> Tuple[int, float]:
        """
        Estimate compression potential via color-refinement based orbit approximation.
        
        Uses Weisfeiler-Leman style coloring to approximate automorphism orbits.
        More orbits relative to nodes = less compressible.
        """
        if not self.nodes:
            return 0, 0.0
        
        # Initial coloring: node type + degree
        coloring = {}
        for node_id, node in self.nodes.items():
            in_deg = len(self.adjacency_in[node_id])
            out_deg = len(self.adjacency_out[node_id])
            node_type = node.get('type', 'entity')
            coloring[node_id] = f"{node_type}|{in_deg}|{out_deg}"
        
        # Refine coloring
        for _ in range(3):  # Limited iterations for efficiency
            new_coloring = {}
            for node_id in self.nodes:
                neighbor_colors = []
                for neighbor, edge_type in self.adjacency_out[node_id]:
                    neighbor_colors.append(f"o:{edge_type}:{coloring[neighbor]}")
                for neighbor, edge_type in self.adjacency_in[node_id]:
                    neighbor_colors.append(f"i:{edge_type}:{coloring[neighbor]}")
                neighbor_colors.sort()
                new_coloring[node_id] = f"{coloring[node_id]}|{'|'.join(neighbor_colors)}"
            
            if new_coloring == coloring:
                break
            coloring = new_coloring
        
        # Count distinct colors (approximate orbits)
        num_orbits = len(set(coloring.values()))
        n = len(self.nodes)
        
        compression_potential = 1 - (num_orbits / n) if n > 0 else 0
        
        return num_orbits, round(compression_potential, 4)
    
    def assess_quality(self, metrics: Dict[str, Any]) -> Tuple[float, List[str], List[str]]:
        """
        Assess overall graph quality and generate recommendations.
        
        Scoring based on research targets:
        - |E|/|V| ≥ 4: +25 points
        - Isolation < 20%: +25 points  
        - Clustering > 0.3: +25 points
        - Compression potential > 0.5: +25 points
        """
        score = 0
        issues = []
        recommendations = []
        
        # Edge-to-node ratio
        ratio = metrics['edge_to_node_ratio']
        if ratio >= 4:
            score += 25
        elif ratio >= 2:
            score += 15
            issues.append(f"|E|/|V| = {ratio:.2f} (target: ≥4)")
            recommendations.append("Add bridging relationships between related concepts")
        else:
            score += 5
            issues.append(f"|E|/|V| = {ratio:.2f} is very low (target: ≥4)")
            recommendations.append("Graph is too sparse - systematic relationship extraction needed")
        
        # Isolation rate
        isolation = metrics['isolation_rate']
        if isolation <= 0.05:
            score += 25
        elif isolation <= 0.20:
            score += 15
            issues.append(f"Isolation rate = {isolation*100:.1f}% (target: <20%)")
            recommendations.append("Connect isolated nodes to central concepts")
        else:
            score += 5
            issues.append(f"Isolation rate = {isolation*100:.1f}% is high (target: <20%)")
            recommendations.append("Many orphan nodes - review extraction completeness")
        
        # Clustering coefficient
        clustering = metrics['avg_clustering_coefficient']
        if clustering >= 0.3:
            score += 25
        elif clustering >= 0.15:
            score += 15
            issues.append(f"Clustering = {clustering:.3f} (target: >0.3)")
            recommendations.append("Add triangulating relationships for small-world property")
        else:
            score += 5
            issues.append(f"Clustering = {clustering:.3f} is low (target: >0.3)")
            recommendations.append("Graph lacks local structure - add transitive relationships")
        
        # Compression potential
        compression = metrics['compression_potential']
        if compression >= 0.5:
            score += 25
        elif compression >= 0.3:
            score += 15
            issues.append(f"Compression potential = {compression*100:.1f}%")
            recommendations.append("Consider normalizing entity types for better compression")
        else:
            score += 10
            issues.append(f"Low compression potential ({compression*100:.1f}%)")
            recommendations.append("Graph has few structural regularities - may be well-optimized or too heterogeneous")
        
        return score, issues, recommendations
    
    def analyze(self) -> TopologyReport:
        """Run complete topology analysis."""
        basic = self.compute_basic_metrics()
        degrees = self.compute_degree_distribution()
        connectivity = self.compute_connectivity_metrics()
        clustering = self.compute_clustering_coefficient()
        path_length = self.compute_average_path_length()
        fractal_dim = self.estimate_fractal_dimension()
        hierarchy = self.compute_hierarchy_depth()
        orbits, compression = self.estimate_compression_potential()
        
        # Combine all metrics
        all_metrics = {
            **basic,
            **degrees,
            **connectivity,
            'avg_clustering_coefficient': round(clustering, 4),
            'avg_path_length': round(path_length, 4) if path_length else None,
            'fractal_dimension_estimate': fractal_dim,
            'hierarchy_depth': hierarchy,
            'estimated_orbits': orbits,
            'compression_potential': compression
        }
        
        score, issues, recommendations = self.assess_quality(all_metrics)
        
        return TopologyReport(
            num_nodes=basic['num_nodes'],
            num_edges=basic['num_edges'],
            edge_to_node_ratio=basic['edge_to_node_ratio'],
            density=basic['density'],
            num_components=connectivity['num_components'],
            largest_component_size=connectivity['largest_component_size'],
            isolated_nodes=connectivity['isolated_nodes'],
            isolation_rate=connectivity['isolation_rate'],
            avg_in_degree=degrees['avg_in_degree'],
            avg_out_degree=degrees['avg_out_degree'],
            max_in_degree=degrees['max_in_degree'],
            max_out_degree=degrees['max_out_degree'],
            degree_variance=degrees['degree_variance'],
            avg_clustering_coefficient=round(clustering, 4),
            avg_path_length=round(path_length, 4) if path_length else None,
            fractal_dimension_estimate=fractal_dim,
            hierarchy_depth=hierarchy,
            estimated_orbits=orbits,
            compression_potential=compression,
            quality_score=score,
            issues=issues,
            recommendations=recommendations
        )


def format_report(report: TopologyReport) -> str:
    """Format topology report as readable string."""
    lines = [
        "=" * 60,
        "KNOWLEDGE GRAPH TOPOLOGY ANALYSIS",
        "=" * 60,
        "",
        "BASIC METRICS",
        f"  Nodes: {report.num_nodes}",
        f"  Edges: {report.num_edges}",
        f"  Edge-to-Node Ratio: {report.edge_to_node_ratio:.2f} (target: ≥4.0)",
        f"  Density: {report.density:.6f}",
        "",
        "CONNECTIVITY",
        f"  Connected Components: {report.num_components}",
        f"  Largest Component: {report.largest_component_size} nodes",
        f"  Isolated Nodes: {report.isolated_nodes} ({report.isolation_rate*100:.1f}%)",
        "",
        "DEGREE DISTRIBUTION",
        f"  Avg In-Degree: {report.avg_in_degree:.2f}",
        f"  Avg Out-Degree: {report.avg_out_degree:.2f}",
        f"  Max In-Degree: {report.max_in_degree}",
        f"  Max Out-Degree: {report.max_out_degree}",
        f"  Degree Variance: {report.degree_variance:.2f}",
        "",
        "SMALL-WORLD PROPERTIES",
        f"  Clustering Coefficient: {report.avg_clustering_coefficient:.4f} (target: >0.3)",
        f"  Avg Path Length: {report.avg_path_length if report.avg_path_length else 'N/A (disconnected)'}",
        "",
        "SCALE-INVARIANCE INDICATORS",
        f"  Fractal Dimension (est): {report.fractal_dimension_estimate or 'N/A'}",
        f"  Hierarchy Depth: {report.hierarchy_depth}",
        "",
        "COMPRESSION POTENTIAL",
        f"  Estimated Orbits: {report.estimated_orbits}",
        f"  Compression Potential: {report.compression_potential*100:.1f}%",
        "",
        "=" * 60,
        f"QUALITY SCORE: {report.quality_score}/100",
        "=" * 60,
    ]
    
    if report.issues:
        lines.extend(["", "ISSUES:"])
        for issue in report.issues:
            lines.append(f"  ⚠ {issue}")
    
    if report.recommendations:
        lines.extend(["", "RECOMMENDATIONS:"])
        for rec in report.recommendations:
            lines.append(f"  → {rec}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze knowledge graph topology for quality and compression potential',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Target metrics for high-quality knowledge graphs:
  - Edge-to-Node Ratio: ≥4:1 (enables emergence through dense connectivity)
  - Isolation Rate: <20% (measures integration completeness)
  - Clustering Coefficient: >0.3 (small-world property indicator)
  - Compression Potential: Higher = more structural regularity

Examples:
  python topology_metrics.py graph.json --report
  python topology_metrics.py graph.json --json
        """
    )
    
    parser.add_argument('input', help='Input graph JSON file')
    parser.add_argument('--report', action='store_true', help='Generate formatted report')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--compression-potential', action='store_true', 
                       help='Focus on compression potential analysis')
    
    args = parser.parse_args()
    
    with open(args.input) as f:
        data = json.load(f)
    
    analyzer = TopologyAnalyzer(data)
    report = analyzer.analyze()
    
    if args.json:
        import dataclasses
        print(json.dumps(dataclasses.asdict(report), indent=2))
    else:
        print(format_report(report))


if __name__ == '__main__':
    main()
