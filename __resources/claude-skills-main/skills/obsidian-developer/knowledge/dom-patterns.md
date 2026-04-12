# Obsidian DOM Patterns

When using `obsidian_inspect_dom`, it helps to know the standard class names Obsidian uses.

## High-Level Layout
- `body`: Root.
- `.workspace`: Container for the entire UI.
- `.workspace-ribbon`: Left sidebar icons.
- `.workspace-split`: Resizable containers.
- `.workspace-tab-header-container`: Tab bars.

## Leaves (Panes)
The content is inside "leaves".
- `.workspace-leaf`: A single tab/pane.
- `.workspace-leaf.mod-active`: The currently focused pane.

## Editor Modes

### 1. Live Preview (CodeMirror 6)
- Container: `.markdown-source-view.mod-cm6`
- Content: `.cm-content` (ContentEditable)
- Lines: `.cm-line`
- Selection logic: Complex (CM6 state), not simple DOM text.

### 2. Reading Mode (Preview)
- Container: `.markdown-preview-view`
- Content: `.markdown-preview-section`
- Structure: Standard HTML (`p`, `h1`, `ul`, `li`).
- **Good for**: Extracting rendered content, checking math rendering (MathJax), or dataview tables.

### 3. Source Mode (Legacy/Raw)
- Similar to Live Preview but with different CSS classes (`.is-source-mode`).

## Modals & Popovers
- `.modal`: Dialog boxes (Settings, Quick Switcher).
- `.popover`: Hover previews.
- `.menu`: Context menus.

## CSS Variables
Obsidian relies heavily on CSS variables for theming.
- `--background-primary`
- `--text-normal`
- `--interactive-accent`

To extract the current theme palette:
```javascript
const style = getComputedStyle(document.body);
({
  bg: style.getPropertyValue('--background-primary'),
  text: style.getPropertyValue('--text-normal')
})
```
