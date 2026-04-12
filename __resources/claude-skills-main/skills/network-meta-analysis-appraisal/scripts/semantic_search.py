#!/usr/bin/env python3
"""
Semantic Evidence Matching for Checklist Items

Maps checklist criteria to PDF content using semantic similarity
to automatically locate supporting evidence.
"""

from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
import json

try:
    from sentence_transformers import SentenceTransformer, util
    import torch
except ImportError:
    print("Error: Install sentence-transformers")
    print("Run: pip install sentence-transformers")
    import sys
    sys.exit(1)


@dataclass
class EvidenceMatch:
    """Single evidence match result"""
    criterion_id: str
    criterion_text: str
    matched_text: str
    source_section: str
    similarity_score: float
    confidence_level: str  # high, moderate, low, unable

    def to_dict(self):
        return {
            'criterion_id': self.criterion_id,
            'criterion_text': self.criterion_text,
            'matched_text': self.matched_text[:300],  # Truncate for readability
            'source_section': self.source_section,
            'similarity_score': round(self.similarity_score, 3),
            'confidence_level': self.confidence_level
        }


class SemanticMatcher:
    """
    Semantic similarity-based evidence matching
    """

    # Confidence thresholds
    HIGH_CONFIDENCE = 0.75
    MODERATE_CONFIDENCE = 0.55
    LOW_CONFIDENCE = 0.35

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize with sentence transformer model

        Args:
            model_name: HuggingFace model name (default: lightweight general-purpose)
        """
        print(f"Loading semantic model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def search_evidence(
        self,
        criterion: Dict[str, str],
        pdf_sections: Dict[str, str],
        top_k: int = 3
    ) -> List[EvidenceMatch]:
        """
        Search PDF content for evidence matching a checklist criterion

        Args:
            criterion: Dict with 'id' and 'text' keys
            pdf_sections: Dict mapping section names to text content
            top_k: Number of top matches to return

        Returns:
            List of EvidenceMatch objects, sorted by similarity
        """
        criterion_embedding = self.model.encode(
            criterion['text'],
            convert_to_tensor=True
        )

        matches = []

        # Search each section
        for section_name, section_text in pdf_sections.items():
            if not section_text or len(section_text) < 50:
                continue

            # Split into paragraphs
            paragraphs = [
                p.strip()
                for p in section_text.split('\n\n')
                if len(p.strip()) > 50
            ]

            # Encode paragraphs
            if not paragraphs:
                continue

            paragraph_embeddings = self.model.encode(
                paragraphs,
                convert_to_tensor=True
            )

            # Calculate similarities
            similarities = util.cos_sim(
                criterion_embedding,
                paragraph_embeddings
            )[0]

            # Get best match from this section
            best_idx = similarities.argmax().item()
            best_score = similarities[best_idx].item()

            matches.append(EvidenceMatch(
                criterion_id=criterion['id'],
                criterion_text=criterion['text'],
                matched_text=paragraphs[best_idx],
                source_section=section_name,
                similarity_score=best_score,
                confidence_level=self._classify_confidence(best_score)
            ))

        # Sort by similarity and return top-k
        matches.sort(key=lambda x: x.similarity_score, reverse=True)
        return matches[:top_k]

    def _classify_confidence(self, score: float) -> str:
        """Classify confidence level from similarity score"""
        if score >= self.HIGH_CONFIDENCE:
            return 'high'
        elif score >= self.MODERATE_CONFIDENCE:
            return 'moderate'
        elif score >= self.LOW_CONFIDENCE:
            return 'low'
        else:
            return 'unable'

    def batch_search(
        self,
        criteria: List[Dict[str, str]],
        pdf_sections: Dict[str, str]
    ) -> List[List[EvidenceMatch]]:
        """
        Search evidence for multiple criteria

        Args:
            criteria: List of dicts with 'id' and 'text' keys
            pdf_sections: PDF content by section

        Returns:
            List of evidence matches for each criterion
        """
        print(f"Searching evidence for {len(criteria)} criteria...")

        results = []
        for i, criterion in enumerate(criteria):
            matches = self.search_evidence(criterion, pdf_sections, top_k=1)
            results.append(matches)

            if (i + 1) % 10 == 0:
                print(f"  Processed {i+1}/{len(criteria)} criteria")

        return results


def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(description='Search PDF for checklist evidence')
    parser.add_argument('pdf_json', type=Path, help='PDF extraction JSON')
    parser.add_argument('criteria_json', type=Path, help='Checklist criteria JSON')
    parser.add_argument('--output', '-o', type=Path, help='Output results JSON')

    args = parser.parse_args()

    # Load inputs
    pdf_data = json.loads(args.pdf_json.read_text())
    criteria = json.loads(args.criteria_json.read_text())

    # Initialize matcher
    matcher = SemanticMatcher()

    # Search evidence
    results = matcher.batch_search(
        criteria=criteria,
        pdf_sections=pdf_data['text_by_section']
    )

    # Format output
    output = [
        {
            'criterion': criteria[i],
            'evidence': [m.to_dict() for m in matches]
        }
        for i, matches in enumerate(results)
    ]

    # Save or print
    if args.output:
        args.output.write_text(json.dumps(output, indent=2))
        print(f"✓ Saved results to: {args.output}")
    else:
        for item in output[:5]:  # Show first 5
            print(f"\n{item['criterion']['id']}: {item['evidence'][0]['confidence_level']}")


if __name__ == '__main__':
    main()
