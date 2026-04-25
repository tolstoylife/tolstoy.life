#!/usr/bin/env bash
# diagnose.sh — Test each component and log the result
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/venv"
LOG="$SCRIPT_DIR/diagnose.log"

echo "Writing diagnostics to $LOG"
exec > >(tee "$LOG") 2>&1

echo "=== LightRAG Diagnostics $(date) ==="
echo ""

# 1. Python version
echo "--- Python ---"
"$VENV/bin/python3" --version || echo "FAIL: python3 not found in venv"
echo ""

# 2. lightrag-server importable?
echo "--- lightrag-server import test ---"
"$VENV/bin/python3" -c "from lightrag.api.lightrag_server import main; print('OK: lightrag_server importable')" || echo "FAIL: import error above"
echo ""

# 3. fastapi / uvicorn present?
echo "--- Key dependencies ---"
"$VENV/bin/python3" -c "import fastapi; print('fastapi', fastapi.__version__)" || echo "FAIL: fastapi missing"
"$VENV/bin/python3" -c "import uvicorn; print('uvicorn', uvicorn.__version__)" || echo "FAIL: uvicorn missing"
"$VENV/bin/python3" -c "import pipmaster; print('pipmaster OK')" || echo "FAIL: pipmaster missing"
echo ""

# 4. Ollama reachable?
echo "--- Ollama ---"
if curl -sf http://localhost:11434 > /dev/null 2>&1; then
  echo "OK: Ollama responding on :11434"
  curl -s http://localhost:11434/api/tags | python3 -c "import sys,json; models=[m['name'] for m in json.load(sys.stdin).get('models',[])]; print('Models:', models)"
else
  echo "NOT running (not required for UI startup, but needed for queries)"
fi
echo ""

# 5. Try starting the server for 5 seconds and capture output
echo "--- lightrag-server startup test (5s) ---"
export WORKING_DIR="$SCRIPT_DIR/data"
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

timeout 8 "$VENV/bin/lightrag-server" 2>&1 || true
echo ""
echo "=== Done. Share the contents of lightrag/diagnose.log ==="
