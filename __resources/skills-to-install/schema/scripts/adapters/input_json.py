"""JSON input adapter - extract structure from JSON data."""

import json
from typing import Any
from scripts.utils.ontology import Ontology, OntologyNode, OntologyEdge


class JSONAdapter:
    """Parse JSON into ontology structure."""

    def __init__(self):
        self.node_counter = 0

    def parse(self, json_str: str) -> Ontology:
        """Extract structure from JSON input."""
        ontology = Ontology()
        ontology.metadata["source_type"] = "json"

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

        self._process_value(data, ontology, parent_id=None, depth=0, key="root")
        return ontology

    def _process_value(self, value: Any, ontology: Ontology,
                       parent_id: str, depth: int, key: str) -> str:
        """Recursively process JSON value and create ontology nodes."""
        node_id = f"json_{self.node_counter}"
        self.node_counter += 1

        if isinstance(value, dict):
            node = OntologyNode(
                id=node_id,
                label=key,
                node_type="object",
                depth=depth,
                parent_id=parent_id,
                description=f"JSON object with {len(value)} properties"
            )
            node.add_property("key", key)
            node.add_property("property_count", len(value))
            ontology.add_node(node)

            for prop_key, prop_value in value.items():
                child_id = self._process_value(
                    prop_value, ontology, node_id, depth + 1, prop_key
                )
                node.children.append(child_id)
                edge = OntologyEdge(
                    source_id=node_id,
                    target_id=child_id,
                    edge_type="has_property"
                )
                ontology.add_edge(edge)

        elif isinstance(value, list):
            node = OntologyNode(
                id=node_id,
                label=key,
                node_type="array",
                depth=depth,
                parent_id=parent_id,
                description=f"JSON array with {len(value)} items"
            )
            node.add_property("key", key)
            node.add_property("length", len(value))
            ontology.add_node(node)

            for i, item in enumerate(value):
                child_id = self._process_value(
                    item, ontology, node_id, depth + 1, f"{key}[{i}]"
                )
                node.children.append(child_id)
                edge = OntologyEdge(
                    source_id=node_id,
                    target_id=child_id,
                    edge_type="contains"
                )
                ontology.add_edge(edge)

        else:
            value_type = type(value).__name__
            node = OntologyNode(
                id=node_id,
                label=key,
                node_type="value",
                depth=depth,
                parent_id=parent_id,
                description=f"{value_type}: {str(value)[:50]}"
            )
            node.add_property("key", key)
            node.add_property("value", value)
            node.add_property("value_type", value_type)
            ontology.add_node(node)

        if parent_id:
            parent = ontology.nodes[parent_id]
            if node_id not in parent.children:
                parent.children.append(node_id)

        return node_id
