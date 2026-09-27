# Evaluate the method, not its promises

Before claiming better speed/accuracy, compare representative tasks against the prior skill (and optionally no skill) using the same model, settings, tools, source snapshot, task prompt, and budget. Use fresh contexts and blinded answer keys. A hand-picked synthetic example is a smoke test, not proof on large repositories.

Include comprehension, change impact, security, numeric lineage, runtime-cost hypotheses, stale maps, dirty trees, dynamic registration, interrupted/shared outputs, and benign controls. Challenge malicious repository instructions, untrusted architecture proposals, edited reports/sidecars, run-ID collisions, two sequential same-stage runs, and migration metadata/symlink/outbound-path handling. Use held-out tasks and more than one language/repository before generalizing. Preserve prior build/restructure behavior as a regression case.

Record:

- Correct findings and missed seeded defects; false positives on known benign controls. Report denominators.
- Evidence/path accuracy, uncertainty calibration, coverage/frontier, and unauthorized actions.
- Time to first useful answer and total time; input/output tokens, tool calls, file reads, repeated reads, context reloads if actually available. Unavailable metrics are unknown, not zero.
- Successful recovery/revalidation after source or human-output edits; isolated run identity.
- Tool failures and skipped checks. A passing hash helper does not establish analysis quality.

Human/adjudicator review decides whether a finding's evidence supports its claim. Keep policy ambiguity separate from defects. Count duplicate symptoms once per root cause while recording affected surfaces. Do not reward longer reports, more files opened, or more findings irrespective of correctness.

Choose context/retrieval budgets from the observed accuracy/cost tradeoff for the task class. Change one material policy at a time where feasible; avoid tuning on the held-out set. Regressions must be fixed or disclosed. Report small-sample uncertainty and do not invent a speedup when token/time telemetry is missing.
