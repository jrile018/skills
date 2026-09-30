# Course Map and Evidence Boundaries

## Module contract

- **Purpose:** Ground claims about course scope, prerequisites, sequencing, availability, and provenance.
- **Load when:** The answer depends on what MIT 18.S096/18.642 taught, how topics depend on one another, or what public material exists.
- **Do not load when:** A self-contained calculation requires no course-specific claim.
- **Inputs:** The user's target topic, background, and whether they want the 2013 course, 2024 course, or a combined path.
- **Output invariant:** Cite or name the supporting source status; label synthesis, extension, and unknowns.

## Provenance

The skill derives from the `jrile018/ingenius` research snapshot at commit [`4cd5ee0`](https://github.com/jrile018/ingenius/tree/4cd5ee039532aa8c1a4a42707a822a5be692e01a), which synthesizes public material for:

- [MIT OCW 18.S096, Fall 2013](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/)
- [MIT OCW 18.642, Fall 2024](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024/)

Use the snapshot as a research guide, not a substitute for the MIT materials. The snapshot is MIT-licensed by its author; linked OCW material retains its own terms.

The empirical module also uses a dated advanced-elective extension researched on 2026-09-26:

- [MIT OCW 14.384, Fall 2013](https://ocw.mit.edu/courses/14-384-time-series-analysis-fall-2013/)
- [MIT OCW 14.387, Fall 2014](https://ocw.mit.edu/courses/14-387-applied-econometrics-mostly-harmless-big-data-fall-2014/)
- [Stanford MS&E 448](https://web.stanford.edu/class/msande448/info.html)

These sources extend methods and validation; they do not change the two-course provenance of the original snapshot or imply institutional endorsement.

## Prerequisites and dependency spine

Expected foundations are multivariable calculus, differential equations, probability and statistics, and linear algebra. Working readiness means manipulating matrices, interpreting eigenvectors, integrating densities, computing conditional expectations, solving elementary differential equations, and reading regression output.

The Graphify-backed dependency spine is:

1. Linear algebra and probability support regression, factors, covariance, and stochastic processes.
2. Regression and time-series diagnostics support volatility, empirical portfolios, and model evaluation.
3. Covariance, factors, and constraints support portfolio/risk decisions.
4. Brownian motion and quadratic variation support Itō calculus and SDEs.
5. Itō/SDE reasoning plus replication support risk-neutral pricing, numerical valuation, rates, commodities, and credit.

This is a conceptual dependency map, not the literal lecture order.

## Coverage status

- The 2013 offering supplies broad statistics, time-series, portfolio/factor, stochastic-calculus, commodities, rates, credit, and counterparty material.
- The 2024 successor refreshes empirical and volatility work, carries forward portfolio and Black–Scholes material, and adds visible treatments of PCA applications, modern rates, margin optimization, biomedical financing, event markets, and machine-learning examples.
- Absence of a dedicated 2024 session does not prove a subject is absent from every resource.
- The 2013 Matrix Primer and FX-execution sessions lack enough public content for reconstruction.
- Several 2024 guest lectures and student presentations are unavailable or description-only. Do not infer their technical content.
- Student-project titles establish topic interest, not a complete instructor-taught module.

## Verification

When asserting course coverage, identify the offering, session/resource status, and whether the claim comes from published teaching material, a student-project list, or the research author's synthesis. For time-sensitive market or legal facts, use fresh authoritative sources rather than treating a dated slide as current.
