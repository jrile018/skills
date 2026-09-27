---
name: "source-command-prime"
description: "Load project context — AGENTS.md, recent commits, structure — before starting work"
---

# source-command-prime

Use this skill when the user asks to run the migrated source command `prime`.

## Command Template

Load project context so you have full situational awareness before the next instruction.

Run in parallel:
1. Read AGENTS.md if it exists
2. `git log --oneline -20` for recent commits
3. `git status` for current state
4. List top-level project structure (2 levels deep, respect .gitignore)
5. Read the first 100 lines of README.md if it exists

Then summarize in 3–5 bullets:
- What the project does
- What's been worked on recently
- Current working state (branch, uncommitted changes, clean tree?)
- Any work-in-progress signals (TODO.md, HANDOFF.md, unfinished feature branches)

Do NOT start implementation work. Just confirm context is loaded and wait for the next instruction.
