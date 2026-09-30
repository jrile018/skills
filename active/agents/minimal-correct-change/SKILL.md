---
name: minimal-correct-change
description: Implement or refactor software with the smallest change that fully satisfies the requested behavior after inspecting the relevant code path. Use for ordinary feature work, bug fixes, cleanup, or subagent implementation where overengineering is a risk; not for research-only tasks, mathematical proofs, mandated architectures, or simplification that would weaken security, validation, accessibility, compatibility, data integrity, or required performance.
---

# Minimal Correct Change

Reduce accidental complexity without reducing the contract. Understand the task and the affected code path before deciding what can safely be omitted.

## Establish the contract

Write down:

- the requested behavior and acceptance criteria;
- repository instructions, existing interfaces, and compatibility constraints;
- security, validation, accessibility, data-integrity, latency, and operational requirements;
- the smallest relevant execution path and its existing tests; and
- uncertainties that could change the design.

Do not count a shorter diff as a better result when it hides a requirement or shifts complexity into an untested assumption.

## Choose a mode

- **Full** — ordinary implementation or refactoring. Apply the complete decision ladder.
- **Guarded** — migrations, security boundaries, financial correctness, concurrency, public APIs, or other high-consequence paths. Preserve defensive structure until tests establish that it is redundant.
- **Off** — research, proofs, source synthesis, requested architecture exploration, or any task where the user explicitly values completeness over implementation economy.

When delegating, state the mode. Do not make a worker infer it from the word “simple.”

## Use the decision ladder

For each proposed abstraction, dependency, configuration layer, or helper:

1. Remove work that is not required by the present contract.
2. Reuse a suitable repository pattern or existing function.
3. Prefer the language standard library or native platform capability.
4. Reuse an already accepted dependency before adding another one.
5. Express straightforward behavior directly when that remains readable and testable.
6. Add a new abstraction or dependency only for a concrete requirement, repeated variation, or verified operational need.

Stop at the first option that satisfies the entire contract. Do not compress nontrivial logic into clever expressions, duplicate logic to avoid a small shared abstraction, or delete validation merely because the happy path passes.

## Implement and verify

1. Make the narrowest coherent change.
2. Add or update the smallest runnable check that would fail without it.
3. Run focused checks, then the broader relevant suite in proportion to risk.
4. Review the diff for unnecessary files, new concepts, flags, dependencies, and public surface area.
5. Report what was changed, what complexity was avoided, the checks run, and any remaining risk.

This policy never authorizes edits, dependency installation, deployment, or destructive actions. Those permissions come from the user and the task owner.

## Subagent contract

A parent assigning this policy must include:

```text
Policy: minimal-correct-change
Mode: full | guarded | off
Required behavior: <acceptance criteria and invariants>
Allowed surface: <files or component>
Verification: <required checks>
Return: <change summary, tests, remaining risk>
```

The parent still owns domain routing and final synthesis. Read [references/design-provenance.md](references/design-provenance.md) only when auditing or maintaining this policy.
