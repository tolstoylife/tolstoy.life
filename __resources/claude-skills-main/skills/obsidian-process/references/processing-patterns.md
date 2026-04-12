# Processing Patterns Reference

Advanced patterns for batch processing Obsidian vaults.

## Regex Patterns

### Wikilink Extraction

```python
# Match all wikilinks (including embeds)
WIKILINK_PATTERN = r'(!?\[\[)([^\]]+?)\]\]'

# Parse link components
LINK_PARTS = r'^([^#|\^]+?)(?:#([^|\^]+?))?(?:\^([^|]+?))?(?:\|(.+?))?$'
# Groups: target, header, block_id, display_text
```

### Tag Extraction

```python
# Inline tags (not in code blocks)
INLINE_TAG = r'(?:^|\s)#([\w/-]+)'

# Frontmatter tags array
# Handled via YAML parsing - supports both formats:
# tags: [tag1, tag2]
# tags:
#   - tag1
#   - tag2
```

### Frontmatter Extraction

```python
# Match YAML frontmatter block
FRONTMATTER = r'^---\s*\n(.*?)\n---\s*\n'
# Flags: DOTALL | MULTILINE
```

## Data Structures

### Link Index (Forward Links)

```python
{
    "source_note.md": [
        {
            "target": "Target Note",
            "header": "Section",      # optional
            "block_id": "abc123",     # optional
            "display_text": "alias",  # optional
            "is_embedded": False,
            "line_number": 42
        }
    ]
}
```

### Backlink Index (Reverse Links)

```python
{
    "Target Note": [
        {
            "source": "source_note.md",
            "context": "...surrounding text...",
            "line_number": 42
        }
    ]
}
```

### Tag Hierarchy

```python
{
    "project": {
        "children": ["active", "archived"],
        "count": 50,
        "files": ["note1.md", "note2.md"]
    },
    "project/active": {
        "parent": "project",
        "children": ["urgent"],
        "count": 20
    }
}
```

## Common Transformations

### Alias Extraction from Title

```python
def extract_aliases(title: str) -> List[str]:
    """Extract potential aliases from note title."""
    aliases = []
    # Handle parenthetical alternates: "Term (Also Known As)"
    if '(' in title and ')' in title:
        base = title.split('(')[0].strip()
        alt = title.split('(')[1].rstrip(')')
        aliases.extend([base, alt])
    return aliases
```

### Path Normalization

```python
def normalize_path(link_target: str, current_file: Path) -> Path:
    """Resolve relative link target to absolute path."""
    if link_target.startswith('/'):
        return vault_root / link_target.lstrip('/')
    return current_file.parent / link_target
```

### Frontmatter Merge

```python
def merge_frontmatter(existing: Dict, updates: Dict, overwrite: bool = False) -> Dict:
    """Merge updates into existing frontmatter."""
    result = existing.copy()
    for key, value in updates.items():
        if key not in result or overwrite:
            result[key] = value
        elif isinstance(result[key], list) and isinstance(value, list):
            result[key] = list(set(result[key] + value))  # Dedupe
    return result
```

## Error Handling Patterns

### Graceful Degradation

```python
def process_file_safe(file_path: Path) -> Optional[ProcessingResult]:
    """Process with fallback on errors."""
    try:
        return process_file(file_path)
    except UnicodeDecodeError:
        logger.warning(f"Encoding issue: {file_path}, trying latin-1")
        return process_file(file_path, encoding='latin-1')
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in {file_path}: {e}")
        return None  # Skip file, continue batch
```

### Batch Error Collection

```python
def process_batch(files: List[Path]) -> ProcessingResult:
    """Process batch collecting all errors."""
    errors, warnings = [], []
    processed, modified = 0, 0

    for file in files:
        try:
            if process_file(file):
                modified += 1
            processed += 1
        except Exception as e:
            errors.append(f"{file}: {e}")

    return ProcessingResult(
        success=len(errors) == 0,
        files_processed=processed,
        files_modified=modified,
        errors=errors,
        warnings=warnings
    )
```

## Performance Optimization

### Lazy File Reading

```python
def iter_files_content(vault: Path) -> Iterator[Tuple[Path, str]]:
    """Lazy iterator over vault files."""
    for md_file in vault.rglob('*.md'):
        if '.obsidian' not in md_file.parts:
            yield md_file, md_file.read_text(encoding='utf-8')
```

### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor

def process_parallel(files: List[Path], workers: int = 4):
    """Process files in parallel."""
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(process_file, files))
    return results
```

### Incremental Updates

```python
def needs_processing(file: Path, cache: Dict[str, float]) -> bool:
    """Check if file needs reprocessing based on mtime."""
    mtime = file.stat().st_mtime
    cached_mtime = cache.get(str(file), 0)
    return mtime > cached_mtime
```
