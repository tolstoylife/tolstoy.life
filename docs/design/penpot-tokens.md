---
layer: reference
lastUpdated: 2026-05-09
tags: [design]
---

# Penpot tokens

How the design tokens in `website/src/_data/designTokens/` are pushed into the **tolstoy.life - design tokens** file on [design.penpot.app](https://design.penpot.app).

## TL;DR

Always regenerate the DTCG artifact from JSON first, then push to Penpot via MCP (preferred) or a manual UI import (fallback):

```bash
cd website
npm run penpot:tokens   # regenerates tokens/penpot-tokens.dtcg.json + ../DESIGN.md
```

Then one of:

- **Live push via MCP** (preferred when the server is running) — ask Claude to push tokens; it walks the DTCG file via the Penpot Plugin API and reports counts per set. See "Live push via MCP" below.
- **Manual import** (fallback) — open `tolstoy.life - design tokens` in Penpot → Tokens panel → import → select `website/tokens/penpot-tokens.dtcg.json`.

Either way, themes (Light / Dark presets) must be set up by hand in the Penpot UI — see "Themes" below.

To regenerate only one artifact:

```bash
cd website
npm run design:md      # only DESIGN.md
node ./src/_config/setup/build-penpot-tokens.js   # only the DTCG file
```

## Sources of truth

| File | Becomes |
| --- | --- |
| `website/src/_data/designTokens/colors.json` | `core/colors` set + `color.semantic.*` in `theme/light` + `theme/dark` |
| `website/src/_data/designTokens/fonts.json` | `font.family.*` in `core/typography` |
| `website/src/_data/designTokens/textWeights.json` | `font.weight.*` in `core/typography` |
| `website/src/_data/designTokens/textSizes.json` | `font.size.*` in `core/typography` |
| `website/src/_data/designTokens/textLeading.json` | `font.lineHeight.*` in `core/typography` |
| `website/src/_data/designTokens/typography.json` | `type.*` composite styles in `core/typography` |
| `website/src/_data/designTokens/spacing.json` | `space.*` in `core/spacing` |
| `website/src/_data/designTokens/borderRadius.json` | `radius.*` in `core/layout` |
| `website/src/_data/designTokens/viewports.json` | `breakpoint.*` in `core/layout` |
| `website/src/_data/designTokens/semanticColors.json` | `color.bg/text/headline/...` in `theme/light` + `theme/dark` |

The JSON files are themselves the source of truth for the website. The DTCG file is a derived artifact you regenerate any time the JSON changes.

`colors.json` is itself generated from `colorsBase.json` by `npm run colors`, so if you edited `colorsBase.json` first, run that before `penpot:tokens`.

## Mapping rules

The build script (`website/src/_config/setup/build-penpot-tokens.js`) applies these transformations:

- **JSON nesting → dot-separated token names.** `gray.100` becomes `color.gray.100`. Hyphens stay (`space.s-m`, `font.size.step-min-2`).
- **Fluid Utopia values become the max, in pixels.** `{min: 10, max: 14}` becomes `"14px"`. Spacing and font sizes both go through this.
- **Border radii keep their rem.** Penpot accepts unit-suffixed strings, so `0.1875rem` stays `"0.1875rem"` and accessibility-relative sizing is preserved.
- **Viewports become `dimension` tokens with px.** `640` → `"640px"`.
- **Light/dark colors are split.** The `red`, `blue`, `green` colors in `colors.json` have a primary value plus a `.subdued` variant. The primary values land in `theme/light`; the subdued values land in `theme/dark`. They share the same token names (e.g. `color.semantic.red`) so a shape bound to `color.semantic.red` automatically follows whichever theme is active. The same theme-swap pattern is used for the semantic background/text/headline tokens defined in `semanticColors.json`, which mirror the `--color-*` CSS variables in `variables.css`.
- **Font families use the Penpot-recognized name.** Penpot's font registry uses canonical names like `Source Serif 4` and `Source Sans 3`, not the CSS-side family + fallback stack. Each entry in `fonts.json` carries an optional `penpot` field (e.g. `"penpot": "Source Serif 4"`); the build script prefers it and emits a single-element `fontFamilies` value. The full CSS fallback stack stays untouched in `$value` for the website.
- **Typography composites bundle several atomic tokens.** Each entry in `typography.json` becomes a `type.*` token of Penpot's `typography` type, with inner keys (`fontFamily`, `fontWeight`, `fontSize`, `lineHeight`) referencing the atomic tokens via the `{token.path}` syntax. Editing a font size in `textSizes.json` cascades through every type style automatically.

## Sets and themes

Six sets are emitted, in this order (order matters — Penpot resolves conflicts in favor of later sets):

1. `core/colors` (24 tokens) — gray, amber, and base palettes
2. `core/typography` (27 tokens) — families, weights, sizes, line heights, and `type.*` composite styles (body, heading.1–3, blockquote, citation, caption)
3. `core/spacing` (16 tokens) — fixed and fluid spacing steps
4. `core/layout` (7 tokens) — border radii and viewport breakpoints
5. `theme/light` (9 tokens) — semantic colors for light mode (accent reds/blues/greens plus bg/text/headline)
6. `theme/dark` (9 tokens) — same names with dark-mode values

Two themes (Light, Dark) are also part of the design, but they have to be created manually — see "Themes" below.

## Live push via MCP (preferred)

When the Penpot MCP server is connected (see "MCP setup"), Claude can write the catalog directly via `mcp__penpot__execute_code`. The walk is:

1. Read `website/tokens/penpot-tokens.dtcg.json`.
2. For each set in `$metadata.tokenSetOrder`:
   - `catalog.addSet({ name })` and `set.toggleActive()`.
   - For each leaf token: `set.addToken({ type, name, value })`.
3. Deactivate `theme/dark` so the default catalog state is light-themed.
4. Skip themes — they're created manually in the UI (see below).

The DTCG file is already in the shape the API expects:

- spacing / dimension / borderRadius / fontSizes are strings with units
- `fontFamilies` `$value` arrays are unwrapped to a single string at push time
- `number`-type values (line heights) are stringified
- references use `{token.path}` syntax — the API resolves them natively

After the push, ask Claude to verify counts (24 / 27 / 16 / 7 / 9 / 9 = 92).

## Manual import (fallback)

If MCP isn't running, the Penpot UI imports the DTCG file directly:

1. Open `tolstoy.life - design tokens` in Penpot.
2. Tokens panel → import → select `website/tokens/penpot-tokens.dtcg.json`.
3. The importer creates sets and tokens. The `$themes` block in the DTCG file *should* auto-create the Light and Dark themes — but we've never confirmed it works, so verify after import.

## Themes (manual — both paths)

The Penpot Plugin API rejects `theme.addSet(set)` with an opaque validation error, so theme membership can't be bound programmatically. Themes have to be created in the UI:

1. Tokens panel → **Themes** tab → **+ Theme**.
2. Name it `Light`. Check `core/colors`, `core/typography`, `core/spacing`, `core/layout`, `theme/light`.
3. Repeat for `Dark` with `theme/dark` instead of `theme/light`.

Once both themes exist, toggling between them flips the `theme/*` set activation, which swaps every semantic color (`bg`, `text`, `headline`, `accent.*`) automatically.

## Plugin API gotchas

For future sessions extending the live-push or doing other Plugin API work — these will save hours:

| Issue | Fix |
| --- | --- |
| `theme.addSet(set)` throws `Value not valid: Field message is invalid: .` and does not bind sets to themes | Create themes manually in the UI (see "Themes") |
| `addTheme({group: "<non-empty>", ...})` throws the same opaque error *but actually creates the theme anyway* — partial success disguised as failure | Use `{group: "", name}` only; if you've already tried other groups, check `catalog.themes` for stray partial creates and `theme.remove()` them |
| The Penpot high-level overview documents `addTheme(group, name)` as two positional strings — it isn't | Actual signature: `addTheme(arg: { group: string; name: string })` (single object) |
| Activating both `theme/light` and `theme/dark` simultaneously makes same-named tokens (e.g. `color.bg`) resolve to the *later* set's value catalog-wide | Default state after a fresh push: `theme/light` active, `theme/dark` inactive. Themes (Light/Dark) flip the activation later. |
| `fontFamilies` value: API expects scalar string; DTCG holds an array | Unwrap `value[0]` at push time (live-push code already does this) |
| `number`-type values must be strings (`"1.4"` not `1.4`) | DTCG already does this; just don't pass raw numbers if writing API calls by hand |
| Composite `typography` value uses singular keys | `{fontFamily, fontWeight, fontSize, lineHeight}` — references via `{font.family.display}` work |
| `File.name` and `Library.name` are read-only getters | Rename via Penpot UI; can't be set programmatically |
| Spacing / dimension / borderRadius / fontSizes reject bare numbers | Always pass strings with units: `"14px"`, `"0.1875rem"` |
| `fontFamilies` rejects CSS fallback stacks | Only the primary family, must match Penpot's font registry; query `penpot.fonts.all` for canonical names |

## Re-running

JSON is always the source. To re-push:

```bash
cd website
npm run colors           # only if colorsBase.json changed
npm run penpot:tokens    # regenerates tokens/penpot-tokens.dtcg.json
# Then either: live-push via MCP, or import in the Penpot UI
```

The push is non-destructive in the JSON direction. On the Penpot side, manual edits made through the UI will be overwritten on the next push, since the build script regenerates the DTCG file from JSON every time.

## Why MCP works for live push

The Penpot Plugin API is only callable from inside an in-browser plugin connected to an open file. There is no Node-side API. The Penpot MCP server bridges that gap: from the user's side it's a CLI endpoint; from Penpot's side it's a connected plugin. The same DTCG file that the UI importer reads can be walked through `mcp__penpot__execute_code` against the live `tokens` catalog — no manual click-through.

## MCP setup (one-time per machine)

The MCP server registration is checked in at `website/.mcp.json`. On a fresh machine:

1. From `website/`, run `npx @penpot/mcp@latest` and leave it running (use `@latest`, not `@beta` — `@beta` has had blocking bugs).
2. Open `tolstoy.life - design tokens` at <https://design.penpot.app>.
3. Inside the workspace, **Ctrl+Alt+P** → if the Penpot MCP plugin is not listed, **Load from URL** with `http://localhost:4400/manifest.json` (one-time).
4. Click the plugin → **Connect to MCP server** → wait for the panel to show **Connected**.
5. Restart Claude Code if `.mcp.json` was just added.

Verify from the host with `claude mcp list` — should show `penpot ✓ Connected`.

The plugin connection drops on tab refresh, plugin panel close, file navigation, or stopping the `npx` server. Recovery: re-open the plugin panel and click **Connect to MCP server** until it says **Connected**. The `npx` server itself doesn't need to be restarted unless you stopped it.

## Files

- `website/src/_config/setup/build-penpot-tokens.js` — the build script
- `website/src/_data/designTokens/*.json` — sources
- `website/tokens/penpot-tokens.dtcg.json` — generated artifact (committed so PR diffs show token changes)
- `website/.mcp.json` — Penpot MCP server registration (committed, project scope)
- `website/package.json` → `scripts.penpot:tokens`
