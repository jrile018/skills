# Course-specialist routing

Read this catalog only when the user explicitly names one of the five courses, requests course-specific learning or provenance, or a multi-course task needs distinct specialist artifacts.

## Specialist catalog

| Observable request condition | Owner | Output contract | Do not route merely because |
|---|---|---|---|
| Concrete profiling, benchmarking, bottleneck diagnosis, optimization implementation, or explicit MIT 6.172 study | `$mit-6172-performance-engineering` | Correctness-preserving performance evidence: baseline, bottleneck, change, verification, comparable result | Finance code happens to be slow without a workload or measurement question |
| Adaptive Markets, hedge-fund ecology, changing efficiency, crowding, liquidity/leverage feedback, crisis mechanisms, ethics, or high-level falsifiable test design | `$mit-15481x-adaptive-markets` | Actor/mechanism map, competing hypotheses, testable implications, evidence gaps | A request merely mentions hedge funds, returns, or risk |
| Explicit MIT 15.450 work or an advanced workflow integrating at least two of econometrics, stochastic pricing, Monte Carlo, volatility, or dynamic portfolio choice | `$mit-15450-analytics-of-finance` | Model contract, derivation or estimation, uncertainty, dependent handoff, and independent verification | A request asks one introductory finance question |
| Explicit MIT 18.642 study, lecture/problem/project help, or broad mathematics-to-finance translation | `$mit-18642-quant-finance` | Prerequisite-aware course guidance, mathematical object, verified result, and source-status label | A general quant problem happens to use a topic taught in 18.642 |
| C++ ownership, object lifetime, RAII, special members, move transfer, memory-safety diagnosis, or explicit Stanford CS106L study | `$stanford-cs106l-cpp-memory` | Ownership graph, lifetime diagnosis, smallest repair or teaching path, and verification evidence | A C++ workload is merely slow, uses memory, or asks about atomics or virtual memory |

The main `ingenius-quant-finance` skill remains the owner of cross-course quantitative-finance analysis when the user did not ask for a particular course lens.

## Multi-course tasks

Keep one agent when the reasoning is tightly coupled. Delegate only when the task has independent artifacts or an explicit dependency handoff.

Use these acyclic handoffs when the request actually needs them:

```text
15.481x adaptive hypothesis and high-level test design
    → 15.450 execution-ready econometric specification and uncertainty
        → 6.172 measured implementation optimization

18.642 broad learning or project design
    → 15.450 advanced multi-method derivation when the project exceeds survey depth
        → 6.172 only if a real implementation bottleneck is measured

CS106L ownership and lifetime contract
    → 6.172 for a measured non-trading allocation or locality bottleneck
    → low-latency quant systems for a measured trading critical path
```

For each worker, name the exact specialist skill path, input artifact, requested output, and forbidden scope. Do not ask all specialists to answer the same broad question and vote.

Examples:

- A crowding thesis and high-level falsifiable test remain with 15.481x. Add a 15.450 worker only when the user needs a dated, execution-ready econometric specification, dependence-valid inference, estimation, or implementation.
- An independent code-performance audit and course-provenance audit may run in parallel because neither consumes the other's result.
- A pricing derivation and its numerical optimization remain with one 15.450 worker unless the implementation has a separately measured bottleneck.

The parent checks that downstream work preserves upstream assumptions, dates, information sets, uncertainty, and boundaries, then returns one synthesis.

## No-match and overlap handling

- If none fits, use the parent's ordinary domain modules or ask for the user's actual decision.
- If 18.642 and 15.450 both appear to fit, use 18.642 for course learning and broad translation; use 15.450 for advanced integrated method work.
- If a course is named only as a citation preference, keep the task with its actual decision owner and add provenance.
- If a requested lecture or artifact is unavailable, say so; never infer it from the title.
- If “memory” is ambiguous, distinguish C++ ownership/lifetime from cache or allocator performance, atomic ordering, and operating-system virtual memory before routing.

## Cold-walk tests

| Request | Expected route |
|---|---|
| “Use 6.172 to optimize this backtest hot path.” | 6.172 only |
| “Does Adaptive Markets explain this crowded trade, and what evidence could test it?” | 15.481x only |
| “Turn that crowding hypothesis into an execution-ready econometric test with dependence-valid inference.” | 15.481x, then 15.450 |
| “Teach me 18.642 PCA.” | 18.642 only |
| “Estimate a volatility model and use it in Monte Carlo pricing.” | 15.450 only |
| “Explain PCA exposure in my portfolio.” | Parent empirical module, then portfolio/risk; no course specialist unless requested |
| “This moved C++ order object double-frees; repair its ownership contract.” | CS106L only; add low-latency systems later only for a measured trading-performance objective |
| “Reduce allocator overhead in this parser.” | 6.172 only unless an ownership/lifetime change is required |
