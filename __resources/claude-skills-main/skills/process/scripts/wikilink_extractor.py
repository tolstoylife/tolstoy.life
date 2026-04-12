#!/usr/bin/env python3
"""
Wikilink Extractor
Extract all wikilinks from Obsidian vault files.

Supports:
- Standard wikilinks: [[Note Name]]
- Wikilinks with aliases: [[Note Name|Display Text]]
- Wikilinks with headers: [[Note Name#Header]]
- Wikilinks with blocks: [[Note Name^block-id]]
- Embedded files: ![[Image.png]]
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Set, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import logging

from batch_processor import BatchProcessor, ProcessingResult

logger = logging.getLogger(__name__)


@dataclass
class Wikilink:
    """Represents a single wikilink."""
    source_file: str  # Relative to vault root
    target: str  # The note/file being linked to
    display_text: Optional[str] = None  # Alias if present
    header: Optional[str] = None  # Header anchor if present
    block_id: Optional[str] = None  # Block ID if present
    is_embedded: bool = False  # Whether it's an embed (![[]])
    line_number: int = 0  # Line number in source file
    raw_link: str = ""  # Original link text


class WikilinkExtractor(BatchProcessor):
    """Extract wikilinks from Obsidian vault."""

    # Regex patterns for different wikilink types
    WIKILINK_PATTERN = re.compile(
        r'(!?\[\[)([^\]]+?)\]\]'
    )

    LINK_PARTS_PATTERN = re.compile(
        r'^([^#|\^]+?)(?:#([^|\^]+?))?(?:\^([^|]+?))?(?:\|(.+?))?$'
    )

    def __init__(self, vault_path: Path, dry_run: bool = False, verbose: bool = False):
        super().__init__(vault_path, dry_run, verbose)
        self.wikilinks: List[Wikilink] = []
        self.link_index: Dict[str, List[Wikilink]] = defaultdict(list)
        self.backlink_index: Dict[str, List[Wikilink]] = defaultdict(list)

    def parse_wikilink(self, match: re.Match, source_file: Path, line_number: int) -> Optional[Wikilink]:
        """Parse a wikilink match into a Wikilink object."""
        try:
            prefix = match.group(1)
            content = match.group(2).strip()
            is_embedded = prefix.startswith('!')

            # Parse link components
            parts_match = self.LINK_PARTS_PATTERN.match(content)
            if not parts_match:
                self.warnings.append(f"Could not parse wikilink '{content}' in {source_file}:{line_number}")
                return None

            target = parts_match.group(1).strip()
            header = parts_match.group(2).strip() if parts_match.group(2) else None
            block_id = parts_match.group(3).strip() if parts_match.group(3) else None
            display_text = parts_match.group(4).strip() if parts_match.group(4) else None

            # Get relative path from vault root
            source_rel = source_file.relative_to(self.vault_path).as_posix()

            return Wikilink(
                source_file=source_rel,
                target=target,
                display_text=display_text,
                header=header,
                block_id=block_id,
                is_embedded=is_embedded,
                line_number=line_number,
                raw_link=match.group(0)
            )
        except Exception as e:
            self.errors.append(f"Error parsing wikilink in {source_file}:{line_number}: {e}")
            return None

    def extract_from_file(self, file_path: Path) -> List[Wikilink]:
        """Extract all wikilinks from a single file."""
        content = self.read_file(file_path)
        if content is None:
            return []

        links = []
        for line_num, line in enumerate(content.split('\n'), start=1):
            # Skip code blocks and inline code
            if '```' in line or line.strip().startswith('    '):
                continue

            # Find all wikilinks in the line
            for match in self.WIKILINK_PATTERN.finditer(line):
                wikilink = self.parse_wikilink(match, file_path, line_num)
                if wikilink:
                    links.append(wikilink)

        return links

    def build_indices(self):
        """Build forward and backward link indices."""
        self.link_index.clear()
        self.backlink_index.clear()

        for link in self.wikilinks:
            # Forward links: source -> targets
            self.link_index[link.source_file].append(link)

            # Backlinks: target -> sources
            self.backlink_index[link.target].append(link)

    def get_statistics(self) -> Dict[str, Any]:
        """Calculate statistics about wikilinks."""
        total_links = len(self.wikilinks)
        embedded_links = sum(1 for link in self.wikilinks if link.is_embedded)
        links_with_aliases = sum(1 for link in self.wikilinks if link.display_text)
        links_with_headers = sum(1 for link in self.wikilinks if link.header)
        links_with_blocks = sum(1 for link in self.wikilinks if link.block_id)

        # Find most linked notes
        target_counts = defaultdict(int)
        for link in self.wikilinks:
            target_counts[link.target] += 1

        most_linked = sorted(
            target_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        # Find notes with most outgoing links
        source_counts = defaultdict(int)
        for link in self.wikilinks:
            source_counts[link.source_file] += 1

        most_outgoing = sorted(
            source_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        return {
            'total_links': total_links,
            'embedded_links': embedded_links,
            'links_with_aliases': links_with_aliases,
            'links_with_headers': links_with_headers,
            'links_with_blocks': links_with_blocks,
            'unique_targets': len(target_counts),
            'unique_sources': len(source_counts),
            'most_linked_notes': [
                {'note': note, 'backlinks': count}
                for note, count in most_linked
            ],
            'notes_with_most_links': [
                {'note': note, 'outgoing_links': count}
                for note, count in most_outgoing
            ]
        }

    def process(self, output_path: Optional[Path] = None, include_aliases: bool = False) -> ProcessingResult:
        """
        Extract wikilinks from all markdown files in vault.

        Args:
            output_path: Path to output JSON file
            include_aliases: Include alias information in output

        Returns:
            ProcessingResult with extraction results
        """
        logger.info(f"Extracting wikilinks from vault: {self.vault_path}")

        # Find all markdown files
        md_files = self.find_markdown_files()
        files_processed = 0

        # Extract wikilinks from each file
        for file_path in md_files:
            if self.verbose:
                logger.info(f"Processing {file_path.relative_to(self.vault_path)}")

            links = self.extract_from_file(file_path)
            self.wikilinks.extend(links)
            files_processed += 1

        # Build indices
        self.build_indices()

        # Get statistics
        stats = self.get_statistics()

        # Prepare output data
        output_data = {
            'vault_path': str(self.vault_path),
            'extraction_timestamp': ProcessingResult(
                success=True,
                files_processed=0,
                files_modified=0,
                errors=[],
                warnings=[],
                metadata={}
            ).timestamp,
            'statistics': stats,
            'links': [asdict(link) for link in self.wikilinks]
        }

        # Add indices if requested
        if include_aliases:
            output_data['link_index'] = {
                source: [asdict(link) for link in links]
                for source, links in self.link_index.items()
            }
            output_data['backlink_index'] = {
                target: [asdict(link) for link in links]
                for target, links in self.backlink_index.items()
            }

        # Write output file
        if output_path:
            if not self.dry_run:
                output_path.write_text(
                    json.dumps(output_data, indent=2),
                    encoding='utf-8'
                )
                logger.info(f"Wikilinks exported to {output_path}")
            else:
                logger.info(f"[DRY-RUN] Would export wikilinks to {output_path}")

        # Print summary
        logger.info(f"Extracted {stats['total_links']} wikilinks from {files_processed} files")
        logger.info(f"  - Embedded links: {stats['embedded_links']}")
        logger.info(f"  - Links with aliases: {stats['links_with_aliases']}")
        logger.info(f"  - Links with headers: {stats['links_with_headers']}")
        logger.info(f"  - Unique targets: {stats['unique_targets']}")

        return ProcessingResult(
            success=True,
            files_processed=files_processed,
            files_modified=0,
            errors=self.errors,
            warnings=self.warnings,
            metadata={
                'statistics': stats,
                'output_path': str(output_path) if output_path else None
            }
        )


def main():
    """Standalone execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Extract wikilinks from Obsidian vault')
    parser.add_argument('--vault', type=Path, required=True, help='Vault path')
    parser.add_argument('--output', type=Path, help='Output JSON file')
    parser.add_argument('--include-aliases', action='store_true', help='Include aliases')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    extractor = WikilinkExtractor(args.vault, verbose=args.verbose)
    result = extractor.process(
        output_path=args.output,
        include_aliases=args.include_aliases
    )

    print(json.dumps(asdict(result), indent=2))


if __name__ == '__main__':
    main()
