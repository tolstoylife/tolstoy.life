"""Constraint validation for fractal mode ontologies."""

from typing import List, Dict, Any
import yaml
from pathlib import Path
from scripts.utils.ontology import Ontology, OntologyNode


class ConstraintValidator:
    """Validate ontology against fractal mode constraints."""

    def __init__(self, config_path: str = None):
        """Initialize validator with configuration.

        Args:
            config_path: Path to YAML config file (defaults to fractal-mode.yaml)
        """
        if config_path is None:
            base_path = Path(__file__).parent.parent.parent
            config_path = base_path / "config" / "fractal-mode.yaml"

        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.constraints = self.config.get("constraints", {})
        self.validation_config = self.config.get("validation", {})

    def validate(self, ontology: Ontology) -> Dict[str, List[Dict[str, Any]]]:
        """Validate ontology against all constraints.

        Returns:
            Dictionary of constraint violations by type
        """
        violations = {
            "branching": [],
            "naming": [],
            "relations": [],
            "topology": [],
            "depth": [],
            "label_length": []
        }

        # C1: Branching factor
        violations["branching"] = self._validate_branching(ontology)

        # C2: Homonymic inheritance
        violations["naming"] = self._validate_naming(ontology)

        # C3: Relation uniformity
        violations["relations"] = self._validate_relations(ontology)

        # C4: Topology density
        violations["topology"] = self._validate_topology(ontology)

        # C5: Label length
        violations["label_length"] = self._validate_label_length(ontology)

        # C6: Depth limit
        violations["depth"] = self._validate_depth(ontology)

        # Filter out empty violation lists
        violations = {k: v for k, v in violations.items() if v}

        return violations

    def _validate_branching(self, ontology: Ontology) -> List[Dict]:
        """Validate branching factor (2-3 children per non-leaf)."""
        violations = []
        branching_config = self.constraints.get("branching", {})
        min_children = branching_config.get("min_children", 2)
        max_children = branching_config.get("max_children", 3)

        for node in ontology.nodes.values():
            if node.children:  # Non-leaf node
                child_count = len(node.children)

                if child_count < min_children:
                    violations.append({
                        "node_id": node.id,
                        "node_label": node.label,
                        "constraint": "C1 - Branching Factor",
                        "error": f"Only {child_count} children (minimum {min_children} required)",
                        "severity": "critical"
                    })
                elif child_count > max_children:
                    violations.append({
                        "node_id": node.id,
                        "node_label": node.label,
                        "constraint": "C1 - Branching Factor",
                        "error": f"{child_count} children (maximum {max_children} allowed)",
                        "severity": "critical"
                    })

        return violations

    def _validate_naming(self, ontology: Ontology) -> List[Dict]:
        """Validate homonymic inheritance (child labels contain parent stem)."""
        violations = []
        naming_config = self.constraints.get("naming", {})

        if not naming_config.get("homonymic_inheritance", False):
            return violations  # Not enforcing this constraint

        for node in ontology.nodes.values():
            if node.depth > 0 and node.parent_id:  # Not root
                parent = ontology.nodes.get(node.parent_id)
                if not parent or not parent.stem:
                    continue

                parent_stem = parent.stem.lower()
                node_label = node.label.lower()

                if parent_stem not in node_label:
                    violations.append({
                        "node_id": node.id,
                        "node_label": node.label,
                        "constraint": "C2 - Homonymic Inheritance",
                        "error": f"Missing parent stem '{parent.stem}'",
                        "parent_label": parent.label,
                        "severity": "critical"
                    })

        return violations

    def _validate_relations(self, ontology: Ontology) -> List[Dict]:
        """Validate relation uniformity (all children same relation type)."""
        violations = []
        relations_config = self.constraints.get("relations", {})

        if not relations_config.get("uniform_per_parent", False):
            return violations

        # Group edges by source (parent)
        parent_edges = {}
        for edge in ontology.edges:
            if edge.source_id not in parent_edges:
                parent_edges[edge.source_id] = []
            parent_edges[edge.source_id].append(edge)

        for parent_id, edges in parent_edges.items():
            if len(edges) < 2:
                continue  # Need at least 2 edges to compare

            # Get unique edge types
            edge_types = set(e.edge_type for e in edges)

            if len(edge_types) > 1:
                parent = ontology.nodes.get(parent_id)
                violations.append({
                    "node_id": parent_id,
                    "node_label": parent.label if parent else parent_id,
                    "constraint": "C3 - Relation Uniformity",
                    "error": f"Mixed relation types: {edge_types}",
                    "severity": "high"
                })

        return violations

    def _validate_topology(self, ontology: Ontology) -> List[Dict]:
        """Validate topology density (edge-to-node ratio)."""
        violations = []
        topology_config = self.constraints.get("topology", {})
        min_score = topology_config.get("min_score", 4.0)

        actual_score = ontology.calculate_topology_score()

        if actual_score < min_score:
            required_edges = int(min_score * len(ontology.nodes))
            current_edges = len(ontology.edges) + sum(len(n.children) for n in ontology.nodes.values())
            missing_edges = required_edges - current_edges

            violations.append({
                "constraint": "C4 - Topology Density",
                "error": f"Topology score {actual_score:.2f} below minimum {min_score}",
                "current_score": actual_score,
                "required_score": min_score,
                "missing_edges": missing_edges,
                "severity": "high"
            })

        return violations

    def _validate_label_length(self, ontology: Ontology) -> List[Dict]:
        """Validate label length (max words)."""
        violations = []
        naming_config = self.constraints.get("naming", {})
        max_words = naming_config.get("max_label_words", 3)

        for node in ontology.nodes.values():
            word_count = len(node.label.split())

            if word_count > max_words:
                violations.append({
                    "node_id": node.id,
                    "node_label": node.label,
                    "constraint": "C5 - Label Length",
                    "error": f"{word_count} words (maximum {max_words} allowed)",
                    "severity": "medium"
                })

        return violations

    def _validate_depth(self, ontology: Ontology) -> List[Dict]:
        """Validate depth limit."""
        violations = []
        depth_config = self.constraints.get("depth", {})
        max_depth = depth_config.get("max_depth", 5)

        for node in ontology.nodes.values():
            if node.depth > max_depth:
                violations.append({
                    "node_id": node.id,
                    "node_label": node.label,
                    "constraint": "C6 - Depth Limit",
                    "error": f"Depth {node.depth} exceeds limit {max_depth}",
                    "current_depth": node.depth,
                    "max_depth": max_depth,
                    "severity": "medium"
                })

        return violations

    def generate_report(self, violations: Dict[str, List[Dict]]) -> str:
        """Generate human-readable validation report.

        Args:
            violations: Dictionary of violations by type

        Returns:
            Formatted report string
        """
        if not violations:
            return "✓ All constraints satisfied (fractal mode compliant)"

        report = ["# Constraint Validation Report\n"]
        total_violations = sum(len(v) for v in violations.values())
        report.append(f"**Total Violations**: {total_violations}\n")

        for constraint_type, violation_list in violations.items():
            if not violation_list:
                continue

            report.append(f"\n## {constraint_type.replace('_', ' ').title()}")
            report.append(f"**Count**: {len(violation_list)}\n")

            for v in violation_list:
                severity = v.get("severity", "medium")
                node_label = v.get("node_label", "N/A")
                error = v.get("error", "")
                constraint = v.get("constraint", constraint_type)

                report.append(f"- **{severity.upper()}**: `{node_label}` - {constraint}: {error}")

        return "\n".join(report)
