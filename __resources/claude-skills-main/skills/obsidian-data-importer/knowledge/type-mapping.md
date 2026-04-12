# Type Mapping Strategies

## Data Type Detection

### String
Default type for text data. Check for special characters requiring YAML quoting.

### Number
Integer or decimal values. No quoting needed in YAML.

### Boolean
true/false, yes/no, 1/0. No quoting needed.

### Date
ISO 8601 or common formats. Quote for safety in YAML.

### URL
Contains ://. Quote for consistency.

### Array
Multiple values (JSON). Use iteration in template.

## Mapping Strategies

See [yaml-safety.md](yaml-safety.md) for quoting rules.  
See [handlebars-syntax.md](handlebars-syntax.md) for iteration patterns.

---
Version 2.0.0 | See [SKILL.md](../SKILL.md)
