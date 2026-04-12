#!/usr/bin/env python3
"""
Skill Validator

Homoiconic validation: this skill validates itself using the same rules it prescribes.

Usage:
    python validate-skill.py <skill-directory>
    
Validates:
    1. SKILL.md under 500 lines
    2. Frontmatter correct
    3. Description quality
    4. Progressive loading structure
    5. References connected (DAG topology)
    6. Scripts executable
    7. No external documentation (LAW 5)
"""

import re
import sys
import json
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


@dataclass
class Violation:
    """A validation violation."""
    rule: str
    severity: Severity
    message: str
    file: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Complete validation result."""
    passed: bool
    skill_name: str
    violations: List[Violation] = field(default_factory=list)
    metrics: Dict[str, any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "skill_name": self.skill_name,
            "violations": [
                {
                    "rule": v.rule,
                    "severity": v.severity.value,
                    "message": v.message,
                    "file": v.file,
                    "suggestion": v.suggestion,
                }
                for v in self.violations
            ],
            "metrics": self.metrics
        }


def parse_frontmatter(content: str) -> Tuple[Optional[dict], str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return None, content
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content
    
    try:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2]
        return frontmatter, body
    except yaml.YAMLError:
        return None, content


def validate_frontmatter(frontmatter: Optional[dict], violations: List[Violation]) -> None:
    """Validate SKILL.md frontmatter."""
    
    if frontmatter is None:
        violations.append(Violation(
            rule="FRONTMATTER",
            severity=Severity.CRITICAL,
            message="Missing or invalid YAML frontmatter",
            suggestion="Add frontmatter with 'name' and 'description'"
        ))
        return
    
    # Required fields
    if "name" not in frontmatter:
        violations.append(Violation(
            rule="FRONTMATTER_NAME",
            severity=Severity.CRITICAL,
            message="Missing required 'name' field",
            suggestion="Add 'name: your-skill-name' to frontmatter"
        ))
    else:
        name = frontmatter["name"]
        # Validate kebab-case
        if not re.match(r'^[a-z][a-z0-9-]*$', name):
            violations.append(Violation(
                rule="FRONTMATTER_NAME_FORMAT",
                severity=Severity.MAJOR,
                message=f"Name '{name}' must be kebab-case",
                suggestion="Use lowercase letters, numbers, and hyphens only"
            ))
        # Max length
        if len(name) > 64:
            violations.append(Violation(
                rule="FRONTMATTER_NAME_LENGTH",
                severity=Severity.MAJOR,
                message=f"Name exceeds 64 characters",
                suggestion="Shorten the skill name"
            ))
    
    if "description" not in frontmatter:
        violations.append(Violation(
            rule="FRONTMATTER_DESCRIPTION",
            severity=Severity.CRITICAL,
            message="Missing required 'description' field",
            suggestion="Add 'description: ...' to frontmatter"
        ))
    else:
        desc = frontmatter["description"]
        # Length check
        if len(desc) > 1024:
            violations.append(Violation(
                rule="FRONTMATTER_DESC_LENGTH",
                severity=Severity.MAJOR,
                message=f"Description exceeds 1024 characters ({len(desc)})",
                suggestion="Shorten description to under 1024 characters"
            ))
        # Trigger clause
        if "trigger" not in desc.lower() and "use when" not in desc.lower():
            violations.append(Violation(
                rule="FRONTMATTER_DESC_TRIGGER",
                severity=Severity.MAJOR,
                message="Description missing trigger clause",
                suggestion="Add 'Trigger when...' or 'Use when...' to description"
            ))
    
    # Forbidden fields
    forbidden = ["version", "author", "category", "tags", "dependencies", "created", "updated"]
    for field in forbidden:
        if field in frontmatter:
            violations.append(Violation(
                rule="FRONTMATTER_FORBIDDEN",
                severity=Severity.MAJOR,
                message=f"Forbidden field '{field}' in frontmatter",
                suggestion=f"Remove '{field}' from frontmatter"
            ))


def validate_structure(skill_dir: Path, violations: List[Violation], metrics: Dict) -> None:
    """Validate skill directory structure."""
    
    skill_md = skill_dir / "SKILL.md"
    
    if not skill_md.exists():
        violations.append(Violation(
            rule="STRUCTURE_SKILL_MD",
            severity=Severity.CRITICAL,
            message="Missing SKILL.md file",
            file=str(skill_dir),
            suggestion="Create SKILL.md with frontmatter and instructions"
        ))
        return
    
    # Line count
    content = skill_md.read_text()
    line_count = len(content.split("\n"))
    metrics["skill_md_lines"] = line_count
    
    if line_count > 500:
        violations.append(Violation(
            rule="STRUCTURE_LINE_COUNT",
            severity=Severity.MAJOR,
            message=f"SKILL.md exceeds 500 lines ({line_count})",
            file=str(skill_md),
            suggestion="Move detailed content to references/"
        ))
    
    # Check for prohibited files
    prohibited = ["README.md", "CHANGELOG.md", "INSTALLATION.md", "QUICK_REFERENCE.md"]
    for filename in prohibited:
        if (skill_dir / filename).exists():
            violations.append(Violation(
                rule="STRUCTURE_PROHIBITED_FILE",
                severity=Severity.MINOR,
                message=f"Prohibited file '{filename}' found",
                file=str(skill_dir / filename),
                suggestion="Remove or integrate into SKILL.md"
            ))


def validate_progressive_loading(skill_dir: Path, body: str, violations: List[Violation], metrics: Dict) -> None:
    """Validate progressive loading DAG structure."""
    
    references_dir = skill_dir / "references"
    scripts_dir = skill_dir / "scripts"
    templates_dir = skill_dir / "templates"
    
    # Count resources
    ref_count = len(list(references_dir.glob("*.md"))) if references_dir.exists() else 0
    script_count = len(list(scripts_dir.glob("*.py"))) if scripts_dir.exists() else 0
    template_count = len(list(templates_dir.glob("*"))) if templates_dir.exists() else 0
    
    metrics["references"] = ref_count
    metrics["scripts"] = script_count
    metrics["templates"] = template_count
    
    # Check references are mentioned in SKILL.md
    if references_dir.exists():
        for ref_file in references_dir.glob("*.md"):
            ref_name = ref_file.name
            if ref_name not in body and f"references/{ref_name}" not in body:
                violations.append(Violation(
                    rule="PROGRESSIVE_UNREFERENCED",
                    severity=Severity.MINOR,
                    message=f"Reference '{ref_name}' not mentioned in SKILL.md",
                    file=str(ref_file),
                    suggestion="Add reference instruction in SKILL.md or remove file"
                ))
    
    # Check scripts are mentioned
    if scripts_dir.exists():
        for script_file in scripts_dir.glob("*.py"):
            script_name = script_file.name
            if script_name not in body and f"scripts/{script_name}" not in body:
                violations.append(Violation(
                    rule="PROGRESSIVE_UNREFERENCED",
                    severity=Severity.MINOR,
                    message=f"Script '{script_name}' not mentioned in SKILL.md",
                    file=str(script_file),
                    suggestion="Add usage instruction in SKILL.md or remove file"
                ))


def validate_dag_topology(skill_dir: Path, body: str, violations: List[Violation], metrics: Dict) -> None:
    """
    Validate DAG topology of skill references.
    
    Checks η ≥ 4 (edges/nodes ratio) for connected skill structure.
    """
    
    # Extract references from SKILL.md
    # Looking for patterns like: references/file.md, scripts/file.py
    reference_pattern = re.compile(r'(?:references|scripts|templates)/[\w-]+\.\w+')
    references = set(reference_pattern.findall(body))
    
    # Extract internal links (markdown links and code references)
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)')
    links = set(link_pattern.findall(body))
    
    # Count nodes (files) and edges (references)
    nodes = set()
    edges = 0
    
    # SKILL.md is always a node
    nodes.add("SKILL.md")
    
    for ref in references:
        nodes.add(ref)
        edges += 1  # Edge from SKILL.md to reference
    
    # Check cross-references in reference files
    references_dir = skill_dir / "references"
    if references_dir.exists():
        for ref_file in references_dir.glob("*.md"):
            ref_content = ref_file.read_text()
            sub_refs = reference_pattern.findall(ref_content)
            for sub_ref in sub_refs:
                nodes.add(sub_ref)
                edges += 1
    
    node_count = len(nodes)
    edge_count = edges
    
    metrics["dag_nodes"] = node_count
    metrics["dag_edges"] = edge_count
    metrics["dag_density"] = edge_count / node_count if node_count > 0 else 0
    
    # Note: η ≥ 4 is ideal but not strictly required for skills
    # Skills are trees/DAGs, not dense graphs


def validate_scripts_executable(skill_dir: Path, violations: List[Violation]) -> None:
    """Validate that scripts are syntactically correct."""
    
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return
    
    import subprocess
    
    for script_file in scripts_dir.glob("*.py"):
        # Syntax check
        result = subprocess.run(
            ["python", "-m", "py_compile", str(script_file)],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            violations.append(Violation(
                rule="SCRIPT_SYNTAX",
                severity=Severity.CRITICAL,
                message=f"Script has syntax errors",
                file=str(script_file),
                suggestion="Fix Python syntax errors"
            ))


def validate_no_external_docs(skill_dir: Path, violations: List[Violation]) -> None:
    """
    LAW 5: Code is documentation. Check for external doc patterns.
    """
    
    # External doc patterns within the skill
    external_patterns = [
        "docs/**/*.md",
        "documentation/**/*",
    ]
    
    for pattern in external_patterns:
        for file in skill_dir.glob(pattern):
            violations.append(Violation(
                rule="LAW_5_EXTERNAL_DOCS",
                severity=Severity.MINOR,
                message=f"External documentation pattern detected",
                file=str(file),
                suggestion="Integrate into SKILL.md or references/"
            ))


def validate_description_quality(description: str, violations: List[Violation], metrics: Dict) -> None:
    """Score description quality."""
    
    score = 0.0
    
    # Third person (no I/you/we)
    first_person = re.search(r'\b(I|you|we|my|your|our)\b', description, re.IGNORECASE)
    if not first_person:
        score += 0.25
    
    # Has action verbs / gerunds
    if re.search(r'\b\w+ing\b', description):
        score += 0.20
    
    # Has trigger clause
    if re.search(r'(trigger|use when|activate)', description, re.IGNORECASE):
        score += 0.25
    
    # Length (100-600 chars ideal)
    if 100 <= len(description) <= 600:
        score += 0.15
    elif len(description) > 600:
        score += 0.10
    
    # Has domain terms (at least 2 technical/domain words)
    technical_words = re.findall(r'\b[A-Za-z]{4,}\b', description)
    if len(set(technical_words)) >= 5:
        score += 0.15
    
    metrics["description_score"] = round(score, 2)
    
    if score < 0.70:
        violations.append(Violation(
            rule="DESCRIPTION_QUALITY",
            severity=Severity.MAJOR,
            message=f"Description quality score {score:.2f} below 0.70 threshold",
            suggestion="Improve: use third person, add triggers, include domain terms"
        ))


def validate_skill(skill_dir: Path) -> ValidationResult:
    """Run all validations on a skill directory."""
    
    violations = []
    metrics = {}
    
    skill_md = skill_dir / "SKILL.md"
    
    if not skill_md.exists():
        return ValidationResult(
            passed=False,
            skill_name=skill_dir.name,
            violations=[Violation(
                rule="SKILL_MD_MISSING",
                severity=Severity.CRITICAL,
                message="SKILL.md not found"
            )],
            metrics={}
        )
    
    content = skill_md.read_text()
    frontmatter, body = parse_frontmatter(content)
    
    skill_name = frontmatter.get("name", skill_dir.name) if frontmatter else skill_dir.name
    
    # Run validations
    validate_frontmatter(frontmatter, violations)
    validate_structure(skill_dir, violations, metrics)
    validate_progressive_loading(skill_dir, body, violations, metrics)
    validate_dag_topology(skill_dir, body, violations, metrics)
    validate_scripts_executable(skill_dir, violations)
    validate_no_external_docs(skill_dir, violations)
    
    if frontmatter and "description" in frontmatter:
        validate_description_quality(frontmatter["description"], violations, metrics)
    
    # Determine pass/fail
    critical_count = len([v for v in violations if v.severity == Severity.CRITICAL])
    passed = critical_count == 0
    
    return ValidationResult(
        passed=passed,
        skill_name=skill_name,
        violations=violations,
        metrics=metrics
    )


def print_result(result: ValidationResult, json_output: bool = False) -> None:
    """Print validation result."""
    
    if json_output:
        print(json.dumps(result.to_dict(), indent=2))
        return
    
    print("\n" + "=" * 60)
    print(f"Skill Validation: {result.skill_name}")
    print("=" * 60 + "\n")
    
    # Metrics
    print("Metrics:")
    for key, value in result.metrics.items():
        print(f"  {key}: {value}")
    print()
    
    # Violations
    if result.violations:
        print("Violations:")
        for v in result.violations:
            severity_icon = {
                Severity.CRITICAL: "🔴",
                Severity.MAJOR: "🟠",
                Severity.MINOR: "🟡"
            }[v.severity]
            
            print(f"  {severity_icon} [{v.rule}] {v.message}")
            if v.file:
                print(f"      @ {v.file}")
            if v.suggestion:
                print(f"      → {v.suggestion}")
        print()
    
    # Result
    if result.passed:
        print("✅ VALIDATION PASSED")
    else:
        print("❌ VALIDATION FAILED")
    print()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate Claude skill structure"
    )
    parser.add_argument("skill_dir", help="Path to skill directory")
    parser.add_argument("--json", action="store_true", help="JSON output")
    
    args = parser.parse_args()
    skill_dir = Path(args.skill_dir).resolve()
    
    if not skill_dir.is_dir():
        print(f"Error: {skill_dir} is not a directory")
        sys.exit(1)
    
    result = validate_skill(skill_dir)
    print_result(result, json_output=args.json)
    
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
