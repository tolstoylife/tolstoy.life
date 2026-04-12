#!/bin/bash
# Comprehensive integration test for schema skill

set -e  # Exit on error

echo "=== Schema Skill Integration Tests ==="
echo

# Create test output directory
TEST_DIR="test_outputs"
mkdir -p "$TEST_DIR"

echo "1. Testing Text Input"
python3 -m scripts.schema_cli \
  --input "AI systems analyze data to generate insights" \
  --output "$TEST_DIR/text-test.md" \
  --format obsidian,jsonld \
  --verbose
echo "✓ Text input test passed"
echo

echo "2. Testing JSON Input"
python3 -m scripts.schema_cli \
  --input examples/sample-data.json \
  --output "$TEST_DIR/json-test.md" \
  --format obsidian,cypher \
  --verbose
echo "✓ JSON input test passed"
echo

echo "3. Testing Markdown Input"
python3 -m scripts.schema_cli \
  --input examples/sample-markdown.md \
  --output "$TEST_DIR/markdown-test.md" \
  --format obsidian,graphql \
  --verbose
echo "✓ Markdown input test passed"
echo

echo "4. Testing Code Input"
python3 -m scripts.schema_cli \
  --input scripts/utils/validation.py \
  --output "$TEST_DIR/code-test.md" \
  --format obsidian \
  --verbose
echo "✓ Code input test passed"
echo

echo "5. Testing Fractal Mode"
python3 -m scripts.schema_cli \
  --input examples/simple-ontology.md \
  --mode fractal \
  --output "$TEST_DIR/fractal-test.md" \
  --verbose
echo "✓ Fractal mode test passed"
echo

echo "6. Testing All Formats"
python3 -m scripts.schema_cli \
  --input examples/sample-markdown.md \
  --format obsidian,jsonld,cypher,graphql \
  --output "$TEST_DIR/all-formats.md" \
  --verbose
echo "✓ All formats test passed"
echo

echo "7. Verifying Output Files"
EXPECTED_FILES=(
  "$TEST_DIR/text-test.md"
  "$TEST_DIR/text-test.jsonld"
  "$TEST_DIR/json-test.md"
  "$TEST_DIR/json-test.cypher"
  "$TEST_DIR/markdown-test.md"
  "$TEST_DIR/markdown-test.graphql"
  "$TEST_DIR/code-test.md"
  "$TEST_DIR/fractal-test.md"
  "$TEST_DIR/all-formats.md"
  "$TEST_DIR/all-formats.jsonld"
  "$TEST_DIR/all-formats.cypher"
  "$TEST_DIR/all-formats.graphql"
)

for file in "${EXPECTED_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "✗ Missing file: $file"
    exit 1
  fi
done
echo "✓ All expected files generated"
echo

echo "8. File Size Check"
for file in "${EXPECTED_FILES[@]}"; do
  if [ ! -s "$file" ]; then
    echo "✗ Empty file: $file"
    exit 1
  fi
done
echo "✓ All files have content"
echo

echo "=== All Integration Tests Passed ==="
echo
echo "Generated files in: $TEST_DIR/"
ls -lh "$TEST_DIR/"
