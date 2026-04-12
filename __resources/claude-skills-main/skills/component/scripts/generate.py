#!/usr/bin/env python3
"""
Component Generator - Scaffold Claude Code configuration files.

Usage:
    python generate.py command <name> [-d desc] [-t tools] [-m model]
    python generate.py agent <name> [-d desc] [-p permission] [-s skills]
    python generate.py skill <name> [-d desc]
    python generate.py style <name> [-d desc]
"""

import argparse
from pathlib import Path

TEMPLATES = {
    'command': '''---
description: {description}
allowed-tools: [{tools}]
model: {model}
{extras}---

# {title}

## Purpose

[What this command accomplishes]

## Procedure

1. [Step one]
2. [Step two]
3. [Output]
''',

    'agent': '''---
description: {description}
allowed-tools: [{tools}]
model: {model}
permissionMode: {permission}
{skills_line}---

# {title}

## Identity

[Role, expertise, personality]

## Capabilities

[What this agent can do]

## Decision Heuristics

[When to proceed vs escalate]
''',

    'skill': '''---
name: {name}
description: {description}
---

# {title}

## Purpose

[Problem this skill solves]

## Workflow

### Step 1

[Procedure]

### Step 2

[Procedure]
''',

    'style': '''---
name: {name}
description: {description}
keep-coding-instructions: true
---

# {title}

## Interaction Pattern

[How interactions flow]

## Output Format

[Expected outputs]
'''
}


def gen_command(args):
    extras = ''
    if args.argument_hint:
        extras = f'argument-hint: [{args.argument_hint}]\n'
    
    content = TEMPLATES['command'].format(
        description=args.description or f'Execute {args.name} operation',
        tools=args.tools or 'Read, Write, Agent',
        model=args.model or 'sonnet',
        extras=extras,
        title=args.name.replace('-', ' ').title(),
    )
    
    out = Path(args.output) / f'{args.name}.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content)
    print(f"✓ Created: {out}")


def gen_agent(args):
    skills_line = f'skills: [{args.skills}]\n' if args.skills else ''
    
    content = TEMPLATES['agent'].format(
        description=args.description or f'{args.name.title()} specialist agent',
        tools=args.tools or 'Read, Write',
        model=args.model or 'sonnet',
        permission=args.permission or 'ask',
        skills_line=skills_line,
        title=args.name.replace('-', ' ').title(),
    )
    
    out = Path(args.output) / f'{args.name}.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content)
    print(f"✓ Created: {out}")


def gen_skill(args):
    content = TEMPLATES['skill'].format(
        name=args.name,
        description=args.description or f'Procedures for {args.name} tasks. Trigger when working with {args.name}.',
        title=args.name.replace('-', ' ').title(),
    )
    
    skill_dir = Path(args.output) / args.name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / 'SKILL.md').write_text(content)
    print(f"✓ Created: {skill_dir}/SKILL.md")


def gen_style(args):
    content = TEMPLATES['style'].format(
        name=args.name,
        description=args.description or f'{args.name.title()} interaction mode',
        title=args.name.replace('-', ' ').title(),
    )
    
    out = Path(args.output) / f'{args.name}.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content)
    print(f"✓ Created: {out}")


def main():
    parser = argparse.ArgumentParser(description='Generate Claude Code components')
    sub = parser.add_subparsers(dest='type', required=True)
    
    # Command
    p = sub.add_parser('command')
    p.add_argument('name')
    p.add_argument('-d', '--description')
    p.add_argument('-t', '--tools', default='Read, Write, Agent')
    p.add_argument('-m', '--model', choices=['sonnet', 'opus', 'haiku'], default='sonnet')
    p.add_argument('-a', '--argument-hint')
    p.add_argument('-o', '--output', default='.claude/commands')
    
    # Agent
    p = sub.add_parser('agent')
    p.add_argument('name')
    p.add_argument('-d', '--description')
    p.add_argument('-t', '--tools', default='Read, Write')
    p.add_argument('-m', '--model', choices=['sonnet', 'opus', 'haiku'], default='sonnet')
    p.add_argument('-p', '--permission', choices=['ask', 'allow', 'deny'], default='ask')
    p.add_argument('-s', '--skills')
    p.add_argument('-o', '--output', default='.claude/agents')
    
    # Skill
    p = sub.add_parser('skill')
    p.add_argument('name')
    p.add_argument('-d', '--description')
    p.add_argument('-o', '--output', default='.claude/skills')
    
    # Style
    p = sub.add_parser('style')
    p.add_argument('name')
    p.add_argument('-d', '--description')
    p.add_argument('-o', '--output', default='.claude/styles')
    
    args = parser.parse_args()
    
    {'command': gen_command, 'agent': gen_agent, 'skill': gen_skill, 'style': gen_style}[args.type](args)


if __name__ == '__main__':
    main()
