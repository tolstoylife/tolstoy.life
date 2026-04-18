#!/usr/bin/env python3
"""
Local query API server for LightRAG.

Exposes the LightRAG query engine as a simple HTTP API that Claude
(or any other tool) can call during wiki operations.

Usage:
    python server.py                 # Start on default port 8420
    python server.py --port 9000     # Custom port

Endpoints:
    POST /query     — Query the knowledge graph
    GET  /health    — Health check
    GET  /stats     — Index statistics
"""

import asyncio
import argparse
import json
from pathlib import Path

from aiohttp import web

from config import API_HOST, API_PORT, LIGHTRAG_DIR, SYNC_STATE_FILE
from rag import create_rag

# Module-level RAG instance (initialized on startup)
rag = None


async def handle_query(request: web.Request) -> web.Response:
    """Handle a query request.

    POST /query
    Body: {
        "query": "What role did Sophia Tolstaya play?",
        "mode": "hybrid",      // optional: naive, local, global, hybrid (default: hybrid)
        "top_k": 60            // optional (default: 60)
    }
    """
    from lightrag import QueryParam

    try:
        body = await request.json()
    except json.JSONDecodeError:
        return web.json_response(
            {"error": "Invalid JSON body"}, status=400
        )

    query_text = body.get("query", "").strip()
    if not query_text:
        return web.json_response(
            {"error": "Missing 'query' field"}, status=400
        )

    mode = body.get("mode", "hybrid")
    if mode not in ("naive", "local", "global", "hybrid", "mix"):
        return web.json_response(
            {"error": f"Invalid mode '{mode}'. Use: naive, local, global, hybrid, mix"},
            status=400,
        )

    top_k = body.get("top_k", 60)

    try:
        result = await rag.aquery(
            query_text,
            param=QueryParam(mode=mode, top_k=top_k),
        )
    except Exception as e:
        return web.json_response(
            {"error": f"Query failed: {str(e)}"}, status=500
        )

    return web.json_response({
        "query": query_text,
        "mode": mode,
        "result": result,
    })


async def handle_health(request: web.Request) -> web.Response:
    """Health check endpoint."""
    return web.json_response({"status": "ok", "service": "tolstoy-lightrag"})


async def handle_stats(request: web.Request) -> web.Response:
    """Return index statistics."""
    stats = {"lightrag_dir": str(LIGHTRAG_DIR)}

    # Sync state
    if SYNC_STATE_FILE.exists():
        sync_state = json.loads(SYNC_STATE_FILE.read_text(encoding="utf-8"))
        stats["sync"] = sync_state

    # File counts
    if LIGHTRAG_DIR.exists():
        files = list(LIGHTRAG_DIR.iterdir())
        stats["index_files"] = len(files)
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        stats["index_size_mb"] = round(total_size / (1024 * 1024), 2)

    return web.json_response(stats)


async def init_app() -> web.Application:
    """Initialize the web application and LightRAG instance."""
    global rag
    rag = create_rag()
    await rag.initialize_storages()
    print(f"LightRAG initialized from: {LIGHTRAG_DIR}")

    app = web.Application()
    app.router.add_post("/query", handle_query)
    app.router.add_get("/health", handle_health)
    app.router.add_get("/stats", handle_stats)
    return app


def main():
    parser = argparse.ArgumentParser(
        description="Local query API server for LightRAG."
    )
    parser.add_argument(
        "--port", type=int, default=API_PORT, help=f"Port to listen on (default: {API_PORT})"
    )
    parser.add_argument(
        "--host", default=API_HOST, help=f"Host to bind to (default: {API_HOST})"
    )
    args = parser.parse_args()

    app = asyncio.get_event_loop().run_until_complete(init_app())
    print(f"Starting LightRAG query API on http://{args.host}:{args.port}")
    print(f"  POST /query  — query the knowledge graph")
    print(f"  GET  /health — health check")
    print(f"  GET  /stats  — index statistics")
    web.run_app(app, host=args.host, port=args.port, print=None)


if __name__ == "__main__":
    main()
