# Use Case 4: Generate Vault Statistics Report

## Scenario

You want to understand your vault's health, growth, and usage patterns. Generate comprehensive statistics including file counts, link density, tag usage, and health metrics.

## Basic Health Check

Generate a quick health report:

```bash
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report vault-health.md
```

**Sample Output** (`vault-health.md`):
```markdown
# Vault Analysis Report

Generated: 2025-01-20 10:30:00
Vault: /Users/me/Documents/ObsidianVault

## Health Score: 87.5/100

## File Statistics

- **Total Files**: 2,487
- **Markdown Files**: 2,341
- **Attachment Files**: 146
- **Total Size**: 125.34 MB

## Content Statistics

- **Total Words**: 456,789
- **Total Lines**: 89,234
- **Average Note Length**: 195 words

## Link Statistics

- **Total Wikilinks**: 8,456
- **Broken Links**: 12 ⚠️
- **Orphaned Notes**: 23 ⚠️

### Most Linked Notes

- `Projects Overview` (87 backlinks)
- `Tasks Dashboard` (65 backlinks)
- `Index` (54 backlinks)

## Tag Statistics

- **Total Tags**: 12,456
- **Unique Tags**: 312

### Most Used Tags

- `#project/alpha` (234 uses)
- `#type/meeting` (198 uses)
- `#task/todo` (187 uses)

## Frontmatter Statistics

- **Notes with Frontmatter**: 1,987 (85%)

### Common Frontmatter Keys

- `tags` (1,987 notes)
- `created` (1,765 notes)
- `modified` (1,432 notes)

## Recommendations

- 🟡 Fix 12 broken links
- 🟡 Review 23 orphaned notes
- 🟢 Vault is in excellent condition!
```

## Advanced Analytics

For deeper insights, create custom analytics scripts:

### Growth Over Time

Track vault growth:

**vault_growth_tracker.py**:
```python
#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

def analyze_growth(vault_path, output_file):
    vault = Path(vault_path)

    # Group files by creation month
    files_by_month = defaultdict(lambda: {
        'count': 0,
        'total_words': 0,
        'total_size': 0
    })

    for md_file in vault.rglob('*.md'):
        # Get creation time
        ctime = datetime.fromtimestamp(md_file.stat().st_ctime)
        month_key = ctime.strftime('%Y-%m')

        # Count file
        files_by_month[month_key]['count'] += 1

        # Add size
        files_by_month[month_key]['total_size'] += md_file.stat().st_size

        # Count words
        content = md_file.read_text()
        words = len(content.split())
        files_by_month[month_key]['total_words'] += words

    # Convert to list and sort
    growth_data = []
    for month, stats in sorted(files_by_month.items()):
        growth_data.append({
            'month': month,
            'files_created': stats['count'],
            'total_words': stats['total_words'],
            'total_size_mb': round(stats['total_size'] / (1024 * 1024), 2)
        })

    # Calculate cumulative
    cumulative_files = 0
    for entry in growth_data:
        cumulative_files += entry['files_created']
        entry['cumulative_files'] = cumulative_files

    # Save report
    report = {
        'generated': datetime.now().isoformat(),
        'vault_path': str(vault_path),
        'total_months': len(growth_data),
        'growth_by_month': growth_data
    }

    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    # Generate markdown report
    md_report = f"# Vault Growth Report\n\n"
    md_report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    md_report += "## Monthly Growth\n\n"
    md_report += "| Month | Files Created | Cumulative | Words | Size (MB) |\n"
    md_report += "|-------|---------------|------------|-------|------------|\n"

    for entry in growth_data:
        md_report += f"| {entry['month']} | {entry['files_created']} | {entry['cumulative_files']} | {entry['total_words']:,} | {entry['total_size_mb']} |\n"

    md_output = output_file.replace('.json', '.md')
    with open(md_output, 'w') as f:
        f.write(md_report)

    print(f"Growth analysis saved to {output_file} and {md_output}")

# Usage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--vault', required=True)
parser.add_argument('--output', default='vault-growth.json')
args = parser.parse_args()

analyze_growth(args.vault, args.output)
```

```bash
python vault_growth_tracker.py --vault ~/vault
```

### Link Network Analysis

Analyze link network and identify clusters:

**link_network_analyzer.py**:
```python
#!/usr/bin/env python3
import json
import re
from pathlib import Path
from collections import defaultdict

def analyze_link_network(vault_path, output_file):
    vault = Path(vault_path)
    wikilink_pattern = re.compile(r'\[\[([^\]|#]+)')

    # Build graph
    links = defaultdict(set)  # source -> targets
    backlinks = defaultdict(set)  # target -> sources

    note_names = {f.stem for f in vault.rglob('*.md')}

    for md_file in vault.rglob('*.md'):
        source = md_file.stem
        content = md_file.read_text()

        for match in wikilink_pattern.finditer(content):
            target = match.group(1).strip()

            if target in note_names:
                links[source].add(target)
                backlinks[target].add(source)

    # Calculate metrics
    metrics = {
        'total_notes': len(note_names),
        'notes_with_outgoing': len(links),
        'notes_with_incoming': len(backlinks),
        'total_connections': sum(len(targets) for targets in links.values()),
        'avg_outgoing': sum(len(targets) for targets in links.values()) / len(note_names),
        'avg_incoming': sum(len(sources) for sources in backlinks.values()) / len(note_names)
    }

    # Find hubs (notes with many outgoing links)
    hubs = sorted(
        [(note, len(targets)) for note, targets in links.items()],
        key=lambda x: x[1],
        reverse=True
    )[:10]

    # Find authorities (notes with many incoming links)
    authorities = sorted(
        [(note, len(sources)) for note, sources in backlinks.items()],
        key=lambda x: x[1],
        reverse=True
    )[:10]

    # Find isolated notes
    isolated = [
        note for note in note_names
        if note not in links and note not in backlinks
    ]

    # Generate report
    report = {
        'metrics': metrics,
        'top_hubs': [{'note': n, 'outgoing_links': c} for n, c in hubs],
        'top_authorities': [{'note': n, 'backlinks': c} for n, c in authorities],
        'isolated_notes': isolated[:20],
        'total_isolated': len(isolated)
    }

    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    # Generate markdown
    md_report = "# Link Network Analysis\n\n"
    md_report += "## Network Metrics\n\n"
    md_report += f"- Total notes: {metrics['total_notes']:,}\n"
    md_report += f"- Notes with outgoing links: {metrics['notes_with_outgoing']:,}\n"
    md_report += f"- Notes with incoming links: {metrics['notes_with_incoming']:,}\n"
    md_report += f"- Total connections: {metrics['total_connections']:,}\n"
    md_report += f"- Average outgoing links: {metrics['avg_outgoing']:.2f}\n"
    md_report += f"- Average incoming links: {metrics['avg_incoming']:.2f}\n"

    md_report += "\n## Top Hubs (Most Outgoing Links)\n\n"
    for item in report['top_hubs']:
        md_report += f"- `{item['note']}` ({item['outgoing_links']} links)\n"

    md_report += "\n## Top Authorities (Most Backlinks)\n\n"
    for item in report['top_authorities']:
        md_report += f"- `{item['note']}` ({item['backlinks']} backlinks)\n"

    md_report += f"\n## Isolated Notes\n\n"
    md_report += f"Total isolated: {len(isolated)}\n\n"
    for note in isolated[:20]:
        md_report += f"- `{note}`\n"

    md_output = output_file.replace('.json', '.md')
    with open(md_output, 'w') as f:
        f.write(md_report)

    print(f"Network analysis saved to {output_file} and {md_output}")

# Usage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--vault', required=True)
parser.add_argument('--output', default='link-network.json')
args = parser.parse_args()

analyze_link_network(args.vault, args.output)
```

```bash
python link_network_analyzer.py --vault ~/vault
```

### Tag Usage Patterns

Analyze tag usage patterns:

**tag_usage_analyzer.py**:
```python
#!/usr/bin/env python3
import json
import re
from pathlib import Path
from collections import defaultdict, Counter

def analyze_tag_usage(vault_path, output_file):
    vault = Path(vault_path)
    tag_pattern = re.compile(r'(?:^|\s)#([\w/-]+)')

    # Collect tag data
    tag_counter = Counter()
    tag_combinations = Counter()
    tags_by_file = {}

    for md_file in vault.rglob('*.md'):
        content = md_file.read_text()
        file_tags = set()

        for match in tag_pattern.finditer(content):
            tag = match.group(1)
            tag_counter[tag] += 1
            file_tags.add(tag)

        tags_by_file[md_file.stem] = list(file_tags)

        # Track tag combinations
        if len(file_tags) > 1:
            combo = tuple(sorted(file_tags))
            tag_combinations[combo] += 1

    # Analyze hierarchies
    hierarchies = defaultdict(set)
    for tag in tag_counter:
        if '/' in tag:
            parts = tag.split('/')
            for i in range(len(parts)):
                level = '/'.join(parts[:i+1])
                hierarchies[parts[0]].add(level)

    # Most common combinations
    top_combinations = tag_combinations.most_common(10)

    report = {
        'total_tags': sum(tag_counter.values()),
        'unique_tags': len(tag_counter),
        'most_used': [
            {'tag': tag, 'count': count}
            for tag, count in tag_counter.most_common(20)
        ],
        'tag_hierarchies': {
            root: list(tags)
            for root, tags in hierarchies.items()
        },
        'common_combinations': [
            {'tags': list(tags), 'count': count}
            for tags, count in top_combinations
        ]
    }

    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    # Generate markdown
    md_report = "# Tag Usage Analysis\n\n"
    md_report += f"- Total tag uses: {report['total_tags']:,}\n"
    md_report += f"- Unique tags: {report['unique_tags']:,}\n"

    md_report += "\n## Most Used Tags\n\n"
    for item in report['most_used']:
        md_report += f"- `#{item['tag']}` ({item['count']} uses)\n"

    md_report += "\n## Tag Hierarchies\n\n"
    for root, tags in report['tag_hierarchies'].items():
        md_report += f"### {root}\n\n"
        for tag in sorted(tags):
            md_report += f"- `#{tag}`\n"
        md_report += "\n"

    md_report += "\n## Common Tag Combinations\n\n"
    for item in report['common_combinations']:
        tags_str = ', '.join(f'`#{t}`' for t in item['tags'])
        md_report += f"- {tags_str} ({item['count']} notes)\n"

    md_output = output_file.replace('.json', '.md')
    with open(md_output, 'w') as f:
        f.write(md_report)

    print(f"Tag analysis saved to {output_file} and {md_output}")

# Usage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--vault', required=True)
parser.add_argument('--output', default='tag-usage.json')
args = parser.parse_args()

analyze_tag_usage(args.vault, args.output)
```

```bash
python tag_usage_analyzer.py --vault ~/vault
```

## Comprehensive Dashboard

Create a single comprehensive dashboard:

```bash
# Run all analytics
python batch_processor.py analyze-vault \
  --vault ~/vault \
  --report vault-health.md

python vault_growth_tracker.py --vault ~/vault
python link_network_analyzer.py --vault ~/vault
python tag_usage_analyzer.py --vault ~/vault

# Combine into dashboard
python create_vault_dashboard.py --vault ~/vault
```

**create_vault_dashboard.py**:
```python
#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

def create_dashboard(vault_path):
    vault = Path(vault_path)

    # Load all reports
    growth = json.load(open('vault-growth.json'))
    network = json.load(open('link-network.json'))
    tags = json.load(open('tag-usage.json'))

    # Create dashboard
    dashboard = []
    dashboard.append("# Vault Dashboard\n\n")
    dashboard.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

    # Growth section
    dashboard.append("## Growth Summary\n\n")
    latest = growth['growth_by_month'][-1]
    dashboard.append(f"- **Total Notes**: {latest['cumulative_files']:,}\n")
    dashboard.append(f"- **Files This Month**: {latest['files_created']}\n")
    dashboard.append(f"- **Total Words**: {sum(m['total_words'] for m in growth['growth_by_month']):,}\n")

    # Network section
    dashboard.append("\n## Network Summary\n\n")
    dashboard.append(f"- **Total Connections**: {network['metrics']['total_connections']:,}\n")
    dashboard.append(f"- **Average Links**: {network['metrics']['avg_outgoing']:.1f} out, {network['metrics']['avg_incoming']:.1f} in\n")
    dashboard.append(f"- **Isolated Notes**: {network['total_isolated']}\n")

    # Tag section
    dashboard.append("\n## Tag Summary\n\n")
    dashboard.append(f"- **Total Tags**: {tags['total_tags']:,}\n")
    dashboard.append(f"- **Unique Tags**: {tags['unique_tags']}\n")
    dashboard.append(f"- **Tag Hierarchies**: {len(tags['tag_hierarchies'])}\n")

    # Top performers
    dashboard.append("\n## Top Performers\n\n")
    dashboard.append("### Most Connected Notes\n\n")
    for item in network['top_authorities'][:5]:
        dashboard.append(f"- [[{item['note']}]] ({item['backlinks']} backlinks)\n")

    dashboard.append("\n### Most Used Tags\n\n")
    for item in tags['most_used'][:5]:
        dashboard.append(f"- `#{item['tag']}` ({item['count']} uses)\n")

    # Recent activity
    dashboard.append("\n## Recent Activity\n\n")
    dashboard.append("### Last 3 Months\n\n")
    dashboard.append("| Month | Files Created | Total Words |\n")
    dashboard.append("|-------|---------------|-------------|\n")
    for month_data in growth['growth_by_month'][-3:]:
        dashboard.append(f"| {month_data['month']} | {month_data['files_created']} | {month_data['total_words']:,} |\n")

    # Quick links
    dashboard.append("\n## Quick Links\n\n")
    dashboard.append("- [[Tags-Index]] - Complete tag index\n")
    dashboard.append("- [Growth Details](vault-growth.md)\n")
    dashboard.append("- [Network Analysis](link-network.md)\n")
    dashboard.append("- [Tag Analysis](tag-usage.md)\n")
    dashboard.append("- [Health Report](vault-health.md)\n")

    # Write dashboard
    output_path = vault / 'Vault-Dashboard.md'
    output_path.write_text(''.join(dashboard))
    print(f"Dashboard created: Vault-Dashboard.md")

# Usage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--vault', required=True)
args = parser.parse_args()

create_dashboard(args.vault)
```

## Automated Reporting

Set up automated weekly reports:

**weekly_report.sh**:
```bash
#!/bin/bash

VAULT="$HOME/vault"
REPORT_DIR="$HOME/vault-reports"
DATE=$(date +%Y-%m-%d)

# Create report directory
mkdir -p "$REPORT_DIR"

# Run all analytics
python batch_processor.py analyze-vault \
  --vault "$VAULT" \
  --report "$REPORT_DIR/health-$DATE.md"

python vault_growth_tracker.py --vault "$VAULT" \
  --output "$REPORT_DIR/growth-$DATE.json"

python link_network_analyzer.py --vault "$VAULT" \
  --output "$REPORT_DIR/network-$DATE.json"

python tag_usage_analyzer.py --vault "$VAULT" \
  --output "$REPORT_DIR/tags-$DATE.json"

# Create dashboard
python create_vault_dashboard.py --vault "$VAULT"

# Copy dashboard to reports
cp "$VAULT/Vault-Dashboard.md" "$REPORT_DIR/dashboard-$DATE.md"

echo "Weekly report generated: $REPORT_DIR/dashboard-$DATE.md"
```

Add to crontab:
```bash
# Run every Monday at 9 AM
0 9 * * 1 /path/to/weekly_report.sh
```

## Sample Dashboard Output

**Vault-Dashboard.md**:
```markdown
# Vault Dashboard

Generated: 2025-01-20 09:00

## Growth Summary

- **Total Notes**: 2,341
- **Files This Month**: 87
- **Total Words**: 456,789

## Network Summary

- **Total Connections**: 8,456
- **Average Links**: 3.6 out, 3.6 in
- **Isolated Notes**: 23

## Tag Summary

- **Total Tags**: 12,456
- **Unique Tags**: 312
- **Tag Hierarchies**: 8

## Top Performers

### Most Connected Notes

- [[Projects Overview]] (87 backlinks)
- [[Tasks Dashboard]] (65 backlinks)
- [[Index]] (54 backlinks)

### Most Used Tags

- `#project/alpha` (234 uses)
- `#type/meeting` (198 uses)
- `#task/todo` (187 uses)

## Recent Activity

### Last 3 Months

| Month | Files Created | Total Words |
|-------|---------------|-------------|
| 2024-11 | 92 | 18,234 |
| 2024-12 | 108 | 21,567 |
| 2025-01 | 87 | 17,234 |

## Quick Links

- [[Tags-Index]] - Complete tag index
- [Growth Details](vault-growth.md)
- [Network Analysis](link-network.md)
- [Tag Analysis](tag-usage.md)
- [Health Report](vault-health.md)
```

Success! You now have comprehensive vault statistics and analytics. 📊
