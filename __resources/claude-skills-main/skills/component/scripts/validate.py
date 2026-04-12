#!/usr/bin/env python3
"""
Component Validator - Validates Claude Code configuration files.

Usage:
    python validate.py <path>           # Single file or directory
    python validate.py <dir> --strict   # Fail on warnings
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# Parameter compatibility matrix from SKILL.md
PARAMS = {
    'command': {
        'allowed': {'description', 'allowed-tools', 'model', 'argument-hint', 'disable-model-invocation'},
        'required': {'description'},
        'forbidden': {'name', 'permissionMode', 'skills', 'keep-coding-instructions', 'disallowed-tools'},
    },
    'agent': {
        'allowed': {'description', 'allowed-tools', 'disallowed-tools', 'model', 'permissionMode', 'skills'},
        'required': {'description'},
        'forbidden': {'argument-hint', 'disable-model-invocation', 'keep-coding-instructions'},
    },
    'skill': {
        'allowed': {'name', 'description', 'allowed-tools', 'license', 'metadata', 'compatibility'},
        'required': {'name', 'description'},
        'forbidden': {'model', 'argument-hint', 'disable-model-invocation', 'permissionMode', 'skills', 'keep-coding-instructions'},
    },
    'style': {
        'allowed': {'name', 'description', 'keep-coding-instructions'},
        'required': {'name', 'description'},
        'forbidden': {'allowed-tools', 'model', 'argument-hint', 'disable-model-invocation', 'permissionMode', 'skills'},
    },
}

VALID_MODELS = {'sonnet', 'opus', 'haiku'}
VALID_PERMISSIONS = {'ask', 'allow', 'deny'}


def extract_frontmatter(content: str) -> Optional[str]:
    """Extract YAML frontmatter."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    return match.group(1) if match else None


def parse_yaml(yaml_str: str) -> Dict[str, any]:
    """Simple YAML parser (no deps)."""
    result = {}
    current_key = None
    current_value = []
    in_array = False
    
    for line in yaml_str.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        
        key_match = re.match(r'^([\w-]+)\s*:\s*(.*)', line)
        if key_match and not line.startswith(' '):
            if current_key:
                val = current_value if in_array else '\n'.join(current_value).strip()
                result[current_key] = val
            
            current_key = key_match.group(1)
            value = key_match.group(2).strip()
            
            if value.startswith('[') and value.endswith(']'):
                items = value[1:-1].split(',')
                current_value = [i.strip() for i in items if i.strip()]
                in_array = True
            elif value == '' or value == '[]':
                current_value = []
                in_array = True
            else:
                current_value = [value]
                in_array = False
        elif stripped.startswith('- ') and current_key:
            current_value.append(stripped[2:])
            in_array = True
    
    if current_key:
        val = current_value if in_array else '\n'.join(current_value).strip()
        result[current_key] = val
    
    return result


def detect_type(filepath: Path) -> Optional[str]:
    """Detect component type from path."""
    path_str = str(filepath).lower()
    if '/commands/' in path_str:
        return 'command'
    if '/agents/' in path_str:
        return 'agent'
    if '/skills/' in path_str and filepath.name.upper() == 'SKILL.MD':
        return 'skill'
    if '/styles/' in path_str:
        return 'style'
    return None


def validate(filepath: Path, comp_type: str) -> Tuple[List[str], List[str]]:
    """Validate component. Returns (errors, warnings)."""
    errors, warnings = [], []
    
    try:
        content = filepath.read_text()
    except Exception as e:
        return [f"Cannot read: {e}"], []
    
    fm = extract_frontmatter(content)
    if not fm:
        return ["No YAML frontmatter"], []
    
    params = parse_yaml(fm)
    param_keys = set(params.keys())
    spec = PARAMS[comp_type]
    
    # Required
    missing = spec['required'] - param_keys
    if missing:
        errors.append(f"Missing required: {', '.join(missing)}")
    
    # Forbidden
    forbidden = param_keys & spec['forbidden']
    if forbidden:
        errors.append(f"Forbidden for {comp_type}: {', '.join(forbidden)}")
    
    # Unknown
    unknown = param_keys - spec['allowed'] - spec['forbidden']
    if unknown:
        warnings.append(f"Unknown params: {', '.join(unknown)}")
    
    # Validate model
    if 'model' in params:
        model = params['model'].lower() if isinstance(params['model'], str) else str(params['model'][0]).lower()
        if model not in VALID_MODELS:
            errors.append(f"Invalid model '{model}'. Use: {VALID_MODELS}")
    
    # Validate permissionMode
    if 'permissionMode' in params:
        mode = params['permissionMode'].lower() if isinstance(params['permissionMode'], str) else str(params['permissionMode'][0]).lower()
        if mode not in VALID_PERMISSIONS:
            errors.append(f"Invalid permissionMode '{mode}'. Use: {VALID_PERMISSIONS}")
    
    # Validate booleans
    for field in ['disable-model-invocation', 'keep-coding-instructions']:
        if field in params:
            val = params[field].lower() if isinstance(params[field], str) else str(params[field][0]).lower()
            if val not in ('true', 'false'):
                errors.append(f"'{field}' must be true/false")
    
    # Skill-specific: name format
    if comp_type == 'skill' and 'name' in params:
        name = params['name'] if isinstance(params['name'], str) else params['name'][0]
        if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$', name):
            errors.append(f"Skill name '{name}' must be kebab-case")
        if '--' in name:
            errors.append(f"Skill name cannot have consecutive hyphens")
        if len(name) > 64:
            errors.append(f"Skill name too long ({len(name)} > 64)")
    
    # Skill-specific: description length
    if comp_type == 'skill' and 'description' in params:
        desc = params['description'] if isinstance(params['description'], str) else ' '.join(params['description'])
        if len(desc) > 1024:
            errors.append(f"Description too long ({len(desc)} > 1024)")
        if '<' in desc or '>' in desc:
            errors.append("Description cannot contain angle brackets")
    
    return errors, warnings


def validate_directory(root: Path, strict: bool = False) -> int:
    """Validate all components in directory. Returns exit code."""
    patterns = [
        ('**/commands/*.md', 'command'),
        ('**/agents/*.md', 'agent'),
        ('**/skills/*/SKILL.md', 'skill'),
        ('**/styles/*.md', 'style'),
    ]
    
    total_errors = 0
    total_warnings = 0
    
    for pattern, comp_type in patterns:
        for filepath in root.glob(pattern):
            errors, warnings = validate(filepath, comp_type)
            
            if errors:
                print(f"❌ {filepath}")
                for e in errors:
                    print(f"   ERROR: {e}")
                total_errors += len(errors)
            elif warnings:
                print(f"⚠️  {filepath}")
                for w in warnings:
                    print(f"   WARN: {w}")
                total_warnings += len(warnings)
            else:
                print(f"✓ {filepath}")
    
    print(f"\n{total_errors} errors, {total_warnings} warnings")
    
    if total_errors > 0:
        return 1
    if strict and total_warnings > 0:
        return 1
    return 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Validate Claude Code components')
    parser.add_argument('path', help='File or directory to validate')
    parser.add_argument('--strict', action='store_true', help='Fail on warnings')
    args = parser.parse_args()
    
    target = Path(args.path)
    
    if target.is_file():
        comp_type = detect_type(target)
        if not comp_type:
            print(f"Cannot determine type for: {target}")
            print("Place in commands/, agents/, skills/, or styles/")
            sys.exit(1)
        
        errors, warnings = validate(target, comp_type)
        if errors:
            print(f"❌ {target}")
            for e in errors:
                print(f"   ERROR: {e}")
            sys.exit(1)
        if warnings:
            print(f"⚠️  {target}")
            for w in warnings:
                print(f"   WARN: {w}")
            sys.exit(1 if args.strict else 0)
        print(f"✓ {target} ({comp_type})")
        sys.exit(0)
    
    elif target.is_dir():
        sys.exit(validate_directory(target, args.strict))
    
    else:
        print(f"Not found: {target}")
        sys.exit(1)


if __name__ == '__main__':
    main()
