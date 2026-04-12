#!/usr/bin/env python3
"""
Task Classification Utility for Knowledge Orchestrator

Analyzes user requests and extracts multi-dimensional features for skill selection.
Can be used standalone for testing or integrated into orchestrator logic.

Usage:
    python task_classifier.py "Create a note about microservices"
    python task_classifier.py --file requests.txt
"""

import argparse
import json
import re
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


# Keyword Catalogs
OBSIDIAN_KEYWORDS = [
    "vault", "wikilink", "dataview", "frontmatter", "callout",
    "note", ".md", "mermaid", "templater", "obsidian"
]

REASONING_KEYWORDS = [
    "analyze", "strategic", "tactical", "decompose", "converge",
    "multi-level", "planning", "reasoning", "approach", "methodology"
]

GRAPH_KEYWORDS = [
    "entities", "relationships", "extract", "ontology", "schema",
    "knowledge graph", "mapping", "network", "connections", "links"
]


@dataclass
class TaskFeatures:
    """Multi-dimensional task feature representation"""
    content_type: str  # code, structured_data, prose, mixed
    artifact_type: str  # file, knowledge, analysis, visualization
    complexity_score: float  # 0.0-1.0
    creates_md_file: bool
    requires_extraction: bool
    requires_decomposition: bool
    obsidian_signals: int
    reasoning_signals: int
    graph_signals: int
    domain: str
    raw_request: str


class TaskClassifier:
    """Semantic task analysis for skill selection"""

    def __init__(self):
        self.obsidian_keywords = set(OBSIDIAN_KEYWORDS)
        self.reasoning_keywords = set(REASONING_KEYWORDS)
        self.graph_keywords = set(GRAPH_KEYWORDS)

    def analyze(self, request: str) -> TaskFeatures:
        """Extract all task features from request"""
        request_lower = request.lower()

        return TaskFeatures(
            content_type=self._classify_content_type(request),
            artifact_type=self._classify_artifact_type(request),
            complexity_score=self._calculate_complexity(request),
            creates_md_file=self._detects_file_creation(request_lower),
            requires_extraction=self._requires_extraction(request_lower),
            requires_decomposition=self._requires_decomposition(request_lower),
            obsidian_signals=self._count_keywords(request_lower, self.obsidian_keywords),
            reasoning_signals=self._count_keywords(request_lower, self.reasoning_keywords),
            graph_signals=self._count_keywords(request_lower, self.graph_keywords),
            domain=self._detect_domain(request),
            raw_request=request
        )

    def _classify_content_type(self, request: str) -> str:
        """Classify content type: code, structured_data, prose, mixed"""
        has_code = any(marker in request for marker in ["```", "function", "class ", "def ", "import "])
        has_structure = any(marker in request for marker in ["json", "yaml", "table", "csv"])
        has_prose = len(request.split()) > 10  # Sufficient text

        if has_code and has_prose:
            return "mixed"
        elif has_code:
            return "code"
        elif has_structure:
            return "structured_data"
        else:
            return "prose"

    def _classify_artifact_type(self, request: str) -> str:
        """Classify desired artifact: file, knowledge, analysis, visualization"""
        request_lower = request.lower()

        file_indicators = ["create", "note", "document", ".md", "file"]
        knowledge_indicators = ["extract", "entities", "relationships", "knowledge"]
        analysis_indicators = ["analyze", "decompose", "understand", "evaluate"]
        viz_indicators = ["visualize", "diagram", "chart", "graph"]

        scores = {
            "file": sum(1 for ind in file_indicators if ind in request_lower),
            "knowledge": sum(1 for ind in knowledge_indicators if ind in request_lower),
            "analysis": sum(1 for ind in analysis_indicators if ind in request_lower),
            "visualization": sum(1 for ind in viz_indicators if ind in request_lower)
        }

        return max(scores, key=scores.get) if max(scores.values()) > 0 else "file"

    def _calculate_complexity(self, request: str) -> float:
        """Calculate complexity score 0.0-1.0"""
        # Factors contributing to complexity
        num_steps = self._count_action_verbs(request)
        num_domains = self._count_distinct_domains(request)
        abstraction_level = self._detect_abstraction_level(request)

        # Weighted combination
        step_score = min(num_steps / 5.0, 1.0) * 0.4
        domain_score = min(num_domains / 3.0, 1.0) * 0.3
        abstraction_score = abstraction_level * 0.3

        return min(step_score + domain_score + abstraction_score, 1.0)

    def _count_action_verbs(self, request: str) -> int:
        """Count action verbs indicating multiple steps"""
        action_verbs = [
            "create", "analyze", "extract", "build", "design", "implement",
            "decompose", "structure", "format", "visualize", "map", "identify"
        ]
        return sum(1 for verb in action_verbs if verb in request.lower())

    def _count_distinct_domains(self, request: str) -> int:
        """Count distinct knowledge domains mentioned"""
        domains = [
            "software", "architecture", "database", "network", "security",
            "machine learning", "data science", "business", "finance", "research"
        ]
        return sum(1 for domain in domains if domain in request.lower())

    def _detect_abstraction_level(self, request: str) -> float:
        """Detect abstraction level: 0.0 (concrete) to 1.0 (abstract)"""
        abstract_indicators = ["strategic", "conceptual", "theoretical", "framework", "paradigm"]
        concrete_indicators = ["specific", "example", "implementation", "code", "exact"]

        request_lower = request.lower()
        abstract_count = sum(1 for ind in abstract_indicators if ind in request_lower)
        concrete_count = sum(1 for ind in concrete_indicators if ind in request_lower)

        if abstract_count > concrete_count:
            return 0.7 + (0.3 * abstract_count / len(abstract_indicators))
        elif concrete_count > 0:
            return 0.3 - (0.3 * concrete_count / len(concrete_indicators))
        else:
            return 0.5  # Neutral

    def _detects_file_creation(self, request_lower: str) -> bool:
        """Check if request involves creating a file"""
        file_creation_patterns = [
            "create a note", "create note", "make a note", "new note",
            "create a file", "new file", "create .md", ".md file"
        ]
        return any(pattern in request_lower for pattern in file_creation_patterns)

    def _requires_extraction(self, request_lower: str) -> bool:
        """Check if request requires entity/knowledge extraction"""
        extraction_indicators = [
            "extract", "identify entities", "relationships", "ontology",
            "knowledge graph", "entities and", "map connections"
        ]
        return any(indicator in request_lower for indicator in extraction_indicators)

    def _requires_decomposition(self, request_lower: str) -> bool:
        """Check if request requires hierarchical decomposition"""
        decomposition_indicators = [
            "decompose", "break down", "analyze", "strategic analysis",
            "multi-level", "levels of", "comprehensive analysis"
        ]
        return any(indicator in request_lower for indicator in decomposition_indicators)

    def _count_keywords(self, request_lower: str, keyword_set: set) -> int:
        """Count occurrences of keywords from set"""
        count = 0
        for keyword in keyword_set:
            if keyword in request_lower:
                count += 1
        return count

    def _detect_domain(self, request: str) -> str:
        """Detect primary domain of request"""
        domain_keywords = {
            "software": ["code", "programming", "software", "application", "api"],
            "data": ["data", "database", "analytics", "metrics"],
            "research": ["research", "paper", "study", "academic"],
            "business": ["business", "strategy", "market", "customer"],
            "technical": ["system", "architecture", "infrastructure", "technology"]
        }

        request_lower = request.lower()
        domain_scores = {}

        for domain, keywords in domain_keywords.items():
            domain_scores[domain] = sum(1 for kw in keywords if kw in request_lower)

        detected_domain = max(domain_scores, key=domain_scores.get)
        return detected_domain if domain_scores[detected_domain] > 0 else "general"


def main():
    """CLI interface for task classification"""
    parser = argparse.ArgumentParser(
        description="Analyze user requests to extract task features for skill selection"
    )
    parser.add_argument(
        "request",
        nargs="?",
        help="User request to analyze"
    )
    parser.add_argument(
        "--file", "-f",
        help="File containing requests (one per line)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    classifier = TaskClassifier()

    if args.file:
        # Process file of requests
        with open(args.file, 'r') as f:
            requests = [line.strip() for line in f if line.strip()]

        results = []
        for request in requests:
            features = classifier.analyze(request)
            results.append(asdict(features))

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for i, (request, result) in enumerate(zip(requests, results), 1):
                print(f"\n{'='*80}")
                print(f"Request {i}: {request[:70]}...")
                print(f"{'='*80}")
                print_features(result)

    elif args.request:
        # Process single request
        features = classifier.analyze(args.request)

        if args.json:
            print(json.dumps(asdict(features), indent=2))
        else:
            print(f"\n{'='*80}")
            print(f"Request: {args.request}")
            print(f"{'='*80}")
            print_features(asdict(features))
    else:
        parser.print_help()


def print_features(features: Dict[str, Any]):
    """Pretty-print task features"""
    print(f"\nContent Type: {features['content_type']}")
    print(f"Artifact Type: {features['artifact_type']}")
    print(f"Complexity Score: {features['complexity_score']:.2f}")
    print(f"\nSignals:")
    print(f"  Creates MD File: {features['creates_md_file']}")
    print(f"  Requires Extraction: {features['requires_extraction']}")
    print(f"  Requires Decomposition: {features['requires_decomposition']}")
    print(f"\nKeyword Counts:")
    print(f"  Obsidian: {features['obsidian_signals']}")
    print(f"  Reasoning: {features['reasoning_signals']}")
    print(f"  Graph: {features['graph_signals']}")
    print(f"\nDomain: {features['domain']}")


if __name__ == "__main__":
    main()
