#!/usr/bin/env python3
"""
Semantic similarity deduplication for skill results
Uses simple text-based similarity (can be enhanced with embeddings)
"""
import sys
import json
from typing import List, Dict
import re
from collections import Counter
import math


def normalize_text(text: str) -> str:
    """Normalize text for comparison"""
    # Lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def tokenize(text: str) -> List[str]:
    """Simple word tokenization"""
    return normalize_text(text).split()


def cosine_similarity(text1: str, text2: str) -> float:
    """
    Calculate cosine similarity between two texts
    Uses simple word frequency vectors (bag-of-words)

    Returns:
        Similarity score between 0 and 1
    """
    # Tokenize
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)

    # Build word frequency vectors
    counter1 = Counter(tokens1)
    counter2 = Counter(tokens2)

    # Get union of all words
    all_words = set(counter1.keys()) | set(counter2.keys())

    # Calculate dot product and magnitudes
    dot_product = sum(counter1[word] * counter2[word] for word in all_words)
    magnitude1 = math.sqrt(sum(count ** 2 for count in counter1.values()))
    magnitude2 = math.sqrt(sum(count ** 2 for count in counter2.values()))

    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def deduplicate_skills(skills: List[Dict], threshold: float = 0.85, key: str = "description") -> List[Dict]:
    """
    Remove semantically similar skills from results

    Args:
        skills: List of skill dictionaries
        threshold: Similarity threshold (0-1), higher = more strict
        key: Dictionary key to use for comparison (default: 'description')

    Returns:
        Deduplicated list of skills
    """
    if not skills:
        return []

    deduplicated = []
    seen_texts = []

    for skill in skills:
        if key not in skill:
            # If key doesn't exist, keep the skill
            deduplicated.append(skill)
            continue

        text = skill[key]
        is_duplicate = False

        # Check against all previously seen texts
        for seen_text in seen_texts:
            similarity = cosine_similarity(text, seen_text)
            if similarity >= threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            deduplicated.append(skill)
            seen_texts.append(text)

    removed_count = len(skills) - len(deduplicated)
    if removed_count > 0:
        print(f"🔍 Removed {removed_count} semantically similar skill(s) (threshold: {threshold})", file=sys.stderr)

    return deduplicated


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: semantic_similarity.py <skills.json> [--threshold=0.85] [--key=description]")
        print("Example: semantic_similarity.py results.json --threshold=0.90")
        print()
        print("Input JSON format: [{\"name\": \"...\", \"description\": \"...\"}, ...]")
        sys.exit(1)

    input_file = sys.argv[1]
    threshold = 0.85
    key = "description"

    # Parse arguments
    for arg in sys.argv[2:]:
        if arg.startswith("--threshold="):
            threshold = float(arg.split("=")[1])
        elif arg.startswith("--key="):
            key = arg.split("=")[1]

    try:
        # Read input
        if input_file == "-":
            data = json.load(sys.stdin)
        else:
            with open(input_file, 'r') as f:
                data = json.load(f)

        # Deduplicate
        deduplicated = deduplicate_skills(data, threshold, key)

        # Output
        print(json.dumps(deduplicated, indent=2))

    except FileNotFoundError:
        print(f"❌ File not found: {input_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
