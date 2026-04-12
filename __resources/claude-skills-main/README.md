# Claude Code Skills Arsenal

> **800 curated skills** for [Claude Code](https://claude.com/claude-code) — automation, development, reasoning, security, infrastructure, and creative skills for the Claude CLI agent.

```
skills/
├──  99  Azure SDK & cloud skills
├──  36  engineering & architecture
├──  35  language & framework specialists
├──  20  product management & UX
├──  28  testing & TDD
├──  10  data science & ML
├──  14  security & vulnerability scanning
├──  15  DevOps & infrastructure
├──  14  marketing & content
├──  21  business & strategy
├──  30  routers & orchestrators
├──  11  reasoning & cognitive tools
├──   8  Hugging Face ML skills
├──   8  Obsidian knowledge management
├──  16  GODMODE MCP integrations
├──  12  Manus platform agents
├──   6  file format processors
├──   7  deployment targets
└── 410  development, research & creative skills
```

## Sources

| Source | Skills | Type |
|--------|--------|------|
| Custom / locally authored | ~160 | Routers, orchestrators, MCP integrations, reasoning frameworks |
| [microsoft/skills](https://github.com/microsoft/skills) | 113 | Azure SDK skills |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | ~190 | Product, marketing, engineering, business |
| [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) | ~110 | Language/framework specialists, testing, security |
| [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) | ~60 | Full-stack development specialists |
| [openai/skills](https://github.com/openai/skills) | 33 | OpenAI patterns |
| [anthropics/skills](https://github.com/anthropics/skills) | 14 | Official Anthropic skills |
| [huggingface/skills](https://github.com/huggingface/skills) | 8 | ML model training & datasets |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 5 | React/Next.js best practices |
| Other (supabase, remotion, gpt-researcher) | 3 | Specialized |

## Architecture

All skills live in `skills/` as self-contained directories with `SKILL.md` files. No external service dependencies — every skill works locally with Claude Code's native tools.

Tracked in `.skill-lock.json` with source provenance, install dates, and content hashes.

## Usage

Skills are loaded on-demand when invoked via `/skill-name` or matched by Claude Code's skill router. Symlink `skills/` to `~/.claude/skills/` for automatic discovery.

## License

Individual skills retain their original licenses. See each skill's directory for details.
