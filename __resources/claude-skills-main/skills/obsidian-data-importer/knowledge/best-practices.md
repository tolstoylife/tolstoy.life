# Best Practices

## Data Preparation
- Clean special characters in advance if possible
- Use consistent date formats (ISO 8601 recommended)
- Ensure unique values for note naming field
- Remove completely empty columns

## Template Design
- Always quote string values in YAML
- Use conditionals for optional fields
- Include inline documentation
- Test with sample data first

## Graph Structure
- Use [[Wikilinks]] for entity relationships
- Apply hierarchical tags (project/alpha/task-001)
- Create MOCs for large imports
- Standardize naming conventions

## Validation
- Preview first before bulk import
- Review 3-5 sample notes after import
- Check for YAML parsing errors
- Verify links resolve correctly

## Performance
- Limit imports to <1000 notes at once
- Use batch processing for large datasets
- Consider splitting by category or project

See [examples/](../examples/) for demonstrations.

---
Version 2.0.0 | See [SKILL.md](../SKILL.md)
