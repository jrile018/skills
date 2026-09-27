---
name: auditing-project-truth
description: Use when determining what is actually implemented, missing, stale, assigned, merged, or deployed across repositories, branches, pull requests, issues, roadmaps, or dashboards.
---

# Auditing Project Truth

## Principle

An audit is a reconciliation of claims against authoritative evidence. Never collapse local code, remote Git state, issue-tracker state, documentation, and runtime behavior into one unlabeled conclusion.

## Evidence Order

Use the most authoritative source available for each claim:

1. Runtime or user-visible behavior for “works now.”
2. Remote branch, pull request, or release state for “merged” or “shipped.”
3. Exact repository files and tests for “implemented.”
4. Live issue tracker for ownership, status, and acceptance criteria.
5. Documentation for intended architecture, not proof of implementation.

Record timestamps or commit identifiers when freshness matters. Fetch or browse only when needed; do not overwrite local work to make an audit convenient.

## Audit Contract

Build one row per requirement, issue, or user-visible capability:

| Item | Owner/repository | Claimed state | Evidence | Verified state | Gap/next action |
|---|---|---|---|---|---|

Allowed verified states are `done`, `partial`, `missing`, `blocked`, and `not verifiable`. A plan, stub, screenshot, or passing unit test is not automatically `done`.

For cross-repository systems, trace the full handoff: producer, transport or API, consumer, and visible result. Assign a gap to the component that must change, not merely the repository where it was noticed.

## Output Order

1. Bottom-line verdict.
2. Highest-impact gaps.
3. Evidence matrix.
4. Recommended sequence of fixes or issue updates.
5. Uncertainties requiring access or user input.

## Example

If an issue says a manual position edit is complete, verify the issue’s acceptance criteria, the backend mutation, the frontend control, the remote branch containing both, and the visible state refresh. Mark it `partial` when only the API exists.

## Common Mistakes

- Treating a local checkout as current remote truth.
- Guessing repository ownership from naming alone.
- Calling code complete because a document describes it.
- Hiding uncertainty instead of using `not verifiable`.
- Updating issue state without evidence or explicit authorization.
