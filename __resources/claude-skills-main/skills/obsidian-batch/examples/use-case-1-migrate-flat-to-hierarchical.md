# Use Case 1: Migrate 1000+ Notes from Flat to Hierarchical Structure

## Scenario

You have 1,200 notes in a flat structure (all in root folder) and want to organize them into a hierarchical folder structure based on tags and content type.

**Current Structure**:
```
vault/
├── Meeting with John.md
├── Project Alpha Notes.md
├── Project Beta Planning.md
├── Quick Thought on AI.md
├── Recipe - Chocolate Cake.md
└── ... (1,197 more files)
```

**Desired Structure**:
```
vault/
├── projects/
│   ├── alpha/
│   │   └── Project Alpha Notes.md
│   └── beta/
│       └── Project Beta Planning.md
├── meetings/
│   └── Meeting with John.md
├── thoughts/
│   └── Quick Thought on AI.md
└── recipes/
    └── Chocolate Cake.md
```

## Prerequisites

1. **Backup your vault**:
```bash
cp -r ~/vault ~/vault-backup-$(date +%Y%m%d)
```

2. **Commit to git** (if using version control):
```bash
cd ~/vault
git add .
git commit -m "Checkpoint before hierarchical migration"
```

3. **Verify tags are consistent**:
```bash
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --case lower \
  --dry-run
```

## Step 1: Analyze Current State

Extract current link structure and statistics:

```bash
# Generate baseline report
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report pre-migration-report.md \
  --format md

# Extract all wikilinks (for validation later)
python batch_processor.py extract-wikilinks \
  --vault ~/vault \
  --output pre-migration-links.json \
  --include-aliases
```

**Review the report**:
- Note the number of files
- Check for broken links (fix before migration)
- Review tag distribution

## Step 2: Create Migration Strategy

Create a configuration file that maps tags to folder paths:

**migration-config.json**:
```json
{
  "strategy": "by-tags",
  "tag_to_folder_map": {
    "projects/alpha": "projects/alpha",
    "projects/beta": "projects/beta",
    "projects": "projects/general",
    "meeting": "meetings",
    "meetings": "meetings",
    "thought": "thoughts",
    "idea": "thoughts",
    "recipe": "recipes",
    "cooking": "recipes",
    "archive": "archive",
    "temp": "archive/temp"
  },
  "default_folder": "uncategorized",
  "update_links": true,
  "create_index_files": true,
  "preserve_original_tags": true,
  "handling": {
    "multiple_tags": "use_first",
    "no_tags": "uncategorized",
    "conflicts": "prompt"
  }
}
```

## Step 3: Preview Migration

Run in dry-run mode to see what would happen:

```bash
python batch_processor.py migrate-structure \
  --vault ~/vault \
  --strategy by-tags \
  --config migration-config.json \
  --dry-run \
  --verbose > migration-preview.txt
```

**Review the preview**:
- Check folder assignments
- Verify no conflicts
- Ensure important notes are categorized correctly

## Step 4: Execute Migration

Run the actual migration:

```bash
python batch_processor.py migrate-structure \
  --vault ~/vault \
  --strategy by-tags \
  --config migration-config.json \
  --verbose
```

**Expected output**:
```
INFO: Starting migration with strategy: by-tags
INFO: Found 1,200 markdown files
INFO: Created folder: projects/alpha
INFO: Created folder: projects/beta
INFO: Created folder: meetings
INFO: Moved: Project Alpha Notes.md → projects/alpha/Project Alpha Notes.md
INFO: Moved: Meeting with John.md → meetings/Meeting with John.md
INFO: Updating wikilinks in 847 files...
INFO: Migration completed successfully
INFO: Files processed: 1,200
INFO: Files moved: 1,200
INFO: Folders created: 15
INFO: Links updated: 3,456
```

## Step 5: Verify Migration

### Check for Broken Links

```bash
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report post-migration-report.md \
  --format md
```

**Review the report for**:
- Broken links (should be 0 if migration was successful)
- Orphaned notes
- Health score

### Validate Link Updates

```bash
# Extract links after migration
python batch_processor.py extract-wikilinks \
  --vault ~/vault \
  --output post-migration-links.json

# Compare link counts
echo "Before migration:"
jq '.statistics.total_links' pre-migration-links.json

echo "After migration:"
jq '.statistics.total_links' post-migration-links.json

# These should match!
```

### Manual Spot Check

Open Obsidian and verify:
1. Notes are in correct folders
2. Wikilinks still work
3. No broken links
4. Graph view shows proper connections

## Step 6: Handle Edge Cases

### Uncategorized Notes

Check notes that ended up in uncategorized:

```bash
# List uncategorized notes
find ~/vault/uncategorized -name "*.md" -exec basename {} \;

# Add appropriate tags and re-run migration on just this folder
```

### Notes with Multiple Tags

Review notes with multiple primary tags:

```bash
# Extract notes with multiple tags
python -c "
import json
with open('post-migration-links.json') as f:
    data = json.load(f)
    # Custom script to find notes with multiple category tags
"
```

Manually review and move if needed.

## Step 7: Create Index Files

Generate index files for each major folder:

```bash
# Create index in each folder
for folder in ~/vault/*/; do
  folder_name=$(basename "$folder")
  echo "# ${folder_name^} Index" > "$folder/README.md"
  echo "" >> "$folder/README.md"
  echo "## Notes in this folder:" >> "$folder/README.md"
  echo "" >> "$folder/README.md"

  # List all markdown files (except README)
  find "$folder" -maxdepth 1 -name "*.md" ! -name "README.md" -exec basename {} .md \; | \
    sort | \
    while read note; do
      echo "- [[$note]]" >> "$folder/README.md"
    done
done
```

## Step 8: Cleanup and Optimization

### Remove Empty Folders

```bash
find ~/vault -type d -empty -delete
```

### Normalize Tags After Migration

```bash
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --case lower
```

### Update Frontmatter

Add folder information to frontmatter:

```python
# update_folder_metadata.py
from pathlib import Path
import yaml
import re

vault_path = Path('~/vault').expanduser()

for md_file in vault_path.rglob('*.md'):
    # Get relative folder path
    folder = md_file.relative_to(vault_path).parent

    # Read content
    content = md_file.read_text()

    # Extract/update frontmatter
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if fm_match:
        fm = yaml.safe_load(fm_match.group(1)) or {}
        fm['folder'] = str(folder)

        # Reconstruct
        new_fm = yaml.dump(fm, default_flow_style=False)
        new_content = f"---\n{new_fm}---\n" + content[fm_match.end():]

        md_file.write_text(new_content)
```

```bash
python update_folder_metadata.py
```

## Step 9: Final Verification

### Compare Statistics

```bash
# Generate final report
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report final-migration-report.md \
  --format md

# Compare reports
diff pre-migration-report.md final-migration-report.md
```

**Expected differences**:
- File count should be same
- Link count should be same
- Broken links should be 0 (or less than before)
- Health score should be same or better

### Test in Obsidian

1. Close and reopen Obsidian
2. Verify all notes are accessible
3. Check graph view
4. Test random wikilinks
5. Search for notes (should all be found)

## Step 10: Commit Changes

```bash
cd ~/vault
git add .
git commit -m "Migrate to hierarchical structure by tags

- Organized 1,200 notes into folder hierarchy
- Updated all wikilinks
- Created index files
- No broken links
"
```

## Rollback Plan

If something goes wrong:

```bash
# Restore from backup
rm -rf ~/vault
mv ~/vault-backup-YYYYMMDD ~/vault

# Or rollback git
cd ~/vault
git reset --hard HEAD~1
```

## Performance Notes

For 1,200 notes:
- Analysis: ~30 seconds
- Migration preview: ~45 seconds
- Actual migration: ~2 minutes
- Link updates: ~3 minutes
- Total time: ~6 minutes

For 10,000+ notes:
- Consider processing in batches
- Use parallel processing options
- Expect 30-60 minutes total

## Troubleshooting

### Issue: Some links are broken after migration

**Solution**:
```bash
# Run the link fixer
python batch_processor.py fix-links \
  --vault ~/vault \
  --auto-resolve \
  --report-broken remaining-broken.md
```

### Issue: Notes in wrong folders

**Solution**:
```bash
# Manually move the note
mv ~/vault/wrong-folder/note.md ~/vault/correct-folder/

# Update all references
python batch_processor.py fix-links \
  --vault ~/vault \
  --source "wrong-folder/note" \
  --target "correct-folder/note"
```

### Issue: Obsidian doesn't see the changes

**Solution**:
1. Close Obsidian completely
2. Re-open the vault
3. Force refresh: Cmd+R (Mac) or Ctrl+R (Windows)

## Post-Migration Best Practices

1. **Update your templates** to include folder information
2. **Create MOCs** (Maps of Content) for major folders
3. **Set up Obsidian folder notes** plugin
4. **Configure folder-specific settings** in Obsidian
5. **Update your daily note template** to use new structure

## Results

**Before**:
- 1,200 notes in root folder
- Difficult to navigate
- No organization
- Chaos!

**After**:
- 15 organized folders
- Clear structure
- Easy navigation
- 0 broken links
- Health score: 92/100

Migration successful! 🎉
