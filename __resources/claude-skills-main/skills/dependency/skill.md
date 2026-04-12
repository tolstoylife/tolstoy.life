---
name: dependency
description: Audit, update, and manage project dependencies — security vulnerabilities, outdated packages, license compliance, and dependency graphs. Works with npm, pip, cargo, go modules, and more.
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
---

# Dependency Management Skill

Comprehensive dependency auditing, updating, and security analysis for any project.

## When to Use
- User asks to audit, check, update, or manage dependencies
- User wants to find vulnerabilities in dependencies
- User wants to understand the dependency tree
- User asks about outdated packages or license compliance

## Workflow

### 1. Detect Package Manager
Scan the project root for:
- `package.json` / `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` → **npm/yarn/pnpm**
- `requirements.txt` / `pyproject.toml` / `setup.py` / `Pipfile` → **pip/poetry/pipenv**
- `Cargo.toml` / `Cargo.lock` → **cargo**
- `go.mod` / `go.sum` → **go modules**
- `Gemfile` / `Gemfile.lock` → **bundler**
- `composer.json` → **composer (PHP)**

### 2. Security Audit
Run the appropriate audit command:

```bash
# npm
npm audit --json

# yarn
yarn audit --json

# pip (requires pip-audit)
pip-audit --format=json -r requirements.txt
# or with safety
safety check --json -r requirements.txt

# cargo
cargo audit --json

# go
govulncheck ./...

# Snyk (universal, if installed)
snyk test --json
```

### 3. Outdated Check
```bash
# npm
npm outdated --json

# pip
pip list --outdated --format=json

# cargo
cargo outdated --format=json

# go
go list -m -u all
```

### 4. Dependency Tree
```bash
# npm
npm ls --all --json

# pip
pipdeptree --json

# cargo
cargo tree

# go
go mod graph
```

### 5. License Check
```bash
# npm
npx license-checker --json --summary

# pip
pip-licenses --format=json

# cargo
cargo license --json
```

## Analysis Format

After running checks, present findings as:

### Security Summary
| Severity | Count | Action Required |
|----------|-------|-----------------|
| Critical | X | Immediate update |
| High | X | Update this sprint |
| Moderate | X | Plan update |
| Low | X | Monitor |

### Outdated Packages (top priority)
| Package | Current | Latest | Breaking? |
|---------|---------|--------|-----------|
| name | x.y.z | a.b.c | Yes/No |

### Recommended Actions
1. Safe updates (patch/minor, no breaking changes)
2. Breaking updates (major version bumps, review needed)
3. Packages with known vulnerabilities (immediate action)

## Update Strategy

- **Safe mode (default):** Only patch and minor updates. Run: `npm update` / `pip install --upgrade` (within constraints)
- **Full mode (user requested):** Include major version bumps. Review breaking changes first.
- **Security-only mode:** Only update packages with known CVEs.

Always run tests after updates:
```bash
# Detect and run project test suite
npm test / pytest / cargo test / go test ./...
```

## Rules
- NEVER auto-update without showing the user what will change
- Always check for lockfile consistency after updates
- Flag any dependency with a known CVE as highest priority
- Note if any dependencies are unmaintained (no commits in 12+ months)
- Check for duplicate/redundant dependencies when possible
