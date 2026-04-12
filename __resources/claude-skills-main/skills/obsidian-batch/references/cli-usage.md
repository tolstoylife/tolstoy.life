# Obsidian Batch Processor - CLI Usage Guide

Complete command-line reference for batch processing Obsidian vaults.

## Installation

```bash
# Clone or download the batch processor scripts
cd obsidian-batch-skill

# Install dependencies
pip install pyyaml  # Only dependency needed

# Make scripts executable
chmod +x batch_processor.py
chmod +x wikilink_extractor.py
chmod +x tag_normalizer.py
chmod +x frontmatter_processor.py
chmod +x vault_analyzer.py
```

## Quick Start

```bash
# Extract all wikilinks from vault
python batch_processor.py extract-wikilinks \
  --vault ~/Documents/ObsidianVault \
  --output links.json

# Normalize tags (preview mode)
python batch_processor.py normalize-tags \
  --vault ~/Documents/ObsidianVault \
  --case lower \
  --dry-run

# Generate vault statistics
python batch_processor.py analyze-vault \
  --vault ~/Documents/ObsidianVault \
  --report stats.md
```

## Global Options

Available for all commands:

```bash
--vault PATH          # Path to Obsidian vault (required)
--dry-run            # Preview changes without modifying files
--verbose, -v        # Enable detailed logging
--help, -h           # Show help message
```

## Commands

### extract-wikilinks

Extract all wikilinks from vault and optionally export to JSON.

**Basic Usage**:
```bash
python batch_processor.py extract-wikilinks \
  --vault ~/vault \
  --output links.json
```

**Options**:
```bash
--output PATH              # Output JSON file path
--include-aliases          # Include alias information in output
```

**Output Format** (`links.json`):
```json
{
  "vault_path": "/Users/me/vault",
  "extraction_timestamp": "2025-01-20T10:30:00",
  "statistics": {
    "total_links": 1543,
    "embedded_links": 87,
    "links_with_aliases": 234,
    "unique_targets": 456
  },
  "links": [
    {
      "source_file": "folder/note.md",
      "target": "Target Note",
      "display_text": "Custom Display",
      "header": "Section Header",
      "is_embedded": false,
      "line_number": 15
    }
  ]
}
```

**Examples**:

```bash
# Extract links with full details
python batch_processor.py extract-wikilinks \
  --vault ~/vault \
  --output links.json \
  --include-aliases \
  --verbose

# Quick link count (no file output)
python batch_processor.py extract-wikilinks \
  --vault ~/vault
```

### normalize-tags

Normalize and validate tags across the vault.

**Basic Usage**:
```bash
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --case lower
```

**Options**:
```bash
--rules PATH              # JSON file with normalization rules
--case CHOICE             # Tag case: lower, upper, title
```

**Rules File Format** (`tag-rules.json`):
```json
{
  "rules": [
    {
      "pattern": "project",
      "replacement": "projects",
      "case_sensitive": false
    },
    {
      "pattern": "TODO",
      "replacement": "tasks/todo",
      "case_sensitive": false
    }
  ]
}
```

**Examples**:

```bash
# Preview tag normalization
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --case lower \
  --dry-run

# Apply normalization rules
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --rules tag-rules.json

# Convert all tags to lowercase
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --case lower

# Combine rules and case normalization
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --rules tag-rules.json \
  --case lower \
  --verbose
```

### process-frontmatter

Process YAML frontmatter in vault files.

**Basic Usage**:
```bash
python batch_processor.py process-frontmatter \
  --vault ~/vault \
  --operation add \
  --key author \
  --value "Your Name"
```

**Options**:
```bash
--operation CHOICE        # Operation: add, remove, update, validate, template
--key TEXT               # Frontmatter key (for add/remove/update)
--value TEXT             # Value to set (for add/update)
--template NAME          # Template name (for template operation)
```

**Available Templates**:
- `basic`: Minimal frontmatter (created, tags, aliases)
- `article`: Article/blog post metadata
- `meeting`: Meeting notes metadata

**Examples**:

```bash
# Add a new field to all notes
python batch_processor.py process-frontmatter \
  --vault ~/vault \
  --operation add \
  --key status \
  --value draft \
  --dry-run

# Update existing field
python batch_processor.py process-frontmatter \
  --vault ~/vault \
  --operation update \
  --key author \
  --value "Jane Doe"

# Remove a field
python batch_processor.py process-frontmatter \
  --vault ~/vault \
  --operation remove \
  --key deprecated_field

# Apply template to notes without frontmatter
python batch_processor.py process-frontmatter \
  --vault ~/vault \
  --operation template \
  --template basic

# Validate frontmatter YAML syntax
python batch_processor.py process-frontmatter \
  --vault ~/vault \
  --operation validate

# Add array value (JSON format)
python batch_processor.py process-frontmatter \
  --vault ~/vault \
  --operation add \
  --key tags \
  --value '["tag1", "tag2"]'
```

### analyze-vault

Generate comprehensive vault statistics and health reports.

**Basic Usage**:
```bash
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report stats.md
```

**Options**:
```bash
--report PATH            # Output report file path
--format CHOICE          # Report format: md, json, html
```

**Report Sections**:
- Health score (0-100)
- File statistics
- Content statistics
- Link statistics (broken links, orphaned notes)
- Tag statistics
- Frontmatter statistics
- Recommendations

**Examples**:

```bash
# Generate markdown report
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report vault-health.md \
  --format md

# Generate JSON report for programmatic use
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report vault-stats.json \
  --format json

# Quick analysis (output to console only)
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --verbose
```

**Sample Markdown Report**:
```markdown
# Vault Analysis Report

Generated: 2025-01-20 10:30:00
Vault: /Users/me/vault

## Health Score: 87.5/100

## File Statistics
- **Total Files**: 1,234
- **Markdown Files**: 987
- **Total Size**: 45.67 MB

## Link Statistics
- **Total Wikilinks**: 3,456
- **Broken Links**: 12 ⚠️
- **Orphaned Notes**: 23 ⚠️

## Recommendations
- 🟡 Fix 12 broken links
- 🟡 Review 23 orphaned notes
- 🟢 Vault is in excellent condition!
```

## Standalone Script Usage

Each processor can also be run independently:

### wikilink_extractor.py

```bash
python wikilink_extractor.py \
  --vault ~/vault \
  --output links.json \
  --include-aliases \
  --verbose
```

### tag_normalizer.py

```bash
python tag_normalizer.py \
  --vault ~/vault \
  --rules tag-rules.json \
  --case lower \
  --dry-run \
  --verbose
```

### frontmatter_processor.py

```bash
python frontmatter_processor.py \
  --vault ~/vault \
  --operation add \
  --key status \
  --value draft \
  --dry-run \
  --verbose
```

### vault_analyzer.py

```bash
python vault_analyzer.py \
  --vault ~/vault \
  --report stats.md \
  --format md \
  --verbose
```

## Advanced Usage

### Piping and Scripting

```bash
# Extract links and process with jq
python batch_processor.py extract-wikilinks \
  --vault ~/vault \
  --output - | jq '.statistics'

# Chain operations
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --case lower && \
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report after-normalize.md

# Process multiple vaults
for vault in ~/vaults/*; do
  echo "Processing $vault"
  python batch_processor.py analyze-vault \
    --vault "$vault" \
    --report "reports/$(basename $vault).md"
done
```

### Using with Git

```bash
# Create checkpoint before batch operation
cd ~/vault
git add .
git commit -m "Before batch processing"

# Run batch operation
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --case lower

# Review changes
git diff

# Rollback if needed
git reset --hard HEAD

# Or commit changes
git add .
git commit -m "Normalized all tags to lowercase"
```

### Configuration Files

Create a configuration file for repeated operations:

**config.json**:
```json
{
  "vault_path": "/Users/me/vault",
  "operations": [
    {
      "command": "normalize-tags",
      "options": {
        "case": "lower",
        "rules": "tag-rules.json"
      }
    },
    {
      "command": "process-frontmatter",
      "options": {
        "operation": "template",
        "template": "basic"
      }
    },
    {
      "command": "analyze-vault",
      "options": {
        "report": "health-report.md",
        "format": "md"
      }
    }
  ]
}
```

Run with config:
```bash
python run_batch_config.py config.json
```

## Common Workflows

### Workflow 1: New Vault Setup

```bash
# 1. Add basic frontmatter to all notes
python batch_processor.py process-frontmatter \
  --vault ~/new-vault \
  --operation template \
  --template basic

# 2. Normalize tag case
python batch_processor.py normalize-tags \
  --vault ~/new-vault \
  --case lower

# 3. Generate initial health report
python batch_processor.py analyze-vault \
  --vault ~/new-vault \
  --report initial-health.md
```

### Workflow 2: Regular Maintenance

```bash
# Weekly vault health check
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report "reports/health-$(date +%Y-%m-%d).md"

# Fix any broken links found
python batch_processor.py fix-links \
  --vault ~/vault \
  --auto-resolve \
  --report-broken broken-links.md
```

### Workflow 3: Migration

```bash
# 1. Backup vault
cp -r ~/vault ~/vault-backup

# 2. Extract current state
python batch_processor.py extract-wikilinks \
  --vault ~/vault \
  --output pre-migration-links.json

# 3. Perform migration
python batch_processor.py migrate-structure \
  --vault ~/vault \
  --strategy by-tags \
  --dry-run  # Preview first

# 4. Execute migration
python batch_processor.py migrate-structure \
  --vault ~/vault \
  --strategy by-tags

# 5. Verify results
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report post-migration.md
```

## Error Handling

### Dry Run Mode

Always use `--dry-run` first to preview changes:

```bash
# Preview before executing
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --case lower \
  --dry-run

# If preview looks good, execute
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --case lower
```

### Verbose Output

Use `--verbose` to see detailed processing information:

```bash
python batch_processor.py process-frontmatter \
  --vault ~/vault \
  --operation add \
  --key status \
  --value draft \
  --verbose
```

### Exit Codes

- `0`: Success
- `1`: Error occurred

Use in scripts:
```bash
if python batch_processor.py analyze-vault --vault ~/vault; then
  echo "Analysis successful"
else
  echo "Analysis failed"
  exit 1
fi
```

## Performance Tips

### Large Vaults (10,000+ notes)

```bash
# Process in batches using find + xargs
find ~/vault -name "*.md" -print0 | \
  xargs -0 -P 4 -I {} python process_single.py {}

# Or use the built-in parallel processing
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --workers 4
```

### Incremental Processing

```bash
# Process only recently modified files
find ~/vault -name "*.md" -mtime -7 | \
  while read file; do
    python process_single.py "$file"
  done
```

## Troubleshooting

### Common Issues

**Issue**: "YAML parsing error"
```bash
# Validate frontmatter syntax
python batch_processor.py process-frontmatter \
  --vault ~/vault \
  --operation validate
```

**Issue**: "Too many broken links"
```bash
# Generate detailed broken links report
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report broken-links.md

# Then fix with fuzzy matching
python batch_processor.py fix-links \
  --vault ~/vault \
  --auto-resolve
```

**Issue**: "Script is slow"
```bash
# Use verbose mode to see what's taking time
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --verbose

# Consider excluding large files or folders
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --exclude-pattern "Archive/*"
```

## Getting Help

```bash
# General help
python batch_processor.py --help

# Command-specific help
python batch_processor.py extract-wikilinks --help
python batch_processor.py normalize-tags --help
python batch_processor.py process-frontmatter --help
python batch_processor.py analyze-vault --help
```

## Version Information

```bash
python batch_processor.py --version
```
