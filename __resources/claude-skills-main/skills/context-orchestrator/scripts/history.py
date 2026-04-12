#!/usr/bin/env python3
"""
Context Extraction History Manager

Logs context extractions for future reference, pattern analysis, and debugging.
Maintains a searchable history of what context was retrieved and when.
"""

import json
import hashlib
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import re

HISTORY_DIR = Path.home() / ".claude" / ".context-cache" / "history"
HISTORY_FILE = HISTORY_DIR / "extractions.jsonl"
INDEX_FILE = HISTORY_DIR / "index.json"

# Configuration
MAX_ENTRIES = 500
MAX_AGE_DAYS = 90
MAX_CONTENT_LENGTH = 5000  # Truncate long content


def ensure_history_dir():
    """Ensure history directory exists."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def generate_id() -> str:
    """Generate unique extraction ID."""
    return hashlib.md5(f"{datetime.now().isoformat()}{os.urandom(8).hex()}".encode()).hexdigest()[:12]


def log_extraction(
    source: str,
    query: str,
    command: str,
    result: Any,
    metadata: Optional[Dict] = None
) -> Dict:
    """
    Log a context extraction event.

    Args:
        source: CLI source (limitless, research, pieces)
        query: User's original query
        command: Executed CLI command
        result: Extraction result (will be truncated if too long)
        metadata: Optional additional metadata

    Returns:
        The logged entry
    """
    ensure_history_dir()

    # Truncate long results
    result_str = json.dumps(result) if isinstance(result, (dict, list)) else str(result)
    if len(result_str) > MAX_CONTENT_LENGTH:
        result_str = result_str[:MAX_CONTENT_LENGTH] + "... [truncated]"
        result = {"truncated": True, "preview": result_str}

    entry = {
        "id": generate_id(),
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "query": query,
        "command": command,
        "result": result,
        "metadata": metadata or {},
        "tags": _extract_tags(query, source),
    }

    # Append to JSONL
    with open(HISTORY_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Update index
    _update_index(entry)

    # Enforce retention
    _enforce_retention()

    return entry


def _extract_tags(query: str, source: str) -> List[str]:
    """Extract tags from query for indexing."""
    tags = [source]

    # Add domain tags based on patterns
    if re.search(r'\b(auth|login|session)\b', query, re.I):
        tags.append("authentication")
    if re.search(r'\b(api|endpoint|rest)\b', query, re.I):
        tags.append("api")
    if re.search(r'\b(db|database|sql)\b', query, re.I):
        tags.append("database")
    if re.search(r'\b(test|testing|spec)\b', query, re.I):
        tags.append("testing")
    if re.search(r'\b(error|bug|fix)\b', query, re.I):
        tags.append("debugging")
    if re.search(r'\b(meeting|call|discussion)\b', query, re.I):
        tags.append("meeting")
    if re.search(r'\b(doc|documentation|guide)\b', query, re.I):
        tags.append("documentation")

    return tags


def _update_index(entry: Dict):
    """Update the search index with new entry."""
    ensure_history_dir()

    index = {"entries": [], "by_source": {}, "by_tag": {}, "updated_at": None}
    if INDEX_FILE.exists():
        try:
            index = json.loads(INDEX_FILE.read_text())
        except json.JSONDecodeError:
            pass

    # Add to entries list (just IDs for lookup)
    index["entries"].append({
        "id": entry["id"],
        "timestamp": entry["timestamp"],
        "source": entry["source"],
        "query_preview": entry["query"][:100],
    })

    # Index by source
    source = entry["source"]
    if source not in index["by_source"]:
        index["by_source"][source] = []
    index["by_source"][source].append(entry["id"])

    # Index by tags
    for tag in entry.get("tags", []):
        if tag not in index["by_tag"]:
            index["by_tag"][tag] = []
        index["by_tag"][tag].append(entry["id"])

    index["updated_at"] = datetime.now().isoformat()

    INDEX_FILE.write_text(json.dumps(index, indent=2))


def _enforce_retention():
    """Enforce retention policy."""
    if not HISTORY_FILE.exists():
        return

    lines = HISTORY_FILE.read_text().strip().split("\n")
    if len(lines) <= MAX_ENTRIES:
        return

    # Keep most recent
    lines = lines[-MAX_ENTRIES:]
    HISTORY_FILE.write_text("\n".join(lines) + "\n")


def search_history(
    query: Optional[str] = None,
    source: Optional[str] = None,
    tag: Optional[str] = None,
    since: Optional[str] = None,
    limit: int = 20
) -> List[Dict]:
    """
    Search extraction history.

    Args:
        query: Text search in queries
        source: Filter by source (limitless, research, pieces)
        tag: Filter by tag
        since: ISO8601 timestamp to filter by
        limit: Max results

    Returns:
        List of matching entries
    """
    ensure_history_dir()

    if not HISTORY_FILE.exists():
        return []

    results = []
    since_dt = datetime.fromisoformat(since) if since else None

    for line in HISTORY_FILE.read_text().strip().split("\n"):
        if not line:
            continue
        try:
            entry = json.loads(line)

            # Apply filters
            if source and entry.get("source") != source:
                continue
            if tag and tag not in entry.get("tags", []):
                continue
            if since_dt:
                entry_dt = datetime.fromisoformat(entry["timestamp"])
                if entry_dt < since_dt:
                    continue
            if query:
                if query.lower() not in entry.get("query", "").lower():
                    continue

            results.append(entry)
        except json.JSONDecodeError:
            continue

    return results[-limit:]


def get_entry(entry_id: str) -> Optional[Dict]:
    """Get a specific entry by ID."""
    ensure_history_dir()

    if not HISTORY_FILE.exists():
        return None

    for line in HISTORY_FILE.read_text().strip().split("\n"):
        if not line:
            continue
        try:
            entry = json.loads(line)
            if entry.get("id") == entry_id:
                return entry
        except json.JSONDecodeError:
            continue

    return None


def get_recent(source: Optional[str] = None, limit: int = 10) -> List[Dict]:
    """Get most recent extractions."""
    return search_history(source=source, limit=limit)


def get_statistics() -> Dict:
    """Get history statistics."""
    ensure_history_dir()

    if not HISTORY_FILE.exists():
        return {"error": "No history data"}

    stats = {
        "total_entries": 0,
        "by_source": {},
        "by_tag": {},
        "time_range": {"earliest": None, "latest": None},
        "avg_queries_per_day": 0,
    }

    entries = []
    for line in HISTORY_FILE.read_text().strip().split("\n"):
        if not line:
            continue
        try:
            entry = json.loads(line)
            entries.append(entry)

            source = entry.get("source", "unknown")
            stats["by_source"][source] = stats["by_source"].get(source, 0) + 1

            for tag in entry.get("tags", []):
                stats["by_tag"][tag] = stats["by_tag"].get(tag, 0) + 1
        except json.JSONDecodeError:
            continue

    stats["total_entries"] = len(entries)

    if entries:
        stats["time_range"]["earliest"] = entries[0]["timestamp"]
        stats["time_range"]["latest"] = entries[-1]["timestamp"]

        # Calculate average per day
        earliest = datetime.fromisoformat(entries[0]["timestamp"])
        latest = datetime.fromisoformat(entries[-1]["timestamp"])
        days = max((latest - earliest).days, 1)
        stats["avg_queries_per_day"] = round(len(entries) / days, 1)

    return stats


def export_history(
    format: str = "json",
    since: Optional[str] = None,
    source: Optional[str] = None
) -> str:
    """Export history in specified format."""
    entries = search_history(source=source, since=since, limit=MAX_ENTRIES)

    if format == "json":
        return json.dumps(entries, indent=2)
    elif format == "csv":
        lines = ["id,timestamp,source,query,tags"]
        for e in entries:
            query = e.get("query", "").replace('"', '""')[:100]
            tags = "|".join(e.get("tags", []))
            lines.append(f'"{e["id"]}","{e["timestamp"]}","{e["source"]}","{query}","{tags}"')
        return "\n".join(lines)
    elif format == "markdown":
        lines = ["# Context Extraction History\n"]
        for e in entries:
            lines.append(f"## {e['timestamp']}")
            lines.append(f"- **Source**: {e['source']}")
            lines.append(f"- **Query**: {e['query']}")
            lines.append(f"- **Tags**: {', '.join(e.get('tags', []))}")
            lines.append("")
        return "\n".join(lines)
    else:
        return json.dumps(entries, indent=2)


def clear_history(older_than_days: Optional[int] = None):
    """Clear history data."""
    ensure_history_dir()

    if older_than_days is None:
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
        if INDEX_FILE.exists():
            INDEX_FILE.unlink()
        return {"status": "cleared", "scope": "all"}

    if not HISTORY_FILE.exists():
        return {"status": "no_data"}

    cutoff = datetime.now() - timedelta(days=older_than_days)
    kept = []
    removed = 0

    for line in HISTORY_FILE.read_text().strip().split("\n"):
        if not line:
            continue
        try:
            entry = json.loads(line)
            entry_dt = datetime.fromisoformat(entry["timestamp"])
            if entry_dt >= cutoff:
                kept.append(line)
            else:
                removed += 1
        except (json.JSONDecodeError, KeyError):
            continue

    HISTORY_FILE.write_text("\n".join(kept) + "\n" if kept else "")
    return {"status": "cleared", "removed": removed, "kept": len(kept)}


def main():
    """CLI interface."""
    if len(sys.argv) < 2:
        print("Usage: history.py <command> [args]")
        print("Commands: log, search, get, recent, stats, export, clear")
        sys.exit(1)

    command = sys.argv[1]

    if command == "log":
        if len(sys.argv) < 5:
            print("Usage: history.py log <source> <query> <command> [result_json]")
            sys.exit(1)
        source = sys.argv[2]
        query = sys.argv[3]
        cmd = sys.argv[4]
        result = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {}
        entry = log_extraction(source, query, cmd, result)
        print(json.dumps({"status": "logged", "id": entry["id"]}))

    elif command == "search":
        kwargs = {}
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--source" and i + 1 < len(sys.argv):
                kwargs["source"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--tag" and i + 1 < len(sys.argv):
                kwargs["tag"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--query" and i + 1 < len(sys.argv):
                kwargs["query"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
                kwargs["limit"] = int(sys.argv[i + 1])
                i += 2
            else:
                i += 1
        results = search_history(**kwargs)
        print(json.dumps(results, indent=2))

    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: history.py get <entry_id>")
            sys.exit(1)
        entry = get_entry(sys.argv[2])
        if entry:
            print(json.dumps(entry, indent=2))
        else:
            print(json.dumps({"error": "Entry not found"}))

    elif command == "recent":
        source = sys.argv[2] if len(sys.argv) > 2 else None
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        results = get_recent(source, limit)
        print(json.dumps(results, indent=2))

    elif command == "stats":
        stats = get_statistics()
        print(json.dumps(stats, indent=2))

    elif command == "export":
        format = sys.argv[2] if len(sys.argv) > 2 else "json"
        output = export_history(format=format)
        print(output)

    elif command == "clear":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else None
        result = clear_history(days)
        print(json.dumps(result))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
