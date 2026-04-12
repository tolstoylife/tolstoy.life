#!/usr/bin/env python3
"""Audit all Claude Code components for frontmatter compliance.

Usage:
    python3 audit-components.py              # Audit all components
    python3 audit-components.py --type skill # Audit only skills
    python3 audit-components.py --fix        # Show remediation suggestions
    python3 audit-components.py --json       # Output as JSON
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    import yaml
except ImportError:
    # Fallback to basic YAML parsing if pyyaml not available
    yaml = None

CLAUDE_DIR = Path.home() / ".claude"

OFFICIAL_SCHEMA = {
    "skill": {
        "required": ["name", "description"],
        "optional": ["allowed-tools", "model", "context", "agent", "hooks",
                    "user-invocable", "disable-model-invocation"]
    },
    "agent": {
        "required": ["name", "description"],
        "optional": ["tools", "disallowedTools", "model", "permissionMode",
                    "skills", "hooks"]
    },
    "command": {
        "required": [],
        "optional": ["description", "allowed-tools", "model", "argument-hint"]
    }
}


def extract_frontmatter(content: str) -> Dict[str, Any]:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}

    frontmatter_str = parts[1].strip()

    if yaml:
        try:
            return yaml.safe_load(frontmatter_str) or {}
        except yaml.YAMLError:
            return {}
    else:
        # Basic parsing without pyyaml
        result = {}
        for line in frontmatter_str.split("\n"):
            if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
                key, _, value = line.partition(":")
                key = key.strip()
                value = value.strip()
                if value:
                    result[key] = value
                else:
                    result[key] = True  # Flag for complex values
        return result


def validate_component(path: Path, component_type: str) -> Dict[str, Any]:
    """Validate a component file against official schema."""
    try:
        content = path.read_text()
    except Exception as e:
        return {
            "file": str(path),
            "type": component_type,
            "status": "error",
            "issues": [{"property": "file", "issue": f"Cannot read: {e}", "action": "Check file permissions"}]
        }

    frontmatter = extract_frontmatter(content)
    schema = OFFICIAL_SCHEMA.get(component_type, {})

    issues = []

    # Check for missing frontmatter
    if not frontmatter:
        issues.append({
            "property": "frontmatter",
            "issue": "No YAML frontmatter found",
            "action": "Add frontmatter with --- delimiters"
        })
        return {
            "file": str(path),
            "type": component_type,
            "status": "non-compliant",
            "issues": issues
        }

    # Check required fields
    for field in schema.get("required", []):
        if field not in frontmatter:
            issues.append({
                "property": field,
                "issue": "Missing required field",
                "action": f"Add '{field}' to frontmatter"
            })

    # Check for non-official fields
    all_official = set(schema.get("required", [])) | set(schema.get("optional", []))
    for field in frontmatter.keys():
        if field not in all_official:
            issues.append({
                "property": field,
                "issue": "Not in official spec",
                "action": "Remove from frontmatter or move to body"
            })

    # Check for architecture pattern (skills only)
    architecture_suggestions = []
    if component_type == "skill":
        if frontmatter.get("context") != "fork":
            architecture_suggestions.append({
                "property": "context",
                "suggestion": "Consider adding 'context: fork' for agent isolation",
                "benefit": "Enables 'one skill = one agent' pattern"
            })
        if "agent" not in frontmatter and frontmatter.get("context") == "fork":
            architecture_suggestions.append({
                "property": "agent",
                "suggestion": "Add designated agent when using context: fork",
                "benefit": "Specialized agent for skill domain"
            })

    status = "compliant" if not issues else "non-compliant"
    if issues and all(i.get("issue") == "Not in official spec" for i in issues):
        status = "has-extensions"  # Only has non-official fields, not missing required

    result = {
        "file": str(path),
        "type": component_type,
        "status": status,
        "issues": issues
    }

    if architecture_suggestions:
        result["suggestions"] = architecture_suggestions

    return result


def audit_skills() -> List[Dict[str, Any]]:
    """Audit all skills."""
    results = []
    skills_dir = CLAUDE_DIR / "skills"

    if not skills_dir.exists():
        return results

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            results.append(validate_component(skill_file, "skill"))

    return results


def audit_agents() -> List[Dict[str, Any]]:
    """Audit all agents."""
    results = []
    agents_dir = CLAUDE_DIR / "agents"

    if not agents_dir.exists():
        return results

    for agent_file in agents_dir.glob("*.md"):
        results.append(validate_component(agent_file, "agent"))

    return results


def audit_commands() -> List[Dict[str, Any]]:
    """Audit all commands."""
    results = []
    commands_dir = CLAUDE_DIR / "commands"

    if not commands_dir.exists():
        return results

    for cmd_file in commands_dir.glob("*.md"):
        results.append(validate_component(cmd_file, "command"))

    return results


def audit_all(component_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """Audit all components or specific type."""
    results = []

    if component_type is None or component_type == "skill":
        results.extend(audit_skills())

    if component_type is None or component_type == "agent":
        results.extend(audit_agents())

    if component_type is None or component_type == "command":
        results.extend(audit_commands())

    return results


def print_report(results: List[Dict[str, Any]], show_fix: bool = False):
    """Print human-readable audit report."""
    if not results:
        print("No components found to audit.")
        return

    compliant = [r for r in results if r["status"] == "compliant"]
    non_compliant = [r for r in results if r["status"] == "non-compliant"]
    has_extensions = [r for r in results if r["status"] == "has-extensions"]
    errors = [r for r in results if r["status"] == "error"]

    print(f"\n{'='*60}")
    print("COMPONENT ARCHITECTURE AUDIT REPORT")
    print(f"{'='*60}\n")

    print(f"Total components: {len(results)}")
    print(f"  ✅ Compliant: {len(compliant)}")
    print(f"  ⚠️  Has extensions: {len(has_extensions)}")
    print(f"  ❌ Non-compliant: {len(non_compliant)}")
    print(f"  🔴 Errors: {len(errors)}")

    if non_compliant or errors:
        print(f"\n{'-'*60}")
        print("ISSUES REQUIRING ATTENTION")
        print(f"{'-'*60}\n")

        for result in non_compliant + errors:
            print(f"📄 {result['file']}")
            print(f"   Type: {result['type']}")
            print(f"   Status: {result['status']}")
            for issue in result.get("issues", []):
                print(f"   • {issue['property']}: {issue['issue']}")
                if show_fix:
                    print(f"     → {issue['action']}")
            print()

    if has_extensions:
        print(f"\n{'-'*60}")
        print("COMPONENTS WITH NON-OFFICIAL EXTENSIONS")
        print(f"{'-'*60}\n")

        for result in has_extensions:
            print(f"📄 {result['file']}")
            non_official = [i["property"] for i in result.get("issues", [])
                          if i.get("issue") == "Not in official spec"]
            print(f"   Extensions: {', '.join(non_official)}")
            print()

    # Show architecture suggestions
    with_suggestions = [r for r in results if r.get("suggestions")]
    if with_suggestions:
        print(f"\n{'-'*60}")
        print("ARCHITECTURE PATTERN SUGGESTIONS")
        print(f"{'-'*60}\n")

        for result in with_suggestions:
            print(f"📄 {result['file']}")
            for suggestion in result.get("suggestions", []):
                print(f"   💡 {suggestion['suggestion']}")
                print(f"      Benefit: {suggestion['benefit']}")
            print()


def main():
    parser = argparse.ArgumentParser(description="Audit Claude Code components for frontmatter compliance")
    parser.add_argument("--type", choices=["skill", "agent", "command"],
                       help="Audit only specific component type")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--fix", action="store_true", help="Show remediation suggestions")
    parser.add_argument("--non-compliant", action="store_true",
                       help="Show only non-compliant components")

    args = parser.parse_args()

    results = audit_all(args.type)

    if args.non_compliant:
        results = [r for r in results if r["status"] in ("non-compliant", "error")]

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_report(results, show_fix=args.fix)


if __name__ == "__main__":
    main()
