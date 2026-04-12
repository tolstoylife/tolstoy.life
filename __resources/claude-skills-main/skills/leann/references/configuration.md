# LEANN Configuration Guide

## Complete Configuration Reference

This document provides comprehensive guidance on all LEANN configuration parameters, when to use each backend, and how to tune for optimal performance.

---

## Configuration Schema

### Full Configuration Example

```json
{
  "backend": "hnsw",
  "complexity": "medium",
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 300,
    "samples": 10000,
    "stratification": {
      "enabled": false,
      "groupBy": "language",
      "minPerGroup": 20,
      "allocation": "proportional"
    }
  },
  "quantization": {
    "subVectors": 96,
    "codebookSize": 256,
    "trainingSamples": 10000
  },
  "embeddingServer": {
    "endpoint": "tcp://localhost:5555",
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "batchSize": 128,
    "timeout": 30000
  },
  "incremental": {
    "enabled": true,
    "deltaIndexThreshold": 1000,
    "rebuildSchedule": "0 2 * * *",
    "watchMode": false,
    "gitIntegration": {
      "enabled": false,
      "trackBranch": "main",
      "pollInterval": 300
    }
  },
  "hnsw": {
    "M": 16,
    "efConstruction": 200,
    "efSearch": 100,
    "maxM0": 32
  },
  "diskann": {
    "R": 64,
    "L": 100,
    "alpha": 1.2,
    "maxDegree": 128,
    "threads": 4,
    "ramBudget": 8
  },
  "reranking": {
    "enabled": false,
    "model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
    "endpoint": "tcp://localhost:5556",
    "candidateMultiplier": 10,
    "batchSize": 100
  },
  "filters": {
    "languages": ["python", "typescript", "go"],
    "excludePaths": [
      "node_modules/",
      "__pycache__/",
      "vendor/",
      "*.test.ts",
      "*.spec.py"
    ],
    "includePatterns": ["src/**/*", "lib/**/*"]
  },
  "scoring": {
    "typeWeights": {
      "code": 1.0,
      "documentation": 1.5,
      "test": 0.8
    }
  }
}
```

---

## Backend Selection

### HNSW (Hierarchical Navigable Small World)

**When to Use:**
- Index size < 50% of available RAM
- Query latency is critical (<30ms)
- Moderate to high-frequency queries

**Characteristics:**
- In-memory graph structure
- Multi-layer hierarchy (fast long-range traversal)
- Query complexity: O(log M × avgDegree)
- Typical latency: 10-30ms

**Configuration Parameters:**

```json
{
  "backend": "hnsw",
  "hnsw": {
    "M": 16,
    "efConstruction": 200,
    "efSearch": 100,
    "maxM0": 32
  }
}
```

#### M (Graph Connectivity)
- **Range:** 8-64
- **Default:** 16
- **Trade-off:** Higher M = better recall, slower construction, more memory

| M | Build Time | Memory | Recall | Use Case |
|---|------------|--------|--------|----------|
| 8 | Fast | Low | Good | Prototyping |
| 16 | Medium | Medium | Better | Production (default) |
| 32 | Slow | High | Best | Critical accuracy |
| 64 | Very Slow | Very High | Excellent | Research/offline |

#### efConstruction (Build Quality)
- **Range:** 50-800
- **Default:** 200
- **Trade-off:** Higher efConstruction = better graph, slower build

```
efConstruction = 100 → Fast build, acceptable quality
efConstruction = 200 → Balanced (recommended)
efConstruction = 400 → Slow build, high quality
```

#### efSearch (Query Recall)
- **Range:** 10-500
- **Default:** 100
- **Trade-off:** Higher efSearch = better recall, slower queries

```
efSearch = 50  → 5-10ms latency, ~85% recall
efSearch = 100 → 10-20ms latency, ~92% recall
efSearch = 200 → 20-40ms latency, ~97% recall
```

**Runtime Override:**
```bash
leann query \
  --index ./leann.index \
  --query "authentication" \
  --ef-search 200  # Override config
```

#### maxM0 (Layer 0 Connectivity)
- **Range:** M to 2×M
- **Default:** 2×M
- **Purpose:** Layer 0 can have more connections for better recall

**Complexity Presets:**

```json
{
  "low": {
    "M": 12,
    "efConstruction": 100,
    "efSearch": 50
  },
  "medium": {
    "M": 16,
    "efConstruction": 200,
    "efSearch": 100
  },
  "high": {
    "M": 32,
    "efConstruction": 400,
    "efSearch": 200
  }
}
```

---

### DiskANN (Disk-Based ANN)

**When to Use:**
- Index size > 50% of available RAM
- Dataset exceeds 1M files
- Acceptable latency: 50-200ms

**Characteristics:**
- Disk-optimized single-layer graph
- SSD required for acceptable performance
- Query complexity: O(log N) with disk I/O
- Typical latency: 50-200ms

**Configuration Parameters:**

```json
{
  "backend": "diskann",
  "diskann": {
    "R": 64,
    "L": 100,
    "alpha": 1.2,
    "maxDegree": 128,
    "threads": 4,
    "ramBudget": 8
  }
}
```

#### R (Search List Size)
- **Range:** 32-256
- **Default:** 64
- **Trade-off:** Higher R = better recall, slower build

```
R = 32  → Fast build, lower recall
R = 64  → Balanced (recommended)
R = 128 → Slow build, high recall
```

#### L (Construction Beam Width)
- **Range:** 50-300
- **Default:** 100
- **Trade-off:** Higher L = better graph quality, slower build

```
L = 50  → Fast construction
L = 100 → Balanced (default)
L = 200 → High-quality graph
```

#### alpha (Pruning Parameter)
- **Range:** 1.0-1.5
- **Default:** 1.2
- **Purpose:** Controls edge pruning aggressiveness

```
alpha = 1.0 → Aggressive pruning, sparse graph
alpha = 1.2 → Balanced (recommended)
alpha = 1.5 → Conservative pruning, dense graph
```

#### maxDegree (Degree Bound)
- **Range:** R to 2×R
- **Default:** 2×R
- **Purpose:** Hard limit on node degree

#### threads (Parallelism)
- **Range:** 1-16
- **Default:** 4
- **Purpose:** Parallel graph construction

**Recommendation:** Use all available CPU cores
```json
{
  "threads": 8  // For 8-core machine
}
```

#### ramBudget (Cache Size in GB)
- **Range:** 1-64
- **Default:** 8
- **Purpose:** RAM for hot node caching

**Sizing Guide:**
```
ramBudget = 25% of total RAM (recommended)
Example: 32 GB RAM → ramBudget: 8
```

**Complexity Presets:**

```json
{
  "low": {
    "R": 32,
    "L": 50,
    "alpha": 1.2,
    "maxDegree": 64
  },
  "medium": {
    "R": 64,
    "L": 100,
    "alpha": 1.2,
    "maxDegree": 128
  },
  "high": {
    "R": 128,
    "L": 200,
    "alpha": 1.2,
    "maxDegree": 256
  }
}
```

---

## Anchor Selection Strategies

### 1. Random Selection

**Configuration:**
```json
{
  "anchorSelection": {
    "type": "random",
    "count": 300
  }
}
```

**Characteristics:**
- Complexity: O(N)
- Quality: Acceptable for homogeneous codebases
- Build time: ~1-2 seconds for 10K files

**Use When:**
- Prototyping or testing
- Single-language codebase
- Speed is critical

---

### 2. K-Means Clustering (Recommended)

**Configuration:**
```json
{
  "anchorSelection": {
    "type": "kmeans",
    "clusters": 300,
    "samples": 10000
  }
}
```

**Parameters:**

#### clusters (Anchor Count)
- **Guideline:** √N (square root of total files)
- **Minimum:** 50
- **Maximum:** N/10

```
1K files   → 100 anchors
10K files  → 300 anchors
100K files → 1K anchors
1M files   → 10K anchors
```

#### samples (Sampling for Speed)
- **Purpose:** Speed up k-means for large datasets
- **Default:** min(N, 50000)
- **Trade-off:** More samples = slower but more representative

```json
{
  "samples": 5000   // For N = 10K (fast)
  "samples": 20000  // For N = 100K (balanced)
  "samples": 50000  // For N = 1M (accurate)
}
```

**Characteristics:**
- Complexity: O(N × k × iterations)
- Quality: Excellent coverage
- Build time: ~30 seconds to 5 minutes

**Use When:**
- Production deployments (default choice)
- Diverse codebases
- Maximum accuracy required

---

### 3. Stratified K-Means (Polyglot)

**Configuration:**
```json
{
  "anchorSelection": {
    "type": "stratified-kmeans",
    "totalClusters": 500,
    "stratification": {
      "enabled": true,
      "groupBy": "language",
      "minPerGroup": 20,
      "allocation": "proportional"
    }
  }
}
```

**Parameters:**

#### groupBy
- **Options:** "language", "directory", "type"
- **Default:** "language"

#### minPerGroup
- **Purpose:** Ensure minority groups get representation
- **Default:** 10

#### allocation
- **Options:** "proportional", "uniform"
- **proportional:** Anchors allocated by group size
- **uniform:** Equal anchors per group

**Example Allocation (proportional):**
```
Files: 10,000 (60% Python, 30% TypeScript, 10% Go)
Total anchors: 500

Allocation:
- Python: 300 anchors (60%)
- TypeScript: 150 anchors (30%)
- Go: 50 anchors (10% → boosted to minPerGroup: 20 if needed)
```

**Use When:**
- Multi-language codebases
- Preventing language dominance
- Cross-language code search

---

### 4. Max-Coverage

**Configuration:**
```json
{
  "anchorSelection": {
    "type": "max-coverage",
    "count": 300,
    "diversityThreshold": 0.2
  }
}
```

**Parameters:**

#### diversityThreshold
- **Range:** 0.1-0.5
- **Default:** 0.2
- **Purpose:** Minimum distance for new anchor

**Characteristics:**
- Complexity: O(N × M²)
- Quality: Best for sparse distributions
- Build time: Slow (minutes to hours)

**Use When:**
- Codebase has significant outliers
- Sparse or long-tailed embedding distribution
- k-means produces too uniform clusters

---

## Product Quantization

**Configuration:**
```json
{
  "quantization": {
    "subVectors": 96,
    "codebookSize": 256,
    "trainingSamples": 10000
  }
}
```

### subVectors (Compression Level)

**For 768-dimensional embeddings:**

| subVectors | Bytes per Delta | Compression | Reconstruction Quality |
|------------|-----------------|-------------|------------------------|
| 64 | 64 | Moderate | High |
| 96 | 96 | Balanced | Good |
| 128 | 128 | Aggressive | Acceptable |
| 192 | 192 | Light | Excellent |

**Recommendation:** 96 subvectors (standard)

### codebookSize (Precision)

| codebookSize | Bits | Storage | Quality |
|--------------|------|---------|---------|
| 128 | 7-bit | 7/8 bytes | Acceptable |
| 256 | 8-bit | 1 byte | Good (default) |
| 512 | 9-bit | 1.125 bytes | Better |
| 1024 | 10-bit | 1.25 bytes | Excellent |

**Recommendation:** 256 (8-bit standard)

### trainingSamples (Codebook Quality)

- **Minimum:** 1000
- **Recommended:** 10× codebookSize
- **Default:** 10000

```
codebookSize = 256 → trainingSamples = 2560 (minimum)
codebookSize = 256 → trainingSamples = 10000 (recommended)
```

### Trade-off Scenarios

**Memory-Optimized:**
```json
{
  "subVectors": 128,
  "codebookSize": 128
}
```
- Storage: ~128 bytes per item
- Quality: Acceptable
- Use case: RAM-constrained environments

**Latency-Optimized:**
```json
{
  "subVectors": 64,
  "codebookSize": 512
}
```
- Storage: ~72 bytes per item
- Quality: Better
- Use case: Query speed critical

**Quality-Optimized:**
```json
{
  "subVectors": 96,
  "codebookSize": 512
}
```
- Storage: ~108 bytes per item
- Quality: Excellent
- Use case: Maximum accuracy required

---

## Embedding Server

**Configuration:**
```json
{
  "embeddingServer": {
    "endpoint": "tcp://localhost:5555",
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "batchSize": 128,
    "timeout": 30000
  }
}
```

### Model Selection

| Model | Dimensions | Speed | Quality | Use Case |
|-------|------------|-------|---------|----------|
| all-MiniLM-L6-v2 | 384 | Fast | Good | General code |
| all-MiniLM-L12-v2 | 384 | Medium | Better | Balanced |
| all-mpnet-base-v2 | 768 | Slow | Best | High quality |
| codebert-base | 768 | Medium | Excellent | Code-specific |

**Recommendation:** all-MiniLM-L6-v2 (default)

### batchSize (GPU Utilization)

| GPU | Recommended batchSize | Throughput |
|-----|----------------------|------------|
| None (CPU) | 32 | 10-20 files/sec |
| 8 GB GPU | 128 | 100-200 files/sec |
| 16 GB GPU | 256 | 200-400 files/sec |
| 24 GB GPU | 512 | 400-800 files/sec |

**Auto-detect:**
```json
{
  "batchSize": "auto"  // Detects GPU memory
}
```

### timeout (Request Timeout)

- **Default:** 30000 (30 seconds)
- **Adjust for:** Large files, slow GPUs

```json
{
  "timeout": 60000  // 60 seconds for large files
}
```

---

## Incremental Updates

**Configuration:**
```json
{
  "incremental": {
    "enabled": true,
    "deltaIndexThreshold": 1000,
    "rebuildSchedule": "0 2 * * *",
    "watchMode": false,
    "gitIntegration": {
      "enabled": false,
      "trackBranch": "main",
      "pollInterval": 300
    }
  }
}
```

### deltaIndexThreshold (Rebuild Trigger)

**Guideline:** 5-10% of main index size

```
10K files → deltaIndexThreshold: 500-1000
100K files → deltaIndexThreshold: 5000-10000
1M files → deltaIndexThreshold: 50000-100000
```

### rebuildSchedule (Cron Expression)

```
"0 2 * * *"      → Daily at 2 AM
"0 2 * * 0"      → Weekly on Sunday at 2 AM
"0 2 1 * *"      → Monthly on 1st at 2 AM
"0 */6 * * *"    → Every 6 hours
```

### watchMode (Live Updates)

**Enable for:** IDE integrations, development servers
**Disable for:** Production (use scheduled rebuilds)

```json
{
  "watchMode": true  // Auto-rebuild on file changes
}
```

### gitIntegration (Commit-Based Updates)

```json
{
  "gitIntegration": {
    "enabled": true,
    "trackBranch": "main",
    "pollInterval": 300  // 5 minutes
  }
}
```

**Use Case:** CI/CD pipelines

---

## Re-ranking (Two-Stage Retrieval)

**Configuration:**
```json
{
  "reranking": {
    "enabled": true,
    "model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
    "endpoint": "tcp://localhost:5556",
    "candidateMultiplier": 10,
    "batchSize": 100
  }
}
```

### candidateMultiplier (Re-rank Ratio)

```
topK = 10
candidateMultiplier = 10
→ Retrieve 100 candidates, re-rank to 10

Higher multiplier → Better accuracy, higher latency
```

| Multiplier | Latency Impact | Accuracy Gain |
|------------|----------------|---------------|
| 5 | +30ms | +5-10% NDCG |
| 10 | +50ms | +10-15% NDCG |
| 20 | +100ms | +15-20% NDCG |

**Recommendation:** 10 (balanced)

### Model Selection

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| ms-marco-MiniLM-L-6-v2 | Fast | Good | Production |
| ms-marco-MiniLM-L-12-v2 | Medium | Better | High accuracy |
| ms-marco-electra-base | Slow | Best | Research |

---

## Filters

**Configuration:**
```json
{
  "filters": {
    "languages": ["python", "typescript", "go"],
    "excludePaths": [
      "node_modules/",
      "__pycache__/",
      "vendor/"
    ],
    "includePatterns": ["src/**/*", "lib/**/*"]
  }
}
```

### Common Exclusions

**Node.js:**
```json
["node_modules/", "dist/", "build/", "*.min.js"]
```

**Python:**
```json
["__pycache__/", "*.pyc", ".venv/", "venv/", ".pytest_cache/"]
```

**Go:**
```json
["vendor/", "*.pb.go", "_test.go"]
```

**Rust:**
```json
["target/", "Cargo.lock"]
```

---

## Summary Cheatsheet

**Quick Start Configs:**

**Small Project (<10K files):**
```json
{
  "backend": "hnsw",
  "complexity": "medium",
  "anchorSelection": {"type": "kmeans", "clusters": 200}
}
```

**Large Project (10K-100K files):**
```json
{
  "backend": "hnsw",
  "complexity": "high",
  "anchorSelection": {"type": "kmeans", "clusters": 500}
}
```

**Massive Scale (1M+ files):**
```json
{
  "backend": "diskann",
  "complexity": "high",
  "anchorSelection": {"type": "kmeans", "clusters": 5000}
}
```

**Memory-Constrained:**
```json
{
  "quantization": {"subVectors": 128, "codebookSize": 128}
}
```

**Latency-Critical:**
```json
{
  "hnsw": {"efSearch": 50}
}
```

**Accuracy-Critical:**
```json
{
  "reranking": {"enabled": true}
}
```
