---
name: "source-command-handoff"
description: "Write HANDOFF.md summarizing session state for a fresh session to resume"
---

# source-command-handoff

Use this skill when the user asks to run the migrated source command `handoff`.

## Command Template

Create or update `HANDOFF.md` in the current working directory with this structure:

```
# Session Handoff — <ISO date>

## Current Goal
One-sentence description of what's being worked on.

## Progress
What's been completed. Reference file paths and line numbers where relevant.

## What Worked
Approaches that produced results. Brief.

## What Didn't
Dead ends and why. Helps the next session avoid the same traps.

## Next Steps
Concrete next 1–3 actions for a fresh session to pick up. Ordered.

## Open Questions
Decisions not yet made, blockers, or areas needing user input.
```

Keep the whole file under one screen (≈60 lines). Prefer bullets over prose. After writing, tell the user where it was saved in one line — no recap.
