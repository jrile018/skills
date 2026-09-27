---
name: claude-code-insights
description: Apply architectural lessons from Claude Code internals — multi-agent orchestration, persistent memory (autoDream), tool safety, and query-engine retry patterns. Use when designing AI agent systems, tuning Claude Code setup, or advising on cost/reliability.
---

# Claude Code Internals — Applied Lessons

Five load-bearing insights distilled from a direct read of the Claude Code source (`coordinator/`, `services/autoDream/`, `Tool.ts`, `tools/`, `main.tsx`, `QueryEngine.ts`). Apply these when designing your own agent systems or optimizing Claude Code usage.

## 1. Orchestration: the LLM is the router

There is no "swarm router." The top-level Claude dispatches specialists via the `Agent` tool with `subagent_type`. Fork mode (omit `subagent_type`) inherits parent context + system prompt verbatim for cache-byte identity; fresh mode loads the specialist's own system prompt with ZERO inherited conversation.

**Apply:**
- Never build a classifier agent. Let the coordinator LLM route.
- Specialists differ by (system prompt, tool allowlist, model, `omitClaudeMd`). Not class hierarchy.
- Results return as full-transcript text in `<task-notification>` blocks, not summaries.

## 2. Memory: 4-phase prompt over heuristics

AutoDream runs as a fire-and-forget background agent on session stop, gated by time (24h) and session count (5). It reads session JSONL transcripts + existing memory files, then runs a 4-phase consolidation prompt: **Orient → Gather signal → Consolidate → Prune & index**. Pruning is LLM-judgment, not age-based. Only hard rule: MEMORY.md capped at 200 lines / 25 KB.

**Apply:**
- For long-horizon memory, offload consolidation to a forked sub-agent with restricted filesystem tools.
- Size-cap the index file; let the LLM handle semantic pruning.
- Standard file naming: `user_*.md`, `project_*.md`, `feedback_*.md`, `reference_*.md`.

## 3. Tool safety: Zod parse + error-as-message

Every tool declares a Zod `strictObject` schema. Validation is post-hoc `safeParse`. On failure, the engine does NOT retry the call — it inserts a `tool_result` block with `is_error: true` and `<tool_use_error>InputValidationError: ...</tool_use_error>`, then lets the model self-correct on the next turn. Bound only by `maxTurns`.

**Apply:**
- Schema-first tool definitions. Feed schema to LLM + validate at call site.
- Recover via conversation, not code retry.
- Bash safety: regex pattern-denylist (command substitution, Zsh dangerous modules, process substitution) + path allowlist + intentional skip of symlink resolution.

## 4. Streaming UI: external store beats useState

Ink + React + Commander.js. Top-level `<App>` wraps a Zustand-style store via `useSyncExternalStore`. Non-React code (query engine, tool executors) calls `store.setState()` directly; React components subscribe. Async iterators from the LLM stream drive `setMessages` via `for await` + callback. No event bus, no Redux.

**Apply:**
- For streaming terminal UI: external mutable store + `useSyncExternalStore` subscription. Avoids provider re-render cascades.
- Ink `<Box>/<Text>` + `useAnimationFrame` covers most terminal UX needs.

## 5. Resilience: exponential backoff + auto-fallback

429/529 retries use exponential backoff (cap 32s, 5min in unattended mode) for up to 10 attempts; Retry-After honored. Three consecutive 529s on Opus → auto-fallback to Sonnet via `FallbackTriggeredError`, orphaned tool_use blocks yielded as tombstones.

**Apply:**
- Don't retry malformed-JSON calls. Emit `is_error` tool_result and let the model self-correct.
- Auto-fallback on persistent overload (3+ consecutive 529s), not on network blips.
- Budget via `maxTurns` on the agent loop, not a retry counter.

## Quick checklist for optimizing your own Claude Code setup

1. Enable OTEL cache telemetry to see hit rate (env vars below).
2. Treat CLAUDE.md as immutable mid-session — every edit invalidates downstream cache.
3. Audit `~/.claude/skills/` — every skill adds to session-start system prompt.
4. Pick ONE memory system (autoDream OR claude-mem), not both.
5. Every `Agent()` call gets an explicit `model` param, weighted toward haiku.
6. Write self-contained briefs with JSON output schema; cap response word counts.
7. Parallel subagents: 3–5 concurrent max, non-overlapping file boundaries.
8. Seed MEMORY.md topic files manually when onboarding a new project — autoDream only fires after 5 sessions.

## Telemetry setup

```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
```

The custom statusline reads `cache_read_input_tokens` from the transcript tail and renders `↻N%` — cache hit share of total input.
