#!/usr/bin/env python3
"""CLI entry point for schema generation."""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from scripts.adapters.input_text import TextAdapter
from scripts.adapters.input_json import JSONAdapter
from scripts.adapters.input_markdown import MarkdownAdapter
from scripts.adapters.input_code import CodeAdapter
from scripts.utils.inheritance import apply_inheritance
from scripts.utils.validation import ConstraintValidator
from scripts.core.layer2_semantic import SemanticAnalyzer
from scripts.core.layer3_llm_enrich import LLMEnricher
from scripts.core.layer4_generator import ObsidianGenerator
from scripts.core.layer4_exporters import JSONLDGenerator, CypherGenerator, GraphQLGenerator


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate knowledge schemas and ontologies from any input"
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input file or inline text"
    )

    parser.add_argument(
        "--output", "-o",
        default="schema.md",
        help="Output file path (default: schema.md)"
    )

    parser.add_argument(
        "--mode", "-m",
        choices=["fractal", "free"],
        default="free",
        help="Generation mode: fractal (strict) or free (flexible)"
    )

    parser.add_argument(
        "--format", "-f",
        default="obsidian",
        help="Output formats (comma-separated): obsidian,jsonld,cypher,graphql"
    )

    parser.add_argument(
        "--deep",
        action="store_true",
        help="Enable Layer 3 LLM enrichment (slower, higher quality)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    return parser.parse_args(argv)


def detect_input_type(input_path: str) -> str:
    """Detect input format from file extension or content."""
    path = Path(input_path)

    if not path.exists():
        return "text"

    suffix = path.suffix.lower()

    if suffix in [".json"]:
        return "json"
    elif suffix in [".md", ".markdown"]:
        return "markdown"
    elif suffix in [".py", ".js", ".ts", ".java", ".cpp", ".rs"]:
        return "code"
    else:
        return "text"


def load_input(input_path: str) -> str:
    """Load input content from file or use as inline text."""
    path = Path(input_path)

    if path.exists():
        return path.read_text(encoding="utf-8")
    else:
        return input_path


def main(argv=None):
    """Main CLI entry point."""
    args = parse_args(argv)

    try:
        if args.verbose:
            print(f"Loading input from: {args.input}")

        input_content = load_input(args.input)
        input_type = detect_input_type(args.input)

        if args.verbose:
            print(f"Detected input type: {input_type}")

        # Select appropriate adapter
        adapter_map = {
            "json": JSONAdapter,
            "markdown": MarkdownAdapter,
            "code": CodeAdapter,
            "text": TextAdapter
        }

        adapter_class = adapter_map.get(input_type, TextAdapter)
        adapter = adapter_class()

        if args.verbose:
            print("Layer 1: Extracting structure...")

        ontology = adapter.parse(input_content)

        ontology.metadata["timestamp"] = datetime.now().isoformat()
        ontology.metadata["mode"] = args.mode
        ontology.metadata["source_file"] = args.input

        # Layer 2: Semantic analysis
        if args.verbose:
            print("Layer 2: Semantic analysis...")

        analyzer = SemanticAnalyzer(use_nlp=False)  # Pattern-based fallback
        ontology = analyzer.analyze(ontology)

        # Layer 3: LLM enrichment (optional)
        if args.deep:
            if args.verbose:
                print("Layer 3: LLM enrichment...")

            enricher = LLMEnricher(use_mcp=False)
            ontology = enricher.enrich(ontology)

        if args.verbose:
            print("Applying property inheritance...")

        apply_inheritance(ontology)

        # Validate constraints if fractal mode
        if args.mode == "fractal":
            if args.verbose:
                print("Validating fractal mode constraints...")

            validator = ConstraintValidator()
            violations = validator.validate(ontology)

            if violations:
                report = validator.generate_report(violations)
                print("\n" + report)
                print("\nWarning: Constraint violations detected in fractal mode")
            elif args.verbose:
                print("✓ All fractal constraints satisfied")

        if args.verbose:
            print(f"Layer 4: Generating {args.format} output...")

        formats = [f.strip() for f in args.format.split(",")]

        # Map formats to generators and file extensions
        format_map = {
            "obsidian": (ObsidianGenerator, ".md"),
            "jsonld": (JSONLDGenerator, ".jsonld"),
            "cypher": (CypherGenerator, ".cypher"),
            "graphql": (GraphQLGenerator, ".graphql")
        }

        for fmt in formats:
            if fmt in format_map:
                generator_class, extension = format_map[fmt]
                generator = generator_class()
                output = generator.generate(ontology)

                # Determine output path
                if fmt == "obsidian":
                    output_path = Path(args.output)
                else:
                    # For other formats, replace extension
                    base_path = Path(args.output)
                    output_path = base_path.with_suffix(extension)

                # Create parent directories if needed
                output_path.parent.mkdir(parents=True, exist_ok=True)

                output_path.write_text(output, encoding="utf-8")

                if args.verbose:
                    print(f"✓ Generated {fmt}: {output_path}")
            else:
                print(f"Warning: Format '{fmt}' not supported")

        print(f"✓ Schema generated successfully")
        print(f"  Nodes: {len(ontology.nodes)}")
        print(f"  Edges: {len(ontology.edges)}")
        print(f"  Topology: {ontology.calculate_topology_score():.2f}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
