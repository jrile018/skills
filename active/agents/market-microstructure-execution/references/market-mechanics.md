# Market mechanics

## Loading boundary

Use for interpreting electronic-market state, not for choosing an optimal schedule before the state and execution rules are defined.

## Market-state contract

Record venue/session, instrument, tick and lot size, price-time or other priority, order types and modifiers, auction state, trade/quote condition codes, sequence numbers, timestamps, hidden or implied liquidity, and cancellation/correction rules. Reconstruct state deterministically before computing features.

Separate:

- quoted spread, effective spread, realized spread, and price impact;
- displayed depth from executable or latent liquidity;
- marketable flow from signed trade classification;
- public information from the agent's private state and latency;
- mechanical response from adverse selection and common information.

## Reasoning procedure

1. Name the mechanism that can produce the observed pattern.
2. Define an observable statistic and its timestamp alignment.
3. List competing explanations and measurement artifacts.
4. Stratify by venue state, liquidity, volatility, size, and time of day.
5. Test stability on later periods and abnormal regimes.

For limit-order fills, model eligibility, queue ahead, cancellations ahead, partial fills, latency, message loss, and exchange-specific priority. If unavailable, provide optimistic and pessimistic bounds rather than a point estimate.

