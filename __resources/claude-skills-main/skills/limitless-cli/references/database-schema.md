# FalkorDB Database Schema Reference

## Node Types

### Lifelog
```cypher
(:Lifelog {
  id: string,           // Limitless API ID
  title: string?,
  startTime: string,    // ISO-8601
  endTime: string,      // ISO-8601
  duration: number,     // seconds
  isStarred: boolean,
  markdown: string?,
  createdAt: string,
  updatedAt: string
})
```

### Person
```cypher
(:Person {
  id: string,           // Generated UUID
  name: string,
  mentionCount: number,
  firstSeen: string,    // ISO-8601
  lastSeen: string,     // ISO-8601
  createdAt: string,
  updatedAt: string
})
```

### Topic
```cypher
(:Topic {
  id: string,
  name: string,
  category: string?,    // medical, technical, business, etc.
  mentionCount: number,
  createdAt: string,
  updatedAt: string
})
```

### Action
```cypher
(:Action {
  id: string,
  action: string,
  context: string,
  status: string,       // pending, in_progress, completed
  dueDate: string?,
  createdAt: string,
  updatedAt: string
})
```

### TimeWindow
```cypher
(:TimeWindow {
  id: string,           // day:2026-01-04, week:2026-W01, month:2026-01
  type: string,         // day, week, month
  startTime: string,
  endTime: string,
  lifelogCount: number,
  totalDuration: number
})
```

### Chat
```cypher
(:Chat {
  id: string,
  title: string?,
  messageCount: number,
  createdAt: string,
  updatedAt: string
})
```

## Relationships

| Relationship | From | To | Properties |
|--------------|------|-----|------------|
| `MENTIONS` | Lifelog | Person | count, firstMention |
| `SPOKE_IN` | Person | Lifelog | - |
| `HAS_TOPIC` | Lifelog | Topic | relevance |
| `DISCUSSED_IN` | Topic | Lifelog | - |
| `OCCURRED_AT` | Lifelog | TimeWindow | - |
| `CO_OCCURRED` | Person | Person | count, strength |
| `RELATED_TOPIC` | Topic | Topic | strength |
| `HAS_ACTION` | Lifelog | Action | - |
| `ASSIGNED_TO` | Action | Person | - |
| `DERIVED_FROM` | Chat | Lifelog | correlation |

## Indexes (21 Total)

### Node Indexes
```cypher
CREATE INDEX lifelog_id FOR (l:Lifelog) ON (l.id)
CREATE INDEX lifelog_startTime FOR (l:Lifelog) ON (l.startTime)
CREATE INDEX lifelog_starred FOR (l:Lifelog) ON (l.isStarred)
CREATE INDEX person_id FOR (p:Person) ON (p.id)
CREATE INDEX person_name FOR (p:Person) ON (p.name)
CREATE INDEX topic_id FOR (t:Topic) ON (t.id)
CREATE INDEX topic_name FOR (t:Topic) ON (t.name)
CREATE INDEX topic_category FOR (t:Topic) ON (t.category)
CREATE INDEX action_id FOR (a:Action) ON (a.id)
CREATE INDEX action_status FOR (a:Action) ON (a.status)
CREATE INDEX timewindow_id FOR (tw:TimeWindow) ON (tw.id)
CREATE INDEX timewindow_type FOR (tw:TimeWindow) ON (tw.type)
CREATE INDEX chat_id FOR (c:Chat) ON (c.id)
CREATE INDEX session_id FOR (s:Session) ON (s.id)
CREATE INDEX concept_id FOR (c:Concept) ON (c.id)
```

### Full-Text Indexes
```cypher
CALL db.idx.fulltext.createNodeIndex('lifelog_search', 'Lifelog', 'title', 'markdown')
CALL db.idx.fulltext.createNodeIndex('topic_search', 'Topic', 'name')
CALL db.idx.fulltext.createNodeIndex('person_search', 'Person', 'name')
CALL db.idx.fulltext.createNodeIndex('action_search', 'Action', 'action', 'context')
CALL db.idx.fulltext.createNodeIndex('concept_search', 'Concept', 'name', 'description')
CALL db.idx.fulltext.createNodeIndex('chat_search', 'Chat', 'title')
```

## Common Queries

### Find Lifelogs by Person
```cypher
MATCH (l:Lifelog)-[:MENTIONS]->(p:Person {name: $name})
RETURN l ORDER BY l.startTime DESC LIMIT 10
```

### Find Lifelogs by Topic
```cypher
MATCH (l:Lifelog)-[:HAS_TOPIC]->(t:Topic {name: $topic})
RETURN l ORDER BY l.startTime DESC LIMIT 10
```

### Find Co-occurring People
```cypher
MATCH (p1:Person)-[:SPOKE_IN]->(l:Lifelog)<-[:SPOKE_IN]-(p2:Person)
WHERE p1.name < p2.name
RETURN p1.name, p2.name, count(l) as co_occurrences
ORDER BY co_occurrences DESC
```

### Full-Text Search
```cypher
CALL db.idx.fulltext.queryNodes('lifelog_search', $query)
YIELD node, score
RETURN node as l ORDER BY score DESC LIMIT 10
```

## Repository Methods

| Repository | Key Methods |
|------------|-------------|
| LifelogRepository | upsert, findById, findByDateRange, findByPerson, search |
| PersonRepository | upsert, findByName, findTopMentioned, findCoOccurring |
| TopicRepository | upsert, findByName, findByCategory, findRelated |
| ActionRepository | upsert, findPending, findByAssignee |
| TimeWindowRepository | upsert, findByType, getStats |
| ChatRepository | upsert, findById, findRecent |
