import pytest
from scripts.utils.ontology import OntologyNode, OntologyEdge, Ontology

def test_ontology_node_creation():
    """Test creating an ontology node with basic properties."""
    node = OntologyNode(
        id="n1",
        label="Test Node",
        node_type="entity",
        depth=0
    )
    assert node.id == "n1"
    assert node.label == "Test Node"
    assert node.node_type == "entity"
    assert node.depth == 0
    assert node.properties == {}
    assert node.inherited_properties == {}

def test_ontology_node_with_properties():
    """Test node with custom properties."""
    node = OntologyNode(
        id="n1",
        label="Test",
        node_type="concept",
        depth=1,
        stem="test",
        properties={"category": "example", "weight": 0.8},
        aliases=["Sample", "Demo"]
    )
    assert node.stem == "test"
    assert node.properties["category"] == "example"
    assert node.properties["weight"] == 0.8
    assert "Sample" in node.aliases

def test_ontology_edge_creation():
    """Test creating an ontology edge."""
    edge = OntologyEdge(
        source_id="n1",
        target_id="n2",
        edge_type="parent_of",
        strength=0.95
    )
    assert edge.source_id == "n1"
    assert edge.target_id == "n2"
    assert edge.edge_type == "parent_of"
    assert edge.strength == 0.95
    assert edge.inferred is False

def test_ontology_edge_validation():
    """Test edge strength validation."""
    with pytest.raises(ValueError, match="Edge strength must be 0.0-1.0"):
        OntologyEdge(
            source_id="n1",
            target_id="n2",
            edge_type="related_to",
            strength=1.5
        )

def test_ontology_add_nodes_and_edges():
    """Test building an ontology with nodes and edges."""
    onto = Ontology()

    # Add nodes
    root = OntologyNode(id="root", label="Root", node_type="concept", depth=0)
    child1 = OntologyNode(id="c1", label="Child 1", node_type="entity", depth=1, parent_id="root")
    child2 = OntologyNode(id="c2", label="Child 2", node_type="entity", depth=1, parent_id="root")

    root.children = ["c1", "c2"]

    onto.add_node(root)
    onto.add_node(child1)
    onto.add_node(child2)

    # Add edge
    edge = OntologyEdge(source_id="root", target_id="c1", edge_type="parent_of")
    onto.add_edge(edge)

    assert len(onto.nodes) == 3
    assert len(onto.edges) == 1
    assert onto.get_children("root") == [child1, child2]
    assert onto.get_parent("c1") == root

def test_ontology_topology_score():
    """Test topology score calculation."""
    onto = Ontology()

    # Create simple hierarchy: root -> 2 children
    root = OntologyNode(id="r", label="Root", node_type="concept", depth=0, children=["c1", "c2"])
    child1 = OntologyNode(id="c1", label="C1", node_type="entity", depth=1, parent_id="r")
    child2 = OntologyNode(id="c2", label="C2", node_type="entity", depth=1, parent_id="r")

    onto.add_node(root)
    onto.add_node(child1)
    onto.add_node(child2)

    # Add cross-link
    onto.add_edge(OntologyEdge(source_id="c1", target_id="c2", edge_type="related_to"))

    # Score = (1 cross-link + 2 hierarchical) / 3 nodes = 1.0
    assert onto.calculate_topology_score() == 1.0
