# Use Case 3: Normalize Tags Across Entire Vault

## Scenario

Your vault has grown organically over 2 years and now has inconsistent tag usage:
- Mix of singular/plural: `#project` vs `#projects`
- Case inconsistencies: `#Meeting`, `#meeting`, `#MEETING`
- Redundant tags: `#todo`, `#task`, `#action-item`
- Inconsistent hierarchy: `#work/project` vs `#projects/work`
- Typos: `#reciepe`, `#recipie`, `#recipe`

**Goal**: Standardize all 847 tags across 2,341 notes to a consistent, hierarchical system.

## Step 1: Analyze Current Tag Usage

Extract and analyze all tags:

```bash
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report tag-analysis.md
```

Review the tag statistics section:

```markdown
## Tag Statistics

- **Total Tags**: 6,234
- **Unique Tags**: 847

### Most Used Tags

- `#project` (342 uses)
- `#projects` (287 uses)
- `#meeting` (234 uses)
- `#Meeting` (156 uses)
- `#todo` (198 uses)
- `#task` (143 uses)
```

## Step 2: Create Tag Inventory

Generate a complete tag inventory:

```bash
python create_tag_inventory.py \
  --vault ~/vault \
  --output tag-inventory.json
```

**create_tag_inventory.py**:
```python
#!/usr/bin/env python3
import json
import re
from pathlib import Path
from collections import Counter

def create_tag_inventory(vault_path, output_file):
    vault = Path(vault_path)
    tag_pattern = re.compile(r'(?:^|\s)#([\w/-]+)')

    # Count all tags
    tag_counter = Counter()
    tag_locations = {}

    for md_file in vault.rglob('*.md'):
        content = md_file.read_text()
        file_rel = str(md_file.relative_to(vault))

        for match in tag_pattern.finditer(content):
            tag = match.group(1)
            tag_counter[tag] += 1

            if tag not in tag_locations:
                tag_locations[tag] = []
            tag_locations[tag].append(file_rel)

    # Create inventory
    inventory = {
        'total_tags': sum(tag_counter.values()),
        'unique_tags': len(tag_counter),
        'tags': []
    }

    for tag, count in tag_counter.most_common():
        inventory['tags'].append({
            'tag': tag,
            'count': count,
            'files': tag_locations[tag][:5]  # Sample files
        })

    # Save
    with open(output_file, 'w') as f:
        json.dump(inventory, f, indent=2)

    print(f"Tag inventory saved to {output_file}")
    print(f"Total tags: {inventory['total_tags']}")
    print(f"Unique tags: {inventory['unique_tags']}")

# Usage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--vault', required=True)
parser.add_argument('--output', default='tag-inventory.json')
args = parser.parse_args()

create_tag_inventory(args.vault, args.output)
```

## Step 3: Design Tag Taxonomy

Create a standard tag taxonomy:

**tag-taxonomy.md**:
```markdown
# Tag Taxonomy

## Top-Level Categories

- `status/*` - Note status
- `type/*` - Content type
- `topic/*` - Subject matter
- `project/*` - Specific projects
- `area/*` - Areas of responsibility

## Standard Tags

### Status
- `status/active`
- `status/archived`
- `status/draft`
- `status/published`

### Type
- `type/article`
- `type/meeting`
- `type/note`
- `type/reference`
- `type/task`

### Topics
- `topic/work`
- `topic/personal`
- `topic/learning`

### Projects
- `project/alpha`
- `project/beta`

### Tasks
- `task/todo`
- `task/doing`
- `task/done`

## Deprecated Tags

These tags should be replaced:

- `todo`, `task`, `action-item` → `task/todo`
- `meeting`, `Meeting` → `type/meeting`
- `project`, `projects` → `project/*` (specific project)
- `work` → `topic/work`
```

## Step 4: Create Normalization Rules

Based on the taxonomy, create normalization rules:

**tag-normalization-rules.json**:
```json
{
  "rules": [
    {
      "pattern": "^todo$",
      "replacement": "task/todo",
      "case_sensitive": false
    },
    {
      "pattern": "^task$",
      "replacement": "task/todo",
      "case_sensitive": false
    },
    {
      "pattern": "^action-item$",
      "replacement": "task/todo",
      "case_sensitive": false
    },
    {
      "pattern": "^meeting$",
      "replacement": "type/meeting",
      "case_sensitive": false
    },
    {
      "pattern": "^Meeting$",
      "replacement": "type/meeting",
      "case_sensitive": false
    },
    {
      "pattern": "^project$",
      "replacement": "project/general",
      "case_sensitive": false
    },
    {
      "pattern": "^projects$",
      "replacement": "project/general",
      "case_sensitive": false
    },
    {
      "pattern": "^work/project$",
      "replacement": "project/work",
      "case_sensitive": false
    },
    {
      "pattern": "^reciepe$",
      "replacement": "topic/recipe",
      "case_sensitive": false
    },
    {
      "pattern": "^recipie$",
      "replacement": "topic/recipe",
      "case_sensitive": false
    },
    {
      "pattern": "^recipe$",
      "replacement": "topic/recipe",
      "case_sensitive": false
    }
  ]
}
```

## Step 5: Preview Normalization

Run in dry-run mode to see what would change:

```bash
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --rules tag-normalization-rules.json \
  --case lower \
  --dry-run \
  --verbose > normalization-preview.txt
```

Review the preview:

```bash
less normalization-preview.txt
```

Look for:
- Unexpected changes
- Tags that shouldn't be changed
- Missing rules

## Step 6: Create Detailed Change Report

Generate a detailed report of what will change:

```bash
python generate_normalization_report.py \
  --vault ~/vault \
  --rules tag-normalization-rules.json \
  --output normalization-report.md
```

**generate_normalization_report.py**:
```python
#!/usr/bin/env python3
import json
import re
from pathlib import Path
from collections import defaultdict

def generate_normalization_report(vault_path, rules_file, output_file):
    # Load rules
    with open(rules_file) as f:
        rules_data = json.load(f)

    rules = []
    for rule in rules_data['rules']:
        pattern = rule['pattern']
        if not rule.get('case_sensitive', False):
            pattern = re.compile(pattern, re.IGNORECASE)
        else:
            pattern = re.compile(pattern)
        rules.append({
            'pattern': pattern,
            'replacement': rule['replacement'],
            'original': rule['pattern']
        })

    vault = Path(vault_path)
    tag_pattern = re.compile(r'(?:^|\s)#([\w/-]+)')

    # Track changes
    changes = defaultdict(lambda: {'old': set(), 'new': None, 'files': set()})

    for md_file in vault.rglob('*.md'):
        content = md_file.read_text()
        file_rel = str(md_file.relative_to(vault))

        for match in tag_pattern.finditer(content):
            tag = match.group(1)

            # Check if tag matches any rule
            for rule in rules:
                if rule['pattern'].match(tag):
                    old_tag = tag
                    new_tag = rule['replacement']

                    changes[new_tag]['old'].add(old_tag)
                    changes[new_tag]['new'] = new_tag
                    changes[new_tag]['files'].add(file_rel)
                    break

    # Generate report
    report = []
    report.append("# Tag Normalization Report\n")
    report.append(f"Total tag consolidations: {len(changes)}\n")
    report.append("\n## Changes\n")

    for new_tag, info in sorted(changes.items()):
        old_tags = ', '.join(f'`#{t}`' for t in sorted(info['old']))
        report.append(f"\n### `#{new_tag}`\n")
        report.append(f"**From**: {old_tags}\n")
        report.append(f"**Files affected**: {len(info['files'])}\n")

        # Show sample files
        sample_files = list(info['files'])[:5]
        report.append("\n**Sample files**:\n")
        for file in sample_files:
            report.append(f"- {file}\n")

    # Summary statistics
    total_old_tags = sum(len(info['old']) for info in changes.values())
    total_files_affected = len(set(
        file for info in changes.values() for file in info['files']
    ))

    report.append(f"\n## Summary\n")
    report.append(f"- Old tags being replaced: {total_old_tags}\n")
    report.append(f"- New standardized tags: {len(changes)}\n")
    report.append(f"- Files affected: {total_files_affected}\n")

    # Write report
    with open(output_file, 'w') as f:
        f.writelines(report)

    print(f"Report generated: {output_file}")

# Usage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--vault', required=True)
parser.add_argument('--rules', required=True)
parser.add_argument('--output', default='normalization-report.md')
args = parser.parse_args()

generate_normalization_report(args.vault, args.rules, args.output)
```

**Sample Report Output**:
```markdown
# Tag Normalization Report

Total tag consolidations: 15

## Changes

### `#task/todo`
**From**: `#todo`, `#task`, `#action-item`
**Files affected**: 487

**Sample files**:
- projects/Project Alpha.md
- meetings/2025-01-15 Meeting.md
- notes/Quick Ideas.md

### `#type/meeting`
**From**: `#meeting`, `#Meeting`, `#MEETING`
**Files affected**: 390

## Summary
- Old tags being replaced: 42
- New standardized tags: 15
- Files affected: 1,234
```

## Step 7: Execute Normalization

After reviewing the report and confirming the changes look good:

```bash
# Backup first!
git add .
git commit -m "Before tag normalization"

# Execute normalization
python batch_processor.py normalize-tags \
  --vault ~/vault \
  --rules tag-normalization-rules.json \
  --case lower \
  --verbose
```

**Expected output**:
```
INFO: Normalizing tags in vault: ~/vault
INFO: Loaded 11 normalization rules
INFO: Found 2,341 markdown files
INFO: Processing notes/Quick Ideas.md
INFO: Processing projects/Project Alpha.md
...
INFO: Processed 2,341 files, modified 1,234
INFO: Tags before: 847, after: 312
```

## Step 8: Handle Frontmatter Tags

The CLI normalizes inline tags, but also update frontmatter:

```bash
python normalize_frontmatter_tags.py \
  --vault ~/vault \
  --rules tag-normalization-rules.json
```

**normalize_frontmatter_tags.py**:
```python
#!/usr/bin/env python3
import json
import re
import yaml
from pathlib import Path

def normalize_frontmatter_tags(vault_path, rules_file):
    # Load rules
    with open(rules_file) as f:
        rules_data = json.load(f)

    # Compile rules
    rules = []
    for rule in rules_data['rules']:
        pattern = rule['pattern']
        flags = 0 if rule.get('case_sensitive', False) else re.IGNORECASE
        rules.append({
            'pattern': re.compile(pattern, flags),
            'replacement': rule['replacement']
        })

    vault = Path(vault_path)
    fm_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL | re.MULTILINE)
    modified = 0

    for md_file in vault.rglob('*.md'):
        content = md_file.read_text()
        match = fm_pattern.match(content)

        if not match:
            continue

        try:
            frontmatter = yaml.safe_load(match.group(1))
            if not frontmatter:
                continue

            # Process tags
            changed = False
            for key in ['tags', 'tag']:
                if key not in frontmatter:
                    continue

                old_tags = frontmatter[key]
                if isinstance(old_tags, str):
                    old_tags = [old_tags]
                elif not isinstance(old_tags, list):
                    continue

                new_tags = []
                for tag in old_tags:
                    tag = str(tag).lstrip('#')
                    # Apply rules
                    for rule in rules:
                        if rule['pattern'].match(tag):
                            tag = rule['replacement']
                            changed = True
                            break
                    new_tags.append(tag)

                if changed:
                    frontmatter[key] = new_tags

            if changed:
                # Reconstruct file
                new_fm = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
                new_content = f"---\n{new_fm}---\n" + content[match.end():]
                md_file.write_text(new_content)
                modified += 1
                print(f"Updated frontmatter: {md_file.relative_to(vault)}")

        except yaml.YAMLError as e:
            print(f"YAML error in {md_file}: {e}")

    print(f"\nTotal files with frontmatter updated: {modified}")

# Usage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--vault', required=True)
parser.add_argument('--rules', required=True)
args = parser.parse_args()

normalize_frontmatter_tags(args.vault, args.rules)
```

## Step 9: Create Tag Index

Generate a tag index for reference:

```bash
python create_tag_index.py \
  --vault ~/vault \
  --output Tags-Index.md
```

**create_tag_index.py**:
```python
#!/usr/bin/env python3
import re
from pathlib import Path
from collections import defaultdict

def create_tag_index(vault_path, output_file):
    vault = Path(vault_path)
    tag_pattern = re.compile(r'(?:^|\s)#([\w/-]+)')

    # Build tag -> files mapping
    tag_files = defaultdict(list)

    for md_file in vault.rglob('*.md'):
        if md_file.name == 'Tags-Index.md':
            continue

        content = md_file.read_text()
        file_rel = md_file.relative_to(vault)
        note_name = md_file.stem

        tags_in_file = set()
        for match in tag_pattern.finditer(content):
            tags_in_file.add(match.group(1))

        for tag in tags_in_file:
            tag_files[tag].append(note_name)

    # Generate index
    lines = []
    lines.append("# Tags Index\n\n")
    lines.append(f"Total unique tags: {len(tag_files)}\n\n")

    # Group by hierarchy
    hierarchy = defaultdict(list)
    for tag in sorted(tag_files.keys()):
        if '/' in tag:
            root = tag.split('/')[0]
            hierarchy[root].append(tag)
        else:
            hierarchy['_root'].append(tag)

    # Write hierarchical index
    for category in sorted(hierarchy.keys()):
        if category == '_root':
            lines.append("## Root Tags\n\n")
        else:
            lines.append(f"## {category}\n\n")

        for tag in sorted(hierarchy[category]):
            notes = tag_files[tag]
            lines.append(f"### #{tag}\n\n")
            lines.append(f"**{len(notes)} notes**\n\n")

            # Show first 10 notes
            for note in sorted(notes)[:10]:
                lines.append(f"- [[{note}]]\n")

            if len(notes) > 10:
                lines.append(f"- ... and {len(notes) - 10} more\n")

            lines.append("\n")

    # Write file
    output_path = vault / output_file
    output_path.write_text(''.join(lines))
    print(f"Tag index created: {output_file}")

# Usage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--vault', required=True)
parser.add_argument('--output', default='Tags-Index.md')
args = parser.parse_args()

create_tag_index(args.vault, args.output)
```

## Step 10: Verification

Verify the normalization was successful:

```bash
# Generate new tag analysis
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report after-normalization.md

# Compare before and after
echo "Before normalization:"
grep "Unique Tags:" tag-analysis.md

echo "After normalization:"
grep "Unique Tags:" after-normalization.md
```

**Expected output**:
```
Before normalization:
- **Unique Tags**: 847

After normalization:
- **Unique Tags**: 312
```

## Step 11: Document Tag Standards

Create a tag usage guide:

**Tag-Standards.md**:
```markdown
# Tag Standards

## Naming Conventions

1. **Use lowercase**: `#project/alpha` not `#Project/Alpha`
2. **Use hierarchies**: `#topic/work/project` not `#work-project`
3. **Be specific**: `#project/alpha` not just `#project`
4. **Avoid redundancy**: `#task/todo` not `#task/todo-task`

## Standard Tag Categories

### Status Tags (`status/*`)
- `#status/active` - Currently active
- `#status/archived` - Archived/completed
- `#status/draft` - Work in progress
- `#status/published` - Published/finalized

### Type Tags (`type/*`)
- `#type/article` - Article or blog post
- `#type/meeting` - Meeting notes
- `#type/note` - General note
- `#type/reference` - Reference material
- `#type/task` - Task or action item

### Topic Tags (`topic/*`)
- `#topic/work` - Work-related
- `#topic/personal` - Personal notes
- `#topic/learning` - Learning materials

### Project Tags (`project/*`)
- Use specific project names: `#project/alpha`
- Avoid generic `#project`

### Task Tags (`task/*`)
- `#task/todo` - To be done
- `#task/doing` - In progress
- `#task/done` - Completed

## Deprecated Tags

Do not use these tags (they will be auto-converted):

- `#todo`, `#task`, `#action-item` → Use `#task/todo`
- `#meeting`, `#Meeting` → Use `#type/meeting`
- `#project` → Use `#project/[name]`
- `#work` → Use `#topic/work`

## Adding New Tags

Before creating a new tag:

1. Check if existing tag can be used
2. Follow naming conventions
3. Update this document
4. Add to tag index
```

## Results

**Before Normalization**:
- 847 unique tags
- Inconsistent case
- Redundant tags
- No hierarchy
- Confusing to navigate

**After Normalization**:
- 312 unique tags (63% reduction)
- Consistent lowercase
- No redundancy
- Clear hierarchy
- Easy to navigate
- Documented standards

## Maintenance

Set up automated tag validation:

```bash
#!/bin/bash
# validate-tags.sh

# Check for tags that don't match standards
python validate_tag_standards.py --vault ~/vault --report tag-violations.md

# If violations found, alert
if [ -s tag-violations.md ]; then
  echo "Tag standard violations found! See tag-violations.md"
fi
```

Run weekly:
```bash
# Add to crontab
0 9 * * 1 /path/to/validate-tags.sh
```

Success! Your tags are now clean, consistent, and maintainable. 🎉
