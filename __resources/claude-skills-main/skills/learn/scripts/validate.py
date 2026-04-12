#!/usr/bin/env python3
"""Validate learn skill topology and structure."""

import re
from pathlib import Path

def validate(root: Path):
    """Validate skill structure and topology."""
    files = list(root.rglob("*.md"))
    nodes = len(files)
    
    # Count markdown links
    edges = 0
    broken = []
    
    for f in files:
        content = f.read_text()
        for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', content):
            target = m.group(2)
            if target.startswith("http"):
                continue
            edges += 1
            target_path = root / target
            if not target_path.exists():
                broken.append(f"{f.relative_to(root)}: {target}")
    
    eta = edges / nodes if nodes > 0 else 0
    
    # Check isolation
    isolated = 0
    for f in files:
        content = f.read_text()
        local_links = re.findall(r'\[([^\]]+)\]\((?!http)([^)]+)\)', content)
        if not local_links:
            isolated += 1
    
    isolation_pct = (isolated / nodes * 100) if nodes > 0 else 0
    
    print(f"Files: {nodes}")
    print(f"Edges: {edges}")
    print(f"η = {eta:.2f} (target: ≥4.0)")
    print(f"Isolation: {isolation_pct:.1f}% (target: <20%)")
    print()
    print("Validation:")
    print(f"  [{'✓' if eta >= 4.0 else '✗'}] η ≥ 4.0 ({eta:.2f})")
    print(f"  [{'✓' if isolation_pct < 20 else '✗'}] isolation < 20% ({isolation_pct:.1f}%)")
    print(f"  [{'✓' if not broken else '✗'}] No broken links ({len(broken)})")
    print(f"  [{'✓' if (root / 'SKILL.md').exists() else '✗'}] SKILL.md exists")
    print(f"  [{'✓' if (root / 'schema.yaml').exists() else '✗'}] schema.yaml exists")
    
    if broken:
        print("\nBroken links:")
        for b in broken[:15]:
            print(f"  {b}")

if __name__ == "__main__":
    validate(Path(__file__).parent.parent)
