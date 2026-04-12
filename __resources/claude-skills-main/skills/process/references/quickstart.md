---
name: quickstart
description: "Quick start for Obsidian batch processing scripts: setup, common commands, and safety checklist."
---

# Quick Start Guide - Obsidian Batch Processing

Get started with Obsidian batch processing in about 5 minutes.

## Installation

Run commands from the repo root:

```bash
cd /path/to/obsidian-batch-skill
python -m venv .venv
source .venv/bin/activate
pip install pyyaml
```

## 5-Minute Tutorial

### 1. Extract Wikilinks (30 seconds)

```bash
python scripts/batch_processor.py extract-wikilinks \
  --vault ~/vault \
  --output links.json
```

Output: JSON file with wikilinks and basic stats.

### 2. Normalize Tags (2 minutes)

```bash
# Preview first
python scripts/batch_processor.py normalize-tags \
  --vault ~/vault \
  --case lower \
  --dry-run

# Apply changes
python scripts/batch_processor.py normalize-tags \
  --vault ~/vault \
  --case lower
```

Result: All tags converted to lowercase.

### 3. Generate Health Report (45 seconds)

```bash
python scripts/batch_processor.py analyze-vault \
  --vault ~/vault \
  --report health.json \
  --format json
```

Output: JSON report with vault statistics and health score.

### 4. Update Frontmatter (1 minute)

```bash
python scripts/batch_processor.py process-frontmatter \
  --vault ~/vault \
  --operation add \
  --key status \
  --value draft
```

Result: Adds a frontmatter field to notes.

## Common Commands

### Analysis

```bash
# Quick health check (logs summary)
python scripts/batch_processor.py analyze-vault --vault ~/vault

# Detailed JSON report
python scripts/batch_processor.py analyze-vault \
  --vault ~/vault \
  --report stats.json \
  --format json
```

### Tags

```bash
# Lowercase all tags
python scripts/batch_processor.py normalize-tags --vault ~/vault --case lower

# Apply custom rules
python scripts/batch_processor.py normalize-tags --vault ~/vault --rules rules.json

# Preview changes
python scripts/batch_processor.py normalize-tags --vault ~/vault --dry-run
```

### Links

```bash
# Extract all links
python scripts/batch_processor.py extract-wikilinks --vault ~/vault --output links.json
```

### Frontmatter

```bash
# Add field to all notes
python scripts/batch_processor.py process-frontmatter \
  --vault ~/vault --operation add --key status --value draft

# Remove field
python scripts/batch_processor.py process-frontmatter \
  --vault ~/vault --operation remove --key deprecated

# Update field
python scripts/batch_processor.py process-frontmatter \
  --vault ~/vault --operation update --key status --value published

# Validate frontmatter
python scripts/batch_processor.py process-frontmatter \
  --vault ~/vault --operation validate
```

## Safety Checklist

Before running any batch operation:

1. Backup your vault.
   ```bash
   cp -r ~/vault ~/vault-backup-$(date +%Y%m%d)
   ```

2. Use dry-run mode.
   ```bash
   python scripts/batch_processor.py <command> --dry-run
   ```

3. Review the preview and test on a small subset.

4. Execute the operation.

5. Verify results.
   ```bash
   python scripts/batch_processor.py analyze-vault --vault ~/vault
   ```

## File Structure

```
obsidian-batch-skill/
├── SKILL.md
├── scripts/
│   ├── batch_processor.py
│   ├── wikilink_extractor.py
│   ├── tag_normalizer.py
│   ├── frontmatter_processor.py
│   └── vault_analyzer.py
├── references/
│   ├── quickstart.md
│   ├── cli-usage.md
│   ├── obsidian-syntax.md
│   └── processing-patterns.md
└── examples/
    ├── use-case-1-migrate-flat-to-hierarchical.md
    ├── use-case-2-fix-broken-links.md
    ├── use-case-3-normalize-tags.md
    └── use-case-4-vault-statistics-report.md
```

## Next Steps

- Read `references/cli-usage.md` for the full command reference.
- Review `references/obsidian-syntax.md` for parsing patterns and edge cases.
- Study `references/processing-patterns.md` for multi-step workflows.
- Browse `examples/` for end-to-end use cases.

## Common Issues

YAML parsing errors:

```bash
python scripts/batch_processor.py process-frontmatter \
  --vault ~/vault --operation validate
```
