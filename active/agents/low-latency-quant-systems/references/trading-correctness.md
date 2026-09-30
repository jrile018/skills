# Trading correctness

## Purpose and loading boundary

Use this module when performance work touches market data, order books, replay, orders, fills, execution, routing, positions, cash, P&L, or point-in-time research data. Do not load it for a numerical kernel whose finance semantics are outside the optimized boundary.

## Event and replay invariants

Define the venue/protocol semantics and verify, as applicable:

- sequence gaps, duplicates, resets, snapshots, incremental recovery, and reconnect behavior;
- event-time and receive-time ordering, with an explicit tie policy;
- nonnegative quantities and valid order-book transitions;
- deterministic replay for the same input, configuration, and seed where promised;
- causal use of information available before each decision;
- explicit limits on reconstructing hidden or iceberg liquidity.

Do not sort away an observed ordering problem or silently discard zero-price-change trades, cancels, rejects, or partial fills merely to simplify the hot path. For venue protocols, pin the revision and derive parser/state-machine oracles from the actual specification.

## Order, execution, and accounting invariants

Use a documented state machine for order lifecycle and reject illegal transitions. Ensure cumulative fills never exceed order or parent quantity. Reconcile after each event:

```text
position = initial_position + signed_fills
remaining_target = target_quantity - cumulative_fills
cash changes agree with fills, prices, fees, and rebates
P&L agrees with the declared mark and accounting convention
```

For finite-horizon execution, make terminal completion or terminal inventory policy explicit. A simulated fill must respect side, price, displayed or modeled liquidity, time availability, queue/fill model, venue rejects, and latency. Report implementation shortfall or net objectives rather than midpoint-only paper profit.

## Research and risk invariants

Preserve point-in-time datasets, corporate-action logic, cost assumptions, constraints, seeds/scenarios, and chronological splits. Track impact, slippage, adverse selection, and parameter sensitivity when they affect the strategy. An optimization that changes aggregation order or precision must remain within a downstream error/risk budget.

## Domain-specific authorization reminder

The parent's authorization boundary is canonical. This module adds one domain check: keep test endpoints, credentials, and live systems outside the benchmark unless a separately authorized operational workflow explicitly places them in scope.
