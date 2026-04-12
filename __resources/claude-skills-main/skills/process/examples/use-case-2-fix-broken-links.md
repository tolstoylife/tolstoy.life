# Use Case 2: Validate and Fix Broken Wikilinks

## Scenario

After reorganizing your vault, renaming notes, or importing content from another system, you have 127 broken wikilinks scattered across 89 different notes.

## Problem Analysis

**Common causes of broken links**:
1. Notes were renamed
2. Notes were moved to different folders
3. Typos in link names
4. Case sensitivity issues
5. Deleted notes still being referenced
6. Import/export issues

## Step 1: Identify Broken Links

Generate a comprehensive broken links report:

```bash
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report broken-links-report.md \
  --format md
```

**Sample Report Output**:
```markdown
## Link Statistics

- **Total Wikilinks**: 3,456
- **Broken Links**: 127 ⚠️

### Broken Links (Sample)

- `Project Planning` → `Stakeholder Analysis` (not found)
- `Meeting Notes 2025-01-15` → `Action Items` (not found)
- `Recipe Collection` → `chocolate-cake` (not found)
```

## Step 2: Extract Detailed Broken Link Information

```bash
# Create a custom script to extract just broken links
python extract_broken_links.py --vault ~/vault --output broken-links.json
```

**extract_broken_links.py**:
```python
#!/usr/bin/env python3
import json
from pathlib import Path
from collections import defaultdict
import re

def find_broken_links(vault_path):
    vault = Path(vault_path)

    # Get all note names
    note_names = {f.stem for f in vault.rglob('*.md')}

    broken_links = defaultdict(list)
    wikilink_pattern = re.compile(r'\[\[([^\]|#]+)')

    for md_file in vault.rglob('*.md'):
        content = md_file.read_text()

        for match in wikilink_pattern.finditer(content):
            target = match.group(1).strip()

            # Check if target exists
            if target not in note_names:
                broken_links[md_file.stem].append({
                    'target': target,
                    'file': str(md_file.relative_to(vault))
                })

    return broken_links

# Usage
vault_path = Path('~/vault').expanduser()
broken = find_broken_links(vault_path)

# Save to JSON
with open('broken-links.json', 'w') as f:
    json.dump(broken, f, indent=2)

# Print summary
total_broken = sum(len(links) for links in broken.values())
print(f"Found {total_broken} broken links in {len(broken)} files")
```

```bash
python extract_broken_links.py
```

**Output** (`broken-links.json`):
```json
{
  "Project Planning": [
    {
      "target": "Stakeholder Analysis",
      "file": "projects/Project Planning.md"
    }
  ],
  "Meeting Notes 2025-01-15": [
    {
      "target": "Action Items",
      "file": "meetings/Meeting Notes 2025-01-15.md"
    }
  ]
}
```

## Step 3: Categorize Broken Links

Analyze the broken links to determine fixing strategy:

```python
# categorize_broken_links.py
import json
from pathlib import Path
from difflib import SequenceMatcher

def categorize_broken_links(broken_links_file, vault_path):
    with open(broken_links_file) as f:
        broken = json.load(f)

    vault = Path(vault_path)
    note_names = {f.stem for f in vault.rglob('*.md')}

    categorized = {
        'typos': [],           # High similarity to existing note
        'renamed': [],         # Likely renamed notes
        'case_mismatch': [],   # Case sensitivity issues
        'deleted': [],         # No similar notes found
        'ambiguous': []        # Multiple possible matches
    }

    for source, links in broken.items():
        for link in links:
            target = link['target']

            # Find similar notes
            matches = []
            for note_name in note_names:
                similarity = SequenceMatcher(None, target.lower(), note_name.lower()).ratio()
                if similarity > 0.7:
                    matches.append({
                        'note': note_name,
                        'similarity': similarity
                    })

            matches.sort(key=lambda x: x['similarity'], reverse=True)

            # Categorize
            if not matches:
                categorized['deleted'].append(link)
            elif len(matches) == 1 and matches[0]['similarity'] > 0.9:
                link['suggested_fix'] = matches[0]['note']
                categorized['typos'].append(link)
            elif matches[0]['similarity'] > 0.8:
                link['suggested_fix'] = matches[0]['note']
                categorized['renamed'].append(link)
            elif target.lower() in [n.lower() for n in note_names]:
                # Find exact case-insensitive match
                exact_match = next(n for n in note_names if n.lower() == target.lower())
                link['suggested_fix'] = exact_match
                categorized['case_mismatch'].append(link)
            elif len(matches) > 1:
                link['possible_matches'] = matches[:3]
                categorized['ambiguous'].append(link)
            else:
                categorized['deleted'].append(link)

    return categorized

# Usage
categorized = categorize_broken_links('broken-links.json', '~/vault')

with open('categorized-broken-links.json', 'w') as f:
    json.dump(categorized, f, indent=2)

# Print summary
for category, links in categorized.items():
    print(f"{category}: {len(links)}")
```

```bash
python categorize_broken_links.py
```

**Output**:
```
typos: 45
renamed: 32
case_mismatch: 18
deleted: 12
ambiguous: 20
```

## Step 4: Automatic Fixes

### Fix Typos and Obvious Mistakes

```bash
# Fix links with high confidence matches (similarity > 0.9)
python fix_broken_links.py \
  --vault ~/vault \
  --categories typos,case_mismatch \
  --min-similarity 0.9 \
  --dry-run
```

**fix_broken_links.py**:
```python
#!/usr/bin/env python3
import json
import re
from pathlib import Path

def fix_broken_links(vault_path, categorized_file, categories, min_similarity=0.9, dry_run=False):
    with open(categorized_file) as f:
        categorized = json.load(f)

    vault = Path(vault_path)
    fixes_applied = 0

    for category in categories:
        if category not in categorized:
            continue

        for link_info in categorized[category]:
            if 'suggested_fix' not in link_info:
                continue

            file_path = vault / link_info['file']
            if not file_path.exists():
                continue

            old_target = link_info['target']
            new_target = link_info['suggested_fix']

            # Read file
            content = file_path.read_text()

            # Replace link (handle various formats)
            patterns = [
                rf'\[\[{re.escape(old_target)}\]\]',  # [[target]]
                rf'\[\[{re.escape(old_target)}\|',     # [[target|alias]]
                rf'\[\[{re.escape(old_target)}#',      # [[target#header]]
            ]

            updated_content = content
            for pattern in patterns:
                updated_content = re.sub(
                    pattern,
                    lambda m: m.group(0).replace(old_target, new_target),
                    updated_content
                )

            if updated_content != content:
                if dry_run:
                    print(f"[DRY-RUN] Would fix in {link_info['file']}: {old_target} → {new_target}")
                else:
                    file_path.write_text(updated_content)
                    print(f"Fixed in {link_info['file']}: {old_target} → {new_target}")

                fixes_applied += 1

    print(f"\nTotal fixes applied: {fixes_applied}")

# Usage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--vault', required=True)
parser.add_argument('--categories', default='typos,case_mismatch')
parser.add_argument('--min-similarity', type=float, default=0.9)
parser.add_argument('--dry-run', action='store_true')
args = parser.parse_args()

fix_broken_links(
    args.vault,
    'categorized-broken-links.json',
    args.categories.split(','),
    args.min_similarity,
    args.dry_run
)
```

**Preview the fixes**:
```bash
python fix_broken_links.py \
  --vault ~/vault \
  --categories typos,case_mismatch \
  --dry-run
```

**Apply the fixes**:
```bash
python fix_broken_links.py \
  --vault ~/vault \
  --categories typos,case_mismatch
```

**Expected output**:
```
Fixed in projects/Project Planning.md: Stakeholder Analysis → Stakeholders Analysis
Fixed in meetings/Meeting Notes 2025-01-15.md: Action Items → Action-Items
Fixed in recipes/Recipe Collection.md: chocolate-cake → Chocolate Cake

Total fixes applied: 63
```

## Step 5: Handle Renamed Notes

For notes that were likely renamed, create a mapping file:

**rename-mapping.json**:
```json
{
  "Old Project Name": "New Project Name",
  "Meeting 2025-01-10": "2025-01-10 Team Meeting",
  "Todo List": "Tasks Overview"
}
```

Apply the mapping:

```bash
python apply_rename_mapping.py \
  --vault ~/vault \
  --mapping rename-mapping.json \
  --dry-run
```

**apply_rename_mapping.py**:
```python
#!/usr/bin/env python3
import json
import re
from pathlib import Path

def apply_rename_mapping(vault_path, mapping_file, dry_run=False):
    with open(mapping_file) as f:
        mapping = json.load(f)

    vault = Path(vault_path)
    updates = 0

    for md_file in vault.rglob('*.md'):
        content = md_file.read_text()
        updated_content = content

        for old_name, new_name in mapping.items():
            # Replace all variations
            patterns = [
                (rf'\[\[{re.escape(old_name)}\]\]', f'[[{new_name}]]'),
                (rf'\[\[{re.escape(old_name)}\|', f'[[{new_name}|'),
                (rf'\[\[{re.escape(old_name)}#', f'[[{new_name}#'),
                (rf'!\[\[{re.escape(old_name)}\]\]', f'![[{new_name}]]'),
            ]

            for pattern, replacement in patterns:
                updated_content = re.sub(pattern, replacement, updated_content)

        if updated_content != content:
            if dry_run:
                print(f"[DRY-RUN] Would update: {md_file.relative_to(vault)}")
            else:
                md_file.write_text(updated_content)
                print(f"Updated: {md_file.relative_to(vault)}")
            updates += 1

    print(f"\nTotal files updated: {updates}")

# Usage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--vault', required=True)
parser.add_argument('--mapping', required=True)
parser.add_argument('--dry-run', action='store_true')
args = parser.parse_args()

apply_rename_mapping(args.vault, args.mapping, args.dry_run)
```

## Step 6: Handle Ambiguous Cases

For ambiguous matches, generate an interactive prompt:

```bash
python resolve_ambiguous_links.py \
  --vault ~/vault \
  --categorized categorized-broken-links.json
```

**resolve_ambiguous_links.py**:
```python
#!/usr/bin/env python3
import json
from pathlib import Path
import re

def resolve_ambiguous_links(vault_path, categorized_file):
    with open(categorized_file) as f:
        categorized = json.load(f)

    vault = Path(vault_path)
    resolutions = {}

    for link_info in categorized.get('ambiguous', []):
        print(f"\n{'='*60}")
        print(f"Broken link: {link_info['target']}")
        print(f"In file: {link_info['file']}")
        print(f"\nPossible matches:")

        matches = link_info.get('possible_matches', [])
        for i, match in enumerate(matches, 1):
            print(f"  {i}. {match['note']} (similarity: {match['similarity']:.2%})")

        print(f"  s. Skip this link")
        print(f"  c. Create new note")
        print(f"  d. Delete this link")

        choice = input("\nSelect action [1-{}/s/c/d]: ".format(len(matches)))

        if choice == 's':
            continue
        elif choice == 'c':
            new_note_name = input("Enter new note name: ")
            resolutions[link_info['target']] = {
                'action': 'create',
                'note': new_note_name
            }
        elif choice == 'd':
            resolutions[link_info['target']] = {
                'action': 'delete'
            }
        elif choice.isdigit() and 1 <= int(choice) <= len(matches):
            selected = matches[int(choice) - 1]['note']
            resolutions[link_info['target']] = {
                'action': 'replace',
                'note': selected
            }

    # Save resolutions
    with open('ambiguous-resolutions.json', 'w') as f:
        json.dump(resolutions, f, indent=2)

    print(f"\n\nResolutions saved to ambiguous-resolutions.json")
    print(f"Total resolutions: {len(resolutions)}")

# Usage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--vault', required=True)
parser.add_argument('--categorized', required=True)
args = parser.parse_args()

resolve_ambiguous_links(args.vault, args.categorized)
```

Apply the resolutions:

```bash
python apply_resolutions.py \
  --vault ~/vault \
  --resolutions ambiguous-resolutions.json
```

## Step 7: Handle Deleted Notes

For links to notes that don't exist and have no good matches, you have options:

### Option A: Create Stub Notes

```bash
python create_stub_notes.py \
  --vault ~/vault \
  --categorized categorized-broken-links.json
```

**create_stub_notes.py**:
```python
#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

def create_stub_notes(vault_path, categorized_file):
    with open(categorized_file) as f:
        categorized = json.load(f)

    vault = Path(vault_path)
    created = 0

    for link_info in categorized.get('deleted', []):
        note_name = link_info['target']
        note_path = vault / f"{note_name}.md"

        if note_path.exists():
            continue

        # Create stub note
        content = f"""---
created: {datetime.now().isoformat()}
tags: [stub]
---

# {note_name}

This note was automatically created because it was referenced in:
- [[{Path(link_info['file']).stem}]]

Add content here or delete this note if not needed.
"""

        note_path.write_text(content)
        print(f"Created stub: {note_name}.md")
        created += 1

    print(f"\nTotal stubs created: {created}")
```

### Option B: Remove Broken Links

```bash
python remove_broken_links.py \
  --vault ~/vault \
  --categorized categorized-broken-links.json \
  --categories deleted
```

## Step 8: Verification

After fixing links, verify the results:

```bash
# Generate new analysis report
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report after-fixes-report.md

# Extract new link statistics
python batch_processor.py extract-wikilinks \
  --vault ~/vault \
  --output after-fixes-links.json
```

**Compare before and after**:

```bash
# Compare broken link counts
echo "Before fixes:"
grep "Broken Links:" broken-links-report.md

echo "After fixes:"
grep "Broken Links:" after-fixes-report.md
```

**Expected output**:
```
Before fixes:
- **Broken Links**: 127 ⚠️

After fixes:
- **Broken Links**: 4 ⚠️
```

## Results Summary

```bash
# Generate summary report
python generate_fix_summary.py
```

**fix-summary.md**:
```markdown
# Broken Links Fix Summary

## Statistics

- **Initial broken links**: 127
- **Automatically fixed**: 95
- **Manually resolved**: 28
- **Remaining broken**: 4

## Breakdown by Category

- Typos (auto-fixed): 45
- Case mismatches (auto-fixed): 18
- Renamed notes (mapped): 32
- Ambiguous (manually resolved): 20
- Deleted notes (stubs created): 8
- Unresolvable: 4

## Success Rate: 97%

## Remaining Issues

1. [[Deleted Project X]] - No matching note found
2. [[Old Reference]] - Ambiguous, needs manual review
3. [[External Link]] - Not an internal note
4. [[TBD Content]] - Intentionally broken, placeholder
```

## Best Practices

1. **Regular link validation**: Run weekly
2. **Fix immediately**: Don't let broken links accumulate
3. **Use aliases**: Prevents breaks when renaming
4. **Careful renaming**: Update links when renaming notes
5. **Version control**: Commit before and after fixes

## Automation

Create a scheduled task to check for broken links:

```bash
#!/bin/bash
# check-broken-links.sh

VAULT_PATH="$HOME/vault"
REPORT_DIR="$HOME/vault-reports"
DATE=$(date +%Y-%m-%d)

# Analyze vault
python batch_processor.py analyze-vault \
  --vault "$VAULT_PATH" \
  --report "$REPORT_DIR/health-$DATE.md"

# Extract broken link count
BROKEN=$(grep -o "Broken Links: [0-9]*" "$REPORT_DIR/health-$DATE.md" | grep -o "[0-9]*")

# Alert if broken links found
if [ "$BROKEN" -gt 0 ]; then
  echo "WARNING: $BROKEN broken links found!"
  # Send notification or email
fi
```

Add to cron:
```bash
# Run daily at 9 AM
0 9 * * * /path/to/check-broken-links.sh
```
