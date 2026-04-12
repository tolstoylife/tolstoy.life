#!/bin/bash
# Installation script for hm-skills/schema
# Ensures all dependencies are installed and global wrapper is configured

set -e

SKILL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
USER_BIN="$HOME/bin"
WRAPPER_PATH="$USER_BIN/schema-gen"

echo "==================================================================="
echo "Installing hm-skills/schema skill"
echo "==================================================================="

# 1. Check Python version
echo ""
echo "1. Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 not found. Please install Python 3.9 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"

# Determine Python executable
if command -v /opt/homebrew/bin/python3.13 &> /dev/null; then
    PYTHON_EXEC="/opt/homebrew/bin/python3.13"
elif command -v python3.13 &> /dev/null; then
    PYTHON_EXEC=$(which python3.13)
else
    PYTHON_EXEC=$(which python3)
fi
echo "  Using: $PYTHON_EXEC"

# 2. Install Python dependencies
echo ""
echo "2. Installing Python dependencies..."
$PYTHON_EXEC -m pip install --user jinja2 pyyaml 2>&1 | tail -3

# 3. Install spaCy language model
echo ""
echo "3. Installing spaCy language model..."
if $PYTHON_EXEC -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null; then
    echo "✓ spaCy model already installed"
else
    $PYTHON_EXEC -m spacy download en_core_web_sm
fi

# 4. Create global wrapper
echo ""
echo "4. Creating global wrapper..."
mkdir -p "$USER_BIN"

cat > "$WRAPPER_PATH" << EOF
#!/bin/bash
# Global wrapper for hm-skills/schema
SCHEMA_DIR="$SKILL_DIR"
cd "\$SCHEMA_DIR" && $PYTHON_EXEC -m scripts.schema_cli "\$@"
EOF

chmod +x "$WRAPPER_PATH"
echo "✓ Wrapper created: $WRAPPER_PATH"

# 5. Configure PATH
echo ""
echo "5. Configuring PATH..."
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q "export PATH=\"\$HOME/bin:\$PATH\"" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# Add user bin to PATH for custom scripts" >> "$SHELL_RC"
        echo "export PATH=\"\$HOME/bin:\$PATH\"" >> "$SHELL_RC"
        echo "✓ Added ~/bin to PATH in $SHELL_RC"
        echo "  Run: source $SHELL_RC"
    else
        echo "✓ PATH already configured"
    fi
fi

# 6. Test installation
echo ""
echo "6. Testing installation..."
if "$WRAPPER_PATH" --help &> /dev/null; then
    echo "✓ schema-gen command works"
else
    echo "❌ Error: schema-gen command failed"
    exit 1
fi

# 7. Summary
echo ""
echo "==================================================================="
echo "✅ Installation complete!"
echo "==================================================================="
echo ""
echo "Usage:"
echo "  schema-gen --input \"your text\" --output schema.md"
echo ""
echo "For help:"
echo "  schema-gen --help"
echo ""
echo "Note: You may need to restart your shell or run:"
echo "  source $SHELL_RC"
echo ""
