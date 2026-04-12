---
type: daily-note
date: {{date:YYYY-MM-DD}}
day: {{date:dddd}}
tags:
  - daily
created: {{date:YYYY-MM-DD HH:mm}}
---

# {{date:dddd, MMMM DD, YYYY}}

> [!tip] Daily Focus
> What's the one thing that matters most today?

## 📋 Tasks

```dataview
TASK
WHERE !completed
AND file.name = this.file.name
```

- [ ]

## 📝 Notes

### Morning

### Afternoon

### Evening

## 🎯 Goals Progress

- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

## 💡 Ideas & Insights

## 🔗 Links Created Today

```dataview
LIST
WHERE file.cday = date(this.date)
AND file.name != this.file.name
SORT file.ctime DESC
LIMIT 10
```

## 📊 Metrics

**Words Written:** `= this.word-count`
**Notes Created:** `= length(filter(file.lists.file, (f) => f.cday = date(this.date)))`
**Tasks Completed:** `= length(filter(file.tasks, (t) => t.completed))`

## 🌅 Daily Reflection

### What went well?

### What could be improved?

### What did I learn?

## Navigation

← [[{{date:YYYY-MM-DD,offset:-1d}}|Yesterday]] | [[{{date:YYYY-MM-DD,offset:1d}}|Tomorrow]] →

---

**Weather:**
**Mood:**
**Energy Level:** ⚡⚡⚡⚡⚡
