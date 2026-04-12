# bv Quick Command Reference

## 🚀 Core Commands

```bash
# Analysis
bv --robot-insights              # Full metrics (9 dimensions)
bv --robot-plan                  # Execution plan
bv --robot-priority              # Priority recommendations

# Historical
bv --diff-since HEAD~10 --robot-diff      # Compare to 10 commits ago
bv --diff-since v1.0.0 --robot-diff       # Compare to tag
bv --diff-since 2025-11-01 --robot-diff   # Compare to date

# Drift Detection
bv --save-baseline "description"          # Save current state
bv --check-drift --robot-drift            # Check for drift
bv --baseline-info                        # View baseline

# Multi-Repo
bv --workspace .bv/workspace.yaml --robot-insights   # All repos
bv --workspace .bv/workspace.yaml --repo api --robot-plan

# Filtering
bv --recipe actionable --robot-plan       # No blockers
bv --recipe high-impact --robot-insights  # High metrics
```

---

## 📊 Metric Quick Reference

| Metric | Range | Meaning | High Score = |
|--------|-------|---------|-------------|
| **PageRank** | 0.0-1.0 | Blocking power | Foundational (>0.7) |
| **Betweenness** | 0.0-1.0 | Bottleneck | Bridge (>0.8) |
| **HITS Authority** | 0.0-1.0 | Depended upon | Foundation (>0.7) |
| **HITS Hub** | 0.0-1.0 | Depends on many | Integration (>0.7) |
| **Critical Path** | 0-20+ | Chain depth | Long chain (>15) |
| **Eigenvector** | 0.0-1.0 | Network influence | Influential (>0.7) |
| **In-Degree** | 0-100+ | Dependents | High blocking (>10) |
| **Out-Degree** | 0-100+ | Dependencies | Integration (>10) |
| **Density** | 0.0-1.0 | Coupling | Over-coupled (>0.7) |

---

## 🎯 Decision Matrix

### Priority Recommendations

| Metrics | Interpretation | Priority |
|---------|---------------|----------|
| PageRank >0.8 + Betweenness >0.8 + CriticalPath >10 | **Critical Bottleneck** | 1 (HIGHEST) |
| PageRank >0.7 + InDegree >10 | **Foundational** | 2 (HIGH) |
| Betweenness >0.8 | **Bridge Issue** | 2 (HIGH) |
| CriticalPath >15 | **Long Chain** | 2 (HIGH) |
| Part of Cycle | **Circular Dependency** | 1 (CRITICAL) |
| InDegree = 0 + OutDegree = 0 | **Isolated** | 5 (FLEXIBLE) |

### Health Indicators

| Density | Cycles | Interpretation | Action |
|---------|--------|---------------|--------|
| < 0.3 | 0 | **HEALTHY** | Maintain modularity |
| 0.3-0.5 | 0-1 | **GOOD** | Monitor trends |
| 0.5-0.7 | 2-3 | **WARNING** | Consider modularization |
| > 0.7 | 4+ | **CRITICAL** | Urgent refactoring |

---

## 🔍 JQ Helpers

```bash
# Extract Data
bv --robot-insights | jq '.recommendations.highImpactIssues'
bv --robot-plan | jq '.summary.recommendedNextIssue'
bv --robot-priority | jq '.recommendations[] | select(.confidence > 0.8)'

# Filter by Metrics
bv --robot-insights | jq '.metrics.pageRank[] | select(.score > 0.7)'
bv --robot-insights | jq '.metrics.betweenness[] | select(.score > 0.8)'
bv --robot-insights | jq '.metrics.degree[] | select(.inDegree > 10)'

# Health Checks
bv --robot-insights | jq '.cycles | length'                    # Count cycles
bv --robot-insights | jq '.graphStats.density.interpretation'  # Density status
bv --robot-insights | jq '.topologicalSort.isValid'            # Valid ordering?
bv --check-drift --robot-drift | jq '.exitCode'                # Drift status

# Diff Analysis
bv --diff-since HEAD~10 --robot-diff | jq '.summary.healthTrend'
bv --diff-since v1.0.0 --robot-diff | jq '.changes.newCycles | length'
```

---

## 📋 Common Workflows

### Sprint Planning
```bash
# 1. Get actionable issues
bv --recipe actionable --robot-plan > sprint.json

# 2. Extract high-impact work
jq '.tracks[].items[] | select(.impactScore > 0.7)' sprint.json

# 3. Find quick wins
jq '.tracks[].items[] | select(.dependencies | length == 0)' sprint.json
```

### CI Health Check
```bash
# 1. Check drift
bv --check-drift --robot-drift > drift.json

# 2. Extract exit code
EXIT_CODE=$(jq -r '.exitCode' drift.json)

# 3. Fail on critical
if [ $EXIT_CODE -eq 1 ]; then exit 1; fi
```

### Refactoring Analysis
```bash
# 1. Save baseline
bv --save-baseline "Pre-refactor $(date +%Y-%m-%d)"

# 2. Get current metrics
bv --robot-insights > current.json

# 3. Identify targets (cycles + bottlenecks)
jq '.cycles + (.metrics.betweenness[] | select(.score > 0.7))' current.json
```

---

## 🔧 Configuration Files

### Workspace (`.bv/workspace.yaml`)
```yaml
repos:
  - name: api
    path: ../api
    prefix: api-
  - name: web
    path: ../web
    prefix: web-
```

### Recipes (`.bv/recipes.yaml`)
```yaml
recipes:
  - name: sprint-ready
    filters:
      state: [open]
      priority: { min: 2 }
      hasBlockers: false
    sort:
      field: priority
      order: desc
```

### Drift Config (`.bv/drift.yaml`)
```yaml
densityWarningPct: 50
blockedIncreaseThreshold: 5
cycleAlertLevel: critical
```

### Hooks (`.bv/hooks.yaml`)
```yaml
preExport:
  - name: validate
    command: ./scripts/validate.sh
postExport:
  - name: notify
    command: ./scripts/notify-slack.sh
```

---

## 🚦 Exit Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| **0** | Success / No drift | Normal operation |
| **1** | Critical | New cycles detected |
| **2** | Warning | Metrics degraded |
| **3+** | Error | Command failure |

---

## 🎨 Built-in Recipes

| Recipe | Description |
|--------|-------------|
| `default` | All issues, sorted by priority |
| `actionable` | No blockers, can start now |
| `recent` | Recently updated |
| `blocked` | Has blocking dependencies |
| `high-impact` | High PageRank/Betweenness |
| `stale` | Not updated recently |

---

## 💡 Pro Tips

### Performance
```bash
# Force all metrics (slow for large graphs)
bv --force-full-analysis --robot-insights

# Profile startup
bv --profile-startup --profile-json
```

### Team Allocation
- **Senior:** impactScore > 0.7
- **Mid-level:** unblocks.length > 0, impactScore 0.5-0.7
- **Junior:** dependencies.length = 0, impactScore < 0.5

### Priority Validation
```bash
# Check misalignments (confidence > 0.8)
bv --robot-priority | jq '[.recommendations[] | select(.confidence > 0.8)] | length'
```

### Health Score Formula
```python
score = 100
score -= cycles * 15
score -= (density > 0.7 ? 20 : density > 0.5 ? 10 : 0)
score -= bottlenecks * 5
```

---

## 📚 File Locations

| File | Purpose |
|------|---------|
| `.beads/` | Issue tracker data |
| `.bv/workspace.yaml` | Multi-repo config |
| `.bv/recipes.yaml` | Custom recipes |
| `.bv/drift.yaml` | Drift thresholds |
| `.bv/hooks.yaml` | Export hooks |
| `.bv/baseline.json` | Saved baseline |

---

## 🔗 Key Resources

- **Skill:** `/Users/mikhail/Downloads/architect/bv/SKILL.md`
- **Types:** `/Users/mikhail/Downloads/architect/bv-codebase/types/core.ts`
- **Metrics Guide:** `/Users/mikhail/Downloads/architect/bv-codebase/principles/graph-metrics.md`
- **Robot Protocol:** `/Users/mikhail/Downloads/architect/bv-codebase/principles/robot-protocol.md`
- **Workflows:** `/Users/mikhail/Downloads/architect/bv-codebase/templates/analysis-workflow.md`

---

## ⚡ One-Liners

```bash
# Next action recommendation
bv --robot-plan | jq -r '.summary.recommendedNextIssue'

# Health trend (improving/degrading/stable)
bv --diff-since HEAD~10 --robot-diff | jq -r '.summary.healthTrend'

# Count critical issues (cycles + high PageRank)
bv --robot-insights | jq '(.cycles | length) + ([.metrics.pageRank[] | select(.score > 0.8)] | length)'

# Top 5 bottlenecks
bv --robot-insights | jq '.metrics.betweenness | sort_by(.score) | reverse | .[0:5]'

# Issues ready to work on now
bv --recipe actionable --robot-plan | jq '.tracks[].items[] | select(.canStartNow == true) | .issueId'

# Priority misalignments (should increase)
bv --robot-priority | jq '.recommendations[] | select(.direction == "increase" and .confidence > 0.8)'
```

---

## 🚨 Critical Rules

1. **NEVER run `bv` without `--robot-*` flags** (will launch TUI)
2. **ALWAYS parse JSON safely** (check for `.error` field)
3. **ALWAYS break cycles first** (before other work)
4. **ALWAYS save baseline before refactoring** (enables drift detection)
5. **ALWAYS check exit codes in CI** (0=success, 1=critical, 2=warning)

---

**Version:** bv v1.0.0+ | Robot Protocol v1.x
