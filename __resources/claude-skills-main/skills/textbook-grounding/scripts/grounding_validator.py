#!/usr/bin/env python3
"""
Textbook Grounding Validator

Validates SAQ/VIVA responses for proper textbook grounding,
citation coverage, and examiner optimization.
"""

import re
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    valid: bool
    word_count: int
    citation_count: int
    issues: list[str]
    warnings: list[str]


def count_words(text: str) -> int:
    """Count words excluding YAML frontmatter and markdown formatting."""
    # Remove YAML frontmatter
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    # Remove footnote definitions
    text = re.sub(r'\[\^\d+\]:.*$', '', text, flags=re.MULTILINE)
    # Remove markdown formatting
    text = re.sub(r'[#*`>\[\]|]', ' ', text)
    # Count words
    words = text.split()
    return len(words)


def count_citations(text: str) -> int:
    """Count unique footnote references."""
    refs = re.findall(r'\[\^(\d+)\]', text)
    return len(set(refs))


def check_citation_definitions(text: str) -> list[str]:
    """Verify all referenced citations have definitions."""
    issues = []
    refs = set(re.findall(r'\[\^(\d+)\](?!:)', text))
    defs = set(re.findall(r'\[\^(\d+)\]:', text))

    undefined = refs - defs
    if undefined:
        issues.append(f"Undefined citations: {sorted(undefined)}")

    unused = defs - refs
    if unused:
        issues.append(f"Unused citation definitions: {sorted(unused)}")

    return issues


def check_citation_format(text: str) -> list[str]:
    """Verify citation format includes page numbers."""
    issues = []
    defs = re.findall(r'\[\^\d+\]:(.+)$', text, re.MULTILINE)

    for defn in defs:
        if not re.search(r'p\.?\s*\d+', defn, re.IGNORECASE):
            # Extract first 50 chars for identification
            preview = defn[:50].strip()
            issues.append(f"Citation missing page number: '{preview}...'")

    return issues


def check_cascades(text: str) -> list[str]:
    """Check for preserved cascades vs decomposed ones."""
    warnings = []

    # Good: cascades with →
    cascade_count = len(re.findall(r'→.*→', text))

    # Potentially bad: sequential bullet points that might be decomposed cascades
    bullets = re.findall(r'^[-•]\s*(.+)$', text, re.MULTILINE)
    if len(bullets) > 10 and cascade_count < 2:
        warnings.append(
            f"High bullet count ({len(bullets)}) with few cascades ({cascade_count}). "
            "Consider consolidating into → chains."
        )

    return warnings


def check_values_context(text: str) -> list[str]:
    """Check that numerical values have clinical context."""
    warnings = []

    # Find isolated values (number + unit without surrounding context)
    # This is a heuristic - may have false positives
    isolated = re.findall(
        r'(?<![→←↑↓])\b(\d+(?:\.\d+)?)\s*(mg|kg|L|ml|min|h|s|mmHg|%)\b(?![→←])',
        text
    )

    if len(isolated) > 5:
        warnings.append(
            f"Found {len(isolated)} potentially isolated values. "
            "Ensure all values have clinical context."
        )

    return warnings


def check_symbol_usage(text: str) -> list[str]:
    """Verify symbol lexicon is used."""
    warnings = []

    # Expected symbols
    expected = ['→', '↑', '↓']
    verbose_alternatives = ['leads to', 'causes', 'increases', 'decreases']

    for alt in verbose_alternatives:
        if alt.lower() in text.lower():
            warnings.append(
                f"Consider replacing '{alt}' with symbol lexicon (→, ↑, ↓)"
            )

    # Check symbol presence
    symbol_count = sum(text.count(s) for s in expected)
    if symbol_count < 3:
        warnings.append(
            f"Low symbol usage ({symbol_count}). Consider using →, ↑, ↓ for cascades."
        )

    return warnings


def validate_response(text: str, mode: str = "saq") -> ValidationResult:
    """
    Full validation of grounded response.

    Args:
        text: The response text to validate
        mode: "saq" (180-220 words) or "viva" (500-800 words)
    """
    issues = []
    warnings = []

    # Word count
    word_count = count_words(text)
    if mode == "saq":
        if word_count < 180:
            issues.append(f"Word count too low: {word_count} < 180")
        elif word_count > 220:
            issues.append(f"Word count too high: {word_count} > 220")
    elif mode == "viva":
        if word_count < 500:
            issues.append(f"Word count too low: {word_count} < 500")
        elif word_count > 800:
            warnings.append(f"Word count high: {word_count} > 800")

    # Citation count
    citation_count = count_citations(text)
    if citation_count < 3:
        issues.append(f"Insufficient citations: {citation_count} < 3")

    # Citation definitions
    issues.extend(check_citation_definitions(text))

    # Citation format
    warnings.extend(check_citation_format(text))

    # Cascade preservation
    warnings.extend(check_cascades(text))

    # Values context
    warnings.extend(check_values_context(text))

    # Symbol usage
    warnings.extend(check_symbol_usage(text))

    return ValidationResult(
        valid=len(issues) == 0,
        word_count=word_count,
        citation_count=citation_count,
        issues=issues,
        warnings=warnings
    )


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python grounding_validator.py <file_or_text> [--mode saq|viva] [--strict]")
        sys.exit(1)

    input_arg = sys.argv[1]
    mode = "saq"
    strict = False

    if "--mode" in sys.argv:
        idx = sys.argv.index("--mode")
        if idx + 1 < len(sys.argv):
            mode = sys.argv[idx + 1]

    if "--strict" in sys.argv:
        strict = True

    # Read input
    if input_arg.endswith('.md'):
        with open(input_arg, 'r') as f:
            text = f.read()
    else:
        text = input_arg

    # Validate
    result = validate_response(text, mode)

    # Output
    print(f"\n{'='*60}")
    print(f"TEXTBOOK GROUNDING VALIDATION")
    print(f"{'='*60}")
    print(f"Mode: {mode.upper()}")
    print(f"Word count: {result.word_count}")
    print(f"Citations: {result.citation_count}")
    print(f"Valid: {'✓ PASS' if result.valid else '✗ FAIL'}")

    if result.issues:
        print(f"\nISSUES ({len(result.issues)}):")
        for issue in result.issues:
            print(f"  ✗ {issue}")

    if result.warnings:
        print(f"\nWARNINGS ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  ⚠ {warning}")

    if strict and (result.issues or result.warnings):
        sys.exit(1)
    elif result.issues:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
