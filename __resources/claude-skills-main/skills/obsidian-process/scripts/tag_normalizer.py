#!/usr/bin/env python3
"""
Tag Normalizer
Normalize and validate tags in Obsidian vault files.

Supports:
- Inline tags: #tag, #nested/tag
- Frontmatter tags: tags: [tag1, tag2]
- Tag validation and normalization
- Tag renaming and merging
- Tag hierarchy enforcement
"""

import re
import json
import yaml
from pathlib import Path
from typing import List, Dict, Set, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import logging

from batch_processor import BatchProcessor, ProcessingResult

logger = logging.getLogger(__name__)


@dataclass
class Tag:
    """Represents a tag occurrence."""
    tag: str  # The tag name (without #)
    source_file: str  # Relative to vault root
    line_number: int  # Line number in source file
    location: str  # 'inline' or 'frontmatter'
    original: str  # Original tag text


@dataclass
class TagRule:
    """Tag normalization rule."""
    pattern: str  # Regex pattern or exact match
    replacement: str  # Replacement tag
    case_sensitive: bool = False


class TagNormalizer(BatchProcessor):
    """Normalize and validate tags in Obsidian vault."""

    # Regex patterns
    INLINE_TAG_PATTERN = re.compile(r'(?:^|\s)#([\w/-]+)')
    FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL | re.MULTILINE)

    def __init__(self, vault_path: Path, dry_run: bool = False, verbose: bool = False):
        super().__init__(vault_path, dry_run, verbose)
        self.tags: List[Tag] = []
        self.tag_counts: Dict[str, int] = defaultdict(int)
        self.normalization_rules: List[TagRule] = []

    def load_rules(self, rules_path: Optional[Path]) -> None:
        """Load normalization rules from JSON file."""
        if not rules_path:
            return

        try:
            rules_data = json.loads(rules_path.read_text())
            for rule_dict in rules_data.get('rules', []):
                self.normalization_rules.append(TagRule(**rule_dict))
            logger.info(f"Loaded {len(self.normalization_rules)} normalization rules")
        except Exception as e:
            self.errors.append(f"Failed to load rules from {rules_path}: {e}")

    def extract_frontmatter_tags(self, content: str, file_path: Path) -> Tuple[List[Tag], Optional[Dict]]:
        """Extract tags from YAML frontmatter."""
        tags = []
        frontmatter = None

        match = self.FRONTMATTER_PATTERN.match(content)
        if not match:
            return tags, None

        try:
            frontmatter = yaml.safe_load(match.group(1))
            if not frontmatter:
                return tags, None

            # Handle different tag formats
            tag_values = frontmatter.get('tags') or frontmatter.get('tag')
            if not tag_values:
                return tags, frontmatter

            # Normalize to list
            if isinstance(tag_values, str):
                tag_values = [tag_values]
            elif not isinstance(tag_values, list):
                self.warnings.append(
                    f"Invalid tag format in {file_path}: {type(tag_values)}"
                )
                return tags, frontmatter

            # Create Tag objects
            source_rel = file_path.relative_to(self.vault_path).as_posix()
            for tag_value in tag_values:
                # Remove # if present
                tag_clean = str(tag_value).lstrip('#').strip()
                if tag_clean:
                    tags.append(Tag(
                        tag=tag_clean,
                        source_file=source_rel,
                        line_number=0,  # Frontmatter
                        location='frontmatter',
                        original=str(tag_value)
                    ))

        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error in {file_path}: {e}")

        return tags, frontmatter

    def extract_inline_tags(self, content: str, file_path: Path) -> List[Tag]:
        """Extract inline tags from content."""
        tags = []
        source_rel = file_path.relative_to(self.vault_path).as_posix()

        # Remove frontmatter before processing
        content_without_fm = self.FRONTMATTER_PATTERN.sub('', content)

        for line_num, line in enumerate(content_without_fm.split('\n'), start=1):
            # Skip code blocks and inline code
            if '```' in line or line.strip().startswith('    '):
                continue

            # Find all inline tags
            for match in self.INLINE_TAG_PATTERN.finditer(line):
                tag_name = match.group(1)
                tags.append(Tag(
                    tag=tag_name,
                    source_file=source_rel,
                    line_number=line_num,
                    location='inline',
                    original=f"#{tag_name}"
                ))

        return tags

    def extract_from_file(self, file_path: Path) -> List[Tag]:
        """Extract all tags from a single file."""
        content = self.read_file(file_path)
        if content is None:
            return []

        tags = []

        # Extract frontmatter tags
        fm_tags, _ = self.extract_frontmatter_tags(content, file_path)
        tags.extend(fm_tags)

        # Extract inline tags
        inline_tags = self.extract_inline_tags(content, file_path)
        tags.extend(inline_tags)

        return tags

    def normalize_tag(self, tag: str, case_normalization: Optional[str] = None) -> str:
        """
        Normalize a single tag according to rules.

        Args:
            tag: Tag to normalize
            case_normalization: 'lower', 'upper', or 'title'

        Returns:
            Normalized tag
        """
        normalized = tag

        # Apply custom rules
        for rule in self.normalization_rules:
            if rule.case_sensitive:
                pattern = re.compile(rule.pattern)
            else:
                pattern = re.compile(rule.pattern, re.IGNORECASE)

            if pattern.match(normalized):
                normalized = pattern.sub(rule.replacement, normalized)
                break

        # Apply case normalization
        if case_normalization:
            if case_normalization == 'lower':
                normalized = normalized.lower()
            elif case_normalization == 'upper':
                normalized = normalized.upper()
            elif case_normalization == 'title':
                # Title case for each segment
                parts = normalized.split('/')
                normalized = '/'.join(part.title() for part in parts)

        # Validate tag format
        if not re.match(r'^[\w/-]+$', normalized):
            self.warnings.append(f"Tag contains invalid characters: {normalized}")

        return normalized

    def apply_normalization(
        self,
        file_path: Path,
        case_normalization: Optional[str] = None
    ) -> bool:
        """Apply tag normalization to a file."""
        content = self.read_file(file_path)
        if content is None:
            return False

        modified = False
        new_content = content

        # Normalize frontmatter tags
        fm_match = self.FRONTMATTER_PATTERN.match(content)
        if fm_match:
            try:
                frontmatter = yaml.safe_load(fm_match.group(1))
                if frontmatter:
                    tag_keys = ['tags', 'tag']
                    for key in tag_keys:
                        if key in frontmatter:
                            old_tags = frontmatter[key]
                            if isinstance(old_tags, str):
                                old_tags = [old_tags]

                            if isinstance(old_tags, list):
                                new_tags = [
                                    self.normalize_tag(
                                        str(t).lstrip('#'),
                                        case_normalization
                                    )
                                    for t in old_tags
                                ]

                                if new_tags != [str(t).lstrip('#') for t in old_tags]:
                                    frontmatter[key] = new_tags
                                    modified = True

                    if modified:
                        # Reconstruct frontmatter
                        new_fm = yaml.dump(
                            frontmatter,
                            default_flow_style=False,
                            allow_unicode=True,
                            sort_keys=False
                        )
                        new_content = f"---\n{new_fm}---\n" + content[fm_match.end():]

            except yaml.YAMLError as e:
                self.errors.append(f"YAML error in {file_path}: {e}")
                return False

        # Normalize inline tags
        def replace_inline_tag(match):
            nonlocal modified
            old_tag = match.group(1)
            new_tag = self.normalize_tag(old_tag, case_normalization)
            if old_tag != new_tag:
                modified = True
                return match.group(0).replace(f"#{old_tag}", f"#{new_tag}")
            return match.group(0)

        # Remove frontmatter before processing inline tags
        if fm_match:
            prefix = new_content[:fm_match.end()]
            body = new_content[fm_match.end():]
        else:
            prefix = ""
            body = new_content

        new_body = self.INLINE_TAG_PATTERN.sub(replace_inline_tag, body)
        new_content = prefix + new_body

        # Write changes
        if modified:
            if self.write_file(file_path, new_content):
                return True

        return False

    def get_statistics(self) -> Dict[str, Any]:
        """Calculate tag statistics."""
        # Count tags
        for tag in self.tags:
            self.tag_counts[tag.tag] += 1

        # Find most used tags
        most_used = sorted(
            self.tag_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]

        # Group by hierarchy
        tag_hierarchy = defaultdict(set)
        for tag in self.tag_counts.keys():
            if '/' in tag:
                root = tag.split('/')[0]
                tag_hierarchy[root].add(tag)

        return {
            'total_tags': len(self.tags),
            'unique_tags': len(self.tag_counts),
            'frontmatter_tags': sum(1 for t in self.tags if t.location == 'frontmatter'),
            'inline_tags': sum(1 for t in self.tags if t.location == 'inline'),
            'hierarchical_tags': sum(1 for t in self.tag_counts if '/' in t),
            'most_used_tags': [
                {'tag': tag, 'count': count}
                for tag, count in most_used
            ],
            'tag_hierarchy': {
                root: list(children)
                for root, children in tag_hierarchy.items()
            }
        }

    def process(
        self,
        rules_path: Optional[Path] = None,
        case_normalization: Optional[str] = None
    ) -> ProcessingResult:
        """
        Normalize tags across the vault.

        Args:
            rules_path: Path to JSON rules file
            case_normalization: Tag case normalization ('lower', 'upper', 'title')

        Returns:
            ProcessingResult with normalization results
        """
        logger.info(f"Normalizing tags in vault: {self.vault_path}")

        # Load rules
        self.load_rules(rules_path)

        # Find all markdown files
        md_files = self.find_markdown_files()
        files_processed = 0
        files_modified = 0

        # First pass: extract all tags
        for file_path in md_files:
            tags = self.extract_from_file(file_path)
            self.tags.extend(tags)

        # Get statistics before normalization
        stats_before = self.get_statistics()

        # Second pass: apply normalization
        for file_path in md_files:
            if self.verbose:
                logger.info(f"Processing {file_path.relative_to(self.vault_path)}")

            if self.apply_normalization(file_path, case_normalization):
                files_modified += 1

            files_processed += 1

        # Get statistics after normalization
        if not self.dry_run:
            self.tags.clear()
            self.tag_counts.clear()
            for file_path in md_files:
                tags = self.extract_from_file(file_path)
                self.tags.extend(tags)

        stats_after = self.get_statistics()

        logger.info(f"Processed {files_processed} files, modified {files_modified}")
        logger.info(f"Tags before: {stats_before['unique_tags']}, after: {stats_after['unique_tags']}")

        return ProcessingResult(
            success=True,
            files_processed=files_processed,
            files_modified=files_modified,
            errors=self.errors,
            warnings=self.warnings,
            metadata={
                'statistics_before': stats_before,
                'statistics_after': stats_after,
                'case_normalization': case_normalization,
                'rules_applied': len(self.normalization_rules)
            }
        )


def main():
    """Standalone execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Normalize tags in Obsidian vault')
    parser.add_argument('--vault', type=Path, required=True, help='Vault path')
    parser.add_argument('--rules', type=Path, help='Normalization rules JSON file')
    parser.add_argument('--case', choices=['lower', 'upper', 'title'], help='Case normalization')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    normalizer = TagNormalizer(args.vault, dry_run=args.dry_run, verbose=args.verbose)
    result = normalizer.process(
        rules_path=args.rules,
        case_normalization=args.case
    )

    print(json.dumps(asdict(result), indent=2))


if __name__ == '__main__':
    main()
