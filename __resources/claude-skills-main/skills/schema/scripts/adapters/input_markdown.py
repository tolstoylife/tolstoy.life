"""Markdown input adapter for structured markdown documents."""

import re
from scripts.utils.ontology import Ontology, OntologyNode, OntologyEdge


class MarkdownAdapter:
    """Parse markdown files with heading hierarchy."""

    def __init__(self):
        """Initialize markdown adapter."""
        self.heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)

    def parse(self, content: str) -> Ontology:
        """Parse markdown content into ontology.

        Args:
            content: Markdown text with headings

        Returns:
            Ontology representing the document structure
        """
        ontology = Ontology()
        ontology.metadata["input_type"] = "markdown"
        ontology.metadata["adapter"] = "MarkdownAdapter"

        # Create document root
        root = OntologyNode(
            id="markdown_root",
            label="Markdown Document",
            node_type="document",
            depth=0
        )
        ontology.add_node(root)

        # Stack to track heading hierarchy
        stack = [(0, root)]  # (level, node)
        heading_counter = {}

        # Find all headings
        for match in self.heading_pattern.finditer(content):
            heading_level = len(match.group(1))
            heading_text = match.group(2).strip()

            # Generate unique ID
            if heading_level not in heading_counter:
                heading_counter[heading_level] = 0
            heading_counter[heading_level] += 1
            node_id = f"h{heading_level}_{heading_counter[heading_level]}"

            # Determine node type based on level
            node_type = self._get_node_type(heading_level)

            # Create node
            node = OntologyNode(
                id=node_id,
                label=heading_text,
                node_type=node_type,
                depth=heading_level
            )

            # Find parent (most recent heading with lower level)
            while len(stack) > 1 and stack[-1][0] >= heading_level:
                stack.pop()

            parent = stack[-1][1]
            node.parent_id = parent.id
            parent.children.append(node.id)

            # Add to ontology
            ontology.add_node(node)

            # Create parent-child edge
            edge = OntologyEdge(
                source_id=parent.id,
                target_id=node.id,
                edge_type="parent_of"
            )
            ontology.add_edge(edge)

            # Push to stack
            stack.append((heading_level, node))

        return ontology

    def _get_node_type(self, level: int) -> str:
        """Map heading level to node type.

        Args:
            level: Heading level (1-6)

        Returns:
            Node type string
        """
        type_map = {
            1: "category",
            2: "concept",
            3: "subconcept",
            4: "detail",
            5: "note",
            6: "annotation"
        }
        return type_map.get(level, "concept")
