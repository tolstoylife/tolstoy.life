import re
import json

INPUT_FILE = '/Users/mikhail/Cursor/Knowledge-Graph/data/SAQAtomic2.fixed.json'
OUTPUT_FILE = '/Users/mikhail/Cursor/Knowledge-Graph/data/SAQAtomic2.fixed.clean.json'

def fix_json_file():
    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # The issue is specifically at line 171-172 where a `]` and `}` for the "messages" array and its object are missing before `"source_id"`.
    # Based on the `sed` output:
    # 167: "messages": [
    # 168:   {
    # 169:     "content": "..."
    # 170:   }
    # 171:
    # 172:     "source_id": 3680,
    #
    # It looks like line 171 is empty or malformed, and line 172 starts a new property of the parent object, BUT the "messages" array wasn't closed properly.
    # Actually, looking at the previous object (lines 1-49), "messages" is a list of objects.
    # The structure should be:
    # {
    #   "messages": [ { "content": "..." } ],
    #   "source_id": ...
    # }
    #
    # The sed output shows:
    # 170:       }
    # 171:
    # 172:        "source_id": 3680,
    #
    # This means the `]` closing the `messages` list is MISSING.
    # And potentially the comma after it.
    #
    # Let's fix this globally:
    # Pattern:  [whitespace] } [whitespace] "source_id":
    # Replacement:  } ], "source_id":

    # Fix 1: Closing messages array if missing
    # We look for `}` (closing content object) followed by `"source_id"`, implying missed `],`
    fixed_content = re.sub(r'(\s*})\s*("source_id":)', r'\1 ], \2', content)

    # Fix 2: General missing comma between objects in the main list
    # Pattern: } [whitespace] {
    fixed_content = re.sub(r'}\s*({)', r'},\1', fixed_content)

    # Try parsing
    try:
        data = json.loads(fixed_content)
        print(f"Successfully parsed {len(data)} records.")
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except json.JSONDecodeError as e:
        print(f"Still failing: {e}")
        # If it fails, let's dump the snippet around the failure
        idx = e.pos
        start = max(0, idx - 100)
        end = min(len(fixed_content), idx + 100)
        print(f"Context around error:\n{fixed_content[start:end]}")
        return False

if __name__ == "__main__":
    fix_json_file()
