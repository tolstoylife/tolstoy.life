# LEANN Indexing Patterns

## When to Index What

This guide helps you decide **when to create/update indexes** and **what to include** based on project characteristics.

---

## Decision Matrix

### By Codebase Size

| Files | Recommended Action | Anchor Count | Backend | Rationale |
|-------|-------------------|--------------|---------|-----------|
| <1K | Skip LEANN, use simple vector DB | N/A | N/A | Overhead not worth it |
| 1K-10K | Standard indexing | 100-300 | HNSW | Sweet spot for LEANN |
| 10K-100K | Production indexing | 300-1K | HNSW | Significant storage savings |
| 100K-1M | Enterprise indexing | 1K-10K | HNSW | Still fits in RAM |
| 1M+ | Massive-scale indexing | 10K-50K | DiskANN | Exceeds RAM, use disk |

### By Update Frequency

| Update Pattern | Strategy | Configuration | CI/CD Integration |
|----------------|----------|---------------|-------------------|
| Static (no updates) | One-time index | `incremental: false` | None needed |
| Rare (monthly) | Scheduled rebuild | `rebuildSchedule: "0 2 1 * *"` | Monthly job |
| Regular (weekly) | Delta + rebuild | `rebuildSchedule: "0 2 * * 0"` | Weekly rebuild |
| Frequent (daily) | Delta index | `deltaIndexThreshold: 1000` | Git hook |
| Real-time (on commit) | Watch mode | `watchMode: true` | Pre-commit hook |

### By Codebase Diversity

| Diversity | Languages | Strategy | Example Config |
|-----------|-----------|----------|----------------|
| Homogeneous | 1 language | Random anchors | `{"type": "random", "count": 300}` |
| Low | 1-2 languages, similar patterns | K-means | `{"type": "kmeans", "clusters": 300}` |
| Medium | 2-4 languages | Stratified k-means | `{"type": "stratified-kmeans", "groupBy": "language"}` |
| High | 5+ languages, varied patterns | Max-coverage | `{"type": "max-coverage", "diversityThreshold": 0.2}` |

### By Query Pattern

| Query Type | Index Configuration | Re-ranking | Notes |
|------------|---------------------|------------|-------|
| Exploratory (broad) | `efSearch: 200` | No | Find many candidates |
| Precise (narrow) | `efSearch: 50` | Yes | Use cross-encoder |
| Real-time (IDE) | `efSearch: 100`, `complexity: medium` | No | Balance speed/accuracy |
| Batch (analytics) | `efSearch: 500` | Optional | Accuracy over latency |

---

## Common Patterns

### Pattern 1: Monorepo with Multiple Services

**Scenario:**
- 50K files across 10 microservices
- Each service is ~5K files
- Services updated independently

**Strategy:** Service-level sharding

```bash
# Index each service independently
for service in service-a service-b service-c; do
  leann index create \
    --config leann.config.json \
    --input "./services/$service" \
    --output "./leann-$service.index" &
done
wait

# Query across all services
leann query \
  --indexes ./leann-*.index \
  --query "authentication middleware" \
  --top-k 10
```

**Benefits:**
- Parallel indexing (4-8× faster)
- Independent updates (only rebuild changed services)
- Service-scoped queries (filter by service)

**Configuration:**
```json
{
  "backend": "hnsw",
  "complexity": "medium",
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 100
  },
  "incremental": {
    "enabled": true,
    "deltaIndexThreshold": 500
  }
}
```

---

### Pattern 2: Polyglot Codebase (Python + TypeScript + Go)

**Scenario:**
- 30K files: 50% Python, 30% TypeScript, 20% Go
- Want balanced representation of all languages

**Strategy:** Language-aware stratification

```json
{
  "backend": "hnsw",
  "complexity": "medium",
  "anchorSelection": {
    "type": "stratified-kmeans",
    "totalClusters": 500,
    "stratification": {
      "enabled": true,
      "groupBy": "language",
      "minPerGroup": 30,
      "allocation": "proportional"
    }
  },
  "filters": {
    "languages": ["python", "typescript", "go"],
    "excludePaths": [
      "node_modules/",
      "__pycache__/",
      "vendor/",
      "*.pyc",
      "*.test.ts"
    ]
  }
}
```

**Anchor Allocation:**
```
Total: 500 anchors
Python (50%):     250 anchors
TypeScript (30%): 150 anchors
Go (20%):         100 anchors (boosted from minimum 30)
```

**Query Example:**
```bash
# Language-filtered query
leann query \
  --index ./leann.index \
  --query "rate limiting middleware" \
  --filters '{"languages": ["typescript", "go"]}' \
  --top-k 5
```

---

### Pattern 3: Documentation + Code (Mixed Content)

**Scenario:**
- 10K code files + 2K markdown docs
- Want code and docs indexed together
- Docs should have higher weight in results

**Strategy:** Weighted embedding with document boosting

```json
{
  "backend": "hnsw",
  "complexity": "medium",
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 400,
    "stratification": {
      "enabled": true,
      "groupBy": "type",
      "allocation": {
        "code": 300,
        "documentation": 100
      }
    }
  },
  "embeddingServer": {
    "endpoint": "tcp://localhost:5555",
    "model": "sentence-transformers/all-mpnet-base-v2",
    "batchSize": 128,
    "timeout": 30000
  },
  "scoring": {
    "typeWeights": {
      "documentation": 1.5,
      "code": 1.0
    }
  }
}
```

**Use Case:**
```bash
# Query documentation primarily
leann query \
  --index ./leann.index \
  --query "how to implement authentication" \
  --filters '{"types": ["documentation", "code"]}' \
  --top-k 10
```

---

### Pattern 4: CI/CD with Incremental Updates

**Scenario:**
- Production index deployed to search API
- Need real-time updates on every commit
- Minimize rebuild time

**Strategy:** Delta index + scheduled weekly rebuild

**Configuration:**
```json
{
  "backend": "hnsw",
  "complexity": "medium",
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 300
  },
  "incremental": {
    "enabled": true,
    "deltaIndexThreshold": 1000,
    "rebuildSchedule": "0 2 * * 0",
    "gitIntegration": {
      "enabled": true,
      "trackBranch": "main",
      "pollInterval": 300
    }
  }
}
```

**CI Pipeline:**
```yaml
# .github/workflows/update-index.yml
name: Update LEANN Index

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * 0'

jobs:
  update-index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Incremental Update
        run: |
          leann index update \
            --index ./leann.index \
            --git-diff origin/main~1 HEAD \
            --output ./leann-updated.index

      - name: Validate
        run: |
          leann index validate ./leann-updated.index
          if [ $? -ne 0 ]; then
            # Validation failed - full rebuild
            leann index create \
              --config leann.config.json \
              --input . \
              --output ./leann-updated.index
          fi

      - name: Deploy to API
        run: |
          aws s3 cp ./leann-updated.index s3://search-api/leann.index
          # Trigger API restart to reload index
```

---

### Pattern 5: IDE Integration (Live Updates)

**Scenario:**
- Developer wants semantic search in IDE
- Index should update automatically on file save
- Queries should be <20ms

**Strategy:** Watch mode with in-memory delta

```bash
# Start LEANN server with watch mode
leann serve \
  --index ~/.cache/leann/project.index \
  --watch \
  --port 8080 \
  --auto-update \
  --log-level info

# IDE extension makes HTTP requests
# Query endpoint: http://localhost:8080/query
```

**IDE Extension Example (TypeScript):**
```typescript
import axios from 'axios';

export class LEANNSearchProvider {
  private baseUrl = 'http://localhost:8080';

  async search(query: string, topK: number = 10) {
    const response = await axios.post(`${this.baseUrl}/query`, {
      query,
      topK,
      filters: {
        languages: ['typescript', 'javascript'],
        paths: ['src/**/*']
      }
    });

    return response.data.results.map(r => ({
      path: r.item.path,
      score: r.score,
      preview: r.preview,
      startLine: r.item.startLine
    }));
  }
}
```

**VS Code Integration:**
```json
{
  "contributes": {
    "commands": [
      {
        "command": "leann.search",
        "title": "LEANN: Semantic Search"
      }
    ],
    "keybindings": [
      {
        "command": "leann.search",
        "key": "ctrl+shift+f",
        "mac": "cmd+shift+f"
      }
    ]
  }
}
```

---

### Pattern 6: Migration from Vector Database

**Scenario:**
- Currently using Pinecone with 50K embeddings
- Monthly cost: $70
- Want to migrate to LEANN (zero cost)

**Strategy:** Export → Import → A/B Test

**Step 1: Export from Pinecone**
```python
import pinecone
import json

pinecone.init(api_key="...")
index = pinecone.Index("codebase")

# Fetch all vectors
embeddings = []
for ids_batch in fetch_all_ids(index, batch_size=1000):
    vectors = index.fetch(ids_batch)
    for id, data in vectors['vectors'].items():
        embeddings.append({
            'id': id,
            'embedding': data['values'],
            'metadata': data['metadata']
        })

# Save to JSONL
with open('embeddings.jsonl', 'w') as f:
    for item in embeddings:
        f.write(json.dumps(item) + '\n')
```

**Step 2: Import to LEANN**
```bash
leann index import \
  --embeddings embeddings.jsonl \
  --config leann.config.json \
  --output ./leann.index \
  --format jsonl

# Validate
leann index validate ./leann.index
```

**Step 3: A/B Test Queries**
```python
import requests

test_queries = [
    "JWT authentication",
    "database connection pooling",
    "error handling middleware"
]

for query in test_queries:
    # Pinecone
    pinecone_results = index.query(
        vector=embed(query),
        top_k=10,
        include_metadata=True
    )

    # LEANN
    leann_results = requests.post('http://localhost:8080/query', json={
        'query': query,
        'topK': 10
    }).json()

    # Compare
    overlap = compute_overlap(pinecone_results, leann_results)
    print(f"Query: {query}")
    print(f"Overlap: {overlap}% (target: >80%)")
    print(f"Latency: Pinecone={pinecone_results['latency']}ms, "
          f"LEANN={leann_results['latency']}ms")
```

**Expected Results:**
- Overlap: 85-95%
- Latency: LEANN 50-70% faster (local vs network)
- Cost: $70/month → $0/month (100% savings)
- Storage: 307 MB → 12.6 MB (95.9% reduction)

---

### Pattern 7: Academic Research (Paper Corpus)

**Scenario:**
- 100K academic papers (PDFs)
- Need to index abstracts + full text
- Query: "transformer architecture for NLP"

**Strategy:** Two-level indexing (coarse + fine)

```bash
# Level 1: Index abstracts (fast search)
leann index create \
  --config leann-abstracts.config.json \
  --input ./abstracts/ \
  --output ./leann-abstracts.index

# Level 2: Index full papers (slower, more accurate)
leann index create \
  --config leann-full.config.json \
  --input ./papers/ \
  --output ./leann-full.index

# Two-stage query
# Stage 1: Fast abstract search (retrieve 100 candidates)
CANDIDATES=$(leann query \
  --index ./leann-abstracts.index \
  --query "transformer architecture for NLP" \
  --top-k 100 \
  --format json | jq -r '.items[].item.id')

# Stage 2: Re-rank with full-text search
leann query \
  --index ./leann-full.index \
  --query "transformer architecture for NLP" \
  --filters "{\"ids\": [$CANDIDATES]}" \
  --top-k 10 \
  --mode rerank
```

**Configuration Differences:**

**Abstracts:**
```json
{
  "backend": "hnsw",
  "complexity": "medium",
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 500
  }
}
```

**Full Papers:**
```json
{
  "backend": "diskann",
  "complexity": "high",
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 2000
  }
}
```

---

## Anti-Patterns (What NOT to Do)

### ❌ Anti-Pattern 1: Over-Indexing

**Problem:** Indexing everything including binaries, logs, node_modules

```json
// BAD: No exclusions
{
  "filters": {
    "languages": []
  }
}
```

**Solution:** Explicit exclusions

```json
// GOOD: Exclude noise
{
  "filters": {
    "languages": ["python", "typescript", "go"],
    "excludePaths": [
      "node_modules/",
      "__pycache__/",
      "vendor/",
      "target/",
      "build/",
      "dist/",
      "*.log",
      "*.bin",
      "*.so",
      "*.dylib"
    ]
  }
}
```

---

### ❌ Anti-Pattern 2: Too Few Anchors

**Problem:** Using 10 anchors for 10K files (poor coverage)

```json
// BAD: Insufficient anchors
{
  "anchorSelection": {
    "type": "random",
    "count": 10
  }
}
```

**Result:** Coverage score <0.50, poor retrieval accuracy

**Solution:** Follow √N guideline

```json
// GOOD: Adequate anchors
{
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 100  // √10000 ≈ 100
  }
}
```

---

### ❌ Anti-Pattern 3: Ignoring Health Metrics

**Problem:** Never validating index, degraded performance

```bash
# BAD: Create and forget
leann index create --input . --output leann.index
# No validation, no monitoring
```

**Solution:** Regular health checks

```bash
# GOOD: Validate after creation
leann index create --input . --output leann.index
leann index validate leann.index

# Schedule periodic validation
crontab -e
# Add: 0 3 * * * /path/to/index-validator.sh leann.index
```

---

### ❌ Anti-Pattern 4: Wrong Backend Choice

**Problem:** Using DiskANN when index fits in RAM

```json
// BAD: Unnecessary disk I/O
{
  "backend": "diskann"
}
```

**Result:** 5-10× slower queries

**Solution:** Check index size first

```bash
# Calculate expected index size
# Anchors: 500 × 768 × 4 = 1.5 MB
# Deltas: 10,000 × 96 = 0.96 MB
# Total: ~2.5 MB (use HNSW)

{
  "backend": "hnsw"
}
```

---

### ❌ Anti-Pattern 5: No Incremental Updates

**Problem:** Full rebuild every commit (slow CI)

```yaml
# BAD: Full rebuild on every commit
- name: Rebuild Index
  run: leann index create --input . --output leann.index
```

**Result:** 10-30 minute CI times

**Solution:** Use incremental updates

```yaml
# GOOD: Incremental updates, scheduled rebuilds
- name: Update Index
  run: |
    leann index update \
      --index leann.index \
      --git-diff origin/main~1 HEAD \
      --output leann-updated.index

- name: Weekly Rebuild
  if: github.event.schedule == '0 2 * * 0'
  run: leann index create --input . --output leann.index
```

---

## Summary Cheatsheet

**Quick Decision Tree:**

```
What are you indexing?
├─ <1K files → Don't use LEANN (overhead not worth it)
├─ 1K-10K files → HNSW, medium complexity, 100-300 anchors
├─ 10K-100K files → HNSW, high complexity, 300-1K anchors
├─ 100K-1M files → HNSW, high complexity, 1K-10K anchors
└─ 1M+ files → DiskANN, high complexity, 10K-50K anchors

How often do you update?
├─ Static → One-time index, no incremental
├─ Rare (monthly) → Scheduled rebuild
├─ Regular (weekly) → Delta + weekly rebuild
└─ Frequent (daily) → Delta index + watch mode

How diverse is your codebase?
├─ 1 language → Random anchors OK
├─ 2-3 languages → K-means (default)
└─ 4+ languages → Stratified k-means

What's your query pattern?
├─ Exploratory → efSearch: 200, no re-ranking
├─ Precise → efSearch: 50, enable re-ranking
└─ Real-time IDE → efSearch: 100, no re-ranking
```

**Golden Rules:**
1. Start with medium complexity
2. Use k-means for production
3. Monitor coverage score (target: >0.80)
4. Enable incremental updates for CI/CD
5. Validate after every rebuild
