# Probability, Martingales, and No-Arbitrage

## Loading boundary

Read this module for filtered probability, stopping, martingale properties, admissible strategies, equivalent martingale measures, fundamental-theorem arguments, completeness, or semimartingale market structure. Do not load it for routine expectation arithmetic.

## Set the market model

State `(Omega, F, (F_t), P)`, the usual conditions if assumed, the traded price processes, numeraire, self-financing rule, and admissible strategy class. Define the exact arbitrage condition being used and whether time is discrete or continuous.

Use conditional expectation with sigma-algebras and integrability stated. Distinguish martingales, sub/supermartingales, local martingales, and class properties required for stopping or convergence. Check stopping-time hypotheses before applying optional sampling.

## No-arbitrage reasoning

State the relevant version of the fundamental theorem rather than saying only “no arbitrage implies risk neutral.” In a finite discrete model, separate linear feasibility from uniqueness. In continuous semimartingale models, name the no-free-lunch condition and topological or admissibility framework needed by the theorem.

Keep these implications distinct:

- existence of an equivalent pricing measure and absence of the relevant arbitrage notion;
- uniqueness of that measure and completeness under the applicable setting;
- replication of one claim and completeness for the full claim class;
- a deflator, local-martingale measure, and true-martingale pricing representation.

## Proof checks

- Verify measurability, adaptedness, predictability, and integrability at their point of use.
- Check self-financing algebra under the chosen numeraire.
- Test a finite-state special case or construct a counterexample when a hypothesis is dropped.
- Do not use terminal wealth strategies that violate lower-bound or admissibility requirements.
- Label whether the conclusion is existence, uniqueness, representation, attainability, or a bound.
