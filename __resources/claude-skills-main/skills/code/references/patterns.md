# Implementation Patterns

Patterns for TODO management, type documentation, and code-based planning.

## TODO-Based Planning

### Category System

```python
# Standard TODO categories

# Basic task (no urgency)
# TODO(feature-id): Description

# Required for merge (blocks CI)
# TODO(feature-id,required): Description

# Blocked by dependency
# TODO(feature-id,blocked:other-feature): Description

# Technical debt (prioritize later)
# TODO(tech-debt): Description

# Security-related (high priority)
# TODO(security): Description

# Known bug requiring fix
# FIXME: Description

# Temporary solution needing proper implementation
# HACK: Description
```

### TODO Anatomy

```python
# TODO(id,flags): Brief title
# Context: Why this is needed
# Approach: How to implement
# Acceptance: Definition of done
# Estimate: Optional time estimate

# Example:
# TODO(auth-1,required): Implement password hashing
# Context: Security requirement SR-101 mandates no plaintext storage
# Approach: bcrypt with cost factor 12, store hash only
# Acceptance: All passwords hashed, verify hash function works
# Estimate: 2 hours
```

### Lifecycle Management

```
┌─────────────────────────────────────────────────────────────────┐
│                      TODO LIFECYCLE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PLAN ──────────► DEVELOP ──────────► VERIFY ──────────► DONE  │
│    │                  │                  │                      │
│    │ Write TODOs      │ Implement        │ Check remaining      │
│    │ at locations     │ Remove when      │ Block if required    │
│    │                  │ complete         │ remain               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Feature Planning Template

```python
# src/features/user-auth/login.py

"""
User Authentication Module

Implementation tracked via TODOs.
Feature complete when: grep "TODO(auth" returns 0
"""

# ============================================
# IMPLEMENTATION PLAN
# ============================================

# TODO(auth-1,required): Implement password hashing
# Context: Security requirement SR-101
# Approach: bcrypt with cost factor 12
# Acceptance: Hash stored, plaintext never persisted

# TODO(auth-2,required): Add rate limiting
# Context: Prevent brute force (SR-102)
# Approach: Redis sliding window, 5/min
# Acceptance: 429 returned after 5 attempts

# TODO(auth-3,required): Implement session management
# Context: User sessions per UX-203
# Approach: JWT (1hr) + refresh token (7d)
# Acceptance: Tokens issued, validated, refreshed

# TODO(auth-4): Add audit logging
# Context: Compliance requirement COMP-15
# Approach: Structured logs to audit sink
# Acceptance: All auth events logged

# ============================================
# IMPLEMENTATION
# ============================================

async def login(credentials: LoginCredentials) -> AuthResult:
    """Authenticate user and create session."""
    # Implementation goes here
    # TODOs removed as each is completed
    pass
```

### Progress Tracking

```bash
# Check feature progress
grep -rn "TODO(auth" src/ | wc -l
# Result: 4 TODOs remaining

# Check required TODOs (blocks merge)
grep -rn "TODO(.*,required" src/
# If any results, cannot merge

# Generate progress report
python scripts/todo-lint.py --report
# Output:
# Feature: auth
#   Total: 4
#   Required: 3
#   Completed: 0
#   Status: IN_PROGRESS
```

---

## Type Documentation Patterns

### Pattern 1: Types as API Documentation

```typescript
/**
 * User entity representing an authenticated account.
 * 
 * @remarks
 * Created via POST /users, retrieved via GET /users/:id
 */
interface User {
    /** Unique identifier (UUID v4) */
    id: string;
    
    /** Display name (1-100 chars) */
    name: string;
    
    /** Unique email address */
    email: string;
    
    /** Permission level */
    role: 'admin' | 'user' | 'guest';
    
    /** ISO 8601 creation timestamp */
    createdAt: string;
}

// Type + JSDoc = Complete API documentation
// If it compiles, docs are current
```

### Pattern 2: Branded Types for Domain Concepts

```typescript
// Branded types prevent mixing incompatible IDs

type UserId = string & { readonly brand: unique symbol };
type OrderId = string & { readonly brand: unique symbol };
type ProductId = string & { readonly brand: unique symbol };

// Compiler prevents:
// getUser(orderId)  // Error: OrderId not assignable to UserId

function createUserId(id: string): UserId {
    return id as UserId;
}

// Type system documents: "These IDs are not interchangeable"
```

### Pattern 3: Discriminated Unions for States

```typescript
// State machine documented via types

type AuthState = 
    | { status: 'unauthenticated' }
    | { status: 'authenticating'; email: string }
    | { status: 'authenticated'; user: User; token: string }
    | { status: 'error'; message: string };

// Type documents all possible states
// Compiler enforces exhaustive handling:

function handleAuth(state: AuthState): void {
    switch (state.status) {
        case 'unauthenticated':
            showLoginForm();
            break;
        case 'authenticating':
            showSpinner();
            break;
        case 'authenticated':
            showDashboard(state.user);
            break;
        case 'error':
            showError(state.message);
            break;
        // TypeScript ensures all cases handled
    }
}
```

### Pattern 4: Result Types for Error Handling

```typescript
// Errors documented in return type

type Result<T, E> = 
    | { success: true; value: T }
    | { success: false; error: E };

type CreateUserError = 
    | { code: 'EMAIL_EXISTS'; email: string }
    | { code: 'INVALID_EMAIL'; reason: string }
    | { code: 'NAME_TOO_LONG'; maxLength: number };

async function createUser(
    request: CreateUserRequest
): Promise<Result<User, CreateUserError>> {
    // Return type documents all possible errors
    // Caller must handle each case
}
```

### Pattern 5: Validation as Documentation

```python
# Pydantic model documents validation rules

from pydantic import BaseModel, Field, validator
from typing import Literal

class CreateUserRequest(BaseModel):
    """
    User creation request.
    
    Validation rules documented via Field() and validators.
    """
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User's display name"
    )
    
    email: str = Field(
        ...,
        regex=r'^[\w\.-]+@[\w\.-]+\.\w+$',
        description="Valid email address"
    )
    
    role: Literal['admin', 'user', 'guest'] = Field(
        default='user',
        description="Permission level"
    )
    
    @validator('name')
    def name_not_empty(cls, v):
        """Names cannot be only whitespace."""
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

# Model IS the validation documentation
# If request validates, it meets all requirements
```

---

## Diagram Generation Patterns

### Pattern 1: Dependency Graph from Imports

```bash
# Generate dependency graph
npx madge --image docs/deps.svg src/

# Options:
# --circular: Highlight circular dependencies
# --orphans: Show files with no dependencies
# --exclude: Pattern to exclude

# Example output: SVG showing import relationships
# Always current because derived from actual imports
```

### Pattern 2: Type Relationship Diagram

```bash
# Generate TypeScript type relationships
npx ts-diagram src/ > docs/types.mmd

# Or use tsviz:
npx tsviz src/ -o docs/types.png
```

### Pattern 3: Database Schema from Migrations

```bash
# PostgreSQL schema diagram
pg_dump --schema-only mydb | sqlt-graph -t postgres > docs/schema.svg

# Or use SchemaSpy:
java -jar schemaspy.jar -t pgsql -db mydb -o docs/schema
```

### Pattern 4: API Diagram from OpenAPI

```bash
# Generate from OpenAPI spec
npx @openapitools/openapi-generator-cli generate \
    -g plantuml \
    -i openapi.yaml \
    -o docs/api-diagram
```

### Pattern 5: Architecture from Container Structure

```python
# scripts/generate-architecture.py

import os
from pathlib import Path

def generate_mermaid_from_structure(root: Path) -> str:
    """Generate Mermaid diagram from directory structure."""
    
    lines = ["graph TD"]
    
    for service_dir in root.glob("services/*/"):
        service_name = service_dir.name
        
        # Check for dependencies
        deps_file = service_dir / "dependencies.txt"
        if deps_file.exists():
            for dep in deps_file.read_text().splitlines():
                lines.append(f"    {service_name} --> {dep}")
    
    return "\n".join(lines)

# Output is always current because derived from structure
```

---

## Linter Configuration as Style Guide

### ESLint as JavaScript Style Guide

```javascript
// .eslintrc.js IS the style documentation

module.exports = {
    rules: {
        // === NAMING ===
        // "Variables use camelCase"
        'camelcase': ['error', { properties: 'always' }],
        
        // === FUNCTIONS ===
        // "Functions must have explicit return types"
        '@typescript-eslint/explicit-function-return-type': 'error',
        
        // "Maximum function length: 50 lines"
        'max-lines-per-function': ['error', { max: 50 }],
        
        // === CODE QUALITY ===
        // "No console.log in production"
        'no-console': 'error',
        
        // "No unused variables"
        '@typescript-eslint/no-unused-vars': 'error',
        
        // === COMPLEXITY ===
        // "Maximum cyclomatic complexity: 10"
        'complexity': ['error', { max: 10 }],
    }
};

// If linting passes, code follows style guide
// No separate style document needed
```

### Ruff as Python Style Guide

```toml
# pyproject.toml IS the Python style documentation

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]  # Allow assert in tests

# If ruff passes, code follows style
```

---

## Schema as Business Rules Documentation

### JSON Schema for Configuration

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Application Configuration",
    "description": "Configuration schema IS the config documentation",
    "type": "object",
    "required": ["database", "server"],
    "properties": {
        "database": {
            "type": "object",
            "properties": {
                "host": {
                    "type": "string",
                    "description": "Database hostname",
                    "default": "localhost"
                },
                "port": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 65535,
                    "default": 5432
                },
                "poolSize": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "default": 10,
                    "description": "Connection pool size"
                }
            }
        },
        "server": {
            "type": "object",
            "properties": {
                "port": {
                    "type": "integer",
                    "default": 3000
                },
                "timeout": {
                    "type": "integer",
                    "minimum": 1000,
                    "maximum": 60000,
                    "default": 30000,
                    "description": "Request timeout in milliseconds"
                }
            }
        }
    }
}
```

### Zod for Runtime Validation

```typescript
// Schema IS the documentation

import { z } from 'zod';

export const UserSchema = z.object({
    id: z.string().uuid(),
    name: z.string().min(1).max(100),
    email: z.string().email(),
    role: z.enum(['admin', 'user', 'guest']).default('user'),
    createdAt: z.string().datetime(),
});

export type User = z.infer<typeof UserSchema>;

// Schema documents:
// - Required fields
// - Field types
// - Validation rules
// - Default values
// If it validates, documentation is correct
```

---

## Migration as History Documentation

### Database Migration Pattern

```python
# migrations/001_create_users.py

"""
Create users table.

Documents:
- Table structure
- Column types and constraints
- Indexes
- Relationships
"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('role', sa.Enum('admin', 'user', 'guest'), default='user'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now()),
    )
    
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_table('users')

# Migration history IS the database documentation
# If migrations run, schema docs are current
```

### Migration as Change Log

```
migrations/
├── 001_create_users.py           # Users table created
├── 002_add_user_settings.py      # Settings column added
├── 003_create_orders.py          # Orders table created
├── 004_add_user_avatar.py        # Avatar URL added
└── 005_add_soft_delete.py        # deleted_at column added

# Directory listing IS the change history
# Each migration documents what changed and when
```
