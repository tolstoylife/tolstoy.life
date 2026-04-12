import re
import json

INPUT_FILE = '/Users/mikhail/Cursor/Knowledge-Graph/data/SAQAtomic2.fixed.json'
OUTPUT_FILE = '/Users/mikhail/Cursor/Knowledge-Graph/data/SAQAtomic2.fixed.clean.json'

def fix_json_file():
    print(f"Reading {INPUT_FILE}...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"Content length: {len(content)} chars")

        # 1. basic fix: ensure it starts with [ and ends with ]
        content = content.strip()
        if not content.startswith('['): content = '[' + content
        if not content.endswith(']'): content = content + ']'

        # 2. Fix missing commas between objects
        # Look for } followed by whitespace (including newlines) then {
        # and insert a comma.
        fixed_content = re.sub(r'}\s*({)', r'},\1', content)

        # 3. Remove any trailing commas before the closing bracket (common issue)
        fixed_content = re.sub(r',\s*]', ']', fixed_content)

        print("Attempting to parse fixed content...")
        data = json.loads(fixed_content)
        print(f"Successfully parsed {len(data)} records.")

        print(f"Writing to {OUTPUT_FILE}...")
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print("Done.")
        return True

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error after naive fix: {e}")
        # If naive fix fails, let's try to isolate where it fails or use a more aggressive approach
        # For now, let's see if this works.
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    fix_json_file()
