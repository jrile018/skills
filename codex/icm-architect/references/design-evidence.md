# Research basis and limits

Reviewed 2026-09-20 (America/New_York). These are primary sources; recommended agent policies are design inferences, not claims that OS benchmarks predict LLM performance. No single OS is universally most efficient: throughput, tail latency, energy, isolation, hardware, and workload can favor different policies. Implementation-level GitHub research and delivery policies: [efficient retrieval](efficient-retrieval.md).

## Hardware and operating systems

- **CPU cache vs OS policy.** Linux exposes supported cache-allocation/monitoring controls through [resctrl](https://docs.kernel.org/filesystems/resctrl.html). This is not general software control over every cache-line replacement. The useful transfer is explicit budgets and interference awareness, not literal L1/L2/L3 prompt tiers.
- **Locality vs parallelism.** Apple's [Clutch/Edge scheduler design](https://github.com/apple-oss-distributions/xnu/blob/main/doc/scheduler/sched_clutch_edge.md) discusses cluster placement, efficiency, and shared-cache locality tradeoffs. Inference: keep related analysis together, but delegate independent slices when coordination cost is justified.
- **Working sets.** Denning's [working-set paper](https://denninginstitute.com/pjd/PUBS/WSModel_1968.pdf) motivates locality and thrashing detection. Inference: retain decisive evidence and stop repeated retrieval/re-derivation. Tokens are unequal semantic objects, not uniform memory pages.
- **Memory placement is distinct from caching.** Linux [NUMA memory policy](https://docs.kernel.org/admin-guide/mm/numa_memory_policy.html) concerns where memory is allocated. [Transparent huge pages](https://docs.kernel.org/admin-guide/mm/transhuge.html) address page/translation behavior. Neither licenses describing all memory optimizations as L3 cache control.

## Reuse, correctness, and state

- [TinyLFU](https://arxiv.org/abs/1512.00727) studies cache admission based on reuse information. Inference: admit context for relevance/reuse, but keep that separate from validity. High hit rate does not imply truthful or fresh evidence.
- Feldman's [Make](https://grosskurth.ca/bib/1979/feldman-man.pdf) supplies dependency-driven rebuilding. Inference: invalidate results through source/configuration dependencies. Undeclared dependencies remain a blind spot.
- [SEDA](https://www.cs.cmu.edu/afs/cs/academic/class/15712-f08/www/readings/Welsh01.pdf) uses staged queues and resource control. Inference: bound queued searches/worker fanout; don't accumulate unreviewed leads indefinitely. Service-throughput results are not agent-accuracy results.
- [ARIES](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging) separates transaction recovery mechanisms. Inference: checkpoints preserve work; completion requires validation. Markdown is not a transaction manager.
- [Optimistic concurrency control](https://www.eecs.harvard.edu/~htk/publication/1981-tods-kung-robinson.pdf) motivates validating read dependencies before publishing private work. [Isolation-level analysis](https://www.microsoft.com/en-us/research/publication/a-critique-of-ansi-sql-isolation-levels/) warns that isolation assumptions matter. Inference: check shared invariants, not only overlapping filenames; a hash check is not serializability.

## Retrieval and context

- The original [ICM paper](https://arxiv.org/html/2603.16021) motivates small routing files, stage contracts, editable handoffs, and scoped context. Its example token ranges and practitioner reports are not controlled evidence that this code-analysis extension improves vulnerability detection or all models.
- [Lost in the Middle](https://arxiv.org/abs/2307.03172) reports position-sensitive performance on its long-context tasks. [RULER](https://arxiv.org/abs/2404.06654) evaluates effective context on multiple synthetic tasks. Inference: measure usable context on the actual task; maximum context capacity is not guaranteed comprehension.
- [RepoCoder](https://aclanthology.org/2023.emnlp-main.151/) supports iterative repository retrieval on code-completion benchmarks. It does not establish universal bug-finding gains or an optimal stopping rule. Inference: bounded retrieval/refinement with explicit unresolved edges, not endless self-review.

## Code analysis and domain correctness

- The [ripgrep guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md) documents search/filter behavior; [Tree-sitter queries](https://tree-sitter.github.io/tree-sitter/using-parsers/queries/1-syntax.html) provide syntactic structure; [SCIP](https://scip-code.org/) provides symbol-index interchange. Inference: escalate from lexical candidates to syntax and identity without conflating them with execution.
- The original [code property graph paper](https://www.mlsec.tu-berlin.de/docs/2014-ieeesp.pdf) combines syntax, control, and dependence information for vulnerability analysis. [CodeQL path queries](https://codeql.github.com/docs/writing-codeql-queries/creating-path-queries/) and [partial-flow debugging](https://codeql.github.com/docs/writing-codeql-queries/debugging-data-flow-queries-using-partial-flow/) motivate path-backed claims and investigating missing edges. Language/framework models bound coverage.
- [Soundiness](https://research.google/pubs/in-defense-of-soundiness-a-manifesto/) discusses practical static-analysis assumptions. Inference: document an analysis envelope; a clean scanner result is not proof of safety.
- [OpenLineage field lineage](https://openlineage.io/docs/spec/facets/dataset-facets/lineage/) motivates tracing output fields to inputs. [dbt data tests](https://docs.getdbt.com/reference/resource-properties/data-tests) supply concrete uniqueness/relationship checks. Inference: add domain grain/cardinality contracts; lineage metadata alone does not prove arithmetic correctness.
- [UCUM](https://unitsofmeasure.org/ucum) supplies unit semantics. Inference: track dimensions and conversions, with additional contracts for currency, scale, time, and business meaning that UCUM alone does not settle.
- AWS's [idempotent API design](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) explains retry-safe request identity and side-effect handling. Inference: distinguish event identity from delivery attempts and check atomic deduplication.
- [ArchUnit](https://www.archunit.org/userguide/html/000_Index.html) demonstrates executable dependency/architecture rules. Inference: turn observed boundary constraints into proportionate checks when implementation is authorized; structural tests cannot capture all runtime topology.

## Deliberate exclusions

No universal token budget, automatic full-repository embedding, mandatory graph database, automatic production probing, unsupported fastest-OS ranking, or automatic caching of unverified summaries. No new background scheduler, privileged hardware tuning, or remote data export is required. Measure this skill with [evaluation.md](evaluation.md), including regressions and false positives, before making performance claims.
