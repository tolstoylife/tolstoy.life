# osgrep Configuration Reference

## Installation

### System Requirements
```yaml
OS: macOS, Linux (Windows WSL)
Node.js: v18+ recommended
Memory: 2GB+ for large codebases
Storage: 100MB-10GB (depends on project size)
```

### Installation Methods

#### Homebrew (macOS)
```bash
brew install osgrep
```

#### npm
```bash
npm install -g osgrep
```

#### From Source
```bash
git clone https://github.com/username/osgrep
cd osgrep
npm install
npm run build
npm link
```

## First-Time Setup

### Download Models
```bash
osgrep setup
```

This downloads:
- `granite-embedding-30m-english-ONNX` (~200MB)
- `osgrep-colbert-q8` (~100MB)
- Tree-sitter grammars (~50MB)

Total: ~350MB

### Directory Structure

After setup:
```
~/.osgrep/
├── data/                      # Vector stores (per-project indexes)
│   ├── project-a/
│   │   ├── chunks.lance       # LanceDB vector store
│   │   ├── fts.db             # Full-text search index
│   │   └── metadata.json      # Index metadata
│   └── project-b/
│       └── ...
├── models/                    # Embedding models
│   ├── granite-embedding-30m-english-ONNX/
│   │   ├── model.onnx
│   │   ├── tokenizer.json
│   │   └── config.json
│   └── osgrep-colbert-q8/
│       ├── model.onnx
│       └── config.json
├── grammars/                  # Tree-sitter parsers
│   ├── tree-sitter-typescript.wasm
│   ├── tree-sitter-python.wasm
│   ├── tree-sitter-rust.wasm
│   └── ... (40+ languages)
└── meta.json                  # Global configuration
```

## Embedding Models

### Granite Embedding (Default)
```yaml
Name: onnx-community/granite-embedding-30m-english-ONNX
Type: Dense embedding
Dimensions: 384
Size: ~200MB
Context: 512 tokens
Best for: English code, documentation, semantic similarity

Characteristics:
  - Fast inference (~10-30ms per query)
  - Good generalization
  - Balanced precision/recall
  - English-optimized
```

### ColBERT Reranker
```yaml
Name: ryandono/osgrep-colbert-q8
Type: Late interaction reranker
Quantization: 8-bit (Q8)
Size: ~100MB
Context: 512 tokens
Best for: Precision refinement, token-level matching

Characteristics:
  - Slower inference (~100-500ms for 50 candidates)
  - High precision at top ranks
  - Token-level cross-attention
  - Code-aware understanding
```

## Indexing Configuration

### Default Settings
```yaml
Chunk size: 512 tokens (~2000 characters)
Chunk overlap: 50 tokens (~200 characters)
Tree-sitter: Enabled
Languages: Auto-detected (40+ supported)
Exclude patterns:
  - node_modules/
  - .git/
  - build/
  - dist/
  - vendor/
  - *.min.js
  - *.bundle.js
```

### Index Creation
```bash
# Index current directory (respects .gitignore)
osgrep index

# Index with custom path
osgrep index /path/to/project

# Dry run (preview what will be indexed)
osgrep index --dry-run
```

### Supported Languages

**Full Tree-sitter support** (code-aware chunking):
- TypeScript/JavaScript (.ts, .tsx, .js, .jsx)
- Python (.py)
- Rust (.rs)
- Go (.go)
- Java (.java)
- C/C++ (.c, .cpp, .h, .hpp)
- C# (.cs)
- Ruby (.rb)
- PHP (.php)
- Swift (.swift)
- Kotlin (.kt)
- Scala (.scala)
- Elixir (.ex, .exs)
- Haskell (.hs)
- OCaml (.ml, .mli)
- Lua (.lua)
- R (.r)
- Dart (.dart)
- Julia (.jl)
- SQL (.sql)
- HTML (.html, .htm)
- CSS (.css, .scss, .sass)
- Markdown (.md)
- JSON (.json)
- YAML (.yaml, .yml)
- TOML (.toml)

**Fallback support** (line-based chunking):
- Any text file (chunked by lines)

## Server Configuration

### Start Server
```bash
osgrep serve [options]

Options:
  --port <port>       Port to listen on (default: 4444)
  --parent-pid <pid>  Parent PID for auto-shutdown
```

### Server Features
```yaml
Live indexing: File system watcher automatically reindexes on changes
Auto-shutdown: Exits when parent process terminates (--parent-pid)
HTTP API: RESTful API on localhost:PORT
WebSocket: Real-time index updates (optional)
```

### Server API Endpoints

**GET /health**
```bash
curl http://localhost:4444/health
```
Response:
```json
{
  "status": "ok",
  "indexed_files": 1234,
  "last_update": "2024-01-15T10:30:00Z"
}
```

**POST /search**
```bash
curl -X POST http://localhost:4444/search \
  -H "Content-Type: application/json" \
  -d '{"query": "authentication logic", "maxCount": 10}'
```
Response:
```json
{
  "query": "authentication logic",
  "results": [...],
  "totalResults": 10,
  "searchTime": 340
}
```

**POST /index**
```bash
curl -X POST http://localhost:4444/index \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/project"}'
```

## Search Configuration

### Command Options
```bash
osgrep search [options] <pattern> [path]

Options:
  -m, --max-count <n>     Maximum total results (default: 10)
  --per-file <n>          Results per file (default: 1)
  -c, --content           Show full chunk content (default: false)
  --scores                Show relevance scores (default: false)
  --compact               File paths only (default: false)
  --plain                 No ANSI colors (default: false)
  -s, --sync              Sync files before search (default: false)
  -d, --dry-run           Preview search without execution (default: false)
  --store <name>          Specify store explicitly (default: auto-detect)
```

### Hybrid Search Parameters

**Internal configuration** (not user-configurable):
```yaml
Vector search:
  Top-k candidates: 100
  Distance metric: Cosine similarity
  ANN algorithm: IVF (Inverted File Index)

Full-text search:
  Algorithm: BM25
  Top-k candidates: 100
  k1: 1.2 (term frequency saturation)
  b: 0.75 (length normalization)

RRF fusion:
  k parameter: 60 (rank weight constant)

Reranking:
  Model: osgrep-colbert-q8
  Top-k to rerank: 50
  Max tokens: 512
```

## Environment Variables

### Configuration
```bash
# osgrep home directory (default: ~/.osgrep)
export OSGREP_HOME=/custom/path/.osgrep

# Model cache directory (default: $OSGREP_HOME/models)
export OSGREP_MODELS=/custom/models

# Data directory (default: $OSGREP_HOME/data)
export OSGREP_DATA=/custom/data

# Disable telemetry (default: enabled)
export OSGREP_TELEMETRY=false

# Log level (default: info)
export OSGREP_LOG_LEVEL=debug  # debug, info, warn, error

# Server port (default: 4444)
export OSGREP_PORT=5555
```

### Performance Tuning
```bash
# Increase Node.js memory limit (for large codebases)
export NODE_OPTIONS="--max-old-space-size=4096"

# Parallel indexing workers (default: CPU cores - 1)
export OSGREP_WORKERS=8

# Chunk batch size for indexing (default: 100)
export OSGREP_BATCH_SIZE=200

# Enable ONNX runtime optimizations (default: true)
export OSGREP_ONNX_OPTIMIZE=true
```

## Advanced Configuration

### Custom Exclusions

Create `.osgrepignore` in project root:
```gitignore
# Custom exclusions (similar to .gitignore)
*.log
*.tmp
coverage/
.next/
.nuxt/
__pycache__/
*.pyc
target/
Cargo.lock
package-lock.json
```

### Per-Project Settings

Create `.osgrep.json` in project root:
```json
{
  "chunkSize": 512,
  "chunkOverlap": 50,
  "languages": ["typescript", "python", "rust"],
  "exclude": [
    "*.test.ts",
    "*.spec.ts",
    "fixtures/"
  ],
  "include": [
    "src/**/*.ts",
    "lib/**/*.ts"
  ],
  "embeddings": {
    "model": "granite-embedding-30m-english",
    "dimensions": 384
  }
}
```

### Store Management

#### List Stores
```bash
osgrep list
```
Output:
```
Store: project-a
  Path: /Users/username/projects/project-a
  Files: 1,234
  Chunks: 12,456
  Size: 150MB
  Updated: 2024-01-15 10:30:00

Store: project-b
  Path: /Users/username/projects/project-b
  Files: 567
  Chunks: 5,670
  Size: 75MB
  Updated: 2024-01-14 09:15:00
```

#### Delete Store
```bash
# Manual deletion
rm -rf ~/.osgrep/data/project-name

# Or use cleanup command (if available)
osgrep cleanup --store project-name
```

#### Export Store Metadata
```bash
# View store metadata
cat ~/.osgrep/data/project-name/metadata.json
```
Example:
```json
{
  "name": "project-a",
  "path": "/Users/username/projects/project-a",
  "created": "2024-01-10T08:00:00Z",
  "updated": "2024-01-15T10:30:00Z",
  "fileCount": 1234,
  "chunkCount": 12456,
  "model": "granite-embedding-30m-english",
  "dimensions": 384,
  "languages": {
    "typescript": 800,
    "python": 300,
    "markdown": 100,
    "json": 34
  }
}
```

## Performance Optimization

### Index Size vs Speed
```yaml
Small chunks (256 tokens):
  - More chunks → Larger index
  - Better granularity
  - Slower indexing
  - Faster search (less context to rerank)

Large chunks (1024 tokens):
  - Fewer chunks → Smaller index
  - Less granularity
  - Faster indexing
  - Slower search (more context to rerank)

Default (512 tokens): Balanced trade-off
```

### Memory Usage
```yaml
Indexing:
  Small project (<1k files): ~500MB RAM
  Medium project (1k-5k files): ~1-2GB RAM
  Large project (5k-10k files): ~2-4GB RAM
  Monorepo (>10k files): ~4-8GB RAM

Searching:
  Query encoding: ~100MB RAM
  Vector search: ~200-500MB RAM (depends on index size)
  Reranking: ~300-800MB RAM (depends on candidates)
```

### Disk Space
```yaml
Per-project index:
  Small (<1k files): ~50-100MB
  Medium (1k-5k files): ~100-500MB
  Large (5k-10k files): ~500MB-2GB
  Monorepo (>10k files): ~2-10GB

Models (shared across all projects):
  Granite embedding: ~200MB
  ColBERT reranker: ~100MB
  Tree-sitter grammars: ~50MB
  Total: ~350MB
```

## Troubleshooting Configuration

### Check Installation
```bash
osgrep doctor
```
Output:
```
✅ Root: /Users/username/.osgrep
✅ Models: /Users/username/.osgrep/models
✅ Data: /Users/username/.osgrep/data
✅ Grammars: /Users/username/.osgrep/grammars
✅ Model: granite-embedding-30m-english-ONNX
✅ Model: osgrep-colbert-q8

System: darwin arm64 | Node: v20.10.0
```

### Reset Configuration
```bash
# Backup existing config
mv ~/.osgrep ~/.osgrep.backup

# Re-run setup
osgrep setup

# Reindex projects
cd /path/to/project
osgrep index
```

### Clear Cache
```bash
# Clear all indexes (keeps models)
rm -rf ~/.osgrep/data/*

# Reindex all projects
for dir in ~/projects/*/; do
  (cd "$dir" && osgrep index)
done
```

## Integration with Claude Code

### MCP Server Configuration

If using osgrep as an MCP tool in Claude Code:

**claude_desktop_config.json**:
```json
{
  "mcpServers": {
    "osgrep": {
      "command": "osgrep",
      "args": ["serve", "--port", "4444"],
      "env": {
        "OSGREP_LOG_LEVEL": "warn",
        "OSGREP_TELEMETRY": "false"
      }
    }
  }
}
```

### Claude Code Skill Integration

The osgrep skill automatically:
- Checks if server is running (`osgrep doctor`)
- Starts server if needed (`osgrep serve`)
- Uses JSON output for structured parsing
- Filters by relevance scores (>0.6)
- Combines with other tools (rg, ast-grep, fzf)

## Updating

### Update osgrep
```bash
# Homebrew
brew upgrade osgrep

# npm
npm update -g osgrep
```

### Update Models
```bash
# Re-run setup to download latest models
osgrep setup --force
```

### Migrate Indexes
```bash
# After major version updates, reindex projects
for dir in ~/projects/*/; do
  (cd "$dir" && osgrep index)
done
```

## Uninstallation

```bash
# Remove osgrep binary
brew uninstall osgrep  # or: npm uninstall -g osgrep

# Remove data and models
rm -rf ~/.osgrep
```

## References

- **GitHub**: https://github.com/username/osgrep
- **Documentation**: https://osgrep.dev
- **Issue Tracker**: https://github.com/username/osgrep/issues
- **Changelog**: https://github.com/username/osgrep/blob/main/CHANGELOG.md
