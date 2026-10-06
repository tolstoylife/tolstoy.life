# CLAUDE.md — Tolstoy Research Platform

Project content (mission, architecture, data flow, schema, conventions, contribution model, roadmap) is imported from @AGENTS.md.

This file is a thin Claude Code overlay — only what's specific to running Claude in this repo.

---

## Claude-specific notes

- **oh-my-claudecode (OMC) is switched off.** It is still installed, but disabled in two places in `~/.claude/settings.json` — `enabledPlugins` and the `DISABLE_OMC` environment variable — so none of its skills, agents or hooks load. Don't reach for `/oh-my-claudecode:*` commands or expect its `.omc/` memory to be read; that folder was deleted 2026-08-10. What is active instead: **superpowers** (planning, debugging, verification), **ponytail** (a build-the-simplest-thing-that-works stance, announced by a hook at session start), and **warp**.
- **Direct write OK** for `~/.claude/**`, `.omc/**`, `.claude/**`, `CLAUDE.md`, `AGENTS.md`, `docs/**`, `_generated/**`. For vault content (`website/src/wiki/**`, `website/src/works/**`, `website/src/sources/**`), follow the wiki operations protocol in AGENTS.md — read source, discuss with Johan, then write.
- **Never modify** `primary-sources/**` (immutable) or the TEXT zone in `website/src/works/**/text/*.md` (source text, do not modify).
- **Filename case:** UPPERCASE for top-level project files only (`CLAUDE.md`, `AGENTS.md`, `MANIFEST.md`, `README.md`, `TODO.md`, `LOG.md`, `ROADMAP.md`). Files inside `docs/`, `_generated/`, and other subdirectories use lowercase (`editorial.md`, `conventions.md`, etc.). Universal-convention exceptions: `README.md` and `INDEX.html` stay uppercase even in subdirectories.
- **Skills:** trigger by name (`/start-of-day`) or by keyword. Most relevant here are `start-of-day`, `end-of-day`, `end-of-session`, `handoff` / `resume-handoff`, `corpus-dive`, `wiki-ingest`, and the `obsidian-*` family. `start-of-day` and `corpus-dive` live in this repo's `.claude/skills/`; the rest are personal skills in `~/.claude/skills/`, and `end-of-session` reads its rules from AGENTS.md → "End-of-session deliverables". (`claude-md-improver` no longer exists; it came from the `claude-md-management` plugin, which is disabled.)
