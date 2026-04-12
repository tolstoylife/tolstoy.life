"""Layer 4: Output generation using templates."""

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from typing import Dict
from scripts.utils.ontology import Ontology, OntologyNode


class ObsidianGenerator:
    """Generate Obsidian-compatible markdown from ontology."""

    def __init__(self, template_dir: str = None):
        """Initialize generator with template directory."""
        if template_dir is None:
            base_path = Path(__file__).parent.parent.parent
            template_dir = base_path / "config" / "templates"

        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def generate(self, ontology: Ontology) -> str:
        """Generate Obsidian markdown from ontology."""
        template = self.env.get_template('obsidian.md.j2')
        context = self._prepare_context(ontology)
        markdown = template.render(**context)
        return markdown

    def _prepare_context(self, ontology: Ontology) -> Dict:
        """Prepare context data for template rendering."""
        root = next((n for n in ontology.nodes.values() if n.depth == 0), None)
        if not root:
            root = OntologyNode(
                id="generated_root",
                label="Schema",
                node_type="concept",
                depth=0
            )

        nodes_sorted = sorted(
            ontology.nodes.values(),
            key=lambda n: (n.depth, n.label)
        )

        tags = set()
        for node in ontology.nodes.values():
            if "tags" in node.properties:
                node_tags = node.properties["tags"]
                if isinstance(node_tags, list):
                    tags.update(node_tags)
                else:
                    tags.add(node_tags)

        hierarchical_edges = [
            e for e in ontology.edges
            if e.edge_type in ["parent_of", "contains", "has_property"]
        ]

        node_relationships = {}
        for edge in ontology.edges:
            if edge.source_id not in node_relationships:
                node_relationships[edge.source_id] = []
            node_relationships[edge.source_id].append(edge)

        if "topology_score" not in ontology.metadata:
            ontology.metadata["topology_score"] = ontology.calculate_topology_score()

        return {
            "metadata": ontology.metadata,
            "root": root,
            "nodes": ontology.nodes,
            "nodes_sorted": nodes_sorted,
            "edges": ontology.edges,
            "hierarchical_edges": hierarchical_edges,
            "node_relationships": node_relationships,
            "tags": sorted(tags)
        }
