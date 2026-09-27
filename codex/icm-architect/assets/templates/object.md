---
type: object
id: <stable-id>
universe: unknown
status: stub
owner: <source-owner>
source_identity: <root/revision plus relevant dirty inputs>
configuration: <build/runtime variant>
dependencies: []
---

# <Product name> / <qualified symbol>

## Purpose and invariant

<One sentence and the load-bearing constraint; link to owning source/policy>.

## Shape and ownership

<Relevant fields/types/keys; units and grain if numeric; trust boundary if sensitive>.

## Evidence and connections

| Claim/typed edge | Path:line and symbol | Fingerprint/version | Observed/inferred/conditional |
|---|---|---|---|
| <claim> | <source> | <identity> | <status> |

## Change impact

- Direct: <consumer and evidence>.
- Transitive/conditional: <path and condition>.
- Inbound external consumers: <known or unresolved>.
- Not affected: <bounded scope and supporting evidence, or not established>.

## Frontier and refresh

<Unresolved wiring, assumptions, checks not run; invalidation triggers>.
