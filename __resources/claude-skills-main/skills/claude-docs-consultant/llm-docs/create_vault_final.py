#!/usr/bin/env python3
"""
Create Obsidian vault from Claude documentation - Final comprehensive version.
Handles all XML→MD conversions, proper code fencing, and wikilink resolution.
"""

import re
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
        return url.rstrip('.md')

    def parse_llms_md(self):
        with open(self.llms_file, 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = r'^- \[([^\]]+)\]\((https://docs\.claude\.com/en/([^\)]+?)(?:\.md)?)\)(?:: (.+))?$'

        for match in re.finditer(pattern, content, re.MULTILINE):
            title = match.group(1)
            url = self.normalize_url(match.group(2))
            path = match.group(3)
            description = match.group(4) or ""

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

    def parse_llms_full_md(self):
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

        print(f"✓ Extracted {len(self.content_sections)} sections")

    def convert_xml_to_markdown(self, content: str) -> str:
        """Comprehensive XML to Markdown conversion."""

        # Handle <CodeGroup> - just remove wrapper, keep code blocks
        content = re.sub(r'<CodeGroup[^>]*>\s*', '', content)
        content = re.sub(r'\s*</CodeGroup>', '', content)

        # Handle <Steps> and <Step>
        # Convert each <Steps>...</Steps> block independently to reset numbering
        def convert_steps_block(match):
            steps_content = match.group(1)
            step_counter = [1]

            def step_to_markdown(step_match):
                attrs = step_match.group(1)
                step_content = step_match.group(2)

                title_match = re.search(r'title="([^"]+)"', attrs)
                title = title_match.group(1) if title_match else f"Step {step_counter[0]}"

                result = f"\n**Step {step_counter[0]}: {title}**\n\n{step_content.strip()}\n"
                step_counter[0] += 1
                return result

            return re.sub(r'<Step([^>]*)>(.*?)</Step>', step_to_markdown, steps_content, flags=re.DOTALL)

        content = re.sub(r'<Steps>(.*?)</Steps>', convert_steps_block, content, flags=re.DOTALL)

        # Handle <Accordion> and <AccordionGroup>
        content = re.sub(r'<AccordionGroup[^>]*>\s*', '', content)
        content = re.sub(r'\s*</AccordionGroup>', '', content)

        def accordion_to_callout(match):
            attrs = match.group(1)
            acc_content = match.group(2)

            title_match = re.search(r'title="([^"]+)"', attrs)
            title = title_match.group(1) if title_match else "Details"

            lines = acc_content.strip().split('\n')
            result = [f"> [!info]- {title}"]
            for line in lines:
                result.append(f"> {line}" if line.strip() else ">")

            return '\n'.join(result)

        content = re.sub(r'<Accordion([^>]*)>(.*?)</Accordion>', accordion_to_callout, content, flags=re.DOTALL)

        # Handle <Tabs> and <Tab>
        content = re.sub(r'<Tabs>\s*', '\n', content)
        content = re.sub(r'\s*</Tabs>', '\n', content)

        def tab_to_section(match):
            attrs = match.group(1)
            tab_content = match.group(2)

            title_match = re.search(r'title="([^"]+)"', attrs)
            title = title_match.group(1) if title_match else "Tab"

            return f"\n**{title}**\n\n{tab_content.strip()}\n"

        content = re.sub(r'<Tab([^>]*)>(.*?)</Tab>', tab_to_section, content, flags=re.DOTALL)

        # Handle <CardGroup> and <Card>
        content = re.sub(r'<CardGroup[^>]*>\s*', '\n', content)
        content = re.sub(r'\s*</CardGroup>', '\n', content)

        def card_to_callout(match):
            attrs = match.group(1)
            card_content = match.group(2)

            title_match = re.search(r'title="([^"]+)"', attrs)
            title = title_match.group(1) if title_match else "Card"

            # Check for icon
            icon_match = re.search(r'icon="([^"]+)"', attrs)
            callout_type = "info"
            if icon_match:
                icon = icon_match.group(1)
                if "check" in icon or "success" in icon:
                    callout_type = "success"
                elif "warn" in icon:
                    callout_type = "warning"
                elif "error" in icon or "danger" in icon:
                    callout_type = "danger"

            lines = card_content.strip().split('\n')
            result = [f"> [!{callout_type}] {title}"]
            for line in lines:
                result.append(f"> {line}" if line.strip() else ">")

            return '\n'.join(result)

        content = re.sub(r'<Card([^>]*)>(.*?)</Card>', card_to_callout, content, flags=re.DOTALL)

        # Handle <Code> tags - convert to inline code or code blocks
        def code_to_markdown(match):
            code_content = match.group(1).strip()
            # If multiline, use code block
            if '\n' in code_content:
                return f"\n```\n{code_content}\n```\n"
            else:
                return f"`{code_content}`"

        content = re.sub(r'<Code>(.*?)</Code>', code_to_markdown, content, flags=re.DOTALL)

        # Handle <Frame> - convert to info callout
        def frame_to_callout(match):
            frame_content = match.group(1)
            lines = frame_content.strip().split('\n')
            result = ["> [!example]"]
            for line in lines:
                result.append(f"> {line}" if line.strip() else ">")
            return '\n'.join(result)

        content = re.sub(r'<Frame>(.*?)</Frame>', frame_to_callout, content, flags=re.DOTALL)

        # Handle standard callout tags
        xml_tags = {
            'Tip': 'tip',
            'Warning': 'warning',
            'Note': 'note',
            'Check': 'success',
            'Info': 'info',
            'Danger': 'danger',
            'Error': 'danger',
            'Success': 'success'
        }

        for xml_tag, md_type in xml_tags.items():
            def tag_to_callout(match):
                tag_content = match.group(1)
                lines = tag_content.strip().split('\n')
                result = [f"> [!{md_type}]"]
                for line in lines:
                    result.append(f"> {line}" if line.strip() else ">")
                return '\n'.join(result)

            content = re.sub(rf'<{xml_tag}>(.*?)</{xml_tag}>', tag_to_callout, content, flags=re.DOTALL | re.IGNORECASE)

        return content

    def convert_content_to_obsidian(self, content: str, page: Dict) -> str:
        """Convert content to Obsidian format."""

        # Step 1: Convert XML to Markdown
        content = self.convert_xml_to_markdown(content)

        # Step 2: Build lookup dictionary for paths
        path_to_filename = {}
        for p in self.pages:
            path_to_filename[f'/en/{p["path"]}'] = p['filename']

        # Step 3: Convert all [Text](/en/path) links
        # - If path matches a page → [[filename|Text]]
        # - If path doesn't match → full URL [Text](https://docs.claude.com/en/path)
        def replace_relative_link(match):
            text = match.group(1)
            full_path = match.group(2)

            # Strip hash fragments and .md extension for lookup
            clean_path = full_path.split('#')[0].rstrip('.md')

            if clean_path in path_to_filename:
                # Convert to wikilink
                filename = path_to_filename[clean_path]
                # Preserve hash fragment if present
                if '#' in full_path:
                    hash_part = '#' + full_path.split('#')[1]
                    return f'[[{filename}{hash_part}|{text}]]'
                else:
                    return f'[[{filename}|{text}]]'
            else:
                # Convert to full URL (directory or page not in our vault)
                full_url = f'https://docs.claude.com{full_path}'
                return f'[{text}]({full_url})'

        content = re.sub(
            r'\[([^\]]+)\]\((/en/[^\)]+)\)',
            replace_relative_link,
            content
        )

        # Step 4: Convert full URLs to wikilinks
        for other_page in self.pages:
            if other_page['title'] == page['title']:
                continue

            url_pattern = re.escape(other_page['url'])

            # [Text](https://docs.claude.com/en/path) → [[filename|Text]]
            content = re.sub(
                rf'\[([^\]]+)\]\({url_pattern}(?:\.md)?\)',
                rf'[[{other_page["filename"]}|\1]]',
                content
            )

        return content

    def _convert_links_in_text(self, text: str) -> str:
        """Convert /en/ links to wikilinks or full URLs in any text."""
        # Build path lookup
        path_to_filename = {}
        for p in self.pages:
            path_to_filename[f'/en/{p["path"]}'] = p['filename']

        def replace_link(match):
            link_text = match.group(1)
            full_path = match.group(2)
            clean_path = full_path.split('#')[0].rstrip('.md')

            if clean_path in path_to_filename:
                # Convert to wikilink
                filename = path_to_filename[clean_path]
                if '#' in full_path:
                    hash_part = '#' + full_path.split('#')[1]
                    return f'[[{filename}{hash_part}|{link_text}]]'
                else:
                    return f'[[{filename}|{link_text}]]'
            else:
                # Convert to full URL for external/directory refs
                full_url = f'https://docs.claude.com{full_path}'
                return f'[{link_text}]({full_url})'

        return re.sub(r'\[([^\]]+)\]\((/en/[^\)]+)\)', replace_link, text)

    def create_frontmatter(self, page: Dict, related: List[str]) -> str:
        today = datetime.now().strftime('%Y-%m-%d')

        tags = [page['category']]
        if page['subcategory']:
            tags.append(page['subcategory'])

        for kw in ['api', 'sdk', 'claude-code', 'agent', 'tool', 'prompt']:
            if kw in page['path'].lower() and kw not in tags:
                tags.append(kw)

        fm = f"""---
created: {today}
modified: {today}
title: "{page['title']}"
url: {page['url']}
category: {page['category']}"""

        if page['subcategory']:
            fm += f"\nsubcategory: {page['subcategory']}"

        if page['description']:
            # Convert /en/ links in description
            desc = self._convert_links_in_text(page["description"])
            fm += f'\ndescription: "{desc.replace('"', '\\"')}"'

        fm += "\ntags:\n"
        for tag in tags:
            fm += f"  - {tag}\n"

        if related:
            fm += "related:\n"
            for r in related[:5]:
                fm += f"  - '[[{r}]]'\n"

        fm += "---\n"
        return fm

    def find_related_pages(self, page: Dict) -> List[str]:
        related = []

        for p in self.pages:
            if p != page and p['subcategory'] == page['subcategory'] and page['subcategory']:
                related.append(p['filename'])

        if len(related) < 3:
            for p in self.pages:
                if p != page and p['category'] == page['category'] and p['filename'] not in related:
                    related.append(p['filename'])
                    if len(related) >= 5:
                        break

        return related

    def create_note(self, page: Dict):
        content_data = self.content_sections.get(page['url'])
        if not content_data:
            return

        related = self.find_related_pages(page)
        frontmatter = self.create_frontmatter(page, related)
        content = self.convert_content_to_obsidian(content_data['content'], page)

        content += f"\n\n---\n\n**Source:** [Official Documentation]({page['url']})\n"
        full_content = frontmatter + "\n# " + page['title'] + "\n\n" + content

        note_dir = self.output_dir / page['folder_path']
        note_dir.mkdir(parents=True, exist_ok=True)

        note_path = note_dir / f"{page['filename']}.md"
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(full_content)

        print(f"  ✓ {page['filename']}")

    def create_moc(self, category: str, pages: List[Dict]):
        today = datetime.now().strftime('%Y-%m-%d')

        subcats: Dict[str, List[Dict]] = {}
        for page in pages:
            subcat = page['subcategory'] or 'general'
            if subcat not in subcats:
                subcats[subcat] = []
            subcats[subcat].append(page)

        fm = f"""---
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
        content += f"> [!abstract] Overview\n> Index for **{category}** documentation\n> {len(pages)} pages across {len(subcats)} sections\n\n"

        for subcat in sorted(subcats.keys()):
            content += f"## {subcat.replace('-', ' ').title()}\n\n"
            for p in sorted(subcats[subcat], key=lambda x: x['title']):
                content += f"- [[{p['filename']}|{p['title']}]]"
                if p['description']:
                    # Convert links in description
                    desc = self._convert_links_in_text(p['description'])
                    content += f" - {desc}"
                content += "\n"
            content += "\n"

        content += f"""## All {category} Pages

```dataview
TABLE description, subcategory
FROM #{category}
WHERE type != "moc"
SORT file.name
```
"""

        moc_path = self.output_dir / category / f"_{category}-index.md"
        moc_path.parent.mkdir(parents=True, exist_ok=True)

        with open(moc_path, 'w', encoding='utf-8') as f:
            f.write(fm + content)

        print(f"  ✓ _{category}-index")

    def create_main_index(self):
        today = datetime.now().strftime('%Y-%m-%d')

        fm = f"""---
created: {today}
modified: {today}
type: moc
tags:
  - index
  - moc
  - claude
aliases:
  - Home
---

"""

        content = f"""# Claude Documentation Vault

> [!info] Welcome
> Complete English documentation for Claude, Claude Code, and APIs
>
> **{len(self.pages)}** pages | **{len(self.categories)}** categories

## Categories

"""

        for cat in sorted(self.categories.keys()):
            count = len(self.categories[cat])
            title = cat.replace('-', ' ').title()
            content += f"### [[_{cat}-index|{title}]]\n{count} pages\n\n"

        content += """## Stats

```dataview
TABLE length(rows) as Pages
FROM ""
WHERE type != "moc"
GROUP BY category
SORT length(rows) DESC
```
"""

        with open(self.output_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(fm + content)

        print("✓ README.md")

    def create_config(self):
        config_dir = self.output_dir / ".obsidian"
        config_dir.mkdir(exist_ok=True)

        with open(config_dir / "app.json", 'w') as f:
            json.dump({
                "alwaysUpdateLinks": True,
                "newLinkFormat": "relative",
                "useMarkdownLinks": False,
                "showFrontmatter": True
            }, f, indent=2)

        print("✓ config")

    def build(self):
        print("\n🚀 Building Obsidian vault\n")

        print("📖 Parsing...")
        self.parse_llms_md()
        self.parse_llms_full_md()

        print(f"\n📁 Creating {self.output_dir.name}/...")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        print("\n⚙️  Config...")
        self.create_config()

        print(f"\n📝 Notes ({len(self.pages)})...")
        for page in self.pages:
            self.create_note(page)

        print(f"\n🗂️  Indices ({len(self.categories)})...")
        for cat, pages in self.categories.items():
            self.create_moc(cat, pages)

        print("\n🏠 Main index...")
        self.create_main_index()

        print(f"\n✅ Done! {self.output_dir.absolute()}\n")


if __name__ == '__main__':
    creator = ObsidianVaultCreator(
        llms_file='llms.md',
        llms_full_file='llms-full.md',
        output_dir='claude-docs-vault'
    )
    creator.build()
