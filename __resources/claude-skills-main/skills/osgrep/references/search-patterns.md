# Common Semantic Query Patterns

## Architecture Patterns

### Entry Points
```bash
osgrep "application entry point main function"
osgrep "server initialization bootstrap"
osgrep "main application setup"
```

### Configuration
```bash
osgrep "configuration loading environment variables"
osgrep "settings management from config files"
osgrep "application configuration setup"
```

### Dependency Injection
```bash
osgrep "dependency injection container setup"
osgrep "service provider registration"
osgrep "inversion of control configuration"
```

### Routing
```bash
osgrep "route definition and registration"
osgrep "URL routing configuration"
osgrep "API endpoint mapping"
```

## Authentication Patterns

### User Authentication
```bash
osgrep "user authentication with password verification"
osgrep "login credential validation"
osgrep "user identity verification"
```

### Token-Based Auth
```bash
osgrep "JWT token generation and signing"
osgrep "access token validation"
osgrep "refresh token rotation"
osgrep "bearer token authentication"
```

### Session Management
```bash
osgrep "session creation and storage"
osgrep "session cookie management"
osgrep "session expiration and cleanup"
```

### OAuth / Social Login
```bash
osgrep "OAuth2 authorization flow"
osgrep "social login integration"
osgrep "third-party authentication provider"
```

### Password Security
```bash
osgrep "password hashing with bcrypt"
osgrep "password strength validation"
osgrep "secure password storage"
```

## Database Patterns

### Connection Management
```bash
osgrep "database connection pool configuration"
osgrep "database connection establishment"
osgrep "connection retry with backoff"
```

### Query Execution
```bash
osgrep "parameterized SQL query execution"
osgrep "prepared statement with placeholders"
osgrep "ORM query builder usage"
```

### Transactions
```bash
osgrep "database transaction management"
osgrep "atomic operation with rollback"
osgrep "transaction commit and error handling"
```

### Migrations
```bash
osgrep "database schema migration"
osgrep "table creation and modification"
osgrep "migration rollback strategy"
```

### Models / Schemas
```bash
osgrep "database model definition"
osgrep "entity schema with relationships"
osgrep "data model with validation"
```

## API Patterns

### Endpoint Handlers
```bash
osgrep "REST API endpoint handler"
osgrep "HTTP request handler function"
osgrep "controller action method"
```

### Request Validation
```bash
osgrep "request body validation"
osgrep "input parameter validation"
osgrep "schema validation with zod"
```

### Response Formatting
```bash
osgrep "JSON response formatting"
osgrep "API response structure"
osgrep "error response with status code"
```

### Middleware
```bash
osgrep "authentication middleware"
osgrep "logging middleware"
osgrep "rate limiting middleware"
osgrep "CORS configuration middleware"
```

### Error Handling
```bash
osgrep "API error handler middleware"
osgrep "exception catching and formatting"
osgrep "error response serialization"
```

## Error Handling Patterns

### Try-Catch
```bash
osgrep "try catch error handling"
osgrep "exception handling with recovery"
osgrep "error catching and logging"
```

### Custom Errors
```bash
osgrep "custom error class definition"
osgrep "application-specific exception"
osgrep "error with custom properties"
```

### Error Recovery
```bash
osgrep "error recovery with fallback"
osgrep "graceful degradation on failure"
osgrep "retry logic with exponential backoff"
```

### Logging
```bash
osgrep "error logging with context"
osgrep "structured logging for errors"
osgrep "error tracking and monitoring"
```

## Async Patterns

### Promises
```bash
osgrep "promise chain with error handling"
osgrep "async operation with promise"
osgrep "promise all parallel execution"
```

### Async/Await
```bash
osgrep "async await pattern"
osgrep "asynchronous function with await"
osgrep "async error handling"
```

### Callbacks
```bash
osgrep "callback function pattern"
osgrep "error-first callback"
osgrep "callback hell refactoring"
```

### Event Handling
```bash
osgrep "event emitter pattern"
osgrep "event listener registration"
osgrep "asynchronous event handling"
```

## Validation Patterns

### Input Validation
```bash
osgrep "user input validation"
osgrep "form data validation"
osgrep "request parameter validation"
```

### Schema Validation
```bash
osgrep "schema validation with zod"
osgrep "JSON schema validation"
osgrep "type checking at runtime"
```

### Business Rules
```bash
osgrep "business rule validation"
osgrep "domain-specific validation logic"
osgrep "constraint checking"
```

### Sanitization
```bash
osgrep "input sanitization against XSS"
osgrep "data cleaning and normalization"
osgrep "HTML escaping for security"
```

## Testing Patterns

### Unit Tests
```bash
osgrep "unit test for function"
osgrep "test case with assertions"
osgrep "mock dependency in test"
```

### Integration Tests
```bash
osgrep "integration test setup"
osgrep "API endpoint testing"
osgrep "database integration test"
```

### Mocking
```bash
osgrep "mock external dependency"
osgrep "stub function for testing"
osgrep "mock API response"
```

### Test Fixtures
```bash
osgrep "test fixture setup"
osgrep "test data preparation"
osgrep "before each test setup"
```

## Performance Patterns

### Caching
```bash
osgrep "caching strategy with TTL"
osgrep "cache invalidation logic"
osgrep "Redis caching implementation"
osgrep "in-memory cache setup"
```

### Rate Limiting
```bash
osgrep "rate limiting with token bucket"
osgrep "API rate limiter middleware"
osgrep "throttling request handling"
```

### Batch Processing
```bash
osgrep "batch processing of records"
osgrep "bulk operation optimization"
osgrep "chunked data processing"
```

### Pagination
```bash
osgrep "cursor-based pagination"
osgrep "offset limit pagination"
osgrep "infinite scroll implementation"
```

### Lazy Loading
```bash
osgrep "lazy loading pattern"
osgrep "deferred initialization"
osgrep "on-demand data fetching"
```

## Security Patterns

### SQL Injection
```bash
osgrep "SQL injection prevention"
osgrep "parameterized query for security"
osgrep "safe database query execution"
```

### XSS Protection
```bash
osgrep "XSS prevention with sanitization"
osgrep "HTML escaping for security"
osgrep "content security policy"
```

### CSRF Protection
```bash
osgrep "CSRF token validation"
osgrep "cross-site request forgery prevention"
osgrep "same-site cookie attribute"
```

### Secrets Management
```bash
osgrep "environment variable for secrets"
osgrep "secure credential storage"
osgrep "API key management"
```

### Authorization
```bash
osgrep "role-based access control"
osgrep "permission checking logic"
osgrep "access control middleware"
```

## File Operations

### Reading
```bash
osgrep "file reading with streaming"
osgrep "asynchronous file read"
osgrep "parse file content"
```

### Writing
```bash
osgrep "file writing with buffering"
osgrep "atomic file write operation"
osgrep "create file with permissions"
```

### Upload
```bash
osgrep "file upload handling"
osgrep "multipart form data parsing"
osgrep "file size validation"
```

### Storage
```bash
osgrep "cloud storage upload"
osgrep "S3 file storage integration"
osgrep "blob storage management"
```

## State Management

### React State
```bash
osgrep "React state management with hooks"
osgrep "useState and useEffect pattern"
osgrep "global state with context"
```

### Redux
```bash
osgrep "Redux store configuration"
osgrep "action creator and reducer"
osgrep "Redux middleware setup"
```

### MobX
```bash
osgrep "MobX observable state"
osgrep "computed value derivation"
osgrep "action for state mutation"
```

### Zustand
```bash
osgrep "Zustand store creation"
osgrep "state selector pattern"
osgrep "store with persistence"
```

## Component Patterns (React)

### Component Definition
```bash
osgrep "React functional component"
osgrep "component with props and state"
osgrep "TypeScript component interface"
```

### Hooks
```bash
osgrep "custom React hook"
osgrep "useEffect hook with cleanup"
osgrep "useMemo for optimization"
```

### Context
```bash
osgrep "React context provider"
osgrep "context consumer pattern"
osgrep "theme context implementation"
```

### Forms
```bash
osgrep "form handling with validation"
osgrep "controlled input component"
osgrep "form submission with async"
```

## Data Fetching

### HTTP Requests
```bash
osgrep "HTTP GET request with fetch"
osgrep "POST request with JSON body"
osgrep "HTTP request with error handling"
```

### GraphQL
```bash
osgrep "GraphQL query execution"
osgrep "mutation with variables"
osgrep "GraphQL client setup"
```

### WebSockets
```bash
osgrep "WebSocket connection setup"
osgrep "real-time data streaming"
osgrep "WebSocket message handling"
```

### Server-Sent Events
```bash
osgrep "SSE event stream"
osgrep "server-sent events handler"
osgrep "real-time updates with SSE"
```

## Deployment Patterns

### Docker
```bash
osgrep "Dockerfile configuration"
osgrep "Docker compose setup"
osgrep "container orchestration"
```

### CI/CD
```bash
osgrep "continuous integration pipeline"
osgrep "automated deployment script"
osgrep "build and test workflow"
```

### Environment
```bash
osgrep "environment-specific configuration"
osgrep "staging and production setup"
osgrep "environment variable loading"
```

### Health Checks
```bash
osgrep "health check endpoint"
osgrep "readiness probe"
osgrep "liveness check implementation"
```

## Logging Patterns

### Structured Logging
```bash
osgrep "structured logging with context"
osgrep "JSON log formatting"
osgrep "log level configuration"
```

### Request Logging
```bash
osgrep "HTTP request logging middleware"
osgrep "request duration tracking"
osgrep "access log formatting"
```

### Error Logging
```bash
osgrep "error logging with stack trace"
osgrep "exception tracking"
osgrep "error aggregation service"
```

## Message Queue Patterns

### Queue Management
```bash
osgrep "message queue producer"
osgrep "job queue consumer"
osgrep "queue retry mechanism"
```

### Event-Driven
```bash
osgrep "event publishing pattern"
osgrep "event subscriber handler"
osgrep "asynchronous event processing"
```

### Worker Jobs
```bash
osgrep "background job processing"
osgrep "scheduled task execution"
osgrep "worker queue management"
```

## Tips for Crafting Effective Queries

### 1. Be Specific About Intent
```bash
# Vague
osgrep "user"

# Specific
osgrep "user registration with email verification"
```

### 2. Include Domain Context
```bash
# Generic
osgrep "validation"

# Context-rich
osgrep "credit card validation with Luhn algorithm"
```

### 3. Combine Related Concepts
```bash
# Single concept
osgrep "authentication"

# Compound concept
osgrep "JWT authentication with refresh token rotation"
```

### 4. Use Action Verbs
```bash
# Noun-only
osgrep "database connection"

# Verb + noun
osgrep "establishing database connection with retry"
```

### 5. Add Technical Details
```bash
# General
osgrep "caching"

# Technical
osgrep "Redis caching with TTL expiration and invalidation"
```

### 6. Specify Error Scenarios
```bash
# General
osgrep "error handling"

# Specific scenario
osgrep "network timeout error handling with retry"
```

### 7. Reference Frameworks/Libraries
```bash
# Generic
osgrep "state management"

# Framework-specific
osgrep "Redux state management with toolkit"
```

## Cross-Language Queries

These queries work across multiple languages:

```bash
# Authentication (works in JS, Python, Go, Rust, etc.)
osgrep "password hashing with bcrypt"

# Database (works in any language with DB access)
osgrep "connection pooling configuration"

# Error handling (universal pattern)
osgrep "retry with exponential backoff"

# Caching (works across languages)
osgrep "cache invalidation strategy"

# Testing (universal concept)
osgrep "mock external API calls"
```

## Anti-Patterns to Avoid

### Don't Use Exact Tokens
```bash
# Bad (use grep instead)
osgrep "getUserById"
osgrep "import { useState }"
osgrep "class UserService"

# Good (conceptual)
osgrep "function to fetch user by identifier"
osgrep "React state management hook"
osgrep "user service class implementation"
```

### Don't Be Too Vague
```bash
# Too vague
osgrep "code"
osgrep "function"
osgrep "test"

# Better
osgrep "business logic implementation"
osgrep "API endpoint handler function"
osgrep "unit test with mock dependencies"
```

### Don't Use Regex Syntax
```bash
# Won't work (osgrep isn't regex-based)
osgrep "user_\d+"
osgrep "get.*Handler"

# Use conceptual description instead
osgrep "user identifier with numeric suffix"
osgrep "HTTP GET request handler"
```
