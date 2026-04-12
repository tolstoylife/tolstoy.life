# Obsidian Markdown Syntax Reference

Complete reference for Obsidian-flavored Markdown syntax patterns.

## Wikilinks

### Basic Wikilinks

```markdown
[[Note Name]]                    # Link to note
[[Folder/Note Name]]            # Link with path
[[Note Name|Display Text]]      # Link with alias
```

### Links with Anchors

```markdown
[[Note Name#Heading]]           # Link to heading
[[Note Name#^block-id]]         # Link to block
[[Note Name#Heading|Alias]]     # Heading link with alias
```

### Embedded Content

```markdown
![[Note Name]]                  # Embed entire note
![[Note Name#Heading]]          # Embed section
![[Image.png]]                  # Embed image
![[Document.pdf]]               # Embed PDF
![[Audio.mp3]]                  # Embed audio
```

**Regex Pattern**:
```python
WIKILINK_PATTERN = re.compile(r'(!?\[\[)([^\]]+?)\]\]')
```

## Tags

### Inline Tags

```markdown
#tag                            # Simple tag
#nested/tag                     # Nested/hierarchical tag
#tag-with-dashes                # Tag with dashes
#tag_with_underscores           # Tag with underscores
```

### Frontmatter Tags

```yaml
---
tags: [tag1, tag2, nested/tag]
tag: single-tag
---
```

**Regex Pattern**:
```python
INLINE_TAG_PATTERN = re.compile(r'(?:^|\s)#([\w/-]+)')
```

## Frontmatter (YAML)

### Basic Structure

```yaml
---
title: Note Title
created: 2025-01-15
modified: 2025-01-20
tags: [tag1, tag2]
aliases: [Alias 1, Alias 2]
---
```

### Common Fields

```yaml
---
# Metadata
title: string
author: string
created: YYYY-MM-DD or ISO-8601
modified: YYYY-MM-DD or ISO-8601

# Organization
tags: [list, of, tags]
aliases: [list, of, aliases]
category: string
folder: string

# Publishing
published: boolean
draft: boolean
public: boolean

# Custom
status: string
priority: number
rating: number
---
```

### Multi-line Values

```yaml
---
description: >
  This is a multi-line
  description that spans
  multiple lines.

notes: |
  Literal block
  preserves newlines
  and formatting
---
```

**Regex Pattern**:
```python
FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL | re.MULTILINE)
```

## Callouts

### Basic Callout Syntax

```markdown
> [!note]
> This is a note callout

> [!info]
> This is an info callout

> [!tip]
> This is a tip callout

> [!warning]
> This is a warning callout

> [!danger]
> This is a danger callout
```

### Callout with Title

```markdown
> [!note] Custom Title
> Callout content here

> [!tip] Pro Tip
> This callout has a custom title
```

### Foldable Callouts

```markdown
> [!note]- Collapsed by default
> This content is hidden initially

> [!note]+ Expanded by default
> This content is visible initially
```

### Nested Callouts

```markdown
> [!note] Outer Callout
> Outer content
>
> > [!tip] Nested Callout
> > Nested content
```

### Available Callout Types

- `note` - Blue info callout
- `abstract`/`summary`/`tldr` - Cyan summary
- `info` - Blue information
- `todo` - Blue task
- `tip`/`hint`/`important` - Cyan tip
- `success`/`check`/`done` - Green success
- `question`/`help`/`faq` - Yellow question
- `warning`/`caution`/`attention` - Orange warning
- `failure`/`fail`/`missing` - Red failure
- `danger`/`error` - Red danger
- `bug` - Red bug
- `example` - Purple example
- `quote`/`cite` - Gray quote

**Regex Pattern**:
```python
CALLOUT_PATTERN = re.compile(r'>\s*\[!(\w+)\]([-+])?\s*(.*?)\n((?:>.*\n?)*)', re.MULTILINE)
```

## Block References

### Creating Block IDs

```markdown
This is a paragraph with a block ID. ^block-id

- List item with block ID ^list-block
- Another item

| Table | Header |
|-------|--------|
| Data  | More   | ^table-block
```

### Referencing Blocks

```markdown
![[Note Name#^block-id]]        # Embed block
[[Note Name#^block-id]]         # Link to block
```

**Regex Pattern**:
```python
BLOCK_ID_PATTERN = re.compile(r'\^([\w-]+)\s*$')
BLOCK_REF_PATTERN = re.compile(r'\[\[([^\]#]+)#\^([\w-]+)\]\]')
```

## Code Blocks

### Fenced Code Blocks

````markdown
```python
def hello():
    print("Hello, world!")
```

```javascript
console.log("Hello, world!");
```

```typescript
const greeting: string = "Hello, world!";
```
````

### Inline Code

```markdown
Use `inline code` for short snippets.
```

## Lists

### Unordered Lists

```markdown
- Item 1
- Item 2
  - Nested item
  - Another nested
- Item 3

* Alternative syntax
* Works the same
```

### Ordered Lists

```markdown
1. First item
2. Second item
   1. Nested item
   2. Another nested
3. Third item
```

### Task Lists

```markdown
- [ ] Uncompleted task
- [x] Completed task
- [ ] Another task
  - [x] Nested completed
  - [ ] Nested incomplete
```

**Regex Pattern**:
```python
TASK_PATTERN = re.compile(r'^\s*[-*+]\s+\[([ xX])\]\s+(.+)$', re.MULTILINE)
```

## Tables

### Basic Tables

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

### Aligned Tables

```markdown
| Left | Center | Right |
|:-----|:------:|------:|
| L1   | C1     | R1    |
| L2   | C2     | R2    |
```

## Highlighting

```markdown
==Highlighted text==            # Yellow highlight
```

**Regex Pattern**:
```python
HIGHLIGHT_PATTERN = re.compile(r'==([^=]+)==')
```

## Comments

```markdown
%% This is a comment %%         # Inline comment

%%
Multi-line comment
that spans multiple lines
%%
```

**Regex Pattern**:
```python
COMMENT_PATTERN = re.compile(r'%%.*?%%', re.DOTALL)
```

## Dataview Queries

### Inline Queries

```markdown
`= this.file.name`              # Inline dataview
`= dateformat(this.file.ctime, "yyyy-MM-dd")`
```

### Block Queries

````markdown
```dataview
TABLE file.ctime as "Created", file.mtime as "Modified"
FROM "folder"
WHERE contains(file.tags, "tag")
SORT file.name ASC
```

```dataview
LIST
FROM #tag
WHERE status = "active"
```
````

## Mathematical Expressions

### Inline Math

```markdown
$E = mc^2$                      # Inline LaTeX
```

### Block Math

```markdown
$$
\frac{n!}{k!(n-k)!}
$$
```

## Metadata Patterns

### File References

```markdown
[[file.pdf]]                    # Link to PDF
[[file.docx]]                   # Link to Word doc
[[file.xlsx]]                   # Link to Excel
![[image.png]]                  # Embed image
![[video.mp4]]                  # Embed video
```

### External Links

```markdown
[Display Text](https://example.com)
[Display Text](https://example.com "Title")
```

## Common Regex Patterns

```python
# Complete pattern collection
PATTERNS = {
    'wikilink': re.compile(r'(!?\[\[)([^\]]+?)\]\]'),
    'inline_tag': re.compile(r'(?:^|\s)#([\w/-]+)'),
    'frontmatter': re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL | re.MULTILINE),
    'callout': re.compile(r'>\s*\[!(\w+)\]([-+])?\s*(.*?)\n((?:>.*\n?)*)', re.MULTILINE),
    'block_id': re.compile(r'\^([\w-]+)\s*$'),
    'block_ref': re.compile(r'\[\[([^\]#]+)#\^([\w-]+)\]\]'),
    'task': re.compile(r'^\s*[-*+]\s+\[([ xX])\]\s+(.+)$', re.MULTILINE),
    'highlight': re.compile(r'==([^=]+)=='),
    'comment': re.compile(r'%%.*?%%', re.DOTALL),
    'external_link': re.compile(r'\[([^\]]+)\]\(([^\)]+)\)'),
    'heading': re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE),
    'code_block': re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL),
}
```

## Special Characters to Escape

When processing Obsidian markdown programmatically:

```python
SPECIAL_CHARS = {
    '[', ']',  # Wikilinks
    '#',       # Tags, headings
    '^',       # Block references
    '|',       # Aliases
    '!',       # Embeds
    '%',       # Comments
    '=',       # Highlights
    '$',       # Math
    '`',       # Code
    '*',       # Bold, italic
    '_',       # Bold, italic
    '~',       # Strikethrough
}
```

## Edge Cases

### Ambiguous Syntax

```markdown
# This could be a tag or heading
#heading vs # heading

# Wikilink vs. external link
[[Note]] vs [Note](url)

# Code vs. inline code
```code``` vs `code`

# Comment vs. percentage
%% comment %% vs 50%
```

### Nested Structures

```markdown
# Callout with embedded wikilink
> [!note]
> See [[Related Note]] for more info

# Wikilink with tag in alias
[[Note|See #tag for details]]

# Code block with Obsidian syntax
```markdown
[[This should not be processed as a link]]
```
```

## Validation Rules

```python
def is_valid_tag(tag: str) -> bool:
    """Validate tag format."""
    return bool(re.match(r'^[\w/-]+$', tag))

def is_valid_wikilink(link: str) -> bool:
    """Validate wikilink target."""
    # No empty links, no invalid chars
    return bool(link.strip()) and '[' not in link and ']' not in link

def is_valid_block_id(block_id: str) -> bool:
    """Validate block ID format."""
    return bool(re.match(r'^[\w-]+$', block_id))

def is_valid_frontmatter(text: str) -> bool:
    """Validate YAML frontmatter."""
    try:
        yaml.safe_load(text)
        return True
    except yaml.YAMLError:
        return False
```

## Processing Order

When parsing Obsidian markdown:

1. **Extract frontmatter** (always at top)
2. **Remove code blocks** (don't process their content)
3. **Remove comments** (don't process their content)
4. **Extract wikilinks**
5. **Extract tags**
6. **Extract callouts**
7. **Extract other syntax**

This order prevents false positives from syntax inside code blocks or comments.
