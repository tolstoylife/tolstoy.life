#!/usr/bin/env bash
# start-ui.sh — Start Ollama (if not running) + LightRAG web UI
#
# Usage:
#   ./lightrag/start-ui.sh
#
# Then open: http://localhost:9621
# API docs:  http://localhost:9621/docs
#
# Prerequisites:
#   - Ollama installed (https://ollama.com)
#   - Models pulled: ollama pull qwen2.5:7b && ollama pull bge-m3

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/venv"
DATA_DIR="$SCRIPT_DIR/data"
OLLAMA_LOG="$SCRIPT_DIR/ollama.log"

# --- Verify prerequisites ---

if [ ! -f "$VENV/bin/lightrag-server" ]; then
  echo "ERROR: lightrag-server not found at $VENV/bin/lightrag-server"
  echo "Re-install: cd lightrag && python3 -m venv venv && venv/bin/pip install -r requirements.txt"
  exit 1
fi

if [ ! -d "$DATA_DIR" ]; then
  echo "ERROR: data directory not found at $DATA_DIR"
  echo "Run ingest.py first to build the index."
  exit 1
fi

# Find ollama binary (Mac app puts it at /usr/local/bin/ollama;
# Homebrew at /opt/homebrew/bin/ollama; also check PATH)
OLLAMA_BIN=""
for candidate in /usr/local/bin/ollama /opt/homebrew/bin/ollama "$(which ollama 2>/dev/null || true)"; do
  if [ -x "$candidate" ]; then
    OLLAMA_BIN="$candidate"
    break
  fi
done

if [ -z "$OLLAMA_BIN" ]; then
  echo "ERROR: ollama not found. Install from https://ollama.com and then run:"
  echo "  ollama pull qwen2.5:7b"
  echo "  ollama pull bge-m3"
  exit 1
fi

# --- Start Ollama if not already running ---

OLLAMA_STARTED=false
if ! curl -sf http://localhost:11434 > /dev/null 2>&1; then
  echo "Ollama is not running — starting it..."
  "$OLLAMA_BIN" serve >> "$OLLAMA_LOG" 2>&1 &
  OLLAMA_PID=$!
  OLLAMA_STARTED=true

  # Wait up to 10 s for Ollama to become ready
  for i in $(seq 1 20); do
    if curl -sf http://localhost:11434 > /dev/null 2>&1; then
      echo "Ollama ready."
      break
    fi
    sleep 0.5
  done

  if ! curl -sf http://localhost:11434 > /dev/null 2>&1; then
    echo "ERROR: Ollama did not start in time. Check $OLLAMA_LOG"
    exit 1
  fi
else
  echo "Ollama already running."
fi

# Stop Ollama on exit only if we started it ourselves
cleanup() {
  if [ "$OLLAMA_STARTED" = true ] && [ -n "${OLLAMA_PID:-}" ]; then
    echo ""
    echo "Stopping Ollama (PID $OLLAMA_PID)..."
    kill "$OLLAMA_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

# --- Launch LightRAG web UI ---

echo ""
echo "Starting LightRAG web UI..."
echo "  Working dir : $DATA_DIR"
echo "  LLM         : qwen2.5:7b (Ollama @ localhost:11434)"
echo "  Embeddings  : bge-m3 1024d (Ollama @ localhost:11434)"
echo ""
echo "  Open: http://localhost:9621"
echo "  Docs: http://localhost:9621/docs"
echo ""
echo "Press Ctrl+C to stop."
echo ""

export WORKING_DIR="$DATA_DIR"
export HOST="127.0.0.1"
export PORT="9621"
export LLM_BINDING="ollama"
export LLM_BINDING_HOST="http://localhost:11434"
export LLM_MODEL="qwen2.5:7b"
export EMBEDDING_BINDING="ollama"
export EMBEDDING_BINDING_HOST="http://localhost:11434"
export EMBEDDING_MODEL="bge-m3"
export EMBEDDING_DIM="1024"
export TIMEOUT="600"
export LOG_LEVEL="INFO"

exec "$VENV/bin/lightrag-server"
