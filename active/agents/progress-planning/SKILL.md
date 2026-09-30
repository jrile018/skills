---
name: progress-planning
description: Create or maintain multi-step plans with explicit task decomposition and visible X/Y completion progress. Use when the user asks for a plan, roadmap, checklist, progress tracking, or a task is complex enough to benefit from a maintained plan. Do not add planning ceremony to a trivial one-step request.
---

# Progress Planning

Break work into outcome-sized tasks and keep the user able to answer two questions at a glance: what is being worked on, and how much remains.

## Create the plan

Use the native plan tool when one is available. Otherwise maintain the same information in a Markdown checklist.

1. Define top-level tasks by independently verifiable outcome, not by tool call or file edit.
2. Keep tasks ordered by real dependency. Run independent tasks in parallel only when the execution environment and task permit it.
3. Give every task one status: `pending`, `in_progress`, `completed`, or `blocked`. Keep at most one task `in_progress` unless the plan explicitly represents parallel workers.
4. Show the progress count with the plan:

```text
Progress: 2/6 tasks complete
```

The denominator is the current number of top-level tasks. The numerator counts only `completed` tasks.

## Progress contract

Every plan creation or plan update must include the exact current count in the form `Progress: X/Y tasks complete`. Include a compact task list when it helps the user see what remains:

```markdown
Progress: 2/4 tasks complete

- [x] Establish the input contract
- [x] Implement the parser
- [ ] Add failure-path tests — in progress
- [ ] Verify and document the result
```

Update the count immediately after a task changes status, a task is added or removed, or scope changes. Renumber or rewrite the visible task list so `Y` always equals the actual number of top-level tasks.

Count a task complete only when its promised artifact exists and its stated verification gate has passed. An attempted command, partial edit, delegated assignment, or unverified implementation is not completion. A blocked or skipped task remains incomplete unless the user explicitly removes it from scope.

## Right-size tasks

- Prefer a small number of meaningful, reviewable deliverables over dozens of mechanical steps.
- Split a task when its parts have different acceptance decisions or one part can complete independently.
- Combine setup, scaffolding, and documentation with the deliverable that needs them unless they produce an independently useful result.
- Name the verification inside the task when correctness depends on it.
- Preserve user-requested task boundaries and terminology when they are clear.

## Communicate while executing

When work is ongoing, begin every plan-status update with `Progress: X/Y tasks complete`, then state the current task, newly completed task, or blocker. Do not repeat the full plan when only one status changed unless the user asks for it.

If new evidence changes the approach, update the plan before proceeding and explain the changed tasks briefly. If the user replaces the objective, retire the old plan and create a new count rather than mixing unrelated work.

On completion, report `Progress: Y/Y tasks complete` and summarize the delivered artifacts and verification. Never claim `Y/Y` while required work remains.
