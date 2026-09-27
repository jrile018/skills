---
name: finishing-approved-work
description: Use when a design or scope has already been approved and the user asks to continue, finish, complete, build the rest, fix everything, or otherwise carry the work through to a verified endpoint.
---

# Finishing Approved Work

## Principle

Treat approval as permission to make ordinary, reversible implementation decisions inside the agreed boundary. Maintain momentum without expanding the scope or inventing authority.

## Execution Contract

1. Restate the approved endpoint in one sentence and identify the current state from files, tools, or live systems.
2. Continue through safe in-scope decisions without asking the user to choose between equivalent implementation details.
3. Group independent checks or work when the environment permits it. Keep user updates short: completed, in progress, and material risk.
4. Stop for input only when a choice changes product behavior, cost, ownership, privacy, destructive impact, or external side effects beyond the authorization already given.
5. Verify the actual endpoint with fresh evidence. Tests alone do not prove UI, hardware, deployment, or external-system state.
6. End with:
   - delivered result;
   - verification evidence;
   - remaining items classified as `blocked`, `out of scope`, or `optional`;
   - exact next action only when one remains.

If unresolved work cannot be completed, record it in the project’s existing tracking document or a concise `BLOCKED.md` when the user requested a durable handoff.

## Quick Reference

| Situation | Action |
|---|---|
| Equivalent technical choices | Choose the best-supported option and proceed |
| Reversible local change | Implement and verify |
| New external mutation | Confirm it is already authorized |
| Destructive or privacy-sensitive action | Stop and obtain explicit authority |
| Genuine dependency failure | Document evidence and the precise unblock condition |

## Example

After the user approves a dashboard architecture and says “build the whole thing,” implement the approved views, run the relevant tests, inspect the rendered result, and report concrete gaps. Do not reopen color, naming, or internal-library choices unless they materially change the approved behavior.

## Common Mistakes

- Repeating design approval after it was already granted.
- Treating “finish” as permission for unrelated cleanup or publication.
- Reporting “done” from a partial test run.
- Hiding unfinished work behind vague phrases such as “future enhancement.”
