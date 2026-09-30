---
name: low-latency-quant-systems
description: Engineer and verify latency-critical quantitative trading systems. Use instead of mit-6172-performance-engineering when an end-to-end trading, market-data, execution, pricing, risk, or research workload needs measured systems optimization; use the MIT skill for non-trading performance or explicit 6.172 study. Not for generic refactoring or strategy research without a systems-performance objective.
---

# Low Latency Quant Systems

Improve the user's actual trading-system objective without weakening market semantics, numerical validity, concurrency correctness, or operability. Treat every optimization as a causal claim that must survive an end-to-end test on the target environment.

## Establish the contract

Identify the path being optimized, semantic and numerical invariants, representative event or batch workload, latency/throughput objective, timestamp boundaries, target hardware/toolchain, and acceptable tradeoffs. Ask only for a missing fact that changes the investigation; otherwise state a bounded assumption.

Do not claim improvement without a reproducible baseline. If the target is not runnable, return a benchmark and instrumentation plan rather than a speedup estimate. This section and **Investigate and verify** are the canonical global measurement and acceptance contract; modules add only decision-specific gates.

## Route to the smallest module set

| Observable condition | Read | Add another module only when |
|---|---|---|
| Benchmark design is nontrivial: clocks cross boundaries, tail/capacity claims are contested, harness overhead matters, or an acceptance record must be audited | [measurement-contract.md](references/measurement-contract.md) | A domain module owns a correctness or mechanism decision |
| The path handles feeds, books, orders, fills, replay, execution, P&L, or point-in-time research data | [trading-correctness.md](references/trading-correctness.md) | The request also asks how to optimize a measured bottleneck |
| Evidence points to generated code, branches, cache, allocation, SIMD, instruction dependencies, or compiler behavior | [cpu-memory-compiler.md](references/cpu-memory-compiler.md) | A numerical method or concurrency contract also changes |
| The hot work is linear algebra, FFT, simulation, optimization, calibration, statistics, or another numerical kernel | [numerical-kernels.md](references/numerical-kernels.md) | Target-specific implementation evidence is also required |
| Threads, queues, atomics, locks, core affinity, NUMA, scheduling, or backpressure dominate | [concurrency-realtime.md](references/concurrency-realtime.md) | Network queue placement or packet ingress/egress is material |
| The path includes sockets, multicast, kernel/NIC queues, packet loss, timestamping, PTP, busy polling, or DPDK | [networking-time.md](references/networking-time.md) | A whole-system placement decision is also requested |
| The user must choose CPU/GPU/FPGA, process boundaries, pipeline stages, or a system-wide latency budget | [system-architecture.md](references/system-architecture.md) | Component evidence is needed to populate the decision |

When several modules apply, load only those that own distinct decisions. The parent already supplies the ordinary measurement contract. Read no more than two technical modules for a normal phase; sequence or delegate a broader investigation into bounded phases. Define trading correctness before tuning. Let a numerical module define algorithm/error obligations before a CPU implementation module changes the kernel. Define timestamp boundaries before comparing network paths.

## Investigate and verify

1. Reproduce correctness and record an end-to-end baseline.
2. Localize the limiting layer with evidence; distinguish algorithmic work, code generation, memory, synchronization, networking, external waits, and measurement artifacts.
3. State the mechanism, predicted metric movement, correctness risk, and rollback condition.
4. Make the smallest change that can test the hypothesis.
5. Run semantic and numerical oracles before comparable repeated measurement.
6. Report the latency distribution or scaling result, variability, resource cost, and any flat or negative result.

A faster microbenchmark, a favorable static pipeline model, or an instruction-table lookup is not end-to-end proof. Preserve event order, point-in-time information, book/order state, fills, positions, cash/P&L, numerical tolerances, random/scenario comparability, and recovery behavior wherever they are part of the contract.

## Delegate selectively

Keep tightly coupled diagnosis with one agent. For independent measurements or a real artifact handoff, read [delegation-routing.md](references/delegation-routing.md) and assign each worker an exact module, input, evidence record, and stopping condition. Do not create one worker per module or treat worker agreement as proof.

## Boundaries

This skill can inspect code, design experiments, and implement scoped optimizations when requested. It does not authorize live trading, production deployment, infrastructure mutation, exchange connectivity, or purchases. It does not promise returns or treat historical course examples as current market facts.

Use `mit-6172-performance-engineering` for non-trading performance work or explicit MIT 6.172 study. Activate both only when the user explicitly asks for both the course lens and the trading-system contract.

Use `stanford-cs106l-cpp-memory` for C++ ownership and object-lifetime correctness when no trading-performance objective exists. When unsafe ownership must be repaired before a measured trading-path optimization, use that verified lifetime contract as an input here rather than treating a faster allocation scheme as evidence of safety.

Read [source-map.md](references/source-map.md) when provenance, course coverage, currentness, or licensing matters. Read [architecture-and-provenance.md](references/architecture-and-provenance.md) only when maintaining module boundaries or auditing the skill tree. Use [evaluation-plan.md](references/evaluation-plan.md) when changing activation, routing, or behavior.
