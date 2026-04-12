#!/usr/bin/env python3
"""
Create Obsidian vault from Claude documentation.
Converts llms.md links and llms-full.md content into interconnected Obsidian notes.
"""

import re
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from urllib.parse import urlparse
import json

class ObsidianVaultCreator:
    def __init__(self, llms_file: str, llms_full_file: str, output_dir: str):
        self.llms_file = llms_file
        self.llms_full_file = llms_full_file
        self.output_dir = Path(output_dir)
        self.pages: List[Dict] = []
        self.content_sections: Dict[str, str] = {}
        self.categories: Dict[str, List[Dict]] = {}

    def parse_llms_md(self):
        """Parse llms.md to extract all page links and metadata."""
        with open(self.llms_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract links with format: - [Title](URL): Description
        # or - [Title](URL)
        pattern = r'^- \[([^\]]+)\]\((https://docs\.claude\.com/en/([^\)]+)\.md)\)(?:: (.+))?$'

        for match in re.finditer(pattern, content, re.MULTILINE):
            title = match.group(1)
            url = match.group(2)
            path = match.group(3)  # The path without https://docs.claude.com/en/
            description = match.group(4) if match.group(4) else ""

            # Extract category from path
            parts = path.split('/')
            category = parts[0] if len(parts) > 1 else 'general'

            page = {
                'title': title,
                'url': url,
                'path': path,
                'description': description,
                'category': category,
                'subcategory': parts[1] if len(parts) > 2 else None,
                'filename': parts[-1],
                'folder_path': '/'.join(parts[:-1]) if len(parts) > 1 else ''
            }

            self.pages.append(page)

            # Group by category
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(page)

        print(f"✓ Parsed {len(self.pages)} pages from llms.md")
        print(f"✓ Found {len(self.categories)} categories: {', '.join(self.categories.keys())}")

    def parse_llms_full_md(self):
        """Parse llms-full.md to extract content for each page."""
        with open(self.llms_full_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by Source: markers
        # Format: # Title\nSource: URL\n\nContent...
        pattern = r'^# (.+?)\nSource: (https://docs\.claude\.com/en/([^\n]+))\n\n(.*?)(?=^# |\Z)'

        for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
            title = match.group(1).strip()
            url = match.group(2).strip()
            path = match.group(3).strip()
            section_content = match.group(4).strip()

            # Store content by URL
            self.content_sections[url] = {
                'title': title,
                'content': section_content
            }

        print(f"✓ Extracted {len(self.content_sections)} content sections from llms-full.md")

    def create_frontmatter(self, page: Dict, related_pages: List[str]) -> str:
        """Generate YAML frontmatter for a page."""
        today = datetime.now().strftime('%Y-%m-%d')

        # Create tags from category and subcategory
        tags = [page['category']]
        if page['subcategory']:
            tags.append(page['subcategory'])
        if 'api' in page['path'].lower():
            tags.append('api')
        if 'sdk' in page['path'].lower():
            tags.append('sdk')
        if 'claude-code' in page['path'].lower():
            tags.append('claude-code')

        # Create aliases
        aliases = [page['title']]

        frontmatter = f"""---
created: {today}
modified: {today}
title: {page['title']}
url: {page['url']}
category: {page['category']}"""

        if page['subcategory']:
            frontmatter += f"\nsubcategory: {page['subcategory']}"

        if page['description']:
            # Escape quotes in description
            desc = page['description'].replace('"', '\\"')
            frontmatter += f'\ndescription: "{desc}"'

        frontmatter += f"\ntags:\n"
        for tag in tags:
            frontmatter += f"  - {tag}\n"

        if related_pages:
            frontmatter += "related:\n"
            for rel in related_pages[:5]:  # Limit to 5 related
                frontmatter += f"  - '[[{rel}]]'\n"

        frontmatter += "---\n"
        return frontmatter

    def find_related_pages(self, page: Dict) -> List[str]:
        """Find related pages based on category, subcategory, and content."""
        related = []

        # Same subcategory
        for p in self.pages:
            if p != page and p['subcategory'] == page['subcategory'] and page['subcategory']:
                related.append(p['title'])

        # Same category if not many in subcategory
        if len(related) < 3:
            for p in self.pages:
                if p != page and p['category'] == page['category'] and p['title'] not in related:
                    related.append(p['title'])
                    if len(related) >= 5:
                        break

        return related

    def convert_content_to_obsidian(self, content: str, page: Dict) -> str:
        """Convert content to Obsidian format with wikilinks."""

        # Convert HTTP links to other Claude docs to wikilinks
        for other_page in self.pages:
            if other_page['title'] == page['title']:
                continue

            # Match [Text](url) format
            url_pattern = re.escape(other_page['url'])
            content = re.sub(
                rf'\[([^\]]+)\]\({url_pattern}\)',
                r'[[\1]]',
                content
            )

            # Also try to match just mentions of the title
            # Be careful not to replace within code blocks or URLs
            title_pattern = re.escape(other_page['title'])
            # Only replace if not in code block (between ` or ```) and not in URL
            content = re.sub(
                rf'(?<!`|\[)({title_pattern})(?!`|\]|\()',
                r'[[\1]]',
                content
            )

        # Convert callout-style sections
        # Convert <Tip> to Obsidian callout
        content = re.sub(
            r'<Tip>(.*?)</Tip>',
            r'> [!tip]\n> \1',
            content,
            flags=re.DOTALL
        )

        # Convert <Check> to Obsidian callout
        content = re.sub(
            r'<Check>(.*?)</Check>',
            r'> [!check]\n> \1',
            content,
            flags=re.DOTALL
        )

        # Convert <Warning> to Obsidian callout
        content = re.sub(
            r'<Warning>(.*?)</Warning>',
            r'> [!warning]\n> \1',
            content,
            flags=re.DOTALL
        )

        # Convert <Note> to Obsidian callout
        content = re.sub(
            r'<Note>(.*?)</Note>',
            r'> [!note]\n> \1',
            content,
            flags=re.DOTALL
        )

        return content

    def create_note(self, page: Dict):
        """Create an Obsidian note for a page."""
        # Get content from parsed sections
        content_data = self.content_sections.get(page['url'])

        if not content_data:
            print(f"⚠ No content found for {page['title']} ({page['url']})")
            return

        # Find related pages
        related_pages = self.find_related_pages(page)

        # Create frontmatter
        frontmatter = self.create_frontmatter(page, related_pages)

        # Convert content to Obsidian format
        content = self.convert_content_to_obsidian(content_data['content'], page)

        # Add source reference at bottom
        content += f"\n\n---\n\n**Source:** [Official Documentation]({page['url']})\n"

        # Combine everything
        full_content = frontmatter + "\n# " + page['title'] + "\n\n" + content

        # Create directory structure
        note_dir = self.output_dir / page['folder_path']
        note_dir.mkdir(parents=True, exist_ok=True)

        # Create file
        note_path = note_dir / f"{page['filename']}.md"
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(full_content)

        print(f"  ✓ Created {page['folder_path']}/{page['filename']}.md")

    def create_moc(self, category: str, pages: List[Dict]):
        """Create a Map of Content (MOC) for a category."""
        today = datetime.now().strftime('%Y-%m-%d')

        # Group pages by subcategory
        subcategories: Dict[str, List[Dict]] = {}
        for page in pages:
            subcat = page['subcategory'] or 'general'
            if subcat not in subcategories:
                subcategories[subcat] = []
            subcategories[subcat].append(page)

        # Create frontmatter
        frontmatter = f"""---
created: {today}
modified: {today}
type: moc
category: {category}
tags:
  - moc
  - {category}
  - index
---

"""

        # Create MOC content
        content = f"# {category.replace('-', ' ').title()} - Index\n\n"
        content += f"> [!abstract] Overview\n"
        content += f"> This is the main index for all **{category}** documentation.\n"
        content += f"> Contains {len(pages)} pages across {len(subcategories)} sections.\n\n"

        # Add table of contents by subcategory
        for subcat in sorted(subcategories.keys()):
            subcat_pages = subcategories[subcat]
            content += f"## {subcat.replace('-', ' ').title()}\n\n"

            for page in sorted(subcat_pages, key=lambda p: p['title']):
                content += f"- [[{page['title']}]]"
                if page['description']:
                    content += f" - {page['description']}"
                content += "\n"
            content += "\n"

        # Add dataview query
        content += f"## All {category} Pages\n\n"
        content += f"```dataview\n"
        content += f"TABLE description AS Description, subcategory AS Section\n"
        content += f"FROM #{category}\n"
        content += f"WHERE type != \"moc\"\n"
        content += f"SORT file.name ASC\n"
        content += f"```\n\n"

        # Create the MOC file
        moc_path = self.output_dir / category / f"_{category}-index.md"
        moc_path.parent.mkdir(parents=True, exist_ok=True)

        with open(moc_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)

        print(f"  ✓ Created MOC: {category}/_{ category}-index.md")

    def create_main_index(self):
        """Create the main vault index."""
        today = datetime.now().strftime('%Y-%m-%d')

        frontmatter = f"""---
created: {today}
modified: {today}
type: moc
tags:
  - index
  - moc
  - claude
aliases:
  - Home
  - Index
---

"""

        content = """# Claude Documentation - Obsidian Vault

> [!info] Welcome
> This is a comprehensive Obsidian vault containing the complete English documentation for Claude, Claude Code, and related APIs.
>
> **Total Pages:** {total_pages}
> **Categories:** {total_categories}
> **Last Updated:** {today}

## 📚 Main Categories

"""

        content = content.format(
            total_pages=len(self.pages),
            total_categories=len(self.categories),
            today=today
        )

        # Add links to category MOCs
        for category in sorted(self.categories.keys()):
            page_count = len(self.categories[category])
            cat_title = category.replace('-', ' ').title()
            content += f"### [[_{category}-index|{cat_title}]]\n\n"
            content += f"{page_count} pages covering {cat_title} documentation.\n\n"

        # Add recent pages dataview
        content += """## 📊 Statistics

```dataview
TABLE length(rows) as "Pages"
FROM ""
WHERE type != "moc"
GROUP BY category
SORT length(rows) DESC
```

## 🔍 Search by Tag

```dataview
TABLE length(rows.file.name) as Count
FROM ""
GROUP BY file.tags
SORT length(rows.file.name) DESC
LIMIT 10
```

## 🗺️ Graph View

This vault is designed for exploration through Obsidian's Graph View. Key navigation points:

- Category indices are prefixed with `_` (e.g., `_api-index`)
- Related documents are linked in frontmatter
- Cross-references use wikilinks throughout

---

**About this vault:** Generated from official Claude documentation at docs.claude.com
"""

        index_path = self.output_dir / "README.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)

        print(f"✓ Created main index: README.md")

    def create_obsidian_config(self):
        """Create .obsidian folder with basic configuration."""
        obsidian_dir = self.output_dir / ".obsidian"
        obsidian_dir.mkdir(exist_ok=True)

        # Create app.json
        app_config = {
            "alwaysUpdateLinks": True,
            "newLinkFormat": "relative",
            "useMarkdownLinks": False,
            "showUnsupportedFiles": False,
            "attachmentFolderPath": "assets",
            "defaultViewMode": "source",
            "readableLineLength": True,
            "showFrontmatter": True
        }

        with open(obsidian_dir / "app.json", 'w') as f:
            json.dump(app_config, f, indent=2)

        # Create appearance.json
        appearance_config = {
            "baseFontSize": 16,
            "theme": "obsidian"
        }

        with open(obsidian_dir / "appearance.json", 'w') as f:
            json.dump(appearance_config, f, indent=2)

        print(f"✓ Created .obsidian configuration")

    def build(self):
        """Main build process."""
        print("\n🚀 Building Obsidian vault from Claude documentation...\n")

        # Parse source files
        print("📖 Step 1: Parsing source files...")
        self.parse_llms_md()
        self.parse_llms_full_md()

        # Create output directory
        print(f"\n📁 Step 2: Creating vault structure at {self.output_dir}...")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create Obsidian config
        print("\n⚙️  Step 3: Creating Obsidian configuration...")
        self.create_obsidian_config()

        # Create all notes
        print(f"\n📝 Step 4: Creating {len(self.pages)} notes...")
        for page in self.pages:
            self.create_note(page)

        # Create MOCs
        print(f"\n🗂️  Step 5: Creating {len(self.categories)} category indices...")
        for category, pages in self.categories.items():
            self.create_moc(category, pages)

        # Create main index
        print("\n🏠 Step 6: Creating main index...")
        self.create_main_index()

        print(f"\n✅ Vault creation complete!")
        print(f"📍 Location: {self.output_dir.absolute()}")
        print(f"📊 Stats: {len(self.pages)} pages, {len(self.categories)} categories")
        print(f"\n💡 Open this folder in Obsidian to explore the vault!")


if __name__ == '__main__':
    creator = ObsidianVaultCreator(
        llms_file='llms.md',
        llms_full_file='llms-full.md',
        output_dir='claude-docs-vault'
    )
    creator.build()
