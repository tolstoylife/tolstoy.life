#!/usr/bin/env python3
"""
Hallucination Validation — Three-Stage Claim Verification

Validates generated claims against source evidence using:
1. Citation presence check (regex)
2. Semantic entailment verification (embedding similarity)
3. LLM-as-judge validation (optional)
"""

import asyncio
import json
import re
import hashlib
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ValidationAction(Enum):
    INCLUDE = "include"         # Claim verified
    REMOVE = "remove"           # Claim is hallucination
    FLAG = "flag"               # Low confidence, include with warning
    REVIEW = "review"           # Needs human review


@dataclass
class Claim:
    text: str
    citation: Optional[str] = None
    source_content: Optional[str] = None
    claim_hash: str = ""

    def __post_init__(self):
        if not self.claim_hash:
            self.claim_hash = hashlib.md5(self.text.encode()).hexdigest()[:12]


@dataclass
class ValidationResult:
    claim: Claim
    stage_1_passed: bool  # Citation presence
    stage_2_passed: bool  # Semantic entailment
    stage_3_passed: Optional[bool] = None  # LLM verification
    similarity_score: float = 0.0
    action: ValidationAction = ValidationAction.INCLUDE
    reason: str = ""


@dataclass
class ValidationReport:
    total_claims: int
    verified_claims: int
    flagged_claims: int
    removed_claims: int
    hallucination_rate: float
    results: List[ValidationResult]
    passed: bool


# Citation patterns for Stage 1
CITATION_PATTERNS = [
    r'\[\^?\d+\]',                          # [1] or [^1]
    r'\[.+?\d{4}.+?\]',                     # [Author 2024]
    r'\([A-Z][a-z]+\s+et\s+al\.?,?\s*\d{4}\)',  # (Smith et al., 2024)
    r'\([A-Z][a-z]+,?\s*\d{4}\)',           # (Smith, 2024)
    r'p\.\s*\d+',                           # p. 123
    r'pp\.\s*\d+-\d+',                      # pp. 123-125
]


def extract_claims(text: str) -> List[Claim]:
    """Extract individual claims from text."""
    # Split by sentence, filtering out non-claim text
    sentences = re.split(r'(?<=[.!?])\s+', text)
    claims = []

    for sentence in sentences:
        sentence = sentence.strip()
        # Skip headers, bullets without content, very short sentences
        if len(sentence) < 20:
            continue
        if sentence.startswith('#'):
            continue
        if re.match(r'^[-*•]\s*$', sentence):
            continue

        # Extract citation if present
        citation = None
        for pattern in CITATION_PATTERNS:
            match = re.search(pattern, sentence)
            if match:
                citation = match.group(0)
                break

        claims.append(Claim(
            text=sentence,
            citation=citation
        ))

    return claims


def check_citation_presence(claim: Claim) -> bool:
    """Stage 1: Check if claim has any citation marker."""
    for pattern in CITATION_PATTERNS:
        if re.search(pattern, claim.text):
            return True
    return False


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two texts.

    In production, this would use embeddings (e.g., sentence-transformers).
    This is a simplified Jaccard + keyword overlap implementation.
    """
    # Tokenize
    def tokenize(text: str) -> set:
        # Remove punctuation and lowercase
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = set(text.split())
        # Remove stopwords (simplified)
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                     'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                     'of', 'in', 'to', 'for', 'with', 'on', 'at', 'by', 'from',
                     'and', 'or', 'but', 'if', 'then', 'that', 'this', 'these',
                     'those', 'it', 'its'}
        return words - stopwords

    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)

    if not tokens1 or not tokens2:
        return 0.0

    # Jaccard similarity
    intersection = tokens1 & tokens2
    union = tokens1 | tokens2

    jaccard = len(intersection) / len(union) if union else 0.0

    # Keyword coverage (how many claim keywords are in source)
    coverage = len(intersection) / len(tokens1) if tokens1 else 0.0

    # Weighted combination
    return round(jaccard * 0.4 + coverage * 0.6, 3)


def check_semantic_entailment(claim: Claim, sources: List[str],
                              threshold: float = 0.75) -> Tuple[bool, float]:
    """Stage 2: Check if claim is semantically entailed by sources."""
    if not sources:
        return False, 0.0

    max_similarity = 0.0

    for source in sources:
        similarity = calculate_similarity(claim.text, source)
        max_similarity = max(max_similarity, similarity)

        if similarity >= threshold:
            claim.source_content = source[:200]
            return True, similarity

    return False, max_similarity


async def check_llm_verification(claim: Claim, sources: List[str]) -> Tuple[bool, str]:
    """
    Stage 3: LLM-as-judge verification.

    In production, this would call an LLM API. Here we use a heuristic proxy.
    """
    # Simplified heuristic for demonstration
    # In production: call claude/gpt API with structured prompt

    claim_lower = claim.text.lower()

    # Red flags for hallucination
    red_flags = [
        r'\b(always|never|all|none|every|no one)\b',  # Absolute claims
        r'\b(proven|guaranteed|certainly|definitely)\b',  # Overconfidence
        r'\b(studies show|research proves|science confirms)\b',  # Vague authority
    ]

    has_red_flag = any(re.search(pattern, claim_lower) for pattern in red_flags)

    # Check if claim uses specific numbers or data
    has_specifics = bool(re.search(r'\d+(\.\d+)?%|\d+\s*(mg|ml|mmol|mcg)', claim_lower))

    # If has specifics but no source support, likely hallucination
    if has_specifics and claim.source_content is None:
        return False, "Specific data without source verification"

    if has_red_flag and claim.source_content is None:
        return False, "Absolute claim without source support"

    return True, "Passed heuristic checks"


def validate_claim(claim: Claim, sources: List[str],
                   entailment_threshold: float = 0.75,
                   run_stage_3: bool = False) -> ValidationResult:
    """Run full validation pipeline on a single claim."""

    # Stage 1: Citation presence
    stage_1_passed = check_citation_presence(claim)

    if not stage_1_passed:
        return ValidationResult(
            claim=claim,
            stage_1_passed=False,
            stage_2_passed=False,
            action=ValidationAction.REMOVE,
            reason="No citation present"
        )

    # Stage 2: Semantic entailment
    stage_2_passed, similarity = check_semantic_entailment(
        claim, sources, entailment_threshold
    )

    if not stage_2_passed:
        return ValidationResult(
            claim=claim,
            stage_1_passed=True,
            stage_2_passed=False,
            similarity_score=similarity,
            action=ValidationAction.FLAG,
            reason=f"Low semantic similarity: {similarity}"
        )

    # Optional Stage 3: LLM verification
    if run_stage_3:
        import asyncio
        stage_3_passed, reason = asyncio.get_event_loop().run_until_complete(
            check_llm_verification(claim, sources)
        )

        if not stage_3_passed:
            return ValidationResult(
                claim=claim,
                stage_1_passed=True,
                stage_2_passed=True,
                stage_3_passed=False,
                similarity_score=similarity,
                action=ValidationAction.REMOVE,
                reason=f"LLM verification failed: {reason}"
            )

        return ValidationResult(
            claim=claim,
            stage_1_passed=True,
            stage_2_passed=True,
            stage_3_passed=True,
            similarity_score=similarity,
            action=ValidationAction.INCLUDE,
            reason="All stages passed"
        )

    return ValidationResult(
        claim=claim,
        stage_1_passed=True,
        stage_2_passed=True,
        similarity_score=similarity,
        action=ValidationAction.INCLUDE,
        reason="Stages 1-2 passed"
    )


def validate_response(response_text: str, sources: List[str],
                      entailment_threshold: float = 0.75,
                      run_stage_3: bool = False) -> ValidationReport:
    """Validate all claims in a response against sources."""

    claims = extract_claims(response_text)
    results = []

    for claim in claims:
        result = validate_claim(
            claim, sources,
            entailment_threshold=entailment_threshold,
            run_stage_3=run_stage_3
        )
        results.append(result)

    # Calculate metrics
    verified = sum(1 for r in results if r.action == ValidationAction.INCLUDE)
    flagged = sum(1 for r in results if r.action == ValidationAction.FLAG)
    removed = sum(1 for r in results if r.action == ValidationAction.REMOVE)
    total = len(results)

    hallucination_rate = removed / total if total > 0 else 0.0

    # Determine if validation passed
    # Pass if < 20% hallucination rate and < 30% flagged
    passed = (hallucination_rate < 0.20) and ((flagged / total if total > 0 else 0) < 0.30)

    return ValidationReport(
        total_claims=total,
        verified_claims=verified,
        flagged_claims=flagged,
        removed_claims=removed,
        hallucination_rate=round(hallucination_rate, 3),
        results=results,
        passed=passed
    )


def format_output(report: ValidationReport, format: str = "json") -> str:
    """Format validation report for output."""

    if format == "json":
        output = {
            "passed": report.passed,
            "total_claims": report.total_claims,
            "verified": report.verified_claims,
            "flagged": report.flagged_claims,
            "removed": report.removed_claims,
            "hallucination_rate": report.hallucination_rate,
            "results": [
                {
                    "claim": r.claim.text[:100] + "..." if len(r.claim.text) > 100 else r.claim.text,
                    "citation": r.claim.citation,
                    "stages": {
                        "1_citation": r.stage_1_passed,
                        "2_entailment": r.stage_2_passed,
                        "3_llm": r.stage_3_passed
                    },
                    "similarity": r.similarity_score,
                    "action": r.action.value,
                    "reason": r.reason
                }
                for r in report.results
            ]
        }
        return json.dumps(output, indent=2)

    elif format == "summary":
        lines = [
            "━" * 50,
            "HALLUCINATION VALIDATION REPORT",
            "━" * 50,
            f"Status: {'✓ PASSED' if report.passed else '✗ FAILED'}",
            f"Total claims: {report.total_claims}",
            f"  Verified: {report.verified_claims}",
            f"  Flagged: {report.flagged_claims}",
            f"  Removed: {report.removed_claims}",
            f"Hallucination rate: {report.hallucination_rate * 100:.1f}%",
            "━" * 50,
        ]

        if report.removed_claims > 0:
            lines.append("REMOVED CLAIMS:")
            for r in report.results:
                if r.action == ValidationAction.REMOVE:
                    lines.append(f"  • {r.claim.text[:60]}...")
                    lines.append(f"    Reason: {r.reason}")

        return "\n".join(lines)

    return str(report)


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Hallucination Validation")
    parser.add_argument("--response", "-r", help="Response text to validate (or file path)")
    parser.add_argument("--sources", "-s", help="Sources JSON file")
    parser.add_argument("--threshold", type=float, default=0.75,
                        help="Entailment similarity threshold")
    parser.add_argument("--llm", action="store_true", help="Run Stage 3 LLM verification")
    parser.add_argument("--format", choices=["json", "summary"], default="summary")

    args = parser.parse_args()

    # Load response
    if args.response:
        if args.response.endswith('.txt') or args.response.endswith('.md'):
            with open(args.response) as f:
                response_text = f.read()
        else:
            response_text = args.response
    else:
        # Read from stdin
        response_text = sys.stdin.read()

    # Load sources
    sources = []
    if args.sources:
        with open(args.sources) as f:
            source_data = json.load(f)
            if isinstance(source_data, list):
                sources = [s.get("content", s) if isinstance(s, dict) else s
                          for s in source_data]
            elif isinstance(source_data, dict):
                sources = [s.get("content", "") for s in source_data.get("sources", [])]

    # Run validation
    report = validate_response(
        response_text,
        sources,
        entailment_threshold=args.threshold,
        run_stage_3=args.llm
    )

    print(format_output(report, args.format))

    # Exit with appropriate code
    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    asyncio.run(main())
