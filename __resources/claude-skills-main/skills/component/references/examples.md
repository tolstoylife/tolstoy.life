# Complete Examples

## Table of Contents

1. [Research Plugin](#research-plugin)
2. [DevOps Plugin](#devops-plugin)
3. [Code Review Plugin](#code-review-plugin)

---

## Research Plugin

Multi-agent research pipeline demonstrating all component types.

### Structure

```
research/
├── .claude-plugin/plugin.json
├── commands/
│   └── research.md
├── agents/
│   ├── researcher.md
│   └── synthesizer.md
├── skills/
│   └── literature-search/SKILL.md
└── styles/
    └── thorough.md
```

### plugin.json

```json
{
  "name": "research",
  "version": "1.0.0",
  "description": "Multi-agent research with literature search and synthesis"
}
```

### commands/research.md

```yaml
---
description: Execute research pipeline on a topic
allowed-tools: [Agent, WebFetch, mcp__scholar__search]
model: opus
argument-hint: [topic]
---

## Phase 1: Literature Search
Spawn researcher agent with topic.

## Phase 2: Synthesis
Pass findings to synthesizer agent.

## Output
Research brief with findings and citations.
```

### agents/researcher.md

```yaml
---
description: Academic researcher for literature discovery. Methodical, thorough.
allowed-tools: [WebFetch, mcp__scholar__search, Read]
model: sonnet
permissionMode: allow
skills: [literature-search]
---

Search multiple databases, assess relevance, extract metadata.
```

### agents/synthesizer.md

```yaml
---
description: Research synthesizer identifying patterns across sources.
allowed-tools: [Read, Write]
model: opus
permissionMode: ask
---

Map concepts, identify convergent findings, generate narrative.
```

### skills/literature-search/SKILL.md

```yaml
---
name: literature-search
description: Systematic literature search procedures. Trigger when searching databases or managing citations.
---

# Literature Search

## Search Strategy
1. Query formulation with Boolean operators
2. Database selection (PubMed, Semantic Scholar)
3. Relevance filtering
4. Citation extraction
```

### styles/thorough.md

```yaml
---
name: thorough
description: Maximum depth research with full audit trail.
keep-coding-instructions: true
---

Search all databases. Include borderline sources.
Document all decisions. Generate methodology section.
```

---

## DevOps Plugin

Build, test, deploy pipeline with staged agents.

### Structure

```
devops/
├── commands/deploy.md
├── agents/
│   ├── builder.md
│   ├── tester.md
│   └── deployer.md
└── skills/
    └── container-ops/SKILL.md
```

### commands/deploy.md

```yaml
---
description: Build, test, and deploy application
allowed-tools: [Agent, Bash(docker:*), Bash(git:*)]
model: sonnet
argument-hint: [environment]
---

## Stage 1: Build
Spawn builder. Create artifacts.

## Stage 2: Test
Spawn tester. Verify quality.

## Stage 3: Deploy
On test pass, spawn deployer.

## Rollback
On failure, execute rollback.
```

### agents/builder.md

```yaml
---
description: Build engineer creating deployable artifacts. Docker expert.
allowed-tools: [Bash(docker:*), Bash(npm:*), Read, Write]
model: sonnet
permissionMode: allow
skills: [container-ops]
---
```

### agents/tester.md

```yaml
---
description: QA engineer executing tests and validating deployment readiness.
allowed-tools: [Bash(npm test:*), Bash(docker:*), Read]
model: sonnet
permissionMode: ask
---

Gate keeper: all tests pass, coverage above threshold, no vulnerabilities.
```

### agents/deployer.md

```yaml
---
description: Operations engineer executing deployments with care.
allowed-tools: [Bash(docker:*), Bash(kubectl:*)]
model: sonnet
permissionMode: ask
skills: [container-ops]
---

Pre-flight checks → backup → rolling deploy → health verify → cleanup.
```

### skills/container-ops/SKILL.md

```yaml
---
name: container-ops
description: Container operations for Docker and Kubernetes. Trigger when building images or deploying containers.
---

# Container Operations

## Multi-stage Build
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

## Health Checks
```bash
kubectl rollout status deployment/app
```
```

---

## Code Review Plugin

Minimal focused plugin.

### Structure

```
code-review/
├── commands/review.md
├── agents/reviewer.md
└── skills/
    └── review-checklist/SKILL.md
```

### commands/review.md

```yaml
---
description: Code review for PR or commit range
allowed-tools: [Agent, Bash(git:*), Bash(gh:*), Read]
model: opus
argument-hint: [pr-number]
---

Spawn reviewer for: correctness, security, performance, maintainability.
```

### agents/reviewer.md

```yaml
---
description: Senior code reviewer. Constructive, specific feedback.
allowed-tools: [Read, Bash(git diff:*), Bash(git log:*)]
model: opus
permissionMode: ask
skills: [review-checklist]
---
```

### skills/review-checklist/SKILL.md

```yaml
---
name: review-checklist
description: Code review procedures and checklists for PR review.
---

# Review Checklist

## Correctness
- Logic errors, edge cases, error handling

## Security
- Input validation, no secrets, auth correct

## Performance
- No N+1 queries, appropriate caching

## Maintainability
- Clear naming, DRY, tests added
```
