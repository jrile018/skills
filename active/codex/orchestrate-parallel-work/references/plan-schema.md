# Dependency-aware plan schema

Use this schema when work may be delegated. Omit fields only when they truly do
not apply.

```markdown
### T1: <checkable deliverable>

- depends_on: []
- owns: [<exclusive paths, component, or research domain>]
- non_goals: [<nearby work this task must not absorb>]
- consumes: [<artifact or interface supplied by a predecessor>]
- produces: [<artifact or stable interface successors may rely on>]
- acceptance: [<observable completion conditions>]
- verification: `<exact command or concrete evidence>`
- estimate: <relative duration: S, M, or L>
- coordination_risk: <safe, low, moderate, high>
- status: <pending, running, review, complete, blocked>
```

## Graph checks

Before dispatch:

1. Every dependency names an existing task.
2. The graph is acyclic.
3. Every requested outcome maps to at least one task.
4. Every produced interface has one owner.
5. Concurrent tasks have disjoint write surfaces or isolated worktrees.
6. A dependent task is not ready until all hard predecessors are verified.
7. Soft ordering preferences are not encoded as hard dependencies.

Split only where each task has an independently checkable deliverable. Merge
tiny tasks whose dispatch and review cost would exceed their execution cost.

## Scheduling heuristic

For each task, estimate remaining critical-path weight as its own duration plus
the largest weight among its successors. When a slot opens, choose from the
ready set in this order:

1. largest remaining critical-path weight;
2. longer estimated duration;
3. lower coordination risk;
4. task that unlocks the most successors.

This heuristic aims to reduce elapsed time without pretending that arbitrary
agent work has perfectly known durations.

## Coordinator state

Only the coordinator changes `status` or the shared ledger. A worker returns:

```text
STATUS: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
OUTPUTS: paths, commits, or findings
VERIFICATION: command and result, or evidence
CONCERNS: none or concise list
```

The coordinator marks a task complete only after checking the promised output
and verification evidence. A worker's completion claim is an input to review,
not the final state transition.
