#!/usr/bin/env python3
"""
LSP Orphan Detection and Management

Identifies orphaned notes (no incoming links) and provides options to:
- List orphaned files
- Generate a report
- Optionally move to archive folder
- Create an index note linking to all orphans

Usage:
    # List orphans
    python lsp_orphan_detection.py --vault ~/Documents/Obsidian --list

    # Generate report
    python lsp_orphan_detection.py --vault ~/Documents/Obsidian --report orphans.md

    # Archive orphans
    python lsp_orphan_detection.py --vault ~/Documents/Obsidian --archive --dry-run

    # Create orphan index
    python lsp_orphan_detection.py --vault ~/Documents/Obsidian --create-index
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from lsp_integration import (
    MarkdownOxideIntegration,
    RecursiveLSP,
    VaultLSPAnalyzer
)
from batch_processor import VaultContext


def find_orphans(vault_path: Path) -> List[Dict[str, Any]]:
    """
    Find all orphaned notes in vault.

    Args:
        vault_path: Path to Obsidian vault

    Returns:
        List of orphan information dicts
    """
    print(f"Scanning vault for orphaned notes: {vault_path}")

    integration = MarkdownOxideIntegration(vault_path, verbose=True)
    recursive_lsp = RecursiveLSP(integration)

    # Find all markdown files
    md_files = list(vault_path.glob("**/*.md"))
    print(f"Found {len(md_files)} markdown files")

    # Find orphans
    print("Detecting orphaned notes...")
    orphan_paths = recursive_lsp.find_orphans(md_files)

    # Gather additional information
    orphans = []
    for orphan_path in orphan_paths:
        file_path = vault_path / orphan_path
        stat = file_path.stat()

        orphans.append({
            'path': orphan_path,
            'absolute_path': str(file_path),
            'size_bytes': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
        })

    print(f"Found {len(orphans)} orphaned notes")
    return orphans


def generate_report(orphans: List[Dict[str, Any]], vault_path: Path, output_path: Path):
    """
    Generate markdown report of orphaned notes.

    Args:
        orphans: List of orphan information
        vault_path: Path to Obsidian vault
        output_path: Output path for report
    """
    print(f"Generating orphan report: {output_path}")

    # Sort by modification date
    orphans_sorted = sorted(orphans, key=lambda x: x['modified'], reverse=True)

    # Build report
    report_lines = [
        "# Orphaned Notes Report",
        "",
        f"Generated: {datetime.now().isoformat()}",
        f"Vault: {vault_path}",
        "",
        f"**Total orphaned notes:** {len(orphans)}",
        "",
        "## Definition",
        "",
        "Orphaned notes are markdown files with no incoming wikilinks from other notes in the vault.",
        "",
        "## Orphaned Notes",
        ""
    ]

    # Add table
    report_lines.extend([
        "| File | Size | Last Modified |",
        "|------|------|---------------|"
    ])

    for orphan in orphans_sorted:
        size_kb = orphan['size_bytes'] / 1024
        modified_date = datetime.fromisoformat(orphan['modified']).strftime('%Y-%m-%d %H:%M')
        report_lines.append(
            f"| [[{orphan['path']}]] | {size_kb:.1f} KB | {modified_date} |"
        )

    report_lines.extend([
        "",
        "## Actions",
        "",
        "Consider the following for orphaned notes:",
        "",
        "- [ ] Review and link relevant notes",
        "- [ ] Archive or delete outdated notes",
        "- [ ] Create index notes for collections",
        "- [ ] Add tags for better discoverability",
        "",
        "## Statistics by Directory",
        ""
    ])

    # Directory statistics
    dir_counts: Dict[str, int] = {}
    for orphan in orphans:
        dir_path = Path(orphan['path']).parent
        dir_name = str(dir_path) if str(dir_path) != '.' else 'root'
        dir_counts[dir_name] = dir_counts.get(dir_name, 0) + 1

    for dir_name, count in sorted(dir_counts.items(), key=lambda x: x[1], reverse=True):
        report_lines.append(f"- **{dir_name}**: {count} orphaned notes")

    # Write report
    output_path.write_text("\n".join(report_lines), encoding='utf-8')
    print(f"Report written to: {output_path}")


def archive_orphans(
    orphans: List[Dict[str, Any]],
    vault_path: Path,
    archive_folder: str = "Archive/Orphans",
    dry_run: bool = False
):
    """
    Move orphaned notes to archive folder.

    Args:
        orphans: List of orphan information
        vault_path: Path to Obsidian vault
        archive_folder: Archive folder path (relative to vault)
        dry_run: Preview changes without executing
    """
    archive_path = vault_path / archive_folder

    if not dry_run:
        archive_path.mkdir(parents=True, exist_ok=True)
        print(f"Created archive folder: {archive_path}")
    else:
        print(f"[DRY-RUN] Would create archive folder: {archive_path}")

    print(f"\nArchiving {len(orphans)} orphaned notes...")

    with VaultContext(vault_path) as ctx:
        for i, orphan in enumerate(orphans, 1):
            source = Path(orphan['absolute_path'])
            dest = archive_path / source.name

            # Handle name conflicts
            counter = 1
            while dest.exists():
                stem = source.stem
                suffix = source.suffix
                dest = archive_path / f"{stem}_{counter}{suffix}"
                counter += 1

            if not dry_run:
                ctx.backup_file(source)
                source.rename(dest)
                print(f"  [{i}/{len(orphans)}] Moved: {orphan['path']} -> {dest.relative_to(vault_path)}")
            else:
                print(f"  [{i}/{len(orphans)}] [DRY-RUN] Would move: {orphan['path']} -> {dest.relative_to(vault_path)}")

        if not dry_run:
            ctx.commit()
            print(f"\n✓ Archived {len(orphans)} orphaned notes to {archive_folder}")
        else:
            print(f"\n[DRY-RUN] Would archive {len(orphans)} orphaned notes to {archive_folder}")


def create_orphan_index(orphans: List[Dict[str, Any]], vault_path: Path, index_path: Path):
    """
    Create an index note linking to all orphaned notes.

    Args:
        orphans: List of orphan information
        vault_path: Path to Obsidian vault
        index_path: Path for index note
    """
    print(f"Creating orphan index: {index_path}")

    # Sort by directory
    orphans_by_dir: Dict[str, List[Dict[str, Any]]] = {}
    for orphan in orphans:
        dir_path = Path(orphan['path']).parent
        dir_name = str(dir_path) if str(dir_path) != '.' else 'root'
        if dir_name not in orphans_by_dir:
            orphans_by_dir[dir_name] = []
        orphans_by_dir[dir_name].append(orphan)

    # Build index
    index_lines = [
        "# Orphaned Notes Index",
        "",
        f"Generated: {datetime.now().isoformat()}",
        "",
        f"**Total orphaned notes:** {len(orphans)}",
        "",
        "This index links to all notes that have no incoming wikilinks.",
        ""
    ]

    for dir_name in sorted(orphans_by_dir.keys()):
        dir_orphans = orphans_by_dir[dir_name]
        index_lines.extend([
            f"## {dir_name}",
            "",
            f"*{len(dir_orphans)} orphaned notes*",
            ""
        ])

        for orphan in sorted(dir_orphans, key=lambda x: x['path']):
            # Create wikilink
            link_text = Path(orphan['path']).stem
            index_lines.append(f"- [[{link_text}]]")

        index_lines.append("")

    # Write index
    index_path.write_text("\n".join(index_lines), encoding='utf-8')
    print(f"Index created: {index_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Detect and manage orphaned notes using LSP integration'
    )
    parser.add_argument('--vault', type=Path, required=True,
                        help='Path to Obsidian vault')
    parser.add_argument('--list', action='store_true',
                        help='List orphaned notes')
    parser.add_argument('--report', type=Path,
                        help='Generate markdown report')
    parser.add_argument('--archive', action='store_true',
                        help='Archive orphaned notes')
    parser.add_argument('--archive-folder', type=str, default='Archive/Orphans',
                        help='Archive folder path (default: Archive/Orphans)')
    parser.add_argument('--create-index', action='store_true',
                        help='Create orphan index note')
    parser.add_argument('--index-path', type=Path,
                        help='Index note path (default: Orphan_Index.md)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without executing')

    args = parser.parse_args()

    # Set defaults
    if args.create_index and not args.index_path:
        args.index_path = args.vault / "Orphan_Index.md"

    try:
        # Find orphans
        orphans = find_orphans(args.vault)

        if len(orphans) == 0:
            print("\n✓ No orphaned notes found!")
            return 0

        # List orphans
        if args.list:
            print("\nOrphaned Notes:")
            for i, orphan in enumerate(orphans, 1):
                print(f"  {i}. {orphan['path']}")

        # Generate report
        if args.report:
            generate_report(orphans, args.vault, args.report)

        # Archive orphans
        if args.archive:
            archive_orphans(
                orphans,
                args.vault,
                archive_folder=args.archive_folder,
                dry_run=args.dry_run
            )

        # Create index
        if args.create_index:
            create_orphan_index(orphans, args.vault, args.index_path)

        print("\n✓ Orphan detection complete!")
        return 0

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
