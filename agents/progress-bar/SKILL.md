---
name: progress-bar
description: Use whenever starting work that has more than 2 tool calls, more than one subagent dispatch, or any visible wait. Renders an inline ASCII progress bar before every step so the user can visually monitor progress and ETA. Always-active.
---

# Progress-Bar Skill — Visual Monitoring Contract

## Rule

Whenever you start any task that meets ANY of these triggers, you MUST render a progress bar:

- More than 2 sequential tool calls
- Any subagent dispatch (parallel or serial)
- Any `Bash` call expected to take >5 seconds (tests, builds, installs, long greps)
- Any user request containing "run", "build", "test", "audit", "analyze", "research"
- Any loop / iteration over a list of items

## Format

Before the FIRST step, emit a one-line plan:

```
Plan ──────────────────────────────
  ▸ 1. <step 1 imperative>
  ▸ 2. <step 2 imperative>
  ▸ 3. <step 3 imperative>
  ...
```

Then, before EACH step, emit a progress bar line as PLAIN TEXT in your chat output (NOT a tool call):

```
[████░░░░░░] 4/10 · ~2m left · Running tests
```

Format rules:
- 10-character bar using `█` (filled) and `░` (empty)
- `N/M` — current step / total steps
- `~<duration> left` — ETA estimate based on elapsed time per completed step. For the first step, write `~? left`.
- Description — one short imperative, max 40 chars.

On completion, emit:

```
[██████████] 10/10 · done · <one-line summary>
```

On failure or deviation:

```
[██████░░░░] 6/10 · ⚠ blocked · <what blocked>
```

## When parallel subagents are in flight

Show a per-agent sub-bar beneath the main bar, updated as notifications arrive:

```
[██░░░░░░░░] 2/10 · Running research agents (4 in flight)
  ├─ [████████░░] research-caching · 80%
  ├─ [██████░░░░] research-hooks · 60%
  ├─ [██░░░░░░░░] research-memory · 20%
  └─ [░░░░░░░░░░] research-dispatch · queued
```

(Sub-bars are estimates — actual Agent tool calls don't stream progress. Update them as agents complete.)

## Anti-patterns

- **Don't render bars for single-tool-call responses.** A one-off `Read` doesn't need `[█░░░░░░░░░] 1/1`. Use judgment.
- **Don't use TaskCreate as a substitute.** TaskCreate tracks state internally; the user wants visible ASCII bars in the chat. Do both when work is multi-step.
- **Don't emit a bar and then silently work for 30s.** If a tool call is slow, the bar for that step must appear BEFORE the tool call.
- **Don't fake ETAs.** If you don't have timing data from prior steps, write `~? left` — not an invented number.

## Integration with existing workflow

- Works alongside TaskCreate/TaskUpdate (the statusline reads `in_progress` todos). Use both.
- Works in parallel with all superpowers skills (brainstorming, executing-plans, etc.).
- The custom statusline (`gsd-statusline.js`) shows context/cost/git at the bottom; this skill complements by showing step-level progress in chat.

## Why this matters

User is a heavy dev workflow operator who wants to visually monitor Codex's work without reading verbose narration. Bars compress "where are we + how long" into a single glance.
