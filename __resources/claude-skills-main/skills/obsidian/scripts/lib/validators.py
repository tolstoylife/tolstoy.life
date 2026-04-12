#!/usr/bin/env python3
"""
validators.py - Python validation helpers for Obsidian skill files

Usage:
    from lib.validators import validate_canvas, validate_base, validate_all

    # Validate single files
    validate_canvas("path/to/file.canvas")
    validate_base("path/to/file.base")

    # Validate directories
    validate_all("path/to/obsidian")
"""

import json
import yaml
import sys
from pathlib import Path
from typing import List, Tuple, Optional


def validate_canvas(filepath: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a .canvas file is valid JSON Canvas.

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    path = Path(filepath)

    if not path.exists():
        return False, f"File not found: {filepath}"

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

    # Check required top-level keys
    if 'nodes' not in data:
        return False, "Missing 'nodes' array"
    if 'edges' not in data:
        return False, "Missing 'edges' array"

    if not isinstance(data['nodes'], list):
        return False, "'nodes' must be an array"
    if not isinstance(data['edges'], list):
        return False, "'edges' must be an array"

    # Validate node structure
    node_ids = set()
    for i, node in enumerate(data['nodes']):
        required = ['id', 'type', 'x', 'y', 'width', 'height']
        for field in required:
            if field not in node:
                return False, f"Node {i} missing required field: {field}"

        if node['type'] not in ['text', 'file', 'link', 'group']:
            return False, f"Node {i} has invalid type: {node['type']}"

        node_ids.add(node['id'])

    # Validate edge structure
    for i, edge in enumerate(data['edges']):
        if 'id' not in edge:
            return False, f"Edge {i} missing 'id'"
        if 'fromNode' not in edge:
            return False, f"Edge {i} missing 'fromNode'"
        if 'toNode' not in edge:
            return False, f"Edge {i} missing 'toNode'"

        if edge['fromNode'] not in node_ids:
            return False, f"Edge {i} references unknown fromNode: {edge['fromNode']}"
        if edge['toNode'] not in node_ids:
            return False, f"Edge {i} references unknown toNode: {edge['toNode']}"

    return True, None


def validate_base(filepath: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a .base file is valid YAML.

    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """
    path = Path(filepath)

    if not path.exists():
        return False, f"File not found: {filepath}"

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return False, f"Invalid YAML: {e}"

    if data is None:
        return False, "Empty file"

    if not isinstance(data, dict):
        return False, "Root must be a mapping/object"

    return True, None


def validate_all(obsidian_dir: str) -> Tuple[int, int, List[str]]:
    """
    Validate all files in an obsidian skill directory.

    Returns:
        (passed_count, failed_count, error_messages)
    """
    root = Path(obsidian_dir)
    passed = 0
    failed = 0
    errors = []

    # Validate canvas files
    for canvas_file in root.glob('**/examples/*.canvas'):
        valid, error = validate_canvas(str(canvas_file))
        if valid:
            passed += 1
        else:
            failed += 1
            errors.append(f"{canvas_file}: {error}")

    for canvas_file in root.glob('**/templates/*.canvas'):
        valid, error = validate_canvas(str(canvas_file))
        if valid:
            passed += 1
        else:
            failed += 1
            errors.append(f"{canvas_file}: {error}")

    # Validate base files
    for base_file in root.glob('**/examples/*.base'):
        valid, error = validate_base(str(base_file))
        if valid:
            passed += 1
        else:
            failed += 1
            errors.append(f"{base_file}: {error}")

    for base_file in root.glob('**/templates/*.base'):
        valid, error = validate_base(str(base_file))
        if valid:
            passed += 1
        else:
            failed += 1
            errors.append(f"{base_file}: {error}")

    return passed, failed, errors


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Validate Obsidian skill files')
    parser.add_argument('path', help='File or directory to validate')
    parser.add_argument('--type', choices=['canvas', 'base', 'all'],
                        default='all', help='File type to validate')

    args = parser.parse_args()
    path = Path(args.path)

    if path.is_file():
        if args.type == 'canvas' or path.suffix == '.canvas':
            valid, error = validate_canvas(str(path))
        elif args.type == 'base' or path.suffix == '.base':
            valid, error = validate_base(str(path))
        else:
            print(f"Unknown file type: {path.suffix}")
            sys.exit(1)

        if valid:
            print(f"✓ {path}")
            sys.exit(0)
        else:
            print(f"✗ {path}: {error}")
            sys.exit(1)

    elif path.is_dir():
        passed, failed, errors = validate_all(str(path))

        for error in errors:
            print(f"✗ {error}")

        print(f"\nValidated {passed + failed} files: {passed} passed, {failed} failed")
        sys.exit(0 if failed == 0 else 1)

    else:
        print(f"Path not found: {path}")
        sys.exit(1)


if __name__ == '__main__':
    main()
