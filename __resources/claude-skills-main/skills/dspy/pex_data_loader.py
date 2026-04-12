import json
import csv
import re
from typing import List, Dict, Any
from pathlib import Path

# Paths to data
JSON_PATH = '/Users/mikhail/Cursor/Knowledge-Graph/data/CICM_ANZCA_LO_SAQ.json'
CSV_PATH = '/Users/mikhail/Cursor/Knowledge-Graph/data/CICM_SAQ.csv'
SAQ_ATOMIC_PATH = '/Users/mikhail/Cursor/Knowledge-Graph/data/SAQAtomic2.fixed.json'

def load_saqs(csv_path: str) -> List[Dict[str, Any]]:
    saqs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.strip(): v for k, v in row.items() if k}
            if 'saq' in clean_row and clean_row['saq']:
                saqs.append({
                    'id': clean_row.get('n', 'unknown'),
                    'question': clean_row.get('saq', ''),
                    'comment': clean_row.get('ec', ''),
                    'pass_rate': clean_row.get('pr', ''),
                    'type': 'SAQ'
                })
    return saqs

def load_atomic_saqs(json_path: str) -> List[Dict[str, Any]]:
    """Load enhanced SAQ data from the atomic JSON file."""
    atomic_saqs = []
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            # Handle potential JSON issues by reading as string first
            content = f.read()
            # Basic fix for common trailing comma issues if present
            content = re.sub(r',(\s*[\]}])', r'\1', content)
            data = json.loads(content)

        for entry in data:
            # Extract content from messages if available, or direct content
            content = entry.get('content', '')
            if not content and entry.get('messages'):
                content = entry['messages'][0].get('content', '')

            if content:
                # Extract entities for better retrieval
                entities = entry.get('entities', [])
                entity_text = " ".join([e.get('label', '') for e in entities])

                atomic_saqs.append({
                    'id': str(entry.get('source_id', 'unknown')),
                    'chunk_uid': entry.get('chunk_uid', ''),
                    'content': content,
                    'entities': entities,
                    'entity_text': entity_text,
                    'type': 'AtomicSAQ'
                })
    except Exception as e:
        print(f"Error loading atomic SAQs: {e}")

    return atomic_saqs

def parse_frontmatter(content: str) -> Dict[str, Any]:
    """Extract YAML frontmatter and body from markdown content."""
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    metadata = {}
    body = content

    if match:
        frontmatter_str = match.group(1)
        body = match.group(2)
        for line in frontmatter_str.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                metadata[key.strip()] = val.strip().strip('"')

    return metadata, body.strip()

def load_los(json_path: str) -> List[Dict[str, Any]]:
    los = []
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        items = data.get('items', [])
        for item in items:
            if item.get('type') == 'file' and item.get('path', '').endswith('.md'):
                content = item.get('content', '')
                meta, body = parse_frontmatter(content)

                if '/LO/' in item.get('path', ''):
                    los.append({
                        'id': Path(item['path']).stem,
                        'content': body,
                        'metadata': meta,
                        'path': item['path'],
                        'type': 'LO'
                    })
    except Exception as e:
        print(f"Error loading LOs: {e}")

    return los

if __name__ == "__main__":
    print("Loading Data...")
    saqs = load_saqs(CSV_PATH)
    atomic = load_atomic_saqs(SAQ_ATOMIC_PATH)
    los = load_los(JSON_PATH)

    print(f"Loaded {len(saqs)} CSV SAQs")
    print(f"Loaded {len(atomic)} Atomic SAQs")
    print(f"Loaded {len(los)} LOs")
