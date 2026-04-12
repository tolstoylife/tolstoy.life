import re
import json

INPUT_FILE = '/Users/mikhail/Cursor/Knowledge-Graph/data/SAQAtomic2.fixed.json'
OUTPUT_FILE = '/Users/mikhail/Cursor/Knowledge-Graph/data/SAQAtomic2.fixed.clean.json'

def fix_json_file():
    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    fixed_lines = []
    for i, line in enumerate(lines):
        # Specific patch for line 172 issue or general pattern
        # The error was at line 172 column 9. Let's look around there.
        # It's likely a missing comma between objects in the list.
        # Pattern:  } [newline] {  -> } , [newline] {
        stripped = line.strip()
        if stripped == '{':
            # Check previous non-empty line
            j = len(fixed_lines) - 1
            while j >= 0:
                prev = fixed_lines[j].strip()
                if prev:
                    if prev == '}' or prev.endswith('}'):
                        # Insert comma to the end of that previous line
                        fixed_lines[j] = fixed_lines[j].rstrip() + ',\n'
                    break
                j -= 1
        fixed_lines.append(line)

    content = "".join(fixed_lines)

    # Try parsing
    try:
        data = json.loads(content)
        print(f"Successfully parsed {len(data)} records.")
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except json.JSONDecodeError as e:
        print(f"Still failing: {e}")
        # Manual patch for the specific error observed previously
        # line 172: "source_id": 3680,
        # This implies the previous object didn't close properly or didn't have a comma.
        # We'll use a more aggressive regex on the full string.
        return False

if __name__ == "__main__":
    fix_json_file()
