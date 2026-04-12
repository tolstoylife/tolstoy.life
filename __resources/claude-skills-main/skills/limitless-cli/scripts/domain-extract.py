#!/usr/bin/env python3
"""
Domain-specific extraction script for Limitless CLI.
Configurable pattern matching for domain entities.

Usage:
    python domain-extract.py --domain medical --input lifelogs.json
    python domain-extract.py --patterns patterns.yaml --input lifelogs.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any

# Built-in domain patterns
DOMAIN_PATTERNS = {
    "medical": {
        "5HT3 antagonist": ["ondansetron", "granisetron", "palonosetron"],
        "Dopamine antagonist": ["droperidol", "metoclopramide", "prochlorperazine", "domperidone"],
        "Antihistamine (H1)": ["cyclizine", "promethazine", "dimenhydrinate"],
        "Corticosteroid": ["dexamethasone", "methylprednisolone"],
        "NK1 antagonist": ["aprepitant", "fosaprepitant"],
        "Adjunct": ["propofol", "midazolam"],
    },
    "technical": {
        "Programming Language": ["python", "typescript", "javascript", "rust", "go"],
        "Framework": ["react", "vue", "angular", "nextjs", "fastapi"],
        "Database": ["postgresql", "mongodb", "redis", "falkordb", "neo4j"],
        "Cloud": ["aws", "gcp", "azure", "kubernetes", "docker"],
    },
    "business": {
        "Meeting Type": ["standup", "retrospective", "planning", "review"],
        "Action Type": ["deadline", "deliverable", "milestone", "blocker"],
        "Stakeholder": ["client", "customer", "partner", "vendor"],
    },
}


def load_patterns(domain: str = None, patterns_file: str = None) -> Dict[str, List[str]]:
    """Load patterns from domain or custom file."""
    if patterns_file:
        with open(patterns_file) as f:
            import yaml
            return yaml.safe_load(f)
    elif domain and domain in DOMAIN_PATTERNS:
        return DOMAIN_PATTERNS[domain]
    else:
        print(f"Available domains: {', '.join(DOMAIN_PATTERNS.keys())}")
        sys.exit(1)


def extract_entities(text: str, patterns: Dict[str, List[str]]) -> Dict[str, List[Dict]]:
    """Extract entities matching patterns from text."""
    results = {}
    text_lower = text.lower()

    for category, keywords in patterns.items():
        matches = []
        for keyword in keywords:
            pattern = re.compile(rf'\b{re.escape(keyword)}\b', re.IGNORECASE)
            found = pattern.findall(text)
            if found:
                matches.append({
                    "keyword": keyword,
                    "count": len(found),
                    "category": category,
                })
        if matches:
            results[category] = matches

    return results


def process_lifelogs(lifelogs: List[Dict], patterns: Dict[str, List[str]]) -> Dict[str, Any]:
    """Process multiple lifelogs and aggregate results."""
    all_entities = {}
    lifelog_matches = []

    for lifelog in lifelogs:
        content = lifelog.get("markdown", "") or lifelog.get("title", "")
        entities = extract_entities(content, patterns)

        if entities:
            lifelog_matches.append({
                "id": lifelog.get("id"),
                "title": lifelog.get("title"),
                "entities": entities,
            })

            # Aggregate by category
            for category, matches in entities.items():
                if category not in all_entities:
                    all_entities[category] = {}
                for match in matches:
                    key = match["keyword"]
                    if key not in all_entities[category]:
                        all_entities[category][key] = 0
                    all_entities[category][key] += match["count"]

    return {
        "total_lifelogs": len(lifelogs),
        "matching_lifelogs": len(lifelog_matches),
        "aggregated_entities": all_entities,
        "matches": lifelog_matches,
    }


def main():
    parser = argparse.ArgumentParser(description="Domain-specific entity extraction")
    parser.add_argument("--domain", choices=list(DOMAIN_PATTERNS.keys()),
                        help="Use built-in domain patterns")
    parser.add_argument("--patterns", type=str,
                        help="Path to custom patterns YAML file")
    parser.add_argument("--input", type=str, required=True,
                        help="Input JSON file with lifelogs")
    parser.add_argument("--output", type=str,
                        help="Output JSON file (default: stdout)")
    parser.add_argument("--format", choices=["json", "summary"], default="json",
                        help="Output format")

    args = parser.parse_args()

    # Load patterns
    patterns = load_patterns(args.domain, args.patterns)

    # Load lifelogs
    with open(args.input) as f:
        data = json.load(f)

    # Handle both array and object with 'items' or 'data'
    if isinstance(data, list):
        lifelogs = data
    elif isinstance(data, dict):
        lifelogs = data.get("items") or data.get("data") or []
    else:
        lifelogs = []

    # Process
    results = process_lifelogs(lifelogs, patterns)

    # Output
    if args.format == "summary":
        print(f"Processed {results['total_lifelogs']} lifelogs")
        print(f"Found matches in {results['matching_lifelogs']} lifelogs")
        print("\nAggregated Entities:")
        for category, entities in results['aggregated_entities'].items():
            print(f"\n{category}:")
            for entity, count in sorted(entities.items(), key=lambda x: -x[1]):
                print(f"  - {entity}: {count}")
    else:
        output = json.dumps(results, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
        else:
            print(output)


if __name__ == "__main__":
    main()
