"""
Read and prepare vault markdown files for LightRAG ingestion.

Each document is identified by its path relative to the vault root.
Frontmatter is preserved as structured context for the knowledge graph.
"""

import re
from pathlib import Path
from dataclasses import dataclass

from config import CONTENT_DIRS, VAULT_ROOT, SKIP_FILENAMES, SKIP_DIRS


@dataclass
class VaultDocument:
    """A single markdown file from the vault."""

    path: Path  # Absolute path
    rel_path: str  # Relative to vault root (used as document ID)
    content: str  # Full file content including frontmatter


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def should_skip(path: Path) -> bool:
    """Check if a file should be skipped during indexing."""
    if path.name in SKIP_FILENAMES:
        return True
    if not path.suffix == ".md":
        return True
    # Skip files inside excluded directories
    for part in path.parts:
        if part in SKIP_DIRS:
            return True
    return False


def read_document(path: Path) -> VaultDocument | None:
    """Read a single markdown file and return a VaultDocument."""
    if should_skip(path):
        return None
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    if not content.strip():
        return None

    rel_path = str(path.relative_to(VAULT_ROOT))
    return VaultDocument(path=path, rel_path=rel_path, content=content)


def collect_documents() -> list[VaultDocument]:
    """Walk all content directories and collect indexable documents."""
    docs = []
    for content_dir in CONTENT_DIRS:
        if not content_dir.exists():
            continue
        for md_file in content_dir.rglob("*.md"):
            doc = read_document(md_file)
            if doc is not None:
                docs.append(doc)
    return docs


def collect_changed_documents(since_timestamp: float) -> list[VaultDocument]:
    """Collect documents modified after the given timestamp."""
    docs = []
    for content_dir in CONTENT_DIRS:
        if not content_dir.exists():
            continue
        for md_file in content_dir.rglob("*.md"):
            if md_file.stat().st_mtime <= since_timestamp:
                continue
            doc = read_document(md_file)
            if doc is not None:
                docs.append(doc)
    return docs


if __name__ == "__main__":
    # Quick test: list all documents that would be indexed
    documents = collect_documents()
    print(f"Found {len(documents)} documents to index:\n")
    for doc in sorted(documents, key=lambda d: d.rel_path):
        lines = doc.content.count("\n")
        print(f"  {doc.rel_path}  ({lines} lines)")
