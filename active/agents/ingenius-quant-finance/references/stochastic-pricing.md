# Stochastic Processes and Pricing

## Module contract

- **Purpose:** Review stochastic-process reasoning, Itō/SDE derivations, replication, options, rates, commodities, and credit models.
- **Load when:** The request involves path dynamics, a pricing measure, hedging, a PDE, simulation, a contingent payoff, or a curve/credit valuation.
- **Do not load when:** The task is solely an empirical forecast or allocation from estimated returns.
- **Inputs:** State variables, filtration/information set, horizon, payoff, tradable instruments, dynamics, measure, and market assumptions.
- **Output invariant:** Name the measure, assumptions, payoff, valuation/hedging principle, and independent verification route.

## Reasoning sequence

1. Define state variables, information set, horizon, payoff, and tradable instruments.
2. State dynamics and parameter assumptions. Continuous Brownian paths are not differentiable and have nonzero quadratic variation.
3. Apply martingale, stopping, Itō, conditional-expectation, or measure-change results only after checking their conditions.
4. Distinguish the physical measure for outcomes/forecasts from a pricing measure for no-arbitrage valuation.
5. Derive through replication, pricing expectation, PDE, tree, finite difference, or Monte Carlo and explain why that route applies.
6. Verify with another representation, state-by-state payoff match, terminal/boundary conditions, limiting case, or martingale/self-financing check.

## Core distinctions

- Apply the parent's measure and payoff/price invariants explicitly at every valuation step.
- In a one-period complete model, verify pricing probabilities lie in `[0,1]` and the replicating portfolio matches every state.
- Applying Itō to geometric Brownian motion produces the `-sigma^2/2` log-drift correction.
- A Black–Scholes-style PDE depends on market and dynamics assumptions; physical drift disappears through replication.
- Simulation must separate time-discretization error from Monte Carlo sampling error.
- Strike derivatives of option prices concern a pricing distribution under appropriate regularity, not an automatic physical forecast.

## Rates, commodities, and credit

For rates, distinguish discounting and projection curves, forwards, sensitivities, and physical versus pricing dynamics. Fitting today's curve does not determine future evolution or volatility; in HJM-style models no-arbitrage links pricing-measure drift to volatility.

For commodities and operational options, state storage, capacity, injection/withdrawal, fuel, non-storability, and completeness assumptions. Do not import equity replication when the underlying cannot be traded or stored as required.

For credit/counterparty exposure, state default timing, recovery, collateral, netting, wrong-way risk, discounting, and valuation-adjustment sign conventions. Adding recovery, diffusion, or another risk source can break a simplified exact hedge.

Event-market material in the corpus is description-only. Do not manufacture contract mechanics or a mathematical model from the lecture title. The 2013 FX-execution lecture is also a documented coverage gap.

## Verification

Check units, terminal and boundary conditions, martingale and self-financing properties, state-by-state replication, limiting cases, and consistency across analytical, tree, PDE, and simulation routes.
