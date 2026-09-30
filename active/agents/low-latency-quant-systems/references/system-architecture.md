# System architecture and placement

## Purpose and loading boundary

Use this module when the user must allocate a latency budget, choose process/stage boundaries, or decide among CPU, GPU, FPGA, kernel networking, and user-space networking. Do not load it for a localized hot loop with an established architecture.

## Build the end-to-end model

Map the actual stages—for example ingress, decode, normalization, book/state update, features, decision, risk, encoding, gateway, and egress. For every boundary record input/output, state ownership, copies/serialization, queue, clock/timestamp, error handling, and latency distribution. Allocate a budget only after measuring or explicitly labeling assumptions.

Model steady state, burst load, recovery, and saturation. Couple tail latency with goodput: one cannot be optimized independently near capacity. Identify which stage determines the critical path and which work can be batched, parallelized, or moved off it.

## Placement decision

Compare candidates on:

| Dimension | Questions |
|---|---|
| Workload | Per-event serial latency, vector batch, throughput, irregular control, state size |
| Data movement | Copies, PCIe/network transfer, serialization, cache/NUMA traffic |
| Determinism | Tail/jitter, scheduling, queueing, warm-up, dynamic frequency |
| Correctness | Precision, ordering, protocol/state-machine semantics, recovery |
| Operations | Observability, deployability, rollback, capacity, power, hardware availability |
| Economics | Engineering effort, specialist maintenance, infrastructure cost, useful lifetime |

CPUs usually own irregular or tightly stateful per-event paths; GPUs favor enough parallel work to amortize launch and transfer; FPGAs can provide deterministic pipelines at higher development and verification cost. These are starting hypotheses, not conclusions. Benchmark the candidate end to end.

## Deliverable

Return the current path and budget, bottleneck evidence, candidate placements, expected mechanism, correctness/operational risks, measurement plan, and rollback condition. Do not recommend a purchase or production migration without user authorization and evidence from the target environment.
