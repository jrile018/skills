# Graphify and ICM-Informed Skill-Tree Networking

Use this reference when designing, updating, auditing, or navigating a complex parent skill with supporting modules or related separate skills. It defines how `$graphify` supplies a source-evidence graph and `$icm-architect` performs a navigability review of the separately derived skill tree.

## Operating Contract

Use the tools at different times:

| Situation | Required action |
|---|---|
| Creating or substantially restructuring a complex modular skill | Use an existing graph or run `$graphify --directed` from the root of an isolated copy, apply the modular classification tests, then use `$icm-architect` for an ICM-informed navigability review. |
| Auditing overlap, dependencies, or change impact | Query an isolated copy of the existing Graphify graph or use its read-only inline NetworkX fallback; update or rebuild only when the corpus is stale, the build is authorized, and the expected value justifies it. |
| Handling an ordinary request after the parent skill exists | Use the parent catalog and module contracts. Do not rebuild the graph. |
| Adding, removing, or promoting a module in an already graph-backed complex tree | Query or update its Graphify source graph, review the derived impact paths, revise the catalog, and rerun routing tests. |
| One short skill or an obvious small module split | Skip both integrations and use the ordinary modular tests unless the user explicitly requested Graphify or ICM Architect. |

Graphify discovers and records source relationships. The modular classification tests convert those observations into architecture candidates. ICM Architect then applies an ICM-informed navigability review; this is not an ICM workspace, form, or compliance claim. None decides activation boundaries automatically; the design brief must justify each boundary from user goals, inputs, outputs, and success criteria.

Graphify writes `graphify-out/` relative to the process working directory, its query preflight may write an interpreter sidecar, and it may dispatch semantic extraction workers. For a new build, create an isolated temporary corpus copy and set the process working directory to that copy's root. For a read-only query, copy the existing `graphify-out/` into a temporary root and run the query there, or use Graphify's inline NetworkX fallback without writing. Never run the query preflight from the audited target. Persist outputs in the target only when the user wants a maintained project graph.

If no fresh graph exists and a build, runtime installation, upgrade, or compatible orchestration path is unavailable, unauthorized, or disproportionate, do not block a design or narrow audit. State that Graphify did not run, derive the evidence map manually, and apply the ordinary modular tests. When the architecture remains complex and ICM Architect is available, invoke it for an ICM-informed cold walk over the manual map. Do not describe this fallback as graph-backed.

Graphify's orchestration snippets express intent but may lag the host's collaboration API. Call the available tools with their declared schema. On a Codex host where `spawn_agent` accepts `task_name` and `message`, use those fields, collect each result with `wait_agent`, merge returned JSON in memory, and do not call `close_agent` when that operation is unavailable. If semantic extraction is required and no compatible worker path exists, use the disclosed manual-map fallback rather than claiming a complete graph.

## Integration Procedure

1. Read this reference before graph construction so the source/derived schema boundary is clear.
2. For an existing fresh graph, query an isolated graph copy or use the read-only inline fallback with the graph root as the working directory. If no graph exists and the threshold is met, create an isolated corpus copy, set the working directory to its root, and invoke `$graphify --directed` on the corpus and current package. Treat installation or upgrade as a separate authorization boundary.
3. Review Graphify's extracted, inferred, and ambiguous relationships; do not convert confidence classes into facts.
4. Read [modular-skill-architecture.md](modular-skill-architecture.md) and classify every material candidate as parent guidance, a supporting module, a separate skill, or a runtime subagent.
5. Create the derived architecture map, then invoke `$icm-architect` for an ICM-informed review of its catalog, one-job boundaries, one-home-per-fact links, context loading, and cold walk. Record form as `N/A` unless the user separately requested a full ICM workspace. A valid outcome is to keep a saved skill and build no workspace.
6. Use the resulting parent catalog at ordinary runtime. Return to Graphify only for graph-backed changes, unclear impact paths, or architecture audits.

## Source Graph and Derived Architecture Map

Do not put architecture-only types or relations into Graphify's extraction schema. Graphify accepts its own fixed node and relation vocabulary. Preserve that native graph as the source-evidence layer, then derive a separate architecture map in the design brief.

### Graphify source layer

Use Graphify's supported `file_type` values and relations exactly as its skill defines them. Build new architecture graphs with `--directed`; if an existing graph is undirected, verify every directional translation against source before relying on it. Architecture-relevant signals commonly include:

- `references` and `cites` edges that identify source ownership or provenance.
- `implements` and `rationale_for` edges that connect behavior to an explicit reason.
- `conceptually_related_to` and `semantically_similar_to` edges that suggest overlap for human review.
- Hyperedges that show a concept spanning three or more source nodes.
- God nodes, community bridges, and weakly connected nodes that reveal central contracts or possible gaps.

These signals are not automatically `routes_to` or `requires` relationships. Inferred and ambiguous edges cannot establish a skill boundary without corroborating evidence.

### Derived architecture layer

After reviewing the native graph, classify material nodes into user goals, capabilities, evidence, parent guidance, supporting modules, separate skills, shared rules, and evaluations. Record architecture relationships in a separate Markdown or YAML map:

| Edge | Meaning |
|---|---|
| `grounded_by` | Capability or instruction is justified by evidence. |
| `routes_to` | Parent request condition selects a module or separate workflow. |
| `requires` | One module's output is a real prerequisite for another. |
| `shares_rule` | Several modules use one canonical cross-cutting rule. |
| `verified_by` | A node has an observable behavioral test. |
| `overlaps_with` | Two candidate owners may compete for the same request. |
| `conflicts_with` | Instructions or source claims disagree and require adjudication. |
| `delegates_when` | A runtime task may use a bounded worker; this is not a storage edge. |

For each derived relationship, cite the Graphify nodes or independent behavioral evidence that justify it and record whether the translation is verified or still proposed. A `references` edge may support `grounded_by`; a semantic-similarity edge may suggest `overlaps_with`; neither conversion is automatic. Derive `routes_to` from observable request conditions and `requires` only from a real input/output dependency.

The derived `routes_to` plus `requires` subgraph must be acyclic. Cross-links such as `grounded_by`, `shares_rule`, and `verified_by` may form a wider network, but they must not create circular loading instructions.

## Apply an ICM-Informed Review to the Derived Map

Invoke `$icm-architect` after the graph is reviewed and candidate nodes are classified with [modular-skill-architecture.md](modular-skill-architecture.md). Ask it for an ICM-informed navigability review using the catalog, one-job, one-home-per-fact, explicit-link, context-loading, and cold-walk ideas. This does not make the skill tree an ICM workspace. Respect its guardrail that a saved skill may be the correct rung: record form as `N/A` and do not create `CLAUDE.md`, `CONTEXT.md`, stage folders, or other ICM scaffolding unless the user explicitly requests a full workspace.

### One parent and supporting modules

When capabilities share one activation boundary and output contract, use the catalog-and-shelves pattern:

```text
parent-skill/
|-- SKILL.md                       small catalog and shared contract
|-- references/
|   |-- shared-rule.md             one canonical home for a shared fact
|   `-- modules/
|       |-- capability-a.md        one job and one explicit load condition
|       `-- capability-b.md
|-- scripts/                       deterministic checks only
`-- agents/openai.yaml             interface metadata, not routing content
```

Do not add nested `SKILL.md` files for supporting modules. The parent is the only discoverable entrypoint; module files are shelves reached through its catalog.

### Separate discoverable skills

When the derived map contains workflows with distinct user goals, triggers, permissions, or success criteria, make them self-contained sibling skills. Do not invent a discoverable parent solely to simulate hierarchy.

When several sibling skills share a packaged reference layer, centralize it only if the installation format guarantees the shared path. Otherwise, keep each skill portable and duplicate only the smallest stable invariant, with an explicit maintenance test. One-home-per-fact applies inside every independently runnable bundle.

### Subagents

Represent subagents only as a runtime overlay. A module may define `delegates_when`, assignment, expected result, synthesis rule, and stopping condition. A subagent is never a child node that stores course content or replaces a module contract.

## Parent Catalog Additions

Use the canonical parent-router and module contracts in [modular-skill-architecture.md](modular-skill-architecture.md). For a graph-backed tree, add only source-node provenance, derived incoming and outgoing edges, dependency rationale, graph freshness, and what should trigger a graph query or update. Do not maintain competing parent or module contracts here.

## Runtime Navigation

After the parent activates:

1. Match the request to the catalog's observable conditions.
2. Choose the smallest module set that owns distinct required decisions.
3. Follow `requires` edges in dependency order; otherwise keep modules independent.
4. Load shared rules once from their canonical home.
5. If no route fits, handle the request from the parent only when its shared contract is sufficient; otherwise ask one material question or state the limiting assumption.
6. If multiple routes overlap, resolve ownership before loading payload. Do not load every module as a substitute for deciding.
7. Query Graphify only for architecture, impact, or stale-map questions—not for ordinary use of a stable route.

Keep the parent plus selected contracts and inputs within a practical context budget. If navigation repeatedly needs most modules, the split is not providing progressive disclosure and should be reconsidered.

## Required Design Artifact

For a comprehensive networked design or audit, include this table for the material nodes. For a narrow impact audit, report only the affected path and its immediate neighbors.

| Node | Type | Parent or owner | Trigger or load condition | Incoming dependency | Outgoing route | Canonical evidence | Test |
|---|---|---|---|---|---|---|---|

Also report:

- Graphify corpus path, build or query status, and any health warnings.
- Extracted, inferred, and ambiguous relationships that materially affected the design.
- The ICM-informed review outcome, including whether the saved skill remains the correct rung or a separately requested workspace is justified.
- Graph-to-tree translations, including rejected promotions to separate skills.
- Dependency cycles, duplicate facts, dangling links, and unresolved overlaps.

## Validation

Run both graph and walk checks:

1. **Graph integrity:** All route and dependency endpoints exist; provenance is retained; ambiguous edges are disclosed; the route/dependency subgraph has no cycles.
2. **Cold walk:** From the parent, a new agent can select the correct module with the entrypoint plus no more than two reads.
3. **One home per fact:** Shared guidance lives once and other nodes link to it.
4. **Routing behavior:** Test each module alone, a valid multi-module request, a parent-only request, a near miss per module, and an ambiguous request.
5. **Change impact:** In an in-memory model or isolated temporary copy, add, remove, and promote one synthetic module; verify every affected route, dependency, and evaluation is identified. Never mutate the audited target for this test.
6. **Baseline:** Compare the routed tree with a monolithic skill. Retain the tree only if it improves context use, correctness, maintenance, or auditability enough to justify its complexity.

Do not treat a visually plausible graph, a successful structural validator, or agreement among subagents as proof that the architecture works. Validate observable routing and output behavior.
