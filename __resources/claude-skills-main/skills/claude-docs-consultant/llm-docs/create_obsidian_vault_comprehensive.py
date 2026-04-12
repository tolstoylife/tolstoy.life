#!/usr/bin/env python3
"""
Create Obsidian vault from Claude documentation.
Comprehensive conversion with proper XML→MD transformation and code fencing.
"""

import re
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import json

class ObsidianVaultCreator:
    def __init__(self, llms_file: str, llms_full_file: str, output_dir: str):
        self.llms_file = llms_file
        self.llms_full_file = llms_full_file
        self.output_dir = Path(output_dir)
        self.pages: List[Dict] = []
        self.content_sections: Dict[str, str] = {}
        self.categories: Dict[str, List[Dict]] = {}
        self.filename_to_page: Dict[str, Dict] = {}

    def normalize_url(self, url: str) -> str:
        """Normalize URL by removing .md extension if present."""
        return url.rstrip('.md')

    def parse_llms_md(self):
        """Parse llms.md to extract all page links and metadata."""
        with open(self.llms_file, 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = r'^- \[([^\]]+)\]\((https://docs\.claude\.com/en/([^\)]+?)(?:\.md)?)\)(?:: (.+))?$'

        for match in re.finditer(pattern, content, re.MULTILINE):
            title = match.group(1)
            url = self.normalize_url(match.group(2))
            path = match.group(3)
            description = match.group(4) if match.group(4) else ""

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
            self.filename_to_page[page['filename']] = page

            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(page)

        print(f"✓ Parsed {len(self.pages)} pages from llms.md")
        print(f"✓ Found {len(self.categories)} categories")

    def parse_llms_full_md(self):
        """Parse llms-full.md to extract content for each page."""
        with open(self.llms_full_file, 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = r'^# (.+?)\nSource: (https://docs\.claude\.com/en/([^\n]+))\n\n(.*?)(?=^# |\Z)'

        for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
            title = match.group(1).strip()
            url = self.normalize_url(match.group(2).strip())
            section_content = match.group(4).strip()

            self.content_sections[url] = {
                'title': title,
                'content': section_content
            }

        print(f"✓ Extracted {len(self.content_sections)} content sections")

    def create_frontmatter(self, page: Dict, related_pages: List[str]) -> str:
        """Generate YAML frontmatter."""
        today = datetime.now().strftime('%Y-%m-%d')

        tags = [page['category']]
        if page['subcategory']:
            tags.append(page['subcategory'])
        
        # Add contextual tags
        for keyword in ['api', 'sdk', 'claude-code', 'agent', 'tool']:
            if keyword in page['path'].lower() and keyword not in tags:
                tags.append(keyword)

        frontmatter = f"""---
created: {today}
modified: {today}
title: "{page['title']}"
url: {page['url']}
category: {page['category']}"""

        if page['subcategory']:
            frontmatter += f"\nsubcategory: {page['subcategory']}"

        if page['description']:
            desc = page['description'].replace('"', '\\"')
            frontmatter += f'\ndescription: "{desc}"'

        frontmatter += "\ntags:\n"
        for tag in tags:
            frontmatter += f"  - {tag}\n"

        if related_pages:
            frontmatter += "related:\n"
            for rel in related_pages[:5]:
                frontmatter += f"  - '[[{rel}]]'\n"

        frontmatter += "---\n"
        return frontmatter

    def find_related_pages(self, page: Dict) -> List[str]:
        """Find related pages - returns filenames."""
        related = []

        # Same subcategory
        for p in self.pages:
            if p != page and p['subcategory'] == page['subcategory'] and page['subcategory']:
                related.append(p['filename'])

        # Same category
        if len(related) < 3:
            for p in self.pages:
                if p != page and p['category'] == page['category'] and p['filename'] not in related:
                    related.append(p['filename'])
                    if len(related) >= 5:
                        break

        return related

    def convert_xml_to_markdown(self, content: str) -> str:
        """Convert XML-style components to Markdown."""
        
        # Handle <Tabs> and <Tab> - convert to simple sections
        # Remove <Tabs> wrapper
        content = re.sub(r'<Tabs>\s*\n', '', content)
        content = re.sub(r'\n\s*</Tabs>', '', content)
        
        # Convert <Tab title="..."> to subheading
        content = re.sub(
            r'<Tab title="([^"]+)">\s*\n',
            r'**\1**\n\n',
            content
        )
        content = re.sub(r'\n\s*</Tab>', '\n', content)
        
        # Handle <CardGroup> and <Card>
        content = re.sub(r'<CardGroup[^>]*>\s*\n', '', content)
        content = re.sub(r'\n\s*</CardGroup>', '', content)
        
        # Convert <Card> to note callout
        def card_to_callout(match):
            attrs = match.group(1)
            card_content = match.group(2)
            
            # Extract title if present
            title_match = re.search(r'title="([^"]+)"', attrs)
            title = title_match.group(1) if title_match else "Info"
            
            # Format as callout
            lines = card_content.strip().split('\n')
            callout_lines = [f"> [!info] {title}"]
            for line in lines:
                callout_lines.append(f"> {line}" if line.strip() else ">")
            
            return '\n'.join(callout_lines)
        
        content = re.sub(
            r'<Card([^>]*)>(.*?)</Card>',
            card_to_callout,
            content,
            flags=re.DOTALL
        )
        
        # Handle other common XML tags
        xml_tags = {
            'Tip': 'tip',
            'Warning': 'warning',
            'Note': 'note',
            'Check': 'success',
            'Info': 'info',
            'Danger': 'danger',
            'Error': 'danger'
        }
        
        for xml_tag, md_type in xml_tags.items():
            content = re.sub(
                rf'<{xml_tag}>(.*?)</{xml_tag}>',
                lambda m: self._to_callout(md_type, m.group(1)),
                content,
                flags=re.DOTALL | re.IGNORECASE
            )
        
        return content
    
    def _to_callout(self, callout_type: str, content: str) -> str:
        """Convert content to Obsidian callout."""
        lines = content.strip().split('\n')
        result = [f"> [!{callout_type}]"]
        for line in lines:
            result.append(f"> {line}" if line.strip() else ">")
        return '\n'.join(result)

    def fence_loose_code(self, content: str) -> str:
        """Fence code-like content that's not already in code blocks."""
        
        # Detect JSX/JavaScript exports
        def fence_export_const(match):
            code = match.group(0)
            return f"\n```javascript\n{code}\n```\n"
        
        # Only fence if not already in a code block
        content = re.sub(
            r'^(export const .+?^};)$',
            fence_export_const,
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        return content

    def convert_content_to_obsidian(self, content: str, page: Dict) -> str:
        """Convert content to Obsidian format with wikilinks and proper MD."""
        
        # Step 1: Convert XML-style components to Markdown
        content = self.convert_xml_to_markdown(content)
        
        # Step 2: Fence loose code blocks
        content = self.fence_loose_code(content)
        
        # Step 3: Convert HTTP links to wikilinks
        for other_page in self.pages:
            if other_page['title'] == page['title']:
                continue

            url_pattern = re.escape(other_page['url'])
            
            # Replace [Text](URL) with [[filename|Text]]
            content = re.sub(
                rf'\[([^\]]+)\]\({url_pattern}(?:\.md)?\)',
                rf'[[{other_page["filename"]}|\1]]',
                content
            )
        
        # Step 4: Convert /en/path style links to wikilinks
        for other_page in self.pages:
            # Match /en/path/to/doc style references
            path_pattern = re.escape(f'/en/{other_page["path"]}')
            content = re.sub(
                rf'\[([^\]]+)\]\({path_pattern}(?:\.md)?\)',
                rf'[[{other_page["filename"]}|\1]]',
                content
            )
        
        return content

    def create_note(self, page: Dict):
        """Create an Obsidian note for a page."""
        content_data = self.content_sections.get(page['url'])

        if not content_data:
            print(f"⚠ No content for {page['title']}")
            return

        related_pages = self.find_related_pages(page)
        frontmatter = self.create_frontmatter(page, related_pages)
        content = self.convert_content_to_obsidian(content_data['content'], page)

        # Add source reference
        content += f"\n\n---\n\n**Source:** [Official Documentation]({page['url']})\n"

        # Combine
        full_content = frontmatter + "\n# " + page['title'] + "\n\n" + content

        # Create directory and file
        note_dir = self.output_dir / page['folder_path']
        note_dir.mkdir(parents=True, exist_ok=True)
        
        note_path = note_dir / f"{page['filename']}.md"
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(full_content)

        print(f"  ✓ {page['folder_path']}/{page['filename']}.md")

    def create_moc(self, category: str, pages: List[Dict]):
        """Create MOC for category."""
        today = datetime.now().strftime('%Y-%m-%d')

        subcategories: Dict[str, List[Dict]] = {}
        for page in pages:
            subcat = page['subcategory'] or 'general'
            if subcat not in subcategories:
                subcategories[subcat] = []
            subcategories[subcat].append(page)

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

        content = f"# {category.replace('-', ' ').title()} - Index\n\n"
        content += f"> [!abstract] Overview\n"
        content += f"> This is the main index for all **{category}** documentation.\n"
        content += f"> Contains {len(pages)} pages across {len(subcategories)} sections.\n\n"

        for subcat in sorted(subcategories.keys()):
            subcat_pages = subcategories[subcat]
            content += f"## {subcat.replace('-', ' ').title()}\n\n"

            for page in sorted(subcat_pages, key=lambda p: p['title']):
                content += f"- [[{page['filename']}|{page['title']}]]"
                if page['description']:
                    content += f" - {page['description']}"
                content += "\n"
            content += "\n"

        content += f"## All {category} Pages\n\n"
        content += f"```dataview\n"
        content += f"TABLE description AS Description, subcategory AS Section\n"
        content += f"FROM #{category}\n"
        content += f"WHERE type != \"moc\"\n"
        content += f"SORT file.name ASC\n"
        content += f"```\n\n"

        moc_path = self.output_dir / category / f"_{category}-index.md"
        moc_path.parent.mkdir(parents=True, exist_ok=True)

        with open(moc_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)

        print(f"  ✓ {category}/_{category}-index.md")

    def create_main_index(self):
        """Create main vault index."""
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

        content = f"""# Claude Documentation - Obsidian Vault

> [!info] Welcome
> Complete English documentation for Claude, Claude Code, and APIs.
>
> **Total Pages:** {len(self.pages)}
> **Categories:** {len(self.categories)}
> **Last Updated:** {today}

## Main Categories

"""

        for category in sorted(self.categories.keys()):
            page_count = len(self.categories[category])
            cat_title = category.replace('-', ' ').title()
            content += f"### [[_{category}-index|{cat_title}]]\n\n"
            content += f"{page_count} pages covering {cat_title} documentation.\n\n"

        content += """## Statistics

```dataview
TABLE length(rows) as "Pages"
FROM ""
WHERE type != "moc"
GROUP BY category
SORT length(rows) DESC
```

## Search by Tag

```dataview
TABLE length(rows.file.name) as Count
FROM ""
GROUP BY file.tags
SORT length(rows.file.name) DESC
LIMIT 10
```

---

**About:** Generated from official Claude documentation
"""

        index_path = self.output_dir / "README.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)

        print(f"✓ README.md")

    def create_obsidian_config(self):
        """Create .obsidian configuration."""
        obsidian_dir = self.output_dir / ".obsidian"
        obsidian_dir.mkdir(exist_ok=True)

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

        print(f"✓ .obsidian config")

    def build(self):
        """Main build process."""
        print("\n🚀 Building Obsidian vault...\n")

        print("📖 Parsing source files...")
        self.parse_llms_md()
        self.parse_llms_full_md()

        print(f"\n📁 Creating vault at {self.output_dir}...")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        print("\n⚙️  Creating Obsidian config...")
        self.create_obsidian_config()

        print(f"\n📝 Creating {len(self.pages)} notes...")
        success = 0
        for page in self.pages:
            self.create_note(page)
            if page['url'] in self.content_sections:
                success += 1

        print(f"\n🗂️  Creating {len(self.categories)} indices...")
        for category, pages in self.categories.items():
            self.create_moc(category, pages)

        print("\n🏠 Creating main index...")
        self.create_main_index()

        print(f"\n✅ Complete!")
        print(f"📍 {self.output_dir.absolute()}")
        print(f"📊 {success}/{len(self.pages)} pages, {len(self.categories)} categories\n")


if __name__ == '__main__':
    creator = ObsidianVaultCreator(
        llms_file='llms.md',
        llms_full_file='llms-full.md',
        output_dir='claude-docs-vault'
    )
    creator.build()
