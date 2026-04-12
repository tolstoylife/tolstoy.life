---
name: repo-rag
description: "Codebase-wide Retrieval-Augmented Generation for deep code understanding. Use when: (1) Answering questions about large codebases by searching across all files, (2) Finding related code patterns, implementations, or dependencies across a project, (3) Building context from multiple files before making changes, (4) Understanding how a feature works end-to-end across the codebase, (5) Tracing data flow through multiple modules"
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Task
  - TaskCreate
  - TaskList
  - TaskUpdate
---

# Repo RAG — Codebase Retrieval-Augmented Generation

Deep codebase understanding through systematic multi-file retrieval, pattern matching, and contextual analysis.

## When to Use

Use this skill when:
- Understanding how a feature works across multiple files
- Finding all implementations of a pattern or interface
- Tracing data flow from UI → API → database
- Building context before making cross-cutting changes
- Answering "how does X work?" for complex codebases
- Finding all callers/consumers of a function or API

## When NOT to Use

- Simple single-file edits (just read the file)
- Known file paths (use Read directly)
- Keyword search in 1-2 files (use Grep directly)

## Core Workflow

### Phase 1: Scope Discovery

Map the codebase structure before diving into specifics:

```bash
# 1. Identify project type and structure
find . -maxdepth 2 -name "package.json" -o -name "pyproject.toml" -o -name "Cargo.toml" -o -name "go.mod" | head -20

# 2. Map directory tree
find . -type d -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/venv/*' | head -50

# 3. Identify entry points
# For web apps: main.ts, index.ts, app.ts, server.ts
# For APIs: routes/, endpoints/, handlers/
# For libraries: src/index.ts, src/lib.rs, src/__init__.py
```

### Phase 2: Multi-Strategy Retrieval

Use parallel retrieval strategies for comprehensive results:

**Strategy A — Structural Search (file patterns)**
```
Glob: **/*auth*.{ts,py,rs,go}
Glob: **/routes/**/*.{ts,py}
Glob: **/models/**/*.{ts,py}
```

**Strategy B — Semantic Search (content patterns)**
```
Grep: "function.*authenticate" or "def authenticate"
Grep: "class.*Controller" or "class.*Handler"
Grep: "import.*from.*module"
```

**Strategy C — Dependency Tracing**
```
Grep: "import.*{targetFunction}"  → find all consumers
Grep: "export.*{targetFunction}"  → find the source
Grep: "require.*targetModule"     → find CommonJS usage
```

**Strategy D — Type/Interface Tracing**
```
Grep: "interface.*TargetType"     → find the definition
Grep: "implements.*TargetType"    → find implementations
Grep: ": TargetType"              → find usage sites
```

### Phase 3: Context Assembly

After retrieval, assemble context in this order:

1. **Core definitions** — Types, interfaces, schemas
2. **Implementation** — The actual logic
3. **Callers** — Who uses this code
4. **Tests** — How it's expected to behave
5. **Config** — Environment, routing, middleware

### Phase 4: Synthesis

Produce a structured understanding:

```markdown
## Feature: [Name]

### Entry Points
- [file:line] — [description]

### Data Flow
1. [source] → [transform] → [destination]

### Key Files
| File | Role | Lines |
|------|------|-------|
| ... | ... | ... |

### Dependencies
- Upstream: [what this depends on]
- Downstream: [what depends on this]

### Patterns Used
- [pattern name]: [where applied]
```

## Parallel Retrieval Pattern

For maximum efficiency, always run retrieval in parallel:

```
# Launch parallel searches using Task subagents:
Task 1: Search for type definitions
Task 2: Search for implementations
Task 3: Search for test files
Task 4: Search for configuration
```

## Language-Specific Patterns

### TypeScript/JavaScript
- Entry: `src/index.ts`, `src/app.ts`, `src/main.ts`
- Routes: `src/routes/`, `src/pages/` (Next.js), `src/api/`
- Types: `src/types/`, `*.d.ts`, `src/interfaces/`
- Tests: `__tests__/`, `*.test.ts`, `*.spec.ts`

### Python
- Entry: `__main__.py`, `app.py`, `manage.py`, `main.py`
- Routes: `views.py`, `routes.py`, `endpoints/`
- Types: `models.py`, `schemas.py`, `types.py`
- Tests: `tests/`, `test_*.py`, `*_test.py`

### Rust
- Entry: `src/main.rs`, `src/lib.rs`
- Modules: `src/*/mod.rs`
- Tests: `tests/`, `#[cfg(test)]` blocks

### Go
- Entry: `cmd/*/main.go`, `main.go`
- Handlers: `internal/handler/`, `pkg/`
- Tests: `*_test.go`

## Quality Checklist

Before reporting findings, verify:
- [ ] Searched both file names AND file contents
- [ ] Checked at least 3 retrieval strategies
- [ ] Traced imports/exports for completeness
- [ ] Included test files for behavior context
- [ ] Noted any gaps or areas that couldn't be resolved
