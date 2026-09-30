# Stochastic Calculus and Pricing

## Loading boundary

Read this module for Itō calculus, stochastic differential equations, Girsanov or numeraire changes, replication, Feynman–Kac, pricing PDEs, rate models, or advanced volatility derivations. Do not load it just to insert values into a standard pricing formula.

## Derivation discipline

State the driving processes, correlation structure, coefficient regularity, measure, filtration, and solution concept. For Itō calculations, show the quadratic-variation terms. For measure change, state the density process and conditions ensuring it defines the required measure; then transform both Brownian motions and drifts explicitly.

For replication and PDE derivations:

1. Specify the claim, tradable assets, strategy, and self-financing condition.
2. Apply Itō's formula with all first-, second-, and cross-derivative terms.
3. Choose holdings to match diffusive exposures where the market permits it.
4. Use the financing account and no-arbitrage condition to obtain the PDE or expectation.
5. State terminal and boundary conditions and the theorem connecting the PDE and stochastic representation.

For a change of numeraire, define the normalized prices and Radon–Nikodym derivative consistently. Never switch measures by changing only a drift symbol.

## Verification

- Re-derive by risk-neutral expectation and by replication/PDE when both are available.
- Check dimensions, sign, monotonicity, parity, boundary behavior, and deterministic or zero-volatility limits.
- For rates, identify the numeraire and distinguish short-rate, forward-rate, and market-measure dynamics.
- For stochastic/local volatility, state which risks are traded, calibrated, or left unhedged and whether the market is complete.
- Treat numerical convergence and calibration as separate evidence from the mathematical pricing identity.
