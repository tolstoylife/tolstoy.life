#!/usr/bin/env python3
"""
Vault Analyzer
Generate comprehensive statistics and health reports for Obsidian vaults.

Provides:
- File and link statistics
- Tag usage analysis
- Orphaned notes detection
- Broken link detection
- Vault health scoring
- Growth trends
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Set, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
from datetime import datetime
import logging

from batch_processor import BatchProcessor, ProcessingResult

logger = logging.getLogger(__name__)


@dataclass
class VaultStatistics:
    """Comprehensive vault statistics."""
    # File statistics
    total_files: int
    markdown_files: int
    attachment_files: int
    total_size_bytes: int

    # Content statistics
    total_words: int
    total_lines: int
    average_note_length: int

    # Link statistics
    total_wikilinks: int
    total_backlinks: int
    broken_links: int
    orphaned_notes: int

    # Tag statistics
    total_tags: int
    unique_tags: int
    most_used_tags: List[Tuple[str, int]]

    # Frontmatter statistics
    notes_with_frontmatter: int
    common_frontmatter_keys: List[Tuple[str, int]]

    # Health score (0-100)
    health_score: float

    # Timestamp
    generated_at: str


class VaultAnalyzer(BatchProcessor):
    """Analyze Obsidian vault and generate reports."""

    WIKILINK_PATTERN = re.compile(r'(!?\[\[)([^\]]+?)\]\]')
    INLINE_TAG_PATTERN = re.compile(r'(?:^|\s)#([\w/-]+)')
    FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL | re.MULTILINE)

    def __init__(self, vault_path: Path, dry_run: bool = False, verbose: bool = False):
        super().__init__(vault_path, dry_run, verbose)
        self.statistics: Optional[VaultStatistics] = None
        self.note_links: Dict[str, Set[str]] = defaultdict(set)
        self.backlinks: Dict[str, Set[str]] = defaultdict(set)
        self.broken_links: List[Tuple[str, str]] = []
        self.orphaned_notes: List[str] = []

    def get_file_statistics(self) -> Dict[str, Any]:
        """Get file-level statistics."""
        md_files = list(self.vault_path.glob('**/*.md'))
        attachment_patterns = ['**/*.png', '**/*.jpg', '**/*.jpeg', '**/*.gif', '**/*.pdf']
        attachment_files = []
        for pattern in attachment_patterns:
            attachment_files.extend(self.vault_path.glob(pattern))

        total_size = sum(f.stat().st_size for f in md_files if f.is_file())

        return {
            'total_files': len(md_files) + len(attachment_files),
            'markdown_files': len(md_files),
            'attachment_files': len(attachment_files),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        }

    def get_content_statistics(self, md_files: List[Path]) -> Dict[str, Any]:
        """Get content-level statistics."""
        total_words = 0
        total_lines = 0

        for file_path in md_files:
            content = self.read_file(file_path)
            if content:
                # Count lines
                lines = content.split('\n')
                total_lines += len(lines)

                # Count words (rough estimate)
                words = content.split()
                total_words += len(words)

        avg_length = total_words // len(md_files) if md_files else 0

        return {
            'total_words': total_words,
            'total_lines': total_lines,
            'average_note_length': avg_length
        }

    def extract_links(self, content: str, file_path: Path) -> List[str]:
        """Extract wikilinks from content."""
        links = []
        for match in self.WIKILINK_PATTERN.finditer(content):
            link_content = match.group(2)
            # Extract just the target, ignoring aliases and anchors
            target = link_content.split('|')[0].split('#')[0].strip()
            if target:
                links.append(target)
        return links

    def build_link_graph(self, md_files: List[Path]) -> None:
        """Build graph of links and backlinks."""
        self.note_links.clear()
        self.backlinks.clear()

        for file_path in md_files:
            content = self.read_file(file_path)
            if not content:
                continue

            source = file_path.stem
            links = self.extract_links(content, file_path)

            for target in links:
                self.note_links[source].add(target)
                self.backlinks[target].add(source)

    def find_broken_links(self, md_files: List[Path]) -> List[Tuple[str, str]]:
        """Find broken wikilinks."""
        broken = []
        note_names = {f.stem for f in md_files}

        for source, targets in self.note_links.items():
            for target in targets:
                if target not in note_names:
                    broken.append((source, target))

        return broken

    def find_orphaned_notes(self, md_files: List[Path]) -> List[str]:
        """Find notes with no incoming or outgoing links."""
        orphaned = []
        note_names = {f.stem for f in md_files}

        for note in note_names:
            has_incoming = note in self.backlinks and self.backlinks[note]
            has_outgoing = note in self.note_links and self.note_links[note]

            if not has_incoming and not has_outgoing:
                orphaned.append(note)

        return orphaned

    def get_link_statistics(self, md_files: List[Path]) -> Dict[str, Any]:
        """Get link-level statistics."""
        self.build_link_graph(md_files)
        self.broken_links = self.find_broken_links(md_files)
        self.orphaned_notes = self.find_orphaned_notes(md_files)

        total_links = sum(len(targets) for targets in self.note_links.values())

        # Find most linked notes
        backlink_counts = {
            note: len(sources)
            for note, sources in self.backlinks.items()
        }
        most_linked = sorted(
            backlink_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        return {
            'total_wikilinks': total_links,
            'total_backlinks': len(self.backlinks),
            'broken_links': len(self.broken_links),
            'orphaned_notes': len(self.orphaned_notes),
            'most_linked_notes': [
                {'note': note, 'backlinks': count}
                for note, count in most_linked
            ],
            'broken_link_details': [
                {'source': src, 'target': tgt}
                for src, tgt in self.broken_links[:20]  # Limit to 20
            ],
            'orphaned_note_list': self.orphaned_notes[:20]  # Limit to 20
        }

    def get_tag_statistics(self, md_files: List[Path]) -> Dict[str, Any]:
        """Get tag usage statistics."""
        tag_counter = Counter()

        for file_path in md_files:
            content = self.read_file(file_path)
            if not content:
                continue

            # Extract inline tags
            for match in self.INLINE_TAG_PATTERN.finditer(content):
                tag = match.group(1)
                tag_counter[tag] += 1

        most_used = tag_counter.most_common(20)

        return {
            'total_tags': sum(tag_counter.values()),
            'unique_tags': len(tag_counter),
            'most_used_tags': [
                {'tag': tag, 'count': count}
                for tag, count in most_used
            ]
        }

    def get_frontmatter_statistics(self, md_files: List[Path]) -> Dict[str, Any]:
        """Get frontmatter usage statistics."""
        notes_with_fm = 0
        key_counter = Counter()

        for file_path in md_files:
            content = self.read_file(file_path)
            if not content:
                continue

            match = self.FRONTMATTER_PATTERN.match(content)
            if match:
                notes_with_fm += 1
                try:
                    import yaml
                    frontmatter = yaml.safe_load(match.group(1))
                    if frontmatter:
                        for key in frontmatter.keys():
                            key_counter[key] += 1
                except:
                    pass

        common_keys = key_counter.most_common(10)

        return {
            'notes_with_frontmatter': notes_with_fm,
            'frontmatter_usage_percent': round(
                (notes_with_fm / len(md_files) * 100) if md_files else 0,
                2
            ),
            'common_frontmatter_keys': [
                {'key': key, 'count': count}
                for key, count in common_keys
            ]
        }

    def calculate_health_score(self, stats: Dict[str, Any]) -> float:
        """
        Calculate vault health score (0-100).

        Factors:
        - Broken links (penalty)
        - Orphaned notes (penalty)
        - Frontmatter usage (bonus)
        - Tag usage (bonus)
        - Link density (bonus)
        """
        score = 100.0

        md_count = stats['markdown_files']
        if md_count == 0:
            return 0.0

        # Broken links penalty (max -30)
        broken_ratio = stats['broken_links'] / md_count
        score -= min(broken_ratio * 100, 30)

        # Orphaned notes penalty (max -20)
        orphaned_ratio = stats['orphaned_notes'] / md_count
        score -= min(orphaned_ratio * 100, 20)

        # Frontmatter usage bonus (max +10)
        fm_ratio = stats['notes_with_frontmatter'] / md_count
        score += min(fm_ratio * 10, 10)

        # Tag usage bonus (max +10)
        if stats['unique_tags'] > 0:
            score += min((stats['unique_tags'] / md_count) * 50, 10)

        # Link density bonus (max +10)
        avg_links = stats['total_wikilinks'] / md_count if md_count else 0
        score += min(avg_links * 2, 10)

        return max(0.0, min(100.0, score))

    def generate_markdown_report(self, stats: Dict[str, Any]) -> str:
        """Generate a markdown report."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        report = f"""# Vault Analysis Report

Generated: {timestamp}
Vault: {self.vault_path}

## Health Score: {stats['health_score']:.1f}/100

## File Statistics

- **Total Files**: {stats['total_files']:,}
- **Markdown Files**: {stats['markdown_files']:,}
- **Attachment Files**: {stats['attachment_files']:,}
- **Total Size**: {stats['total_size_mb']:.2f} MB

## Content Statistics

- **Total Words**: {stats['total_words']:,}
- **Total Lines**: {stats['total_lines']:,}
- **Average Note Length**: {stats['average_note_length']:,} words

## Link Statistics

- **Total Wikilinks**: {stats['total_wikilinks']:,}
- **Broken Links**: {stats['broken_links']:,} ⚠️
- **Orphaned Notes**: {stats['orphaned_notes']:,} ⚠️

"""

        if stats.get('broken_link_details'):
            report += "### Broken Links (Sample)\n\n"
            for item in stats['broken_link_details'][:10]:
                report += f"- `{item['source']}` → `{item['target']}`\n"
            report += "\n"

        if stats.get('orphaned_note_list'):
            report += "### Orphaned Notes (Sample)\n\n"
            for note in stats['orphaned_note_list'][:10]:
                report += f"- `{note}`\n"
            report += "\n"

        if stats.get('most_linked_notes'):
            report += "### Most Linked Notes\n\n"
            for item in stats['most_linked_notes'][:10]:
                report += f"- `{item['note']}` ({item['backlinks']} backlinks)\n"
            report += "\n"

        report += f"""## Tag Statistics

- **Total Tags**: {stats['total_tags']:,}
- **Unique Tags**: {stats['unique_tags']:,}

"""

        if stats.get('most_used_tags'):
            report += "### Most Used Tags\n\n"
            for item in stats['most_used_tags'][:10]:
                report += f"- `#{item['tag']}` ({item['count']} uses)\n"
            report += "\n"

        report += f"""## Frontmatter Statistics

- **Notes with Frontmatter**: {stats['notes_with_frontmatter']:,} ({stats.get('frontmatter_usage_percent', 0)}%)

"""

        if stats.get('common_frontmatter_keys'):
            report += "### Common Frontmatter Keys\n\n"
            for item in stats['common_frontmatter_keys']:
                report += f"- `{item['key']}` ({item['count']} notes)\n"
            report += "\n"

        report += """
## Recommendations

"""

        if stats['broken_links'] > 0:
            report += f"- 🔴 Fix {stats['broken_links']} broken links\n"

        if stats['orphaned_notes'] > 10:
            report += f"- 🟡 Review {stats['orphaned_notes']} orphaned notes\n"

        if stats.get('frontmatter_usage_percent', 0) < 50:
            report += "- 🟡 Consider adding frontmatter to more notes for better organization\n"

        if stats['health_score'] >= 80:
            report += "- 🟢 Vault is in excellent condition!\n"
        elif stats['health_score'] >= 60:
            report += "- 🟡 Vault is in good condition with room for improvement\n"
        else:
            report += "- 🔴 Vault needs attention to improve health\n"

        return report

    def process(
        self,
        report_path: Optional[Path] = None,
        report_format: str = 'md'
    ) -> ProcessingResult:
        """
        Analyze vault and generate report.

        Args:
            report_path: Path to output report file
            report_format: Report format ('md', 'json', 'html')

        Returns:
            ProcessingResult with analysis results
        """
        logger.info(f"Analyzing vault: {self.vault_path}")

        # Find all markdown files
        md_files = self.find_markdown_files()

        # Gather statistics
        file_stats = self.get_file_statistics()
        content_stats = self.get_content_statistics(md_files)
        link_stats = self.get_link_statistics(md_files)
        tag_stats = self.get_tag_statistics(md_files)
        fm_stats = self.get_frontmatter_statistics(md_files)

        # Combine all statistics
        all_stats = {
            **file_stats,
            **content_stats,
            **link_stats,
            **tag_stats,
            **fm_stats
        }

        # Calculate health score
        all_stats['health_score'] = self.calculate_health_score(all_stats)
        all_stats['generated_at'] = datetime.now().isoformat()

        # Generate report
        if report_path:
            if report_format == 'md':
                report_content = self.generate_markdown_report(all_stats)
            elif report_format == 'json':
                report_content = json.dumps(all_stats, indent=2)
            else:
                self.errors.append(f"Unsupported report format: {report_format}")
                report_content = ""

            if report_content and not self.dry_run:
                report_path.write_text(report_content, encoding='utf-8')
                logger.info(f"Report written to {report_path}")
            elif report_content:
                logger.info(f"[DRY-RUN] Would write report to {report_path}")

        # Log summary
        logger.info(f"Vault Health Score: {all_stats['health_score']:.1f}/100")
        logger.info(f"Files: {all_stats['markdown_files']:,} markdown, {all_stats['attachment_files']:,} attachments")
        logger.info(f"Links: {all_stats['total_wikilinks']:,} total, {all_stats['broken_links']:,} broken")
        logger.info(f"Tags: {all_stats['unique_tags']:,} unique")

        return ProcessingResult(
            success=True,
            files_processed=len(md_files),
            files_modified=0,
            errors=self.errors,
            warnings=self.warnings,
            metadata={'statistics': all_stats}
        )


def main():
    """Standalone execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze Obsidian vault')
    parser.add_argument('--vault', type=Path, required=True, help='Vault path')
    parser.add_argument('--report', type=Path, help='Output report path')
    parser.add_argument('--format', choices=['md', 'json'], default='md', help='Report format')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    analyzer = VaultAnalyzer(args.vault, verbose=args.verbose)
    result = analyzer.process(
        report_path=args.report,
        report_format=args.format
    )

    if not args.report:
        print(json.dumps(asdict(result), indent=2))


if __name__ == '__main__':
    main()
