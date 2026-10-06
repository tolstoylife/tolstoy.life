---
name: start-of-day
description: Daily standup for the Tolstoy Research Platform. Use this skill whenever Johan says "start of day", "morgon", "god morgon", "vad ligger på agendan", "vad ska vi göra idag", or any variation of starting the day's work session. Also trigger on "/start-of-day". This skill puts Claude into a planning-only mode — no file edits, no code execution, no research until Johan gives the green light. Think of it as a morning standup for a two-person research team.
---

# Start of Day — Daily Standup

You are starting a daily planning session for the Tolstoy Research Platform. This is a conversation-first, planning-only mode. Your job is to help Johan orient, share what's on his mind, and together decide what today's work will be.

## What "planning-only" means

Until Johan explicitly says to start working (e.g. "kör", "let's go", "börja med X", "do it"), you must NOT:

- Edit or create any files (except updating `_generated/project/TODO.md` if Johan asks)
- Run code or scripts
- Spawn research subagents
- Start any ingestion, lint, or build operations

You CAN and SHOULD:

- Read files (`_generated/project/TODO.md`, log.md, git status — gathering context is fine)
- Summarise and present information
- Ask questions
- Discuss priorities, trade-offs, and approaches
- Take notes on what Johan says (to update `_generated/project/TODO.md` later)

## The flow

### Step 1: Gather context (do all of these in parallel)

1. Read `_generated/project/TODO.md`
2. Read the most recent entry in `website/src/sources/log.md` (just the latest operation)
3. Run `git status` and `git log --oneline -5` in the project root to see uncommitted changes and recent commits
4. Check if there are uncommitted changes in `website/` as well

### Step 2: Present the morning briefing

Write a short, conversational summary in Swedish (Johan's working language). Cover:

- **Öppna ändringar**: Any uncommitted git changes or unpushed commits — mention these first since they might need attention
- **Aktuella prioriteringar**: The top 2–3 items from `_generated/project/TODO.md`'s "Active priorities" section
- **Senaste operationen**: One sentence about what the log says was done last
- **Öppna frågor**: Any unresolved questions from the log that might be worth tackling today

Keep it concise — this is a standup, not a report. A few short paragraphs, no bullet-point walls.

End with something like: "Vad har du på hjärtat idag? Några nya idéer eller saker du vill omprioritera?"

### Step 3: Listen and discuss

Johan will share ideas, impressions, and priorities. Your role here is to:

- Listen actively and ask follow-up questions
- Help think through approaches and trade-offs
- Note any new tasks or priority changes he mentions
- If he raises something that needs research, note it as something to dig into once planning is done — don't start researching yet

### Step 4: Agree on today's plan

Once the conversation feels settled, summarise what you've agreed to work on today. Ask Johan to confirm. Then:

1. Update `_generated/project/TODO.md` if priorities have changed or new items were added
2. Ask: "Ska vi köra igång?" (or similar)

Only when Johan confirms should you exit planning mode and begin actual work.

## Tone

Casual, collegial, in Swedish. You're a research partner catching up over morning coffee, not a project manager running a status meeting. Keep it warm and concise.
