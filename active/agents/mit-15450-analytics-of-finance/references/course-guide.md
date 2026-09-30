# 15.450 course-grounded guide

Read this reference for method checks, cross-block handoffs, source boundaries, tutoring, and behavioral evaluation.

## Method checks

### Pricing and Monte Carlo

- Establish no-arbitrage, replication, or pricing-measure assumptions before computation.
- Specify payoff, state dynamics, numeraire, discounting, and completeness limitations.
- Report sampling error and test convergence against analytical or special-case benchmarks.
- Document bias from time discretization or approximation.
- Use control variates or other variance reduction only with a justified estimator.

### Dynamic portfolio choice

- State state variables, controls, objective/utility, constraints, transitions, and terminal condition.
- Verify the Bellman recursion or optimality condition.
- Compare a numerical policy with an analytical or simplified benchmark.
- Stress preferences, estimated dynamics, constraints, and boundary conditions.

### Econometrics and inference

- State the likelihood or moment conditions and identification argument.
- Match standard errors and resampling to serial dependence and heteroskedasticity.
- Report economic magnitude alongside statistical significance.
- Preserve the observation-time information set.
- Diagnose residuals, parameter stability, and conditional variance.

### Volatility

Distinguish realized, historical, conditional, forecast, and implied volatility. State the horizon, sampling scheme, model, and use. A fitted conditional model is not automatically the appropriate pricing or risk input.

## Cross-block handoff

An empirical stage should return:

- dated data and information-set definition;
- parameter estimates and covariance/uncertainty;
- diagnostics and rejected specifications;
- forecast horizon and conditions;
- limits on downstream use.

A pricing or optimization stage must consume that artifact without silently changing the data, measure, horizon, or assumptions. If it needs a different object, return to estimation explicitly.

## Course map and provenance

The public Fall 2010 sequence covers arbitrage-free pricing, stochastic calculus, Monte Carlo, three stages of dynamic portfolio choice, parameter estimation, standard errors/tests, bootstrap, and volatility models. Public resources include MATLAB examples, six problem sets, recitations, and an exam.

- [Course home](https://ocw.mit.edu/courses/15-450-analytics-of-finance-fall-2010/)
- [Syllabus](https://ocw.mit.edu/courses/15-450-analytics-of-finance-fall-2010/pages/syllabus/)
- [Lecture notes and code inventory](https://ocw.mit.edu/courses/15-450-analytics-of-finance-fall-2010/pages/lecture-notes/)
- [Resource download](https://ocw.mit.edu/courses/15-450-analytics-of-finance-fall-2010/download/)
- Full research brief in the Ingenius repository: `research/courses/mit-15-450-analytics-of-finance.md`

Do not infer modern library APIs, market conventions, regulation, or production readiness from this offering.

## Behavioral evaluation

| Request | Expected behavior |
|---|---|
| “Estimate volatility with uncertainty and feed it into Monte Carlo pricing.” | Activate; empirical artifact precedes pricing |
| “Derive and numerically verify this continuous-time allocation problem.” | Activate; require state, objective, constraints, and terminal condition |
| “Audit the GMM estimate used by this portfolio optimizer.” | Activate; examine identification, errors, diagnostics, and sensitivity |
| “What is a bond?” | Do not activate |
| “Why do hedge-fund strategies become crowded?” | Do not activate; use Adaptive Markets |

Output tests:

1. Reject physical-drift substitution for a risk-neutral pricing object.
2. Flag a bootstrap scheme incompatible with serial dependence.
3. Stop or bound a dynamic program with no terminal condition.
4. Propagate estimation uncertainty rather than report false downstream precision.
5. Distinguish historical teaching code from a production implementation.

