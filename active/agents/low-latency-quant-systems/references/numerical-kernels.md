# Numerical kernels

## Purpose and loading boundary

Use this module when the hot work is linear algebra, FFT, optimization, calibration, Monte Carlo, statistics, filtering, or another numerical method. Do not load it for byte parsing, queueing, or socket work with no numerical contract.

## Define mathematical acceptance first

Record the problem, shapes and sparsity, precision, conditioning or sensitivity, residual/error metric, convergence condition, tolerances, determinism requirement, and downstream effect of error. Keep a trusted reference implementation or independent oracle. Test ordinary, boundary, ill-conditioned, degenerate, and nonconvergent cases that are plausible for the workload.

A faster wrong answer is a failure. An approximation is acceptable only with a stated error budget and downstream risk check.

## Optimize in the right order

1. Remove redundant mathematical work or choose a more appropriate algorithm.
2. Exploit guaranteed structure such as symmetry, sparsity, low rank, or repeated operands.
3. Estimate arithmetic intensity and data movement; use roofline-style bounds to identify the limiting resource.
4. Consider blocking, packing, batching, fusion, sparse layouts, iterative methods, library kernels, or parallel decomposition.
5. Inspect target-specific code generation only after the algorithm and data movement are credible.

Benchmark representative shapes and distributions, not only square dense matrices. Include setup, packing, conversion, transfer, convergence, and synchronization costs when they occur on the measured path.

## CPU, GPU, and reproducibility

A GPU or accelerator is plausible when parallel work amortizes launch and transfer costs; preserve the same mathematical contract and compare end to end. Pin libraries, algorithms, thread counts, and relevant determinism settings. If reductions or parallel scheduling change rounding order, quantify the difference rather than assume bitwise equivalence.

For stochastic computation, preserve seeds, random-number method, scenario set, and variance-reduction logic. For iterative methods, report iteration count and convergence behavior alongside time.
