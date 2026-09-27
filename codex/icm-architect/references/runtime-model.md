# Working sets, freshness, isolation, and recovery

Contents: Residence · Validity · Completion · Concurrency · Helper

## Residence is not validity

CPU caches, virtual memory, and database transactions inspire this design; none is a literal implementation of model context. ICM L0–L4 are semantic layers, not CPU L1/L2/L3. Hardware primarily manages CPU cache-line replacement/coherence; OS placement, scheduling, and supported resource controls influence locality/contention.

| Residence | Keep here | Admission/eviction |
|---|---|---|
| Active working set | Current task, permissions, constraints, decisive source/guards, local hypotheses | Admit when it answers an unresolved question. Never evict governing constraints for speed. |
| Run-local evidence | Source identities, proven paths, findings, frontier, checkpoints | Reuse only if relevant and valid; evicted excerpts retain pointers. |
| Shared navigation | Small catalogs and source-backed stable cards | Promote verified reusable knowledge; keep run-specific hypotheses separate. |
| Backing source | Code, schemas, configuration, authoritative records | Fetch on demand; don't replace with summaries. |

Prefer locality (same symbol, component, contract) but cross boundaries when evidence requires it. Repeated rereads, repeated searches for the same fact, or oscillating hypotheses signal thrashing: keep a small structured checkpoint in the answer, persist it only with write authority, finish one path, or split the task. More context or more agents is not automatically the remedy.

Bound queued searches and workers. Finish or reject weak leads before expanding the frontier indefinitely. Any token/file/time thresholds are task-specific budgets; reaching a limit preserves uncertainty rather than lowering evidence standards.

Optional incremental-query and serving-cache ideas have separate correctness conditions; read [efficient-retrieval.md](efficient-retrieval.md) only when optimizing repeated workloads. Matching summary text is not evidence that source semantics are unchanged.

## Validity and invalidation

Each reusable result identifies source root/revision, dirty inputs, read-set hashes, configuration/build variant, schema/generator/tool versions where relevant, and dependency scope. Line numbers, recency, cache hits, and HEAD alone do not establish freshness.

Track explicit dependencies including newly discovered dynamic wiring. File edits invalidate dependents; additions/removals in searched directories can invalidate absence and discovery claims even when previously read files are unchanged. Interface, schema, plugin/config, policy, or tool-model changes may invalidate a whole cluster. If dependencies are incomplete, conservatively re-discover the affected slice; do not invent a precise invalidation graph.

Before reuse/promotion, compare identities and fingerprints and reread decisive evidence. Human edits to source, intermediate inputs, or outputs are version changes. Upstream artifact changes invalidate downstream products transitively. A TTL is only a reminder to check, not a proof of freshness. A matching hash proves declared bytes, not meaning, runtime state, completeness, or safety.

Negative claims require a recorded search envelope and discovery inputs, not only a hash of matched files. Empty results without scope cannot be cached as "absent."

## Completion and recovery

Use the [run template](../assets/templates/run.md) for authorized substantial/resumable work; for a tiny or read-only task, equivalent evidence in the response is sufficient. Every repeatable run, sequential or concurrent, uses a fresh UUID/ULID or equivalent collision-resistant ID and create-new-only directory creation. On collision, select a new ID; never overwrite/reuse a previous run. One writer owns each artifact.

Lifecycle: `planned → running → validated → complete` (or `complete-with-limitations`); interruption yields `partial`; changed dependencies yield `stale`; missing required input/authority yields `blocked`. These are artifact states, not product automation/goal statuses.

A stage is consumable only when:

1. Run/stage and source/config identities match the intended inputs.
2. Declared dependency and output fingerprints match actual artifacts.
3. Acceptance checks have passed, with commands/results or source-only reasoning recorded.
4. Required approval exists for the exact version, if the contract calls for one.
5. Coverage/frontier and limitations are explicit; unresolved acceptance failures are not labeled complete.

Keep `report.md` (and other delivered outputs) separate from `completion.md`, using the [completion template](../assets/templates/completion.md). The sidecar hashes every delivered output including the report; it does not hash itself. Draft privately, validate, then publish the sidecar last with an atomic same-filesystem operation where supported. Treat published records as immutable; changed output creates a new validated record, never an invented approval. Frontmatter status is advisory: derive consumability from a valid sidecar, not its filename or an editable status field. This is integrity checking, not cryptographic authentication against malicious record tampering. Atomic publication protects one step, not a multi-file/distributed transaction.

Resume from the last validated checkpoint after checking freshness. An interrupted draft can contain useful evidence but cannot silently become final. Retrying a stage must not repeat external side effects; use supported idempotency/transaction facilities and user authorization. Do not simulate distributed transactions with Markdown.

## Concurrency and promotion

Give a worker a bounded question, source identity, relevant contracts, artifact ownership, budget, and evidence format. Prefer independent slices. Keep shared source read-only during analysis; use isolated checkouts only when justified. Never let workers overwrite one shared report.

Before combining results, reconcile versions, assumptions, duplicate root causes, contradictory evidence, and shared invariants. Disjoint writes can still conflict semantically. A coordinator owns reconciliation and publication, not unquestioning concatenation.

Before applying authorized edits, revalidate read dependencies and current destination content. On conflict, preserve user changes and refresh the patch; never restore an old snapshot over them. Retention/cleanup is explicit: do not automatically delete unreferenced source, user artifacts, or old runs.

## Optional bounded freshness helper

`scripts/context_snapshot.py` uses Python's standard library. It hashes only explicit files/directories; it performs no writes, builds, or network operations. Supply a small dependency slice, including relevant wiring and directories whose membership matters. It includes hidden files and refuses symlinks/reparse points and out-of-root paths. Never select secrets merely to get a complete hash inventory.

```text
python <skill>/scripts/context_snapshot.py capture --root <repo> --path src/billing --path config/providers.yaml
python <skill>/scripts/context_snapshot.py check --root <repo> --manifest <saved-manifest.json>
```

Capture emits JSON; save it using the host's authorized artifact mechanism if needed. Check exits 0 for current, 1 for stale, 2 for invalid/incomplete input. Default limits: 10,000 files and 128 MiB of file content, plus hard caps of 50,000 traversed entries, depth 128, and 16 MiB per input manifest; excess fails closed. Narrow scope rather than reflexively increasing limits. See `--help` for optional file/byte budgets.

This is a declared-byte dependency check, not an atomic filesystem snapshot, semantic dependency discovery, repository security scanner, or completion validator. Capture/check can race with writers; it detects some read-time changes but cannot promise a consistent snapshot. Use a stable checkout for stronger guarantees. Revalidate after final edits; a source can change immediately after any check.
