---
name: orchestrate-parallel-work
description: Plan and execute substantial work with dependency-aware Codex subagents while minimizing elapsed time, context cost, and write conflicts. Use when the user asks to parallelize, delegate, use subagents, execute a multi-part plan, or complete substantial work with independent lanes; do not use for small or inherently sequential tasks.
---

# Orchestrate Parallel Work

Optimize for verified completion on the critical path, not maximum agent count.
Parallelism must earn its coordination cost.

## Choose the execution shape

Apply `$parallelize` when the split is uncertain or strategically important.
Keep work with the coordinator when it is short, sequential, or coupled through
shared mutable state. Delegate only when at least two ready units have stable
contracts and either reduce elapsed time or materially improve independent
coverage.

Before dispatch, read [references/plan-schema.md](references/plan-schema.md) and
represent the work as a dependency graph. Use `$writing-plans` for detailed
implementation steps, then add the dependency, ownership, and scheduling fields
from that schema.

If the user asked only for a plan, stop after planning. If the user already
asked to implement or execute, the plan is an internal control artifact and
does not require a second approval pause; continue unless execution needs new
authority or reaches a genuine blocker.

Choose one execution path:

- Independent research or disjoint write lanes: use
  `$dispatching-parallel-agents` with the scheduling rules below.
- Tightly coupled implementation or work needing a review gate after every
  change: use `$subagent-driven-development` sequentially.
- No useful delegation seam: execute locally; do not create ceremonial agents.

Do not combine parallel dispatch and subagent-driven development for the same
task set.

## Protect ownership and state

The coordinator exclusively owns the dependency graph, shared plan or ledger,
task status, integration, approvals, and the final answer. Workers report
structured results; they never edit the shared progress record.

Give every write lane exclusive file or component ownership. For overlapping
write surfaces, either sequence the tasks, assign the shared surface to one
contract owner, or use isolated worktrees and an explicit merge order. Central
manifests, lockfiles, schemas, generated indexes, and shared fixtures count as
overlap even when source files differ.

When writers use isolated worktrees, include the absolute worktree path and
branch ownership in each worker packet. The coordinator alone integrates those
branches and removes worktrees after verified integration.

## Dispatch bounded leaf workers

Prefer isolated context (`fork_turns: "none"`) and provide a self-contained
packet containing:

- goal and exact deliverable;
- owned paths or domain and explicit non-goals;
- dependency outputs and interface contracts;
- acceptance criteria and exact verification command;
- permitted side effects and escalation conditions; and
- required report: status, files or findings, evidence, concerns, and blockers.

Every packet must state: "You are a leaf worker. Do not spawn or delegate. Do
the assigned work yourself and return the completed deliverable in this turn;
do not return a promise of future results."

## Schedule for useful concurrency

Use the actual collaboration-tool slot limit. Keep the coordinator available
unless all remaining work is safely delegated. Among ready tasks, prioritize
the longest remaining critical path, then longer tasks, then lower coordination
risk. Fill only slots whose tasks can run without shared-write contention.

Dispatch independent ready tasks together. As each finishes, validate its
receipt, update coordinator-owned state, and immediately start the newly ready
highest-priority task when a slot is available. This is a work-conserving DAG
schedule, not a rigid wait-for-the-whole-wave barrier.

Do not poll workers repeatedly. Wait for completion or a meaningful status
change, and continue safe coordinator work while agents run.

## Verify and integrate

Reject status-only, unevidenced, or out-of-scope worker returns. Resume the same
worker for focused fixes when possible. Use an independent reviewer when the
cost of a defect justifies another context; do not duplicate reviews by default.

After integrating all lanes:

1. inspect the combined diff or synthesized result;
2. run cross-lane and full-scope verification;
3. check every acceptance criterion and unresolved worker concern;
4. run `$verification-before-completion`; and
5. report completed, blocked, and deliberately deferred work distinctly.

Never claim optimality merely because every slot was busy. The successful
schedule is the narrowest safe graph that finishes the verified outcome with
the least critical-path delay and avoidable rework.
