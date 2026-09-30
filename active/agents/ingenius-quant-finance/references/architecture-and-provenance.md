# Architecture and Provenance

Load this file only when auditing, maintaining, or extending the skill tree.

## Selected architecture

This package is one discoverable parent skill, five conditional domain modules, and four orchestration/maintenance references (`delegation-routing.md`, `policy-overlays.md`, `architecture-and-provenance.md`, and `evaluation-plan.md`). It has exactly one `SKILL.md`; none of these references is a nested skill.

Why this shape:

- One monolithic file would load unrelated empirical, portfolio, pricing, and tutoring detail on every request.
- Separate discoverable skills would create overlapping activation boundaries because the modules share the same course corpus, assumptions, safety boundary, and verification contract.
- One subagent per topic would confuse stored knowledge with runtime execution and add synthesis cost without independent workstreams.

Promote a module to a separate skill only after realistic requests show a distinct standalone goal, inputs/outputs, success criteria, and non-overlapping evaluation set.

## Parent-to-module network

```text
SKILL.md (activation, shared workflow, invariants)
|-- course-map.md -------- provenance, prerequisites, coverage boundaries
|-- empirical-research.md - estimation, diagnostics, time-respecting evaluation
|-- portfolio-risk.md ----- exposure, objectives, constraints, robustness
|-- stochastic-pricing.md - measures, replication, dynamics, valuation
|-- learning-projects.md -- tutoring, sequencing, assignments, transfer
|-- delegation-routing.md - conditional parent-to-worker routing overlay
|-- policy-overlays.md ---- optional worker implementation/output policies
|-- architecture-and-provenance.md - maintenance-only structure audit
`-- evaluation-plan.md ---- validation-only test contract
```

`delegation-routing.md` is a runtime overlay reached only when the parent has already selected modules and justified subagents. It maps each bounded worker to an exact module contract, keeps independent nodes parallel, stages real dependency edges, and returns synthesis ownership to the parent.

`policy-overlays.md` is one level below that delegation decision. It can assign the sibling `minimal-correct-change` and `context-efficient-output` skills with explicit modes, but those policies cannot select a domain module, relax its invariants, or authorize an action. The precedence is user and safety requirements, then domain contract, then worker contract, then optional policies.

Material cross-links:

- Empirical research → portfolio/risk when estimated factors, means, covariance, or backtests feed an allocation.
- Empirical research → stochastic pricing when volatility, curve, or model parameters are estimated.
- Course map → learning/projects when prerequisites or source availability determine a study plan.
- Stochastic pricing → portfolio/risk when valuation exposures feed margin, counterparty, or hedge optimization.

These links are directional routing dependencies, not instructions to load both modules every time.

## Parent-to-worker overlay

```text
parent selects modules and retains synthesis
|-- independent route A ------> worker A reads exact module A --|
|-- independent route B ------> worker B reads exact module B --|--> parent verifies and synthesizes
`-- upstream module worker --> validated artifact --> downstream module worker --'
```

The overlay does not create one permanent agent per topic. A worker exists only for a bounded workstream with a result contract and stopping condition. A dependency is staged rather than parallelized; a tightly coupled argument stays with one agent even when it reads two modules.

## Graphify result

Graphify analyzed the five source Markdown files: 52 nodes, 67 edges, and 6 communities. The health check found no missing/dangling endpoints, self-loops, or collapsed edges. The principal communities were quantitative foundations, stochastic-pricing applications, learning/projects, modern portfolio applications, course scope/evidence, and risk-neutral pricing.

The material edges that influenced the design were:

- the quantitative dependency chain from linear algebra/probability through empirical and stochastic methods;
- the bridge from Brownian motion/Itō/SDEs to risk-neutral pricing;
- the 2013-to-2024 continuity in volatility, portfolio management, and Black–Scholes;
- evidence/availability boundaries as a cross-cutting concern;
- empirical assignments and case studies as a learning layer rather than a lecture-per-module hierarchy.

Graph community labels were treated as evidence, not copied mechanically into modules. The graph's generic token-reduction benchmark could not match its sample questions to this domain and remains unvalidated.

A routing-focused Graphify query found related bridges between PCA and portfolio management, volatility and risk-neutral valuation, and the 2024 course and the updated study path. Those paths were undirected and partly similarity-inferred, so they were not treated as execution dependencies. Runtime arrows were defined only where a downstream decision consumes an upstream artifact. This keeps Graphify as construction evidence rather than allowing semantic proximity to spawn workers.

## ICM review

The package uses the ICM knowledge-bundle pattern within Codex skill constraints:

- `SKILL.md` is the small catalog.
- `references/` is the stable knowledge shelf.
- Each domain module has one job, explicit load/do-not-load conditions, inputs, and an output invariant. Maintenance references are routed by their audit or validation purpose instead.
- The delegation reference is a conditional orchestration shelf: it names exact worker inputs/outputs and leaves domain knowledge in the owning modules.
- The policy-overlay shelf owns cross-cutting worker modes; the two policy skills remain independently discoverable siblings because implementation economy and communication economy are useful outside quantitative finance.
- Shared activation, safety, and interpretation rules are canonical in the parent. Domain modules contain only the operational checks needed to apply those rules to a task.
- The normal cold walk reaches any operational module from the parent in one additional read. A delegated walk uses at most two: the delegation contract, then the assigned module.

The source snapshot, Graphify artifacts, earlier baseline, and final skill are separated at the repository level so evidence, analysis, comparison, and product do not blur together.

## Maintenance protocol

1. Change the source corpus only in `source-material/`; preserve source dates and licensing.
2. Run Graphify on the exact source corpus when material is added or relationships change. Record graph health, new/removed material edges, and ambiguities.
3. Use ICM Architect to review module ownership, one-home-per-fact, routing depth, and the cold walk.
4. Update the smallest affected module and its routing/evaluation cases.
5. Run structural validation and held-out activation, routing, and output tests.
6. Re-run subagent ablation only if a new task creates genuinely independent workstreams.

Do not run Graphify or ICM during ordinary finance questions. Their role is skill-tree construction and maintenance; the compiled routing table handles normal navigation.
