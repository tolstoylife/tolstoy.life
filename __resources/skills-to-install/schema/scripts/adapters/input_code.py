"""Code input adapter for parsing source code structure."""

import re
from scripts.utils.ontology import Ontology, OntologyNode, OntologyEdge


class CodeAdapter:
    """Parse code files to extract structure (classes, functions, etc.)."""

    def __init__(self):
        """Initialize code adapter."""
        # Pattern for Python classes and functions
        self.class_pattern = re.compile(r'^class\s+(\w+)', re.MULTILINE)
        self.function_pattern = re.compile(r'^(?:async\s+)?def\s+(\w+)', re.MULTILINE)
        self.method_pattern = re.compile(r'^\s+(?:async\s+)?def\s+(\w+)', re.MULTILINE)

    def parse(self, content: str) -> Ontology:
        """Parse code content into ontology.

        Currently supports Python. Can be extended for other languages.

        Args:
            content: Source code text

        Returns:
            Ontology representing the code structure
        """
        ontology = Ontology()
        ontology.metadata["input_type"] = "code"
        ontology.metadata["adapter"] = "CodeAdapter"
        ontology.metadata["language"] = "python"

        # Create module root
        root = OntologyNode(
            id="code_root",
            label="Code Module",
            node_type="module",
            depth=0
        )
        ontology.add_node(root)

        # Extract classes
        class_nodes = {}
        for match in self.class_pattern.finditer(content):
            class_name = match.group(1)
            class_id = f"class_{class_name.lower()}"

            node = OntologyNode(
                id=class_id,
                label=class_name,
                node_type="class",
                depth=1,
                parent_id=root.id
            )
            root.children.append(class_id)
            ontology.add_node(node)
            class_nodes[class_name] = node

            # Create edge
            edge = OntologyEdge(
                source_id=root.id,
                target_id=class_id,
                edge_type="contains"
            )
            ontology.add_edge(edge)

        # Extract top-level functions
        for match in self.function_pattern.finditer(content):
            func_name = match.group(1)

            # Skip if it's a method (indented)
            if content[match.start():match.end()].startswith(' '):
                continue

            func_id = f"func_{func_name.lower()}"

            node = OntologyNode(
                id=func_id,
                label=func_name,
                node_type="function",
                depth=1,
                parent_id=root.id
            )
            root.children.append(func_id)
            ontology.add_node(node)

            # Create edge
            edge = OntologyEdge(
                source_id=root.id,
                target_id=func_id,
                edge_type="contains"
            )
            ontology.add_edge(edge)

        # Extract methods (indented functions)
        for match in self.method_pattern.finditer(content):
            method_name = match.group(1)

            # Find which class this method belongs to
            # Simple heuristic: find the nearest preceding class
            method_start = match.start()
            nearest_class = None
            min_distance = float('inf')

            for class_match in self.class_pattern.finditer(content):
                class_start = class_match.start()
                if class_start < method_start:
                    distance = method_start - class_start
                    if distance < min_distance:
                        min_distance = distance
                        nearest_class = class_match.group(1)

            if nearest_class and nearest_class in class_nodes:
                parent_node = class_nodes[nearest_class]
                method_id = f"method_{nearest_class.lower()}_{method_name.lower()}"

                node = OntologyNode(
                    id=method_id,
                    label=method_name,
                    node_type="method",
                    depth=2,
                    parent_id=parent_node.id
                )
                parent_node.children.append(method_id)
                ontology.add_node(node)

                # Create edge
                edge = OntologyEdge(
                    source_id=parent_node.id,
                    target_id=method_id,
                    edge_type="has_method"
                )
                ontology.add_edge(edge)

        return ontology
