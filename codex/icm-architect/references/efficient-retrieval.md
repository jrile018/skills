# Efficient information delivery: implementation lessons

Read for repeated retrieval, working-set compaction, or indexing decisions, not for every code question. Research accessed 2026-09-20 (America/New_York). GitHub links below are moving branches, not pinned releases. Policies are adaptations; no external code is copied or installed by this skill.

## Default policy: selective, diverse, source-backed

1. Start from task anchors: concrete symbols, endpoints, fields, errors, tests, and changed interfaces.
2. Generate candidates with selective exact literals/path filters, then symbol/structural/semantic search where useful. Inspect exclusions. A query with zero hits is a retrieval observation, not an absence proof.
3. Rank by direct relevance, resolved dependency proximity, unresolved risk, evidence authority, and novelty relative to what is already read. Avoid decorative scores without measured inputs.
4. Reserve space for boundary/configuration/test evidence and a disconfirming path. A rarely referenced plugin, migration, or permission check may matter more than a central utility. Popularity and graph rank are priors, not verdicts.
5. Pack coherent source spans: signature, relevant body, guards, error path, schema/units, and source identity. Do not cut at arbitrary token boundaries or omit the guard to fit a budget. Deduplicate identical excerpts, not distinct behavior that looks similar.
6. After each retrieval round, ask what uncertainty it resolved. Continue only for a named missing edge or acceptance check; otherwise report the frontier. Track candidate-to-useful-evidence ratio, repeat reads, uncovered paths, and token/tool/time cost when available.

This is query planning plus an evidence budget, not a requirement to implement a search engine. Use `rg` for small/one-off slices. An existing maintained index pays off only when repeated query savings exceed build/update/storage and coverage costs.

For explicitly bounded acquisition, see the optional [source reader](source-reader.md). Continue unread ranges when the claim needs them; otherwise carry them as frontier. On compaction retain task/authority, decisive source identities, guards/units, rejected alternatives, unresolved edges and next action. Link cold detail rather than summarizing summaries. Revalidate on reuse using [runtime freshness](runtime-model.md).

## GitHub implementation research

### Aider: graph-ranked repository maps

[aider/repomap.py](https://github.com/Aider-AI/aider/blob/main/aider/repomap.py), especially `get_ranked_tags` and `get_ranked_tags_map_uncached`, extracts definition/reference tags, builds a weighted file graph, personalizes ranking toward task/chat identifiers, and fits rendered material to a token budget. [License: Apache-2.0](https://github.com/Aider-AI/aider/blob/main/LICENSE.txt).

Adopt task anchors, ranking, and bounded packing. Add boundary diversity and retain evidence references. Do not confuse name-based references with resolved dispatch, or implement PageRank merely to answer one question. Automated graph extraction/ranking requires runtime tooling; the selection policy can be applied manually.

### Tree-sitter: reuse unchanged syntax

[parser.c](https://github.com/tree-sitter/tree-sitter/blob/master/lib/src/parser.c) (`ts_parser__reuse_node`) checks subtree reuse conditions; [api.h](https://github.com/tree-sitter/tree-sitter/blob/master/lib/include/tree_sitter/api.h) exposes tree edits and changed ranges. [License: MIT](https://github.com/tree-sitter/tree-sitter/blob/master/LICENSE).

With a trustworthy incremental parser, re-extract syntax artifacts only for affected ranges and enclosing structures. Preserve parser/grammar identity and edit coordinates. Changed syntax ranges do NOT bound semantic impact: an unchanged caller may depend on a changed definition elsewhere. Invalidate semantic conclusions through their dependencies; fall back to file/cluster reanalysis on parse errors or missing edit state. This optimization needs parser/runtime support, not Markdown instructions alone.

### Zoekt: selective candidate generation, then verification

[index/indexdata.go](https://github.com/sourcegraph/zoekt/blob/main/index/indexdata.go) (`iterateNgrams`, `findSelectiveNgrams`) uses positional ngram postings to prune candidates and verify matches; its [design](https://github.com/sourcegraph/zoekt/blob/main/doc/design.md) explains indexing tradeoffs. [License: Apache-2.0](https://github.com/sourcegraph/zoekt/blob/main/LICENSE).

Prefer rare required literals plus appropriate repo/language/path filters before costly regex/semantic work. Keep candidate-generation separate from source verification. Short/common patterns, dynamic names, index omissions, and stale shards constrain results. Track skipped coverage as well as speed. A real index has construction/update/storage costs; this skill does not claim Zoekt's implementation speeds for manual searches.

### Salsa: demand-driven incremental queries

[maybe_changed_after.rs](https://github.com/salsa-rs/salsa/blob/master/src/function/maybe_changed_after.rs) and its [algorithm](https://github.com/salsa-rs/salsa/blob/master/book/src/reference/algorithm.md) validate memoized query dependencies and support retaining result change identity when recomputation gives an equal result. [License metadata: Apache-2.0 OR MIT](https://github.com/salsa-rs/salsa/blob/master/Cargo.toml).

For an existing analysis runtime, key pure results by repository, source/config/tool version, query parameters, and access scope. Record actual dynamic reads, including negative discovery inputs. Recompute on invalidation. Downstream reuse based on unchanged output is safe only for a typed, sufficiently complete contract with reliable equality. Equal prose summaries are NOT proof of semantic equivalence; refresh citations and never suppress security/numeric revalidation because a summary looks unchanged. Hidden time/network/filesystem reads break purity. Full dependency tracking is infrastructure, not a feature this skill claims to implement.

### CodeQL: precision-aware numeric analysis

[SimpleRangeAnalysis.qll](https://github.com/github/codeql/blob/main/cpp/ql/lib/semmle/code/cpp/rangeanalysis/SimpleRangeAnalysis.qll) computes supported expression bounds and uses widening to control recursive growth. [Guide](https://codeql.github.com/docs/codeql-language-guides/using-range-analsis-in-cpp/). [Query/library licensing](https://github.com/github/codeql/blob/main/README.md) is distinct from separately licensed CLI use.

For arithmetic/security claims backed by static analysis, record a precision envelope: supported types/operations, conversions, guards, interprocedural scope, widening/approximations, extraction errors, and unresolved models. A broad interval is not a demonstrated overflow; no reported path is not proof of safety. Check runtime availability and licensing before recommending private-code integration.

## Serving caches are a different layer

[PagedAttention](https://arxiv.org/abs/2309.06180) applies paging ideas to inference KV memory. [vLLM prefix caching](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/) can reuse prefix computation; its documented benefit concerns prefill, not eliminating output-token decoding. Those results do not imply that a filesystem summary cache changes GPU cache management.

[SGLang radix_cache.py](https://github.com/sgl-project/sglang/blob/main/python/sglang/srt/mem_cache/radix_cache.py) implements prefix matching, namespacing, protected references, and eviction (Apache-2.0 header). The useful separation is reusable stable prefixes versus request-specific suffixes, with explicit isolation. It needs a serving runtime; it cannot be activated by renaming Markdown folders.

If the host already supports prompt-prefix caching and exposes metrics, keep genuinely stable applicable instructions consistently ordered and put task-specific evidence after them without changing instruction priority. Never pad with irrelevant text to gain cache hits, share private context across access scopes, or claim cache savings without measured cached-token/latency data. Source-analysis memoization, retrieval indexes, and inference KV caching have different validity rules.

## Compression and language

Prefer lossless reductions first: remove duplicate payloads, use links/qualified symbols, keep concise contracts, move optional detail behind routing, and select the right evidence. A summary is lossy: retain exact units, guard conditions, exceptions, evidence identity, uncertainties, and a source pointer for recovery. Never replace a decisive source check with a summary of a summary.

[tiktoken](https://github.com/openai/tiktoken) uses encoding-specific tokenization; [encoding definitions](https://github.com/openai/tiktoken/blob/main/tiktoken_ext/openai_public.py) and [model mapping](https://github.com/openai/tiktoken/blob/main/tiktoken/model.py) make the dependency explicit (MIT). Character count and language alone do not establish token cost. Measure equivalent English, concise English, and Chinese using the target model's verified tokenizer before translating for savings. Preserve code identifiers/paths and human auditability. A proxy encoding or four sample passages does not establish the actual host's billed usage or universal language ranking.

## Adopt now vs optional infrastructure

Use task-anchor selection, coherent evidence spans, boundary diversity, precision envelopes, source versions, and measured stop rules now. Consider incremental AST extraction, indexed search, query memoization, graph ranking, or serving changes only when repeated workload measurements justify them and implementation is authorized. Validate [runtime freshness](runtime-model.md) independently of retrieval speed.
