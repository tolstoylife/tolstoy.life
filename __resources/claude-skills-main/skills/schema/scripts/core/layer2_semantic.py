"""Layer 2: Semantic analysis and relationship inference."""

import re
from typing import List, Set, Tuple
from scripts.utils.ontology import Ontology, OntologyNode, OntologyEdge
from scripts.utils.graph_analytics import GraphNavigator


class SemanticAnalyzer:
    """Analyze ontology for semantic relationships and patterns."""

    def __init__(self, use_nlp: bool = False):
        """Initialize semantic analyzer.

        Args:
            use_nlp: Whether to use NLP libraries (spaCy) if available
        """
        self.use_nlp = use_nlp
        self.nlp = None

        if use_nlp:
            try:
                import spacy
                self.nlp = spacy.load("en_core_web_sm")
            except (ImportError, OSError):
                # spaCy not available, fall back to pattern matching
                self.use_nlp = False

    def analyze(self, ontology: Ontology) -> Ontology:
        """Perform semantic analysis on ontology.

        Adds:
        - Semantic relationships between nodes
        - Entity type classification
        - Implicit relationship inference

        Args:
            ontology: The ontology to analyze

        Returns:
            Enhanced ontology with semantic relationships
        """
        # Extract stems for nodes that don't have them
        self._extract_stems(ontology)

        # Classify node types semantically
        self._classify_node_types(ontology)

        # Infer relationships based on patterns
        self._infer_relationships(ontology)

        # Add co-occurrence relationships
        self._add_cooccurrence_relationships(ontology)

        # Calculate semantic similarity
        self._add_similarity_relationships(ontology)

        # Add multi-dimensional navigation
        navigator = GraphNavigator(ontology)
        navigator.enrich_with_all_dimensions()

        return ontology

    def _extract_stems(self, ontology: Ontology) -> None:
        """Extract lexical stems for nodes."""
        for node in ontology.nodes.values():
            if not node.stem:
                node.stem = self._get_stem(node.label)

    def _get_stem(self, label: str) -> str:
        """Get lexical stem from label."""
        # Simple stemming: take first word, lowercase, remove common suffixes
        words = label.split()
        if not words:
            return label.lower()

        stem = words[0].lower()

        # Remove common suffixes
        suffixes = ['ing', 'ed', 's', 'es', 'tion', 'ment', 'ness', 'ly']
        for suffix in suffixes:
            if stem.endswith(suffix) and len(stem) > len(suffix) + 2:
                stem = stem[:-len(suffix)]
                break

        return stem

    def _classify_node_types(self, ontology: Ontology) -> None:
        """Classify nodes semantically."""
        for node in ontology.nodes.values():
            # Check content for classification hints
            content = node.properties.get("content", "")
            description = node.description or ""
            text = f"{node.label} {content} {description}".lower()

            # Detect entity types
            if self._is_person(text):
                node.add_property("entity_type", "person")
            elif self._is_organization(text):
                node.add_property("entity_type", "organization")
            elif self._is_location(text):
                node.add_property("entity_type", "location")
            elif self._is_temporal(text):
                node.add_property("entity_type", "temporal")
            elif self._is_process(text):
                node.add_property("entity_type", "process")

    def _is_person(self, text: str) -> bool:
        """Check if text references a person."""
        person_indicators = ['person', 'user', 'customer', 'employee', 'manager']
        return any(indicator in text for indicator in person_indicators)

    def _is_organization(self, text: str) -> bool:
        """Check if text references an organization."""
        org_indicators = ['company', 'organization', 'corp', 'inc', 'llc', 'team', 'department']
        return any(indicator in text for indicator in org_indicators)

    def _is_location(self, text: str) -> bool:
        """Check if text references a location."""
        location_indicators = ['city', 'country', 'place', 'location', 'region', 'area']
        return any(indicator in text for indicator in location_indicators)

    def _is_temporal(self, text: str) -> bool:
        """Check if text references time."""
        temporal_indicators = ['time', 'date', 'period', 'duration', 'when', 'schedule']
        return any(indicator in text for indicator in temporal_indicators)

    def _is_process(self, text: str) -> bool:
        """Check if text describes a process."""
        process_indicators = ['process', 'procedure', 'method', 'workflow', 'algorithm', 'step']
        return any(indicator in text for indicator in process_indicators)

    def _infer_relationships(self, ontology: Ontology) -> None:
        """Infer semantic relationships using pattern matching."""
        nodes_list = list(ontology.nodes.values())

        for i, node_a in enumerate(nodes_list):
            for node_b in nodes_list[i+1:]:
                # Skip if already related
                if self._are_related(node_a, node_b, ontology):
                    continue

                # Check for causal relationships
                if self._has_causal_relationship(node_a, node_b):
                    edge = OntologyEdge(
                        source_id=node_a.id,
                        target_id=node_b.id,
                        edge_type="causes",
                        inferred=True,
                        strength=0.7
                    )
                    ontology.add_edge(edge)

                # Check for opposite relationships
                elif self._are_opposites(node_a, node_b):
                    edge = OntologyEdge(
                        source_id=node_a.id,
                        target_id=node_b.id,
                        edge_type="opposite_of",
                        inferred=True,
                        strength=0.8
                    )
                    ontology.add_edge(edge)

    def _are_related(self, node_a: OntologyNode, node_b: OntologyNode, ontology: Ontology) -> bool:
        """Check if two nodes are already related."""
        for edge in ontology.edges:
            if (edge.source_id == node_a.id and edge.target_id == node_b.id) or \
               (edge.source_id == node_b.id and edge.target_id == node_a.id):
                return True
        return False

    def _has_causal_relationship(self, node_a: OntologyNode, node_b: OntologyNode) -> bool:
        """Check if nodes have a causal relationship."""
        content_a = node_a.properties.get("content", "").lower()
        content_b = node_b.properties.get("content", "").lower()

        # Look for causal patterns
        causal_patterns = [
            r'causes?\s+',
            r'leads?\s+to',
            r'results?\s+in',
            r'produces?',
            r'creates?',
        ]

        for pattern in causal_patterns:
            if re.search(pattern, content_a) and node_b.label.lower() in content_a:
                return True
            if re.search(pattern, content_b) and node_a.label.lower() in content_b:
                return True

        return False

    def _are_opposites(self, node_a: OntologyNode, node_b: OntologyNode) -> bool:
        """Check if nodes are semantic opposites."""
        label_a = node_a.label.lower()
        label_b = node_b.label.lower()

        # Common antonym pairs
        antonyms = [
            ('hot', 'cold'), ('big', 'small'), ('high', 'low'),
            ('input', 'output'), ('start', 'end'), ('begin', 'finish'),
            ('create', 'destroy'), ('add', 'remove'), ('increase', 'decrease'),
            ('enable', 'disable'), ('open', 'close'), ('public', 'private'),
            ('read', 'write'), ('get', 'set'), ('push', 'pull'),
        ]

        for word1, word2 in antonyms:
            if (word1 in label_a and word2 in label_b) or \
               (word2 in label_a and word1 in label_b):
                return True

        return False

    def _add_cooccurrence_relationships(self, ontology: Ontology) -> None:
        """Add relationships based on co-occurrence in text."""
        # Group nodes by their parent (context)
        context_groups = {}
        for node in ontology.nodes.values():
            if node.parent_id:
                if node.parent_id not in context_groups:
                    context_groups[node.parent_id] = []
                context_groups[node.parent_id].append(node)

        # Add co-occurrence edges between siblings
        for parent_id, siblings in context_groups.items():
            if len(siblings) < 2:
                continue

            for i, node_a in enumerate(siblings):
                for node_b in siblings[i+1:]:
                    if not self._are_related(node_a, node_b, ontology):
                        # Add weak co-occurrence relationship
                        edge = OntologyEdge(
                            source_id=node_a.id,
                            target_id=node_b.id,
                            edge_type="related_to",
                            inferred=True,
                            strength=0.5,
                            dimension="cooccurrence"
                        )
                        ontology.add_edge(edge)

    def _add_similarity_relationships(self, ontology: Ontology) -> None:
        """Add relationships based on semantic similarity."""
        nodes_list = list(ontology.nodes.values())

        for i, node_a in enumerate(nodes_list):
            for node_b in nodes_list[i+1:]:
                if self._are_related(node_a, node_b, ontology):
                    continue

                # Calculate simple similarity based on label overlap
                similarity = self._calculate_similarity(node_a, node_b)

                if similarity > 0.6:
                    edge = OntologyEdge(
                        source_id=node_a.id,
                        target_id=node_b.id,
                        edge_type="similar_to",
                        inferred=True,
                        strength=similarity
                    )
                    ontology.add_edge(edge)

    def _calculate_similarity(self, node_a: OntologyNode, node_b: OntologyNode) -> float:
        """Calculate semantic similarity between nodes."""
        # Simple word overlap similarity
        words_a = set(node_a.label.lower().split())
        words_b = set(node_b.label.lower().split())

        if not words_a or not words_b:
            return 0.0

        intersection = len(words_a & words_b)
        union = len(words_a | words_b)

        jaccard = intersection / union if union > 0 else 0.0

        # Boost if stems match
        if node_a.stem and node_b.stem and node_a.stem == node_b.stem:
            jaccard = min(1.0, jaccard + 0.3)

        return jaccard
