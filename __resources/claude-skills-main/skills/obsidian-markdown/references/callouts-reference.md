# Obsidian Callouts Reference

Callouts add highlighted content blocks without breaking note flow.

## Basic Syntax

```markdown
> [!type] Optional Title
> Content goes here.
> Supports **Markdown**, [[Wikilinks]], and ![[embeds]]
```

## Foldable Callouts

- `> [!type]+` - Expands by default
- `> [!type]-` - Collapses by default

```markdown
> [!faq]- Are callouts foldable?
> Yes! Contents are hidden when collapsed.
```

## Nested Callouts

```markdown
> [!question] Can callouts be nested?
> > [!todo] Yes, they can.
> > > [!example] Multiple levels supported.
```

## Supported Types

### note
```markdown
> [!note]
> Default callout type.
```

### abstract
```markdown
> [!abstract]
> Summary or overview.
```
**Aliases:** `summary`, `tldr`

### info
```markdown
> [!info]
> Informational content.
```

### todo
```markdown
> [!todo]
> Task or action item.
```

### tip
```markdown
> [!tip]
> Helpful suggestion.
```
**Aliases:** `hint`, `important`

### success
```markdown
> [!success]
> Successful outcome.
```
**Aliases:** `check`, `done`

### question
```markdown
> [!question]
> Question or query.
```
**Aliases:** `help`, `faq`

### warning
```markdown
> [!warning]
> Warning or caution.
```
**Aliases:** `caution`, `attention`

### failure
```markdown
> [!failure]
> Failed outcome.
```
**Aliases:** `fail`, `missing`

### danger
```markdown
> [!danger]
> Dangerous or critical issue.
```
**Alias:** `error`

### bug
```markdown
> [!bug]
> Bug or defect.
```

### example
```markdown
> [!example]
> Example or demonstration.
```

### quote
```markdown
> [!quote]
> Quotation or citation.
```
**Alias:** `cite`

## Custom Callouts (CSS)

```css
.callout[data-callout="custom-type"] {
    --callout-color: 0, 0, 0;
    --callout-icon: lucide-alert-circle;
}
```

- `--callout-color`: RGB values (0-255)
- `--callout-icon`: Lucide icon ID from lucide.dev or SVG element

```css
--callout-icon: '<svg>...custom svg...</svg>';
```
