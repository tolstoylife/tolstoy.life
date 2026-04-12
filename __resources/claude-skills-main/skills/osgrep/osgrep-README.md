# osgrep Claude Code Skill

Complete Claude Code skill for osgrep semantic code search.

## Quick Start

```bash
# 1. Review the skill
cat osgrep/SKILL.md

# 2. Review codebase documentation
cat osgrep-codebase/README.md

# 3. Test the validator
cd osgrep/scripts
chmod +x search-validator.sh
./search-validator.sh "test query" 0.6 5
```

## Installation

### Option 1: Copy to Claude Skills Directory
```bash
cp -r osgrep ~/.claude/skills/
cp -r osgrep-codebase ~/.claude/skills/
```

### Option 2: Use Custom Location
Keep files in current location and reference via `context_codebase` path in SKILL.md.

## What's Included

- **SKILL.md**: Main skill definition with YAML frontmatter
- **Codebase**: Complete agents-md knowledge base
  - Core principles (semantic search, hybrid ranking)
  - Type definitions (TypeScript)
  - Workflow templates
  - README overview
- **References**: 
  - 200+ search pattern examples
  - Complete configuration guide
- **Assets**: Quick reference cheatsheet
- **Scripts**: Search quality validator

## Total Documentation

~4,410 lines of comprehensive guidance

## Key Features

- Semantic search principles
- Hybrid ranking (RRF + ColBERT)
- 10 workflow templates
- 200+ query patterns
- Complete config reference
- Quality validation script
- Integration with Claude Code

## Usage with Claude Code

The skill automatically activates when:
- User requests semantic code search
- Exploring unfamiliar codebases
- Finding similar implementations
- Architectural understanding

## See Also

- **osgrep-OVERVIEW.md**: Complete package documentation
- **osgrep/assets/cheatsheet.md**: Quick reference
- **osgrep-codebase/README.md**: Technical overview
