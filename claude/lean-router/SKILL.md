---
name: lean-router
description: Decompose work into steps, assign cheapest capable model (Haiku/Sonnet/Opus) per step, add quality gates, persist plan, report savings. Use for any multi-step task to cut costs 50-95%. Haiku for exploration/validation, Sonnet for codegen, Opus for judgment calls.
---

# Lean Task Router

Plan tasks with optimal model routing. Break work into steps, assign each the cheapest capable model, add quality gates between stages, persist the plan, report savings.

## Activation

`/lean-router` or `/lean` — Analyzes your task and creates a routed execution plan.

## Workflow

1. **Understand** — Clarify what needs doing
2. **Gather Context** — Read files, check scope before planning
3. **Decompose & Assign** — Break into steps, assign models per routing table
4. **Stage** — Test on 1 representative item first, validate, then scale
5. **Present Plan** — Show structured breakdown with model mix and cost estimate
6. **Persist** — Save to `.lean-plan.md` for session continuity
7. **Execute** — Run steps sequentially with quality gates between stages
8. **Report** — Calculate savings vs all-Opus baseline

## Model Routing Table

| Task Type | Model | Why |
|-----------|-------|-----|
| Single file read (1-2 calls) | Direct (no subagent) | Overhead exceeds benefit |
| Multi-file research (3+ files) | Haiku | Read-only, no reasoning needed |
| Codebase mapping/enumeration | Haiku | Mechanical listing |
| Pattern recognition in code | Sonnet | Needs understanding, not judgment |
| Content extraction from large files | Haiku | Filter and summarize |
| Well-defined code generation | Sonnet | Clear spec, predictable output |
| Writing/updating tests | Sonnet | Follows existing patterns |
| Mechanical plan execution | Sonnet | Pre-defined steps, no ambiguity |
| Ambiguous/complex execution | Opus | Judgment calls required |
| Refactoring (clear transform) | Sonnet | Well-defined transformation |
| Architecture/design decisions | Opus | Deepest reasoning needed |
| Debugging novel problems | Opus | Requires investigation + insight |
| Validation/verification | Haiku | Execute and report pass/fail |

## Quality Gates

Between every stage transition, run a **Haiku validator**:
- Did the previous step produce expected output?
- Any errors, missing files, or unexpected results?
- Is the next step still appropriate given what we learned?

If a gate fails: stop, diagnose, re-plan that step (potentially upgrading model tier).

## Plan Format (.lean-plan.md)

```markdown
# Lean Plan: [Task Description]

## Steps
| # | Step | Model | Est. Tokens | Status |
|---|------|-------|-------------|--------|
| 1 | Research existing auth patterns | haiku | 2K | pending |
| 2 | Gate: verify patterns found | haiku | 500 | pending |
| 3 | Generate auth middleware | sonnet | 8K | pending |
| 4 | Gate: middleware compiles | haiku | 1K | pending |
| 5 | Write tests | sonnet | 5K | pending |
| 6 | Gate: tests pass | haiku | 1K | pending |

## Model Mix
- Haiku: 4 steps (22%)
- Sonnet: 3 steps (72%)
- Opus: 0 steps (0%)

## Estimated Savings
- All-Opus baseline: ~50K tokens @ $15/M = $0.75
- Routed plan: ~17.5K tokens @ blended $4/M = $0.07
- Savings: ~90%
```

## Subagent Dispatch

When executing, use the Agent tool with the `model` parameter:
- `model: "haiku"` for Haiku steps
- `model: "sonnet"` for Sonnet steps
- Opus steps run in the main conversation (no subagent needed)

## Staging Protocol

For bulk operations (e.g., "refactor 20 files"):
1. Run step on 1 file
2. Haiku gate: verify output quality
3. If pass: scale to remaining files (parallel if independent)
4. If fail: diagnose, adjust approach, retry on same file

## Cost Reference

Approximate per-million-token costs (as of 2026):
- Haiku: ~$0.25 input / $1.25 output
- Sonnet: ~$3 input / $15 output
- Opus: ~$15 input / $75 output

## Typical Savings by Task Type

| Task | Savings vs All-Opus |
|------|-------------------|
| Pure research | 85-95% |
| Research + implementation | 75-85% |
| Bulk refactoring | 70-85% |
| Feature implementation | 50-70% |
| Complex debugging | 30-50% |

## Disable

The plan persists in `.lean-plan.md`. Delete the file or say "skip lean" to bypass routing.
