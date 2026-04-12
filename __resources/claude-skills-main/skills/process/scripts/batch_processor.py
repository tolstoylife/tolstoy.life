#!/usr/bin/env python3
"""
Obsidian Batch Processor
Main CLI entry point for batch processing Obsidian vault operations.

Usage:
    batch_processor.py <command> [options]

Commands:
    extract-wikilinks   Extract all wikilinks from files
    normalize-tags      Normalize and validate tags
    process-frontmatter Process YAML frontmatter
    analyze-vault       Generate vault statistics
    migrate-structure   Migrate notes to new structure
    fix-links           Fix broken wikilinks
    transform-callouts  Transform callout formats

Examples:
    # Extract all wikilinks from vault
    batch_processor.py extract-wikilinks --vault ~/Documents/Obsidian --output links.json

    # Normalize tags with dry-run
    batch_processor.py normalize-tags --vault ~/Documents/Obsidian --dry-run

    # Generate vault statistics
    batch_processor.py analyze-vault --vault ~/Documents/Obsidian --report stats.md
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ProcessingResult:
    """Result of a batch processing operation."""
    success: bool
    files_processed: int
    files_modified: int
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class BatchProcessor:
    """Base class for batch processing operations."""

    def __init__(self, vault_path: Path, dry_run: bool = False, verbose: bool = False):
        self.vault_path = Path(vault_path)
        self.dry_run = dry_run
        self.verbose = verbose
        self.errors: List[str] = []
        self.warnings: List[str] = []

        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {vault_path}")

        if not self.vault_path.is_dir():
            raise ValueError(f"Vault path is not a directory: {vault_path}")

    def find_markdown_files(self, pattern: str = "**/*.md") -> List[Path]:
        """Find all markdown files in vault matching pattern."""
        files = list(self.vault_path.glob(pattern))
        logger.info(f"Found {len(files)} markdown files")
        return files

    def read_file(self, file_path: Path) -> Optional[str]:
        """Read file content with error handling."""
        try:
            return file_path.read_text(encoding='utf-8')
        except Exception as e:
            error_msg = f"Failed to read {file_path}: {e}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return None

    def write_file(self, file_path: Path, content: str) -> bool:
        """Write file content with dry-run support."""
        if self.dry_run:
            logger.info(f"[DRY-RUN] Would write to {file_path}")
            return True

        try:
            # Create backup
            backup_path = file_path.with_suffix('.md.bak')
            file_path.rename(backup_path)

            # Write new content
            file_path.write_text(content, encoding='utf-8')

            # Remove backup on success
            backup_path.unlink()
            return True
        except Exception as e:
            error_msg = f"Failed to write {file_path}: {e}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False

    def process(self) -> ProcessingResult:
        """Execute the batch processing operation. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement process()")


class VaultContext:
    """Context manager for vault operations with rollback support."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.backups: Dict[Path, Path] = {}
        self.changes: List[Dict[str, Any]] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.error(f"Error during processing: {exc_val}")
            self.rollback()
            return False
        return True

    def backup_file(self, file_path: Path) -> Path:
        """Create a backup of the file."""
        backup_path = file_path.with_suffix('.md.bak')
        backup_path.write_bytes(file_path.read_bytes())
        self.backups[file_path] = backup_path
        return backup_path

    def rollback(self):
        """Rollback all changes."""
        logger.info("Rolling back changes...")
        for original, backup in self.backups.items():
            try:
                original.write_bytes(backup.read_bytes())
                backup.unlink()
            except Exception as e:
                logger.error(f"Failed to rollback {original}: {e}")

    def commit(self):
        """Commit changes by removing backups."""
        logger.info("Committing changes...")
        for backup in self.backups.values():
            try:
                backup.unlink()
            except Exception as e:
                logger.warning(f"Failed to remove backup {backup}: {e}")


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description='Obsidian Batch Processor - Batch operations for Obsidian vaults',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Extract wikilinks from vault
    %(prog)s extract-wikilinks --vault ~/vault --output links.json

    # Normalize tags with preview
    %(prog)s normalize-tags --vault ~/vault --dry-run

    # Generate vault report
    %(prog)s analyze-vault --vault ~/vault --report stats.md

For detailed command help:
    %(prog)s <command> --help
        """
    )

    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Common arguments
    def add_common_args(subparser):
        subparser.add_argument('--vault', type=Path, required=True,
                             help='Path to Obsidian vault')
        subparser.add_argument('--dry-run', action='store_true',
                             help='Preview changes without modifying files')
        subparser.add_argument('--verbose', '-v', action='store_true',
                             help='Enable verbose output')

    # extract-wikilinks command
    p_extract = subparsers.add_parser('extract-wikilinks',
                                      help='Extract all wikilinks from files')
    add_common_args(p_extract)
    p_extract.add_argument('--output', type=Path,
                          help='Output JSON file path')
    p_extract.add_argument('--include-aliases', action='store_true',
                          help='Include alias information')

    # normalize-tags command
    p_tags = subparsers.add_parser('normalize-tags',
                                   help='Normalize and validate tags')
    add_common_args(p_tags)
    p_tags.add_argument('--rules', type=Path,
                       help='JSON file with normalization rules')
    p_tags.add_argument('--case', choices=['lower', 'upper', 'title'],
                       help='Tag case normalization')

    # process-frontmatter command
    p_fm = subparsers.add_parser('process-frontmatter',
                                 help='Process YAML frontmatter')
    add_common_args(p_fm)
    p_fm.add_argument('--operation', required=True,
                     choices=['add', 'remove', 'update', 'validate'],
                     help='Frontmatter operation')
    p_fm.add_argument('--key', help='Frontmatter key to process')
    p_fm.add_argument('--value', help='Value to set (for add/update)')

    # analyze-vault command
    p_analyze = subparsers.add_parser('analyze-vault',
                                      help='Generate vault statistics')
    add_common_args(p_analyze)
    p_analyze.add_argument('--report', type=Path,
                          help='Output report file path')
    p_analyze.add_argument('--format', choices=['md', 'json', 'html'],
                          default='md', help='Report format')

    # migrate-structure command
    p_migrate = subparsers.add_parser('migrate-structure',
                                      help='Migrate notes to new structure')
    add_common_args(p_migrate)
    p_migrate.add_argument('--strategy', required=True,
                          choices=['flat-to-hierarchical', 'by-tags', 'by-date', 'custom'],
                          help='Migration strategy')
    p_migrate.add_argument('--config', type=Path,
                          help='Migration configuration file')

    # fix-links command
    p_links = subparsers.add_parser('fix-links',
                                    help='Fix broken wikilinks')
    add_common_args(p_links)
    p_links.add_argument('--auto-resolve', action='store_true',
                        help='Automatically resolve ambiguous links')
    p_links.add_argument('--report-broken', type=Path,
                        help='Output file for broken links report')

    # transform-callouts command
    p_callouts = subparsers.add_parser('transform-callouts',
                                       help='Transform callout formats')
    add_common_args(p_callouts)
    p_callouts.add_argument('--from-format', required=True,
                           help='Source callout format')
    p_callouts.add_argument('--to-format', required=True,
                           help='Target callout format')

    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Import command modules dynamically
    try:
        if args.command == 'extract-wikilinks':
            from wikilink_extractor import WikilinkExtractor
            processor = WikilinkExtractor(
                args.vault,
                dry_run=args.dry_run,
                verbose=args.verbose
            )
            result = processor.process(
                output_path=args.output,
                include_aliases=args.include_aliases
            )

        elif args.command == 'normalize-tags':
            from tag_normalizer import TagNormalizer
            processor = TagNormalizer(
                args.vault,
                dry_run=args.dry_run,
                verbose=args.verbose
            )
            result = processor.process(
                rules_path=args.rules,
                case_normalization=args.case
            )

        elif args.command == 'process-frontmatter':
            from frontmatter_processor import FrontmatterProcessor
            processor = FrontmatterProcessor(
                args.vault,
                dry_run=args.dry_run,
                verbose=args.verbose
            )
            result = processor.process(
                operation=args.operation,
                key=args.key,
                value=args.value
            )

        elif args.command == 'analyze-vault':
            from vault_analyzer import VaultAnalyzer
            processor = VaultAnalyzer(
                args.vault,
                dry_run=args.dry_run,
                verbose=args.verbose
            )
            result = processor.process(
                report_path=args.report,
                report_format=args.format
            )

        elif args.command == 'migrate-structure':
            logger.error("migrate-structure not yet implemented")
            sys.exit(1)

        elif args.command == 'fix-links':
            logger.error("fix-links not yet implemented")
            sys.exit(1)

        elif args.command == 'transform-callouts':
            logger.error("transform-callouts not yet implemented")
            sys.exit(1)

        else:
            parser.print_help()
            sys.exit(1)

        # Output result
        if args.verbose:
            print(json.dumps(asdict(result), indent=2))

        if result.success:
            logger.info("Processing completed successfully")
            logger.info(f"Files processed: {result.files_processed}")
            logger.info(f"Files modified: {result.files_modified}")
            if result.warnings:
                logger.warning(f"Warnings: {len(result.warnings)}")
        else:
            logger.error("Processing failed")
            if result.errors:
                logger.error(f"Errors: {len(result.errors)}")
                for error in result.errors:
                    logger.error(f"  - {error}")

        sys.exit(0 if result.success else 1)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
