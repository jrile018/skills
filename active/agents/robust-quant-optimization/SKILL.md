---
name: robust-quant-optimization
description: Formulate, solve, and verify constrained, convex, robust, or stochastic optimization problems in quantitative research and trading systems. Use when objective, constraints, duality, conditioning, uncertainty, or solver correctness is the decision. Not for generic mathematical exercises, unconstrained model fitting, portfolio advice, or low-level kernel tuning.
---

# Robust Quant Optimization

Convert the real decision into a dimensionally consistent optimization problem, then verify both mathematical validity and numerical behavior. A solver status is evidence, not proof that the intended problem was expressed or that estimated inputs are stable.

## Establish the contract

Define decision variables, objective, constraints, units, horizon, uncertainty set or distribution, tolerance, data provenance, and operational use. Identify which requirements are hard constraints and which are preferences. Record scale, sparsity, frequency, and latency only when they affect method choice.

## Route narrowly

| Observable request | Read |
|---|---|
| Formulation, convexity, KKT/duality, decomposition, solver selection, or translating a financial decision into a program | [formulation-and-solver.md](references/formulation-and-solver.md) |
| Parameter uncertainty, regularization, robust/stochastic optimization, sensitivity, infeasibility, or regime stress | [robustness-and-sensitivity.md](references/robustness-and-sensitivity.md) |
| Numerical verification, evaluation cases, course/source coverage, or maintaining this skill | [validation-and-sources.md](references/validation-and-sources.md) |

Use no module when a short self-contained derivation is sufficient. Load robustness only when uncertain inputs or stability change the decision; do not add it as ceremony.

## Workflow

1. Write the problem before naming a solver: variables, domains, objective, constraints, parameters, and units.
2. Classify convexity and identify transformations or relaxations. Label approximations and lost guarantees.
3. Select an algorithm compatible with structure, scale, accuracy, and warm-start or online requirements.
4. Scale the data; state stopping criteria and solver tolerances.
5. Verify primal feasibility, objective reconstruction, residuals, and—when applicable—dual feasibility, complementarity, and the duality gap.
6. Perturb uncertain inputs, compare a simple baseline, and report infeasibility or instability rather than forcing a precise answer.

## Invariants and boundaries

- Never invert a matrix merely to express a solve; consider factorization and conditioning.
- Do not call a nonconvex local solution globally optimal without a valid certificate.
- Estimated returns, covariances, impacts, and scenarios carry uncertainty into the optimizer.
- Tight solver tolerance does not repair misspecified data or constraints.
- Preserve financial, operational, and numerical units across transformations.

Use `ingenius-quant-finance` for finance-model interpretation and portfolio advice boundaries, `market-microstructure-execution` for impact or execution mechanisms, and `low-latency-quant-systems` only when the formulated problem's implementation is measurably performance-bound. This skill does not authorize trades or production changes.
