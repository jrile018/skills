# Design Provenance

Load this reference only to audit, evaluate, or revise the policy.

## Source influence

The policy adapts the implementation-economy ideas in [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) at reviewed commit `e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156` (MIT license). The reusable ideas are:

- understand the task and code before minimizing;
- prefer required behavior, repository reuse, native capabilities, and existing dependencies before new machinery;
- preserve non-negotiable correctness and safety constraints; and
- pass an explicit policy mode to implementation subagents.

The wording and Codex packaging here are original to Ingenius. Upstream hooks, plugin machinery, sibling commands, and benchmark claims are not bundled.

## Evidence boundary

Ponytail's published benchmark is useful design evidence, not proof of a universal effect: it is repository- and model-specific, small-sample, and authored by the same project. This skill therefore makes no general token, quality, or line-count guarantee. Evaluate it against representative local tasks with at least:

1. required-behavior pass rate;
2. security and validation preservation;
3. changed lines and introduced concepts;
4. dependency and public-surface growth; and
5. review defects or follow-up fixes.

Accept fewer lines only when correctness is non-inferior. Use the guarded mode when the cost of silently dropping a requirement is high.
