#!/usr/bin/env python3
"""
Parallel Source Extraction — Concurrent CLI Orchestration

Executes source extraction across all available CLIs in parallel,
merges results, and calculates diversity metrics.
"""

import asyncio
import json
import hashlib
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from enum import Enum


class SourceType(Enum):
    PERSONAL = "personal"       # limitless
    LOCAL = "local"            # pieces
    TEXTBOOK = "textbook"      # pdf-search/pdf-brain
    AUTHORITATIVE = "authoritative"  # research


@dataclass
class Source:
    content: str
    source_type: SourceType
    title: Optional[str] = None
    url: Optional[str] = None
    page: Optional[int] = None
    citation: Optional[str] = None
    confidence: float = 0.8
    content_hash: str = ""

    def __post_init__(self):
        if not self.content_hash:
            self.content_hash = hashlib.md5(self.content.encode()).hexdigest()[:16]


@dataclass
class ExtractionResult:
    sources: List[Source]
    source_distribution: Dict[str, int]
    diversity_score: float
    total_sources: int
    unique_sources: int
    extraction_time_ms: float
    errors: List[Dict[str, str]] = field(default_factory=list)


async def extract_limitless(query: str, limit: int = 5, timeout: float = 10.0) -> List[Source]:
    """Extract personal context from limitless."""
    try:
        proc = await asyncio.create_subprocess_shell(
            f'limitless lifelogs search "{query}" --limit {limit} --json',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

        if proc.returncode != 0:
            return []

        data = json.loads(stdout.decode())
        sources = []

        for item in data if isinstance(data, list) else [data]:
            sources.append(Source(
                content=item.get("markdown", ""),
                source_type=SourceType.PERSONAL,
                title=item.get("title"),
                confidence=0.75
            ))

        return sources

    except (asyncio.TimeoutError, json.JSONDecodeError, Exception):
        return []


async def extract_pieces(query: str, timeout: float = 8.0) -> List[Source]:
    """Extract local context from pieces LTM."""
    try:
        proc = await asyncio.create_subprocess_shell(
            f'echo "" | pieces ask "{query}" --ltm',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

        if proc.returncode != 0:
            return []

        content = stdout.decode().strip()
        if content:
            return [Source(
                content=content,
                source_type=SourceType.LOCAL,
                title="Pieces LTM Response",
                confidence=0.70
            )]

        return []

    except (asyncio.TimeoutError, Exception):
        return []


async def extract_textbook(query: str, limit: int = 10, tags: str = "", timeout: float = 5.0) -> List[Source]:
    """Extract textbook chunks from pdf-search."""
    try:
        cmd = f'pdf-search "{query}" --limit {limit}'
        if tags:
            cmd += f' --tags {tags}'

        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

        if proc.returncode != 0:
            # Fallback to pdf-brain
            return await extract_textbook_fallback(query, limit, timeout)

        data = json.loads(stdout.decode())
        sources = []

        results = data.get("results", []) if isinstance(data, dict) else data
        for chunk in results:
            sources.append(Source(
                content=chunk.get("content", ""),
                source_type=SourceType.TEXTBOOK,
                title=chunk.get("document"),
                page=chunk.get("page"),
                citation=f'{chunk.get("document", "Unknown")}, p.{chunk.get("page", "?")}',
                confidence=min(chunk.get("score", 0.8), 1.0)
            ))

        return sources

    except (asyncio.TimeoutError, json.JSONDecodeError, Exception):
        return await extract_textbook_fallback(query, limit, timeout)


async def extract_textbook_fallback(query: str, limit: int, timeout: float) -> List[Source]:
    """Fallback to pdf-brain if pdf-search fails."""
    try:
        proc = await asyncio.create_subprocess_shell(
            f'pdf-brain search "{query}" --limit {limit}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

        if proc.returncode != 0:
            return []

        data = json.loads(stdout.decode())
        sources = []

        results = data.get("results", []) if isinstance(data, dict) else data
        for chunk in results:
            sources.append(Source(
                content=chunk.get("content", ""),
                source_type=SourceType.TEXTBOOK,
                title=chunk.get("document"),
                page=chunk.get("page"),
                citation=f'{chunk.get("document", "Unknown")}, p.{chunk.get("page", "?")}',
                confidence=min(chunk.get("score", 0.8), 1.0)
            ))

        return sources

    except Exception:
        return []


async def extract_research(query: str, mode: str = "pex-grounding",
                          specialty: str = "", timeout: float = 15.0) -> List[Source]:
    """Extract authoritative sources from research CLI."""
    try:
        cmd = f'research {mode} -t "{query}" --format json'
        if specialty and mode == "pex-grounding":
            cmd += f' --specialty {specialty}'

        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

        if proc.returncode != 0:
            return []

        data = json.loads(stdout.decode())
        sources = []

        results = data.get("results", []) if isinstance(data, dict) else data
        for item in results:
            sources.append(Source(
                content=item.get("content", ""),
                source_type=SourceType.AUTHORITATIVE,
                title=item.get("title"),
                url=item.get("url"),
                citation=format_research_citation(item),
                confidence=item.get("confidence", 0.85)
            ))

        return sources

    except (asyncio.TimeoutError, json.JSONDecodeError, Exception):
        return []


def format_research_citation(item: Dict[str, Any]) -> str:
    """Format a research result as a citation."""
    title = item.get("title", "Unknown")
    url = item.get("url", "")
    date = item.get("date", "")

    if url:
        return f'{title}. {url}'
    return title


def deduplicate_sources(sources: List[Source]) -> List[Source]:
    """Remove duplicate sources by content hash."""
    seen = set()
    unique = []

    for source in sources:
        if source.content_hash not in seen:
            seen.add(source.content_hash)
            unique.append(source)

    return unique


def calculate_diversity(sources: List[Source]) -> float:
    """Calculate source type diversity score (0-1)."""
    if not sources:
        return 0.0

    type_counts = {}
    for source in sources:
        type_name = source.source_type.value
        type_counts[type_name] = type_counts.get(type_name, 0) + 1

    # Shannon diversity index normalized
    total = len(sources)
    max_types = 4  # personal, local, textbook, authoritative

    if len(type_counts) == 0:
        return 0.0

    # Evenness score
    proportions = [count / total for count in type_counts.values()]
    import math
    entropy = -sum(p * math.log(p) for p in proportions if p > 0)
    max_entropy = math.log(max_types)

    # Combine type coverage and evenness
    type_coverage = len(type_counts) / max_types
    evenness = entropy / max_entropy if max_entropy > 0 else 0

    return round((type_coverage * 0.6 + evenness * 0.4), 3)


async def extract_all(
    query: str,
    limit: int = 10,
    tags: str = "",
    specialty: str = "",
    parallel: bool = True
) -> ExtractionResult:
    """Extract from all sources, optionally in parallel."""
    import time
    start = time.time()

    errors = []

    if parallel:
        # Run all extractions concurrently
        results = await asyncio.gather(
            extract_limitless(query, limit=5),
            extract_pieces(query),
            extract_textbook(query, limit=limit, tags=tags),
            extract_research(query, specialty=specialty),
            return_exceptions=True
        )

        all_sources = []
        source_names = ["limitless", "pieces", "pdf-search", "research"]

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                errors.append({"cli": source_names[i], "error": str(result)})
            elif isinstance(result, list):
                all_sources.extend(result)

    else:
        # Sequential extraction (for debugging)
        all_sources = []
        all_sources.extend(await extract_limitless(query, limit=5))
        all_sources.extend(await extract_pieces(query))
        all_sources.extend(await extract_textbook(query, limit=limit, tags=tags))
        all_sources.extend(await extract_research(query, specialty=specialty))

    # Deduplicate
    unique_sources = deduplicate_sources(all_sources)

    # Calculate distribution
    distribution = {}
    for source in unique_sources:
        type_name = source.source_type.value
        distribution[type_name] = distribution.get(type_name, 0) + 1

    elapsed = (time.time() - start) * 1000

    return ExtractionResult(
        sources=unique_sources,
        source_distribution=distribution,
        diversity_score=calculate_diversity(unique_sources),
        total_sources=len(all_sources),
        unique_sources=len(unique_sources),
        extraction_time_ms=round(elapsed, 2),
        errors=errors
    )


def format_output(result: ExtractionResult, format: str = "json") -> str:
    """Format extraction result for output."""

    if format == "json":
        output = {
            "extraction_time_ms": result.extraction_time_ms,
            "total_sources": result.total_sources,
            "unique_sources": result.unique_sources,
            "diversity_score": result.diversity_score,
            "distribution": result.source_distribution,
            "errors": result.errors,
            "sources": [
                {
                    "type": s.source_type.value,
                    "title": s.title,
                    "content": s.content[:500] + "..." if len(s.content) > 500 else s.content,
                    "citation": s.citation,
                    "confidence": s.confidence,
                    "hash": s.content_hash
                }
                for s in result.sources
            ]
        }
        return json.dumps(output, indent=2)

    elif format == "summary":
        lines = [
            f"Extraction complete in {result.extraction_time_ms}ms",
            f"  Total sources: {result.total_sources}",
            f"  Unique sources: {result.unique_sources}",
            f"  Diversity score: {result.diversity_score}",
            f"  Distribution: {result.source_distribution}"
        ]
        if result.errors:
            lines.append(f"  Errors: {len(result.errors)}")
        return "\n".join(lines)

    return str(result)


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Parallel Source Extraction")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Max results per source")
    parser.add_argument("--tags", default="", help="Textbook tags filter")
    parser.add_argument("--specialty", default="", help="Medical specialty")
    parser.add_argument("--format", choices=["json", "summary"], default="json")
    parser.add_argument("--sequential", action="store_true", help="Run sequentially (debug)")

    args = parser.parse_args()

    result = await extract_all(
        args.query,
        limit=args.limit,
        tags=args.tags,
        specialty=args.specialty,
        parallel=not args.sequential
    )

    print(format_output(result, args.format))


if __name__ == "__main__":
    asyncio.run(main())
