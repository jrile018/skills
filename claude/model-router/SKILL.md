---
name: model-router
description: Use on EVERY prompt. Auto-routes subagent work to cheapest capable model (Haiku for search/read, Sonnet for codegen, Opus for architecture/judgment). No activation command needed — this skill is always active.
---

# Model Router (Always Active)

Route every subagent dispatch to the cheapest capable model. This is NOT optional — check the routing table before every Agent call.

## Routing Table

| Task | Model | Rationale |
|------|-------|-----------|
| File search, grep, glob, listing | **haiku** | Mechanical, no reasoning |
| Read files and summarize | **haiku** | Extraction only |
| Status checks, validation runs | **haiku** | Pass/fail reporting |
| Codebase exploration | **haiku** | Discovery, not judgment |
| Code generation (clear spec) | **sonnet** | Moderate reasoning |
| Test writing | **sonnet** | Pattern following |
| Bug fix (known root cause) | **sonnet** | Defined transformation |
| Refactoring (clear rules) | **sonnet** | Mechanical transform |
| Documentation generation | **sonnet** | Synthesis, not judgment |
| Code review | **sonnet** | Pattern matching |
| Architecture decisions | **opus** | Deep reasoning |
| Debugging (unknown cause) | **opus** | Investigation + insight |
| Security analysis | **opus** | Adversarial thinking |
| Novel algorithm design | **opus** | Creative reasoning |
| Multi-system integration | **opus** | Complex tradeoffs |
| Ambiguous requirements | **opus** | Judgment needed |

## Rules

1. **Default to the cheapest model that can do the job.** When in doubt between two tiers, start with the cheaper one.
2. **Never use Opus for search/read.** Haiku handles file exploration at 1/60th the cost.
3. **Main conversation stays on its current model.** Only subagents get routed.
4. **If a subagent fails or produces poor output, escalate** — retry with the next tier up.
5. **Never downgrade mid-task.** If Opus started a task, Opus finishes it.

## How to Apply

Before every `Agent()` call, add the `model` parameter:

```
Agent({
  model: "haiku",     // for search/exploration
  subagent_type: "Explore",
  prompt: "Find all files related to auth..."
})

Agent({
  model: "sonnet",    // for code generation
  prompt: "Implement the login endpoint..."
})

// Opus: just omit model (inherits parent) or set explicitly
Agent({
  model: "opus",      // for deep analysis
  subagent_type: "code-reviewer",
  prompt: "Review the security of..."
})
```

## Red Flags

If you're about to dispatch a subagent WITHOUT setting `model`, stop and classify:
- Is this a read/search? → haiku
- Is this codegen with a clear spec? → sonnet
- Does this need judgment? → opus
