#!/usr/bin/env python3
"""
test_evaluator_discovery.py
Unit test to verify all 10 evaluator subagents are discoverable.
"""

import sys
from pathlib import Path


def test_evaluator_discovery():
    """Test that all 10 evaluator subagents exist and are valid."""
    evaluators_dir = Path.home() / '.claude' / 'skills' / 'refactor' / 'evaluators'

    # Expected evaluators
    expected_evaluators = [
        'claude-md-evaluator.md',
        'skills-evaluator.md',
        'agents-evaluator.md',
        'hooks-evaluator.md',
        'commands-evaluator.md',
        'plugins-evaluator.md',
        'mcp-evaluator.md',
        'cli-evaluator.md',
        'architecture-evaluator.md',
        'performance-evaluator.md',
    ]

    print("\n🔍 Testing Evaluator Discovery...")
    print(f"   Evaluators directory: {evaluators_dir}")
    print(f"   Expected evaluators: {len(expected_evaluators)}\n")

    found_count = 0
    missing = []
    invalid = []

    for evaluator_name in expected_evaluators:
        evaluator_path = evaluators_dir / evaluator_name
        status = "✗ Missing"

        if evaluator_path.exists():
            # Check for required frontmatter
            with open(evaluator_path, 'r') as f:
                content = f.read()

            if '---' in content and 'name:' in content and 'description:' in content:
                status = "✓ Found"
                found_count += 1
            else:
                status = "⚠ Invalid frontmatter"
                invalid.append(evaluator_name)
        else:
            missing.append(evaluator_name)

        print(f"   {status}  {evaluator_name}")

    print(f"\n📊 Results:")
    print(f"   Found: {found_count}/{len(expected_evaluators)}")
    print(f"   Missing: {len(missing)}")
    print(f"   Invalid: {len(invalid)}")

    if missing:
        print(f"\n⚠️  Missing evaluators:")
        for name in missing:
            print(f"   - {name}")

    if invalid:
        print(f"\n⚠️  Invalid evaluators:")
        for name in invalid:
            print(f"   - {name}")

    # Test passes if all evaluators found and valid
    success = found_count == len(expected_evaluators) and len(invalid) == 0

    if success:
        print(f"\n✅ Test PASSED: All 10 evaluators discoverable")
        return 0
    else:
        print(f"\n❌ Test FAILED: {len(expected_evaluators) - found_count} evaluators not found, {len(invalid)} invalid")
        return 1


if __name__ == '__main__':
    sys.exit(test_evaluator_discovery())
