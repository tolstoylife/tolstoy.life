# bd Claude Code Skill - Installation Guide

## Quick Install

```bash
# Link the skill to Claude Code
ln -s /Users/mikhail/Downloads/architect/bd ~/.claude/skills/bd

# Restart Claude Code
# The skill will activate automatically when needed
```

## Detailed Installation Steps

### 1. Prerequisites

**Required:**
- ✅ Claude Code installed and running
- ✅ bd (beads) installed: `which bd` should return a path
- ✅ Git repository to track issues in

**Optional but Recommended:**
- `jq` - JSON processing for advanced queries
- `sqlite3` - Direct database queries
- `bv` - Interactive issue graph visualization
- `graphviz` - Static graph rendering

### 2. Verify bd Installation

```bash
# Check bd is installed
which bd
# Expected: /opt/homebrew/bin/bd (or similar)

# Check version
bd --version
# Expected: bd version 0.28.0+

# If not installed:
brew install bd  # macOS
# or follow bd installation instructions for your OS
```

### 3. Install the Skill

**Option A: Symbolic Link (Recommended)**

```bash
# Create link to skill directory
ln -s /Users/mikhail/Downloads/architect/bd ~/.claude/skills/bd

# Verify link
ls -la ~/.claude/skills/bd
```

**Option B: Copy Files**

```bash
# Copy skill to Claude Code skills directory
cp -r /Users/mikhail/Downloads/architect/bd ~/.claude/skills/

# Verify copy
ls -la ~/.claude/skills/bd
```

**Option C: Custom Location**

If you prefer a different location:

```bash
# Copy to custom location
cp -r /Users/mikhail/Downloads/architect/bd ~/my-skills/bd

# Link to Claude Code
ln -s ~/my-skills/bd ~/.claude/skills/bd
```

### 4. Verify Installation

```bash
# Check skill files exist
ls ~/.claude/skills/bd/SKILL.md
ls ~/.claude/skills/bd/README.md
ls ~/.claude/skills/bd/scripts/issue-validator.sh

# Verify YAML frontmatter
head -20 ~/.claude/skills/bd/SKILL.md
# Should show YAML with name: bd, description, etc.
```

### 5. Initialize bd in a Project

```bash
# Navigate to your project
cd /path/to/your/project

# Initialize bd
bd init

# Optional: Configure project-specific prefix
bd config set prefix myproject

# Verify setup
bd status
ls -la .beads/
```

### 6. Test the Skill

Start Claude Code and try:

```
User: "Create a task to add user authentication"
```

Claude should use bd to create the issue:
```bash
bd create "Add user authentication" --type task --priority 2
```

Or try:
```
User: "What tasks are blocking us?"
```

Claude should run:
```bash
bd blocked
```

### 7. Optional: Install Supporting Tools

**jq (JSON processing)**
```bash
brew install jq  # macOS
```

**sqlite3 (Database queries)**
```bash
brew install sqlite3  # macOS (usually pre-installed)
```

**bv (Interactive visualization)**
```bash
# Check bv installation instructions
# (Separate tool, may require additional setup)
```

**graphviz (Graph rendering)**
```bash
brew install graphviz  # macOS
```

## Directory Structure After Installation

```
~/.claude/skills/bd/
├── SKILL.md                    # Main skill documentation
├── README.md                   # Skill overview
├── scripts/
│   └── issue-validator.sh      # Validation script
├── references/
│   ├── task-patterns.md        # Common patterns
│   └── daemon-mode.md          # Daemon/RPC guide
└── assets/
    └── cheatsheet.md           # Quick reference
```

## Configuration

### bd Configuration

Create `.beads/config.json` in your project:

```json
{
  "prefix": "myproject",
  "default_priority": 2,
  "default_type": "task",
  "daemon": {
    "enabled": true,
    "port": 0,
    "sync_interval": 300
  },
  "git": {
    "auto_sync": true,
    "sync_branch": "main",
    "remote": "origin"
  }
}
```

### Git Hooks (Recommended)

```bash
# Install bd git hooks for auto-sync
bd hooks install

# Hooks added:
# - pre-commit: Validate issue references
# - post-commit: Auto-sync JSONL
```

### Claude Code Settings

No additional Claude Code configuration needed. The skill activates automatically based on:

1. **Context**: Presence of `.beads/` directory
2. **Triggers**: Keywords like "task tracking", "issue management"
3. **User Intent**: Explicit bd commands or issue operations

## Troubleshooting Installation

### Skill Not Activating

**Problem**: Claude Code doesn't use the bd skill

**Solutions:**
1. Verify skill path: `ls ~/.claude/skills/bd/SKILL.md`
2. Check YAML frontmatter is valid: `head -20 ~/.claude/skills/bd/SKILL.md`
3. Restart Claude Code
4. Try explicit trigger: "Use bd to track this task"

### bd Not Found

**Problem**: `bd: command not found`

**Solutions:**
```bash
# Check installation
which bd

# Install if missing
brew install bd  # macOS
# or follow platform-specific instructions
```

### Permission Issues

**Problem**: Permission denied when running scripts

**Solutions:**
```bash
# Make validator executable
chmod +x ~/.claude/skills/bd/scripts/issue-validator.sh

# Or run with bash
bash ~/.claude/skills/bd/scripts/issue-validator.sh
```

### Daemon Won't Start

**Problem**: bd daemon fails to start

**Solutions:**
```bash
# Check daemon status
bd daemon status

# View logs
bd daemon logs

# Force restart
bd daemon stop --force
bd daemon start

# Or use direct mode (bypass daemon)
bd --no-daemon list
```

## Updating the Skill

### Update Skill Files

```bash
# If using symbolic link, update source
cd /Users/mikhail/Downloads/architect/bd
git pull  # if git-tracked

# If using copy, re-copy
rm -rf ~/.claude/skills/bd
cp -r /Users/mikhail/Downloads/architect/bd ~/.claude/skills/

# Restart Claude Code
```

### Update bd

```bash
# Update bd itself
brew upgrade bd  # macOS

# Restart daemon
bd daemon stop
bd daemon start
```

## Verification Checklist

- [ ] bd installed and accessible: `which bd`
- [ ] Skill files in place: `ls ~/.claude/skills/bd/SKILL.md`
- [ ] YAML frontmatter valid: `head -20 ~/.claude/skills/bd/SKILL.md`
- [ ] Project initialized: `bd init` in project directory
- [ ] Daemon running: `bd daemon status`
- [ ] Git hooks installed: `bd hooks install`
- [ ] Test issue creation: `bd create "Test task"`
- [ ] Skill activates in Claude Code: Ask "Create a task"

## Next Steps

After installation:

1. **Initialize in Project**: `cd your-project && bd init`
2. **Create First Issue**: `bd create "First task"`
3. **Visualize**: `bv .beads/beads.jsonl` (if bv installed)
4. **Test Skill**: Ask Claude to "Show open tasks"
5. **Read Docs**: `cat ~/.claude/skills/bd/assets/cheatsheet.md`

## Getting Help

### Documentation

- **Quick Reference**: `~/.claude/skills/bd/assets/cheatsheet.md`
- **Task Patterns**: `~/.claude/skills/bd/references/task-patterns.md`
- **Daemon Mode**: `~/.claude/skills/bd/references/daemon-mode.md`
- **Complete Guide**: `~/.claude/skills/bd/SKILL.md`

### Commands

```bash
# Built-in help
bd help
bd <command> --help

# Quick start guide
bd quickstart

# Health check
bd doctor
```

### Validation

```bash
# Run comprehensive validation
~/.claude/skills/bd/scripts/issue-validator.sh

# With auto-fix
~/.claude/skills/bd/scripts/issue-validator.sh --fix
```

## Uninstallation

If you need to remove the skill:

```bash
# Remove skill link/directory
rm ~/.claude/skills/bd

# Optionally remove bd data from projects
cd your-project
rm -rf .beads/

# Uninstall bd (if desired)
brew uninstall bd  # macOS
```

## Support

- **bd Issues**: Report to bd repository
- **Skill Issues**: Check `/Users/mikhail/Downloads/architect/bd/README.md`
- **Claude Code**: See Claude Code documentation

---

**Installation Complete!**

The bd skill is now ready to use with Claude Code. Try asking:
- "Create a task for implementing authentication"
- "Show me what's blocking our work"
- "List all high priority open issues"

Claude will automatically use bd to manage your tasks and issues.
