# LEANN Quick Reference Cheatsheet

## Installation

```bash
# Via pip
pip install leann

# Via conda
conda install -c conda-forge leann

# Docker embedding server
docker run -d --gpus all -p 5555:5555 leann/embedding-server:latest
```

---

## Index Operations

### Create Index

```bash
# Basic
leann index create \
  --input /path/to/codebase \
  --output ./leann.index

# With config
leann index create \
  --config leann.config.json \
  --input /path/to/codebase \
  --output ./leann.index \
  --progress

# Parallel (by directory)
parallel -j 4 leann index create \
  --input /path/to/{} --output leann-{}.index ::: service-a service-b service-c
```

### Update Index

```bash
# Incremental update
leann index update \
  --index ./leann.index \
  --git-diff HEAD~1 HEAD

# Watch mode (live updates)
leann index update \
  --index ./leann.index \
  --watch

# Full rebuild
leann index rebuild \
  --index ./leann.index \
  --output ./leann-rebuilt.index
```

### Validate Index

```bash
# Quick health check
leann index validate ./leann.index

# Detailed validation
leann index validate ./leann.index --verbose

# Specific metric
leann index validate ./leann.index --metric coverage

# JSON output
leann index validate ./leann.index --json

# With repair attempts
REPAIR=true ./scripts/index-validator.sh ./leann.index
```

### Index Stats

```bash
# Basic stats
leann index stats ./leann.index

# Detailed breakdown
leann index stats ./leann.index --verbose

# JSON output
leann index stats ./leann.index --json | jq
```

---

## Query Operations

### Basic Query

```bash
# Standard query
leann query \
  --index ./leann.index \
  --query "JWT authentication middleware" \
  --top-k 10

# JSON output
leann query \
  --index ./leann.index \
  --query "database connection pooling" \
  --format json | jq
```

### Advanced Query

```bash
# With filters
leann query \
  --index ./leann.index \
  --query "error handling" \
  --filters '{"languages": ["typescript"], "paths": ["src/**/*"]}' \
  --top-k 5

# Re-ranking mode
leann query \
  --index ./leann.index \
  --query "rate limiting" \
  --mode rerank \
  --top-k 10

# Override efSearch
leann query \
  --index ./leann.index \
  --query "authentication" \
  --ef-search 200 \
  --top-k 10
```

### Batch Query

```bash
# From file
leann query \
  --index ./leann.index \
  --queries-file queries.txt \
  --top-k 5 \
  --output results.jsonl
```

---

## Server Mode

### Start Server

```bash
# Basic server
leann serve \
  --index ./leann.index \
  --port 8080

# With watch mode
leann serve \
  --index ./leann.index \
  --watch \
  --port 8080 \
  --auto-update

# Production mode
leann serve \
  --index ./leann.index \
  --port 8080 \
  --workers 4 \
  --log-level info
```

### Query Server

```bash
# HTTP POST
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "authentication middleware",
    "topK": 10
  }'

# Health check
curl http://localhost:8080/health

# Stats endpoint
curl http://localhost:8080/stats
```

---

## Configuration Quick Snippets

### Minimal Config

```json
{
  "backend": "hnsw",
  "complexity": "medium",
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 300
  },
  "embeddingServer": {
    "endpoint": "tcp://localhost:5555",
    "model": "sentence-transformers/all-MiniLM-L6-v2"
  }
}
```

### Production Config

```json
{
  "backend": "hnsw",
  "complexity": "high",
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 1000
  },
  "incremental": {
    "enabled": true,
    "deltaIndexThreshold": 1000,
    "rebuildSchedule": "0 2 * * *"
  },
  "hnsw": {
    "M": 32,
    "efConstruction": 400,
    "efSearch": 200
  }
}
```

### Polyglot Config

```json
{
  "anchorSelection": {
    "type": "stratified-kmeans",
    "totalClusters": 500,
    "stratification": {
      "groupBy": "language",
      "minPerGroup": 20
    }
  },
  "filters": {
    "languages": ["python", "typescript", "go"],
    "excludePaths": ["node_modules/", "__pycache__/", "vendor/"]
  }
}
```

---

## Python API

### Basic Usage

```python
from leann import LEANNIndex

# Load index
index = LEANNIndex.load('./leann.index')

# Query
results = index.query(
    query="database connection pooling",
    top_k=10
)

# Access results
for item in results.items:
    print(f"{item.item.path} (score: {item.score:.2f})")
```

### Advanced Usage

```python
# Query with filters
results = index.query(
    query="authentication",
    top_k=5,
    mode='rerank',
    filters={
        'languages': ['typescript'],
        'paths': ['src/middleware/*.ts']
    }
)

# Batch queries
queries = ["JWT auth", "database migration", "error handling"]
results_batch = index.batch_query(queries, top_k=5)

# Get index stats
stats = index.get_stats()
print(f"Health Score: {stats.healthScore}/100")
print(f"Storage: {stats.storageSize / 1024 / 1024:.1f} MB")
print(f"Avg Latency: {stats.avgLatency:.1f}ms")
```

---

## Common Workflows

### Initial Setup

```bash
# 1. Start embedding server
docker run -d -p 5555:5555 leann/embedding-server:latest

# 2. Create config
cat > leann.config.json <<EOF
{
  "backend": "hnsw",
  "complexity": "medium",
  "anchorSelection": {"type": "kmeans", "clusters": 300},
  "embeddingServer": {"endpoint": "tcp://localhost:5555"}
}
EOF

# 3. Create index
leann index create \
  --config leann.config.json \
  --input . \
  --output ./leann.index \
  --progress

# 4. Validate
leann index validate ./leann.index
```

### CI/CD Integration

```yaml
# .github/workflows/update-index.yml
- name: Update Index
  run: |
    leann index update \
      --index ./leann.index \
      --git-diff origin/main~1 HEAD

- name: Validate
  run: |
    leann index validate ./leann.index
    if [ $? -ne 0 ]; then
      leann index rebuild --index ./leann.index
    fi
```

### IDE Integration

```typescript
// VS Code extension
import { LEANNSearchProvider } from './search';

const provider = new LEANNSearchProvider('http://localhost:8080');

// On search command
const results = await provider.search(
  'authentication middleware',
  10
);

// Display results in QuickPick
vscode.window.showQuickPick(
  results.map(r => ({
    label: r.path,
    description: `Score: ${r.score.toFixed(2)}`
  }))
);
```

---

## Troubleshooting

### Index Issues

```bash
# Health check
leann index validate ./leann.index --verbose

# Check specific metrics
leann index validate ./leann.index --metric coverage
leann index validate ./leann.index --metric quantization
leann index validate ./leann.index --metric balance

# Attempt repair
REPAIR=true ./scripts/index-validator.sh ./leann.index
```

### Query Issues

```bash
# Increase efSearch for better recall
leann query --index ./leann.index --query "auth" --ef-search 200

# Enable re-ranking for better precision
leann query --index ./leann.index --query "auth" --mode rerank

# Check index stats
leann index stats ./leann.index
```

### Server Issues

```bash
# Check embedding server
curl http://localhost:5555/health

# Restart server
docker restart leann-embeddings

# Check logs
docker logs leann-embeddings
```

---

## Performance Tuning

### Query Latency

```json
{
  "hnsw": {
    "efSearch": 50  // Reduce for speed
  }
}
```

### Storage Optimization

```json
{
  "quantization": {
    "subVectors": 128,  // More aggressive compression
    "codebookSize": 128
  }
}
```

### Accuracy Improvement

```json
{
  "anchorSelection": {
    "clusters": 1000  // More anchors
  },
  "reranking": {
    "enabled": true
  }
}
```

---

## Metrics & Monitoring

### Key Metrics

```bash
# Coverage score (target: >0.80)
leann index validate ./leann.index --metric coverage

# Quantization error (target: <0.05)
leann index validate ./leann.index --metric quantization

# Utilization balance (target: >0.70)
leann index validate ./leann.index --metric balance

# Overall health (target: >80/100)
leann index validate ./leann.index --json | jq .healthScore
```

### Rebuild Triggers

```bash
# Check delta index size
STATS=$(leann index stats ./leann.index --json)
DELTA_SIZE=$(echo $STATS | jq .deltaIndexSize)
MAIN_SIZE=$(echo $STATS | jq .mainIndexSize)
RATIO=$(echo "scale=2; $DELTA_SIZE / $MAIN_SIZE * 100" | bc)

if (( $(echo "$RATIO > 10" | bc -l) )); then
  echo "Rebuild recommended (delta index: ${RATIO}%)"
fi
```

---

## Configuration Presets

### Small Project (<10K files)

```json
{
  "backend": "hnsw",
  "complexity": "medium",
  "anchorSelection": {"type": "kmeans", "clusters": 200}
}
```

### Large Project (10K-100K files)

```json
{
  "backend": "hnsw",
  "complexity": "high",
  "anchorSelection": {"type": "kmeans", "clusters": 500}
}
```

### Massive Scale (1M+ files)

```json
{
  "backend": "diskann",
  "complexity": "high",
  "anchorSelection": {"type": "kmeans", "clusters": 5000},
  "diskann": {"ramBudget": 8}
}
```

### Memory-Constrained

```json
{
  "quantization": {"subVectors": 128, "codebookSize": 128}
}
```

### Latency-Critical

```json
{
  "hnsw": {"efSearch": 50}
}
```

### Accuracy-Critical

```json
{
  "anchorSelection": {"clusters": 1000},
  "reranking": {"enabled": true}
}
```

---

## Decision Trees

### Backend Selection

```
Index Size < RAM/2 → HNSW (10-30ms latency)
Index Size > RAM/2 → DiskANN (50-200ms latency)

Index Size = anchors × 768 × 4 + files × 96
Example: 1K anchors × 3KB + 10K files × 96B ≈ 4MB
```

### Anchor Count

```
Use M = √N as baseline

1K files   → 100 anchors
10K files  → 300 anchors
100K files → 1K anchors
1M files   → 10K anchors
```

### Anchor Selection Strategy

```
Homogeneous codebase → random
Diverse codebase → kmeans (default)
Polyglot codebase → stratified-kmeans
Sparse distribution → max-coverage
```

---

## Common Gotchas

**❌ Don't:**
- Index everything (exclude node_modules, build dirs)
- Use too few anchors (coverage < 0.70)
- Ignore health metrics
- Use DiskANN when HNSW fits in RAM
- Skip validation after creation

**✓ Do:**
- Start with medium complexity
- Use k-means for production
- Monitor coverage score
- Enable incremental updates
- Validate after every rebuild

---

## Quick Reference Tables

### Complexity Levels

| Level | Build Time | Query Time | Accuracy | Use Case |
|-------|------------|------------|----------|----------|
| low | Fast | 5-10ms | Good | Prototyping |
| medium | Moderate | 10-20ms | Better | Production |
| high | Slow | 20-40ms | Best | Critical |

### Storage Impact

| Anchor Count | Index Size (10K files) | Coverage | Rebuild Time |
|--------------|------------------------|----------|--------------|
| 100 | ~1.2 MB | Acceptable | Fast |
| 300 | ~1.8 MB | Good | Moderate |
| 1000 | ~4 MB | Excellent | Slow |

### Backend Comparison

| Backend | Latency | Memory | Max Files | Use Case |
|---------|---------|--------|-----------|----------|
| HNSW | 10-30ms | High | 1M | Fast queries |
| DiskANN | 50-200ms | Low | 100M+ | Large scale |

---

## Environment Variables

```bash
# Index validation thresholds
export COVERAGE_MIN=0.70
export QUANT_ERROR_MAX=0.05
export BALANCE_MIN=0.70

# Verbose output
export VERBOSE=true

# JSON output
export JSON_OUTPUT=true

# Attempt repairs
export REPAIR=true
```

---

## Links

**Documentation:**
- Skill: `/Users/mikhail/Downloads/architect/leann/SKILL.md`
- Configuration: `/Users/mikhail/Downloads/architect/leann/references/configuration.md`
- Indexing Patterns: `/Users/mikhail/Downloads/architect/leann/references/indexing-patterns.md`

**Codebase:**
- Types: `/Users/mikhail/Downloads/architect/leann-codebase/types/core.ts`
- Anchor Selection: `/Users/mikhail/Downloads/architect/leann-codebase/principles/anchor-selection.md`
- Graph Navigation: `/Users/mikhail/Downloads/architect/leann-codebase/principles/graph-navigation.md`
- Workflows: `/Users/mikhail/Downloads/architect/leann-codebase/templates/indexing-workflow.md`

**Scripts:**
- Validator: `/Users/mikhail/Downloads/architect/leann/scripts/index-validator.sh`
