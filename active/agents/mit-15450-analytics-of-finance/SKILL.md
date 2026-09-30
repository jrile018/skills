---
name: mit-15450-analytics-of-finance
description: Integrate financial econometrics, stochastic pricing, Monte Carlo, volatility, and dynamic portfolio choice using MIT 15.450. Use for explicit 15.450 work or advanced workflows spanning multiple of those methods; not for introductory definitions, behavioral-market analysis, or live trade advice.
---

# MIT 15.450 Analytics of Finance

Solve advanced quantitative-finance problems by keeping model definition, estimation uncertainty, and downstream valuation or optimization distinct.

## Establish the Model Contract

Identify the economic object, traded assets, horizon, state variables, information set, physical or pricing measure, objective, constraints, supplied data, and requested artifact. State material missing assumptions or ask only when no bounded assumption is safe.

## Choose the Integrated Path

| Required decision | Primary block |
|---|---|
| No-arbitrage value, replication, stochastic calculus, or derivative simulation | Pricing and Monte Carlo |
| Intertemporal allocation, Bellman recursion, or numerical policy | Dynamic portfolio choice |
| Estimated parameters, moments, standard errors, tests, or bootstrap | Econometrics and inference |
| Conditional variance dynamics or GARCH-family interpretation | Volatility modeling |

When the request spans blocks, order them by real dependency. Estimated inputs and their uncertainty must exist before a valuation or optimization consumes them.

Read [references/course-guide.md](references/course-guide.md) for block-specific checks, handoff contracts, historical-source boundaries, and evaluation cases.

## Work and Verify

1. Derive or justify the method from the stated assumptions.
2. Preserve physical-versus-pricing measures and expected-payoff-versus-price distinctions.
3. For estimation, state identification, dependence assumptions, diagnostics, and uncertainty.
4. For Monte Carlo or numerical methods, state discretization, sampling error, convergence checks, and known benchmarks.
5. For dynamic choice, state utility/objective, transition law, constraints, terminal condition, and approximation.
6. Stress estimated inputs and verify through dimensions, limiting cases, replication, simulation, residual diagnostics, or an independent derivation.

## Boundaries

This is an advanced integrated-method skill. A single basic formula or broad introductory course question should use ordinary reasoning or the 18.642 course skill. Market ecology and hedge-fund behavior belong to 15.481x. Code performance belongs to 6.172.

Treat the 2010 code and market examples as historical. Do not present MATLAB teaching files as production software, use dated course material as current market fact, recommend securities, or infer authority to execute trades.

