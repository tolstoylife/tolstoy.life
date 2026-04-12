#!/usr/bin/env python3
"""
memory-manager.py - Advanced memory management for Obsidian skill

Usage:
    python memory-manager.py init           # Initialize memory file
    python memory-manager.py stats          # Show usage statistics
    python memory-manager.py learn "text"   # Add a learning entry
    python memory-manager.py export         # Export memory as JSON
    python memory-manager.py reset          # Reset memory (keep structure)
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

# Memory file location
MEMORY_FILE = Path.cwd() / ".claude" / "obsidian-memory.json"


def get_default_memory() -> dict:
    """Return default memory structure."""
    now = datetime.now(timezone.utc).isoformat() + "Z"
    return {
        "version": "1.0.0",
        "created": now,
        "lastUpdated": now,
        "sessions": {
            "total": 0,
            "lastSessionDate": None
        },
        "patterns": {
            "markdown": {
                "wikilinks": 0,
                "callouts": 0,
                "embeds": 0,
                "properties": 0,
                "tags": 0
            },
            "bases": {
                "filters": 0,
                "formulas": 0,
                "views": 0,
                "summaries": 0
            },
            "canvas": {
                "textNodes": 0,
                "fileNodes": 0,
                "linkNodes": 0,
                "groupNodes": 0,
                "edges": 0
            }
        },
        "userPreferences": {
            "preferredCalloutTypes": [],
            "commonProperties": [],
            "frequentFilters": [],
            "favoriteColors": [],
            "topMarkdownPatterns": [],
            "topBasesPatterns": [],
            "topCanvasPatterns": []
        },
        "learnings": [],
        "vaultContext": {
            "hasVault": False,
            "pluginsDetected": []
        }
    }


def load_memory() -> dict:
    """Load memory from file or create default."""
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return get_default_memory()
    return get_default_memory()


def save_memory(memory: dict) -> None:
    """Save memory to file."""
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    memory["lastUpdated"] = datetime.now(timezone.utc).isoformat() + "Z"
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, indent=2)


def init_memory() -> None:
    """Initialize memory file."""
    memory = get_default_memory()
    save_memory(memory)
    print(f"Memory initialized at {MEMORY_FILE}")


def show_stats() -> None:
    """Show usage statistics."""
    memory = load_memory()

    print("\n=== Obsidian Skill Memory Statistics ===\n")
    print(f"Version: {memory.get('version', 'unknown')}")
    print(f"Created: {memory.get('created', 'unknown')}")
    print(f"Last Updated: {memory.get('lastUpdated', 'unknown')}")
    print(f"Total Sessions: {memory['sessions']['total']}")

    # Pattern statistics
    print("\n--- Pattern Usage ---")

    for category, patterns in memory["patterns"].items():
        total = sum(patterns.values())
        if total > 0:
            print(f"\n{category.upper()}:")
            sorted_patterns = sorted(patterns.items(), key=lambda x: -x[1])
            for pattern, count in sorted_patterns:
                if count > 0:
                    bar = "█" * min(count, 20)
                    print(f"  {pattern:15} {count:5} {bar}")

    # Preferences
    prefs = memory.get("userPreferences", {})
    if any(prefs.get(k) for k in ["topMarkdownPatterns", "topBasesPatterns", "topCanvasPatterns"]):
        print("\n--- Derived Preferences ---")
        for key in ["topMarkdownPatterns", "topBasesPatterns", "topCanvasPatterns"]:
            if prefs.get(key):
                print(f"  {key}: {', '.join(prefs[key])}")

    # Vault context
    vault = memory.get("vaultContext", {})
    if vault.get("hasVault"):
        print("\n--- Vault Context ---")
        print(f"  Vault detected: Yes")
        if vault.get("pluginsDetected"):
            print(f"  Plugins: {', '.join(vault['pluginsDetected'])}")

    # Learnings
    learnings = memory.get("learnings", [])
    if learnings:
        print(f"\n--- Recent Learnings ({len(learnings)} total) ---")
        for learning in learnings[-5:]:
            timestamp = learning.get("timestamp", "")[:10]
            text = learning.get("text", "")[:60]
            print(f"  [{timestamp}] {text}...")


def add_learning(text: str) -> None:
    """Add a learning entry."""
    memory = load_memory()
    memory["learnings"].append({
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "text": text
    })
    save_memory(memory)
    print(f"Learning added: {text[:50]}...")


def export_memory() -> None:
    """Export memory as formatted JSON."""
    memory = load_memory()
    print(json.dumps(memory, indent=2))


def reset_memory() -> None:
    """Reset memory keeping structure."""
    memory = get_default_memory()
    save_memory(memory)
    print("Memory reset to defaults")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "init":
        init_memory()
    elif command == "stats":
        show_stats()
    elif command == "learn":
        if len(sys.argv) < 3:
            print("Usage: memory-manager.py learn 'learning text'")
            sys.exit(1)
        add_learning(sys.argv[2])
    elif command == "export":
        export_memory()
    elif command == "reset":
        reset_memory()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
