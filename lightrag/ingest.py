#!/usr/bin/env python3
"""
Full ingestion: index all vault markdown files into LightRAG.

Run this once for the initial batch indexing, or to rebuild from scratch.

Usage:
    python ingest.py              # Index all documents
    python ingest.py --dry-run    # Show what would be indexed without doing it
"""

import asyncio
import argparse
import time

from vault_reader import collect_documents


async def ingest_all(dry_run: bool = False) -> None:
    """Read all vault documents and insert them into LightRAG."""
    documents = collect_documents()

    if not documents:
        print("No documents found to index.")
        return

    print(f"Found {len(documents)} documents to index.")

    if dry_run:
        for doc in sorted(documents, key=lambda d: d.rel_path):
            size_kb = len(doc.content.encode("utf-8")) / 1024
            print(f"  {doc.rel_path}  ({size_kb:.1f} KB)")
        print(f"\nDry run complete. {len(documents)} documents would be indexed.")
        return

    from rag import create_rag

    rag = create_rag()
    await rag.initialize_storages()

    total = len(documents)
    start_time = time.time()

    for i, doc in enumerate(sorted(documents, key=lambda d: d.rel_path), 1):
        print(f"  [{i}/{total}] Indexing: {doc.rel_path}")
        try:
            await rag.ainsert(doc.content)
        except Exception as e:
            print(f"    ERROR: {e}")
            continue

    elapsed = time.time() - start_time
    print(f"\nDone. Indexed {total} documents in {elapsed:.1f}s.")
    print(f"LightRAG data stored in: {rag.working_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Index all vault markdown files into LightRAG."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be indexed without actually doing it.",
    )
    args = parser.parse_args()
    asyncio.run(ingest_all(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
