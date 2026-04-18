#!/usr/bin/env python3
"""
Incremental sync: re-index only files changed since last run.

Designed to run as a nightly cron job or on-demand after editing sessions.

Usage:
    python sync.py              # Sync changed files
    python sync.py --dry-run    # Show what would be synced
    python sync.py --full       # Force full re-index (same as ingest.py)

State is stored in lightrag/data/sync_state.json.
"""

import asyncio
import argparse
import json
import time

from config import SYNC_STATE_FILE
from vault_reader import collect_documents, collect_changed_documents


def load_sync_state() -> dict:
    """Load the last sync timestamp."""
    if SYNC_STATE_FILE.exists():
        return json.loads(SYNC_STATE_FILE.read_text(encoding="utf-8"))
    return {"last_sync": 0.0, "files_indexed": 0}


def save_sync_state(state: dict) -> None:
    """Save sync state to disk."""
    SYNC_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    SYNC_STATE_FILE.write_text(
        json.dumps(state, indent=2), encoding="utf-8"
    )


async def sync(dry_run: bool = False, full: bool = False) -> None:
    """Sync changed vault files to LightRAG."""
    state = load_sync_state()
    last_sync = state.get("last_sync", 0.0)

    if full or last_sync == 0.0:
        print("Full sync requested." if full else "No previous sync found — running full index.")
        documents = collect_documents()
    else:
        from datetime import datetime

        last_dt = datetime.fromtimestamp(last_sync)
        print(f"Last sync: {last_dt.isoformat()}")
        documents = collect_changed_documents(last_sync)

    if not documents:
        print("No changed documents found. Everything is up to date.")
        return

    print(f"Found {len(documents)} document(s) to sync.")

    if dry_run:
        for doc in sorted(documents, key=lambda d: d.rel_path):
            size_kb = len(doc.content.encode("utf-8")) / 1024
            print(f"  {doc.rel_path}  ({size_kb:.1f} KB)")
        print(f"\nDry run complete. {len(documents)} document(s) would be synced.")
        return

    from rag import create_rag

    rag = create_rag()
    await rag.initialize_storages()

    start_time = time.time()
    total = len(documents)
    errors = 0

    for i, doc in enumerate(sorted(documents, key=lambda d: d.rel_path), 1):
        print(f"  [{i}/{total}] Syncing: {doc.rel_path}")
        try:
            await rag.ainsert(doc.content)
        except Exception as e:
            print(f"    ERROR: {e}")
            errors += 1
            continue

    elapsed = time.time() - start_time

    # Update sync state
    new_state = {
        "last_sync": time.time(),
        "files_indexed": state.get("files_indexed", 0) + total - errors,
        "last_run_files": total,
        "last_run_errors": errors,
        "last_run_seconds": round(elapsed, 1),
    }
    save_sync_state(new_state)

    print(f"\nSynced {total - errors}/{total} documents in {elapsed:.1f}s.")
    if errors:
        print(f"  {errors} error(s) — check output above.")


def main():
    parser = argparse.ArgumentParser(
        description="Incremental sync of vault files to LightRAG."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be synced without doing it.",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Force a full re-index (ignore last sync timestamp).",
    )
    args = parser.parse_args()
    asyncio.run(sync(dry_run=args.dry_run, full=args.full))


if __name__ == "__main__":
    main()
