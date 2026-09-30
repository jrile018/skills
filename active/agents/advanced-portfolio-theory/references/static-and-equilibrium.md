# Static Portfolio Theory and Equilibrium

## Loading boundary

Read this module for portfolio geometry, utility, factor structure, equilibrium, performance attribution, and risk-premium reasoning. Do not load it solely to estimate inputs, select a solver, or value a derivative.

## Core reasoning

Write risky excess returns as a vector with conditional mean `mu` and covariance `Sigma`. For quadratic mean-variance analysis, state the convention explicitly, for example

`max_w  w' mu - (gamma / 2) w' Sigma w`

subject to the actual budget, leverage, holding, and exposure constraints. Verify units and whether cash or a risk-free asset is included. If `Sigma` is singular or estimated noisily, do not silently invert it.

Use geometry to answer what spans the frontier and which constraints change it. Use utility to connect risk aversion and wealth to a decision, while stating where a quadratic approximation or return distribution assumption is being made.

For factor models, distinguish:

- statistical factors from economically named factors;
- exposure attribution from causal explanation;
- factor covariance from idiosyncratic covariance;
- a pricing restriction from a forecasting model.

For CAPM, APT, or another equilibrium model, state the market, investor, friction, and spanning assumptions that generate the restriction. An empirical rejection may indicate bad measurement, omitted factors, changing opportunities, or failure of the equilibrium assumptions; it does not identify one cause automatically.

## Checks

- Reconstruct portfolio mean, variance, factor contribution, and residual contribution from the same units and horizon.
- Compare marginal and component risk contributions; confirm that components sum under the selected risk measure when the decomposition permits it.
- Test affine or scale invariance only where the model should possess it.
- Compare the optimized allocation with an equal-weight, benchmark, cash, or stated risk-balanced portfolio.
- Report concentration and exposure changes, not only a Sharpe ratio.
