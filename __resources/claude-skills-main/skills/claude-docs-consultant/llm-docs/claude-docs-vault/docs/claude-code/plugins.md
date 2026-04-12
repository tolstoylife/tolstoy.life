---
created: 2025-11-05
modified: 2025-11-05
title: "Plugins"
url: https://docs.claude.com/en/docs/claude-code/plugins
category: docs
subcategory: claude-code
description: "Extend Claude Code with custom commands, agents, hooks, Skills, and MCP servers through the plugin system."
tags:
  - docs
  - claude-code
related:
  - '[[amazon-bedrock]]'
  - '[[analytics]]'
  - '[[checkpointing]]'
  - '[[claude-code-on-the-web]]'
  - '[[cli-reference]]'
---

# Plugins

Extend Claude Code with custom commands, agents, hooks, Skills, and MCP servers through the plugin system.

> [!tip]
> For complete technical specifications and schemas, see [[plugins-reference|Plugins reference]]. For marketplace management, see [[plugin-marketplaces|Plugin marketplaces]].

Plugins let you extend Claude Code with custom functionality that can be shared across projects and teams. Install plugins from [[plugin-marketplaces|marketplaces]] to add pre-built commands, agents, hooks, Skills, and MCP servers, or create your own to automate your workflows.

## Quickstart

Let's create a simple greeting plugin to get you familiar with the plugin system. We'll build a working plugin that adds a custom command, test it locally, and understand the core concepts.

### Prerequisites

* Claude Code installed on your machine
* Basic familiarity with command-line tools

### Create your first plugin


  
**Step 1: Create the marketplace structure**

```bash  theme={null}
    mkdir test-marketplace
    cd test-marketplace
    ```


  
**Step 2: Create the plugin directory**

```bash  theme={null}
    mkdir my-first-plugin
    cd my-first-plugin
    ```


  
**Step 3: Create the plugin manifest**

```bash Create .claude-plugin/plugin.json theme={null}
    mkdir .claude-plugin
    cat > .claude-plugin/plugin.json << 'EOF'
    {
    "name": "my-first-plugin",
    "description": "A simple greeting plugin to learn the basics",
    "version": "1.0.0",
    "author": {
    "name": "Your Name"
    }
    }
    EOF
    ```


  
**Step 4: Add a custom command**

```bash Create commands/hello.md theme={null}
    mkdir commands
    cat > commands/hello.md << 'EOF'
    ---
    description: Greet the user with a personalized message
    ---

    # Hello Command

    Greet the user warmly and ask how you can help them today. Make the greeting personal and encouraging.
    EOF
    ```


  
**Step 5: Create the marketplace manifest**

```bash Create marketplace.json theme={null}
    cd ..
    mkdir .claude-plugin
    cat > .claude-plugin/marketplace.json << 'EOF'
    {
    "name": "test-marketplace",
    "owner": {
    "name": "Test User"
    },
    "plugins": [
    {
      "name": "my-first-plugin",
      "source": "./my-first-plugin",
      "description": "My first test plugin"
    }
    ]
    }
    EOF
    ```


  
**Step 6: Install and test your plugin**

```bash Start Claude Code from parent directory theme={null}
    cd ..
    claude
    ```

    ```shell Add the test marketplace theme={null}
    /plugin marketplace add ./test-marketplace
    ```

    ```shell Install your plugin theme={null}
    /plugin install my-first-plugin@test-marketplace
    ```

    Select "Install now". You'll then need to restart Claude Code in order to use the new plugin.

    ```shell Try your new command theme={null}
    /hello
    ```

    You'll see Claude use your greeting command! Check `/help` to see your new command listed.



You've successfully created and tested a plugin with these key components:

* **Plugin manifest** (`.claude-plugin/plugin.json`) - Describes your plugin's metadata
* **Commands directory** (`commands/`) - Contains your custom slash commands
* **Test marketplace** - Allows you to test your plugin locally

### Plugin structure overview

Your plugin follows this basic structure:

```
my-first-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/                 # Custom slash commands (optional)
│   └── hello.md
├── agents/                   # Custom agents (optional)
│   └── helper.md
├── skills/                   # Agent Skills (optional)
│   └── my-skill/
│       └── SKILL.md
└── hooks/                    # Event handlers (optional)
    └── hooks.json
```

**Additional components you can add:**

* **Commands**: Create markdown files in `commands/` directory
* **Agents**: Create agent definitions in `agents/` directory
* **Skills**: Create `SKILL.md` files in `skills/` directory
* **Hooks**: Create `hooks/hooks.json` for event handling
* **MCP servers**: Create `.mcp.json` for external tool integration

> [!note]
> **Next steps**: Ready to add more features? Jump to [Develop more complex plugins](#develop-more-complex-plugins) to add agents, hooks, and MCP servers. For complete technical specifications of all plugin components, see [[plugins-reference|Plugins reference]].

***

## Install and manage plugins

Learn how to discover, install, and manage plugins to extend your Claude Code capabilities.

### Prerequisites

* Claude Code installed and running
* Basic familiarity with command-line interfaces

### Add marketplaces

Marketplaces are catalogs of available plugins. Add them to discover and install plugins:

```shell Add a marketplace theme={null}
/plugin marketplace add your-org/claude-plugins
```

```shell Browse available plugins theme={null}
/plugin
```

For detailed marketplace management including Git repositories, local development, and team distribution, see [[plugin-marketplaces|Plugin marketplaces]].

### Install plugins

#### Via interactive menu (recommended for discovery)

```shell Open the plugin management interface theme={null}
/plugin
```

Select "Browse Plugins" to see available options with descriptions, features, and installation options.

#### Via direct commands (for quick installation)

```shell Install a specific plugin theme={null}
/plugin install formatter@your-org
```

```shell Enable a disabled plugin theme={null}
/plugin enable plugin-name@marketplace-name
```

```shell Disable without uninstalling theme={null}
/plugin disable plugin-name@marketplace-name
```

```shell Completely remove a plugin theme={null}
/plugin uninstall plugin-name@marketplace-name
```

### Verify installation

After installing a plugin:

1. **Check available commands**: Run `/help` to see new commands
2. **Test plugin features**: Try the plugin's commands and features
3. **Review plugin details**: Use `/plugin` → "Manage Plugins" to see what the plugin provides

## Set up team plugin workflows

Configure plugins at the repository level to ensure consistent tooling across your team. When team members trust your repository folder, Claude Code automatically installs specified marketplaces and plugins.

**To set up team plugins:**

1. Add marketplace and plugin configuration to your repository's `.claude/settings.json`
2. Team members trust the repository folder
3. Plugins install automatically for all team members

For complete instructions including configuration examples, marketplace setup, and rollout best practices, see [[plugin-marketplaces#how-to-configure-team-marketplaces|Configure team marketplaces]].

***

## Develop more complex plugins

Once you're comfortable with basic plugins, you can create more sophisticated extensions.

### Add Skills to your plugin

Plugins can include [[skills|Agent Skills]] to extend Claude's capabilities. Skills are model-invoked—Claude autonomously uses them based on the task context.

To add Skills to your plugin, create a `skills/` directory at your plugin root and add Skill folders with `SKILL.md` files. Plugin Skills are automatically available when the plugin is installed.

For complete Skill authoring guidance, see [[skills|Agent Skills]].

### Organize complex plugins

For plugins with many components, organize your directory structure by functionality. For complete directory layouts and organization patterns, see [[plugins-reference#plugin-directory-structure|Plugin directory structure]].

### Test your plugins locally

When developing plugins, use a local marketplace to test changes iteratively. This workflow builds on the quickstart pattern and works for plugins of any complexity.


  
**Step 1: Set up your development structure**

Organize your plugin and marketplace for testing:

    ```bash Create directory structure theme={null}
    mkdir dev-marketplace
    cd dev-marketplace
    mkdir my-plugin
    ```

    This creates:

    ```
    dev-marketplace/
    ├── .claude-plugin/marketplace.json  (you'll create this)
    └── my-plugin/                        (your plugin under development)
        ├── .claude-plugin/plugin.json
        ├── commands/
        ├── agents/
        └── hooks/
    ```


  
**Step 2: Create the marketplace manifest**

```bash Create marketplace.json theme={null}
    mkdir .claude-plugin
    cat > .claude-plugin/marketplace.json << 'EOF'
    {
    "name": "dev-marketplace",
    "owner": {
    "name": "Developer"
    },
    "plugins": [
    {
      "name": "my-plugin",
      "source": "./my-plugin",
      "description": "Plugin under development"
    }
    ]
    }
    EOF
    ```


  
**Step 3: Install and test**

```bash Start Claude Code from parent directory theme={null}
    cd ..
    claude
    ```

    ```shell Add your development marketplace theme={null}
    /plugin marketplace add ./dev-marketplace
    ```

    ```shell Install your plugin theme={null}
    /plugin install my-plugin@dev-marketplace
    ```

    Test your plugin components:

    * Try your commands with `/command-name`
    * Check that agents appear in `/agents`
    * Verify hooks work as expected


  
**Step 4: Iterate on your plugin**

After making changes to your plugin code:

    ```shell Uninstall the current version theme={null}
    /plugin uninstall my-plugin@dev-marketplace
    ```

    ```shell Reinstall to test changes theme={null}
    /plugin install my-plugin@dev-marketplace
    ```

    Repeat this cycle as you develop and refine your plugin.



> [!note]
> **For multiple plugins**: Organize plugins in subdirectories like `./plugins/plugin-name` and update your marketplace.json accordingly. See [[plugin-marketplaces#plugin-sources|Plugin sources]] for organization patterns.

### Debug plugin issues

If your plugin isn't working as expected:

1. **Check the structure**: Ensure your directories are at the plugin root, not inside `.claude-plugin/`
2. **Test components individually**: Check each command, agent, and hook separately
3. **Use validation and debugging tools**: See [[plugins-reference#debugging-and-development-tools|Debugging and development tools]] for CLI commands and troubleshooting techniques

### Share your plugins

When your plugin is ready to share:

1. **Add documentation**: Include a README.md with installation and usage instructions
2. **Version your plugin**: Use semantic versioning in your `plugin.json`
3. **Create or use a marketplace**: Distribute through plugin marketplaces for easy installation
4. **Test with others**: Have team members test the plugin before wider distribution

> [!note]
> For complete technical specifications, debugging techniques, and distribution strategies, see [[plugins-reference|Plugins reference]].

***

## Next steps

Now that you understand Claude Code's plugin system, here are suggested paths for different goals:

### For plugin users

* **Discover plugins**: Browse community marketplaces for useful tools
* **Team adoption**: Set up repository-level plugins for your projects
* **Marketplace management**: Learn to manage multiple plugin sources
* **Advanced usage**: Explore plugin combinations and workflows

### For plugin developers

* **Create your first marketplace**: [[plugin-marketplaces|Plugin marketplaces guide]]
* **Advanced components**: Dive deeper into specific plugin components:
  * [[slash-commands|Slash commands]] - Command development details
  * [[sub-agents|Subagents]] - Agent configuration and capabilities
  * [[skills|Agent Skills]] - Extend Claude's capabilities
  * [[hooks|Hooks]] - Event handling and automation
  * [[mcp|MCP]] - External tool integration
* **Distribution strategies**: Package and share your plugins effectively
* **Community contribution**: Consider contributing to community plugin collections

### For team leads and administrators

* **Repository configuration**: Set up automatic plugin installation for team projects
* **Plugin governance**: Establish guidelines for plugin approval and security review
* **Marketplace maintenance**: Create and maintain organization-specific plugin catalogs
* **Training and documentation**: Help team members adopt plugin workflows effectively

## See also

* [[plugin-marketplaces|Plugin marketplaces]] - Creating and managing plugin catalogs
* [[slash-commands|Slash commands]] - Understanding custom commands
* [[sub-agents|Subagents]] - Creating and using specialized agents
* [[skills|Agent Skills]] - Extend Claude's capabilities
* [[hooks|Hooks]] - Automating workflows with event handlers
* [[mcp|MCP]] - Connecting to external tools and services
* [[settings|Settings]] - Configuration options for plugins

---

**Source:** [Official Documentation](https://docs.claude.com/en/docs/claude-code/plugins)
