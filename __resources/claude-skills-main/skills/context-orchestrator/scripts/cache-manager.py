#!/usr/bin/env python3
"""
Context Orchestrator Cache Manager

Manages session-based caching for context extraction results.
Supports TTL-based expiration and cache operations.
"""

import json
import hashlib
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Any, Dict

CACHE_DIR = Path.home() / ".claude" / ".context-cache"
CACHE_FILE = CACHE_DIR / "session-context.json"

# TTL configuration (in minutes)
TTL_CONFIG = {
    "limitless": 30,
    "research": 60,
    "pieces": 15,
}

MAX_ENTRIES = 50
MAX_CACHE_SIZE_MB = 5


def ensure_cache_dir():
    """Ensure cache directory exists."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def load_cache() -> Dict:
    """Load cache from disk."""
    ensure_cache_dir()
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return create_empty_cache()
    return create_empty_cache()


def save_cache(cache: Dict):
    """Save cache to disk."""
    ensure_cache_dir()
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2, default=str)


def create_empty_cache() -> Dict:
    """Create a new empty cache structure."""
    return {
        "session_id": hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12],
        "created_at": datetime.now().isoformat(),
        "sources": {
            "limitless": True,
            "research": True,
            "pieces": True,
        },
        "entries": {},
    }


def generate_key(source: str, query: str) -> str:
    """Generate cache key from source and query."""
    query_hash = hashlib.md5(query.lower().strip().encode()).hexdigest()[:8]
    return f"{source}:{query_hash}"


def is_expired(entry: Dict) -> bool:
    """Check if cache entry is expired."""
    if "cached_at" not in entry or "ttl_minutes" not in entry:
        return True

    cached_at = datetime.fromisoformat(entry["cached_at"])
    ttl = timedelta(minutes=entry["ttl_minutes"])
    return datetime.now() > cached_at + ttl


def get_cache(source: str, query: str) -> Optional[Any]:
    """Get cached result if available and not expired."""
    cache = load_cache()
    key = generate_key(source, query)

    if key in cache["entries"]:
        entry = cache["entries"][key]
        if not is_expired(entry):
            return entry.get("result")
        else:
            # Clean up expired entry
            del cache["entries"][key]
            save_cache(cache)

    return None


def set_cache(source: str, query: str, result: Any):
    """Store result in cache."""
    cache = load_cache()
    key = generate_key(source, query)

    # Enforce max entries (LRU-style: remove oldest)
    if len(cache["entries"]) >= MAX_ENTRIES:
        oldest_key = min(
            cache["entries"].keys(),
            key=lambda k: cache["entries"][k].get("cached_at", "")
        )
        del cache["entries"][oldest_key]

    cache["entries"][key] = {
        "source": source,
        "query": query,
        "result": result,
        "cached_at": datetime.now().isoformat(),
        "ttl_minutes": TTL_CONFIG.get(source, 30),
    }

    save_cache(cache)


def clear_cache(source: Optional[str] = None):
    """Clear cache entries. If source specified, only clear that source."""
    cache = load_cache()

    if source:
        cache["entries"] = {
            k: v for k, v in cache["entries"].items()
            if not k.startswith(f"{source}:")
        }
    else:
        cache["entries"] = {}

    save_cache(cache)


def cleanup_expired():
    """Remove all expired entries."""
    cache = load_cache()
    cache["entries"] = {
        k: v for k, v in cache["entries"].items()
        if not is_expired(v)
    }
    save_cache(cache)


def get_stats() -> Dict:
    """Get cache statistics."""
    cache = load_cache()
    entries = cache.get("entries", {})

    by_source = {"limitless": 0, "research": 0, "pieces": 0}
    expired_count = 0

    for entry in entries.values():
        source = entry.get("source", "unknown")
        if source in by_source:
            by_source[source] += 1
        if is_expired(entry):
            expired_count += 1

    cache_size = CACHE_FILE.stat().st_size if CACHE_FILE.exists() else 0

    return {
        "session_id": cache.get("session_id"),
        "created_at": cache.get("created_at"),
        "total_entries": len(entries),
        "by_source": by_source,
        "expired_entries": expired_count,
        "cache_size_kb": round(cache_size / 1024, 2),
    }


def main():
    """CLI interface for cache manager."""
    if len(sys.argv) < 2:
        print("Usage: cache-manager.py <command> [args]")
        print("Commands: init, get, set, clear, stats, cleanup")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        cache = create_empty_cache()
        save_cache(cache)
        print(json.dumps({"status": "initialized", "session_id": cache["session_id"]}))

    elif command == "get":
        if len(sys.argv) < 4:
            print("Usage: cache-manager.py get <source> <query>")
            sys.exit(1)
        source, query = sys.argv[2], sys.argv[3]
        result = get_cache(source, query)
        if result:
            print(json.dumps({"hit": True, "result": result}))
        else:
            print(json.dumps({"hit": False}))

    elif command == "set":
        if len(sys.argv) < 5:
            print("Usage: cache-manager.py set <source> <query> <result_json>")
            sys.exit(1)
        source, query, result_json = sys.argv[2], sys.argv[3], sys.argv[4]
        result = json.loads(result_json)
        set_cache(source, query, result)
        print(json.dumps({"status": "cached"}))

    elif command == "clear":
        source = sys.argv[2] if len(sys.argv) > 2 else None
        clear_cache(source)
        print(json.dumps({"status": "cleared", "source": source or "all"}))

    elif command == "stats":
        stats = get_stats()
        print(json.dumps(stats, indent=2))

    elif command == "cleanup":
        cleanup_expired()
        print(json.dumps({"status": "cleaned"}))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
