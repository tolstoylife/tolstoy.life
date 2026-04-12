# Example 01: Simple Task List CSV

## Scenario

You have a CSV file exported from your task management system with tasks, statuses, priorities, and assignees. You want to create individual Obsidian notes for each task to track work and link to related projects.

## Input Data

**File:** `tasks.csv`

```csv
Task,Status,Priority,Due,Assignee,Notes
Review PR #456,In Progress,High,2025-10-25,John Smith,Check security implications & update documentation
Update API documentation,Not Started,Medium,2025-10-28,Jane Doe,Include new endpoints from v2.0 release
```

### Data Characteristics
- **5 tasks** across different statuses
- **Special characters:** '#' in task names, '&' in notes
- **Dates** in ISO format
- **Person names** suitable for linking
- **Categorical fields:** Status, Priority

## Processing Steps

### Step 1: Field Analysis

When you provide this CSV, the system analyzes:

| Field | Type | YAML Safe? | Treatment |
|-------|------|------------|-----------|
| Task | String | ⚠️ Contains '#' | Frontmatter (quoted) + Note name |
| Status | Categorical | ✅ Safe | Frontmatter + Tag |
| Priority | Categorical | ✅ Safe | Frontmatter + Tag |
| Due | Date | ✅ Safe | Frontmatter |
| Assignee | String | ✅ Safe | Frontmatter + Link |
| Notes | String (long) | ⚠️ Contains '&' '#' | Body (quoted) |

**Key Findings:**
- Task field is unique → suitable for note names
- Status and Priority are categorical → good for tags
- Assignee should become wikilinks
- Special characters require YAML quoting

### Step 2: Template Generation

The system generates `template.hbs` (see file in this directory) with:
- YAML-safe frontmatter
- Quoted fields with special characters
- Hierarchical tags (status/Priority, priority/High)
- Wikilinks for assignees
- Conditional sections for optional fields

### Step 3: Preview

**Sample output for first task:**

```markdown
---
title: 'Review PR #456'
status: 'In Progress'
priority: 'High'
due: '2025-10-25'
assigned: '[[John Smith]]'
tags: [task, status/In Progress, priority/High]
type: task
---

# Review PR #456

**Status:** In Progress | **Priority:** High | **Due:** 2025-10-25

**Assigned to:** [[John Smith]]

---

## Notes

Check security implications & update documentation

---

## Activity Log

[Track work and updates here]

## Related Tasks

[Link related tasks and notes]
```

### Step 4: Import

1. Save `template.hbs` to your Obsidian vault
2. Open JSON/CSV Importer plugin
3. Select `tasks.csv`
4. Select `template.hbs`
5. Set "Task" as the field for note names
6. Choose target folder (e.g., "Tasks/")
7. Click Import

Result: 5 new notes created, one for each task.

## Key Learning Points

### ✅ YAML Safety Demonstrated
- Fields with '#' are quoted: `'Review PR #456'`
- Fields with '&' are quoted in notes section
- This prevents YAML parsing errors

### ✅ Smart Field Mapping
- **Frontmatter:** Short, queryable fields (status, priority, due, assignee)
- **Body:** Long text (notes)
- **Tags:** Hierarchical categories (status/In Progress)
- **Links:** Person names become navigable nodes

### ✅ Graph Structure
After import, your graph shows:
- Task notes connected to people (assignees)
- Tasks clustered by status tags
- Tasks clustered by priority tags
- Clickable links between related entities

## Variations

### Add Project Field
If your CSV has a Project column:
```handlebars
project: '[[{{Project}}]]'
tags: [task, project/{{Project}}, status/{{Status}}]
```

### Add Time Tracking
```handlebars
{{#if TimeSpent}}
time_spent: '{{TimeSpent}}'
{{/if}}
```

### Link Related Tasks
```handlebars
{{#if RelatedTo}}
## Related
{{#each RelatedTo}}
- [[{{this}}]]
{{/each}}
{{/if}}
```

## Troubleshooting

### Issue: Task names with '#' break YAML

**Cause:** Unquoted hash character  
**Solution:** Template already handles this with quotes: `title: '{{Task}}'`

### Issue: Tags not showing in Obsidian

**Cause:** Spaces in tag values  
**Solution:** Template formats as: `status/In-Progress` (hyphens instead of spaces)

### Issue: Assignee links not created

**Cause:** Assignee notes don't exist yet  
**Solution:** Create person notes manually or import assignees as separate batch

## Next Steps

1. Try this example with your own task data
2. Customize the template to match your workflow
3. Explore [02-contacts-csv](../02-contacts-csv/) for more special character handling
4. See [04-nested-json-projects](../../intermediate/04-nested-json-projects/) for more complex structures

---

**Complexity:** ⭐ Simple  
**Duration:** 3-5 minutes  
**Skills Practiced:** CSV parsing, YAML quoting, basic templating