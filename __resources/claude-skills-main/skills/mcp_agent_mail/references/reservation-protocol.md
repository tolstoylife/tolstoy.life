# File Reservation Protocol Reference

Quick reference guide for file locking patterns and reservation management.

---

## Basic Reservation Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│                   Reservation Flow                       │
└─────────────────────────────────────────────────────────┘

1. CHECK      → Verify file is available
2. RESERVE    → Acquire lock (exclusive or shared)
3. WORK       → Modify/read file
4. RELEASE    → Free lock immediately
```

---

## Quick Command Reference

### Check Reservation Status
```bash
# Check if file is reserved
agent-mail reserve check /path/to/file.ts

# Output format:
# Status: active | available
# Agent: agent-id (if reserved)
# Purpose: edit | read | delete | create | refactor
# Mode: exclusive | shared
# Expires: 2024-03-15T14:30:00Z
```

### Reserve File
```bash
# Exclusive mode (default)
agent-mail reserve /path/to/file.ts \
  --agent agent-id \
  --purpose edit \
  --mode exclusive \
  --expires-in 3600

# Shared mode (multiple readers)
agent-mail reserve /path/to/file.ts \
  --agent agent-id \
  --purpose read \
  --mode shared \
  --expires-in 1800
```

### Release Reservation
```bash
# Release specific reservation
agent-mail release <reservation-id>

# Release all reservations for agent
agent-mail release --agent agent-id --all

# Force release (coordinator only)
agent-mail release <reservation-id> --force
```

### List Reservations
```bash
# List all active reservations
agent-mail reservations list --status active

# List reservations by agent
agent-mail reservations list --agent agent-id

# List stale reservations (>2 hours old)
agent-mail reservations audit --stale
```

---

## TypeScript API Reference

### Check Before Reserving (Always!)

```typescript
const status = await tools.agent_mail.checkReservation({
  path: "/src/auth/login.ts"
});

if (status.status === "active") {
  console.log(`Reserved by: ${status.agentId}`);
  console.log(`Purpose: ${status.purpose}`);
  console.log(`Expires: ${status.expiresAt}`);

  // Coordinate with owner
  await coordinateWithAgent(status.agentId);
} else {
  // Proceed to reserve
}
```

### Reserve File (Exclusive)

```typescript
const reservation = await tools.agent_mail.reserveFile({
  agentId: "my-agent-id",
  path: "/src/auth/login.ts",
  purpose: "refactor",        // edit | read | delete | create | refactor
  mode: "exclusive",           // Only I can access
  expiresIn: 3600,            // Auto-release after 1 hour
  metadata: {
    threadId: "refactor-auth",
    notes: "Extracting login logic to separate module",
    priority: "high"
  }
});

console.log(`Reservation ID: ${reservation.id}`);
```

### Reserve File (Shared)

```typescript
const reservation = await tools.agent_mail.reserveFile({
  agentId: "my-agent-id",
  path: "/src/complex-module.ts",
  purpose: "read",             // Read-only access
  mode: "shared",              // Multiple readers allowed
  expiresIn: 1800,            // 30 minutes
  metadata: {
    notes: "Code analysis for refactoring plan"
  }
});
```

### Reserve Multiple Files (Atomic)

```typescript
const files = [
  "/src/auth/login.ts",
  "/src/auth/session.ts",
  "/src/auth/token.ts"
];

// Reserve all or none
try {
  const reservations = await tools.agent_mail.reserveFiles({
    agentId: "my-agent-id",
    paths: files,
    purpose: "refactor",
    mode: "exclusive",
    atomic: true  // Fails if any file already reserved
  });

  // All files reserved successfully
  await doWork(files);

  // Release all
  await tools.agent_mail.releaseFiles({
    reservationIds: reservations.map(r => r.id)
  });
} catch (error) {
  // One or more files unavailable
  console.error("Reservation conflict:", error);
}
```

### Release Reservation

```typescript
// Always release in finally block
try {
  const reservation = await tools.agent_mail.reserveFile({...});
  await doWork();
} finally {
  await tools.agent_mail.releaseReservation({
    reservationId: reservation.id
  });
}
```

### Extend Reservation

```typescript
// Extend expiry time
await tools.agent_mail.extendReservation({
  reservationId: reservation.id,
  additionalSeconds: 1800  // Add 30 more minutes
});
```

---

## Reservation Modes

### Exclusive Mode

**Use for:** Modifying files

```typescript
{
  mode: "exclusive"
}
```

**Behavior:**
- ✓ Only reserving agent can access file
- ✗ No other agents can read or write
- ✓ Prevents all conflicts
- ⚠️ Blocks other agents completely

**Best for:**
- Editing files
- Refactoring
- Deleting files
- Creating new files
- Structural changes

### Shared Mode

**Use for:** Read-only access

```typescript
{
  mode: "shared"
}
```

**Behavior:**
- ✓ Multiple agents can reserve for reading
- ✗ No agent can write while shared reservations exist
- ✓ Allows parallel analysis
- ⚠️ Must upgrade to exclusive for editing

**Best for:**
- Code analysis
- Documentation reading
- Research/investigation
- Non-destructive operations

---

## Reservation Purposes

### edit
```typescript
{ purpose: "edit" }
```
Planning to modify file content

### read
```typescript
{ purpose: "read" }
```
Read-only access for analysis

### delete
```typescript
{ purpose: "delete" }
```
Planning to remove file

### create
```typescript
{ purpose: "create" }
```
Planning to create new file

### refactor
```typescript
{ purpose: "refactor" }
```
Structural changes to file

---

## Common Patterns

### Pattern 1: Simple Edit

```typescript
async function editFile(path: string) {
  // 1. Check
  const status = await tools.agent_mail.checkReservation({ path });
  if (status.status === "active") {
    throw new Error(`File reserved by ${status.agentId}`);
  }

  // 2. Reserve
  const reservation = await tools.agent_mail.reserveFile({
    agentId: myAgentId,
    path,
    purpose: "edit",
    mode: "exclusive",
    expiresIn: 3600
  });

  try {
    // 3. Work
    await modifyFile(path);
  } finally {
    // 4. Release
    await tools.agent_mail.releaseReservation({
      reservationId: reservation.id
    });
  }
}
```

### Pattern 2: Progressive Lock (Shared → Exclusive)

```typescript
async function analyzeAndEdit(path: string) {
  // Phase 1: Analysis (shared mode)
  const analysisReservation = await tools.agent_mail.reserveFile({
    agentId: myAgentId,
    path,
    purpose: "read",
    mode: "shared"
  });

  const analysis = await analyzeCode(path);

  // Release shared lock
  await tools.agent_mail.releaseReservation({
    reservationId: analysisReservation.id
  });

  // Phase 2: Editing (exclusive mode)
  const editReservation = await tools.agent_mail.reserveFile({
    agentId: myAgentId,
    path,
    purpose: "edit",
    mode: "exclusive"
  });

  try {
    await applyChanges(path, analysis);
  } finally {
    await tools.agent_mail.releaseReservation({
      reservationId: editReservation.id
    });
  }
}
```

### Pattern 3: Cascading Reservations

```typescript
async function refactorWithDependencies(mainFile: string) {
  // Find dependencies
  const dependencies = await analyzeDependencies(mainFile);

  // Reserve all dependencies as shared (read-only)
  const depReservations = await Promise.all(
    dependencies.map(dep =>
      tools.agent_mail.reserveFile({
        agentId: myAgentId,
        path: dep,
        purpose: "read",
        mode: "shared"
      })
    )
  );

  // Reserve main file as exclusive
  const mainReservation = await tools.agent_mail.reserveFile({
    agentId: myAgentId,
    path: mainFile,
    purpose: "refactor",
    mode: "exclusive"
  });

  try {
    await refactor(mainFile, dependencies);
  } finally {
    // Release all reservations
    await tools.agent_mail.releaseReservation({
      reservationId: mainReservation.id
    });

    await Promise.all(
      depReservations.map(res =>
        tools.agent_mail.releaseReservation({
          reservationId: res.id
        })
      )
    );
  }
}
```

### Pattern 4: Time-Boxed Work

```typescript
async function timeBoxedEdit(path: string, maxMinutes: number) {
  const reservation = await tools.agent_mail.reserveFile({
    agentId: myAgentId,
    path,
    purpose: "edit",
    mode: "exclusive",
    expiresIn: maxMinutes * 60
  });

  // Set reminder before expiry
  const reminderTime = (maxMinutes - 5) * 60 * 1000;
  setTimeout(async () => {
    await tools.agent_mail.sendMessage({
      to: "self",
      priority: "high",
      subject: "Reservation expiring soon",
      body: { text: `5 minutes until ${path} auto-releases` }
    });
  }, reminderTime);

  try {
    await doWork(path);

    // If need more time, extend
    if (needMoreTime()) {
      await tools.agent_mail.extendReservation({
        reservationId: reservation.id,
        additionalSeconds: maxMinutes * 60
      });
    }
  } finally {
    await tools.agent_mail.releaseReservation({
      reservationId: reservation.id
    });
  }
}
```

### Pattern 5: Reservation Queue

```typescript
async function waitForFile(path: string) {
  while (true) {
    const status = await tools.agent_mail.checkReservation({ path });

    if (status.status === "available") {
      // File available, reserve now
      return await tools.agent_mail.reserveFile({
        agentId: myAgentId,
        path,
        purpose: "edit",
        mode: "exclusive"
      });
    }

    // Wait for current reservation to expire
    const expiresIn = new Date(status.expiresAt) - new Date();
    console.log(`Waiting ${expiresIn}ms for ${path}...`);

    await sleep(Math.min(expiresIn, 60000)); // Check every minute
  }
}
```

---

## Conflict Resolution

### Scenario 1: File Already Reserved

**Detection:**
```typescript
const status = await tools.agent_mail.checkReservation({
  path: "/src/file.ts"
});

if (status.status === "active") {
  console.log("Conflict detected!");
  // Handle conflict...
}
```

**Resolution Options:**

#### Option A: Wait for Expiry
```typescript
const expiryTime = new Date(status.expiresAt);
const waitTime = expiryTime - new Date();

console.log(`Waiting ${waitTime}ms for file to be released...`);
await sleep(waitTime + 1000); // Add 1 second buffer

// Try reserving again
await tools.agent_mail.reserveFile({...});
```

#### Option B: Request Handoff
```typescript
await tools.agent_mail.sendMessage({
  from: myAgentId,
  to: status.agentId,
  priority: "high",
  subject: `Request access to ${status.path}`,
  body: {
    text: `I need to work on this file. Can you release it or shall we coordinate?

    My need: ${myPurpose}
    Your current: ${status.purpose}

    Deadline: ${myDeadline}
    `
  }
});

// Wait for response and coordination
```

#### Option C: Escalate to Coordinator
```typescript
await tools.agent_mail.sendMessage({
  to: "coordinator",
  priority: "urgent",
  subject: "Reservation Conflict",
  body: {
    text: `Conflict on ${status.path}

    Current holder: ${status.agentId}
    Requesting: ${myAgentId}

    Both have high-priority tasks. Need resolution.
    `
  }
});
```

### Scenario 2: Stale Reservation

**Detection:**
```bash
agent-mail reservations audit --stale

# Output:
# Reservation: res-123
# Path: /src/file.ts
# Agent: agent-offline (status: offline)
# Age: 3 hours
# Status: stale
```

**Resolution (Coordinator):**
```bash
# Force release stale reservation
agent-mail release res-123 --force \
  --reason "Agent offline >2 hours"

# Log the action
agent-mail send --to audit-log \
  --subject "Force-released stale reservation" \
  --body "res-123 released: agent offline"
```

### Scenario 3: Accidental Violation

**What happened:**
```typescript
// Agent modified file without checking reservation
await modifyFile("/src/file.ts");
// Oops! File was reserved by another agent
```

**Resolution:**
```typescript
// 1. Notify reservation owner immediately
await tools.agent_mail.sendMessage({
  to: reservationOwner,
  priority: "urgent",
  subject: "Accidental Reservation Violation",
  body: {
    text: `I accidentally modified ${path} without realizing it was reserved.

    Commit: ${commitHash}
    Changes: ${changeDescription}

    Options:
    1. I can revert my changes
    2. We can merge our work
    3. You can review and integrate

    What would you prefer?
    `
  }
});

// 2. Mark reservation as violated
await tools.agent_mail.updateReservation({
  reservationId,
  status: "violated",
  metadata: {
    violatedBy: myAgentId,
    commit: commitHash,
    timestamp: new Date().toISOString()
  }
});

// 3. Create incident report
await tools.agent_mail.sendMessage({
  to: "coordinator",
  priority: "high",
  subject: "Reservation Protocol Violation",
  body: {
    text: "Accidental violation occurred. Coordinating resolution."
  }
});
```

---

## Integration Examples

### With Git Hooks

**pre-commit hook:**
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Checking file reservations..."

# Get list of staged files
STAGED_FILES=$(git diff --cached --name-only)

for file in $STAGED_FILES; do
  # Check if file is reserved by another agent
  RESERVATION=$(agent-mail reserve check "$file" --format json)
  STATUS=$(echo "$RESERVATION" | jq -r '.status')
  AGENT=$(echo "$RESERVATION" | jq -r '.agentId')

  if [ "$STATUS" = "active" ] && [ "$AGENT" != "$MY_AGENT_ID" ]; then
    echo "❌ Error: $file is reserved by $AGENT"
    echo "Cannot commit. Coordinate with $AGENT first."
    exit 1
  fi
done

echo "✓ All files clear for commit"
```

### With CI/CD

**GitHub Actions workflow:**
```yaml
name: Check Reservations
on: [push, pull_request]

jobs:
  check-reservations:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Check file reservations
        run: |
          # Get changed files
          CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD)

          # Check each file
          for file in $CHANGED_FILES; do
            STATUS=$(agent-mail reserve check "$file" --format json)

            if echo "$STATUS" | jq -e '.status == "active"' > /dev/null; then
              echo "::error::$file is reserved"
              exit 1
            fi
          done
```

### With Editor (VS Code Extension)

```typescript
// Show reservation status in editor
import * as vscode from 'vscode';

vscode.workspace.onDidOpenTextDocument(async (doc) => {
  const status = await checkReservation(doc.uri.fsPath);

  if (status.status === "active") {
    // Show warning banner
    vscode.window.showWarningMessage(
      `⚠️ File reserved by ${status.agentId} for ${status.purpose}`,
      "Contact Agent",
      "Request Access"
    ).then(selection => {
      if (selection === "Contact Agent") {
        contactAgent(status.agentId, doc.uri.fsPath);
      }
    });

    // Add decoration to editor
    const decoration = vscode.window.createTextEditorDecorationType({
      backgroundColor: 'rgba(255, 165, 0, 0.1)',
      isWholeLine: true
    });

    // Highlight entire file
    const editor = vscode.window.activeTextEditor;
    if (editor) {
      const fullRange = new vscode.Range(
        editor.document.lineAt(0).range.start,
        editor.document.lineAt(editor.document.lineCount - 1).range.end
      );
      editor.setDecorations(decoration, [fullRange]);
    }
  }
});
```

---

## Best Practices Checklist

### Before Reserving
- ✅ Check if file is available
- ✅ Verify no conflicts with team work
- ✅ Choose appropriate mode (exclusive vs shared)
- ✅ Set reasonable expiry time

### During Reservation
- ✅ Work only on reserved files
- ✅ Monitor expiry time
- ✅ Update progress if long-running
- ✅ Extend if need more time

### After Work
- ✅ Release immediately after completion
- ✅ Notify team if significant changes
- ✅ Document what was done
- ✅ Verify release was successful

### General
- ✅ Reserve minimally (only what you'll modify)
- ✅ Use shared mode for read-only access
- ✅ Handle failures gracefully (finally blocks)
- ✅ Coordinate on conflicts
- ✅ Respect others' reservations

---

## Troubleshooting

### Can't Reserve File
```bash
# Check why
agent-mail reserve check /path/to/file.ts --verbose

# Outputs:
# Status: active
# Agent: agent-other
# Purpose: refactor
# Expires: 2024-03-15T14:30:00Z
# Solution: Wait or coordinate with agent-other
```

### Forgotten Release
```bash
# List my active reservations
agent-mail reservations list --agent my-agent-id --status active

# Release all
agent-mail release --agent my-agent-id --all
```

### Reservation Expired
```bash
# Check status
agent-mail reservations info res-123

# Output:
# Status: expired
# Reason: Auto-released after timeout
# Solution: Reserve again if still needed
```

### Force Release (Emergency)
```bash
# Coordinator only
agent-mail release res-123 --force \
  --reason "Production emergency override"

# Notify owner
agent-mail send --to agent-owner \
  --priority urgent \
  --subject "Force release: Production emergency" \
  --body "Your reservation was released due to P0 incident"
```

---

## Quick Reference Card

```
╔═══════════════════════════════════════════════════════╗
║         File Reservation Quick Reference              ║
╠═══════════════════════════════════════════════════════╣
║ CHECK     → agent-mail reserve check <path>           ║
║ RESERVE   → agent-mail reserve <path> --mode ...      ║
║ RELEASE   → agent-mail release <reservation-id>       ║
║ LIST      → agent-mail reservations list              ║
║ EXTEND    → agent-mail extend <id> --seconds ...      ║
╠═══════════════════════════════════════════════════════╣
║ Modes:                                                ║
║   exclusive  → Only I can access                      ║
║   shared     → Multiple readers allowed               ║
║                                                       ║
║ Purposes:                                             ║
║   edit       → Modifying content                      ║
║   read       → Read-only analysis                     ║
║   delete     → Removing file                          ║
║   create     → Creating new file                      ║
║   refactor   → Structural changes                     ║
╠═══════════════════════════════════════════════════════╣
║ Always:                                               ║
║   1. Check before reserving                           ║
║   2. Reserve minimally                                ║
║   3. Set expiry time                                  ║
║   4. Release in finally block                         ║
╚═══════════════════════════════════════════════════════╝
```
