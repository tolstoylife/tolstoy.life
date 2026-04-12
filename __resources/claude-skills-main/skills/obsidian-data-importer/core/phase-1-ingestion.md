# Phase 1: Data Ingestion & Analysis

## Purpose

Parse input data and generate a comprehensive field inventory with type inference, safety analysis, and treatment recommendations.

## Inputs

- Raw CSV or JSON content (file or pasted data)
- Optional: User hints about data structure

## Process Flow

```
Raw Data
    ↓
Format Detection
    ↓
Structure Parsing
    ↓
Field Analysis
    ↓
Field Inventory (Output)
```

## Step 1: Format Detection

**Objective:** Determine if data is CSV or JSON

**Detection Logic:**
```
IF starts with '{' or '[' AND valid JSON → JSON
ELIF contains comma-separated values → CSV
ELSE → Request clarification
```

**Confidence Indicators:**
- JSON: Proper bracket balance, quoted strings, colons
- CSV: Consistent column count across rows, header row
- Ambiguous: Single-column CSV might look like text

## Step 2: Structure Parsing

### For CSV:

**Extract:**
1. Header row (column names)
2. Data rows (limit to first 10 for analysis)
3. Total row count (estimate)

**Validation:**
- All rows have same column count
- Headers are unique
- No completely empty columns

**Output:**
```javascript
{
  format: 'csv',
  headers: ['Field1', 'Field2', ...],
  sampleRows: [...],
  totalRows: N,
  issues: [...]
}
```

### For JSON:

**Extract:**
1. Top-level structure (array of objects or single object)
2. All property paths (including nested)
3. Nesting depth
4. Sample objects (first 3-5)

**Path Discovery:**
```javascript
// Flat JSON
{"title": "Book"} → ["title"]

// Nested JSON
{"book": {"title": "Name"}} → ["book.title"]

// Array in object
{"tags": ["a", "b"]} → ["tags"] (marked as array)
```

**Output:**
```javascript
{
  format: 'json',
  structure: 'array' | 'object',
  paths: ['field1', 'nested.field2', 'array.0.field3'],
  depth: N,
  sampleObjects: [...],
  totalObjects: N,
  issues: [...]
}
```

## Step 3: Field Analysis

For each field/path, determine:

### 3.1 Data Type Inference

**Algorithm:**
```
FOR each field:
  Get sample values
  
  IF all values match date pattern → DATE
  ELIF all values are numeric → NUMBER
  ELIF all values are true/false → BOOLEAN
  ELIF all values contain :// → URL
  ELIF values are array → ARRAY
  ELSE → STRING
  
  IF STRING:
    Check for special characters
    Check length distribution
    Detect categorical (few unique values)
```

**Type Patterns:**
- **DATE**: ISO 8601, common formats (2025-10-21, 10/21/2025, etc.)
- **NUMBER**: Integer or decimal, possibly with formatting
- **BOOLEAN**: true/false, yes/no, 1/0, Y/N
- **URL**: Contains `://` or starts with `www.`
- **EMAIL**: Contains `@` with domain pattern
- **ARRAY**: Multiple values in JSON array
- **STRING**: Default fallback

### 3.2 Special Character Detection

**Check for YAML-problematic characters:**
- `: # & * @ ` % ! ? | > [ ] { }`

**Risk Assessment:**
```
LOW: No special characters
MEDIUM: Has special chars but can be quoted
HIGH: Has both quote types or newlines (needs block)
```

### 3.3 Treatment Recommendation

**Frontmatter Candidates:**
- Unique identifiers
- Categorical fields (status, type, category)
- Dates
- Short strings (<50 chars)
- Fields that should be queryable

**Body Candidates:**
- Long text (>50 chars)
- Descriptions
- Notes
- Content fields

**Tag Candidates:**
- Categorical with few values (<20 unique)
- Status fields
- Type indicators
- Project/category names

**Link Candidates:**
- Fields referencing other entities
- Person names
- Project names
- Related items

### 3.4 Unique Field Detection

**Identify fields suitable for note names:**
- Has unique values across rows
- Reasonably short (<100 chars)
- No file-system-invalid characters (: / \ * ? " < > |)
- Not empty or null

**Ranking:**
1. Field explicitly named "id", "name", "title"
2. String fields with 100% unique values
3. Combination of fields that create uniqueness

## Step 4: Field Inventory Generation

**Output Format:**

```markdown
## 📊 Field Inventory

### CSV: filename.csv (50 rows)

| # | Field Name | Type | Sample Values | YAML Safe | Recommended Treatment |
|---|------------|------|---------------|-----------|----------------------|
| 1 | Title | String | "Task 1", "Task 2" | ⚠️ May contain ':' | Frontmatter (note name) |
| 2 | Description | String (long) | "Complete the..." | ✅ Safe | Body (main content) |
| 3 | Status | Categorical | "Done", "In Progress" | ✅ Safe | Frontmatter + Tag |
| 4 | Priority | Categorical | "High", "Medium", "Low" | ✅ Safe | Frontmatter + Tag |
| 5 | DueDate | Date | "2025-10-21" | ✅ Safe | Frontmatter |
| 6 | Assignee | String | "John", "Jane" | ✅ Safe | Frontmatter + Link |
| 7 | Notes | String (long) | "Need to check..." | ⚠️ May contain '#' | Body (quoted) |
| 8 | URL | URL | "https://..." | ✅ Safe | Frontmatter |

### Analysis Summary
- **Unique ID Candidates:** Title (100% unique)
- **Tag-worthy Fields:** Status, Priority
- **Link-worthy Fields:** Assignee
- **Special Attention:** Title (contains ':' in 30% of rows), Notes (contains '#')

### Recommendations
1. **Note Naming:** Use Title field (ensure YAML-safe in template)
2. **Status Tracking:** Include Status and Priority in frontmatter
3. **Relationships:** Convert Assignee to wikilinks
4. **Safety:** Quote Title and Notes fields
```

## Key Algorithms

### Type Inference Pseudocode

```python
def infer_type(values):
    # Remove null/empty
    values = [v for v in values if v is not None and v != '']
    
    if len(values) == 0:
        return 'UNKNOWN'
    
    # Check dates
    if all(is_date_pattern(v) for v in values):
        return 'DATE'
    
    # Check numbers
    if all(is_numeric(v) for v in values):
        return 'NUMBER'
    
    # Check booleans
    if all(v in ['true', 'false', '1', '0', 'yes', 'no'] for v in values):
        return 'BOOLEAN'
    
    # Check URLs
    if all('://' in v or v.startswith('www.') for v in values):
        return 'URL'
    
    # Check arrays (JSON only)
    if all(isinstance(v, list) for v in values):
        return 'ARRAY'
    
    # Default to string
    return 'STRING'

def detect_categorical(values):
    unique_count = len(set(values))
    total_count = len(values)
    
    # If less than 20 unique values and represents <50% of total
    if unique_count < 20 and unique_count < (total_count * 0.5):
        return True
    
    return False
```

### Special Character Detection

```python
def detect_special_chars(value):
    yaml_special = [':','#','&','*','@','`','%','!','?','|','>','[',']','{','}']
    
    found = []
    for char in yaml_special:
        if char in value:
            found.append(char)
    
    return {
        'has_issues': len(found) > 0,
        'characters': found,
        'risk_level': determine_risk(found, value)
    }

def determine_risk(chars, value):
    if '\n' in value or ('\'' in value and '"' in value):
        return 'HIGH'  # Needs block literal
    elif chars:
        return 'MEDIUM'  # Needs quoting
    else:
        return 'LOW'  # Safe
```

## Output Specification

The phase must produce:

1. **Field Inventory Table** - Formatted as markdown
2. **Analysis Summary** - Key findings and recommendations
3. **Proposed Mappings** - Which fields go where (frontmatter/body/tags/links)
4. **Safety Warnings** - Any fields requiring special handling
5. **Unique Field Recommendation** - Best field for note naming

This output feeds directly into Phase 2 (Strategy Selection).

## Error Handling

**Empty Data:**
- Message: "No data provided or file is empty"
- Action: Request valid input

**Malformed CSV:**
- Message: "Inconsistent column count detected"
- Action: Show row numbers with issues, suggest repair

**Invalid JSON:**
- Message: "JSON syntax error at position X"
- Action: Show error location, suggest validation

**No Unique Fields:**
- Message: "No field suitable for note names found"
- Action: Suggest combining fields or using row numbers

## Related Modules

- **Next Phase:** [Phase 2: Strategy Selection](phase-2-strategy.md)
- **Depends On:** DataParser module
- **Used By:** FieldAnalyzer module
- **References:** [type-mapping.md](../knowledge/type-mapping.md)

---

**Version:** 2.0.0  
**Last Updated:** October 2025