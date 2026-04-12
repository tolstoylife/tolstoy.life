#!/usr/bin/env python3
"""
Preflight Check — CLI Health Verification for Grounding Orchestrator

Verifies availability and health of all required CLIs before pipeline execution.
Returns structured status for pipeline decision-making.
"""

import asyncio
import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional


class Status(Enum):
    FULL = "FULL"           # All CLIs available
    DEGRADED = "DEGRADED"   # Partial availability
    CRITICAL = "CRITICAL"   # Insufficient CLIs


@dataclass
class CLICheck:
    name: str
    available: bool
    version: Optional[str] = None
    error: Optional[str] = None
    latency_ms: Optional[float] = None


@dataclass
class PreflightResult:
    status: Status
    available_count: int
    total_count: int
    checks: list[CLICheck]
    degraded: bool
    abort: bool
    confidence_impact: float
    missing: list[str]


async def check_cli_async(name: str, command: str, timeout: float = 5.0) -> CLICheck:
    """Check if a CLI is available and responsive."""
    import time
    start = time.time()

    try:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=timeout
            )
            latency = (time.time() - start) * 1000

            if proc.returncode == 0:
                # Try to extract version
                output = stdout.decode().strip()
                version = extract_version(output)
                return CLICheck(
                    name=name,
                    available=True,
                    version=version,
                    latency_ms=round(latency, 2)
                )
            else:
                return CLICheck(
                    name=name,
                    available=False,
                    error=stderr.decode().strip()[:100]
                )

        except asyncio.TimeoutError:
            return CLICheck(
                name=name,
                available=False,
                error=f"Timeout after {timeout}s"
            )

    except Exception as e:
        return CLICheck(
            name=name,
            available=False,
            error=str(e)[:100]
        )


def extract_version(output: str) -> Optional[str]:
    """Extract version string from CLI output."""
    import re
    # Common version patterns
    patterns = [
        r'v?(\d+\.\d+\.\d+)',
        r'version[:\s]+(\d+\.\d+)',
        r'(\d+\.\d+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, output, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


async def run_preflight() -> PreflightResult:
    """Run all preflight checks in parallel."""

    cli_checks = {
        "limitless": "limitless lifelogs list --limit 1 --json 2>/dev/null | head -1",
        "research": "research --version 2>/dev/null",
        "pieces": "which pieces",
        "pdf-search": "pdf-search --stats 2>/dev/null | head -1",
        "pdf-brain": "pdf-brain --stats 2>/dev/null | head -1"
    }

    # Run all checks concurrently
    tasks = [
        check_cli_async(name, cmd)
        for name, cmd in cli_checks.items()
    ]
    results = await asyncio.gather(*tasks)

    # Calculate status
    available = [r for r in results if r.available]
    available_count = len(available)
    total_count = len(results)
    missing = [r.name for r in results if not r.available]

    # Determine status and confidence impact
    if available_count >= 4:
        status = Status.FULL
        confidence_impact = 0.0
        degraded = False
        abort = False
    elif available_count >= 3:
        status = Status.DEGRADED
        confidence_impact = -0.05
        degraded = True
        abort = False
    elif available_count >= 2:
        status = Status.DEGRADED
        confidence_impact = -0.15
        degraded = True
        abort = False
    else:
        status = Status.CRITICAL
        confidence_impact = -0.50
        degraded = True
        abort = True

    return PreflightResult(
        status=status,
        available_count=available_count,
        total_count=total_count,
        checks=results,
        degraded=degraded,
        abort=abort,
        confidence_impact=confidence_impact,
        missing=missing
    )


def format_output(result: PreflightResult, format: str = "json") -> str:
    """Format preflight result for output."""

    if format == "json":
        output = {
            "status": result.status.value,
            "available": result.available_count,
            "total": result.total_count,
            "degraded": result.degraded,
            "abort": result.abort,
            "confidence_impact": result.confidence_impact,
            "missing": result.missing,
            "checks": [asdict(c) for c in result.checks]
        }
        return json.dumps(output, indent=2)

    elif format == "table":
        lines = [
            "┌─────────────────────────────────────────────────┐",
            "│           PREFLIGHT CHECK RESULTS               │",
            "├─────────────────────────────────────────────────┤"
        ]

        for check in result.checks:
            status_icon = "✓" if check.available else "✗"
            version = f" ({check.version})" if check.version else ""
            latency = f" [{check.latency_ms}ms]" if check.latency_ms else ""
            error = f" - {check.error}" if check.error else ""

            line = f"│ {status_icon} {check.name:12}{version}{latency}{error}"
            lines.append(line[:49].ljust(49) + "│")

        lines.append("├─────────────────────────────────────────────────┤")
        lines.append(f"│ STATUS: {result.status.value:8} ({result.available_count}/{result.total_count} CLIs)".ljust(49) + "│")
        lines.append(f"│ Confidence Impact: {result.confidence_impact:+.2f}".ljust(49) + "│")
        if result.abort:
            lines.append("│ ⚠️  ABORT RECOMMENDED                            │")
        lines.append("└─────────────────────────────────────────────────┘")

        return "\n".join(lines)

    else:
        return f"Status: {result.status.value}, Available: {result.available_count}/{result.total_count}"


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Grounding Orchestrator Preflight Check")
    parser.add_argument("--format", choices=["json", "table", "short"], default="json")
    parser.add_argument("--exit-on-critical", action="store_true",
                        help="Exit with code 1 if status is CRITICAL")

    args = parser.parse_args()

    result = await run_preflight()
    print(format_output(result, args.format))

    if args.exit_on_critical and result.abort:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
