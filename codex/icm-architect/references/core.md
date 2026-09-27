# ICM core

## Principles

One stage owns one coherent job. Plain Markdown/JSON exposes handoffs. Load context by task, separate stable references from products, keep human edits inspectable, and configure reusable rules once. Small local scripts may handle mechanical work; a full orchestration framework is optional, not prohibited.

## Semantic hierarchy (not CPU cache levels)

| Layer | Typical artifact | Purpose |
|---|---|---|
| L0 | Existing host entry file | Identity, constraints, routing |
| L1 | Root `CONTEXT.md` | Workspace routing |
| L2 | Stage `CONTEXT.md` | Inputs, process, acceptance, review policy |
| L3 | `references/`, `_shared/` | Stable factory rules |
| L4 | Run-local outputs | Products and evidence |

These describe meaning, not residence, latency, trust level, or freshness. A current task can need material from all five layers. Each large reference collection may have its own small router. Avoid duplicating governing instructions across entry files; use a link where the host supports it.

## Contract

Use [stage-CONTEXT.md](../assets/templates/stage-CONTEXT.md). Exact paths distinguish source, reference, and previous-run inputs. Declare what cannot be read or changed, what constitutes success, and whether a human decision is required. Folder order is a visual aid; dependencies determine legal execution order.

For every repeatable pipeline, including sequential runs, store products at `runs/<run-id>/<stage>/`, not shared `stages/<stage>/output/`. A genuinely one-off task can retain its layout but must still validate completion and freshness. Never reuse a run namespace. See [runtime-model.md](runtime-model.md).

## Library rules

- A catalog holds pointers and tiny discriminators, not a second copy of the knowledge.
- Prefer a symbol plus repository-relative path and source fingerprint; line numbers help navigation but drift.
- A generated index is derived, not authoritative. Record its generation scope/version; rebuild when its inputs change. A generator does not prevent staleness or incomplete discovery.
- Names: `NN_kebab-name` for ordered stages; `_meta/`, `_shared/`, `_templates/` for support; stable IDs for records. Follow host conventions rather than gratuitously renaming.
- Closed schemas should include only fields that a person or tool uses. Add detail to high-risk boundaries, not every leaf.
- A human edit is a new input version. Preserve it and revalidate downstream dependencies; never silently overwrite it during regeneration.
- Do not schedule index rebuilds or export private knowledge without authorization. Derived patterns retain source sensitivity unless explicitly cleared.

## Working-set discipline

Start with routing + contract + primary slice + relevant constraints/tests. Expand when a concrete unresolved edge requires it; evict unrelated excerpts while retaining their evidence identities and paths. Do not discard a guard, error path, or business rule merely to hit a token target.

The original ICM examples use roughly 2k–8k tokens per stage; that is not a validated optimum across models or codebases. Measure correctness, omitted evidence, repeated reads, latency, and token cost. Repeatedly reopening the same material suggests a missing intermediate note or a badly chosen task boundary, not automatically a need for a larger prompt.

## Limits

Files are useful control surfaces for sequential and bounded delegated workflows. High-concurrency writers, durable job scheduling, remote state, and real-time services need appropriate infrastructure. Keep one coordinator for reconciliation; independent workers receive narrow tasks and explicit artifact ownership, not full copies of the entire context.
