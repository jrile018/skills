# Transactions, recovery, and distribution

## Loading boundary

Use when concurrent writes, retries, partial failure, replication, or recovery can violate business invariants.

## Design procedure

1. State each invariant and the operation that can break it.
2. Choose transaction and isolation boundaries from that invariant; list anomalies explicitly.
3. Define idempotency key, deduplication horizon, retry behavior, poison-message handling, and reconciliation.
4. State ordering and consistency by key/operation rather than labeling the whole system “strong” or “eventual.”
5. Define checkpoint, log, snapshot, backup, failover, RPO, RTO, and restore tests.
6. Test crash points before, during, and after every externally visible effect.

For streams, separate delivery semantics from business-effect semantics. For dual writes, use a transactionally coupled outbox/log or an explicit reconciliation design. For distributed replicas, name the leader/quorum or conflict-resolution rule and behavior during partitions.

Choose indexes and materializations from real read/write workloads. Benchmark with representative cardinality, skew, concurrency, cache state, and failure/recovery work; a query-plan improvement must preserve result semantics.

