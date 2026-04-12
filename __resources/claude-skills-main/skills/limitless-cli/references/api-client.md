# Limitless API Client Reference

## Rate Limiting

| Parameter | Value |
|-----------|-------|
| Requests per minute | 180 |
| Token refill rate | 3 per second |
| Burst capacity | 180 tokens |
| Retry strategy | Exponential backoff with jitter |

### Retry Configuration

```typescript
const RETRY_CONFIG = {
  maxRetries: 3,
  baseDelay: 1000,      // 1 second
  maxDelay: 8000,       // 8 seconds
  jitter: 0.2,          // 20% jitter
};
```

## Endpoints

### Lifelogs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/lifelogs` | GET | List/search lifelogs |
| `/v1/lifelogs/{id}` | GET | Get specific lifelog |
| `/v1/lifelogs/{id}` | DELETE | Delete lifelog |

### Chats

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/chats` | GET | List AI chats |
| `/v1/chats/{id}` | GET | Get specific chat |
| `/v1/chats/{id}` | DELETE | Delete chat |

### Audio

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/download-audio` | GET | Download audio (max 2hr) |

## Query Parameters

### List Lifelogs

```typescript
interface ListLifelogsParams {
  limit?: number;        // Max 100, default 10
  cursor?: string;       // Pagination cursor
  direction?: 'asc' | 'desc';
  date?: string;         // YYYY-MM-DD
  starred?: boolean;
  includeMarkdown?: boolean;
  includeHeadings?: boolean;
}
```

### Get Lifelog

```typescript
interface GetLifelogParams {
  includeMarkdown?: boolean;
  includeHeadings?: boolean;
}
```

## Response Types

### Lifelog

```typescript
interface Lifelog {
  id: string;
  title?: string;
  startTime: string;     // ISO-8601
  endTime: string;       // ISO-8601
  isStarred: boolean;
  markdown?: string;
  contents?: LifelogContent[];
}
```

### Chat

```typescript
interface Chat {
  id: string;
  title?: string;
  createdAt: string;
  updatedAt: string;
  messages: ChatMessage[];
}
```

## Error Handling

| Status | Error | Action |
|--------|-------|--------|
| 401 | Unauthorized | Check LIMITLESS_API_KEY |
| 429 | Rate Limited | Wait for retry-after header |
| 500 | Server Error | Retry with backoff |

## Usage Examples

```typescript
import { LimitlessApiClient } from './src/api/client.ts';

const client = new LimitlessApiClient();

// List recent lifelogs
const { data, meta } = await client.listLifelogs({ limit: 10 });

// Search with date filter
const results = await client.listLifelogs({
  date: '2026-01-04',
  includeMarkdown: true,
});

// Get specific lifelog
const lifelog = await client.getLifelog('abc123');
```
