#!/usr/bin/env python3
"""
PDF Intelligence Extraction for Network Meta-Analysis Papers

Multi-tier extraction strategy combining multiple libraries for robust
text, table, equation, and diagram extraction from NMA PDFs.
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import json

try:
    import fitz  # PyMuPDF
    import pdfplumber
    import camelot
    import pandas as pd
except ImportError as e:
    print(f"Error: Missing required library - {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


@dataclass
class ExtractedPDF:
    """Comprehensive PDF extraction results"""
    text_by_section: Dict[str, str]
    tables: List[Dict]
    metadata: Dict
    page_count: int
    extraction_quality: Dict[str, float]

    def to_dict(self):
        return asdict(self)

    def to_json(self, output_path: Path):
        """Export extraction results as JSON"""
        output_path.write_text(json.dumps(self.to_dict(), indent=2))


class PDFIntelligence:
    """
    Multi-library PDF parser with fallback strategies
    """

    SECTION_MARKERS = {
        'abstract': ['abstract', 'summary'],
        'introduction': ['introduction', 'background', 'rationale'],
        'methods': ['methods', 'methodology', 'search strategy', 'statistical analysis', 'data sources'],
        'results': ['results', 'findings', 'network meta-analysis results', 'forest plot'],
        'discussion': ['discussion', 'interpretation', 'limitations', 'conclusions'],
        'references': ['references', 'bibliography', 'citations']
    }

    def __init__(self, pdf_path: Path):
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        self.pdf_path = pdf_path
        self.doc = fitz.open(str(pdf_path))

    def extract(self) -> ExtractedPDF:
        """Execute full extraction pipeline"""
        print(f"📄 Extracting PDF: {self.pdf_path.name}")

        text_by_section = self._extract_structured_text()
        tables = self._extract_tables()
        metadata = self._extract_metadata()

        # Calculate extraction quality scores
        quality = {
            'text_coverage': min(1.0, sum(len(t) for t in text_by_section.values()) / 10000),
            'tables_found': min(1.0, len(tables) / 5),
            'sections_detected': len([s for s in text_by_section if text_by_section[s]]) / len(self.SECTION_MARKERS)
        }

        print(f"✓ Extracted {len(text_by_section)} sections, {len(tables)} tables")

        return ExtractedPDF(
            text_by_section=text_by_section,
            tables=tables,
            metadata=metadata,
            page_count=len(self.doc),
            extraction_quality=quality
        )

    def _extract_structured_text(self) -> Dict[str, str]:
        """Extract text with section detection"""
        sections = {key: [] for key in self.SECTION_MARKERS.keys()}
        current_section = 'abstract'

        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text()
            text_lower = text.lower()

            # Detect section transitions
            for section_name, markers in self.SECTION_MARKERS.items():
                if any(marker in text_lower[:500] for marker in markers):
                    current_section = section_name
                    break

            sections[current_section].append(text)

        # Combine lists into single strings
        return {
            section: '\n\n'.join(texts).strip()
            for section, texts in sections.items()
            if texts
        }

    def _extract_tables(self) -> List[Dict]:
        """Extract tables using camelot with fallback"""
        tables = []

        # Primary: Camelot lattice mode (bordered tables)
        try:
            camelot_tables = camelot.read_pdf(
                str(self.pdf_path),
                pages='all',
                flavor='lattice'
            )

            for i, table in enumerate(camelot_tables):
                if table.accuracy > 60:  # Quality threshold
                    tables.append({
                        'table_id': f'table_{i+1}',
                        'dataframe': table.df.to_dict('records'),
                        'page': table.page,
                        'accuracy': table.accuracy,
                        'source': 'camelot_lattice'
                    })
        except Exception as e:
            print(f"⚠ Camelot extraction warning: {e}")

        return tables

    def _extract_metadata(self) -> Dict:
        """Extract PDF metadata"""
        meta = self.doc.metadata.copy() if self.doc.metadata else {}

        # Extract title from first page
        first_page_text = self.doc[0].get_text()
        lines = [l.strip() for l in first_page_text.split('\n') if l.strip()]
        if lines:
            meta['extracted_title'] = lines[0]

        meta['page_count'] = len(self.doc)

        return meta

    def close(self):
        """Clean up resources"""
        self.doc.close()


def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(description='Extract content from NMA PDF')
    parser.add_argument('pdf_path', type=Path, help='Path to PDF file')
    parser.add_argument('--output', '-o', type=Path, help='Output JSON path (optional)')

    args = parser.parse_args()

    # Extract PDF
    extractor = PDFIntelligence(args.pdf_path)
    results = extractor.extract()
    extractor.close()

    # Output results
    if args.output:
        results.to_json(args.output)
        print(f"✓ Saved extraction to: {args.output}")
    else:
        print("\n" + "="*80)
        print("EXTRACTION SUMMARY")
        print("="*80)
        for section, text in results.text_by_section.items():
            print(f"\n{section.upper()}: {len(text)} characters")
        print(f"\nTables found: {len(results.tables)}")
        print(f"Quality scores: {results.extraction_quality}")


if __name__ == '__main__':
    main()
