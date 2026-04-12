# Error Resolution Guide

## Common Errors

### "mapping values are not allowed here"
**Cause:** Unquoted colon in value  
**Solution:** Add quotes: `title: 'Chapter 1: Introduction'`

### "could not find expected ':'"
**Cause:** Unbalanced quotes  
**Solution:** Check quote pairing

### Value truncated
**Cause:** Unquoted # character  
**Solution:** Quote the value: `task: 'PR #123'`

### Variables not replacing
**Cause:** Field name mismatch (case-sensitive)  
**Solution:** Verify exact field name from data

## Troubleshooting Workflow

1. Check error message for line number
2. Verify YAML syntax at that line
3. Check for special characters
4. Ensure proper quoting
5. Test with simpler data first

See [examples/troubleshooting/](../examples/troubleshooting/) for demonstrations.

---
Version 2.0.0 | See [SKILL.md](../SKILL.md)
