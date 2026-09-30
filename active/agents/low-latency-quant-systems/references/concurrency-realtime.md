# Concurrency and real-time behavior

## Purpose and loading boundary

Use this module when threads, queues, atomics, locks, core affinity, NUMA, scheduling, ownership, or backpressure materially affect the path. Do not load it for independent batch jobs whose only question is numerical scaling.

## Establish the concurrency contract

Map producers, consumers, state ownership, queue capacity, ordering, backpressure, and shutdown/recovery. State whether the objective is single-message latency, bounded jitter, throughput, fairness, deterministic replay, or some combination. Identify which operations may block or allocate and which cores, NUMA nodes, and shared cache levels are involved.

Correctness gates include race freedom, legal memory ordering, no lost/duplicated events, progress requirements, bounded queue behavior, and lifecycle-safe reclamation. “Lock-free” is not a synonym for faster or wait-free; document the actual progress property and contention pattern.

## Diagnose scaling and jitter

Record per-worker timing and queue occupancy where possible. Test load balance, contention, false sharing, cache-line ownership, remote NUMA traffic, synchronization frequency, scheduling/preemption, allocation, and producer/consumer rate mismatch before adding threads or replacing a lock.

Use production-shaped bursts and sustained load. Report tail latency, dropped/retried work, queue growth, CPU reservation, and power cost. A design that wins unloaded median latency but becomes unstable near saturation fails the system objective.

## Candidate changes

Prefer clear ownership and partitioning before sophisticated synchronization. Candidate experiments may include sharding, single-writer state, batching with a bounded latency budget, queue sizing, cache-line separation, core/NUMA placement, allocation removal, or a different synchronization primitive. Change one mechanism at a time and preserve a simpler control.

Run race, stress, ordering, wraparound, shutdown, and recovery tests as applicable. If a change relaxes deterministic ordering, make the new semantics explicit and confirm downstream trading and numerical contracts.
