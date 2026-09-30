# Robustness and sensitivity

## Loading boundary

Use when input uncertainty, regime change, regularization, or constraint stress can alter the selected action.

## Procedure

1. Identify uncertain parameters and how they were estimated.
2. Define plausible perturbations, scenarios, confidence regions, or ambiguity sets with provenance.
3. Evaluate solution turnover, active constraints, objective degradation, and feasibility under perturbation.
4. Compare nominal, regularized, robust, and simple baseline decisions.
5. Report the price of robustness and which assumptions dominate it.

Do not disguise arbitrary conservatism as statistical confidence. Robust uncertainty sets, stochastic scenario distributions, chance constraints, and distributionally robust ambiguity sets answer different questions.

For portfolio or execution inputs, expect estimated means and impact coefficients to be less stable than the optimizer output suggests. Prefer shrinkage, turnover/control penalties, exposure bounds, and scenario stress when justified by the decision—not as universal defaults.

When infeasible, produce an irreducible or prioritized conflict explanation where tooling permits; do not silently relax hard constraints. When a soft constraint is introduced, expose its penalty and realized violation.

