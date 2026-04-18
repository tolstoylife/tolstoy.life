"""
LightRAG configuration for tolstoy.life

All paths and model settings in one place.
"""

import os
from pathlib import Path

# --- Paths ---

# Project root (parent of this file's directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Vault root — override with TOLSTOY_VAULT env var if needed (cron, testing, submodule)
VAULT_ROOT = Path(
    os.environ.get("TOLSTOY_VAULT", PROJECT_ROOT / "website" / "src")
)

# Content directories to index
CONTENT_DIRS = [
    VAULT_ROOT / "wiki",
    VAULT_ROOT / "works",
    VAULT_ROOT / "letters",
    VAULT_ROOT / "images",
]

# LightRAG working directory (index, vectors, graph) — co-located with scripts
LIGHTRAG_DIR = Path(__file__).resolve().parent / "data"

# Sync state file (tracks last sync timestamp)
SYNC_STATE_FILE = LIGHTRAG_DIR / "sync_state.json"

# --- Ollama ---

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_TIMEOUT = 600  # seconds — local models can be slow; default 60s causes failures
LLM_MODEL = "qwen2.5:7b"
LLM_CONTEXT_WINDOW = 32768  # LightRAG requires >= 32k for entity extraction

# Embedding model: nomic-embed-text (768 dims, fast, good quality)
# Alternative: bge-m3 (1024 dims, better multilingual/Russian support, slower)
EMBED_MODEL = "nomic-embed-text"
EMBED_DIM = 768
EMBED_MAX_TOKENS = 8192

# --- File filtering ---

# Skip files matching these names exactly
SKIP_FILENAMES = {
    "index.njk",
    "index.md",
}

# Skip directories
SKIP_DIRS = {
    "_staging",
    "assets",
    "node_modules",
    ".obsidian",
}

# --- Query API ---

API_HOST = "127.0.0.1"
API_PORT = 8420
