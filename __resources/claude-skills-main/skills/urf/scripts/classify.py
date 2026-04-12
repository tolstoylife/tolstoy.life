#!/usr/bin/env python3
"""
URF Complexity Classifier

Routes queries to optimal pipelines based on multi-factor scoring.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class Pipeline(Enum):
    R0 = 0  # Direct response
    R1 = 1  # Single skill
    R2 = 2  # Skill composition
    R3 = 3  # Full orchestration

@dataclass
class ClassificationResult:
    pipeline: Pipeline
    score: float
    confidence: float
    rationale: str
    holons: List[str]
    tools: List[str]

# Domain detection patterns
DOMAIN_PATTERNS = {
    "technical": r"\b(code|api|database|algorithm|system|architecture)\b",
    "medical": r"\b(health|medical|symptom|diagnosis|treatment|patient)\b",
    "legal": r"\b(law|legal|contract|regulation|compliance|liability)\b",
    "financial": r"\b(finance|investment|market|trading|portfolio|risk)\b",
    "scientific": r"\b(research|study|experiment|hypothesis|evidence|data)\b",
    "strategic": r"\b(strategy|planning|decision|analysis|evaluation)\b",
}

# Verification triggers
VERIFICATION_PATTERNS = [
    r"\b(latest|current|recent|today|now|2025|2024)\b",
    r"\b(still|anymore|yet|currently)\b",
    r"\b(who is|what is the current)\b",
]

# Trivial query patterns
TRIVIAL_PATTERNS = [
    r"^(what is|define|explain)\s+\w+\??$",
    r"^\d+\s*[\+\-\*\/]\s*\d+",
    r"^(hi|hello|hey|thanks|thank you)",
]

def detect_domains(query: str) -> List[str]:
    """Identify active domains in query."""
    query_lower = query.lower()
    domains = []
    for domain, pattern in DOMAIN_PATTERNS.items():
        if re.search(pattern, query_lower, re.IGNORECASE):
            domains.append(domain)
    return domains

def estimate_reasoning_depth(query: str) -> int:
    """Estimate required reasoning depth (1-5)."""
    depth = 1
    
    # Depth indicators
    if any(w in query.lower() for w in ["why", "how", "explain", "analyze"]):
        depth += 1
    if any(w in query.lower() for w in ["compare", "contrast", "evaluate", "assess"]):
        depth += 1
    if any(w in query.lower() for w in ["design", "create", "develop", "build"]):
        depth += 1
    if any(w in query.lower() for w in ["optimize", "improve", "recommend", "strategy"]):
        depth += 1
    if len(query.split()) > 50:  # Long queries usually complex
        depth += 1
        
    return min(depth, 5)

def is_high_stakes(query: str) -> bool:
    """Check for high-stakes indicators."""
    high_stakes_patterns = [
        r"\b(critical|urgent|emergency|important|crucial)\b",
        r"\b(decision|choose|select|recommend)\b.*\b(should|must|need)\b",
        r"\b(health|safety|security|legal|financial)\b",
    ]
    return any(
        re.search(p, query, re.IGNORECASE) 
        for p in high_stakes_patterns
    )

def requires_verification(query: str) -> bool:
    """Check if query needs fact verification."""
    return any(
        re.search(p, query, re.IGNORECASE)
        for p in VERIFICATION_PATTERNS
    )

def is_trivial(query: str) -> bool:
    """Check if query is trivial."""
    return any(
        re.match(p, query.strip(), re.IGNORECASE)
        for p in TRIVIAL_PATTERNS
    )

def classify(query: str) -> ClassificationResult:
    """
    Classify query and route to appropriate pipeline.
    
    Score = domains×2 + depth×3 + stakes×1.5 + verification×2
    """
    # Fast path for trivial queries
    if is_trivial(query):
        return ClassificationResult(
            pipeline=Pipeline.R0,
            score=0.0,
            confidence=0.95,
            rationale="Trivial query - direct response",
            holons=[],
            tools=[]
        )
    
    # Calculate score components
    domains = detect_domains(query)
    depth = estimate_reasoning_depth(query)
    stakes = is_high_stakes(query)
    verification = requires_verification(query)
    
    score = (
        len(domains) * 2 +
        depth * 3 +
        (1.5 if stakes else 0) +
        (2 if verification else 0)
    )
    
    # Apply stakes multiplier
    if stakes and ("medical" in domains or "legal" in domains):
        score *= 1.5
    
    # Route to pipeline
    if score < 2:
        pipeline = Pipeline.R0
        holons = []
        tools = []
        rationale = "Simple query - direct response"
    elif score < 4:
        pipeline = Pipeline.R1
        holons = ["ρ"]  # reason only
        tools = []
        rationale = "Single skill sufficient"
    elif score < 8:
        pipeline = Pipeline.R2
        holons = ["ρ", "θ", "γ", "η"]
        tools = ["infranodus"] if depth > 2 else []
        rationale = "Multi-skill composition needed"
    else:
        pipeline = Pipeline.R3
        holons = ["ρ", "θ", "ω", "γ", "η", "κ", "α", "ν", "β", "χ"]
        tools = ["infranodus", "exa", "clear-thought"]
        rationale = "Full orchestration required"
    
    # Override for verification requests
    if verification and pipeline.value < 3:
        pipeline = Pipeline.R3
        rationale += " (escalated for verification)"
    
    confidence = min(0.95, 0.7 + (score / 20))
    
    return ClassificationResult(
        pipeline=pipeline,
        score=score,
        confidence=confidence,
        rationale=rationale,
        holons=holons,
        tools=tools
    )

def main():
    """Example usage."""
    test_queries = [
        "What is 2+2?",
        "Explain the concept of machine learning",
        "Compare and analyze the strategic implications of entering the European market",
        "What is the current stock price of Apple?",
        "Design a sustainable urban transportation system that balances environmental impact with accessibility",
    ]
    
    for query in test_queries:
        result = classify(query)
        print(f"\nQuery: {query[:60]}...")
        print(f"  Pipeline: {result.pipeline.name}")
        print(f"  Score: {result.score:.1f}")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Holons: {result.holons}")
        print(f"  Rationale: {result.rationale}")

if __name__ == "__main__":
    main()
