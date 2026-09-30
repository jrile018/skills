# Execution design

## Loading boundary

Use when the user must choose, compare, or analyze an execution or market-making policy. Do not use as a generic alpha-strategy module.

## Objective and benchmark

State the benchmark—decision, arrival, close, VWAP, or another explicit price—and measure all costs in consistent price, basis-point, or currency units. A useful decomposition distinguishes explicit fees/rebates, spread, delay, market impact, opportunity cost, and residual price movement.

For liquidation or acquisition, define inventory path, horizon, participation constraints, terminal obligation, risk measure, temporary/permanent/transient impact choice, and signal assumptions. For market making, define inventory limits, fill intensities, adverse selection, fees/rebates, quote controls, and terminal inventory treatment.

## Model ladder

1. Deterministic baseline such as TWAP, VWAP, or capped participation.
2. Simple empirical cost model with monotonicity and unit checks.
3. Dynamic schedule or quote policy only when its state variables can be observed and estimated.
4. Reinforcement learning only after a realistic simulator, stable baseline, off-policy evaluation plan, and explicit tail-risk controls exist.

Validate with chronological splits, identical constraints, capacity/size sweeps, regime stress, parameter perturbations, and distributional cost metrics. Report fill rate, unfilled quantity, inventory exposure, tail cost, turnover, and sensitivity—not only average implementation shortfall.

