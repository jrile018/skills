# Dynamic and Multi-Period Allocation

## Loading boundary

Read this module when current allocation affects future wealth, opportunities, liabilities, consumption, costs, or constraints. Do not load it for a one-period rebalance with no meaningful state transition.

## Model the state and timing

Define the state before writing Bellman or HJB equations. A state may include wealth, holdings, liabilities, predictive variables, regime beliefs, transaction-cost state, and time. Specify which controls are chosen before which returns or observations arrive.

For discrete time, write the transition and Bellman recursion with terminal utility or liability explicitly. For continuous time, state the controlled SDE, admissible controls, objective, and candidate HJB equation. Keep the control in the generator and preserve covariance and cross-derivative terms.

Distinguish:

- myopic demand from intertemporal hedging demand;
- state uncertainty from parameter uncertainty;
- rebalancing benefit from turnover and market impact;
- a liability hedge from a return-seeking allocation;
- a regime known at time `t` from a latent regime inferred from observations.

## Verification and implementation

- Check terminal and boundary conditions and whether the candidate value function has the required regularity.
- Verify the candidate control attains the HJB/Bellman optimum under admissibility conditions; a first-order condition alone is insufficient.
- Test limiting cases against a one-period or constant-opportunity solution.
- Simulate the complete policy with point-in-time state estimates and costs.
- Compare the dynamic policy with a static or periodic-rebalance baseline.
- Report policy instability, estimation burden, approximation error, turnover, and state misspecification.

Use `rigorous-mathematical-finance` when the theorem-level stochastic-control derivation is itself the deliverable. Return here only with a verified state equation, value equation, conditions, and candidate control to assess implementability and out-of-sample consequences.
