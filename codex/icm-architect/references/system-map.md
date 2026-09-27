# System map: an evidence-backed edit graph

Use for a body of work that later agents must navigate or change. For an immediate code question, first use [codebase-analysis.md](codebase-analysis.md); a persistent map is optional. Keep source authoritative and build only the slice that repays future retrieval.

## Placement and structure

Choose an authorized shelf beside existing orientation, such as `docs/map/`. Preserve existing instructions. Use the host's established entry filename; add one routing link, not generated twins that overwrite instructions.

A small tree needs only a catalog plus cards. Add `objects/`, `processes/`, and an `effects/CONTEXT.md` index only when populated and useful. Reuse [object](../assets/templates/object.md) and [process](../assets/templates/process.md) templates. Indexes route into cards; they do not duplicate their contents.

## Build in evidence-sized slices

1. Inventory in scope: runtime entrypoints, configurations, source owners, schemas, tests, generators, and consumers. Note naming collisions between product terms and code symbols.
2. Create a small catalog of actual questions and relevant cards. Unmapped areas remain an explicit frontier, not imaginary completed cards.
3. Add object cards for load-bearing entities/contracts and process cards for real movements. Cite source paths, symbols, lines, revision/fingerprints, and selected configuration.
4. Trace change impact through direct and transitive consumers, contract boundaries, configuration, generated artifacts, migrations, and tests. Stop when the claim is supported or mark the unresolved boundary.
5. Reverify decisive claims and index freshness; test a cold walk. Continue authorized analysis without artificial per-slice approval gates. Ask when a material policy, source mutation, migration, or scope choice needs the user.

## Two independent classifications

| Field | Values and meaning |
|---|---|
| `universe` | `live`: evidenced active wiring; `leftover`: evidenced superseded but still present; `ghost`: aspirational/stub; `unknown`: wiring unresolved |
| `status` | `stub`, `verified`, `stale`, `partial`: quality/freshness of this card |

Do not infer leftover/ghost solely from missing search hits. A verified card requires evidence for its stated scope at a recorded version, not merely a date. A current index can point at stale cards; validate at use.

## Object and process cards

Capture what an editor needs, not an exhaustive paraphrase of code:

- Purpose, owning source/symbol, and relevant invariant.
- Shape/units/grain/trust/ownership when material to the entity.
- Edges typed as reads, writes, calls, authorizes, registers, transforms, emits, or consumes; cite the evidence.
- Process input → transformations/control → output, with errors/retries and side effects where relevant.
- Change impact: direct, transitive, conditional, unknown. Include inbound consumers outside the repository when known.
- Evidence identity/read set and configuration; important assumptions and uncovered paths.

“Does not hit” must be a bounded negative claim with search/configuration evidence. When uncertain, use “not established.” Do not prescribe first-order-only impact: schema, event, or policy changes often propagate across several components.

## Invalidation and promotion

Use [runtime-model.md](runtime-model.md). Invalidate a card when a declared dependency, relevant directory membership, interface, build/configuration, or generator changes. Invalidate dependent cards/indexes transitively; if dependency coverage is weak, re-discover conservatively.

Keep tentative findings in run-local reports. Promote stable verified facts with source pointers, not private incident data or unsupported model conclusions. Summaries inherit sensitivity. A map is not a second specification.

## Cold walk

A fresh reader should locate the right card through the entry and at most two routing reads, then verify a consequential claim at the cited source. Check one cross-component impact, one conditional/unresolved edge, and one stale-card scenario. Entry/card brevity is a usability target; do not exclude decisive evidence to satisfy an arbitrary token count.

## Frequent failures

- Intent docs labeled as runtime behavior.
- A branch/commit/date standing in for dirty-tree or configuration identity.
- Search misses called dead code or no vulnerabilities.
- Every card asserting `verified` despite unresolved dynamic wiring.
- Impact stopping at immediate callers or ignoring incoming external consumers.
- Shared reports overwritten by another run; edited outputs still considered approved.
- Giant inventories that take longer to maintain than the questions they answer.
