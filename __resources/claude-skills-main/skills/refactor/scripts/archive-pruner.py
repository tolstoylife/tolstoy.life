#!/usr/bin/env python3
"""
archive-pruner.py
Identifies and archives unused components based on usage metrics and age.
Part of the refactor skill infrastructure.
"""

import argparse
import json
import sys
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set
from collections import defaultdict
import os


def get_file_age(file_path: Path) -> int:
    """Get file age in days."""
    mtime = os.path.getmtime(file_path)
    age = datetime.now() - datetime.fromtimestamp(mtime)
    return age.days


def find_references_in_files(
    search_paths: List[Path],
    target_name: str
) -> List[Path]:
    """Find files that reference the target component."""
    references = []

    for search_path in search_paths:
        if search_path.is_file():
            files_to_search = [search_path]
        else:
            files_to_search = list(search_path.rglob('*.md')) + \
                               list(search_path.rglob('*.json')) + \
                               list(search_path.rglob('*.sh'))

        for file_path in files_to_search:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for various reference patterns
                if target_name in content:
                    references.append(file_path)

            except Exception:
                # Skip files that can't be read
                pass

    return references


def load_activity_log(log_path: Path) -> Dict[str, datetime]:
    """Load component activity log and extract last access times."""
    last_access = {}

    if not log_path.exists():
        return last_access

    try:
        with open(log_path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    timestamp = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                    component = entry.get('file') or entry.get('component') or entry.get('description', '')

                    # Extract component name from path
                    if '/' in component:
                        component = Path(component).stem

                    # Track most recent access
                    if component not in last_access or timestamp > last_access[component]:
                        last_access[component] = timestamp

                except Exception:
                    continue

    except Exception as e:
        print(f"Warning: Could not read activity log: {e}", file=sys.stderr)

    return last_access


def identify_candidates_for_archival(
    directory: Path,
    pattern: str,
    age_threshold: int,
    search_paths: List[Path],
    activity_log: Path
) -> List[Dict]:
    """Identify components that are candidates for archival."""
    candidates = []
    component_files = list(directory.rglob(pattern))

    # Load activity log
    last_access = load_activity_log(activity_log)

    for file_path in component_files:
        component_name = file_path.stem
        file_age = get_file_age(file_path)

        # Check if component is old enough
        if file_age < age_threshold:
            continue

        # Check for references
        references = find_references_in_files(search_paths, component_name)

        # Check activity log
        last_used = last_access.get(component_name)
        days_since_use = None
        if last_used:
            days_since_use = (datetime.now().replace(tzinfo=last_used.tzinfo) - last_used).days

        # Component is a candidate if:
        # 1. Old enough (age_threshold)
        # 2. No references OR references only from archive
        # 3. Not used recently (if activity log available)

        is_referenced = len([r for r in references if '/db/' not in str(r) and '/archive/' not in str(r)]) > 0
        is_recently_used = days_since_use is not None and days_since_use < age_threshold

        if not is_referenced and not is_recently_used:
            candidates.append({
                'file_path': file_path,
                'component_name': component_name,
                'age_days': file_age,
                'references': references,
                'last_used_days': days_since_use,
                'reason': 'unused'
            })

    return candidates


def archive_component(
    component_file: Path,
    archive_dir: Path,
    dry_run: bool = False
) -> bool:
    """Archive a component file."""
    # Preserve directory structure in archive
    relative_path = Path(component_file.parent.name) / component_file.name

    archive_path = archive_dir / relative_path

    if dry_run:
        print(f"   [DRY RUN] Would move: {component_file} → {archive_path}")
        return True

    try:
        # Create archive directory
        archive_path.parent.mkdir(parents=True, exist_ok=True)

        # Move file to archive
        shutil.move(str(component_file), str(archive_path))

        print(f"   ✓ Archived: {component_file.name} → {archive_path}")
        return True

    except Exception as e:
        print(f"   ✗ Error archiving {component_file}: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Identify and archive unused components based on usage and age'
    )
    parser.add_argument(
        'directory',
        type=Path,
        help='Directory to analyze (e.g., ~/.claude/skills)'
    )
    parser.add_argument(
        '--archive-dir',
        type=Path,
        default=None,
        help='Archive destination (default: ~/.claude/db/archive/)'
    )
    parser.add_argument(
        '--age-threshold',
        type=int,
        default=90,
        help='Minimum age in days for archival consideration (default: 90)'
    )
    parser.add_argument(
        '--pattern',
        type=str,
        default='*.md',
        help='File pattern to match (default: *.md)'
    )
    parser.add_argument(
        '--search-paths',
        type=str,
        nargs='+',
        default=None,
        help='Paths to search for references (default: ~/.claude/)'
    )
    parser.add_argument(
        '--activity-log',
        type=Path,
        default=None,
        help='Activity log file (JSONL format)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be archived without actually moving files'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )

    args = parser.parse_args()

    # Set defaults
    if args.archive_dir is None:
        args.archive_dir = Path.home() / '.claude' / 'db' / 'archive'

    if args.search_paths is None:
        args.search_paths = [Path.home() / '.claude']
    else:
        args.search_paths = [Path(p) for p in args.search_paths]

    if args.activity_log is None:
        args.activity_log = Path.home() / '.claude' / '.refactor-activity.jsonl'

    # Identify candidates
    candidates = identify_candidates_for_archival(
        args.directory,
        args.pattern,
        args.age_threshold,
        args.search_paths,
        args.activity_log
    )

    if args.json:
        output = {
            'total_candidates': len(candidates),
            'archive_dir': str(args.archive_dir),
            'age_threshold_days': args.age_threshold,
            'dry_run': args.dry_run,
            'candidates': [
                {
                    'component_name': c['component_name'],
                    'file_path': str(c['file_path']),
                    'age_days': c['age_days'],
                    'last_used_days': c['last_used_days'],
                    'reference_count': len(c['references']),
                    'reason': c['reason']
                }
                for c in candidates
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print(f"\n🗂️  Archive Pruner: {args.directory}")
        print(f"   Age threshold: {args.age_threshold} days")
        print(f"   Archive destination: {args.archive_dir}")
        print(f"   Candidates found: {len(candidates)}")

        if args.dry_run:
            print(f"   Mode: DRY RUN (no files will be moved)\n")
        else:
            print(f"   Mode: ACTIVE (files will be moved)\n")

        if not candidates:
            print("   ✓ No components eligible for archival")
            return 0

        print("📦 Archival Candidates:")
        for candidate in candidates:
            print(f"\n   Component: {candidate['component_name']}")
            print(f"     File: {candidate['file_path']}")
            print(f"     Age: {candidate['age_days']} days")
            if candidate['last_used_days'] is not None:
                print(f"     Last used: {candidate['last_used_days']} days ago")
            else:
                print(f"     Last used: Never (no activity log entry)")
            print(f"     References: {len(candidate['references'])}")

        # Perform archival if not dry run
        if not args.dry_run:
            print("\n📦 Archiving components...")
            archived_count = 0

            for candidate in candidates:
                if archive_component(candidate['file_path'], args.archive_dir, dry_run=False):
                    archived_count += 1

            print(f"\n✓ Archived {archived_count} of {len(candidates)} candidates")

    return 0


if __name__ == '__main__':
    sys.exit(main())
