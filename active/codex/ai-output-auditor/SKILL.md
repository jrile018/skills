---
name: ai-output-auditor
description: Audit an AI-generated answer, research report, calculation, chart, code change, dependency, or tool-action plan for unsupported claims, hidden assumptions, incorrect computation, unsafe actions, and missing verification. Use when the user asks to check or review AI output before relying on it; auditing alone does not authorize fixes or execution.
---

# AI Output Auditor

Determine whether an AI-generated result is safe and justified enough for its intended use. Remain read-only unless the user separately asks for corrections or implementation.

## Scope the audit

Identify the artifact, its intended decision or action, the available source material, and the consequence of error. Separate:

- claims that can be checked against sources;
- inferences or recommendations;
- calculations and data transformations;
- code, commands, dependencies, downloads, and external actions;
- transcription or OCR;
- facts that remain unknown.

Read [references/audit-checks.md](references/audit-checks.md) and apply only the sections relevant to the artifact. Start with deterministic checks and high-impact failure modes rather than stylistic preferences.

## Audit principles

- Recompute exact results with an appropriate deterministic tool when possible.
- Inspect inputs, units, missing-data treatment, baselines, and intermediate values—not only the final number or chart.
- Open decisive citations and verify that they support the exact nearby claim.
- Treat model consensus and polished wording as weak evidence.
- For code or agent work, inspect the diff, executed or proposed commands, dependency provenance, network access, secrets exposure, licenses, tests, and rollback path.
- Confirm OCR and transcription before interpreting images, labels, tables, or audio.
- Scale scrutiny to stakes and clearly state what could not be verified.

Do not silently repair the artifact and then report it as correct. Preserve the distinction between the submitted output and any proposed remediation.

## Report findings first

Order findings by potential impact. For each finding, state the defect, evidence, consequence, and smallest useful remediation. Then summarize:

- overall reliability and confidence;
- checks performed and passed;
- checks not performed or blocked;
- assumptions the user must confirm;
- whether the artifact is usable as-is, usable with caveats, needs revision, or should not be relied upon.

If there are no material findings, say so without inventing concerns and still identify the verification boundary.
