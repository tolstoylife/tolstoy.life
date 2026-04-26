# CLAUDE.md — Tolstoy Research Platform

See [AGENTS.md](./AGENTS.md) for project content: mission, architecture, data flow, schema, conventions, contribution model, roadmap.

This file is a thin Claude Code overlay — only what's specific to running Claude in this repo.

---

## Claude-specific notes

- **OMC orchestration** (agent delegation, model routing, skills, hooks, verification protocols) lives in `~/.claude/CLAUDE.md` and is loaded automatically. Nothing project-specific to add right now.
- **Direct write OK** for `~/.claude/**`, `.omc/**`, `.claude/**`, `CLAUDE.md`, `AGENTS.md`, `docs/**`, `_generated/**`. For vault content (`website/src/wiki/**`, `website/src/works/**`, `website/src/letters/**`, `website/src/sources/**`), follow the wiki operations protocol in AGENTS.md — read source, discuss with Johan, then write.
- **Never modify** `primary-sources/**` (immutable) or the TEXT zone in `website/src/works/**/text/*.md` (source text, do not modify).
- **Filename case:** UPPERCASE for top-level project files only (`CLAUDE.md`, `AGENTS.md`, `MANIFEST.md`, `README.md`, `TODO.md`, `LOG.md`, `ROADMAP.md`). Files inside `docs/`, `_generated/`, and other subdirectories use lowercase (`editorial.md`, `conventions.md`, etc.). Universal-convention exceptions: `README.md` and `INDEX.html` stay uppercase even in subdirectories.
- **Skills:** trigger via `/oh-my-claudecode:<name>` or keyword. The `claude-md-improver`, `start-of-day`, `end-of-day`, and `obsidian-*` skills are particularly relevant here.
