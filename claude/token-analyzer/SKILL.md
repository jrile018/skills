---
name: token-analyzer
description: Analyze token waste in your Claude Code setup. Finds unused skills, orphaned memory files, bloated MEMORY.md entries, stale reads, and duplicate prompts. Gives a quality score (S/A/B/C/D/F) tracking session degradation. Use when costs are high or sessions feel slow.
---

# Token Analyzer

Find where your tokens are going. Identify waste, measure quality degradation, checkpoint decisions before compaction destroys them.

## Activation

`/token-analyzer` — Full analysis of your current setup.

## Analysis Modules

### 1. Skill Waste Scanner

Check which installed skills are actually being used:

```
Scan: ~/.claude/skills/
Action: For each skill directory, check:
  - Was this skill invoked in the last 10 sessions? (check history.jsonl)
  - Is it referenced in any CLAUDE.md?
  - Does the description match any recent task patterns?

Report:
  ACTIVE:  caveman, lean-router, tdd (used 3+ times)
  IDLE:    slack-gif-creator, raffle-winner-picker (0 uses in 30 days)
  UNKNOWN: template-skill (no usage data)

Recommendation: Idle skills consume ~200-500 tokens each in the skill
list shown to Claude at session start. Consider removing unused ones.
```

### 2. Memory Orphan Detector

Check MEMORY.md index against actual memory files:

```
Scan: ~/.claude/projects/*/memory/
Action:
  - Parse MEMORY.md for file references
  - Glob all .md files in memory directory
  - Cross-reference

Report:
  INDEXED & EXISTS:  8 files (healthy)
  INDEXED & MISSING: 2 files (broken links - remove from MEMORY.md)
  EXISTS & UNINDEXED: 3 files (orphans - add to MEMORY.md or delete)
  STALE (>90 days):  4 files (review for relevance)
```

### 3. MEMORY.md Line Audit

Lines after 200 in MEMORY.md are truncated and never seen by Claude:

```
Scan: MEMORY.md line count
Report:
  Total lines: 247
  Visible (loaded): 200
  Truncated (wasted): 47 lines
  Action: Consolidate or remove entries to fit under 200 lines
```

### 4. Context Fill Estimator

Estimate current context window utilization:

```
Signals (weighted scoring):
  Context fill     (20%): How full is the context window?
  Stale reads      (20%): Files read but never referenced again
  Bloated results  (20%): Tool outputs >4KB that could be summarized
  Compaction depth (15%): How many times has context been compacted?
  Duplicates       (10%): Same file read multiple times
  Decision density  (8%): Ratio of decisions to total conversation
  Agent efficiency  (7%): Subagent output vs tokens consumed

Grade: S(90-100) A(80-89) B(70-79) C(60-69) D(50-59) F(0-49)
```

### 5. System Prompt Bloat Check

Analyze what's consuming tokens before you even start:

```
Estimate token costs of:
  - CLAUDE.md files (project + parent directories)
  - Loaded skills (description text in system prompt)
  - MCP server instructions
  - Memory system (MEMORY.md)
  - Hook configurations
  - Plugin metadata

Report:
  CLAUDE.md:        ~1,200 tokens
  Skills (12):      ~3,600 tokens (avg 300 each)
  MCP instructions: ~800 tokens
  Memory:           ~600 tokens
  Hooks:            ~200 tokens
  TOTAL OVERHEAD:   ~6,400 tokens per message

  Top consumers:
  1. skills/gsd-* (48 skills @ ~300 each = ~14,400 in skill list)
  2. CLAUDE.md (1,200 tokens - could be slimmed)
  3. MCP figma instructions (800 tokens)
```

### 6. Decision Checkpoint

Before compaction destroys context, save key decisions:

```
Checkpoint saved to ~/.claude/_backups/token-optimizer/
  - decisions.md: Key architectural decisions from this session
  - context-summary.md: What was being worked on
  - open-questions.md: Unresolved items
```

## Quality Score Interpretation

| Grade | Meaning | Action |
|-------|---------|--------|
| S | Excellent efficiency | Keep doing what you're doing |
| A | Good, minor waste | Review stale reads |
| B | Moderate waste | Clean up duplicates and bloated results |
| C | Significant waste | Restructure docs, remove unused skills |
| D | Heavy waste | Major cleanup needed |
| F | Critical | Session is degraded, consider fresh start |

## Quick Commands

- `/token-analyzer` — Full analysis
- `/token-analyzer skills` — Skill waste only
- `/token-analyzer memory` — Memory audit only
- `/token-analyzer grade` — Quality score only
- `/token-analyzer checkpoint` — Save decisions before compaction

## Output Format

```
Token Analysis Report
=====================
Quality Grade: B (74/100)

Skill Waste:     3 idle skills (~900 tokens/session)
Memory Orphans:  2 broken links, 3 unindexed files
MEMORY.md:       47 lines over limit (truncated)
System Overhead: ~6,400 tokens/message
Stale Reads:     4 files read but unused

Top 3 Recommendations:
1. Remove idle skills: slack-gif-creator, raffle-winner-picker
2. Fix MEMORY.md: remove 2 broken links, trim to <200 lines
3. Slim CLAUDE.md from 1,200 to ~450 tokens (use /doc-optimizer)

Estimated monthly savings: ~$180 (based on 30 sessions/day)
```

## Implementation Note

This skill runs 100% locally. Zero network calls. All analysis is done by reading local files and doing basic counting/matching. No telemetry, no external dependencies.
