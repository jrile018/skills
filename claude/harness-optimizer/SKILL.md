---
name: harness-optimizer
description: Agent harness performance optimization. Configure Sonnet as default model (~60% cost reduction), cap MAX_THINKING_TOKENS (~70% thinking cost reduction), route subagents to Haiku (~80% cheaper). Tunes settings.json, model selection, and subagent dispatch for maximum cost efficiency.
---

# Harness Optimizer

Optimize your Claude Code agent harness for cost and performance. Three levers: model selection, thinking budget, subagent routing.

## Activation

`/harness-optimizer` — Audit current setup and recommend optimizations.

## Three Optimization Levers

### 1. Default Model Selection (~60% cost reduction)

Most coding tasks don't need Opus. Sonnet handles well-defined work at ~1/5 the cost.

**When to use each model:**

| Model | Use For | Cost (approx) |
|-------|---------|---------------|
| Haiku | File reads, searches, validation, formatting | $0.25/$1.25 per M tokens |
| Sonnet | Code generation, test writing, refactoring, reviews | $3/$15 per M tokens |
| Opus | Architecture, debugging unknowns, novel problems | $15/$75 per M tokens |

**Recommendation:** Default to Sonnet for daily work. Escalate to Opus only for tasks requiring deep judgment. This alone cuts costs ~60% for most users.

**How to switch:**
- Use `/model sonnet` in Claude Code to change the active model
- Or set in your workflow: start with Sonnet, upgrade to Opus when stuck

### 2. Thinking Token Budget (~70% thinking cost reduction)

Extended thinking can consume massive hidden tokens. Cap it.

**The problem:** Uncapped thinking on a complex prompt can burn 10K-50K thinking tokens — often more than the visible output. You're paying for Claude's internal monologue.

**Strategies:**
- For routine tasks (code gen, tests, refactoring): thinking adds little value. Use Sonnet which has efficient built-in reasoning.
- For complex tasks (architecture, debugging): Opus with thinking is worth it, but set a budget.
- For validation/checking: Haiku with no extended thinking. Pure execution.

**Implementation:**
When using the API or configuring agents, set `max_tokens` on thinking:
- Routine: 1,024 tokens thinking budget
- Moderate: 4,096 tokens
- Complex: 16,384 tokens
- Never: unlimited (the default burns tokens)

### 3. Subagent Model Routing (~80% cheaper subagents)

Most subagent tasks are mechanical — they don't need the parent's model.

**Routing rules for Agent tool dispatch:**

```
Agent({
  model: "haiku",   // For: file research, enumeration, validation
  model: "sonnet",  // For: code generation, test writing
  // omit model     // For: inherits parent (Opus for complex work)
})
```

**Task-to-model mapping for subagents:**

| Subagent Task | Model | Savings vs Opus |
|---------------|-------|-----------------|
| Explore codebase | haiku | 98% |
| Search for patterns | haiku | 98% |
| Validate output | haiku | 98% |
| Generate code from spec | sonnet | 80% |
| Write tests | sonnet | 80% |
| Review code | sonnet | 80% |
| Architecture decisions | opus (inherit) | 0% |
| Debug novel issues | opus (inherit) | 0% |

### Combined Savings Example

Typical feature implementation session (before):
```
All Opus, uncapped thinking:
  Main conversation: 100K tokens @ $15/$75 = $8.25
  Thinking: 50K tokens @ $15 = $0.75
  3 subagents @ 30K each: 90K tokens @ $15/$75 = $7.43
  TOTAL: ~$16.43
```

After optimization:
```
Sonnet main + capped thinking + routed subagents:
  Main (Sonnet): 100K tokens @ $3/$15 = $1.80
  Thinking: 4K tokens @ $3 = $0.01
  2 Haiku subagents: 60K @ $0.25/$1.25 = $0.09
  1 Sonnet subagent: 30K @ $3/$15 = $0.54
  TOTAL: ~$2.44
```

**Savings: 85% ($13.99 saved per session)**

## Audit Workflow

When invoked, the optimizer:

1. **Check current model** — What model is active? Could it be downgraded?
2. **Review recent subagent usage** — Were Opus-level subagents used for Haiku-level tasks?
3. **Estimate thinking overhead** — Based on task complexity, is thinking budget appropriate?
4. **Check settings.json** — Any hooks or configs adding unnecessary overhead?
5. **Report** — Show current costs, recommended changes, projected savings

## Report Format

```
Harness Optimization Report
===========================
Current Setup:
  Model: opus (could be sonnet for 80% of tasks)
  Thinking: uncapped (recommend 4K cap for routine)
  Subagents: all inherit opus (recommend haiku/sonnet routing)

Estimated Current Cost: ~$16/session
Optimized Cost: ~$2.50/session
Potential Savings: 85%

Recommendations:
1. [HIGH] Switch to Sonnet for daily coding work
2. [HIGH] Route exploration/validation subagents to Haiku
3. [MED]  Cap thinking at 4,096 for routine tasks
4. [LOW]  Remove 3 unused MCP servers from config
```

## Quick Reference

```
Daily coding:    Sonnet + 1K thinking + Haiku subagents
Code review:     Sonnet + 4K thinking + Haiku subagents
Feature design:  Opus + 16K thinking + Sonnet subagents
Debugging:       Opus + 16K thinking + Haiku exploration
```
