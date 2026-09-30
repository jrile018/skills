---
name: advanced-portfolio-theory
description: Design and validate advanced portfolio construction and allocation decisions under estimation error, constraints, costs, and multiple periods. Use for equilibrium or factor models, Bayesian or robust construction, risk budgeting, dynamic allocation, and implementation-aware portfolio research. Not for basic portfolio arithmetic, generic solver mechanics, derivative pricing, security recommendations, or trade execution.
---

# Advanced Portfolio Theory

Turn forecasts, risk estimates, investor objectives, and implementation limits into an allocation whose assumptions and out-of-sample behavior can be inspected. Treat the optimizer as one stage in a decision system—not as a source of economic truth.

## Establish the decision contract

Identify the investable universe, numeraire, objective or utility, benchmark, horizon, rebalance rule, information set, liabilities, constraints, financing, liquidity, transaction costs, and required output. Distinguish estimated inputs from contractual facts. Ask for missing inputs only when a reasonable labeled assumption would materially change the decision.

## Route narrowly

| Observable request | Read |
|---|---|
| Mean-variance geometry, utility, CAPM/APT, factor spanning, equilibrium, attribution, or risk premia | [static-and-equilibrium.md](references/static-and-equilibrium.md) |
| Expected-return and covariance estimation, shrinkage, Bayesian views, Black–Litterman, robust construction, constraints, turnover, or implementation costs | [estimation-and-construction.md](references/estimation-and-construction.md) |
| Multi-period allocation, liabilities, consumption, regime state, rebalancing, Bellman recursion, or continuous-time portfolio choice | [dynamic-allocation.md](references/dynamic-allocation.md) |
| Backtesting, uncertainty, stress tests, attribution, course/source coverage, or maintaining this skill | [validation-and-sources.md](references/validation-and-sources.md) |

Use at most two modules in an ordinary phase. Route by the decision being made, not by a term such as “factor,” “risk,” or “optimization” in isolation.

## Workflow

1. Define the decision and evaluation horizon before choosing a model.
2. Specify the information available at each decision time and the estimators fitted from it.
3. Build a simple investable baseline before adding views, dynamics, or robustness.
4. Write the objective, constraints, costs, and units. Separate economic assumptions from numerical implementation.
5. Solve or characterize the allocation, then inspect binding constraints, turnover, concentration, and sensitivity to uncertain inputs.
6. Evaluate with point-in-time data, realistic rebalancing and costs, multiple regimes, and an untouched final test where feasible.
7. Attribute results to exposures, timing, costs, constraints, and estimation choices. Report uncertainty and failure modes, not only a point estimate.

## Invariants and handoffs

- No future information may enter an estimator, universe, constraint, or rebalance decision.
- An efficient frontier conditional on estimated inputs is not a guarantee of an efficient realized portfolio.
- Expected-return error usually dominates superficial numerical precision; show sensitivity or shrinkage when it matters.
- Constraints and costs are part of the economic problem, not post-processing.
- Compare with simple allocations such as cash, benchmark, equal weight, or a stated risk-balanced baseline.
- Do not infer causality or stable risk premia from an in-sample factor fit.

Use `ingenius-quant-finance` for routine allocation, covariance, VaR/ES, or empirical estimation. Use `robust-quant-optimization` when generic formulation, KKT/duality, uncertainty-set design, or solver certification is the requested artifact. Use `rigorous-mathematical-finance` when the core deliverable is a theorem-level martingale, measure-change, stochastic-control, or no-arbitrage derivation. Pass only a named artifact—such as a point-in-time estimate with uncertainty, a fully specified program, or a verified value-function equation—between skills.

This skill supports education and research. It does not provide individualized investment advice, promise performance, authorize trades, or mutate production systems.
