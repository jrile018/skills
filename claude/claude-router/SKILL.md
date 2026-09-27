---
name: claude-router
description: Intelligent model orchestration — automatically routes queries to optimal Claude model (Haiku/Sonnet/Opus) based on complexity classification. Zero-latency rule-based routing with cost tracking. Reduces costs up to 80%.
---

# Claude Router

Intelligent model orchestration. Routes each query or subtask to the optimal Claude model based on complexity analysis.

## Activation

- `/claude-router` or `/route` — Enable auto-routing for the session
- `/route haiku|sonnet|opus` — Force a specific model for next task
- `/router-stats` — Show routing stats and cost savings for the session

## Complexity Classification

### Rule-Based (Zero Latency)

Classify before dispatching. No LLM call needed for classification.

**Haiku Indicators** (simple, mechanical):
- File reads, searches, listing, enumeration
- Grep/glob operations
- Status checks, validation runs
- Summarizing existing content
- Format conversions
- Simple Q&A about visible code

**Sonnet Indicators** (moderate reasoning):
- Code generation with clear spec
- Test writing
- Bug fixes with identified root cause
- Refactoring with defined transformation
- Documentation generation
- Code review (non-security)

**Opus Indicators** (deep reasoning):
- Architecture decisions
- Novel algorithm design
- Security analysis
- Debugging without clear root cause
- Multi-system integration design
- Ambiguous requirements needing judgment
- Performance optimization requiring tradeoffs

### Escalation Rules

- If Haiku produces low-confidence or incomplete output → retry with Sonnet
- If Sonnet struggles or output quality is poor → escalate to Opus
- Never downgrade mid-task (if Opus started, Opus finishes)

## Routing Commands

| Command | Effect |
|---------|--------|
| `/route` | Enable auto-routing |
| `/route haiku` | Force Haiku for next task |
| `/route sonnet` | Force Sonnet for next task |
| `/route opus` | Force Opus for next task |
| `/route auto` | Return to auto-routing |
| `/router-stats` | Show session routing statistics |

## Session Statistics

Track per session:
- Tasks routed per model tier
- Estimated tokens per tier
- Cost estimate vs all-Opus baseline
- Escalation count (Haiku→Sonnet, Sonnet→Opus)

## Implementation

When routing subagent work, use the Agent tool's `model` parameter:

```
Agent({
  model: "haiku",  // or "sonnet" or "opus"
  prompt: "...",
  description: "..."
})
```

For main-conversation work that needs Opus, just proceed directly (the parent is already Opus).

## Multi-Task Orchestration

For complex requests with multiple subtasks:

1. Decompose the request into independent subtasks
2. Classify each subtask
3. Present the routing plan:
   ```
   Task Routing:
   [H] Search codebase for auth patterns
   [H] List all API endpoints
   [S] Implement new endpoint
   [S] Write tests
   [O] Security review
   ```
4. Execute with appropriate models
5. Report savings

## Learning Mode

`/learn` — After task completion, evaluate whether routing was optimal:
- Was the model overpowered for the task? (wasted cost)
- Was the model underpowered? (poor output, needed escalation)
- Update routing heuristics for similar future tasks

## Cost Tracking Format

```
Session Routing Summary:
  Haiku:  12 tasks, ~15K tokens  ($0.02)
  Sonnet:  8 tasks, ~40K tokens  ($0.72)
  Opus:    2 tasks, ~10K tokens  ($0.90)
  Total: $1.64
  All-Opus baseline: $4.88
  Savings: 66% ($3.24)
```

## Disable

Say "stop routing" or "route off" to disable and use default model for everything.
