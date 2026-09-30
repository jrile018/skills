---
name: reliable-quant-data-systems
description: Design and audit correct, reproducible, recoverable data platforms for quantitative research, market data, backtests, risk, and trading operations. Use for temporal semantics, lineage, schemas, idempotency, transactions, concurrency, replication, recovery, and research-to-production data contracts. Not for generic analytics, pure database tuning, or nanosecond hot-path optimization.
---

# Reliable Quant Data Systems

Design the data system around facts that can be reconstructed at a stated decision time. Prefer explicit temporal, ownership, failure, and recovery semantics over pipelines that merely complete on the happy path.

## Establish the contract

Identify producers and consumers, event and knowledge times, identifiers, revision policy, ordering guarantees, expected volume, freshness and availability targets, authoritative stores, replay requirements, failure model, and the decision that consumes the data.

## Route narrowly

| Observable request | Read |
|---|---|
| Point-in-time correctness, schemas, symbology, corporate actions, revisions, lineage, reproducibility, or research/production parity | [temporal-data-and-lineage.md](references/temporal-data-and-lineage.md) |
| Transactions, idempotency, concurrency, indexing, recovery, replication, consistency, queues, or failure handling | [transactions-recovery-distribution.md](references/transactions-recovery-distribution.md) |
| Verification, workload tests, course/source coverage, boundaries with other skills, or maintaining this skill | [validation-and-sources.md](references/validation-and-sources.md) |

Use both technical modules when temporal truth must survive distributed ingestion or recovery. Keep a single module for a bounded schema, lineage, transaction, or failure-semantics question.

## Workflow

1. Model the facts and time axes before choosing storage or streaming technology.
2. Define identities, schemas, invariants, deduplication keys, ordering, corrections, and authoritative ownership.
3. Map writes and reads to transaction, consistency, and isolation requirements.
4. Specify retries, idempotency, checkpoints, replay, reconciliation, and recovery objectives.
5. Exercise normal, duplicate, late, reordered, partial, stale, corrupt, and unavailable cases.
6. Demonstrate a reproducible consumer output from immutable inputs, code/config version, and lineage.

## Invariants and boundaries

- Event time, receipt time, effective time, and knowledge time are not interchangeable.
- Exactly-once business effects require idempotent application and reconciliation; a delivery label alone is insufficient.
- Replication is not a backup, and a backup is not verified until restore is tested.
- Availability and consistency claims require a named failure model and operation.
- A backtest must not see revisions or universe membership unavailable at the simulated decision time.

Use `low-latency-quant-systems` for measured feed-to-decision hot-path performance and `ingenius-quant-finance` for statistical or financial interpretation. This skill may design or implement scoped data changes when requested, but does not authorize production migration, credential use, destructive data operations, or live trading.
