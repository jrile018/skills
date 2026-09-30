# Estimation-Aware Portfolio Construction

## Loading boundary

Read this module when forecasts, covariance estimation, Bayesian views, shrinkage, robustness, constraints, turnover, or costs determine the allocation. Do not load it for a pure theorem proof or generic solver tutorial.

## Treat inputs as uncertain

Record how returns, covariances, factors, views, and transaction-cost parameters were estimated and what information was available at each rebalance. Align horizons between forecasts, risk, costs, and holding period. Preserve universe membership and delisting information through time.

Expected returns are especially fragile. Compare the chosen estimator with a simple prior or shrinkage target and show how allocation changes under plausible perturbations. For covariance, inspect positive semidefiniteness, conditioning, effective sample size, missing-data policy, and regime sensitivity.

## Construction methods

Select a method because it matches the decision, not because it is fashionable:

- shrinkage or structured covariance for estimation stability;
- Bayesian updating when prior, likelihood, and view confidence can be stated;
- Black–Litterman-style construction when equilibrium returns and linear views have interpretable units and uncertainty;
- robust optimization when an uncertainty set and its conservatism have operational meaning;
- risk budgeting when allocation by risk contribution is the actual mandate;
- resampling or distributional analysis as a stability diagnostic, not an automatic cure.

Include turnover, spread, fees, impact, borrow, financing, taxes, and capacity only to the fidelity required by the use case. State whether costs enter the objective, constraints, or evaluation. Avoid double-counting them.

## Verification

1. Check feasibility with current holdings and operational constraints.
2. Inspect active constraints, dual information when meaningful, and unexpected corner solutions.
3. Perturb return, covariance, cost, and constraint inputs.
4. Compare gross and net performance and turnover against simple baselines.
5. Separate estimator improvement from optimization improvement with controlled ablations.
6. Reject a construction that succeeds only under one seed, period, universe, or cost assumption.

When the requested artifact is a formal convex, robust, or stochastic program and certificate, hand the fully specified decision contract to `robust-quant-optimization` rather than duplicating its solver work here.
