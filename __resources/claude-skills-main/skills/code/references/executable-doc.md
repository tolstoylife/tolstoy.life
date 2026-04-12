# Executable Documentation System

Complete specification of the documentation tier hierarchy and conversion methodology.

## Core Thesis

```yaml
axiom: "Documentation that can drift, will drift, and will harm."
corollary: "The only trustworthy documentation is documentation that executes."
```

**The Drift Problem:**
```
TIME_0: Code implements X, Doc describes X     → ALIGNED
TIME_1: Code changes to Y, Doc still says X   → DRIFT
TIME_2: Developer reads Doc, expects X        → BUG
TIME_3: AI reads Doc, generates X-compatible  → COMPOUNDED BUG
```

## Tier Hierarchy

### Tier 1: Type Signatures (Trust: 0.95)

**Verification:** Compiler
**Drift Risk:** Zero

```typescript
// Type IS the documentation
interface UserResponse {
    id: string;
    name: string;
    email: string;
    createdAt: Date;
}

// If this compiles, the documentation is correct
async function getUser(id: string): Promise<UserResponse | null> {
    // Implementation
}
```

**Conversion Pattern:**
```
BEFORE (external doc):
  "The getUser function takes a user ID and returns user data 
   including name, email, and creation date"

AFTER (type as doc):
  function getUser(id: UserId): Promise<User | null>
  
  // Type definition IS the documentation
```

### Tier 2: Schema Definitions (Trust: 0.95)

**Verification:** Schema validator
**Drift Risk:** Zero

```python
# Pydantic schema IS the API documentation
class CreateUserRequest(BaseModel):
    """User creation payload. Schema validates = docs current."""
    
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    role: Literal["admin", "user", "guest"] = "user"
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "role": "user"
            }
        }
```

**JSON Schema:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["name", "email"],
  "properties": {
    "name": { "type": "string", "minLength": 1, "maxLength": 100 },
    "email": { "type": "string", "format": "email" },
    "role": { "enum": ["admin", "user", "guest"], "default": "user" }
  }
}
```

### Tier 3: API Specifications (Trust: 0.95)

**Verification:** Generator
**Drift Risk:** Zero if generated from code

```python
# FastAPI generates OpenAPI from code
@app.post("/users", response_model=UserResponse)
async def create_user(request: CreateUserRequest) -> UserResponse:
    """
    Create a new user.
    
    - **name**: User's display name
    - **email**: Unique email address
    - **role**: Permission level (default: user)
    """
    pass

# OpenAPI spec generated automatically
# Documentation = code annotations + types
```

**Generation Command:**
```bash
# Generate OpenAPI from code annotations
npm run generate:openapi

# If generation succeeds, API docs are current
```

### Tier 4: Database Migrations (Trust: 0.95)

**Verification:** Migration runner
**Drift Risk:** Zero

```python
# Alembic migration IS the schema documentation
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('role', sa.Enum('admin', 'user', 'guest'), default='user'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

# Migration history IS the database documentation
# If migrations run, schema docs are current
```

### Tier 5: Linter Rules (Trust: 0.90)

**Verification:** Linter
**Drift Risk:** Zero

```javascript
// .eslintrc.js IS the style guide
module.exports = {
  rules: {
    // "Functions must have explicit return types"
    '@typescript-eslint/explicit-function-return-type': 'error',
    
    // "No console.log in production code"
    'no-console': 'error',
    
    // "Max function length: 50 lines"
    'max-lines-per-function': ['error', { max: 50 }],
  }
};

// If linting passes, style guide is followed
```

### Tier 6: Test Assertions (Trust: 0.70)

**Verification:** Test runner
**Drift Risk:** Low (but watch for tautology)

```python
# Tests document expected behavior
def test_user_creation():
    """Users can be created with valid data."""
    response = client.post("/users", json={
        "name": "Jane",
        "email": "jane@example.com"
    })
    
    assert response.status_code == 201
    assert response.json()["name"] == "Jane"
    assert "id" in response.json()

# WARNING: Tests can be tautological (see Law 3 caveat)
# Trust: 0.70 (not 0.95) because of tautology risk
```

**Tautology Detection:**
```python
# BAD: Test documents implementation, not requirement
def test_authenticate():
    # This test just verifies code does what code does
    assert authenticate("user", "pass") == True

# GOOD: Test documents requirement
def test_authenticate_with_valid_credentials():
    # Create actual user with known password
    user = create_user(password="secret123")
    
    # Verify actual authentication
    result = authenticate(user.email, "secret123")
    assert result.authenticated == True
    assert result.user_id == user.id
```

### Tier 7: TODOs in Code (Trust: 0.60)

**Verification:** Grep/lint
**Drift Risk:** Low

```python
# TODO(auth-1,required): Implement password hashing
# Context: Security requirement SR-101
# Acceptance: bcrypt cost factor 12

# TODO documents intent at implementation point
# Removed when implemented = no drift
```

### Tier 8: Inline Comments (Trust: 0.50)

**Verification:** Human review
**Drift Risk:** Medium (localized)

```python
# WHY comments are valuable (explain intent)
def calculate_tax(price: Decimal) -> Decimal:
    # Tax rate is 10% per 2024 tax code section 4.2.1
    # Updated annually in January
    return price * Decimal("0.10")

# WHAT comments are dangerous (can drift)
def process(data):
    # Sort the data  ← May not actually sort anymore
    return transform(data)
```

### Tier 9: External Documentation (Trust: 0.10)

**Verification:** None
**Drift Risk:** **Certain**

```
❌ README.md         → Will drift
❌ docs/api.md       → Will drift
❌ ARCHITECTURE.md   → Will drift
❌ Wiki pages        → Will drift
❌ Confluence        → Will drift
❌ IMPLEMENTATION.md → Already stale
```

**Never rely on Tier 9 for authoritative information.**

---

## Conversion Methodology

### Step 1: Identify Documentation Need

```python
def identify_need(requirement: str) -> DocNeed:
    """Classify what type of documentation is needed."""
    
    if describes_data_shape(requirement):
        return DocNeed.DATA_STRUCTURE
    
    if describes_api_contract(requirement):
        return DocNeed.API_CONTRACT
    
    if describes_behavior_rule(requirement):
        return DocNeed.BUSINESS_RULE
    
    if describes_style_convention(requirement):
        return DocNeed.STYLE_RULE
    
    if describes_future_work(requirement):
        return DocNeed.IMPLEMENTATION_PLAN
    
    return DocNeed.GENERAL_CONTEXT
```

### Step 2: Select Target Tier

```python
def select_tier(need: DocNeed) -> Tier:
    """Select highest-trust tier that can express the need."""
    
    tier_mapping = {
        DocNeed.DATA_STRUCTURE: Tier.T1_TYPES,
        DocNeed.API_CONTRACT: Tier.T3_API_SPEC,
        DocNeed.BUSINESS_RULE: Tier.T2_SCHEMA,  # or T5_LINTER
        DocNeed.STYLE_RULE: Tier.T5_LINTER,
        DocNeed.IMPLEMENTATION_PLAN: Tier.T7_TODO,
        DocNeed.GENERAL_CONTEXT: Tier.T8_COMMENT,
    }
    
    return tier_mapping.get(need, Tier.T8_COMMENT)
```

### Step 3: Convert to Code Form

**Data Structures → Types (T1):**
```
BEFORE: "User has name, email, and creation date"
AFTER:
  interface User {
    name: string;
    email: string;
    createdAt: Date;
  }
```

**API Contracts → Generated Specs (T3):**
```
BEFORE: "POST /users creates a user with name and email"
AFTER:
  @app.post("/users")
  async def create_user(name: str, email: EmailStr) -> User:
      pass
  # OpenAPI generated automatically
```

**Business Rules → Validation (T2/T5):**
```
BEFORE: "Email must be unique and valid format"
AFTER:
  class User(BaseModel):
      email: EmailStr = Field(..., unique=True)
```

**Style Rules → Linter Config (T5):**
```
BEFORE: "Functions should be less than 50 lines"
AFTER:
  // .eslintrc.js
  'max-lines-per-function': ['error', { max: 50 }]
```

**Implementation Plans → TODOs (T7):**
```
BEFORE: "PLAN.md: Implement auth with bcrypt, rate limiting, sessions"
AFTER:
  // TODO(auth-1): Implement bcrypt hashing
  // TODO(auth-2): Add rate limiting  
  // TODO(auth-3): Implement sessions
```

### Step 4: Verify Conversion

```python
def verify_conversion(original: ExternalDoc, converted: CodeDoc) -> bool:
    """Verify conversion preserved semantics."""
    
    # Check tier improvement
    assert converted.tier < original.tier  # Lower number = higher trust
    
    # Check executability
    assert converted.can_execute()
    
    # Check semantic preservation
    assert semantic_match(original.content, converted.content)
    
    return True
```

---

## Common Conversion Patterns

### Pattern 1: README → Generated + Types

```markdown
# BEFORE: README.md
## Installation
npm install my-package

## Usage
import { process } from 'my-package';
const result = process(data);
```

```typescript
// AFTER: Types + JSDoc (extracted to docs via typedoc)
/**
 * Process input data according to business rules.
 * @example
 * const result = process({ input: "data" });
 */
export function process(data: InputData): ProcessResult {
    // Implementation
}

// README now generated from code:
// npm run generate:docs
```

### Pattern 2: API Docs → OpenAPI Generation

```markdown
# BEFORE: docs/api.md
## POST /users
Creates a new user.
- name (string, required): User's name
- email (string, required): User's email
Returns: User object with id, name, email
```

```python
# AFTER: Code annotations → OpenAPI
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(request: CreateUserRequest) -> UserResponse:
    """
    Create a new user.
    
    Returns the created user with assigned ID.
    """
    pass

# API docs generated: npm run generate:openapi
```

### Pattern 3: Architecture Docs → Generated Diagrams

```markdown
# BEFORE: ARCHITECTURE.md
The system consists of:
- API Gateway
- User Service
- Database

API Gateway talks to User Service which talks to Database.
```

```bash
# AFTER: Generated from code
npx madge --image docs/architecture.svg src/

# Diagram always current because derived from imports
```

### Pattern 4: Implementation Plan → TODOs

```markdown
# BEFORE: IMPLEMENTATION_PLAN.md
## Phase 1: Authentication
1. Implement password hashing with bcrypt
2. Add rate limiting (5 attempts/minute)
3. Create session management with JWT
```

```python
# AFTER: TODOs at implementation points

# TODO(auth-1,required): Implement password hashing
# Approach: bcrypt with cost factor 12
# Acceptance: Hash stored, plaintext never persisted

# TODO(auth-2,required): Add rate limiting
# Approach: Redis sliding window
# Acceptance: 429 after 5 attempts/minute

# TODO(auth-3,required): Create session management
# Approach: JWT (1hr) + refresh (7d)
# Acceptance: Tokens issued and validated

async def login(credentials: LoginCredentials) -> AuthResult:
    pass
```

---

## Anti-Patterns

### Anti-Pattern 1: Commented-Out Documentation

```python
# BAD: External docs referenced in comments
# See docs/api.md for full specification  ← Will drift

# GOOD: Type IS the specification
def get_user(id: UserId) -> User | None:
    pass
```

### Anti-Pattern 2: Duplicate Documentation

```python
# BAD: Same info in code AND external doc
# README says "accepts name and email"
# Code also has type definition
# Result: Two places to update = guaranteed drift

# GOOD: Single source (code)
class CreateUser(BaseModel):
    name: str
    email: EmailStr
# README generated or removed
```

### Anti-Pattern 3: Hand-Written Diagrams

```markdown
# BAD: Hand-drawn architecture in docs/
┌─────┐     ┌─────┐
│ API │────►│ DB  │
└─────┘     └─────┘
# Will become wrong when architecture changes

# GOOD: Generated from code
npx madge --image docs/deps.svg src/
# Always current because derived
```

---

## Validation Checklist

```yaml
conversion_checklist:
  - question: "Is this documented in code?"
    tier_if_yes: T1-T7
    tier_if_no: T8-T9 (risky)
  
  - question: "Does it execute/validate?"
    tier_if_yes: T1-T6
    tier_if_no: T7-T9
  
  - question: "Is it generated from code?"
    tier_if_yes: T3
    tier_if_no: Check if should be
  
  - question: "Can it drift from implementation?"
    tier_if_yes: T8-T9 (avoid)
    tier_if_no: T1-T7 (preferred)
```
