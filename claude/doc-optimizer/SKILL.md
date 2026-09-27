---
name: doc-optimizer
description: Restructure project documentation for minimal token consumption at session startup. Reduces auto-loaded docs from ~11K to ~800 tokens by creating tiered doc structure with lazy-loading. Use when documentation bloat is eating context window.
---

# Documentation Token Optimizer

Restructure your project's documentation so Claude only loads what it needs. Reduce session startup from ~11,000 tokens to ~800 tokens.

## Activation

`/doc-optimizer` — Analyzes current project docs and restructures them.

## The Problem

Claude Code auto-loads all documentation at session start:
- CLAUDE.md (often bloated with history)
- Multiple doc files in .claude/
- Session notes, old learnings, stale context

This consumes thousands of tokens before you even ask a question.

## The Solution

Tiered documentation structure. Only 4 essential files auto-load (~800 tokens). Everything else is on-demand at zero token cost until accessed.

## Target Structure

```
your-project/
├── CLAUDE.md                    # Slim entry point (~450 tokens)
├── .claudeignore                # Prevents auto-loading of docs/
│
├── .claude/
│   ├── COMMON_MISTAKES.md       # Top 5 critical bugs only (~350 tokens)
│   ├── QUICK_START.md           # Daily commands (~100 tokens)
│   ├── ARCHITECTURE_MAP.md      # Structural overview (~150 tokens)
│   ├── completions/             # Archived tasks (0 tokens - never auto-loaded)
│   └── sessions/                # Historical work (0 tokens)
│
└── docs/
    ├── INDEX.md                 # On-demand directory
    ├── learnings/               # Topic-specific files (~500 tokens each, on-demand)
    └── archive/                 # Legacy docs (0 tokens)
```

## Workflow

### Step 1: Audit Current State
Read existing CLAUDE.md and all .claude/ docs. Measure approximate token count:
- Count words, multiply by 1.3 for token estimate
- Flag files >500 tokens
- Identify stale/duplicate content

### Step 2: Triage Content

| Content Type | Action |
|-------------|--------|
| Active project rules | Keep in slim CLAUDE.md |
| Top 5 bugs (>1hr debugging) | COMMON_MISTAKES.md |
| Daily commands | QUICK_START.md |
| Architecture overview | ARCHITECTURE_MAP.md |
| Completed task docs | Move to completions/ |
| Old session notes | Move to sessions/ |
| Historical learnings | Move to docs/learnings/ (one topic per file) |
| Stale/outdated content | Move to docs/archive/ or delete |

### Step 3: Write Slim CLAUDE.md

The new CLAUDE.md should contain ONLY:
- Project name and one-line description
- Tech stack (one line)
- Build/test/run commands
- 3-5 most critical rules
- Pointer: "Read .claude/COMMON_MISTAKES.md for known pitfalls"
- Pointer: "Read .claude/ARCHITECTURE_MAP.md for project structure"

Target: under 450 tokens.

### Step 4: Create .claudeignore

```
docs/
.claude/completions/
.claude/sessions/
```

### Step 5: Report Savings

```
Documentation Token Audit:
  Before: ~11,200 tokens at startup
  After:  ~800 tokens at startup
  Freed:  ~10,400 tokens (93% reduction)

  Files restructured: 12
  Files archived: 7
  Files deleted: 3
```

## Framework-Specific Patterns

### Express.js
Common mistakes: middleware ordering, async error handlers, env validation

### Next.js
Common mistakes: client/server boundary, dynamic imports, ISR cache

### Django
Common mistakes: N+1 queries, migration ordering, settings overrides

### React
Common mistakes: useEffect deps, stale closures, key prop in lists

## Maintenance Rules

1. Bug cost you >1 hour? Add to COMMON_MISTAKES.md (keep max 5, rotate oldest)
2. New daily command? Add to QUICK_START.md
3. Architecture changed? Update ARCHITECTURE_MAP.md
4. Finished a task? Move docs to completions/
5. Monthly: review and archive stale learnings

## Disable

Delete .claudeignore to restore full auto-loading. The restructured files still work fine either way.
