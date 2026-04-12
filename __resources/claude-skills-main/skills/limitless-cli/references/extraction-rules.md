# Extraction Rules Reference

## Rule-Based Extraction

### Speaker Extraction
Extracts speakers from lifelog contents based on `speakerName` field.

```typescript
interface ExtractedPerson {
  name: string;
  identifier: 'user' | 'known' | 'unknown';
  mentions: number;
  speakingTime?: number;
  firstMention: number;
  contexts: string[];
}
```

### Date Reference Extraction
Detects temporal references in text.

```typescript
const DATE_PATTERNS = [
  /\b(today|tomorrow|yesterday)\b/gi,
  /\b(next|last)\s+(week|month|year|monday|tuesday|...)\b/gi,
  /\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b/g,
  /\b(january|february|...)\s+\d{1,2}(st|nd|rd|th)?\b/gi,
];
```

### Action Pattern Extraction
Detects action items, todos, and commitments.

```typescript
const ACTION_PATTERNS = [
  { pattern: /\b(need to|should|must|have to)\s+(.+)/gi, type: 'todo' },
  { pattern: /\b(will|going to|planning to)\s+(.+)/gi, type: 'commitment' },
  { pattern: /\b(follow up|remind me|don't forget)\s+(.+)/gi, type: 'followup' },
  { pattern: /\?$/m, type: 'question' },
];
```

### Entity Mention Extraction
Detects people, organizations, products, and locations.

```typescript
const MENTION_PATTERNS = [
  // Person names (capitalized words)
  { pattern: /\b[A-Z][a-z]+\s+[A-Z][a-z]+\b/g, type: 'person' },
  // Organizations (common suffixes)
  { pattern: /\b[A-Z][\w]+\s+(Inc|Corp|Ltd|LLC|Co)\b/g, type: 'organization' },
  // Products (with trademark indicators)
  { pattern: /\b[A-Z][\w]+(?:®|™)?\b/g, type: 'product' },
];
```

## Domain-Specific Patterns

### Medical/Pharmacology
```typescript
const MEDICAL_PATTERNS = [
  // 5HT3 antagonists
  { pattern: /ondansetron/gi, category: '5HT3 antagonist' },
  { pattern: /granisetron/gi, category: '5HT3 antagonist' },
  { pattern: /palonosetron/gi, category: '5HT3 antagonist' },

  // Dopamine antagonists
  { pattern: /droperidol/gi, category: 'Dopamine antagonist' },
  { pattern: /metoclopramide/gi, category: 'Dopamine antagonist' },
  { pattern: /prochlorperazine/gi, category: 'Dopamine antagonist' },

  // Antihistamines
  { pattern: /cyclizine/gi, category: 'Antihistamine (H1)' },
  { pattern: /promethazine/gi, category: 'Antihistamine (H1)' },

  // Corticosteroids
  { pattern: /dexamethasone/gi, category: 'Corticosteroid' },

  // NK1 antagonists
  { pattern: /aprepitant/gi, category: 'NK1 antagonist' },
];
```

### Clinical Concepts
```typescript
const CLINICAL_CONCEPTS = [
  { keywords: ['mechanism', 'receptor', 'agonist', 'antagonist'], concept: 'Mechanism of action' },
  { keywords: ['adverse', 'side effect', 'toxicity'], concept: 'Side effects' },
  { keywords: ['indication', 'treatment', 'prophylaxis'], concept: 'Clinical application' },
  { keywords: ['ponv', 'postoperative', 'nausea'], concept: 'PONV management' },
];
```

## LLM-Based Extraction

### Topic Extraction Prompt
```typescript
const TOPIC_EXTRACTION_PROMPT = `
Extract the main topics discussed in this text.
For each topic, provide:
- name: The topic name (2-4 words)
- confidence: 0.0-1.0 based on how prominently it's discussed
- category: work, personal, technical, medical, or other
- keywords: 3-5 related keywords
`;
```

### Action Extraction Prompt
```typescript
const ACTION_EXTRACTION_PROMPT = `
Extract action items from this text.
For each action, provide:
- description: What needs to be done
- assignee: Who should do it (if mentioned)
- dueDate: When it's due (if mentioned)
- priority: high, medium, or low
- status: pending, in_progress, or completed
`;
```

## Hierarchical Extraction

### Session Detection
Groups lifelogs into sessions based on time gaps.

```typescript
const SESSION_GAP_MINUTES = 30;

function detectSessions(lifelogs: Lifelog[]): Session[] {
  // Sort by start time
  // Group consecutive lifelogs within 30-minute gaps
  // Return session boundaries
}
```

### Day-Level Aggregation
```typescript
interface ExtractedDay {
  date: string;
  sessions: ExtractedSession[];
  totalDuration: number;
  topics: ExtractedTopic[];
  people: ExtractedPerson[];
  actions: ExtractedAction[];
  summary?: string;
}
```

## Extraction Pipeline

```
Lifelog Content
    ↓
Rule-Based Extraction (fast, deterministic)
    ├── Speakers
    ├── Date References
    ├── Action Patterns
    └── Entity Mentions
    ↓
LLM Extraction (optional, semantic)
    ├── Topics with confidence
    ├── Actions with context
    └── Relationships
    ↓
Merge & Deduplicate
    ↓
Graph Sync (FalkorDB)
```

## Configuration

```typescript
interface ExtractionConfig {
  enableRules: boolean;           // Default: true
  enableLLM: boolean;             // Default: true (if API key)
  llmModel: 'haiku' | 'sonnet';   // Default: 'sonnet'
  sessionGapMinutes: number;      // Default: 30
  topicConfidenceThreshold: number;   // Default: 0.5
  actionConfidenceThreshold: number;  // Default: 0.6
}
```
