#!/usr/bin/env python3
"""
redundancy-detector.py
Detects redundant components using Jaccard similarity and PageRank analysis.
Part of the refactor skill infrastructure.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import re


def extract_text_from_file(file_path: Path) -> str:
    """Extract text content from markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove YAML frontmatter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Remove code blocks (preserve inline code)
        content = re.sub(r'```[^`]*```', '', content, flags=re.DOTALL)

        return content.lower()
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return ""


def tokenize(text: str) -> Set[str]:
    """Tokenize text into word set."""
    # Split on whitespace and punctuation
    words = re.findall(r'\b\w+\b', text)

    # Remove very short words and common stopwords
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    words = [w for w in words if len(w) > 2 and w not in stopwords]

    return set(words)


def jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    """Compute Jaccard similarity between two sets."""
    if not set_a or not set_b:
        return 0.0

    intersection = len(set_a & set_b)
    union = len(set_a | set_b)

    return intersection / union if union > 0 else 0.0


def find_redundant_pairs(
    components: Dict[str, Set[str]],
    threshold: float = 0.85
) -> List[Tuple[str, str, float]]:
    """Find component pairs with similarity above threshold."""
    redundant_pairs = []
    component_names = list(components.keys())

    for i, comp_a in enumerate(component_names):
        for comp_b in component_names[i+1:]:
            similarity = jaccard_similarity(components[comp_a], components[comp_b])

            if similarity >= threshold:
                redundant_pairs.append((comp_a, comp_b, similarity))

    # Sort by similarity (descending)
    redundant_pairs.sort(key=lambda x: x[2], reverse=True)

    return redundant_pairs


def extract_references(file_path: Path) -> Set[str]:
    """Extract references (@import, skill names, agent names) from file."""
    references = set()

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # @import references
        imports = re.findall(r'@import\s+([\w/./-]+)', content)
        references.update(imports)

        # agent: property
        agent_refs = re.findall(r'^agent:\s*([\w-]+)', content, re.MULTILINE)
        references.update(agent_refs)

        # Skill references in Task tool calls (approximate)
        task_refs = re.findall(r'Task.*?subagent_type.*?["\'](\w+)["\']', content, re.DOTALL)
        references.update(task_refs)

    except Exception as e:
        print(f"Error extracting references from {file_path}: {e}", file=sys.stderr)

    return references


def build_dependency_graph(component_files: List[Path]) -> Dict[str, Set[str]]:
    """Build dependency graph from component references."""
    graph = defaultdict(set)

    for file_path in component_files:
        component_name = file_path.stem
        references = extract_references(file_path)
        graph[component_name] = references

    return dict(graph)


def compute_pagerank(
    graph: Dict[str, Set[str]],
    damping: float = 0.85,
    max_iter: int = 100,
    tolerance: float = 1e-6
) -> Dict[str, float]:
    """Compute PageRank scores for components."""
    nodes = set(graph.keys())

    # Add referenced nodes that might not be in graph
    for refs in graph.values():
        nodes.update(refs)

    n = len(nodes)
    if n == 0:
        return {}

    # Initialize uniform distribution
    rank = {node: 1.0 / n for node in nodes}

    # Build reverse graph (incoming edges)
    reverse_graph = defaultdict(set)
    for node, refs in graph.items():
        for ref in refs:
            reverse_graph[ref].add(node)

    # Iterative PageRank
    for iteration in range(max_iter):
        new_rank = {}

        for node in nodes:
            # Teleportation term
            teleport = (1 - damping) / n

            # Weighted sum of incoming links
            incoming_sum = 0.0
            if node in reverse_graph:
                for incoming in reverse_graph[node]:
                    outgoing_count = len(graph.get(incoming, set()))
                    if outgoing_count > 0:
                        incoming_sum += rank[incoming] / outgoing_count

            new_rank[node] = teleport + damping * incoming_sum

        # Check convergence
        max_delta = max(abs(new_rank[n] - rank[n]) for n in nodes)
        if max_delta < tolerance:
            break

        rank = new_rank

    return rank


def main():
    parser = argparse.ArgumentParser(
        description='Detect redundant components using Jaccard similarity and PageRank'
    )
    parser.add_argument(
        'directory',
        type=Path,
        help='Directory to analyze (e.g., ~/.claude/skills)'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.85,
        help='Jaccard similarity threshold for redundancy (default: 0.85)'
    )
    parser.add_argument(
        '--pattern',
        type=str,
        default='*.md',
        help='File pattern to match (default: *.md)'
    )
    parser.add_argument(
        '--pagerank',
        action='store_true',
        help='Compute PageRank scores for prioritization'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )

    args = parser.parse_args()

    # Find all matching files
    component_files = list(args.directory.rglob(args.pattern))

    if not component_files:
        print(f"No files matching {args.pattern} found in {args.directory}", file=sys.stderr)
        return 1

    # Extract tokens from each file
    components = {}
    for file_path in component_files:
        text = extract_text_from_file(file_path)
        tokens = tokenize(text)

        if tokens:  # Only include non-empty files
            # Use relative path as component name
            rel_path = file_path.relative_to(args.directory)
            components[str(rel_path)] = tokens

    # Find redundant pairs
    redundant_pairs = find_redundant_pairs(components, args.threshold)

    # Compute PageRank if requested
    pagerank_scores = {}
    if args.pagerank:
        dep_graph = build_dependency_graph(component_files)
        pagerank_scores = compute_pagerank(dep_graph)

    # Output results
    if args.json:
        output = {
            'total_components': len(components),
            'redundant_pairs': [
                {
                    'component_a': a,
                    'component_b': b,
                    'similarity': round(sim, 4)
                }
                for a, b, sim in redundant_pairs
            ],
            'pagerank': {k: round(v, 6) for k, v in sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)} if pagerank_scores else None
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print(f"\n📊 Redundancy Analysis: {args.directory}")
        print(f"   Total components: {len(components)}")
        print(f"   Similarity threshold: {args.threshold}")
        print(f"   Redundant pairs found: {len(redundant_pairs)}\n")

        if redundant_pairs:
            print("🔄 Redundant Component Pairs:")
            for comp_a, comp_b, similarity in redundant_pairs[:20]:  # Show top 20
                print(f"   {similarity:.2%} similarity")
                print(f"     - {comp_a}")
                print(f"     - {comp_b}")
                print()

        if pagerank_scores:
            print("\n📈 PageRank Scores (Top 10):")
            top_scores = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:10]
            for component, score in top_scores:
                print(f"   {score:.6f}  {component}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
