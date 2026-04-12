# Pareto-Optimal Ranking Algorithms

## Core Ranking Function

### Objective

Maximize skill relevance and diversity while minimizing redundancy and cognitive load.

### Multi-Objective Formula

```
score(skill, query, presented_skills) =
    α · relevance(skill, query)
  + β · popularity(skill.downloads)
  + γ · recency(skill.last_update)
  - δ · redundancy(skill, presented_skills)

where:
  α, β, γ, δ are weight parameters (α + β + γ = 1.0, δ independent)
```

## Component Functions

### 1. Relevance Score

**Method**: Cosine similarity between query and skill description

```python
def relevance(skill_description: str, query: str) -> float:
    """
    Calculate relevance using bag-of-words cosine similarity

    Returns: Score ∈ [0, 1]
    """
    from scripts.semantic_similarity import cosine_similarity

    score = cosine_similarity(skill_description, query)
    return score
```

**Alternative**: Keyword match count (simpler, faster)
```python
def relevance_keywords(skill_description: str, query: str) -> float:
    """
    Calculate relevance by keyword overlap

    Returns: Score ∈ [0, 1]
    """
    query_keywords = set(query.lower().split())
    desc_keywords = set(skill_description.lower().split())

    if len(query_keywords) == 0:
        return 0.0

    overlap = len(query_keywords & desc_keywords)
    return overlap / len(query_keywords)
```

### 2. Popularity Score

**Method**: Logarithmic scaling of download counts

```python
def popularity(downloads: int, max_downloads: int = 100000) -> float:
    """
    Normalize download counts using log scale

    Rationale: Difference between 100 and 1000 downloads is more significant
    than difference between 10,000 and 10,900 downloads

    Returns: Score ∈ [0, 1]
    """
    import math

    if downloads <= 0:
        return 0.0

    # Log scale with smoothing
    log_downloads = math.log(downloads + 1)
    log_max = math.log(max_downloads + 1)

    return log_downloads / log_max
```

**Example**:
```
100 downloads      → log(101) / log(100001) ≈ 0.40
1,000 downloads    → log(1001) / log(100001) ≈ 0.60
10,000 downloads   → log(10001) / log(100001) ≈ 0.80
100,000 downloads  → log(100001) / log(100001) = 1.00
```

### 3. Recency Score

**Method**: Exponential decay based on days since last update

```python
def recency(last_update_days: int, max_age: int = 365) -> float:
    """
    Score based on how recently the skill was updated

    Rationale: Recently updated skills are more likely to be maintained
    and compatible with current tooling

    Returns: Score ∈ [0, 1]
    """
    if last_update_days < 0:
        return 1.0  # Unknown update time → assume recent

    # Exponential decay: score = e^(-days / half_life)
    half_life = max_age / 2  # ~180 days for half score

    import math
    score = math.exp(-last_update_days / half_life)

    return max(0.0, min(1.0, score))
```

**Example**:
```
0 days (today)    → 1.00
30 days           → 0.90
90 days           → 0.69
180 days          → 0.50
365 days          → 0.25
730 days (2 yrs)  → 0.06
```

### 4. Redundancy Penalty

**Method**: Maximum semantic similarity with already-presented skills

```python
def redundancy(skill_description: str, presented_skills: List[str]) -> float:
    """
    Calculate redundancy as max similarity with presented skills

    Rationale: Presenting very similar skills wastes user attention

    Returns: Score ∈ [0, 1]
    """
    from scripts.semantic_similarity import cosine_similarity

    if not presented_skills:
        return 0.0  # No redundancy if nothing presented yet

    similarities = [
        cosine_similarity(skill_description, presented_desc)
        for presented_desc in presented_skills
    ]

    return max(similarities)
```

## Pareto Frontier Configurations

### Configuration 1: Balanced Discovery (Default)

**Use Case**: General skill discovery, balanced priorities

**Parameters**:
```python
α = 0.60  # Relevance (primary)
β = 0.25  # Popularity (secondary)
γ = 0.10  # Recency (tertiary)
δ = 0.05  # Redundancy penalty
```

**Characteristics**:
- Prioritizes relevance but considers popularity
- Recent updates slightly favored
- Minimal redundancy penalty (diversity not critical)

**Example Scores**:
```
Skill A: relevance=0.90, popularity=0.50, recency=0.80, redundancy=0.10
→ score = 0.60(0.90) + 0.25(0.50) + 0.10(0.80) - 0.05(0.10)
→ score = 0.54 + 0.125 + 0.08 - 0.005 = 0.74

Skill B: relevance=0.70, popularity=0.95, recency=0.60, redundancy=0.05
→ score = 0.60(0.70) + 0.25(0.95) + 0.10(0.60) - 0.05(0.05)
→ score = 0.42 + 0.238 + 0.06 - 0.0025 = 0.72

Result: Skill A ranked higher (more relevant despite less popular)
```

### Configuration 2: High Precision (Research Mode)

**Use Case**: Critical tasks requiring best-match skills

**Parameters**:
```python
α = 0.80  # Relevance (dominant)
β = 0.10  # Popularity (minor)
γ = 0.05  # Recency (minimal)
δ = 0.05  # Redundancy penalty
```

**Characteristics**:
- Heavily prioritizes relevance
- Popularity and recency less important
- Willing to accept longer search time

**Trade-offs**:
- Higher precision, potentially lower recall
- May miss popular but less-directly-relevant skills

### Configuration 3: Popularity Mode (Social Proof)

**Use Case**: User wants battle-tested, widely-used skills

**Parameters**:
```python
α = 0.30  # Relevance (reduced)
β = 0.60  # Popularity (dominant)
γ = 0.05  # Recency (minimal)
δ = 0.05  # Redundancy penalty
```

**Characteristics**:
- Prioritizes download count as quality signal
- Relevance still considered but secondary
- Surfaces "greatest hits" of skill ecosystem

**Example**:
```
Query: "testing"

Precision Mode Results:
  1. test-pattern-matcher (90% relevant, 500 downloads)
  2. tdd-workflow (85% relevant, 2k downloads)
  3. test-automation-helper (80% relevant, 800 downloads)

Popularity Mode Results:
  1. test-driven-development (70% relevant, 45k downloads)
  2. systematic-debugging (65% relevant, 13k downloads)
  3. tdd-workflow (85% relevant, 2k downloads)
```

### Configuration 4: Exploration Mode (Diversity)

**Use Case**: User browsing, wants variety of options

**Parameters**:
```python
α = 0.30  # Relevance (relaxed)
β = 0.40  # Popularity (moderate)
γ = 0.20  # Recency (favored)
δ = 0.10  # Redundancy penalty (doubled)
```

**Characteristics**:
- Balanced weights across metrics
- Higher redundancy penalty for diversity
- Favors recently updated skills (active maintenance)

**Trade-offs**:
- May present less-directly-relevant but interesting alternatives
- Good for serendipitous discovery

## Ranking Pipeline

### Step 1: Filter

Remove skills that don't meet minimum thresholds:

```python
def filter_skills(skills: List[Skill]) -> List[Skill]:
    """
    Apply minimum quality thresholds

    Filters:
    - Relevance < 0.20 (too unrelated)
    - Popularity = 0 and Recency > 730 days (abandoned)
    """
    filtered = []

    for skill in skills:
        if skill.relevance < 0.20:
            continue  # Too irrelevant

        if skill.downloads == 0 and skill.days_since_update > 730:
            continue  # Likely abandoned

        filtered.append(skill)

    return filtered
```

### Step 2: Score

Apply Pareto optimization formula:

```python
def score_skills(skills: List[Skill], query: str, config: Config) -> List[Tuple[Skill, float]]:
    """
    Calculate Pareto scores for all skills

    Returns: List of (skill, score) tuples
    """
    scored = []
    presented_descriptions = []  # Track for redundancy

    for skill in skills:
        rel = relevance(skill.description, query)
        pop = popularity(skill.downloads)
        rec = recency(skill.days_since_update)
        red = redundancy(skill.description, presented_descriptions)

        score = (config.alpha * rel +
                 config.beta * pop +
                 config.gamma * rec -
                 config.delta * red)

        scored.append((skill, score))

    return scored
```

### Step 3: Deduplicate

Remove semantically similar skills:

```python
def deduplicate_skills(scored_skills: List[Tuple[Skill, float]], threshold: float = 0.85) -> List[Tuple[Skill, float]]:
    """
    Remove semantically similar skills using semantic_similarity.py

    Keeps highest-scoring skill from each cluster
    """
    # Use scripts/semantic_similarity.py
    # Implementation in that script
    pass
```

### Step 4: Sort and Select

```python
def rank_and_select(scored_skills: List[Tuple[Skill, float]], top_n: int = 3) -> List[Skill]:
    """
    Sort by score descending and select top N

    Returns: Top N skills
    """
    sorted_skills = sorted(scored_skills, key=lambda x: x[1], reverse=True)
    top_skills = [skill for skill, score in sorted_skills[:top_n]]

    return top_skills
```

## Complete Ranking Example

### Query: "frontend debugging tools"

**Input Skills**:
```
Skill A: "Frontend debugging and developer tools"
  downloads=12000, last_update=30 days
  relevance=0.95

Skill B: "General debugging framework"
  downloads=45000, last_update=90 days
  relevance=0.60

Skill C: "Frontend development best practices"
  downloads=25000, last_update=15 days
  relevance=0.70

Skill D: "Browser debugging utilities"
  downloads=8000, last_update=60 days
  relevance=0.85
```

**Balanced Config Scores**:
```
Skill A:
  0.60(0.95) + 0.25(log(12001)/log(100001)) + 0.10(exp(-30/180)) - 0.05(0.0)
  = 0.570 + 0.199 + 0.085 - 0.0 = 0.854

Skill B:
  0.60(0.60) + 0.25(log(45001)/log(100001)) + 0.10(exp(-90/180)) - 0.05(0.0)
  = 0.360 + 0.234 + 0.069 - 0.0 = 0.663

Skill C:
  0.60(0.70) + 0.25(log(25001)/log(100001)) + 0.10(exp(-15/180)) - 0.05(0.0)
  = 0.420 + 0.218 + 0.092 - 0.0 = 0.730

Skill D:
  0.60(0.85) + 0.25(log(8001)/log(100001)) + 0.10(exp(-60/180)) - 0.05(0.0)
  = 0.510 + 0.189 + 0.075 - 0.0 = 0.774
```

**Ranking**:
```
1. Skill A (0.854) - "Frontend debugging and developer tools"
2. Skill D (0.774) - "Browser debugging utilities"
3. Skill C (0.730) - "Frontend development best practices"
4. Skill B (0.663) - "General debugging framework"
```

**Presented to User** (Top 3):
```
1. Frontend debugging and developer tools (@tools/frontend-debug) - 12k downloads
   Comprehensive debugging toolkit specifically for frontend development

2. Browser debugging utilities (@utils/browser-debug) - 8k downloads
   Specialized utilities for debugging in browser environments

3. Frontend development best practices (@guides/frontend-best) - 25k downloads
   Best practices guide including debugging strategies for frontend
```

## Dynamic Configuration Selection

Auto-select configuration based on query characteristics:

```python
def select_config(query: str, context: dict) -> Config:
    """
    Dynamically choose Pareto configuration

    Rules:
    - Specific keywords → High Precision
    - "popular" or "best" → Popularity Mode
    - "show me" or "explore" → Exploration Mode
    - Default → Balanced
    """
    query_lower = query.lower()

    if 'popular' in query_lower or 'best' in query_lower or 'top' in query_lower:
        return POPULARITY_CONFIG

    if 'explore' in query_lower or 'show' in query_lower or 'browse' in query_lower:
        return EXPLORATION_CONFIG

    # Check query specificity (number of unique keywords)
    keywords = set(query.lower().split())
    if len(keywords) >= 4:  # Very specific query
        return PRECISION_CONFIG

    return BALANCED_CONFIG  # Default
```

## Performance Metrics

- **Ranking time**: < 100ms for 50 skills
- **Relevance@3**: ≥ 0.85 (85% of top 3 results useful)
- **Diversity**: ≤ 0.85 semantic similarity between presented skills
- **User satisfaction**: ≥ 0.70 (70% install rate for presented skills)
