# Control, Optimal Stopping, and Incomplete Markets

## Loading boundary

Read this module for utility maximization, continuous- or discrete-time portfolio control, Bellman/HJB equations, American-style stopping, dual methods, or incomplete-market prices and hedges. Do not load it for a routine static allocation.

## Control problems

Define state, control, controlled dynamics, admissibility, objective, and terminal or boundary data. Derive the Bellman or HJB equation from the dynamic programming principle and state the regularity or viscosity framework required. A maximizing first-order condition is only a candidate until a verification theorem or other sufficiency argument applies.

For Merton-style problems, preserve wealth constraints, utility domain, and covariance structure. Separate consumption and terminal-wealth objectives. Identify myopic and intertemporal-hedging components only when the derivation supports that decomposition.

## Optimal stopping

Define the stopping-time class and reward process. Relate value to the Snell envelope or the appropriate variational inequality. Check exercise, continuation, value matching, and smooth fit only where smooth fit is justified; it can fail.

## Incomplete markets and duality

When an equivalent martingale measure is not unique, do not select one without an economic or optimization criterion. State whether the output is a superhedging bound, utility-indifference price, minimal-martingale construction, variance-optimal hedge, or another selection. For convex duality, define primal and dual domains, conjugate utility, feasibility, and attainment assumptions.

## Checks and handoff

- Verify candidate controls or stopping rules against the original objective and admissibility constraints.
- Test special cases with known solutions and inspect boundary behavior.
- Distinguish exact characterization from numerical approximation.
- Report whether incompleteness creates a range, residual risk, or preference-dependent value.

If the requested endpoint is an implementable allocation under estimated states, costs, and constraints, pass the verified state dynamics, value equation, candidate policy, and assumptions to `advanced-portfolio-theory`.
