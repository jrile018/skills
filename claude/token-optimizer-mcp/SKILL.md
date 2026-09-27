---
name: token-optimizer-mcp
description: MCP-based token optimization achieving 95%+ token reduction through intelligent caching, response compression, and smart tool dispatch. Use when working with MCP servers that produce large outputs or when tool results are repetitive across sessions.
---

# Token Optimizer MCP

Intelligent token optimization through caching, compression, and smart tool intelligence. Targets 95%+ token reduction on repetitive MCP tool interactions.

## Activation

`/token-optimizer-mcp` — Analyze MCP tool usage and apply optimizations.

## Three Optimization Strategies

### 1. Response Caching

Cache tool results that are unlikely to change between calls:

**Cache-friendly (safe to cache):**
- File structure listings (cache 5 min)
- Package.json / config file reads (cache until file changes)
- API schema definitions (cache 1 hour)
- Git log output (cache until new commit)
- Search results for same query (cache 2 min)

**Never cache:**
- File content reads (may be edited)
- Git status/diff (changes constantly)
- Runtime state (process lists, server status)
- Anything with side effects

**Implementation pattern:**
Before making an MCP tool call, check:
1. Have I called this exact tool with these exact params recently?
2. Is the result likely to have changed?
3. If no change expected, reuse the previous result.

### 2. Response Compression

Large tool outputs waste context. Compress before consuming:

**Compression strategies by output type:**

| Output Type | Strategy | Reduction |
|------------|----------|-----------|
| Directory listings | Show structure, omit node_modules/dist | 80-90% |
| Git log | Show last 10 commits, summarize rest | 70-80% |
| Test output | Show failures only, count passes | 90-95% |
| Build output | Show errors/warnings only | 85-95% |
| Large file reads | Show relevant sections + line numbers | 60-80% |
| API responses | Extract fields needed, drop metadata | 70-90% |

**Implementation:**
When a tool result exceeds 4KB:
1. Identify the output type
2. Apply appropriate compression strategy
3. Preserve all actionable information (errors, warnings, paths)
4. Drop noise (success messages, progress bars, verbose logs)

### 3. Smart Tool Intelligence

Optimize which tools get called and when:

**Avoid redundant calls:**
- Don't re-read a file you just wrote (you know the content)
- Don't glob for a file path you already have
- Don't grep after reading the whole file (search your memory)
- Don't run git status after every single edit

**Batch where possible:**
- Instead of 5 separate file reads, use one Agent to read all 5
- Instead of grep + glob + read, use one targeted search
- Combine related MCP tool calls into one operation

**Prefer cheaper alternatives:**
- Glob before Grep (file existence is cheaper than content search)
- Read specific line ranges instead of whole files
- Use `head_limit` on Grep to avoid massive result sets

## Analysis Workflow

When invoked:

1. **Audit MCP servers** — List configured servers and their tool counts
2. **Check for unused servers** — Any MCP servers with 0 tool calls in recent sessions?
3. **Identify repeat calls** — Same tool + same params called multiple times
4. **Measure output sizes** — Which tools produce the largest outputs?
5. **Recommend caching** — Which results are safe to cache?
6. **Report** — Show waste and savings potential

## Report Format

```
MCP Token Optimization Report
==============================
Configured MCP Servers: 4
  figma:      12 tools (used 3 in last 7 days)
  claude-mem: 14 tools (used 8 in last 7 days)
  gmail:       2 tools (used 0 — consider removing)
  calendar:    2 tools (used 0 — consider removing)

Repeat Call Analysis (last session):
  Read same file 3x:     ~4,500 tokens wasted
  Grep same pattern 2x:  ~1,200 tokens wasted
  Git status 8x:         ~2,400 tokens wasted
  TOTAL REPEAT WASTE:    ~8,100 tokens

Large Output Analysis:
  git log (full):        ~3,200 tokens (compress to ~800)
  npm test output:       ~5,600 tokens (compress to ~200)
  Directory listing:     ~2,100 tokens (compress to ~400)
  COMPRESSION SAVINGS:   ~9,500 tokens

Recommendations:
1. Remove unused MCP servers (gmail, calendar) — saves ~400 tokens/session overhead
2. Cache config file reads — saves ~2,000 tokens/session
3. Compress test/build output — saves ~5,000 tokens/session
4. Avoid re-reading files just written — saves ~3,000 tokens/session

Total Potential Savings: ~10,400 tokens/session (estimated 60-70% reduction)
```

## Best Practices

1. **Prune MCP servers** — Each configured server adds overhead to every message (tool descriptions in system prompt). Remove servers you don't use regularly.
2. **Batch operations** — Use subagents to batch related MCP calls instead of sequential individual calls.
3. **Set head_limit** — Always set `head_limit` on Grep to avoid unbounded results.
4. **Read specific ranges** — Use `offset` and `limit` on Read to get only the lines you need.
5. **Trust your memory** — If you just wrote a file, don't re-read it. You know what's in it.
