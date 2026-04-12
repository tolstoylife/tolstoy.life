#!/usr/bin/env python3
"""
OntoLog Reasoner
================

Execute λ-calculus reasoning over holarchic structures.

Usage:
    python reason.py "Explain how A connects to B"
    python reason.py --file structure.ol --query "Explain A"
    python reason.py --interactive

Pipeline:
    Query → Encode(Σ) → Topology(dgm) → Resolve(λ) → Target(τ) → Synthesize(H)
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Set, Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents import (
    execute_ontolog, execute_ontolog_verbose,
    OrchestratorConfig, EffortLevel,
    Holon, CompactFormatter, TripartiteFormatter, ProseFormatter
)


def format_holon(H: Holon, format_type: str = "tripartite") -> str:
    """Format holon for output."""
    if format_type == "compact":
        return CompactFormatter().format(H)
    elif format_type == "prose":
        return ProseFormatter().format(H)
    else:
        return TripartiteFormatter().format(H)


def run_query(
    query_text: str,
    known_vertices: Set[str] = None,
    format_type: str = "tripartite",
    verbose: bool = False
) -> str:
    """
    Execute query and return formatted result.
    """
    config = OrchestratorConfig(
        validate=True,
        decompose_holons=True
    )
    
    if verbose:
        result = execute_ontolog_verbose(
            query_text,
            known_vertices=known_vertices,
            config=config
        )
        
        if not result["success"]:
            return f"Error: {result['errors']}"
        
        lines = []
        lines.append(f"Trace: {result['trace']}")
        lines.append(f"Metrics: {result['metrics'].compact() if result['metrics'] else 'N/A'}")
        lines.append("")
        lines.append(format_holon(result["holon"], format_type))
        return "\n".join(lines)
    else:
        H = execute_ontolog(
            query_text,
            known_vertices=known_vertices,
            config=config
        )
        return format_holon(H, format_type)


def load_vertices_from_file(filepath: Path) -> Set[str]:
    """Extract vertices from ontology file."""
    vertices = set()
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            cmd = parts[0].lower()
            
            if cmd == 'vertex' and len(parts) >= 2:
                vertices.add(parts[1])
            elif cmd == 'edge' and len(parts) >= 3:
                vertices.add(parts[1])
                vertices.add(parts[2])
            elif cmd == 'simplex' and len(parts) >= 2:
                vertices.update(parts[1:])
    
    return vertices


def interactive_mode(known_vertices: Set[str] = None):
    """Run in interactive REPL mode."""
    print("OntoLog Interactive Reasoner")
    print("λ-calculus over simplicial complexes")
    print("Type 'quit' to exit, 'help' for commands")
    print()
    
    format_type = "tripartite"
    verbose = False
    
    while True:
        try:
            query = input("λ> ").strip()
        except EOFError:
            break
        except KeyboardInterrupt:
            print()
            continue
        
        if not query:
            continue
        
        if query.lower() == 'quit' or query.lower() == 'exit':
            break
        
        if query.lower() == 'help':
            print("Commands:")
            print("  :format [compact|prose|tripartite] - Set output format")
            print("  :verbose [on|off] - Toggle verbose mode")
            print("  :vertices - Show known vertices")
            print("  quit - Exit")
            print()
            continue
        
        if query.startswith(':format '):
            format_type = query.split()[1]
            print(f"Format set to: {format_type}")
            continue
        
        if query.startswith(':verbose '):
            verbose = query.split()[1].lower() == 'on'
            print(f"Verbose: {'on' if verbose else 'off'}")
            continue
        
        if query == ':vertices':
            print(f"Known vertices: {known_vertices or 'none'}")
            continue
        
        # Execute query
        try:
            result = run_query(query, known_vertices, format_type, verbose)
            print()
            print(result)
            print()
        except Exception as e:
            print(f"Error: {e}")
            print()


def main():
    parser = argparse.ArgumentParser(
        description="Execute λ-calculus reasoning over holarchic structures"
    )
    parser.add_argument(
        "query",
        nargs="?",
        type=str,
        help="Query text to execute"
    )
    parser.add_argument(
        "--file", "-f",
        type=Path,
        help="Load vertices from ontology file"
    )
    parser.add_argument(
        "--format",
        choices=["compact", "prose", "tripartite"],
        default="tripartite",
        help="Output format (default: tripartite)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output with trace"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Interactive REPL mode"
    )
    
    args = parser.parse_args()
    
    # Load known vertices
    known_vertices = None
    if args.file:
        known_vertices = load_vertices_from_file(args.file)
    
    # Interactive mode
    if args.interactive:
        interactive_mode(known_vertices)
        return
    
    # Single query mode
    if not args.query:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.json:
            result = execute_ontolog_verbose(
                args.query,
                known_vertices=known_vertices
            )
            # Convert non-serializable objects
            output = {
                "success": result["success"],
                "trace": result["trace"],
                "errors": result["errors"],
                "metrics": result["metrics"].__dict__ if result["metrics"] else None,
                "holon_id": result["holon"].id if result["holon"] else None,
                "vertex_count": len(result["complex"].vertices) if result["complex"] else 0,
                "operation_count": len(result["operations"]) if result["operations"] else 0,
                "terminal_count": len(result["terminals"]) if result["terminals"] else 0,
            }
            print(json.dumps(output, indent=2))
        else:
            result = run_query(
                args.query,
                known_vertices,
                args.format,
                args.verbose
            )
            print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
