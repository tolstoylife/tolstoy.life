# Complete Robot Command Reference for bv

## Quick Reference

| Command | Purpose | Output | Performance |
|---------|---------|--------|-------------|
| `--robot-insights` | Full graph analysis | JSON | Medium (1-5s) |
| `--robot-plan` | Execution plan | JSON | Fast (<1s) |
| `--robot-priority` | Priority recommendations | JSON | Fast (<1s) |
| `--robot-diff` | Historical comparison (with `--diff-since`) | JSON | Fast (<2s) |
| `--robot-drift` | Drift detection (with `--check-drift`) | JSON | Fast (<1s) |
| `--robot-recipes` | Available recipes | JSON | Instant |
| `--robot-help` | AI agent help | Text | Instant |

---

## Analysis Commands

### `--robot-insights`

**Full graph analysis with all 9 metrics**

**Command:**
```bash
bv --robot-insights
```

**Output Schema:**
```json
{
  "timestamp": "2025-12-02T10:30:00Z",
  "graphStats": {
    "totalIssues": 150,
    "openIssues": 120,
    "closedIssues": 30,
    "totalDependencies": 245,
    "density": {
      "density": 0.42,
      "totalNodes": 150,
      "totalEdges": 245,
      "maxPossibleEdges": 583,
      "interpretation": "balanced"
    }
  },
  "metrics": {
    "pageRank": [...],
    "betweenness": [...],
    "hits": [...],
    "criticalPath": [...],
    "eigenvector": [...],
    "degree": [...]
  },
  "cycles": [],
  "topologicalSort": {
    "order": [...],
    "isValid": true
  },
  "recommendations": {
    "highImpactIssues": ["core-001", "api-005"],
    "bottleneckIssues": ["api-gateway-012"],
    "foundationalIssues": ["database-007"]
  }
}
```

**Use Cases:**
- Initial project assessment
- Health monitoring
- Identifying architectural issues
- Understanding dependency structure

**Performance:** Medium (1-5s for large graphs)

**Example Usage:**
```bash
# Save to file
bv --robot-insights > insights.json

# Extract high-impact issues
bv --robot-insights | jq '.recommendations.highImpactIssues'

# Check for cycles
bv --robot-insights | jq '.cycles | length'

# Get density interpretation
bv --robot-insights | jq -r '.graphStats.density.interpretation'
```

---

### `--robot-plan`

**Dependency-respecting execution plan**

**Command:**
```bash
bv --robot-plan
```

**Output Schema:**
```json
{
  "timestamp": "2025-12-02T10:30:00Z",
  "summary": {
    "totalTracks": 3,
    "totalActionableIssues": 12,
    "recommendedNextIssue": "core-001",
    "reasoning": "Highest PageRank (0.85) with 8 direct dependents"
  },
  "tracks": [
    {
      "trackId": 1,
      "description": "Core Infrastructure Track",
      "items": [
        {
          "issueId": "core-001",
          "title": "Implement authentication service",
          "state": "open",
          "priority": 3,
          "dependencies": [],
          "unblocks": ["api-005", "frontend-012"],
          "impactScore": 0.85,
          "canStartNow": true,
          "reasoning": "Zero dependencies, high PageRank"
        }
      ],
      "parallelizable": true
    }
  ]
}
```

**Use Cases:**
- "What should I work on next?"
- Identifying parallelizable work streams
- Sprint planning
- Team allocation

**Performance:** Fast (<1s)

**Example Usage:**
```bash
# Get recommended next issue
bv --robot-plan | jq -r '.summary.recommendedNextIssue'

# Find parallelizable tracks
bv --robot-plan | jq '.tracks[] | select(.parallelizable == true)'

# Get actionable issues
bv --robot-plan | jq '.tracks[].items[] | select(.canStartNow == true)'

# Extract high-impact work
bv --robot-plan | jq '.tracks[].items[] | select(.impactScore > 0.7)'
```

---

### `--robot-priority`

**Priority adjustment recommendations**

**Command:**
```bash
bv --robot-priority
```

**Output Schema:**
```json
{
  "timestamp": "2025-12-02T10:30:00Z",
  "recommendations": [
    {
      "issueId": "database-migration-007",
      "currentPriority": 2,
      "recommendedPriority": 4,
      "direction": "increase",
      "confidence": 0.92,
      "reasoning": "Critical path score of 15 (blocking 12 downstream)",
      "metrics": {
        "pageRank": 0.81,
        "betweenness": 0.67,
        "criticalPath": 15,
        "unblocksPotential": 12
      }
    }
  ],
  "summary": {
    "totalRecommendations": 5,
    "highConfidenceCount": 3,
    "averageImpactDelta": 1.8
  }
}
```

**Use Cases:**
- Validating current priorities
- Detecting misaligned priorities
- Sprint re-planning
- Quarterly reviews

**Performance:** Fast (<1s)

**Example Usage:**
```bash
# Get high-confidence recommendations
bv --robot-priority | jq '.recommendations[] | select(.confidence > 0.8)'

# Find under-prioritized issues
bv --robot-priority | jq '.recommendations[] | select(.direction == "increase")'

# Find over-prioritized issues
bv --robot-priority | jq '.recommendations[] | select(.direction == "decrease")'

# Count recommendations
bv --robot-priority | jq '.summary.totalRecommendations'
```

---

## Historical Analysis Commands

### `--diff-since` + `--robot-diff`

**Compare current state to historical point**

**Command:**
```bash
bv --diff-since <commit|date> --robot-diff
```

**Accepts:**
- Git SHA: `abc1234`
- Branch: `main`, `develop`
- Tag: `v1.0.0`
- Relative: `HEAD~5`
- Date: `2025-11-01`

**Output Schema:**
```json
{
  "timestamp": "2025-12-02T10:30:00Z",
  "comparisonPoint": "2025-11-01",
  "changes": {
    "newIssues": [...],
    "closedIssues": [...],
    "removedIssues": [...],
    "modifiedIssues": [...],
    "newCycles": [],
    "resolvedCycles": [
      {
        "path": ["feature-A-001", "feature-B-002", "feature-A-001"],
        "length": 2,
        "severity": "critical"
      }
    ]
  },
  "summary": {
    "totalChanges": 12,
    "healthTrend": "improving",
    "criticalChanges": [
      "Resolved critical cycle between feature-A and feature-B",
      "Density decreased from 0.58 to 0.51"
    ]
  }
}
```

**Use Cases:**
- "What changed since last sprint?"
- Impact analysis
- Tracking evolution
- Health monitoring

**Performance:** Fast (<2s)

**Example Usage:**
```bash
# Compare to 10 commits ago
bv --diff-since HEAD~10 --robot-diff

# Compare to release tag
bv --diff-since v1.0.0 --robot-diff

# Compare to date
bv --diff-since 2025-11-01 --robot-diff

# Get health trend
bv --diff-since HEAD~10 --robot-diff | jq -r '.summary.healthTrend'

# Check for new cycles
bv --diff-since v1.0.0 --robot-diff | jq '.changes.newCycles | length'

# List resolved cycles
bv --diff-since HEAD~10 --robot-diff | jq '.changes.resolvedCycles'
```

---

### `--as-of`

**View historical state (non-robot, but useful)**

**Command:**
```bash
bv --as-of <commit|date>
```

**Combine with robot commands:**
```bash
bv --as-of v1.0.0 --robot-insights
bv --as-of 2025-11-01 --robot-plan
```

**Use Cases:**
- Historical auditing
- Understanding past decisions
- Release retrospectives

---

## Drift Detection Commands

### `--save-baseline`

**Save current metrics as reference point**

**Command:**
```bash
bv --save-baseline "description"
```

**Example:**
```bash
bv --save-baseline "Q4 2025 baseline - pre-refactoring"
bv --save-baseline "v1.0.0 release baseline"
bv --save-baseline "Before microservices migration"
```

**Output:** Saves to `.bv/baseline.json`

**Use Cases:**
- Before major refactoring
- Quarterly snapshots
- Release milestones
- CI baseline establishment

---

### `--check-drift` + `--robot-drift`

**Detect metric drift from baseline**

**Command:**
```bash
bv --check-drift --robot-drift
```

**Output Schema:**
```json
{
  "hasDrift": true,
  "exitCode": 2,
  "summary": "Warning: 2 alerts - density increased 45%, 3 more blocked issues",
  "alerts": [
    {
      "level": "warning",
      "category": "density",
      "message": "Graph density increased by 45% since baseline",
      "currentValue": 0.58,
      "baselineValue": 0.40,
      "changePercent": 45
    }
  ],
  "baseline": {
    "createdAt": "2025-11-01T09:00:00Z",
    "gitCommit": "abc1234",
    "description": "Q4 2025 baseline",
    "graphStats": {
      "totalIssues": 140,
      "openIssues": 105,
      "blockedIssues": 15,
      "density": 0.40,
      "cycleCount": 0
    }
  }
}
```

**Exit Codes:**
- `0` = No drift or info-only
- `1` = Critical (new cycles)
- `2` = Warning (density increase, more blocked)

**Use Cases:**
- CI health checks
- Continuous monitoring
- Preventing degradation
- Alerting

**Performance:** Fast (<1s)

**Example Usage:**
```bash
# Check drift
bv --check-drift --robot-drift > drift-report.json

# Get exit code
EXIT_CODE=$(jq -r '.exitCode' drift-report.json)

# Check for critical alerts
jq '.alerts[] | select(.level == "critical")' drift-report.json

# Check density drift
jq '.alerts[] | select(.category == "density")' drift-report.json

# CI integration
bv --check-drift --robot-drift
if [ $? -eq 1 ]; then
  echo "CRITICAL: Fail build"
  exit 1
fi
```

**Configuration (`.bv/drift.yaml`):**
```yaml
densityWarningPct: 50        # Warn if density +50%
blockedIncreaseThreshold: 5   # Warn if 5+ more blocked
cycleAlertLevel: critical     # New cycles = critical
```

---

### `--baseline-info`

**View current baseline metadata**

**Command:**
```bash
bv --baseline-info
```

**Output:** Human-readable (no JSON, but parseable)

**Use Cases:**
- Verify baseline before drift check
- Audit baseline history

---

## Configuration Commands

### `--robot-recipes`

**List available filtering recipes**

**Command:**
```bash
bv --robot-recipes
```

**Output Schema:**
```json
{
  "recipes": [
    {
      "name": "actionable",
      "description": "Issues with no blockers, sorted by priority",
      "source": "builtin"
    },
    {
      "name": "high-impact",
      "description": "High PageRank or betweenness scores",
      "source": "builtin"
    },
    {
      "name": "sprint-ready",
      "description": "Custom recipe for sprint planning",
      "source": "project"
    }
  ]
}
```

**Use Cases:**
- Discovering built-in recipes
- Validating custom recipes
- Dynamic recipe selection

**Performance:** Instant

**Example Usage:**
```bash
# List all recipes
bv --robot-recipes | jq '.recipes[].name'

# Get builtin recipes
bv --robot-recipes | jq '.recipes[] | select(.source == "builtin")'

# Get project recipes
bv --robot-recipes | jq '.recipes[] | select(.source == "project")'
```

---

### `--recipe`

**Apply filtering recipe**

**Command:**
```bash
bv --recipe <name>
```

**Built-in Recipes:**
- `default` - All issues, sorted by priority
- `actionable` - No blockers, sorted by priority
- `recent` - Recently updated issues
- `blocked` - Issues with blockers
- `high-impact` - High PageRank/betweenness
- `stale` - Not updated recently

**Combine with robot commands:**
```bash
bv --recipe actionable --robot-plan
bv --recipe high-impact --robot-insights
bv --recipe blocked --robot-priority
```

**Custom Recipe (`.bv/recipes.yaml`):**
```yaml
recipes:
  - name: my-sprint
    description: Sprint-ready frontend issues
    filters:
      state: [open]
      priority:
        min: 2
      hasBlockers: false
      labels: [frontend]
    sort:
      field: priority
      order: desc
```

---

## Multi-Repository Commands

### `--workspace`

**Aggregate multiple repositories**

**Command:**
```bash
bv --workspace <config-file>
```

**Configuration (`.bv/workspace.yaml`):**
```yaml
repos:
  - name: core-api
    path: ../core-api
    prefix: api-

  - name: web-frontend
    path: ../web-frontend
    prefix: web-
```

**Example Usage:**
```bash
# View all repos
bv --workspace .bv/workspace.yaml --robot-insights

# Filter by repo
bv --workspace .bv/workspace.yaml --repo api --robot-plan
bv --workspace .bv/workspace.yaml --repo web --robot-priority

# Identify cross-repo dependencies
bv --workspace .bv/workspace.yaml --robot-insights | \
  jq '.metrics.betweenness[] | select(.score > 0.7)'
```

**Namespaced Issue IDs:** `api-issue-001`, `web-issue-002`

---

### `--repo`

**Filter by repository prefix**

**Command:**
```bash
bv --workspace <config> --repo <prefix>
```

**Example:**
```bash
bv --workspace .bv/workspace.yaml --repo api
bv --workspace .bv/workspace.yaml --repo web
```

---

## Export Commands

### `--export-md`

**Generate Markdown report**

**Command:**
```bash
bv --export-md <file>
```

**Example:**
```bash
bv --export-md report.md
bv --export-md health-report-$(date +%Y-%m-%d).md
```

**Features:**
- Mermaid.js dependency graphs
- Top metrics tables
- Cycle warnings
- Hook integration

**Skip Hooks:**
```bash
bv --export-md report.md --no-hooks
```

---

## Performance Commands

### `--force-full-analysis`

**Compute all metrics regardless of graph size**

**Command:**
```bash
bv --force-full-analysis --robot-insights
```

**Use when:**
- Comprehensive audit required
- Betweenness needed for large graphs
- CI with long timeouts

**Performance:** Can take 30s+ for very large graphs (> 5000 nodes)

---

### `--profile-startup`

**Output detailed startup timing**

**Command:**
```bash
bv --profile-startup
bv --profile-startup --profile-json
```

**Use Cases:**
- Performance diagnostics
- Identifying bottlenecks
- Monitoring system health

---

## Help Commands

### `--robot-help`

**Show AI agent help**

**Command:**
```bash
bv --robot-help
```

**Output:** Human-readable text (not JSON)

---

### `--help`

**Show general help**

**Command:**
```bash
bv --help
```

---

## Command Combinations

### Sprint Planning Workflow

```bash
# 1. Get actionable issues
bv --recipe actionable --robot-plan > sprint-plan.json

# 2. Get high-impact work
bv --robot-insights | jq '.recommendations.highImpactIssues'

# 3. Verify priorities
bv --robot-priority | jq '.recommendations[] | select(.confidence > 0.8)'
```

---

### CI Health Check Workflow

```bash
# 1. Check drift
bv --check-drift --robot-drift > drift-report.json

# 2. Check exit code
EXIT_CODE=$(jq -r '.exitCode' drift-report.json)

# 3. Fail on critical
if [ $EXIT_CODE -eq 1 ]; then
  exit 1
fi
```

---

### Refactoring Workflow

```bash
# 1. Save baseline
bv --save-baseline "Pre-refactoring - $(date +%Y-%m-%d)"

# 2. Get current metrics
bv --robot-insights > current.json

# 3. Identify targets
jq '.cycles + (.metrics.betweenness[] | select(.score > 0.7))' current.json
```

---

### Historical Analysis Workflow

```bash
# 1. Compare to last release
bv --diff-since v1.0.0 --robot-diff > release-diff.json

# 2. View historical state
bv --as-of v1.0.0 --robot-insights > release-state.json

# 3. Check health trend
jq -r '.summary.healthTrend' release-diff.json
```

---

## Quick Reference Card

```bash
# Analysis
bv --robot-insights                          # Full metrics
bv --robot-plan                              # Execution plan
bv --robot-priority                          # Priority suggestions

# Historical
bv --diff-since HEAD~10 --robot-diff         # Compare
bv --as-of v1.0.0 --robot-insights           # View past

# Drift
bv --save-baseline "description"             # Save
bv --check-drift --robot-drift               # Check

# Multi-Repo
bv --workspace .bv/workspace.yaml --robot-insights
bv --workspace .bv/workspace.yaml --repo api --robot-plan

# Filtering
bv --recipe actionable --robot-plan          # No blockers
bv --recipe high-impact --robot-insights     # High metrics

# Performance
bv --force-full-analysis --robot-insights    # All metrics
bv --profile-startup --profile-json          # Profile
```

---

## Exit Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 0 | Success | Normal operation, no drift, info-only alerts |
| 1 | Critical | New cycles detected (drift check) |
| 2 | Warning | Non-critical drift (density increase, more blocked) |
| 3+ | Error | Command failure, invalid arguments |

---

## Version

This reference is compatible with:
- **bv:** v1.0.0+
- **Robot Protocol:** v1.x (semver-stable)
