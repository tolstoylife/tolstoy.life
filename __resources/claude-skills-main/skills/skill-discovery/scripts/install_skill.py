#!/usr/bin/env python3
"""
Wrapper for claude-plugins skills install
Provides deterministic skill installation with validation
"""
import sys
import subprocess
import re
from typing import Tuple, Optional


def validate_identifier(identifier: str) -> Tuple[bool, Optional[str]]:
    """
    Validate skill identifier format

    Valid formats:
        - @owner/repo/skill-name
        - owner/repo/skill-name
        - skill-name (resolved via registry)

    Returns:
        (is_valid, error_message)
    """
    if not identifier:
        return False, "Identifier cannot be empty"

    # Check for valid characters (alphanumeric, hyphens, slashes, @)
    if not re.match(r'^[@a-zA-Z0-9/_-]+$', identifier):
        return False, f"Invalid characters in identifier: {identifier}"

    return True, None


def install_skill(identifier: str, local: bool = False, force: bool = False) -> bool:
    """
    Install a skill using claude-plugins CLI

    Args:
        identifier: Skill identifier (@owner/repo/name or variants)
        local: Install to local ./.claude/skills/ instead of global
        force: Force reinstall if already exists

    Returns:
        True if installation successful, False otherwise
    """
    # Validate identifier
    is_valid, error = validate_identifier(identifier)
    if not is_valid:
        print(f"❌ Validation error: {error}", file=sys.stderr)
        return False

    # Construct command
    cmd = ["claude-plugins", "skills", "install", identifier]

    if local:
        cmd.append("--local")
    if force:
        cmd.append("--force")

    try:
        print(f"📦 Installing skill: {identifier}")
        if local:
            print("   Scope: Local (./.claude/skills/)")
        else:
            print("   Scope: Global (~/.claude/skills/)")

        # Execute installation
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )

        print("✅ Installation successful!")
        if result.stdout:
            print(result.stdout)

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}", file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        return False
    except FileNotFoundError:
        print("❌ claude-plugins command not found. Install it with: npm install -g claude-plugins", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return False


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: install_skill.py <identifier> [--local] [--force]")
        print("Examples:")
        print("  install_skill.py @anthropics/claude-code/frontend-design")
        print("  install_skill.py skill-writer --local")
        print("  install_skill.py @obra/superpowers/brainstorming --force")
        sys.exit(1)

    identifier = sys.argv[1]
    local = "--local" in sys.argv or "-l" in sys.argv
    force = "--force" in sys.argv or "-f" in sys.argv

    success = install_skill(identifier, local, force)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
