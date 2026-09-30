---
name: mit-6172-performance-engineering
description: Diagnose and verify non-trading codebase performance using MIT 6.172's measurement-first, cross-layer method, or support explicit 6.172 study. Use low-latency-quant-systems instead for trading-system performance unless the user explicitly requests both lenses. Not for ordinary refactoring or performance claims without a workload.
---

# MIT 6.172 Performance Engineering

Improve the user's actual performance objective without weakening correctness. Treat every optimization as a measured causal claim, not as a generally faster coding style.

## Establish the Contract

Identify the semantic behavior that must remain unchanged, the representative workload, target metric, environment, and acceptable tradeoffs. Ask only for missing information that would change the investigation; otherwise state a bounded assumption.

Do not optimize before there is a reproducible baseline. If no runnable target is available, produce a benchmark and instrumentation plan rather than claiming a speedup.

## Investigate

1. Reproduce correctness and record the baseline with workload, build/runtime configuration, hardware, statistic, and measurement noise.
2. Profile end to end. Classify the dominant limit as algorithmic work, instructions/vectorization, cache or bandwidth, allocation, synchronization/parallelism, I/O, or measurement artifact.
3. State the bottleneck evidence, proposed mechanism, expected metric movement, correctness risk, and rollback condition.
4. Make the smallest change that tests that hypothesis. Preserve local conventions and maintainability unless the user explicitly accepts a tradeoff.
5. Run the correctness oracle before comparable repeated measurements. Report negative and flat results, not only successful changes.

Read [references/course-guide.md](references/course-guide.md) when selecting a cross-layer optimization, interpreting measurements, tutoring from 6.172, or checking source and historical-tooling boundaries.

## Verification Invariants

- A faster wrong answer is a failure.
- Compare the same workload and environment; disclose material deviations.
- Report representative statistics and variability, never only the best run.
- Use Amdahl-style bounds before optimizing a small fraction of total time.
- Treat races, nondeterminism, floating-point drift, and changed event ordering as correctness risks.
- Do not infer production improvement from a microbenchmark alone.
- Do not claim that historical Cilk, compiler, AWS, or hardware behavior is current without verification.

## Boundaries

This skill does not own generic cleanup, distributed-system architecture, capacity procurement, finance modeling, or security review unless they are part of a concrete performance investigation. It may analyze code and propose or implement scoped changes, but it does not authorize production deployment or infrastructure mutation.

Use `low-latency-quant-systems` instead when the performance target is a trading, market-data, execution, pricing, or risk path. Activate both only when the user explicitly requests both the MIT 6.172 lens and the trading-system contract.

Use `stanford-cs106l-cpp-memory` instead for C++ ownership, object-lifetime, RAII, special-member, move-transfer, leak, dangling, or double-deletion work without a performance objective. When a measured optimization also changes lifetime or ownership, establish the C++ correctness contract first and preserve it through this skill's benchmark loop.

For behavioral validation, use the positive, negative, correctness, and measurement cases in [references/course-guide.md](references/course-guide.md).
