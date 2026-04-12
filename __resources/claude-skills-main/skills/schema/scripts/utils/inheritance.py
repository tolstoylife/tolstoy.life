"""Property inheritance logic for ontology nodes."""

from typing import Dict, Any
from scripts.utils.ontology import Ontology, OntologyNode


def compute_inherited_properties(node: OntologyNode, ontology: Ontology) -> Dict[str, Any]:
    """Compute properties inherited from ancestors."""
    inherited = {}
    current = node

    while current.parent_id:
        parent = ontology.nodes.get(current.parent_id)
        if not parent:
            break

        for key, value in parent.properties.items():
            if key not in inherited and key not in node.properties:
                inherited[key] = {
                    "value": value,
                    "from": parent.id
                }

        current = parent

    return inherited


def apply_inheritance(ontology: Ontology) -> None:
    """Apply property inheritance to all nodes in the ontology."""
    for node in ontology.nodes.values():
        if node.parent_id:
            node.inherited_properties = compute_inherited_properties(node, ontology)


def get_effective_property(node: OntologyNode, property_name: str) -> Any:
    """Get property value, checking local properties first, then inherited."""
    if property_name in node.properties:
        return node.properties[property_name]

    if property_name in node.inherited_properties:
        return node.inherited_properties[property_name]["value"]

    return None


def get_property_source(node: OntologyNode, property_name: str) -> str:
    """Get the source node ID for a property."""
    if property_name in node.properties:
        return node.id

    if property_name in node.inherited_properties:
        return node.inherited_properties[property_name]["from"]

    return None
