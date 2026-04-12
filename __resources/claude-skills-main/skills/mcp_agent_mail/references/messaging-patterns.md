# Common Messaging Patterns

Reference guide for common message types and structures used in agent-to-agent communication.

---

## Message Type Categories

### 1. Request Messages

Messages asking for action or information.

#### Code Review Request
```typescript
{
  type: "request",
  priority: "normal",
  subject: "Review Request: PR #123",
  body: {
    text: `Please review my changes.

    **Scope:** Authentication module refactor
    **Files changed:** 8 files, +320/-180 lines
    **Focus areas:**
    - Error handling in login flow
    - Token refresh logic
    - Test coverage

    **Timeline:** Need approval by EOD for release.
    `,
    files: [
      "/src/auth/login.ts",
      "/src/auth/token.ts",
      "/tests/auth.test.ts"
    ]
  }
}
```

#### Information Request
```typescript
{
  type: "question",
  priority: "normal",
  subject: "Question: Database migration strategy",
  body: {
    text: `What's the recommended approach for the upcoming schema migration?

    Context: Adding user roles table with foreign keys.

    Options I'm considering:
    1. Online migration with backfill
    2. Maintenance window approach
    3. Blue-green deployment

    What are your thoughts?
    `
  }
}
```

#### Task Assignment
```typescript
{
  type: "task",
  priority: "high",
  subject: "Task: Implement OAuth2 Integration",
  body: {
    text: `Please implement OAuth2 support.

    **Requirements:**
    - Google and GitHub providers
    - Token refresh mechanism
    - Integration tests
    - Documentation

    **Resources:**
    - Spec: /docs/auth-spec.md
    - Examples: /examples/oauth/

    **Deadline:** Friday EOD
    **Estimated effort:** 8 hours

    Reply to acknowledge receipt and confirm ETA.
    `,
    files: ["/docs/auth-spec.md"],
    data: {
      taskId: "TASK-1234",
      milestone: "v2.0",
      labels: ["feature", "auth"]
    }
  }
}
```

---

### 2. Response Messages

Replies to requests.

#### Acknowledgment Response
```typescript
{
  type: "response",
  priority: "normal",
  subject: "Re: Task: Implement OAuth2 Integration",
  body: {
    text: `Acknowledged. Starting implementation now.

    **Estimated completion:** Thursday EOD (1 day ahead of deadline)
    **Plan:**
    - Today: Google provider integration
    - Tomorrow: GitHub provider + tests
    - Thursday: Documentation + review

    Will send progress updates daily.
    `,
    metadata: {
      replyTo: "msg-task-1234"
    }
  }
}
```

#### Review Feedback Response
```typescript
{
  type: "response",
  priority: "normal",
  subject: "Re: Review Request: PR #123 - Feedback",
  body: {
    text: `Review complete. Found 2 issues:

    **Critical:**
    1. Line 145 in login.ts - SQL injection vulnerability
       Use parameterized queries instead of string concatenation

    **Minor:**
    2. Line 67 in token.ts - Missing error handling
       Add try-catch around refresh logic

    **Status:** Requesting changes
    **Re-review needed:** Yes, after fixes

    Otherwise looks good. Nice refactoring!
    `,
    codeSnippets: [
      {
        language: "typescript",
        file: "/src/auth/login.ts",
        lines: [145, 150],
        code: `// Bad\nconst query = \`SELECT * FROM users WHERE id = '\${userId}'\`;\n\n// Good\nconst query = 'SELECT * FROM users WHERE id = ?';\nconst result = await db.execute(query, [userId]);`
      }
    ]
  }
}
```

#### Question Answer
```typescript
{
  type: "response",
  priority: "normal",
  subject: "Re: Question: Database migration strategy",
  body: {
    text: `For your use case, I recommend **Option 1: Online migration with backfill**.

    **Rationale:**
    - No downtime required
    - Can be rolled back easily
    - Minimal user impact

    **Implementation steps:**
    1. Deploy new column (nullable)
    2. Backfill existing data
    3. Make column non-nullable
    4. Add constraints

    **Timeline:** ~4 hours total

    Let me know if you need help with the migration script.
    `
  }
}
```

---

### 3. Update Messages

Status and progress updates.

#### Progress Update
```typescript
{
  type: "update",
  priority: "low",
  subject: "Progress Update: OAuth2 Implementation",
  body: {
    text: `Daily standup update:

    **Yesterday:**
    - ✓ Implemented Google OAuth provider
    - ✓ Added basic token storage

    **Today:**
    - Working on GitHub provider
    - Writing integration tests

    **Blockers:** None
    **ETA:** Still on track for Thursday EOD
    `,
    data: {
      progress: 60,
      tasksCompleted: 3,
      tasksRemaining: 2
    }
  }
}
```

#### Completion Update
```typescript
{
  type: "update",
  priority: "normal",
  subject: "Complete: OAuth2 Implementation",
  body: {
    text: `OAuth2 implementation complete!

    **Delivered:**
    - ✓ Google OAuth provider
    - ✓ GitHub OAuth provider
    - ✓ Token refresh mechanism
    - ✓ Integration tests (95% coverage)
    - ✓ Documentation

    **Artifacts:**
    - PR: #456 (ready for review)
    - Docs: /docs/auth/oauth2.md
    - Tests: All passing ✓

    **Next steps:** Code review

    Completed 1 day ahead of schedule.
    `,
    files: [
      "/src/auth/oauth/google.ts",
      "/src/auth/oauth/github.ts",
      "/docs/auth/oauth2.md"
    ]
  }
}
```

#### Status Change
```typescript
{
  type: "update",
  priority: "normal",
  subject: "Status Change: Going Offline",
  body: {
    text: `Signing off for the day. Will resume tomorrow 9am.

    **Current state:**
    - All active reservations released
    - No pending urgent tasks
    - Next: Continue with payment integration

    **Availability:** Offline until tomorrow
    `
  }
}
```

---

### 4. Notification Messages

FYI updates requiring no response.

#### Deployment Notification
```typescript
{
  type: "notification",
  priority: "high",
  subject: "Deployment: v2.3.1 to Production",
  body: {
    text: `Production deployment completed successfully.

    **Version:** v2.3.1
    **Environment:** Production
    **Time:** ${new Date().toISOString()}
    **Duration:** 5 minutes

    **Changes:**
    - OAuth2 integration
    - Bug fixes in payment flow
    - Performance improvements

    **Rollback plan:** Available if needed
    **Monitoring:** All metrics healthy

    No action required.
    `,
    data: {
      version: "2.3.1",
      environment: "production",
      deploymentId: "deploy-789"
    }
  }
}
```

#### Breaking Change Announcement
```typescript
{
  type: "notification",
  priority: "urgent",
  subject: "Breaking Change: API v2 Migration Required",
  body: {
    text: `BREAKING CHANGE announced.

    **What:** API v1 endpoints deprecated
    **When:** Shutdown on March 31
    **Impact:** All API consumers must migrate

    **Migration guide:** /docs/migration/v1-to-v2.md

    **Timeline:**
    - Now: Announcement
    - March 1: v1 returns deprecation warnings
    - March 15: Reminder notifications
    - March 31: v1 shutdown

    **Action required:** Review your API calls and plan migration.

    Questions? Reply to this thread.
    `,
    files: ["/docs/migration/v1-to-v2.md"]
  }
}
```

#### System Notification
```typescript
{
  type: "notification",
  priority: "normal",
  subject: "System Maintenance: Scheduled Downtime",
  body: {
    text: `Scheduled maintenance window announced.

    **When:** Sunday, March 15, 2:00-4:00 AM UTC
    **Duration:** 2 hours
    **Impact:** Agent Mail server unavailable

    **During maintenance:**
    - No message sending/receiving
    - File reservations preserved
    - Messages queued for delivery after

    **Preparation:**
    - Complete critical work before window
    - Release non-essential reservations
    - Plan for offline period

    Server will auto-resume after maintenance.
    `
  }
}
```

---

### 5. Broadcast Messages

One-to-many announcements.

#### Team Announcement
```typescript
{
  type: "broadcast",
  priority: "normal",
  to: "broadcast",
  subject: "New Agent Joining Team",
  body: {
    text: `Welcome our new team member!

    **Agent:** agent-security-scanner
    **Role:** Security specialist
    **Capabilities:**
    - Static code analysis
    - Dependency vulnerability scanning
    - OWASP compliance checking

    **Integration:**
    - Available for code review requests
    - Runs automated scans on PRs
    - Contact for security questions

    Please add to your agent roster.
    `
  }
}
```

#### Emergency Broadcast
```typescript
{
  type: "broadcast",
  priority: "urgent",
  to: "broadcast",
  subject: "🚨 EMERGENCY: Production Incident",
  body: {
    text: `PRODUCTION INCIDENT - IMMEDIATE ACTION REQUIRED

    **Severity:** P0 - Complete outage
    **Impact:** All users unable to access service
    **Started:** ${new Date().toISOString()}

    **IMMEDIATE ACTIONS:**
    1. STOP all non-critical work
    2. RELEASE all file reservations
    3. DO NOT push to main branch
    4. JOIN incident thread: "incident-2024-03-15"

    **Incident Commander:** agent-oncall
    **Updates:** Every 15 minutes in incident thread

    This is not a drill. Acknowledge receipt.
    `
  }
}
```

#### Code Freeze Announcement
```typescript
{
  type: "broadcast",
  priority: "high",
  to: "broadcast",
  subject: "Code Freeze: Release v2.0",
  body: {
    text: `Code freeze in effect for release v2.0

    **Start:** Now
    **End:** Friday 5pm (after release)
    **Duration:** ~24 hours

    **Restrictions:**
    - No merges to main branch
    - No new feature work
    - Bug fixes only (with approval)

    **Allowed:**
    - Documentation updates
    - Test improvements
    - Release preparation

    Release tracking: thread "release-v2.0"
    Questions? Contact release manager.
    `
  }
}
```

---

## Message Priority Guidelines

### Urgent Priority
```typescript
{ priority: "urgent" }
```

**Use for:**
- Production incidents
- Critical blockers
- Security vulnerabilities
- Emergency coordination

**Expected response:** < 5 minutes

**Example:**
```typescript
{
  priority: "urgent",
  subject: "🚨 Security Vulnerability Detected",
  body: {
    text: "SQL injection vulnerability in production. Needs immediate patch."
  }
}
```

### High Priority
```typescript
{ priority: "high" }
```

**Use for:**
- Important bugs
- Release blockers
- Time-sensitive requests
- Breaking changes

**Expected response:** < 1 hour

**Example:**
```typescript
{
  priority: "high",
  subject: "Release Blocker: Test Failures",
  body: {
    text: "Integration tests failing on release branch. Blocks deployment."
  }
}
```

### Normal Priority
```typescript
{ priority: "normal" }
```

**Use for:**
- Standard requests
- Code reviews
- Questions
- Regular updates

**Expected response:** Same day

**Example:**
```typescript
{
  priority: "normal",
  subject: "Code Review Request: Feature X",
  body: {
    text: "Please review when you have time today."
  }
}
```

### Low Priority
```typescript
{ priority: "low" }
```

**Use for:**
- FYI updates
- Optional improvements
- Non-urgent questions
- Nice-to-have features

**Expected response:** Best effort

**Example:**
```typescript
{
  priority: "low",
  subject: "Suggestion: Performance Optimization",
  body: {
    text: "Found potential optimization. Low priority, no rush."
  }
}
```

---

## Rich Content Patterns

### With Code Snippets
```typescript
{
  body: {
    text: "Here's the solution:",
    codeSnippets: [
      {
        language: "typescript",
        code: `async function fetchUser(id: string) {
  const query = 'SELECT * FROM users WHERE id = ?';
  return await db.execute(query, [id]);
}`,
        file: "/src/users/fetch.ts",
        lines: [10, 13]
      }
    ]
  }
}
```

### With File Attachments
```typescript
{
  body: {
    text: "Attached architecture diagram:",
    attachments: [
      {
        name: "architecture.png",
        type: "image/png",
        size: 125000,
        url: "https://storage/architecture.png"
      },
      {
        name: "spec.pdf",
        type: "application/pdf",
        size: 450000,
        url: "https://storage/spec.pdf"
      }
    ]
  }
}
```

### With Structured Data
```typescript
{
  body: {
    text: "Test results summary:",
    data: {
      totalTests: 150,
      passed: 145,
      failed: 5,
      duration: "2m 34s",
      failures: [
        { test: "auth.login", error: "Timeout" },
        { test: "payment.process", error: "Network error" }
      ]
    }
  }
}
```

### With File References
```typescript
{
  body: {
    text: "Modified the following files:",
    files: [
      "/src/auth/login.ts",
      "/src/auth/session.ts",
      "/tests/auth.test.ts",
      "/docs/auth.md"
    ]
  }
}
```

---

## Thread Patterns

### Starting a Discussion Thread
```typescript
const thread = await tools.agent_mail.createThread({
  subject: "Architecture Decision: Microservices vs Monolith",
  participants: [
    "agent-architect",
    "agent-backend",
    "agent-devops"
  ]
});

await tools.agent_mail.sendMessageToThread({
  threadId: thread.id,
  body: {
    text: "Let's discuss the architecture for the new billing system..."
  }
});
```

### Contributing to Thread
```typescript
await tools.agent_mail.replyToThread({
  threadId: "thread-123",
  body: {
    text: "I agree with the microservices approach. Here's why...",
    metadata: {
      replyTo: "msg-456" // Specific message ID
    }
  }
});
```

### Closing a Thread
```typescript
await tools.agent_mail.closeThread({
  threadId: "thread-123",
  summary: `
  **Decision:** Microservices architecture approved

  **Rationale:** Better scalability and team autonomy

  **Action items:**
  1. DevOps: Set up Kubernetes cluster
  2. Architect: Create service boundaries
  3. Backend: Begin service extraction
  `
});
```

---

## Anti-Patterns to Avoid

### ❌ Vague Subjects
```typescript
// Bad
{ subject: "Question" }
{ subject: "Help needed" }
{ subject: "Issue" }

// Good
{ subject: "Question: Database migration strategy" }
{ subject: "Help needed: OAuth2 integration error" }
{ subject: "Issue: Test failures on PR #123" }
```

### ❌ Missing Context
```typescript
// Bad
{
  body: {
    text: "Can you review this?"
  }
}

// Good
{
  body: {
    text: "Can you review PR #123? Focus on error handling in login flow.",
    files: ["/src/auth/login.ts"]
  }
}
```

### ❌ Wrong Priority
```typescript
// Bad - Misusing urgent priority
{
  priority: "urgent",
  subject: "Reminder: Team meeting tomorrow"
}

// Good
{
  priority: "normal",
  subject: "Reminder: Team meeting tomorrow"
}
```

### ❌ Overly Long Messages
```typescript
// Bad - Wall of text
{
  body: {
    text: `[3000 words of detailed explanation]`
  }
}

// Good - Concise with attachments
{
  body: {
    text: "See attached document for detailed analysis.",
    attachments: [{ name: "analysis.md", url: "..." }]
  }
}
```

---

## Best Practices Summary

1. **Clear subjects** - Recipient should know content at a glance
2. **Appropriate priority** - Use urgency levels correctly
3. **Rich context** - Include files, code, data as needed
4. **Structured content** - Use formatting for readability
5. **Actionable items** - Make requests explicit
6. **Timely responses** - Respect priority expectations
7. **Thread hygiene** - Keep conversations focused
8. **Acknowledge receipt** - Confirm you received important messages
