---
name: rigorous-mathematical-finance
description: Derive and verify advanced mathematical-finance results using filtered probability, martingales, measure changes, semimartingales, stochastic control, optimal stopping, PDE methods, and incomplete-market theory. Use for proof-level or multi-theorem pricing, hedging, and allocation work. Not for routine Black–Scholes calculations, empirical forecasting, portfolio recommendations, generic probability exercises, or numerical performance tuning.
---

# Rigorous Mathematical Finance

Make the probability space, admissible strategies, market assumptions, and theorem conditions explicit before manipulating formulas. The output is a derivation or proof that states where no-arbitrage, completeness, integrability, regularity, and boundary conditions enter.

## Establish the mathematical contract

Specify the filtered probability space, traded assets and numeraire, dynamics, information filtration, admissible strategies, claim or control objective, horizon, market frictions, and desired rigor. State whether the task is discrete or continuous time and whether the result concerns pricing, hedging, optimal stopping, utility, or control.

## Route narrowly

| Observable request | Read |
|---|---|
| Conditional expectation, martingales, stopping times, equivalent martingale measures, arbitrage, completeness, FTAP, admissibility, or semimartingale market structure | [probability-martingales-ftap.md](references/probability-martingales-ftap.md) |
| Itō integration/formula, SDEs, Girsanov, numeraire changes, replication, Feynman–Kac, pricing PDEs, rates, or volatility models | [stochastic-calculus-pricing.md](references/stochastic-calculus-pricing.md) |
| Utility maximization, Merton problems, Bellman/HJB equations, optimal stopping, American claims, duality, or incomplete-market bounds | [control-stopping-incomplete-markets.md](references/control-stopping-incomplete-markets.md) |
| Proof checks, simulation or discretization checks, counterexamples, source/course coverage, or maintaining this skill | [validation-and-sources.md](references/validation-and-sources.md) |

Use at most two modules in an ordinary phase. Do not load a rigorous module merely because a routine formula contains a stochastic term.

## Workflow

1. Define the stochastic objects, filtration, measures, numeraire, strategy class, and objective.
2. List the theorem or representation to be used and verify its hypotheses before invoking it.
3. Derive the result line by line, preserving measure labels, adaptedness, integrability, and boundary or terminal conditions.
4. Identify exactly where no-arbitrage, completeness, Markov structure, smoothness, or convex duality is required.
5. Verify with an independent route when practical: replication versus expectation, martingale versus PDE, dynamic programming versus a candidate-control check, limiting cases, or a small simulation.
6. Distinguish mathematical existence or uniqueness from calibration quality, numerical stability, liquidity, and tradability.

## Invariants and handoffs

- Never use a risk-neutral measure before establishing an appropriate no-arbitrage measure and numeraire relationship.
- Keep physical and pricing measures labeled through every expectation and drift change.
- A local martingale is not automatically a true martingale; check the property needed by the conclusion.
- State admissibility and integrability conditions instead of hiding doubling strategies or undefined expectations.
- Do not infer market completeness merely because one payoff has a replication.
- A formal PDE solution is not enough without applicable regularity, terminal/boundary conditions, and a verification argument.
- Discretization or Monte Carlo evidence can test a derivation but cannot replace theorem hypotheses.

Use `ingenius-quant-finance` for routine stochastic pricing and broad finance analysis, `mit-15450-analytics-of-finance` for explicit MIT 15.450 work, and `mit-18642-quant-finance` for explicit MIT 18.642 study. Use `advanced-portfolio-theory` when a verified control result feeds an implementable allocation decision; use `robust-quant-optimization` when the output becomes a numerical program requiring solver certification.

This skill is analytical and educational. It does not provide security recommendations, authorize trades, or treat a model price as an executable market price.
