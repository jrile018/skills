# 18.642 course-grounded guide

Read this reference for detailed routing, tutoring and project design, source boundaries, and behavioral evaluation.

## Detailed map

| Financial problem | Mathematical objects | Required distinctions |
|---|---|---|
| Bonds and rates | discount factors, cash flows, curves, linear-rate models | price versus return; quoted versus effective rates |
| Quantitative equities | regression, exposures, residuals, covariance | prediction versus explanation; selection bias |
| PCA in finance | covariance/correlation, eigenvectors, scores | statistical direction versus stable economic factor |
| Counterparty and portfolios | objective, covariance, exposure, constraints | estimated input versus optimized decision |
| Time series and volatility | dependence, stationarity, conditional variance | historical/realized/conditional/implied volatility |
| Derivatives | stochastic process, replication, pricing measure, PDE/SDE | physical expectation versus arbitrage-free price |
| Machine learning | features, loss, validation, temporal splits | fit versus generalization; observation-time information |

## Learning workflow

- Diagnose prerequisites in calculus, linear algebra, probability, statistics, finance, and programming.
- Ask for the learner's attempt before replacing it.
- Give the smallest useful hint, then reveal additional structure progressively.
- Verify the result and ask for transfer to a changed example.
- For a project, require a precise question, data/source provenance, mathematical development, implementation or empirical evidence, limitations, and reflection.

The public course includes five problem sets, an optional investment game, a group lecture-note/presentation project, and a final paper. Do not treat the investment game as validation of a strategy.

## Empirical invariants

- Preserve observation dates and realistic publication lags.
- Separate training, selection, and final evaluation in time.
- Flag look-ahead, survivorship, revised data, and repeated testing.
- Stress covariance, factor, and forecast instability before consuming estimates downstream.
- Keep PCA components as statistical summaries unless economic interpretation has independent evidence.

## Source boundaries

- [Course home](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024/)
- [Calendar](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024/pages/calendar/)
- [Lecture notes](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024/resources/lecture-notes/)
- [Assignments](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024/pages/assignments/)
- [Week 12 unavailable-lecture notice](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024/pages/week-12/)
- Full research brief in the Ingenius repository: `research/courses/mit-18-642-quantitative-finance.md`

Guest lectures are attributed teaching sources, not current universal market facts. Browse when a time-sensitive claim matters.

## Behavioral evaluation

| Request | Expected behavior |
|---|---|
| “Build an 18.642 study plan for quant equities and risk.” | Activate; diagnose prerequisites and route through relevant blocks |
| “Give me a hint on this course PCA problem.” | Activate; use progressive hints and verify transfer |
| “Turn the volatility material into a reproducible project.” | Activate; define data timing, model, evaluation, and limitations |
| “What did the Millennium systematic-trading lecture teach?” | State that it is unavailable; do not invent content |
| “Optimize this lock-free queue.” | Do not activate; use performance engineering |

Output tests:

1. A coverage question mentioning PCA stays a provenance question unless technical analysis is requested.
2. Physical drift and pricing measure remain distinct.
3. Revised or future data in a backtest is flagged.
4. A broad request routes to only the needed blocks.
5. Unavailable lecture content is never reconstructed.

