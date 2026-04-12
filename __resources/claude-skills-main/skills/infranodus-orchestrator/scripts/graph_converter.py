#!/usr/bin/env python3
"""
Graph Converter for InfraNodus Orchestrator

Converts InfraNodus graph format to local knowledge-graph JSON format
with provenance tracking and confidence mapping.

Usage:
    python graph_converter.py infranodus_output.json local_graph.json
"""

import sys
import json
from datetime import datetime
from typing import Dict, List


def normalize_name(name: str) -> str:
    """Normalize entity name for ID generation."""
    return name.lower().replace(' ', '_').replace('-', '_')


def derive_confidence_from_centrality(centrality: float) -> float:
    """Map InfraNodus centrality score to local confidence score."""
    # InfraNodus centrality is typically 0-1, map to confidence
    # High centrality = high confidence in entity importance
    return min(1.0, max(0.5, centrality))


def convert_infranodus_to_local(infranodus_data: Dict, graph_name: str) -> Dict:
    """Convert InfraNodus output to local knowledge graph format."""
    timestamp = datetime.now().isoformat()

    entities = []
    relationships = []

    # Extract topical clusters and create concept entities
    if 'topical_clusters' in infranodus_data:
        for cluster in infranodus_data['topical_clusters']:
            cluster_id = cluster.get('cluster_id', 0)
            cluster_theme = cluster.get('cluster_name', f"Cluster {cluster_id}")

            # Get concepts from cluster
            concepts = cluster.get('main_concepts', [])

            for concept in concepts:
                # Get centrality score if available
                centrality = 0.7  # default
                if 'main_concepts' in infranodus_data:
                    concept_data = infranodus_data['main_concepts'].get(concept, {})
                    centrality = concept_data.get('centrality', 0.7)

                entity = {
                    'id': f"concept_{normalize_name(concept)}",
                    'type': 'Concept',
                    'name': concept,
                    'confidence': derive_confidence_from_centrality(centrality),
                    'provenance': {
                        'source': 'InfraNodus',
                        'graph_name': graph_name,
                        'cluster_id': cluster_id,
                        'extraction_date': timestamp
                    },
                    'properties': {
                        'cluster': cluster_theme,
                        'centrality': centrality
                    }
                }
                entities.append(entity)

    # Extract relationships from co-occurrences
    if 'main_concepts' in infranodus_data:
        processed_pairs = set()

        for concept1, concept1_data in infranodus_data['main_concepts'].items():
            # Get co-occurrence information
            co_occurrences = concept1_data.get('co_occurrences', [])

            for concept2 in co_occurrences:
                # Avoid duplicate relationships
                pair = tuple(sorted([concept1, concept2]))
                if pair in processed_pairs:
                    continue
                processed_pairs.add(pair)

                relationship = {
                    'source': f"concept_{normalize_name(concept1)}",
                    'target': f"concept_{normalize_name(concept2)}",
                    'type': 'CO_OCCURS_WITH',
                    'confidence': 0.75,  # Default confidence for co-occurrence
                    'properties': {
                        'relationship_type': 'semantic_association',
                        'derived_from': 'InfraNodus co-occurrence analysis'
                    }
                }
                relationships.append(relationship)

    # Create local graph structure
    local_graph = {
        'metadata': {
            'source': 'InfraNodus',
            'original_graph': graph_name,
            'conversion_date': timestamp,
            'converter_version': '1.0.0'
        },
        'entities': entities,
        'relationships': relationships,
        'statistics': {
            'total_entities': len(entities),
            'total_relationships': len(relationships),
            'average_confidence': sum(e['confidence'] for e in entities) / len(entities) if entities else 0
        }
    }

    return local_graph


def main():
    if len(sys.argv) < 3:
        print("Usage: python graph_converter.py infranodus_output.json local_graph.json [graph_name]")
        sys.exit(1)

    infranodus_file = sys.argv[1]
    local_file = sys.argv[2]
    graph_name = sys.argv[3] if len(sys.argv) > 3 else "unnamed_graph"

    # Load InfraNodus output
    with open(infranodus_file, 'r') as f:
        infranodus_data = json.load(f)

    # Convert to local format
    local_graph = convert_infranodus_to_local(infranodus_data, graph_name)

    # Save local graph
    with open(local_file, 'w') as f:
        json.dump(local_graph, f, indent=2)

    print(f"Converted InfraNodus graph to local format:")
    print(f"  Entities: {local_graph['statistics']['total_entities']}")
    print(f"  Relationships: {local_graph['statistics']['total_relationships']}")
    print(f"  Average confidence: {local_graph['statistics']['average_confidence']:.2f}")
    print(f"  Saved to: {local_file}")


if __name__ == '__main__':
    main()
