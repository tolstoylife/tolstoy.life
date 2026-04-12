"""Text input adapter - extract structure from plain text or markdown."""

import re
from typing import List, Tuple
from scripts.utils.ontology import Ontology, OntologyNode, OntologyEdge


class TextAdapter:
    """Parse plain text or markdown into ontology structure."""

    def parse(self, text: str) -> Ontology:
        """Extract structure from text input."""
        ontology = Ontology()
        ontology.metadata["source_type"] = "text"
        ontology.metadata["input_length"] = len(text)

        headings = self._extract_headings(text)

        if headings:
            self._build_heading_hierarchy(headings, ontology)
        else:
            self._build_paragraph_structure(text, ontology)

        return ontology

    def _extract_headings(self, text: str) -> List[Tuple[int, str, str]]:
        """Extract markdown headings with their levels."""
        headings = []
        lines = text.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                heading_text = match.group(2).strip()

                content_lines = []
                i += 1
                while i < len(lines) and not re.match(r'^#{1,6}\s+', lines[i].strip()):
                    content_lines.append(lines[i])
                    i += 1

                content = '\n'.join(content_lines).strip()
                headings.append((level, heading_text, content))
            else:
                i += 1

        return headings

    def _build_heading_hierarchy(self, headings: List[Tuple[int, str, str]],
                                  ontology: Ontology) -> None:
        """Build ontology from markdown heading hierarchy."""
        if not headings:
            return

        root = OntologyNode(
            id="text_root",
            label="Document",
            node_type="document",
            depth=0
        )
        ontology.add_node(root)

        stack = [(0, root)]
        node_counter = 1

        for level, heading_text, content in headings:
            while stack and stack[-1][0] >= level:
                stack.pop()

            parent_level, parent_node = stack[-1] if stack else (0, root)

            node_id = f"heading_{node_counter}"
            node = OntologyNode(
                id=node_id,
                label=heading_text,
                node_type="section",
                depth=level,
                parent_id=parent_node.id,
                description=content[:200] if content else None
            )
            node.add_property("content", content)
            node.add_property("heading_level", level)

            ontology.add_node(node)
            parent_node.children.append(node_id)

            edge = OntologyEdge(
                source_id=parent_node.id,
                target_id=node_id,
                edge_type="parent_of"
            )
            ontology.add_edge(edge)

            stack.append((level, node))
            node_counter += 1

    def _build_paragraph_structure(self, text: str, ontology: Ontology) -> None:
        """Build flat structure from paragraphs."""
        root = OntologyNode(
            id="text_root",
            label="Text Document",
            node_type="document",
            depth=0
        )
        ontology.add_node(root)

        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        for i, para in enumerate(paragraphs):
            node_id = f"para_{i}"
            node = OntologyNode(
                id=node_id,
                label=f"Paragraph {i+1}",
                node_type="paragraph",
                depth=1,
                parent_id="text_root",
                description=para[:100]
            )
            node.add_property("content", para)
            node.add_property("index", i)

            ontology.add_node(node)
            root.children.append(node_id)

            edge = OntologyEdge(
                source_id="text_root",
                target_id=node_id,
                edge_type="parent_of"
            )
            ontology.add_edge(edge)
