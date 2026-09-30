# Measurement contract

## Purpose and loading boundary

The parent owns the ordinary baseline and acceptance gate. Use this module only when measurement design itself is nontrivial: clocks cross boundaries, harness overhead matters, load approaches saturation, effects are small relative to drift, or an acceptance record must be audited. Do not load it merely because a task needs a normal before/after benchmark.

## Define the record before tuning

Capture:

- semantic and numerical correctness commands or oracles;
- event stream, data shape, rate, burst model, warm state, and provenance;
- path boundaries and clock/timestamp source;
- target metric: latency distribution, deadline misses, throughput under load, scaling efficiency, or resource cost;
- machine, CPU/NIC/GPU, NUMA placement, power/frequency policy, OS/kernel, toolchain, build flags, and process/thread layout;
- baseline distribution, repetitions, warm-up, variability, and background-load controls;
- candidate identity, changed mechanism, expected effect, and rollback trigger.

Use quantiles appropriate to the objective and include sample count and variability. Do not hide a tail regression behind a lower mean. For capacity work, measure latency while increasing offered load and record loss, queue growth, backpressure, and saturation. For small effects, interleave or randomize comparable runs when feasible so drift does not masquerade as improvement.

## Timestamp and harness checks

Name the exact boundaries: for example packet arrival, decoded event, book update, decision, risk approval, send call, driver, or hardware transmit. Verify monotonicity, resolution, synchronization, overhead, and whether timestamps cross clocks or machines. Measure the harness overhead when it is not negligible.

Use a production-shaped replay or clearly disclose why a synthetic workload is representative. Preserve burstiness, event mix, state size, branch distribution, numerical shapes, and concurrency. A tiny uniform microbenchmark is useful only for isolating a mechanism.

## Advanced acceptance record

Apply the parent's global acceptance gate. For a complex experiment, also record whether:

1. every required correctness oracle passes;
2. the baseline and candidate use comparable workloads and environments;
3. the predicted metric moves enough to exceed noise or the uncertainty is disclosed;
4. end-to-end behavior improves at the relevant load, not only the isolated kernel;
5. resource, complexity, power, operability, and portability costs remain acceptable;
6. the evidence and rollback condition are recorded.

A flat or negative result remains a valid outcome. Record it and revise the hypothesis rather than retaining an unmeasured optimization.
