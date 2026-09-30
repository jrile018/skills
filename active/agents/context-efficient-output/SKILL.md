---
name: context-efficient-output
description: Produce compact agent messages, handoffs, progress updates, and technical summaries while preserving exact facts needed for verification and continuation. Use when output or cross-agent context should be shorter or cheaper; not for a requested detailed tutorial, complete logs, exhaustive evidence, or compression that would hide assumptions, source limits, proof conditions, safety warnings, errors, commands, paths, or numerical results.
---

# Context-Efficient Output

Compress presentation, not truth. Preserve the information another person or agent needs to verify the result, continue the task, or detect a bad assumption.

## Select a mode

- **Compact** — default for routine worker receipts, progress updates, and implementation summaries.
- **Detailed** — source-sensitive research, proofs, incident analysis, high-risk decisions, or user-requested explanation. Remove repetition but retain the reasoning chain and evidence boundary.
- **Exact** — logs, errors, commands, code, schemas, measurements, quotations, or protocol data whose literal form matters.

An explicit user request for detail wins. Never use a context budget as a reason to omit a material caveat.

## Preserve the continuation contract

Before shortening, identify and retain:

- the goal, status, and observable completion condition;
- decisions made and the rationale that constrains future work;
- assumptions, dates, units, versions, and source or evidence limits;
- exact file paths, symbols, commands, error text, code, and measured values when relevant;
- permissions, safety boundaries, blockers, and unresolved uncertainty; and
- named artifacts handed to downstream work.

Then remove duplicated narration, replace repeated prose with a small schema or table, link to durable artifacts instead of restating them, and lead with the result.

## Handle source context safely

Output summarization and source transformation are different operations. If source material itself would be shortened:

1. keep the original in an authorized, retrievable location;
2. label the summary as lossy and identify the original artifact;
3. preserve exact spans that downstream checks require;
4. verify retrieval before discarding working context; and
5. retain the original unchanged when recovery or fidelity cannot be established.

This skill does not provide a proxy, database, compression engine, telemetry, or recovery service. Do not install hooks, send context externally, or claim reversible compression unless a separately authorized runtime actually supplies and verifies it.

## Measure net value

Shorter text is not automatically cheaper or better. For repeated workflows, compare the compact and normal variants using provider-billed tokens when available, total latency, answer correctness, missing-fact rate, and recovery failures. Include routing and compression overhead. Fall back to the original representation when savings are negative or correctness degrades.

## Worker receipt

For a delegated task, prefer:

```text
Status: complete | blocked | partial
Result: <bounded answer or artifact>
Evidence: <checks, sources, or measurements>
Assumptions: <material assumptions>
Risks: <remaining uncertainty or none>
Handoff: <exact artifact and next consumer, or none>
```

The parent owns synthesis and may request detail. Read [references/design-provenance.md](references/design-provenance.md) only when auditing or maintaining this policy.
