# Graph Analysis: Interpreting Metrics for AI Decision-Making

## Overview

This guide provides practical interpretation strategies for the 9 graph metrics computed by `bv`. Each metric reveals different aspects of project health and helps AI agents make intelligent prioritization decisions.

---

## Metric Interpretation Framework

### 1. PageRank: Blocking Power

**What it tells you:**
- How foundational an issue is
- How much downstream work depends on it
- Priority impact if completed

**Score Ranges:**

| Score | Interpretation | Action |
|-------|---------------|--------|
| **0.8-1.0** | Critical foundation | **HIGHEST PRIORITY** - unblocks massive downstream work |
| **0.6-0.8** | Important foundation | **HIGH PRIORITY** - significant blocking power |
| **0.4-0.6** | Moderate importance | **MEDIUM PRIORITY** - affects some downstream |
| **0.2-0.4** | Low importance | **LOW PRIORITY** - minimal blocking impact |
| **0.0-0.2** | Leaf/isolated | **INDEPENDENT** - can be scheduled flexibly |

**Decision Rules:**
```python
def interpret_pagerank(score: float, issue_id: str) -> str:
    if score > 0.8:
        return f"{issue_id}: CRITICAL - Highest priority (foundational)"
    elif score > 0.6:
        return f"{issue_id}: HIGH - Significant blocking power"
    elif score > 0.4:
        return f"{issue_id}: MEDIUM - Moderate importance"
    else:
        return f"{issue_id}: LOW - Minimal blocking impact"
```

**Example:**
```json
{
  "issueId": "auth-service-001",
  "score": 0.92,
  "interpretation": "foundational"
}
```
**Recommendation:** "Prioritize immediately - 12 features depend on auth service"

---

### 2. Betweenness: Bottleneck Status

**What it tells you:**
- How much this issue bridges different work streams
- Integration point detection
- Cross-team coordination needs

**Score Ranges:**

| Score | Interpretation | Action |
|-------|---------------|--------|
| **0.8-1.0** | Critical bottleneck | **URGENT** - blocks multiple independent streams |
| **0.6-0.8** | Significant bridge | **HIGH PRIORITY** - connects important clusters |
| **0.4-0.6** | Moderate connector | **MEDIUM PRIORITY** - some bridging role |
| **0.2-0.4** | Minor connector | **LOW PRIORITY** - limited bridging |
| **0.0-0.2** | Not a bottleneck | **NORMAL** - no special coordination needed |

**Decision Rules:**
```python
def interpret_betweenness(score: float, pagerank: float) -> str:
    if score > 0.8 and pagerank > 0.7:
        return "CRITICAL BOTTLENECK - highest priority"
    elif score > 0.8:
        return "INTEGRATION POINT - requires coordination"
    elif score > 0.6:
        return "BRIDGE ISSUE - connects work streams"
    else:
        return "NORMAL - no special bottleneck status"
```

**Example:**
```json
{
  "issueId": "api-gateway-012",
  "score": 0.89,
  "interpretation": "critical_bridge"
}
```
**Recommendation:** "Critical integration point - frontend, mobile, and backend all depend on this"

---

### 3. HITS: Hub vs Authority

**What it tells you:**
- **Authority:** How many issues depend on this (foundational)
- **Hub:** How many issues this depends on (integration)
- Nature of dependency relationships

**Interpretation Matrix:**

| Authority | Hub | Interpretation | Action |
|-----------|-----|---------------|--------|
| **High** | **Low** | Pure foundation | **Prioritize early** - many depend on it |
| **High** | **High** | Central coordinator | **Prioritize + coordinate** - complex dependencies |
| **Low** | **High** | Integration sink | **Requires coordination** - many inputs needed |
| **Low** | **Low** | Isolated/leaf | **Flexible scheduling** - independent work |

**Decision Rules:**
```python
def interpret_hits(authority: float, hub: float) -> tuple[str, str]:
    dominant = "authority" if authority > hub else "hub" if hub > authority else "balanced"

    if authority > 0.7 and hub < 0.3:
        return ("FOUNDATIONAL", "Prioritize early - many depend on this")
    elif authority > 0.7 and hub > 0.7:
        return ("CENTRAL COORDINATOR", "High priority + careful coordination")
    elif authority < 0.3 and hub > 0.7:
        return ("INTEGRATION POINT", "Requires many inputs - coordinate carefully")
    else:
        return ("BALANCED", "Normal scheduling")
```

**Example:**
```json
{
  "issueId": "database-schema-003",
  "hubScore": 0.12,
  "authorityScore": 0.91,
  "dominantRole": "authority"
}
```
**Recommendation:** "Pure foundation - 18 features depend on this schema"

---

### 4. Critical Path: Chain Depth

**What it tells you:**
- How deep in a sequential chain this issue sits
- Length of dependent work if delayed
- Sequential vs parallelizable nature

**Score Ranges:**

| Score | Interpretation | Action |
|-------|---------------|--------|
| **15+** | Very deep chain | **HIGHEST PRIORITY** - blocks long sequence |
| **10-15** | Deep chain | **HIGH PRIORITY** - significant sequential work |
| **5-10** | Moderate chain | **MEDIUM PRIORITY** - some sequential dependencies |
| **1-5** | Shallow chain | **LOW PRIORITY** - near leaves or roots |
| **0** | Root or leaf | **FLEXIBLE** - no sequential constraints |

**Decision Rules:**
```python
def interpret_critical_path(score: int, pagerank: float) -> str:
    if score > 15 and pagerank > 0.7:
        return "CRITICAL PATH - must do first"
    elif score > 15:
        return "LONG CHAIN - high sequential impact (but isolated)"
    elif score > 10:
        return "SIGNIFICANT CHAIN - prioritize to unblock sequence"
    else:
        return "SHORT CHAIN - normal priority"
```

**Example:**
```json
{
  "issueId": "migration-007",
  "score": 18,
  "depthBlocking": 15
}
```
**Recommendation:** "Blocks 15 sequential steps - critical path bottleneck"

---

### 5. Eigenvector: Network Influence

**What it tells you:**
- Importance based on importance of neighbors
- Quality of connections (not just quantity)
- Network position in dependency graph

**Score Ranges:**

| Score | Interpretation | Action |
|-------|---------------|--------|
| **0.8-1.0** | Highly influential | **HIGH PRIORITY** - connected to other critical issues |
| **0.6-0.8** | Influential | **MEDIUM-HIGH PRIORITY** - good network position |
| **0.4-0.6** | Moderate influence | **MEDIUM PRIORITY** - normal network position |
| **0.0-0.4** | Low influence | **LOW PRIORITY** - peripheral or isolated |

**Decision Rules:**
```python
def interpret_eigenvector(score: float, degree: int) -> str:
    if score > 0.7 and degree > 10:
        return "CENTRAL HUB - high priority (quality + quantity)"
    elif score > 0.7 and degree < 5:
        return "STRATEGIC POSITION - high priority (quality over quantity)"
    elif score > 0.5:
        return "MODERATE INFLUENCE - normal priority"
    else:
        return "LOW INFLUENCE - flexible scheduling"
```

**Example:**
```json
{
  "issueId": "core-api-design-002",
  "score": 0.85,
  "influenceLevel": "high_influence"
}
```
**Recommendation:** "Connected to other critical architectural decisions - coordinate carefully"

---

### 6. Degree Centrality: Connection Count

**What it tells you:**
- Simple count of dependencies
- In-degree: how many depend on this
- Out-degree: how many this depends on

**Interpretation:**

| Metric | Range | Interpretation | Action |
|--------|-------|---------------|--------|
| **In-Degree** | **10+** | Many dependents | **HIGH PRIORITY** - unblocks many |
| **In-Degree** | **5-10** | Several dependents | **MEDIUM PRIORITY** - unblocks some |
| **In-Degree** | **0-5** | Few dependents | **LOW PRIORITY** - minimal blocking |
| **Out-Degree** | **10+** | Many dependencies | **COORDINATE** - requires many inputs |
| **Out-Degree** | **0** | No dependencies | **PARALLELIZABLE** - can start anytime |

**Decision Rules:**
```python
def interpret_degree(in_degree: int, out_degree: int) -> str:
    if in_degree > 10:
        return "HIGH BLOCKING POWER - prioritize to unblock many"
    elif out_degree > 10:
        return "INTEGRATION POINT - coordinate inputs carefully"
    elif in_degree == 0 and out_degree == 0:
        return "ISOLATED - work independently anytime"
    else:
        return "NORMAL - standard prioritization"
```

**Example:**
```json
{
  "issueId": "shared-utils-005",
  "inDegree": 27,
  "outDegree": 3,
  "totalDegree": 30
}
```
**Recommendation:** "27 issues depend on this - very high blocking power"

---

### 7. Graph Density: Coupling Measure

**What it tells you:**
- Overall graph interconnection level
- Architectural coupling health
- Modularization opportunities

**Density Ranges:**

| Density | Interpretation | Health | Action |
|---------|---------------|--------|--------|
| **0.0-0.3** | Sparse | **HEALTHY** | Modular, loosely coupled - maintain |
| **0.3-0.5** | Balanced | **GOOD** | Reasonable interconnection - monitor |
| **0.5-0.7** | Dense | **WARNING** | High coupling - consider modularization |
| **0.7-0.9** | Very dense | **CRITICAL** | Over-coupled - refactoring needed |
| **0.9-1.0** | Extremely dense | **EMERGENCY** | Architectural crisis - major refactor |

**Decision Rules:**
```python
def interpret_density(density: float, cycle_count: int) -> str:
    if density > 0.8:
        return "CRITICAL: Over-coupled architecture - major refactor needed"
    elif density > 0.6:
        return "WARNING: High coupling - identify modularization opportunities"
    elif density > 0.4:
        return "BALANCED: Reasonable interconnection - monitor trends"
    else:
        return "HEALTHY: Sparse, modular structure - maintain"
```

**Example:**
```json
{
  "density": 0.72,
  "interpretation": "dense"
}
```
**Recommendation:** "High coupling detected - prioritize breaking dependencies and modularization"

---

### 8. Cycles: Circular Dependencies

**What it tells you:**
- Presence of circular dependencies
- Architectural health problems
- Blocking execution plan generation

**Interpretation:**

| Cycle Count | Severity | Health | Action |
|-------------|----------|--------|--------|
| **0** | None | **HEALTHY** | Valid DAG - can generate execution plan |
| **1-2** | Low | **WARNING** | Design errors - break cycles |
| **3-5** | Medium | **CRITICAL** | Architectural issues - urgent refactoring |
| **6+** | High | **EMERGENCY** | Major architectural debt - stop new work |

**Cycle Length Impact:**

| Length | Severity | Action |
|--------|----------|--------|
| **2** | Usually design error | Break by removing one dependency |
| **3-4** | Tight coupling | Identify least critical edge to break |
| **5+** | Architectural problem | May require module extraction |

**Decision Rules:**
```python
def interpret_cycles(cycles: list, topological_valid: bool) -> str:
    if len(cycles) == 0:
        return "HEALTHY: No cycles - valid DAG"
    elif len(cycles) <= 2:
        return f"WARNING: {len(cycles)} cycle(s) - break dependencies"
    elif len(cycles) <= 5:
        return f"CRITICAL: {len(cycles)} cycles - urgent refactoring needed"
    else:
        return f"EMERGENCY: {len(cycles)} cycles - stop new work, fix architecture"
```

**Example:**
```json
{
  "path": ["feature-A-001", "feature-B-002", "feature-C-003", "feature-A-001"],
  "length": 3,
  "severity": "critical"
}
```
**Recommendation:** "Break cycle: feature-A → feature-B → feature-C → feature-A"

---

### 9. Topological Sort: Valid Execution Order

**What it tells you:**
- Whether a valid linear execution order exists
- Ability to generate dependency-respecting plan
- Overall graph health

**Interpretation:**

| Valid? | Cycles? | Health | Action |
|--------|---------|--------|--------|
| **true** | 0 | **HEALTHY** | Can generate execution plan |
| **false** | 1+ | **BLOCKED** | Must resolve cycles first |

**Decision Rules:**
```python
def interpret_topological_sort(is_valid: bool, order: list, cycles: list) -> str:
    if is_valid:
        return f"VALID: Can execute in order (topological sort of {len(order)} issues)"
    else:
        return f"INVALID: {len(cycles)} cycle(s) prevent valid ordering - must break cycles"
```

**Example:**
```json
{
  "order": ["core-001", "api-002", "feature-003"],
  "isValid": true
}
```
**Recommendation:** "Valid execution order - work on issues in this sequence"

---

## Combined Metric Analysis

### Priority Decision Matrix

Use multiple metrics together for intelligent prioritization:

```python
def calculate_priority(
    pagerank: float,
    betweenness: float,
    critical_path: int,
    in_degree: int,
    cycles: list
) -> tuple[int, str]:
    """
    Returns (priority, reasoning)
    Priority: 1 (highest) to 5 (lowest)
    """

    # Check if in cycle (highest priority)
    if any(issue_id in cycle['path'] for cycle in cycles):
        return (1, "CRITICAL: Part of circular dependency - break cycle")

    # Critical bottleneck
    if pagerank > 0.8 and betweenness > 0.8 and critical_path > 10:
        return (1, "CRITICAL: Blocks everything - highest priority")

    # Foundational work
    if pagerank > 0.7 and in_degree > 10:
        return (2, "HIGH: Foundational - unblocks many issues")

    # Integration point
    if betweenness > 0.7:
        return (2, "HIGH: Critical bridge between work streams")

    # Long chain
    if critical_path > 15:
        return (2, "HIGH: Blocks long sequential chain")

    # Moderate importance
    if pagerank > 0.5 or in_degree > 5:
        return (3, "MEDIUM: Moderate blocking power")

    # Low priority or isolated
    if pagerank < 0.3 and in_degree < 3:
        return (5, "LOW: Minimal blocking impact - flexible scheduling")

    return (4, "NORMAL: Standard priority")
```

---

### Health Score Calculation

```python
def calculate_health_score(insights: dict) -> int:
    """
    Returns health score 0-100
    100 = perfect health
    0 = critical issues
    """
    score = 100

    # Deduct for cycles (15 points each)
    cycle_count = len(insights['cycles'])
    score -= cycle_count * 15

    # Deduct for high density
    density = insights['graphStats']['density']['density']
    if density > 0.8:
        score -= 25
    elif density > 0.6:
        score -= 15
    elif density > 0.4:
        score -= 5

    # Deduct for bottlenecks (5 points each)
    bottlenecks = [m for m in insights['metrics']['betweenness'] if m['score'] > 0.8]
    score -= len(bottlenecks) * 5

    # Deduct for invalid topological sort
    if not insights['topologicalSort']['isValid']:
        score -= 20

    return max(0, score)
```

**Interpretation:**
- **90-100:** Excellent health
- **80-89:** Good health
- **70-79:** Fair health (some issues)
- **60-69:** Poor health (multiple issues)
- **< 60:** Critical health (immediate action needed)

---

### Team Allocation Strategy

```python
def allocate_work(plan: dict, team_sizes: dict) -> dict:
    """
    Allocate work based on metrics and team skill levels
    """
    all_items = [item for track in plan['tracks'] for item in track['items']]

    # Senior engineers: high impact + coordination needed
    senior_work = [
        item for item in all_items
        if item['impactScore'] > 0.7 or len(item['unblocks']) > 5
    ][:team_sizes['senior']]

    # Mid-level engineers: unblocking work
    mid_work = [
        item for item in all_items
        if 0.5 <= item['impactScore'] <= 0.7 and len(item['unblocks']) > 0
    ][:team_sizes['mid']]

    # Junior engineers: quick wins (no dependencies)
    junior_work = [
        item for item in all_items
        if len(item['dependencies']) == 0 and item['impactScore'] < 0.5
    ][:team_sizes['junior']]

    return {
        'senior': senior_work,
        'mid': mid_work,
        'junior': junior_work
    }
```

---

## Trend Analysis

### Tracking Metrics Over Time

```python
def analyze_trend(current: dict, baseline: dict) -> dict:
    """
    Compare current metrics to baseline for trend analysis
    """
    return {
        'density_change': {
            'from': baseline['graphStats']['density']['density'],
            'to': current['graphStats']['density']['density'],
            'delta': current['graphStats']['density']['density'] - baseline['graphStats']['density']['density'],
            'trend': 'improving' if current['graphStats']['density']['density'] < baseline['graphStats']['density']['density'] else 'degrading'
        },
        'cycle_change': {
            'from': len(baseline['cycles']),
            'to': len(current['cycles']),
            'delta': len(current['cycles']) - len(baseline['cycles']),
            'trend': 'improving' if len(current['cycles']) < len(baseline['cycles']) else 'degrading'
        },
        'health_change': {
            'from': calculate_health_score(baseline),
            'to': calculate_health_score(current),
            'delta': calculate_health_score(current) - calculate_health_score(baseline)
        }
    }
```

---

## Red Flags

### Critical Warning Signs

1. **New Cycles Introduced**
   - Immediate action required
   - Stop new work until resolved
   - Identify least critical edge to break

2. **Density > 0.7**
   - Over-coupled architecture
   - Recommend modularization
   - Review high-betweenness issues for extraction

3. **Multiple Bottlenecks (Betweenness > 0.8)**
   - Serial bottlenecks forming
   - Extract to separate modules/services
   - Parallelize work streams

4. **Invalid Topological Sort**
   - Cycles prevent execution plan
   - Must resolve before other work
   - Use cycle paths to identify breaks

5. **High Priority Misalignments (Confidence > 0.9)**
   - Critical issues under-prioritized
   - Review priority recommendations
   - Re-plan sprint/quarter

---

## Quick Reference

### Metric Priority for Different Goals

**Sprint Planning:**
1. PageRank (foundational work)
2. Degree (in-degree for unblocking)
3. Cycles (must break first)

**Architectural Refactoring:**
1. Cycles (break first)
2. Betweenness (extract bottlenecks)
3. Density (modularization opportunities)

**Team Allocation:**
1. Impact Score (combined metrics)
2. Dependencies (coordination needs)
3. Unblocks (unlocking potential)

**Health Monitoring:**
1. Cycles (critical issues)
2. Density (coupling trends)
3. Topological Sort (valid ordering)

---

## Tools & Scripts

### JQ Helpers

```bash
# Extract high-impact issues (PageRank > 0.7)
jq '.metrics.pageRank[] | select(.score > 0.7)' insights.json

# Find bottlenecks (Betweenness > 0.8)
jq '.metrics.betweenness[] | select(.score > 0.8)' insights.json

# Get issues in cycles
jq '.cycles[].path[]' insights.json | sort -u

# Calculate average density
jq '.graphStats.density.density' insights.json

# Count high-confidence priority adjustments
jq '[.recommendations[] | select(.confidence > 0.8)] | length' priority.json
```

---

## Version Compatibility

This guide is compatible with:
- **bv:** v1.0.0+
- **Robot Protocol:** v1.x
