---
name: market-microstructure-execution
description: Analyze market mechanics, order books, price impact, transaction costs, execution schedules, and market-making models. Use for execution-quality or microstructure decisions and explicit advanced course study. Not for live order placement, alpha claims, generic backtests, or systems-latency tuning; use low-latency-quant-systems for measured implementation performance.
---

# Market Microstructure and Execution

Turn an execution question into a market-state, objective, model, and validation contract. Preserve the distinction between a model of trading costs and evidence that the model describes the user's venue, instrument, horizon, and order flow.

## Establish the decision

Identify the instrument and venue, trading mechanism, order types, timestamp convention, information available at decision time, side and size, urgency or inventory objective, benchmark, constraints, and whether the user wants explanation, analysis, simulation, implementation, or review. State bounded assumptions rather than silently treating a continuous model as exchange mechanics.

## Route narrowly

| Observable request | Read |
|---|---|
| Limit-order-book mechanics, spread/depth, queue priority, adverse selection, auctions, or interpreting quotes/orders/trades | [market-mechanics.md](references/market-mechanics.md) |
| Arrival-price or implementation-shortfall analysis, impact models, liquidation/acquisition schedules, limit-order choice, or market making | [execution-design.md](references/execution-design.md) |
| TCA or model validation, simulation/backtest design, course coverage, source status, or maintaining this skill | [validation-and-sources.md](references/validation-and-sources.md) |

Load only the modules that own the decision. Market mechanics normally precedes execution design when order-state semantics are unclear. Validation is required before a strategy or policy is presented as supported by data.

## Workflow

1. Define the market-state representation and executable decision boundary.
2. Choose a benchmark and decompose costs without mixing spread, delay, impact, fees, and opportunity cost.
3. State the model's mechanism, units, horizon, and assumptions; include queue and fill assumptions when limit orders matter.
4. Estimate only from point-in-time data and separate calibration from evaluation.
5. Compare against a simple policy under identical constraints and stress size, liquidity, volatility, and regime.
6. Report uncertainty, sensitivity, failure modes, and what would be required for deployment.

## Invariants and boundaries

- A mid-price move after an order is not automatically causal impact.
- A simulated fill is not an executable fill without a queue and latency model.
- Do not transfer parameters across instruments, venues, horizons, or regimes without revalidation.
- Keep alpha, execution, inventory risk, and implementation latency as separate effects.
- Historical coursework is a method source, not present-market evidence.

This skill may analyze supplied data and implement research code when asked. It does not authorize live orders, exchange connectivity, production deployment, or investment recommendations. For implementation latency use `low-latency-quant-systems`; for broad empirical design use `ingenius-quant-finance`; for portfolio construction use the finance skill's portfolio/risk module.
