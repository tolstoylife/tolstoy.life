"""Layer 4: Export generators for additional formats (JSON-LD, Cypher, etc.)."""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from scripts.utils.ontology import Ontology


class BaseExporter:
    """Base class for export generators."""

    def __init__(self, template_name: str):
        """Initialize exporter with template.

        Args:
            template_name: Name of the Jinja2 template file
        """
        base_path = Path(__file__).parent.parent.parent
        template_dir = base_path / "config" / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))
        self.template = self.env.get_template(template_name)

    def generate(self, ontology: Ontology) -> str:
        """Generate export from ontology.

        Args:
            ontology: The ontology to export

        Returns:
            Formatted export string
        """
        # Sort nodes by depth for hierarchical output
        nodes_sorted = sorted(
            ontology.nodes.values(),
            key=lambda n: (n.depth, n.id)
        )

        return self.template.render(
            nodes_sorted=nodes_sorted,
            edges=ontology.edges,
            metadata=ontology.metadata,
            nodes=ontology.nodes
        )


class JSONLDGenerator(BaseExporter):
    """Generate JSON-LD (Linked Data) exports."""

    def __init__(self):
        """Initialize JSON-LD generator."""
        super().__init__("jsonld.json.j2")


class CypherGenerator(BaseExporter):
    """Generate Cypher queries for Neo4j graph database."""

    def __init__(self):
        """Initialize Cypher generator."""
        super().__init__("cypher.cypher.j2")


class GraphQLGenerator(BaseExporter):
    """Generate GraphQL schema definitions."""

    def __init__(self):
        """Initialize GraphQL generator."""
        super().__init__("graphql.graphql.j2")
