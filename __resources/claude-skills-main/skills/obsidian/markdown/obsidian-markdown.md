---
name: obsidian-markdown
description: This skill should be used when the user asks to "create an Obsidian note", "add wikilinks", "write callouts", "add frontmatter properties", "create embeds", or when working with .md files in Obsidian vaults.
user-invocable: false
---

# Obsidian Flavored Markdown

## Directory Index

**References:**
- [references/basic-formatting.md](references/basic-formatting.md)
- [references/wikilinks-and-embeds.md](references/wikilinks-and-embeds.md)
- [references/callouts.md](references/callouts.md)
- [references/lists-and-tasks.md](references/lists-and-tasks.md)
- [references/code-and-math.md](references/code-and-math.md)
- [references/properties-frontmatter.md](references/properties-frontmatter.md)
- [references/tags-and-html.md](references/tags-and-html.md)

**Examples:** [examples/complete-note.md](examples/complete-note.md) | [examples/research-note.md](examples/research-note.md) | [examples/project-note.md](examples/project-note.md)

**Templates:** [templates/daily-note.md](templates/daily-note.md) | [templates/meeting-note.md](templates/meeting-note.md) | [templates/literature-note.md](templates/literature-note.md)

---

Create and edit Obsidian `.md` files with wikilinks, embeds, callouts, properties, and more.

## Quick Syntax Reference

| Feature | Syntax | Example |
|---------|--------|---------|
| Wikilink | `[[Note]]` | `[[My Note]]` |
| Link with alias | `[[Note\|Display]]` | `[[My Note\|click here]]` |
| Heading link | `[[Note#Heading]]` | `[[Note#Section]]` |
| Block link | `[[Note#^block-id]]` | `[[Note#^abc123]]` |
| Embed note | `![[Note]]` | `![[My Note]]` |
| Embed image | `![[image.png]]` | `![[photo.png\|300]]` |
| Tag | `#tag` | `#project/active` |
| Callout | `> [!type]` | `> [!note] Title` |

## Core Concepts

### Wikilinks vs Markdown Links

```markdown
[[Note Name]]                    # Wikilink (Obsidian)
[Display](Note%20Name.md)        # Markdown link (portable)
```

Use wikilinks for internal vault navigation. Use markdown links for portability.

### Embeds

```markdown
![[Note]]                        # Embed entire note
![[Note#Heading]]                # Embed section
![[Note#^block-id]]              # Embed specific block
![[image.png|400]]               # Embed image (400px wide)
```

### Callouts

```markdown
> [!note] Optional Title
> Content here

> [!warning]- Collapsed by default
> Hidden content
```

**Types**: note, tip, warning, danger, info, success, question, example, quote

### Properties (Frontmatter)

```yaml
---
title: My Note
date: 2024-01-15
tags: [project, active]
status: in-progress
---
```

## Detailed Documentation

For comprehensive syntax, see:

- [Basic Formatting](references/basic-formatting.md) - Paragraphs, headings, text styles
- [Wikilinks & Embeds](references/wikilinks-and-embeds.md) - Links, embeds, block references
- [Callouts](references/callouts.md) - All callout types, nesting, custom CSS
- [Lists & Tasks](references/lists-and-tasks.md) - Lists, checkboxes, quotes
- [Code & Math](references/code-and-math.md) - Code blocks, LaTeX, Mermaid
- [Properties](references/properties-frontmatter.md) - YAML frontmatter
- [Tags & HTML](references/tags-and-html.md) - Tags, HTML, comments

## Examples

Working Obsidian notes you can copy:

- [Complete Note](examples/complete-note.md) - Full-featured project note
- [Research Note](examples/research-note.md) - Academic literature review
- [Project Note](examples/project-note.md) - Project management dashboard

## Templates

Starter templates to fill in:

- [Daily Note](templates/daily-note.md) - Daily journal template
- [Meeting Note](templates/meeting-note.md) - Meeting notes template
- [Literature Note](templates/literature-note.md) - Literature review template

## References

- [Obsidian Help - Formatting](https://help.obsidian.md/syntax)
- [Obsidian Help - Links](https://help.obsidian.md/links)
- [Obsidian Help - Callouts](https://help.obsidian.md/callouts)

## Memory Integration

This subskill contributes to the [Obsidian skill's](../SKILL.md) self-iterative memory:

- **Tracked patterns**: wikilinks, embeds, callouts, properties, tags
- **Memory location**: `.claude/obsidian-memory.json`
- **Learning**: Your frequently used patterns inform future suggestions

[← Back to Obsidian Skill](../SKILL.md)
