#!/usr/bin/env python3
"""
Context Orchestrator Metrics & Logging System

Tracks usage patterns, latency, and outcomes for context extraction operations.
Provides insights for optimization and debugging.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import defaultdict
import hashlib

METRICS_DIR = Path.home() / ".claude" / ".context-cache" / "metrics"
METRICS_FILE = METRICS_DIR / "usage.jsonl"
SUMMARY_FILE = METRICS_DIR / "summary.json"

# Retention policy
MAX_EVENTS = 1000
MAX_AGE_DAYS = 30


def ensure_metrics_dir():
    """Ensure metrics directory exists."""
    METRICS_DIR.mkdir(parents=True, exist_ok=True)


def log_event(event_type: str, data: Dict[str, Any]) -> Dict:
    """
    Log a context extraction event.

    Event types:
    - intent_detected: Hook detected context-relevant intent
    - source_selected: CLI source(s) selected for extraction
    - cli_invoked: CLI command executed
    - cli_completed: CLI command finished (success/error)
    - cache_hit: Result served from cache
    - cache_miss: Cache miss, CLI invoked
    - extraction_complete: Full extraction finished
    """
    ensure_metrics_dir()

    event = {
        "id": hashlib.md5(f"{datetime.now().isoformat()}{event_type}".encode()).hexdigest()[:12],
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "data": data,
    }

    # Append to JSONL file
    with open(METRICS_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

    # Enforce retention
    _enforce_retention()

    return event


def _enforce_retention():
    """Enforce retention policy on metrics file."""
    if not METRICS_FILE.exists():
        return

    lines = METRICS_FILE.read_text().strip().split("\n")
    if len(lines) <= MAX_EVENTS:
        return

    # Keep only most recent events
    lines = lines[-MAX_EVENTS:]
    METRICS_FILE.write_text("\n".join(lines) + "\n")


def get_events(
    event_type: Optional[str] = None,
    source: Optional[str] = None,
    since: Optional[datetime] = None,
    limit: int = 100
) -> List[Dict]:
    """Retrieve events with optional filtering."""
    ensure_metrics_dir()

    if not METRICS_FILE.exists():
        return []

    events = []
    for line in METRICS_FILE.read_text().strip().split("\n"):
        if not line:
            continue
        try:
            event = json.loads(line)

            # Apply filters
            if event_type and event.get("event_type") != event_type:
                continue
            if source and event.get("data", {}).get("source") != source:
                continue
            if since:
                event_time = datetime.fromisoformat(event["timestamp"])
                if event_time < since:
                    continue

            events.append(event)
        except json.JSONDecodeError:
            continue

    return events[-limit:]


def calculate_summary() -> Dict:
    """Calculate usage summary statistics."""
    ensure_metrics_dir()

    if not METRICS_FILE.exists():
        return {"error": "No metrics data available"}

    events = get_events(limit=MAX_EVENTS)

    if not events:
        return {"error": "No events found"}

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_events": len(events),
        "event_counts": defaultdict(int),
        "source_usage": defaultdict(int),
        "cache_stats": {"hits": 0, "misses": 0, "hit_rate": 0.0},
        "latency_stats": defaultdict(list),
        "error_count": 0,
        "time_range": {
            "earliest": events[0]["timestamp"] if events else None,
            "latest": events[-1]["timestamp"] if events else None,
        },
    }

    for event in events:
        event_type = event.get("event_type", "unknown")
        data = event.get("data", {})

        # Count events
        summary["event_counts"][event_type] += 1

        # Track source usage
        if source := data.get("source"):
            summary["source_usage"][source] += 1

        # Track cache stats
        if event_type == "cache_hit":
            summary["cache_stats"]["hits"] += 1
        elif event_type == "cache_miss":
            summary["cache_stats"]["misses"] += 1

        # Track latency
        if latency := data.get("latency_ms"):
            source = data.get("source", "unknown")
            summary["latency_stats"][source].append(latency)

        # Count errors
        if data.get("error"):
            summary["error_count"] += 1

    # Calculate cache hit rate
    total_cache = summary["cache_stats"]["hits"] + summary["cache_stats"]["misses"]
    if total_cache > 0:
        summary["cache_stats"]["hit_rate"] = round(
            summary["cache_stats"]["hits"] / total_cache * 100, 1
        )

    # Calculate latency percentiles
    latency_summary = {}
    for source, latencies in summary["latency_stats"].items():
        if latencies:
            sorted_lat = sorted(latencies)
            latency_summary[source] = {
                "count": len(latencies),
                "min_ms": min(latencies),
                "max_ms": max(latencies),
                "avg_ms": round(sum(latencies) / len(latencies), 1),
                "p50_ms": sorted_lat[len(sorted_lat) // 2],
                "p90_ms": sorted_lat[int(len(sorted_lat) * 0.9)] if len(sorted_lat) >= 10 else sorted_lat[-1],
            }
    summary["latency_stats"] = latency_summary

    # Convert defaultdicts
    summary["event_counts"] = dict(summary["event_counts"])
    summary["source_usage"] = dict(summary["source_usage"])

    # Save summary
    with open(SUMMARY_FILE, "w") as f:
        json.dump(summary, f, indent=2)

    return summary


def get_recommendations() -> List[str]:
    """Generate optimization recommendations based on metrics."""
    summary = calculate_summary()
    recommendations = []

    if "error" in summary:
        return ["Insufficient data for recommendations"]

    # Cache hit rate recommendations
    hit_rate = summary["cache_stats"]["hit_rate"]
    if hit_rate < 20:
        recommendations.append(
            f"Low cache hit rate ({hit_rate}%). Consider increasing TTLs or "
            "reducing query variation."
        )
    elif hit_rate > 80:
        recommendations.append(
            f"High cache hit rate ({hit_rate}%). Cache is working well."
        )

    # Source usage balance
    source_usage = summary["source_usage"]
    if source_usage:
        total = sum(source_usage.values())
        for source, count in source_usage.items():
            pct = count / total * 100 if total > 0 else 0
            if pct > 70:
                recommendations.append(
                    f"Heavy reliance on {source} ({pct:.0f}%). "
                    "Consider diversifying context sources."
                )

    # Latency recommendations
    for source, stats in summary.get("latency_stats", {}).items():
        if stats.get("p90_ms", 0) > 5000:
            recommendations.append(
                f"{source} has high P90 latency ({stats['p90_ms']}ms). "
                "Consider timeout adjustments or caching."
            )

    # Error rate
    if summary["total_events"] > 0:
        error_rate = summary["error_count"] / summary["total_events"] * 100
        if error_rate > 10:
            recommendations.append(
                f"High error rate ({error_rate:.1f}%). "
                "Check CLI availability and connectivity."
            )

    return recommendations if recommendations else ["No recommendations - system performing well"]


def clear_metrics(older_than_days: Optional[int] = None):
    """Clear metrics data."""
    ensure_metrics_dir()

    if older_than_days is None:
        # Clear all
        if METRICS_FILE.exists():
            METRICS_FILE.unlink()
        if SUMMARY_FILE.exists():
            SUMMARY_FILE.unlink()
        return {"status": "cleared", "scope": "all"}

    # Clear old events
    if not METRICS_FILE.exists():
        return {"status": "no_data"}

    cutoff = datetime.now() - timedelta(days=older_than_days)
    kept_lines = []
    removed = 0

    for line in METRICS_FILE.read_text().strip().split("\n"):
        if not line:
            continue
        try:
            event = json.loads(line)
            event_time = datetime.fromisoformat(event["timestamp"])
            if event_time >= cutoff:
                kept_lines.append(line)
            else:
                removed += 1
        except (json.JSONDecodeError, KeyError):
            continue

    METRICS_FILE.write_text("\n".join(kept_lines) + "\n" if kept_lines else "")
    return {"status": "cleared", "removed": removed, "kept": len(kept_lines)}


def main():
    """CLI interface for metrics."""
    if len(sys.argv) < 2:
        print("Usage: metrics.py <command> [args]")
        print("Commands: log, events, summary, recommendations, clear")
        sys.exit(1)

    command = sys.argv[1]

    if command == "log":
        if len(sys.argv) < 4:
            print("Usage: metrics.py log <event_type> <data_json>")
            sys.exit(1)
        event_type = sys.argv[2]
        data = json.loads(sys.argv[3])
        result = log_event(event_type, data)
        print(json.dumps(result))

    elif command == "events":
        event_type = sys.argv[2] if len(sys.argv) > 2 else None
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        events = get_events(event_type=event_type, limit=limit)
        print(json.dumps(events, indent=2))

    elif command == "summary":
        summary = calculate_summary()
        print(json.dumps(summary, indent=2))

    elif command == "recommendations":
        recs = get_recommendations()
        for i, rec in enumerate(recs, 1):
            print(f"{i}. {rec}")

    elif command == "clear":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else None
        result = clear_metrics(days)
        print(json.dumps(result))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
