---
name: rules
description: Personal working rules, decision frameworks, and preferences for ejarbe. Invoke with /rules to surface these during any session. AUTO-TRIGGER when working with MCP servers, MCP transport, SSE, streamable HTTP, server migration, .well-known metadata, or MCP server discovery/registration.
user_invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - WebFetch
  - WebSearch
  - mcp__godmode__*
---

# Rules — ejarbe's Working Principles

## Decision Framework

### Bayesian 80% Threshold
Every action must have P(correct) ≥ 80% before executing. If confidence is below threshold, ask — don't guess. Surface the probability and verdict (PASS/FAIL) for non-trivial decisions.

**Pre-execution checklist:**
1. Platform check (macOS/Apple Silicon, not Linux)
2. Existence check (does the file/tool/service exist?)
3. Redundancy check (is this already built in manus-chatbot?)
4. Surface P(correct) → PASS or FAIL

### Think Before Changing
- Read actual files before modifying them
- Check persistent memory before asking questions
- Verify with `git log`, `git blame`, or file reads — don't assume
- No speculative or exploratory actions without justification

## Tool Hierarchy

### Always Use manus-chatbot First
The manus-chatbot repo is the primary toolbox. Before reaching for system tools or external packages:

1. **Check repo tools:** `~/manus-chatbot/tools/`, `~/manus-chatbot/agents/job_tools/`
2. **Check repo agents:** 23 agents including CivicAIPolicyAgent, DataScientistAgent
3. **Check MCP servers:** godmode (106 tools), ml-toolkit (14), intelligence (14)
4. **Check skills:** 1,255 skills in `~/.claude/skills/`
5. **Last resort:** System tools, `pip install`, `brew install`

Never run `which <tool>` when repo capabilities exist.

### MCP Server Rules
- godmode + intelligence = SSE transport. Do NOT migrate to streamable-http (breaks Claude Code + Desktop)
- ml-toolkit = streamable-http (already migrated, works fine)
- For new Python clients, use stdio direct to `godmode_server.py` / `intelligence_server.py`
- Launchd manages all 3 persistent servers — restart via `launchctl stop/start com.manus.*`

## Coding Standards

### Bandit Variant System
The coding style is selected automatically by the bandit orchestrator:
- **strict_tdd** — Minimal, correct code. Edge cases first. No extras.
- **balanced** — Pragmatic, clean, readable. Brief comments where helpful.
- **exploratory** — Elegant, Pythonic, creative. Refactor for clarity.

Task type determines variant: greenfield = exploratory, refactor = balanced, test = strict_tdd.

### Code Principles
- Smallest diffs. No drive-by refactors.
- Only change what's necessary for the task
- Don't add features that weren't requested
- Test before declaring done: `python3 -m pytest tests/ -v`
- Format before committing: `black agents/ && isort agents/`

### What Not To Do
- Don't use `sed -i` on critical files (wiped `.env` to 0 bytes on Mar 2)
- Don't read/write `.env` files directly (blocked in settings)
- Don't install system tools when repo tools exist
- Don't ask project/priority questions at session start — check memory
- Don't tell me to restart things — do it yourself

## Architecture Preferences

### Intent-First, Not Keyword
- Route via IntentClassifierAgent, not string matching
- Track user behavior with UserIntentTracker
- Share context via message bus

### Model Selection
- FREE local models first (deepseek-r1:32b, qwen3:32b, phi4)
- Cloud only when quality demands it (Claude Sonnet for research, GPT-4 for premium)
- Fallback chains: primary → fallback → never escalate to premium by default

### Deployment
- senna-deploy handles Azure (dev/staging/prod via Pulumi)
- 5 CI/CD workflows in GitHub Actions
- 7 governance gates (PII, injection, toxicity, bias, groundedness, jailbreak, config)

## Communication Preferences

- Be concise. Lead with the answer, not the reasoning.
- Don't summarize what you just did — I can read the diff.
- Don't use emojis unless I ask.
- Use `/think` before risky decisions.
- Save session context to memory before ending — always.
- If unsure, surface the trade-offs and let me decide.

## Projects & Context

| Project | Location | What It Is |
|---------|----------|-----------|
| manus-chatbot | `~/manus-chatbot/` | My platform — 23 agents, 505 passing tests, civic AI |
| senna-deploy | `~/senna-deploy/` | Deployment copy — 3 Azure environments |
| OpenManus | `~/OpenManus/` | Fork — reference only, effectively stale upstream |
| Government AI | `~/Desktop/Government AI/` | NIST, Maryland, San Jose, Manatee County docs |
| Bandit | `~/llm_bandit_orchestrator/` | Coding style optimizer (Thompson sampling) |

## MCP Transport Direction (March 2026)

Streamable HTTP is the transport that lets MCP servers run as remote services rather than local processes. It unlocked production deployments but surfaced gaps at scale: stateful sessions fight with load balancers, horizontal scaling requires workarounds, and there's no standard way for a registry or crawler to learn what a server does without connecting to it.

**Two workstreams happening:**
1. **Transport + session model evolution** — Make servers horizontally scalable without holding state. Clear, explicit session mechanisms.
2. **Standard metadata format** — Served via `.well-known`, so server capabilities are discoverable without a live connection.

**Critical constraint:** No new official transports this cycle — only evolving the existing transport. Keeping the transport set small is a deliberate MCP design principle.

**What this means for us:**
- Don't build on SSE transport for new integrations — it's legacy
- Don't invent custom transports — wait for the spec to evolve
- Streamable HTTP is the path forward, but expect breaking changes around sessions and statefulness
- Watch for `.well-known` metadata spec — will change how we discover and register MCP servers
- Our godmode/intelligence SSE servers will eventually need migration, but not until the spec stabilizes

## Hard-Won Lessons

0. **Empty ≠ unused, stale ≠ unreferenced** (Mar 15) — Deleted `~/mcp-store/` because it was empty; it was the `--work-dir` for a running MCP server. Before deleting or moving ANYTHING: check running processes, grep all configs (.zshrc, .mcp.json, launchd plists, desktop config), verify with process list. Never optimize for "looks unused" — only act on "verified unused."
1. **sed on macOS wiped .env** (Mar 2) — Always `cp` backup first, or use a verifiable method
2. **Ollama naming** — `phi4` not `phi-4`, `nemotron-3-nano` not `nemotron`
3. **Open WebUI Gemini URL** — NO trailing slash on `generativelanguage.googleapis.com/v1beta/openai`
4. **MCP SSE vs streamable-http** — Python MCP client 1.26.0 hangs on old SSE servers. Use stdio.
5. **NODE_OPTIONS with npx** — Unreliable. Use bash wrapper scripts instead.
6. **Test stubs ≠ broken code** — Tests for unimplemented features are specs, not regressions. Implement them.
7. **Config.toml with keys** — Always gitignore. Check before every push.
