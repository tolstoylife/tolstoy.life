# Limit guessing in Claude

Rules:
- Only extract values explicitly stated in the documentation.
- When a value is ambiguous, missing, or unclear, leave the
  field BLANK.
- A wrong answer is 3x worse than a blank. When in doubt,
  leave it blank.
- For each field with a value, add a "Source" column:
  EXTRACTED = directly stated, exact match
  INFERRED = derived, calculated, or interpreted
- For every INFERRED field, add a one-sentence explanation.
- For every BLANK field, add a row to a separate "Flags" table
  explaining why the value could not be extracted.