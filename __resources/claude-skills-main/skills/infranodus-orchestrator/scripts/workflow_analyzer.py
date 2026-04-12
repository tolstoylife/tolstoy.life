#!/usr/bin/env python3
"""
Workflow Analyzer for InfraNodus Orchestrator

Analyzes user requests to extract task features and calculate confidence scores
for workflow pattern selection.

Usage:
    python workflow_analyzer.py "user request text"
"""

import sys
import re
import json
from typing import Dict, List, Tuple

# Keyword catalogs for pattern detection
KEYWORDS = {
    'infranodus_specific': ['infranodus', 'topical cluster', 'content gap', 'research question'],
    'seo_keywords': ['seo', 'optimize', 'search', 'ranking', 'keywords', 'serp'],
    'comparison_keywords': ['compare', 'difference', 'overlap', 'similarity', 'contrast'],
    'development_keywords': ['develop', 'refine', 'expand', 'iterate', 'deepen', 'elaborate'],
    'search_keywords': ['google', 'search results', 'queries', 'serp', 'trends'],
    'gap_keywords': ['gap', 'missing', 'underexplored', 'latent'],
    'research_keywords': ['research', 'analysis', 'comprehensive', 'explore', 'investigate']
}

# Workflow pattern triggers
PATTERNS = {
    'pattern_1': {  # Deep Research & Gap Analysis
        'name': 'Deep Research & Gap Analysis',
        'required_keywords': ['research_keywords', 'gap_keywords'],
        'optional_keywords': ['infranodus_specific'],
        'min_complexity': 0.7,
        'base_confidence': 0.85
    },
    'pattern_2': {  # SEO Content Optimization
        'name': 'SEO Content Optimization',
        'required_keywords': ['seo_keywords'],
        'optional_keywords': ['search_keywords'],
        'min_complexity': 0.5,
        'base_confidence': 0.85
    },
    'pattern_3': {  # Comparative Text Analysis
        'name': 'Comparative Text Analysis',
        'required_keywords': ['comparison_keywords'],
        'optional_keywords': [],
        'min_complexity': 0.6,
        'base_confidence': 0.80
    },
    'pattern_4': {  # Iterative Topic Development
        'name': 'Iterative Topic Development',
        'required_keywords': ['development_keywords'],
        'optional_keywords': ['gap_keywords'],
        'min_complexity': 0.6,
        'base_confidence': 0.75
    },
    'pattern_5': {  # Google Search Intelligence
        'name': 'Google Search Intelligence',
        'required_keywords': ['search_keywords'],
        'optional_keywords': ['seo_keywords'],
        'min_complexity': 0.5,
        'base_confidence': 0.85
    }
}


def extract_features(request: str) -> Dict:
    """Extract task features from user request."""
    request_lower = request.lower()

    # Count keyword matches
    keyword_matches = {}
    for category, keywords in KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in request_lower)
        keyword_matches[category] = matches

    # Detect content type
    content_type = 'single_text'
    if any(word in request_lower for word in ['multiple', 'compare', 'several', 'texts']):
        content_type = 'multiple_texts'
    elif any(word in request_lower for word in ['search', 'google', 'queries']):
        content_type = 'search_queries'

    # Calculate complexity score
    complexity_factors = {
        'multi_step': 0.3 if any(word in request_lower for word in ['comprehensive', 'analyze', 'research']) else 0,
        'integration': 0.3 if keyword_matches['infranodus_specific'] > 0 else 0,
        'strategic': 0.2 if any(word in request_lower for word in ['strategy', 'plan', 'roadmap']) else 0,
        'documentation': 0.2 if any(word in request_lower for word in ['document', 'note', 'report']) else 0
    }
    complexity_score = sum(complexity_factors.values())

    return {
        'content_type': content_type,
        'keyword_matches': keyword_matches,
        'complexity_score': min(1.0, complexity_score),
        'request_length': len(request.split())
    }


def calculate_pattern_confidence(features: Dict, pattern_config: Dict) -> float:
    """Calculate confidence score for a specific pattern."""
    score_components = {
        'keyword_match': 0.0,
        'complexity_alignment': 0.0,
        'base': pattern_config['base_confidence']
    }

    # Keyword matching (30% weight)
    required_matches = 0
    for req_category in pattern_config['required_keywords']:
        if features['keyword_matches'].get(req_category, 0) > 0:
            required_matches += 1

    if len(pattern_config['required_keywords']) > 0:
        keyword_score = required_matches / len(pattern_config['required_keywords'])
    else:
        keyword_score = 1.0

    score_components['keyword_match'] = keyword_score * 0.30

    # Complexity alignment (25% weight)
    complexity_delta = abs(features['complexity_score'] - pattern_config['min_complexity'])
    complexity_alignment = max(0, 1 - complexity_delta)
    score_components['complexity_alignment'] = complexity_alignment * 0.25

    # Calculate final confidence
    final_confidence = (
        pattern_config['base_confidence'] * 0.45 +  # Base confidence (45%)
        score_components['keyword_match'] +          # Keyword match (30%)
        score_components['complexity_alignment']     # Complexity (25%)
    )

    return min(1.0, final_confidence)


def analyze_request(request: str) -> Dict:
    """Analyze user request and recommend workflow pattern."""
    features = extract_features(request)

    # Calculate confidence for each pattern
    pattern_scores = {}
    for pattern_id, pattern_config in PATTERNS.items():
        confidence = calculate_pattern_confidence(features, pattern_config)
        pattern_scores[pattern_id] = {
            'name': pattern_config['name'],
            'confidence': confidence
        }

    # Sort by confidence
    sorted_patterns = sorted(
        pattern_scores.items(),
        key=lambda x: x[1]['confidence'],
        reverse=True
    )

    # Recommendation
    top_pattern = sorted_patterns[0]
    recommendation = {
        'action': 'execute_immediately' if top_pattern[1]['confidence'] >= 0.90 else
                  'execute_with_note' if top_pattern[1]['confidence'] >= 0.70 else
                  'present_options' if top_pattern[1]['confidence'] >= 0.50 else
                  'ask_clarification'
    }

    return {
        'features': features,
        'pattern_scores': {k: v for k, v in sorted_patterns},
        'recommendation': recommendation,
        'top_pattern': top_pattern[0],
        'top_confidence': top_pattern[1]['confidence']
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python workflow_analyzer.py \"user request text\"")
        sys.exit(1)

    request = ' '.join(sys.argv[1:])
    analysis = analyze_request(request)

    print(json.dumps(analysis, indent=2))


if __name__ == '__main__':
    main()
