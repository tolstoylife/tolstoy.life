#!/bin/bash
# Graph Health Check Script
# Verifies FalkorDB connection and displays statistics

set -e

FALKORDB_HOST="${FALKORDB_HOST:-localhost}"
FALKORDB_PORT="${FALKORDB_PORT:-6379}"
PROJECT_DIR="${PROJECT_DIR:-$HOME/Projects/limitless-cli}"

echo "🔍 FalkorDB Health Check"
echo "========================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    echo "   Start Docker first: open -a Docker"
    exit 1
fi
echo "✅ Docker is running"

# Check if FalkorDB container exists and is running
if docker ps --format '{{.Names}}' | grep -q falkordb; then
    echo "✅ FalkorDB container is running"
else
    echo "⚠️  FalkorDB container not running"
    echo "   Start with: docker compose up -d"

    # Try to start it
    if [ -f "$PROJECT_DIR/docker-compose.yml" ]; then
        echo ""
        echo "Attempting to start FalkorDB..."
        cd "$PROJECT_DIR" && docker compose up -d
        sleep 2
    else
        exit 1
    fi
fi

# Check Redis connectivity
echo ""
echo "Testing connection to $FALKORDB_HOST:$FALKORDB_PORT..."
if redis-cli -h "$FALKORDB_HOST" -p "$FALKORDB_PORT" ping > /dev/null 2>&1; then
    echo "✅ Connection successful"
else
    echo "❌ Cannot connect to FalkorDB"
    exit 1
fi

# Get graph info
echo ""
echo "📊 Graph Statistics"
echo "-------------------"

cd "$PROJECT_DIR"

# Run stats command
bun run src/index.ts graph stats 2>/dev/null || {
    echo "⚠️  Could not get graph stats"
    echo "   Run 'graph init' first if this is a new installation"
}

echo ""
echo "✅ Health check complete"
