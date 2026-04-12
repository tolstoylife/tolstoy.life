# CLI Usage Reference

Complete command-line reference for obsidian-process scripts.

## Global Options

All scripts support these common arguments:

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--vault PATH` | | Path to Obsidian vault | Required |
| `--dry-run` | | Preview changes without writing | False |
| `--verbose` | `-v` | Enable detailed logging | False |
| `--output PATH` | `-o` | Output file for results (JSON) | stdout |

## wikilink_extractor.py

Extract and analyze wikilinks across the vault.

### Basic Usage

```bash
# Extract all wikilinks to JSON
python wikilink_extractor.py --vault ~/vault --output links.json

# Preview with verbose output
python wikilink_extractor.py --vault ~/vault -v --dry-run
```

### Analysis Options

| Argument | Description |
|----------|-------------|
| `--find-broken` | Report links to non-existent notes |
| `--find-orphans` | Report notes with no incoming links |
| `--stats-only` | Output statistics without full index |
| `--include-embeds` | Include embedded files (`![[...]]`) |
| `--exclude-pattern PATTERN` | Exclude files matching regex |

### Examples

```bash
# Find broken links
python wikilink_extractor.py --vault ~/vault --find-broken

# Find orphaned notes (no backlinks)
python wikilink_extractor.py --vault ~/vault --find-orphans

# Statistics only
python wikilink_extractor.py --vault ~/vault --stats-only

# Exclude templates folder
python wikilink_extractor.py --vault ~/vault --exclude-pattern "templates/.*"
```

### Output Format

```json
{
  "link_index": {
    "Note A.md": [
      {"target": "Note B", "header": null, "display_text": null}
    ]
  },
  "backlink_index": {
    "Note B": [
      {"source": "Note A.md", "line": 5}
    ]
  },
  "statistics": {
    "total_links": 150,
    "unique_targets": 45,
    "broken_links": 3,
    "orphaned_notes": 12
  }
}
```

## tag_normalizer.py

Normalize and transform tags across the vault.

### Basic Usage

```bash
# Normalize to lowercase
python tag_normalizer.py --vault ~/vault --case lower

# Preview changes
python tag_normalizer.py --vault ~/vault --case lower --dry-run
```

### Normalization Options

| Argument | Description |
|----------|-------------|
| `--case {lower,upper,title}` | Case normalization mode |
| `--rules PATH` | JSON file with transformation rules |
| `--stats-only` | Output tag statistics only |
| `--include-frontmatter` | Process frontmatter tags (default: true) |
| `--include-inline` | Process inline tags (default: true) |

### Examples

```bash
# Lowercase all tags
python tag_normalizer.py --vault ~/vault --case lower

# Title case (hierarchical aware)
python tag_normalizer.py --vault ~/vault --case title
# project/active -> Project/Active

# Apply custom rules
python tag_normalizer.py --vault ~/vault --rules tag-rules.json

# Statistics only
python tag_normalizer.py --vault ~/vault --stats-only
```

### Rules File Format

```json
{
  "rules": [
    {
      "pattern": "^todo$",
      "replacement": "task",
      "case_sensitive": false
    },
    {
      "pattern": "^WIP$",
      "replacement": "status/in-progress",
      "case_sensitive": true
    },
    {
      "pattern": "project/(\\w+)",
      "replacement": "projects/$1",
      "case_sensitive": false
    }
  ]
}
```

### Output Format

```json
{
  "statistics": {
    "total_tags": 500,
    "unique_tags": 45,
    "frontmatter_tags": 200,
    "inline_tags": 300,
    "hierarchical_tags": 120
  },
  "tag_hierarchy": {
    "project": {"count": 50, "children": ["active", "archived"]},
    "project/active": {"count": 30, "parent": "project"}
  },
  "modifications": [
    {"file": "note.md", "old": "TODO", "new": "task"}
  ]
}
```

## frontmatter_processor.py

CRUD operations on YAML frontmatter.

### Basic Usage

```bash
# Add field to all notes
python frontmatter_processor.py --vault ~/vault --operation add \
  --key status --value draft

# Preview changes
python frontmatter_processor.py --vault ~/vault --operation add \
  --key status --value draft --dry-run
```

### Operations

| Operation | Description | Required Args |
|-----------|-------------|---------------|
| `add` | Add/update field | `--key`, `--value` |
| `remove` | Delete field | `--key` |
| `update` | Same as add | `--key`, `--value` |
| `validate` | Check against validators | None |
| `template` | Apply template | `--template` |

### Options

| Argument | Description |
|----------|-------------|
| `--operation OP` | Operation to perform |
| `--key KEY` | Frontmatter key name |
| `--value VALUE` | Value to set (supports JSON) |
| `--template NAME` | Template name |
| `--overwrite` | Overwrite existing values |

### Examples

```bash
# Add single field
python frontmatter_processor.py --vault ~/vault \
  --operation add --key created --value "2024-01-01"

# Add array field (JSON)
python frontmatter_processor.py --vault ~/vault \
  --operation add --key tags --value '["new", "imported"]'

# Add object field (JSON)
python frontmatter_processor.py --vault ~/vault \
  --operation add --key metadata --value '{"source": "import", "version": 1}'

# Remove field
python frontmatter_processor.py --vault ~/vault \
  --operation remove --key deprecated_field

# Apply template
python frontmatter_processor.py --vault ~/vault \
  --operation template --template article

# Validate all frontmatter
python frontmatter_processor.py --vault ~/vault --operation validate
```

### Built-in Templates

**basic**:
```yaml
created: <ISO timestamp>
tags: []
aliases: []
```

**article**:
```yaml
created: <ISO timestamp>
modified: <ISO timestamp>
tags: []
aliases: []
author: ""
published: false
draft: true
```

**meeting**:
```yaml
created: <ISO timestamp>
tags: [meeting]
attendees: []
date: <current date>
location: ""
```

### Output Format

```json
{
  "success": true,
  "files_processed": 100,
  "files_modified": 45,
  "errors": [],
  "warnings": ["note.md: frontmatter already has 'status' field"],
  "metadata": {
    "operation": "add",
    "key": "status",
    "value": "draft"
  }
}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Vault not found |
| 4 | Permission denied |
| 5 | Partial failure (some files had errors) |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OBSIDIAN_VAULT` | Default vault path if `--vault` not specified |
| `OBSIDIAN_PROCESS_LOG` | Log file path |
| `OBSIDIAN_PROCESS_BACKUP` | Backup directory for modified files |
