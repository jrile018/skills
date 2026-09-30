# Delegation Routing

Load this reference only after the parent has activated, selected the owning modules, and decided that the request contains independent or staged workstreams worth separate contexts.

## Worker map

| Module ID | Exact worker reference | Assign when the bounded workstream owns | Required worker return |
|---|---|---|---|
| `course-map` | [course-map.md](course-map.md) | Course coverage, prerequisites, availability, or provenance | Supported coverage claims, source status, unknowns, and any prerequisite edge needed downstream |
| `empirical-research` | [empirical-research.md](empirical-research.md) | Data, estimation, forecasts, factors, PCA, ML, or time-respecting evaluation | Assumptions, information set, diagnostics, uncertainty, checks, and a clearly named output artifact if another worker will consume it |
| `portfolio-risk` | [portfolio-risk.md](portfolio-risk.md) | Allocation, exposures, risk measures, objectives, constraints, or implementation feasibility | Objective and feasible set, inputs used, robustness checks, residual risks, and sensitivity to upstream estimates |
| `stochastic-pricing` | [stochastic-pricing.md](stochastic-pricing.md) | Stochastic dynamics, replication, pricing measures, derivatives, rates, commodities, or credit valuation | Measure and assumptions, derivation or valuation, independent check, and exposures or parameters needed downstream |
| `learning-projects` | [learning-projects.md](learning-projects.md) | Tutoring, misconception diagnosis, study sequencing, assignments, or project design | Learner diagnosis, intervention or sequence, source boundary, and transfer/verification task |

These are supporting modules, not independently discoverable skills. A worker uses the assigned module as its local operating contract; it does not reinterpret the entire tree.

When a worker also needs an implementation or communication policy, read [policy-overlays.md](policy-overlays.md) and assign the exact overlay mode. The overlay refines worker behavior only after the domain route is fixed.

Choose the worker's primary module by the decision it owns, not by nouns in the prompt. A source-coverage worker does not also receive the empirical or pricing module merely because the named lecture topic is PCA or options. Add another module only for a separate requested decision and normally assign that decision to its own worker.

## Runtime graph

```text
parent orchestrator
|-- course-map ---------> learning-projects
|-- empirical-research -> portfolio-risk
|-- empirical-research -> stochastic-pricing
`-- stochastic-pricing -> portfolio-risk
```

An arrow is a dependency only when the downstream decision actually consumes the upstream output. Otherwise the selected workstreams remain independent and may run in parallel. Examples:

- A coverage audit and an unrelated option derivation can run in parallel.
- A PCA estimate that becomes a portfolio input must be validated before the portfolio worker uses it.
- A volatility forecast used by an option model must be validated before the pricing worker values with it.
- Pricing exposures that feed margin or counterparty optimization must be produced before the portfolio/risk worker optimizes them.
- A prerequisite-aware study plan needs course availability and prerequisite findings before final sequencing.

The route/dependency graph is acyclic. Do not invent reverse dependencies merely because two topics are related in the source graph.

## Spawn decision

Use one agent when the request is short, one coherent derivation, one tutoring conversation, or a tightly coupled cross-module argument whose parts cannot be judged independently.

Spawn when all are true:

1. At least two bounded work products or an independent solver/checker split exist.
2. Each worker can receive sufficient inputs and a checkable return contract.
3. The expected quality, error isolation, or wall-clock benefit justifies added tokens and synthesis.
4. The parent can state how the results will be reconciled and when work stops.

One worker may receive a small ordered module set when its work is intrinsically cross-domain. Do not split a dependency into simultaneous workers just to obtain one agent per module.

## Assignment contract

Every spawned task must state:

```text
Parent skill: ingenius-quant-finance
Primary module: <exact references/*.md path>
Additional allowed module: <path or none>
Policy overlays: minimal-correct-change=<full|guarded|off>; context-efficient-output=<compact|detailed|exact|off>
Overlay boundary: <domain invariants and evidence that must be preserved>
Forbidden modules/actions: <unneeded modules and side effects>
Inputs: <data, assumptions, upstream artifact, and dates>
Question: <one bounded decision>
Return: <assumptions, result, verification, uncertainty, and handoff fields>
Stop when: <observable completion or blocking condition>
```

Do not ask a worker to “handle its topic” or read the whole package. For a solver/checker pair, assign the same primary module but give distinct jobs: one produces the result; the other attacks assumptions, derivation, numerical behavior, or source fidelity.

## Parent synthesis

The parent:

1. checks that every result stayed within its module and permission scope;
2. compares assumptions, dates, units, measures, horizons, and definitions across workers;
3. resolves conflicts using source evidence or deterministic checks rather than majority vote;
4. passes only validated, explicitly labeled artifacts to downstream workers;
5. separates calculation, evidence, interpretation, and unresolved uncertainty in the final answer; and
6. stops when the requested deliverable is complete—workers may not broaden the task or authorize execution.

If a worker fails, retry only when the failure is transient and the retry remains in scope. Otherwise synthesize the verified partial result and disclose the gap.
