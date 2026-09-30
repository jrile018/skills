# Portfolio, Risk, and Calibration

## Module contract

- **Purpose:** Analyze allocation, covariance, factor exposure, risk measures, constraints, calibration stability, and margin/counterparty optimization.
- **Load when:** The task asks how exposures combine, how an objective is optimized, or how estimated inputs and operational constraints affect a decision.
- **Do not load when:** The question is only a derivative replication or stochastic transformation.
- **Inputs:** Assets/exposures, horizon, return convention, objective, constraints, estimates, and operational limits.
- **Output invariant:** Separate mathematical optimum, estimation uncertainty, and implementation feasibility.

## Portfolio workflow

1. Define assets, horizon, numeraire, return convention, objective, and feasible constraints.
2. State the mean, covariance or factor model, estimation window, and data available when weights are formed.
3. Write the objective and constraints before solving. For fixed weights, `E[R_p] = w' mu` and `Var(R_p) = w' Sigma w`.
4. Check covariance symmetry and positive semidefiniteness, constraint feasibility, units, exposure totals, and sign conventions.
5. Stress means, volatilities, correlations, lookbacks, position caps, leverage, liquidity, financing, and transaction costs.
6. Report concentration, factor exposures, turnover, sensitivity, and scenario losses alongside the optimized objective.

## Risk and calibration

Define the loss variable, horizon, confidence level, and aggregation convention. VaR is a quantile threshold; expected shortfall summarizes loss beyond a threshold. Neither replaces scenarios, model-risk review, or stress testing.

Exact repricing does not guarantee stable parameters, valuations, or hedges. Inspect conditioning and small singular values. When regularizing, identify the penalty, scaling, and tuning rule, then show the fit–stability tradeoff. Smoothness or sparsity is a modeling choice, not directly observed market information.

## Factors and operational applications

Distinguish common-factor covariance from specific risk and statistical components from economic explanations. PCA portfolios require the empirical checks in `empirical-research.md` before an allocation claim.

For margin or counterparty-network optimization, include netting, collateral, clearing, discrete trade constraints, fairness, feasibility, sparse structure, and rounding. A continuous optimum can be operationally invalid. Biomedical-project diversification and other practitioner cases are demonstrations of portfolio reasoning; retain their stated dependence assumptions and dated evidence status.

## Verification

Check limiting correlations, constraint residuals, scenario P&L, perturbation sensitivity, alternative estimation windows, and rounding effects. For a two-asset example, test correlations `-1`, `0`, and `1` to expose covariance or sign errors.
