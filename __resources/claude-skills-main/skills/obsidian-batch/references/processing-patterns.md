# Obsidian Batch Processing Patterns

Common patterns and recipes for batch processing Obsidian vaults.

## Table of Contents

1. [Vault Migration Patterns](#vault-migration-patterns)
2. [Link Management Patterns](#link-management-patterns)
3. [Tag Management Patterns](#tag-management-patterns)
4. [Frontmatter Patterns](#frontmatter-patterns)
5. [Content Transformation Patterns](#content-transformation-patterns)
6. [Quality Assurance Patterns](#quality-assurance-patterns)

## Vault Migration Patterns

### Pattern: Flat to Hierarchical Migration

**Use Case**: Migrate 1000+ notes from flat structure to organized folders.

**Strategy**:
```python
def migrate_by_tags(vault_path: Path, dry_run: bool = False):
    """
    Organize notes into folders based on their primary tag.

    Example:
        #projects/alpha → projects/alpha/note.md
        #archive → archive/note.md
    """
    for note in find_notes(vault_path):
        tags = extract_tags(note)
        if not tags:
            continue

        # Use first tag as folder path
        primary_tag = tags[0].replace('#', '').replace('/', os.sep)
        new_path = vault_path / primary_tag / note.name

        if not dry_run:
            new_path.parent.mkdir(parents=True, exist_ok=True)
            note.rename(new_path)

        # Update wikilinks in other notes
        update_wikilinks(vault_path, note.stem, f"{primary_tag}/{note.stem}")
```

**Execution**:
```bash
# Preview migration
python batch_processor.py migrate-structure \
  --vault ~/vault \
  --strategy by-tags \
  --dry-run

# Execute migration
python batch_processor.py migrate-structure \
  --vault ~/vault \
  --strategy by-tags
```

### Pattern: Date-Based Organization

**Use Case**: Organize daily notes and journals by year/month.

**Strategy**:
```python
def migrate_by_date(vault_path: Path, date_format: str = "%Y-%m-%d"):
    """
    Organize notes by creation date into year/month folders.

    Example:
        note.md (created 2025-01-15) → 2025/01/note.md
    """
    for note in find_notes(vault_path):
        # Extract date from filename or frontmatter
        date = extract_date(note)
        if not date:
            continue

        year_month = date.strftime("%Y/%m")
        new_path = vault_path / year_month / note.name

        new_path.parent.mkdir(parents=True, exist_ok=True)
        note.rename(new_path)
```

**Execution**:
```bash
python batch_processor.py migrate-structure \
  --vault ~/vault \
  --strategy by-date \
  --config migration-config.json
```

**Configuration** (`migration-config.json`):
```json
{
  "date_format": "%Y-%m-%d",
  "date_source": "frontmatter",
  "fallback_date_source": "filename",
  "preserve_tags": true,
  "update_links": true
}
```

## Link Management Patterns

### Pattern: Fix Broken Links with Fuzzy Matching

**Use Case**: Automatically fix broken wikilinks after file renames.

**Strategy**:
```python
def fix_broken_links(vault_path: Path, threshold: float = 0.8):
    """
    Use fuzzy matching to resolve broken links.

    Example:
        [[Old Name]] → [[New Name]] (if similarity > threshold)
    """
    from difflib import SequenceMatcher

    # Get all note names
    note_names = {note.stem for note in find_notes(vault_path)}

    # Find broken links
    broken_links = find_broken_links(vault_path)

    # Attempt to resolve each broken link
    for source_file, broken_target in broken_links:
        # Find best match
        best_match = None
        best_score = 0

        for note_name in note_names:
            score = SequenceMatcher(None, broken_target, note_name).ratio()
            if score > best_score and score >= threshold:
                best_match = note_name
                best_score = score

        if best_match:
            replace_link(source_file, broken_target, best_match)
            print(f"Fixed: {broken_target} → {best_match} (score: {best_score:.2f})")
```

**Execution**:
```bash
# Preview fixes
python batch_processor.py fix-links \
  --vault ~/vault \
  --auto-resolve \
  --dry-run

# Apply fixes
python batch_processor.py fix-links \
  --vault ~/vault \
  --auto-resolve \
  --report-broken broken-links.md
```

### Pattern: Update Links After Refactoring

**Use Case**: Update all references when renaming or moving notes.

**Strategy**:
```python
def update_all_links(vault_path: Path, old_name: str, new_name: str):
    """
    Update all references to a note after rename/move.

    Handles:
    - Basic wikilinks: [[Old]] → [[New]]
    - Aliased links: [[Old|Alias]] → [[New|Alias]]
    - Embedded: ![[Old]] → ![[New]]
    - With headers: [[Old#Header]] → [[New#Header]]
    """
    pattern = re.compile(
        rf'(!?\[\[){re.escape(old_name)}([#|\]])',
        re.IGNORECASE
    )

    for note in find_notes(vault_path):
        content = note.read_text()
        updated = pattern.sub(rf'\1{new_name}\2', content)

        if updated != content:
            note.write_text(updated)
            print(f"Updated links in: {note}")
```

### Pattern: Convert External Links to Wikilinks

**Use Case**: Convert markdown links to wikilinks for internal notes.

**Strategy**:
```python
def convert_to_wikilinks(vault_path: Path):
    """
    Convert [text](note.md) to [[note|text]].
    """
    external_link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')

    for note in find_notes(vault_path):
        content = note.read_text()

        def replace_link(match):
            text = match.group(1)
            target = Path(match.group(2)).stem

            # Check if target exists
            if (vault_path / match.group(2)).exists():
                return f"[[{target}|{text}]]"
            return match.group(0)  # Keep original if not found

        updated = external_link_pattern.sub(replace_link, content)
        note.write_text(updated)
```

## Tag Management Patterns

### Pattern: Normalize Tag Hierarchy

**Use Case**: Enforce consistent tag hierarchy across vault.

**Strategy**:
```python
def normalize_tag_hierarchy(vault_path: Path, rules: Dict[str, str]):
    """
    Apply hierarchy normalization rules.

    Example rules:
        "project" → "projects"
        "Projects" → "projects"
        "proj" → "projects"
    """
    for note in find_notes(vault_path):
        content = note.read_text()
        updated = content

        for old_tag, new_tag in rules.items():
            # Inline tags
            updated = re.sub(
                rf'#\b{re.escape(old_tag)}\b',
                f'#{new_tag}',
                updated,
                flags=re.IGNORECASE
            )

        # Update frontmatter tags
        updated = update_frontmatter_tags(updated, rules)

        if updated != content:
            note.write_text(updated)
```

**Rules File** (`tag-rules.json`):
```json
{
  "rules": [
    {
      "pattern": "project",
      "replacement": "projects",
      "case_sensitive": false
    },
    {
      "pattern": "todo",
      "replacement": "tasks/todo",
      "case_sensitive": false
    },
    {
      "pattern": "^temp.*",
      "replacement": "archive/temp",
      "case_sensitive": false
    }
  ]
}
```

**Execution**:
```bash
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --rules tag-rules.json \
  --case lower \
  --dry-run
```

### Pattern: Merge Duplicate Tags

**Use Case**: Consolidate tags with different variations.

**Strategy**:
```python
def merge_tags(vault_path: Path, merge_map: Dict[str, str]):
    """
    Merge multiple tags into canonical form.

    Example:
        #meeting, #meetings, #mtg → #meetings
    """
    for note in find_notes(vault_path):
        content = note.read_text()

        for old_tags, canonical in merge_map.items():
            for old_tag in old_tags.split(','):
                old_tag = old_tag.strip()
                content = re.sub(
                    rf'#\b{re.escape(old_tag)}\b',
                    f'#{canonical}',
                    content,
                    flags=re.IGNORECASE
                )

        note.write_text(content)
```

## Frontmatter Patterns

### Pattern: Add Missing Frontmatter

**Use Case**: Add standard frontmatter to notes that don't have it.

**Strategy**:
```python
def add_missing_frontmatter(vault_path: Path, template: Dict[str, Any]):
    """
    Add frontmatter template to notes without it.
    """
    for note in find_notes(vault_path):
        content = note.read_text()

        if not has_frontmatter(content):
            # Generate frontmatter
            fm_data = template.copy()
            fm_data['created'] = datetime.fromtimestamp(
                note.stat().st_ctime
            ).isoformat()
            fm_data['title'] = note.stem

            # Add to note
            fm_str = create_frontmatter(fm_data)
            note.write_text(fm_str + content)
```

**Template**:
```json
{
  "created": "auto",
  "modified": "auto",
  "tags": [],
  "aliases": [],
  "draft": false
}
```

**Execution**:
```bash
python batch_processor.py process-frontmatter \
  --vault ~/vault \
  --operation template \
  --template basic \
  --dry-run
```

### Pattern: Update Timestamps

**Use Case**: Keep frontmatter timestamps in sync with file system.

**Strategy**:
```python
def sync_timestamps(vault_path: Path):
    """
    Update frontmatter timestamps from file metadata.
    """
    for note in find_notes(vault_path):
        content = note.read_text()
        fm = extract_frontmatter(content)

        if fm:
            # Update created if missing
            if 'created' not in fm:
                fm['created'] = datetime.fromtimestamp(
                    note.stat().st_ctime
                ).isoformat()

            # Always update modified
            fm['modified'] = datetime.fromtimestamp(
                note.stat().st_mtime
            ).isoformat()

            # Write back
            updated = update_frontmatter(content, fm)
            note.write_text(updated)
```

### Pattern: Bulk Property Update

**Use Case**: Add or update a property across multiple notes.

**Strategy**:
```python
def bulk_update_property(
    vault_path: Path,
    key: str,
    value: Any,
    filter_func: Optional[Callable] = None
):
    """
    Update a frontmatter property in filtered notes.

    Example:
        Set "published: false" on all draft notes
    """
    for note in find_notes(vault_path):
        if filter_func and not filter_func(note):
            continue

        content = note.read_text()
        updated = update_frontmatter(content, {key: value})
        note.write_text(updated)
```

**Execution**:
```bash
# Add 'status: draft' to all notes
python batch_processor.py process-frontmatter \
  --vault ~/vault \
  --operation add \
  --key status \
  --value draft

# Update existing 'author' field
python batch_processor.py process-frontmatter \
  --vault ~/vault \
  --operation update \
  --key author \
  --value "Your Name"
```

## Content Transformation Patterns

### Pattern: Transform Callout Formats

**Use Case**: Migrate from one callout format to another.

**Strategy**:
```python
def transform_callouts(vault_path: Path, from_fmt: str, to_fmt: str):
    """
    Transform callout syntax between formats.

    Supported formats:
    - obsidian: > [!note]
    - admonition: !!! note
    - custom: >> NOTE:
    """
    for note in find_notes(vault_path):
        content = note.read_text()

        if from_fmt == 'obsidian' and to_fmt == 'admonition':
            # > [!note] → !!! note
            content = re.sub(
                r'>\s*\[!(\w+)\]\s*(.*?)\n',
                r'!!! \1 \2\n',
                content
            )

        note.write_text(content)
```

### Pattern: Batch Content Replacement

**Use Case**: Replace text patterns across entire vault.

**Strategy**:
```python
def batch_replace(
    vault_path: Path,
    pattern: str,
    replacement: str,
    use_regex: bool = False
):
    """
    Replace text across all notes.

    Safety features:
    - Dry run mode
    - Backups before modification
    - Match counting and reporting
    """
    import re

    total_matches = 0
    modified_files = []

    for note in find_notes(vault_path):
        content = note.read_text()

        if use_regex:
            updated, count = re.subn(pattern, replacement, content)
        else:
            updated = content.replace(pattern, replacement)
            count = content.count(pattern)

        if count > 0:
            total_matches += count
            modified_files.append(note)
            note.write_text(updated)

    print(f"Replaced {total_matches} occurrences in {len(modified_files)} files")
```

## Quality Assurance Patterns

### Pattern: Validate Vault Consistency

**Use Case**: Regular vault health checks.

**Strategy**:
```python
def validate_vault(vault_path: Path) -> Dict[str, Any]:
    """
    Comprehensive vault validation.

    Checks:
    - Broken wikilinks
    - Orphaned notes
    - Invalid frontmatter
    - Duplicate note names
    - Invalid tag syntax
    - Empty notes
    """
    issues = {
        'broken_links': [],
        'orphaned_notes': [],
        'invalid_frontmatter': [],
        'duplicate_names': [],
        'invalid_tags': [],
        'empty_notes': []
    }

    # Check for broken links
    all_notes = {note.stem for note in find_notes(vault_path)}
    for note in find_notes(vault_path):
        links = extract_links(note)
        for link in links:
            if link not in all_notes:
                issues['broken_links'].append({
                    'file': note.name,
                    'link': link
                })

    # Check for orphaned notes
    linked_notes = set()
    for note in find_notes(vault_path):
        linked_notes.update(extract_links(note))

    for note in find_notes(vault_path):
        if note.stem not in linked_notes:
            issues['orphaned_notes'].append(note.name)

    # Additional checks...

    return issues
```

**Execution**:
```bash
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report health-report.md \
  --format md
```

### Pattern: Automated Cleanup

**Use Case**: Regular vault maintenance.

**Strategy**:
```python
def automated_cleanup(vault_path: Path):
    """
    Automated vault maintenance tasks.

    Tasks:
    - Remove empty notes
    - Fix formatting issues
    - Update timestamps
    - Normalize whitespace
    - Remove duplicate empty lines
    """
    for note in find_notes(vault_path):
        content = note.read_text()
        original = content

        # Remove trailing whitespace
        content = '\n'.join(line.rstrip() for line in content.split('\n'))

        # Remove multiple consecutive blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)

        # Ensure single newline at end
        content = content.rstrip() + '\n'

        # Write if changed
        if content != original:
            note.write_text(content)
```

## Advanced Patterns

### Pattern: Parallel Processing for Large Vaults

**Use Case**: Process 10,000+ notes efficiently.

**Strategy**:
```python
from multiprocessing import Pool
from functools import partial

def process_note_parallel(note_path: Path, processor_func: Callable):
    """Process a single note (worker function)."""
    try:
        return processor_func(note_path)
    except Exception as e:
        return {'error': str(e), 'file': str(note_path)}

def parallel_process(
    vault_path: Path,
    processor_func: Callable,
    num_workers: int = 4
):
    """
    Process vault in parallel for better performance.
    """
    notes = list(find_notes(vault_path))

    with Pool(num_workers) as pool:
        worker = partial(process_note_parallel, processor_func=processor_func)
        results = pool.map(worker, notes)

    return results
```

### Pattern: Incremental Processing with State

**Use Case**: Resume processing after interruption.

**Strategy**:
```python
import json

def incremental_process(
    vault_path: Path,
    processor_func: Callable,
    state_file: Path
):
    """
    Process vault with ability to resume.
    """
    # Load previous state
    if state_file.exists():
        state = json.loads(state_file.read_text())
        processed = set(state.get('processed', []))
    else:
        processed = set()
        state = {'processed': []}

    notes = list(find_notes(vault_path))

    try:
        for note in notes:
            if str(note) in processed:
                continue

            processor_func(note)
            processed.add(str(note))

            # Save state periodically
            if len(processed) % 100 == 0:
                state['processed'] = list(processed)
                state_file.write_text(json.dumps(state))

    finally:
        # Save final state
        state['processed'] = list(processed)
        state_file.write_text(json.dumps(state))
```

## Best Practices

1. **Always use dry-run first**: Preview changes before applying
2. **Create backups**: Use `.bak` files or git commits
3. **Process in stages**: Validate → Preview → Execute → Verify
4. **Log everything**: Track what was changed and why
5. **Use version control**: Commit before major batch operations
6. **Test on subset**: Try on small folder before full vault
7. **Validate after**: Run health checks post-processing
8. **Document changes**: Keep log of batch operations performed
