# Large-codebase analysis

Contents: Scope · Orient · Evidence slice · Critical paths · Challenge · Verify · Report

## 1. Establish the analysis envelope

State the concrete question: explain a feature, assess a change, investigate a defect, audit a risk, or design an improvement. Do not promise to understand every file. Default audits/explanations to read-only source access; creating requested reports is separate from permission to fix source or run unsafe workloads.

Record repository/root identity, revision, relevant working-tree edits and untracked/generated inputs, language/build variants, active configuration, and tool availability. For non-Git trees, use content fingerprints. A commit ID alone does not identify a dirty checkout. Distinguish checked-in intent, source implementation, configured deployment, and observed runtime behavior: each answers a different question.

Set a practical time/tool budget and acceptance conditions. Prioritize exposed trust boundaries, money/units, state ownership, high-fanout dependencies, recently changed code, and irreversible effects. Do not manufacture a numerical risk score without defensible inputs. Keep a short ledger: question → evidence acquired → unresolved edge → next useful action.

## 2. Orient without ingesting the tree

Read applicable workspace instructions, then a bounded inventory (`rg --files`, manifests, existing map). Locate languages, packages, executable entrypoints, build/test targets, schema/migrations, queue consumers, schedulers, deployment configuration, plugins, code generators, and external interfaces. Use file counts to plan scope, not as a measure of understanding.

Distinguish authored source, generated source, vendored dependencies, fixtures, archived code, and aspirational docs. Follow generators when generated code affects behavior. Check whether ignored/hidden files or symlinks hide relevant wiring; explicitly widen a search when warranted. Do not blanket-read secrets, dependencies, build artifacts, or binaries.

If a map exists, check its source identity before trusting its statements. Use stale cards only as navigation hints. If no map exists, an orientation note in the response is enough; persist it only when writes are authorized. Mapping the whole repository is not a prerequisite.

## 3. Build a task-shaped evidence slice

Use the cheapest tool that answers the current question. Escalate only when it reduces an actual ambiguity:

| Layer | Establishes | Does not establish |
|---|---|---|
| Exact path/literal search (`rg`) | Candidate locations and naming variants | Binding, reachability, safety, absence outside filters |
| Syntax/AST queries | Declarations, calls, joins, control syntax | Resolved dispatch or valid business policy |
| Language server / SCIP / compiler index | Symbol identity, references, implementations | Complete runtime graph or data-flow |
| Build/import/config graph | Wiring and selected build dependencies | All reflection, runtime loading, or deployed state |
| Static data/control flow (e.g. CodeQL) | Paths within its model | All feasible executions or absence of all defects |
| Focused tests/runtime traces | Behavior for exercised configurations and inputs | Exhaustive correctness or production equivalence |

Prefer existing tools/indexes. Record versions, analyzed files/builds, parse failures, unsupported languages, and custom-framework model gaps. If a tool is unavailable, use scoped manual tracing and state the limitation; do not claim it ran. Do not install large tooling or launch expensive whole-repository analysis without a task-specific reason and appropriate authority.

Resolve ambiguous names with qualified symbols, package, schema, and owning source. Follow definitions, callers/callees, implementations/overrides, configuration registration, tests, and persistence boundaries. Semantic/vector search is supplemental discovery, not evidence or a completeness oracle.

Maintain typed edges only where useful: calls, registers, configures, reads, writes, transforms, authorizes, emits, retries, owns. Each consequential edge gets a source citation and status: observed, inferred, conditional, unresolved. No graph database is required; a short table suffices.

Rank candidates by task anchors, resolved dependency proximity, evidence value, and unresolved risk; retain diversity for configuration, tests, and disconfirming paths. Pack coherent spans with their guards and source identities, not arbitrary token slices. If repeated retrieval is costly, use the implementation lessons in [efficient-retrieval.md](efficient-retrieval.md); do not build an index without a measured need.

If the available reader silently clips long definitions, the optional [source reader](source-reader.md) provides Python syntax selection or language-neutral line paging with hash-bound continuation. Existing tools are fine when they expose the same needed evidence. A complete syntax unit is not a complete dependency or evidence slice; inspect relevant external guards/configuration/callers separately. Generated read records do not prove reception or understanding.

## 4. Trace across boundaries

Walk forward from the input/entrypoint and backward from the output/sensitive effect. Meet at the same typed path. Include HTTP/RPC, jobs, CLI/admin routes, event consumers, frontend/backend schemas, SQL, queues, caches, generated clients, and external services that actually touch this slice.

At each boundary ask:

- Who selects the destination/handler/tenant/account/partition? From trusted context or supplied input?
- What contract changes: type, units, grain, schema version, lifetime, ownership, permissions?
- What is synchronous, delayed, cached, retried, duplicated, reordered, or partially committed?
- Which error/timeout/cancellation branch changes the outcome?
- Which reader, subscriber, report, or downstream aggregate consumes the result?

For security, numeric correctness, and repeated work, read [security-and-numerics.md](security-and-numerics.md). For architecture, inspect responsibilities, dependency direction/cycles, data ownership, failure domains, compatibility, migration/deployment order, observability, and operational cost. Cross-file disjoint edits can still break the same invariant.

Impact is not restricted to immediate callers. Traverse direct and transitive consumers until the relevant contract stabilizes or the scope/budget is reached. Mark conditional build/plugin paths. Unresolved external consumers belong in the frontier; ask about them only when necessary to decide safely.

## 5. Challenge hypotheses

A suspicious pattern is a lead, not a finding. Search for disconfirming guards, constraints, upstream validation, database policies, dead branches, feature flags, compensating transactions, alternate units, and caller contracts. Inspect whether tests assert semantics or merely mirror implementation.

For a candidate finding, assemble: trigger/preconditions → actual path → violated invariant → impact → strongest benign explanation → verification. Use a minimal counterexample where possible. Keep severity (impact/exposure) separate from confidence (quality of evidence). Do not mark every billing/security defect critical: calibrate to demonstrated reachability, scale, reversibility, and threat model; unknown production exposure remains conditional. Separate confirmed source behavior from conditional concerns and unverified runtime impact. Unknown policy is a question or hypothesis, not a confirmed defect.

For a negative claim, record search scope, filters, symbol/build coverage, unresolved dispatch, and specific paths checked. Say "no path found in the analyzed configuration" rather than "no vulnerability." No search hits never proves dead code; unconfigured is not the same as unreachable in every deployment.

## 6. Verify proportionally

Use source tracing first, then focused static checks, existing unit tests, small synthetic cases, property checks, and selected integration tests according to risk. Read commands before running repository scripts; audit authority is not permission for production writes, network probes, migrations, uploads, or dependency lifecycle scripts.

Record actual commands, input/configuration, result, and scope. Label not-run, failed, and unavailable separately. If no execution is possible, explicitly retain source-only status. Review test counterexamples at the contract boundary, not only within the changed function.

Before finalizing a claim or applying an authorized patch, recheck the relevant read set and configuration for changes. If stale, refresh evidence and rerun affected verification. A hash match validates declared bytes, not the completeness of dependencies or business assumptions. See [runtime-model.md](runtime-model.md).

## 7. Hand off usable conclusions

Lead with the answer/findings, not the browsing history. Each finding has location and symbol, source identity, precise path, expected vs actual behavior, impact, confidence, and verification status. Group duplicates by root cause without erasing affected entrypoints. Include benign controls and unresolved concerns where they prevent misinterpretation.

Keep the coverage summary small: covered domains/configurations; frontier; skipped tools/tests; relevant stale inputs; remaining questions. Budget exhaustion yields an honest partial result, not a clean bill of health. Complete-with-limitations means the agreed bounded audit finished, not the repository is defect-free.

Persist reusable cards only for stable, valuable paths using [system-map.md](system-map.md). Encode demonstrated architectural constraints as existing-tool checks when implementation is requested; propose tradeoffs before large redesigns. An architecture is good relative to its workload and constraints, not because it uses more layers or services.
