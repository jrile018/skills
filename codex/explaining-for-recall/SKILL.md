---
name: explaining-for-recall
description: Use when the user asks for a simple, digestible, intuitive, memorable, exam-ready, or step-by-step explanation, especially after saying an earlier answer was confusing or incorrect.
---

# Explaining for Recall

## Principle

Optimize for the user being able to reproduce the reasoning unaided, not merely recognize a correct answer.

## Response Contract

Present the explanation in this order:

1. **Answer first:** one or two plain-language sentences stating the result.
2. **Intuition:** what the idea is doing and why it works, with minimal notation.
3. **Reusable rule:** the formula, decision test, or procedure that transfers to a new problem.
4. **Worked example:** one complete example with every non-obvious step shown.
5. **Memory hook:** a compact phrase, contrast, or mini-table.
6. **Recall check:** one short question the user can answer without rereading.

Define every symbol before using it. Keep algebra aligned vertically when transformations matter. If there are branches such as even versus odd, show the decision first and then the corresponding formula.

## Handling Corrections

When the user says an answer is wrong:

- acknowledge the exact disputed result;
- recompute from the original conditions rather than defending the prior path;
- identify the first step where the old reasoning diverged;
- give the corrected answer in the same reproducible structure.

When source material may itself be inconsistent, separate “what the source expects” from “what follows mathematically” and show the evidence for both.

## Quick Reference

| User need | Best shape |
|---|---|
| Exam preparation | Formula sheet, recognition cues, one timed-style example |
| Conceptual confusion | Analogy, invariant, then notation |
| Code understanding | Input → transformation → output with one trace |
| Wrong answer dispute | Fresh derivation and exact divergence point |
| Many similar problems | Decision table and reusable procedure |

## Example

For a Fourier-series parity question, begin with “even functions keep cosine terms; odd functions keep sine terms.” Then show how symmetry cancels the other coefficient, work one integral, and end with a two-row parity table.

## Common Mistakes

- Starting with a dense derivation before stating the idea.
- Giving a formula without recognition cues for when to use it.
- Skipping the step the user explicitly asked about.
- Adding multiple examples before the first one is fully explained.
