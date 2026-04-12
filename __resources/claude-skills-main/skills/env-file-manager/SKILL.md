---
name: env-file-manager
description: Safely manage .env files — generate templates, diff environments, validate required vars, detect secrets in code, and create .env.example files without exposing values.
---

# Env File Manager

Safely manage environment variables across projects and environments.

## When to Use

- Setting up a new project and need .env template
- Comparing env vars between dev/staging/prod
- Auditing for hardcoded secrets in source code
- Generating .env.example from existing .env
- Validating all required env vars are set before deploy

## Workflow

1. **Scan project** — Find all env var references in code (process.env, os.environ, etc.)
2. **Generate template** — Create .env.example with descriptions and placeholder values
3. **Validate** — Check current .env has all required vars, flag missing ones
4. **Diff environments** — Compare vars across .env files (dev vs prod)
5. **Secret audit** — Scan for hardcoded API keys, tokens, passwords in source

## Safety Rules

- NEVER read or display actual .env values
- NEVER commit .env files — verify .gitignore includes them
- Use placeholder patterns: `your-api-key-here`, `changeme`, `<required>`
- Group vars by service (DB, API, Auth, etc.)
