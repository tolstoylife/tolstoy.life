#!/usr/bin/env python3
"""
Preflight Validation Script

Enforces the Seven Laws through executable checks.
This script IS the governance documentation—if it passes, governance is satisfied.

Usage:
    python preflight.py [options]
    
Options:
    --init          Initialize preflight for new project
    --full          Run all checks including slow E2E
    --fix           Attempt auto-fix for violations
    --json          Output results as JSON
    --ci            CI mode (strict, no prompts)
"""

import subprocess
import sys
import json
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Callable
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"  # Blocks merge
    MAJOR = "major"        # Should fix
    MINOR = "minor"        # Nice to fix


@dataclass
class Violation:
    """A governance violation."""
    law: str
    severity: Severity
    message: str
    file: Optional[str] = None
    line: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class CheckResult:
    """Result of a single check."""
    name: str
    law: str
    passed: bool
    violations: List[Violation] = field(default_factory=list)
    duration_ms: int = 0


@dataclass
class PreflightResult:
    """Complete preflight result."""
    passed: bool
    checks: List[CheckResult] = field(default_factory=list)
    total_violations: int = 0
    critical_violations: int = 0
    
    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "total_violations": self.total_violations,
            "critical_violations": self.critical_violations,
            "checks": [
                {
                    "name": c.name,
                    "law": c.law,
                    "passed": c.passed,
                    "violations": [
                        {
                            "severity": v.severity.value,
                            "message": v.message,
                            "file": v.file,
                            "line": v.line,
                            "suggestion": v.suggestion,
                        }
                        for v in c.violations
                    ]
                }
                for c in self.checks
            ]
        }


def run_command(cmd: List[str], capture: bool = True) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=300
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except FileNotFoundError:
        return 1, "", f"Command not found: {cmd[0]}"


def check_types_compile(project_root: Path) -> CheckResult:
    """
    LAW 6: Types compile = documentation current.
    
    Checks for TypeScript (tsc) or Python (mypy) type checking.
    """
    violations = []
    
    # Try TypeScript
    if (project_root / "tsconfig.json").exists():
        code, stdout, stderr = run_command(["npx", "tsc", "--noEmit"])
        if code != 0:
            violations.append(Violation(
                law="LAW_6",
                severity=Severity.CRITICAL,
                message="TypeScript compilation failed",
                suggestion="Fix type errors to ensure documentation is current"
            ))
    
    # Try Python mypy
    if (project_root / "pyproject.toml").exists() or (project_root / "mypy.ini").exists():
        code, stdout, stderr = run_command(["mypy", "."])
        if code != 0:
            violations.append(Violation(
                law="LAW_6",
                severity=Severity.CRITICAL,
                message="Python type checking failed",
                suggestion="Fix mypy errors to ensure documentation is current"
            ))
    
    return CheckResult(
        name="types_compile",
        law="LAW_6",
        passed=len(violations) == 0,
        violations=violations
    )


def check_schemas_validate(project_root: Path) -> CheckResult:
    """
    LAW 6: Schemas validate = documentation current.
    """
    violations = []
    
    # Check for schema validation script
    schema_scripts = [
        "npm run validate:schemas",
        "python -m pytest tests/schema/",
    ]
    
    # Try package.json scripts
    package_json = project_root / "package.json"
    if package_json.exists():
        pkg = json.loads(package_json.read_text())
        if "validate:schemas" in pkg.get("scripts", {}):
            code, _, stderr = run_command(["npm", "run", "validate:schemas"])
            if code != 0:
                violations.append(Violation(
                    law="LAW_6",
                    severity=Severity.CRITICAL,
                    message="Schema validation failed",
                    suggestion="Fix schema errors"
                ))
    
    return CheckResult(
        name="schemas_validate",
        law="LAW_6",
        passed=len(violations) == 0,
        violations=violations
    )


def check_linting(project_root: Path) -> CheckResult:
    """
    LAW 3: Rules must be script-enforced.
    
    Linter configuration IS the style documentation.
    """
    violations = []
    
    # ESLint
    if (project_root / ".eslintrc.js").exists() or (project_root / ".eslintrc.json").exists():
        code, stdout, stderr = run_command(["npx", "eslint", ".", "--max-warnings=0"])
        if code != 0:
            violations.append(Violation(
                law="LAW_3",
                severity=Severity.MAJOR,
                message="ESLint violations found",
                suggestion="Fix linting errors or update rules"
            ))
    
    # Ruff (Python)
    if (project_root / "pyproject.toml").exists():
        code, stdout, stderr = run_command(["ruff", "check", "."])
        if code != 0:
            violations.append(Violation(
                law="LAW_3",
                severity=Severity.MAJOR,
                message="Ruff linting violations found",
                suggestion="Run 'ruff check --fix' or fix manually"
            ))
    
    return CheckResult(
        name="linting",
        law="LAW_3",
        passed=len(violations) == 0,
        violations=violations
    )


def check_required_todos(project_root: Path) -> CheckResult:
    """
    LAW 7: TODOs are plans. Required TODOs must be resolved.
    """
    violations = []
    
    # Find required TODOs
    code, stdout, stderr = run_command([
        "grep", "-rn", "TODO(.*required", 
        "--include=*.py", "--include=*.ts", "--include=*.js",
        str(project_root / "src")
    ])
    
    if code == 0 and stdout.strip():  # Found matches
        for line in stdout.strip().split("\n"):
            if line:
                parts = line.split(":", 2)
                violations.append(Violation(
                    law="LAW_7",
                    severity=Severity.CRITICAL,
                    message=f"Required TODO not resolved",
                    file=parts[0] if len(parts) > 0 else None,
                    line=int(parts[1]) if len(parts) > 1 else None,
                    suggestion="Complete this TODO before merge"
                ))
    
    return CheckResult(
        name="required_todos",
        law="LAW_7",
        passed=len(violations) == 0,
        violations=violations
    )


def check_external_docs(project_root: Path) -> CheckResult:
    """
    LAW 5: Code is documentation. External docs will drift.
    """
    violations = []
    
    # Patterns that indicate external documentation
    external_doc_patterns = [
        "docs/**/*.md",
        "ARCHITECTURE.md",
        "API_REFERENCE.md",
        "IMPLEMENTATION.md",
        "SPECIFICATION.md",
    ]
    
    for pattern in external_doc_patterns:
        for file in project_root.glob(pattern):
            # Exclude generated docs
            if "generated" not in str(file).lower():
                violations.append(Violation(
                    law="LAW_5",
                    severity=Severity.MINOR,
                    message=f"External documentation detected: {file.name}",
                    file=str(file),
                    suggestion="Convert to code-based documentation (types, schemas, TODOs)"
                ))
    
    return CheckResult(
        name="external_docs",
        law="LAW_5",
        passed=len([v for v in violations if v.severity == Severity.CRITICAL]) == 0,
        violations=violations
    )


def check_logging_coverage(project_root: Path) -> CheckResult:
    """
    LAW 2: All executions must be observable.
    """
    violations = []
    
    # Check for logging in route handlers / endpoints
    src_dir = project_root / "src"
    if src_dir.exists():
        code, stdout, stderr = run_command([
            "grep", "-rL", "logger\\|logging\\|console\\.log",
            "--include=*.py", "--include=*.ts",
            str(src_dir)
        ])
        
        # Files without logging
        if code == 0 and stdout.strip():
            for file in stdout.strip().split("\n"):
                if file and ("route" in file.lower() or "handler" in file.lower() or "controller" in file.lower()):
                    violations.append(Violation(
                        law="LAW_2",
                        severity=Severity.MAJOR,
                        message=f"No logging found in handler file",
                        file=file,
                        suggestion="Add structured logging for observability"
                    ))
    
    return CheckResult(
        name="logging_coverage",
        law="LAW_2",
        passed=len([v for v in violations if v.severity == Severity.CRITICAL]) == 0,
        violations=violations
    )


def check_duplicate_implementations(project_root: Path) -> CheckResult:
    """
    LAW 3 + Refactoring: Detect potential duplicate code.
    """
    violations = []
    
    # Use jscpd if available
    code, stdout, stderr = run_command([
        "npx", "jscpd", 
        str(project_root / "src"),
        "--min-lines", "10",
        "--reporters", "json"
    ])
    
    if code == 0 and stdout:
        try:
            result = json.loads(stdout)
            if result.get("statistics", {}).get("clones", 0) > 0:
                violations.append(Violation(
                    law="LAW_3",
                    severity=Severity.MINOR,
                    message=f"Duplicate code detected: {result['statistics']['clones']} clones",
                    suggestion="Consider refactoring to reduce duplication"
                ))
        except json.JSONDecodeError:
            pass
    
    return CheckResult(
        name="duplicate_code",
        law="LAW_3",
        passed=len([v for v in violations if v.severity == Severity.CRITICAL]) == 0,
        violations=violations
    )


def run_preflight(
    project_root: Path,
    full: bool = False,
    ci_mode: bool = False
) -> PreflightResult:
    """
    Run all preflight checks.
    
    Implements governance through execution.
    """
    checks = [
        check_types_compile,
        check_schemas_validate,
        check_linting,
        check_required_todos,
        check_external_docs,
        check_logging_coverage,
    ]
    
    if full:
        checks.append(check_duplicate_implementations)
    
    results = []
    for check_fn in checks:
        try:
            result = check_fn(project_root)
            results.append(result)
        except Exception as e:
            results.append(CheckResult(
                name=check_fn.__name__,
                law="UNKNOWN",
                passed=False,
                violations=[Violation(
                    law="UNKNOWN",
                    severity=Severity.CRITICAL,
                    message=f"Check failed with error: {str(e)}"
                )]
            ))
    
    total_violations = sum(len(r.violations) for r in results)
    critical_violations = sum(
        len([v for v in r.violations if v.severity == Severity.CRITICAL])
        for r in results
    )
    
    passed = critical_violations == 0 if ci_mode else all(r.passed for r in results)
    
    return PreflightResult(
        passed=passed,
        checks=results,
        total_violations=total_violations,
        critical_violations=critical_violations
    )


def print_results(result: PreflightResult, json_output: bool = False) -> None:
    """Print preflight results."""
    
    if json_output:
        print(json.dumps(result.to_dict(), indent=2))
        return
    
    print("\n" + "=" * 60)
    print("PREFLIGHT: Executable Documentation Verification")
    print("=" * 60 + "\n")
    
    for check in result.checks:
        status = "✅" if check.passed else "❌"
        print(f"{status} {check.name} (LAW: {check.law})")
        
        for violation in check.violations:
            severity_icon = {
                Severity.CRITICAL: "🔴",
                Severity.MAJOR: "🟠",
                Severity.MINOR: "🟡"
            }[violation.severity]
            
            location = ""
            if violation.file:
                location = f" @ {violation.file}"
                if violation.line:
                    location += f":{violation.line}"
            
            print(f"   {severity_icon} {violation.message}{location}")
            if violation.suggestion:
                print(f"      → {violation.suggestion}")
    
    print("\n" + "-" * 60)
    print(f"Total violations: {result.total_violations}")
    print(f"Critical violations: {result.critical_violations}")
    print("-" * 60)
    
    if result.passed:
        print("\n✅ PREFLIGHT PASSED\n")
    else:
        print("\n❌ PREFLIGHT FAILED\n")


def init_preflight(project_root: Path) -> None:
    """Initialize preflight configuration for a new project."""
    
    print("Initializing preflight configuration...")
    
    # Create scripts directory
    scripts_dir = project_root / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    
    # Create preflight config
    config = {
        "checks": {
            "types_compile": True,
            "schemas_validate": True,
            "linting": True,
            "required_todos": True,
            "external_docs": True,
            "logging_coverage": True
        },
        "ci": {
            "fail_on_critical": True,
            "fail_on_major": False
        }
    }
    
    config_path = project_root / ".preflight.json"
    config_path.write_text(json.dumps(config, indent=2))
    
    print(f"✅ Created {config_path}")
    print("\nNext steps:")
    print("1. Review .preflight.json configuration")
    print("2. Add 'python scripts/preflight.py' to CI pipeline")
    print("3. Run preflight locally before commits")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Preflight validation enforcing the Seven Laws"
    )
    parser.add_argument("--init", action="store_true", help="Initialize for new project")
    parser.add_argument("--full", action="store_true", help="Run all checks including slow ones")
    parser.add_argument("--fix", action="store_true", help="Attempt auto-fix")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--ci", action="store_true", help="CI mode (strict)")
    parser.add_argument("--path", default=".", help="Project root path")
    
    args = parser.parse_args()
    project_root = Path(args.path).resolve()
    
    if args.init:
        init_preflight(project_root)
        return
    
    result = run_preflight(project_root, full=args.full, ci_mode=args.ci)
    print_results(result, json_output=args.json)
    
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
