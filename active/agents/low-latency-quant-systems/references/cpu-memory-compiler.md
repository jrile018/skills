# CPU, memory, and compiler diagnosis

## Purpose and loading boundary

Use this module after evidence points to generated code, front-end/back-end limits, branches, cache/TLB behavior, allocation, data layout, SIMD, instruction dependencies, or compiler transformations. Do not load it because C++ or “fast” appears in the request without a measured hot region.

## Diagnose before choosing a transformation

Profile the production-shaped path and classify the leading mechanism: excessive work, branch behavior, dependency chains, instruction/port pressure, cache or TLB misses, bandwidth, allocation/lifetime, copying, or compiler failure. Inspect optimization remarks, IR when useful, and final assembly for claims about inlining, devirtualization, vectorization, aliasing, or loop transformation.

Prefer the smallest experiment that distinguishes hypotheses. Candidate families include data layout and traversal changes, removal of redundant work/copies, blocking, precomputation, branch restructuring, allocation/lifetime changes, compiler flags, SIMD, and target-specific dispatch. Keep a scalar or previous implementation as a correctness oracle.

## Target-specific evidence

Pin the CPU model, ISA features, compiler, flags, and relevant manual/tool version. Use uops.info and vendor manuals to explain exact instruction forms on the exact microarchitecture. Use LLVM MCA to test static scheduling/resource hypotheses. Keep latency, reciprocal throughput, dependency chains, and resource pressure distinct.

These tools omit important application effects. Confirm with real measurements and counters. Never transfer instruction numbers across CPU generations, and never ship a target-specific instruction path without feature detection or a deployment guarantee plus tested fallback.

## SIMD and memory invariants

Test non-multiple vector lengths, alignment variants, aliasing, exceptional values, and divergent control flow. Account for gather/scatter, packing, and conversion cost. Measure working-set transitions rather than one cache-resident size. Treat prefetching as workload- and CPU-specific. Preserve numerical tolerance and event ordering when vector or parallel reduction changes operation order.

## Acceptance

Apply the parent acceptance gate. Additionally require that the claimed CPU mechanism matches the target code and microarchitecture. A shorter instruction sequence or better static throughput does not override a cache, branch, synchronization, or network bottleneck.
