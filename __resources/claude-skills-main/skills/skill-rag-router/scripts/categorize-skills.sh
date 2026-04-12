#!/bin/bash
# Categorize all skills into router categories
# Generates a JSON mapping of skill -> router category

set -e

SKILL_DIR="${HOME}/.claude/skills"
ROUTER_DIR="${HOME}/.claude/skills/routers"
OUTPUT_FILE="${HOME}/.claude/.skill-index/cache/skill-categories.json"

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Category patterns (keywords -> router)
categorize_skill() {
    local skill_path="$1"
    local skill_name=$(basename "$(dirname "$skill_path")")
    local content=$(cat "$skill_path" 2>/dev/null | tr '[:upper:]' '[:lower:]')

    # Skip router skills themselves
    if echo "$skill_name" | grep -qE '(meta-router|development-router|analysis-router|documentation-router|research-router|infrastructure-router|data-router|reasoning-router)'; then
        echo "meta"
        return
    fi

    # Reasoning patterns (check first - most specific)
    if echo "$content" | grep -qE '(reasoning|atomic|calculus|holarchic|ontology|logic|λ|formal|axiom|proof|synthesis|hypothesis|verification)'; then
        echo "reasoning"
        return
    fi

    # Data patterns
    if echo "$content" | grep -qE '(graph|neo4j|cypher|vector|embedding|rag|knowledge graph|database|csv|data process|structured data|graphrag)'; then
        echo "data"
        return
    fi

    # Meta patterns (skills about skills)
    if echo "$content" | grep -qE '(skill|agent|workflow|orchestrat|router|command|plugin|mcp server builder|component)'; then
        echo "meta"
        return
    fi

    # Research patterns
    if echo "$content" | grep -qE '(research|investigat|explore|discover|deep.?research|comprehensive|multi.?source)'; then
        echo "research"
        return
    fi

    # Analysis patterns
    if echo "$content" | grep -qE '(analyz|debug|troubleshoot|diagnos|security|performance|audit|review|critical|retrospective|validation)'; then
        echo "analysis"
        return
    fi

    # Documentation patterns
    if echo "$content" | grep -qE '(document|readme|api.?doc|guide|tutorial|explain|obsidian|markdown|pdf|docx|documentation)'; then
        echo "documentation"
        return
    fi

    # Infrastructure patterns
    if echo "$content" | grep -qE '(mcp|infrastructure|deploy|ci.?cd|observability|tool|terminal|cli|server|docker|kubernetes)'; then
        echo "infrastructure"
        return
    fi

    # Development patterns (default for code-related)
    if echo "$content" | grep -qE '(implement|build|code|component|frontend|backend|api|feature|refactor|test|tdd|fullstack|design system)'; then
        echo "development"
        return
    fi

    # Default to meta if nothing matches
    echo "meta"
}

# Build categorization
echo "{"
first=true

find "$SKILL_DIR" -name "SKILL.md" -type f 2>/dev/null | while read skill_path; do
    skill_name=$(basename "$(dirname "$skill_path")")
    category=$(categorize_skill "$skill_path")

    if [ "$first" = true ]; then
        first=false
    else
        echo ","
    fi
    echo -n "  \"$skill_name\": \"$category\""
done

echo ""
echo "}"
