# osgrep Quick Reference Cheatsheet

## 🚀 Quick Start

```bash
# Setup (one-time)
osgrep setup

# Index project
osgrep index

# Search
osgrep "user authentication logic"

# Server mode (recommended)
osgrep serve &
```

## 📖 Basic Commands

```bash
osgrep <query>                      # Search current project
osgrep <query> src/                 # Search specific path
osgrep <query> --max-count 20       # More results
osgrep <query> --content            # Full content
osgrep <query> --compact            # Paths only
osgrep <query> --scores             # Show relevance
osgrep <query> --json               # JSON output
```

## 🔍 Search Patterns

```bash
# Authentication
osgrep "JWT token validation"
osgrep "password hashing with bcrypt"
osgrep "user authentication flow"

# Database
osgrep "database connection pooling"
osgrep "parameterized SQL query"
osgrep "transaction with rollback"

# Error Handling
osgrep "error handling with retry"
osgrep "exception catching and logging"
osgrep "network timeout error"

# API
osgrep "REST API endpoint handler"
osgrep "request validation middleware"
osgrep "JSON response formatting"

# Testing
osgrep "unit test with mocking"
osgrep "integration test setup"
osgrep "test fixture preparation"
```

## ⚙️ Server Mode

```bash
# Start server
osgrep serve                        # Port 4444 (default)
osgrep serve --port 5555            # Custom port
osgrep serve --parent-pid $$        # Auto-shutdown

# Check if running
lsof -i :4444

# Stop server
kill $(lsof -t -i:4444)
```

## 🗂️ Index Management

```bash
osgrep index                        # Index current dir
osgrep list                         # List all stores
osgrep doctor                       # Health check
osgrep "query" --sync               # Sync before search
```

## 📊 Output Formats

```bash
# Default (snippets)
osgrep "query"
# Output: path:line | snippet

# Full content
osgrep "query" --content
# Output: Full chunk with context

# Compact (paths only)
osgrep "query" --compact
# Output: path/to/file.ts

# With scores
osgrep "query" --scores
# Output: path:line (0.85) | snippet

# JSON (structured)
osgrep "query" --json
# Output: {"query": "...", "results": [...]}

# Plain (no colors)
osgrep "query" --plain
```

## 🎯 Result Control

```bash
osgrep "query" --max-count 5        # Total results (default: 10)
osgrep "query" --per-file 3         # Per file (default: 1)
osgrep "query" --sync               # Update index first
```

## 🔗 Tool Combinations

```bash
# osgrep → grep/rg
osgrep "API endpoint" --compact | xargs rg "POST"

# osgrep → ast-grep
osgrep "validation" --compact | xargs ast-grep --pattern 'validate($$$)'

# osgrep → fzf
osgrep "component" --compact | fzf --preview 'bat {}'

# osgrep → jq
osgrep "error handling" --json | jq -r '.results[] | select(.score > 0.7) | .path'

# osgrep → parallel
osgrep "auth" --compact | parallel 'echo "File: {}"; wc -l {}'
```

## 📈 Relevance Scores

```
0.9-1.0  Nearly identical    ★★★★★
0.7-0.9  Highly relevant     ★★★★☆
0.5-0.7  Moderately relevant ★★★☆☆
0.3-0.5  Weakly relevant     ★★☆☆☆
0.0-0.3  Low relevance       ★☆☆☆☆
```

**Filter by score**:
```bash
osgrep "query" --scores | awk '$2 > 0.7'
```

## 🛠️ Common Workflows

### Explore Codebase
```bash
osgrep "authentication" --max-count 20
osgrep "authentication" --compact | sort -u
osgrep "JWT token" --content
```

### Find Similar Code
```bash
osgrep "rate limiting" --per-file 1
osgrep "rate limiting" --max-count 15
```

### Debug Issue
```bash
osgrep "connection timeout" --scores
osgrep "connection timeout" --scores | awk '$2 > 0.7' | cut -d: -f1
```

### API Discovery
```bash
osgrep "API endpoint" --max-count 30
osgrep "POST endpoint" --compact | xargs rg "POST"
```

### Security Audit
```bash
osgrep "SQL injection" --scores
osgrep "hardcoded secret" --scores
osgrep "plaintext password" --scores
```

### Refactoring Prep
```bash
osgrep "legacy pattern" --compact > old.txt
osgrep "new pattern" --compact > new.txt
comm -23 <(sort old.txt) <(sort new.txt)
```

## 🎨 Query Best Practices

### ✅ Good Queries
```bash
osgrep "JWT authentication with refresh tokens"
osgrep "database connection pooling configuration"
osgrep "error handling for network timeouts"
osgrep "input validation using zod schemas"
```

### ❌ Poor Queries
```bash
osgrep "function"              # Too vague
osgrep "getUserById"           # Use grep for exact names
osgrep "import { something }"  # Use grep for imports
osgrep "x = y"                 # Too generic
```

### 💡 Query Tips
- Be specific about intent
- Include domain context
- Combine related concepts
- Use action verbs
- Add technical details

## 🚨 Troubleshooting

```bash
# No results
osgrep "query" --sync              # Update index
osgrep "broader query"             # Try broader

# Low scores
osgrep "more specific query"       # Add context

# Server not responding
lsof -i :4444                      # Check if running
osgrep serve &                     # Start server

# Installation issues
osgrep doctor                      # Check health
osgrep setup                       # Re-setup
```

## 📁 File Structure

```
~/.osgrep/
├── data/           # Indexes (per-project)
├── models/         # Embedding models
├── grammars/       # Tree-sitter parsers
└── meta.json       # Config
```

## 🔧 Environment Variables

```bash
export OSGREP_HOME=/custom/path        # Default: ~/.osgrep
export OSGREP_LOG_LEVEL=debug          # Default: info
export OSGREP_TELEMETRY=false          # Default: true
export OSGREP_PORT=5555                # Default: 4444
export NODE_OPTIONS="--max-old-space-size=4096"  # For large codebases
```

## 📦 Installation

```bash
# Homebrew
brew install osgrep

# npm
npm install -g osgrep

# First-time setup
osgrep setup
```

## 🔄 Updates

```bash
# Update osgrep
brew upgrade osgrep        # or: npm update -g osgrep

# Update models
osgrep setup --force

# Reindex after updates
osgrep index
```

## 🗑️ Cleanup

```bash
# Clear all indexes
rm -rf ~/.osgrep/data/*

# Uninstall
brew uninstall osgrep      # or: npm uninstall -g osgrep
rm -rf ~/.osgrep
```

## 📚 Quick Examples

### Example 1: Auth System
```bash
osgrep "authentication system" --max-count 20 --scores
osgrep "JWT token generation" --content
osgrep "password validation" --content
```

### Example 2: API Audit
```bash
osgrep "API endpoint" --compact > endpoints.txt
cat endpoints.txt | xargs rg "POST|PUT|DELETE"
```

### Example 3: Error Investigation
```bash
osgrep "database error" --scores --max-count 15
osgrep "database error" --scores | awk '$2 > 0.7' | cut -d: -f1 | xargs bat
```

### Example 4: Multi-Project Search
```bash
for dir in ~/projects/*/; do
  echo "=== $(basename $dir) ==="
  (cd "$dir" && osgrep "authentication" --compact)
done
```

### Example 5: JSON Pipeline
```bash
osgrep "validation" --json |
  jq -r '.results[] | select(.score > 0.7) | "\(.path):\(.line)"' |
  sort -u
```

## 🎓 Learning Resources

```bash
# Help
osgrep --help
osgrep search --help
osgrep serve --help

# Health check
osgrep doctor

# List indexed projects
osgrep list

# Version
osgrep --version
```

## 🔑 Key Differences

| Feature | grep/rg | osgrep |
|---------|---------|--------|
| Search type | Lexical (exact) | Semantic (meaning) |
| Query | Regex/string | Natural language |
| Speed | Very fast (<50ms) | Fast (~400ms) |
| Precision | High (exact) | High (top results) |
| Recall | Medium (exact match only) | High (similar concepts) |
| Use case | Known tokens | Conceptual exploration |

## 💻 Claude Code Integration

```bash
# Check index
osgrep doctor
osgrep list | grep -q "$(pwd)" || osgrep index

# Start server
osgrep serve --port 4444 &

# Search with filtering
osgrep "query" --scores | awk '$2 > 0.7'

# JSON for parsing
osgrep "query" --json | jq -r '.results[] | .path' | sort -u

# Combine with tools
osgrep "concept" --compact | xargs rg "token"
```

## 🌟 Pro Tips

1. **Always use server mode** for active development
2. **Filter by score** (>0.6) for quality results
3. **Use --compact** when piping to other tools
4. **Combine with grep/ast-grep** for powerful workflows
5. **Be specific** in queries - add context and intent
6. **Check scores** to diagnose query quality
7. **Use --per-file** strategically (1 for entry points, 5 for exploration)
8. **Keep indexes fresh** with --sync or server mode
9. **Use JSON output** for scripting and automation
10. **Document common patterns** as shell aliases

## 🔖 Aliases

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Quick search
alias og='osgrep'
alias ogs='osgrep --scores'
alias ogc='osgrep --compact'
alias ogj='osgrep --json'

# Server
alias ogs-start='osgrep serve --port 4444 &'
alias ogs-stop='kill $(lsof -t -i:4444)'

# Index
alias og-index='osgrep index'
alias og-list='osgrep list'
alias og-doc='osgrep doctor'

# Common patterns
alias og-auth='osgrep "authentication logic"'
alias og-api='osgrep "API endpoint handler"'
alias og-err='osgrep "error handling"'
alias og-test='osgrep "unit test"'
```

---

**Version**: osgrep 0.4.15
**Models**: Granite Embedding + ColBERT
**Strategy**: Hybrid (Vector + BM25 + RRF + Rerank)

**Remember**: `grep` finds strings, `osgrep` finds meaning! 🎯
