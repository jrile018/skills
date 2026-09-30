# Architecture and provenance

## Chosen shape

This package has one discoverable parent skill and conditionally loaded reference modules. A module is stored guidance, not another discoverable `SKILL.md` and not a permanent agent.

```text
low-latency-quant-systems/SKILL.md
    ├── measurement-contract.md
    ├── trading-correctness.md
    ├── cpu-memory-compiler.md
    ├── numerical-kernels.md
    ├── concurrency-realtime.md
    ├── networking-time.md
    ├── system-architecture.md
    ├── delegation-routing.md
    ├── source-map.md
    └── evaluation-plan.md
```

The parent owns activation, the ordinary baseline and acceptance contract, safety boundaries, and final synthesis. Each technical module owns one decision family and only its domain-specific additions. `source-map.md`, this file, and `evaluation-plan.md` are maintenance references and are not normally loaded during task execution.

## Routing and dependencies

The runtime route is a directed acyclic graph:

```text
request
  → parent activation and scope
  → correctness contract, when trading state is touched
  → parent baseline and acceptance contract
  → one or more mechanism modules
       advanced measurement, only when experiment design is itself nontrivial
       numerical method → CPU implementation, when implementation follows a math decision
       network path → system placement, when architecture consumes network evidence
  → comparable correctness and performance gates
  → parent synthesis
```

Topical similarity does not create a dependency. A dependency exists only when a downstream decision consumes an upstream artifact. Independent modules may be investigated in parallel; tightly coupled diagnosis stays with one agent.

## Why this is not a skill per course

The evidence overlaps heavily. Several courses teach measurement, parallel scaling, memory behavior, or accelerator tradeoffs, while the trading sources constrain the same implementation through event and state semantics. One course skill per source would duplicate shared rules and create competing activation boundaries. One monolithic `SKILL.md` would load unrelated material for every task. The selected parent-plus-references design gives shared invariants one home and lets ordinary requests load only the modules that own their decisions.

## Boundary with the MIT 6.172 skill

`mit-6172-performance-engineering` owns general measured software-performance work and explicit MIT 6.172 study. This skill owns end-to-end trading-system work where performance must be reconciled with venue/event/order semantics, numerical kernels, real-time concurrency, networking/time, or hardware placement. For a generic image-processing loop, use the 6.172 skill. For a feed-to-book path or intraday risk kernel whose result affects trading state, use this skill; borrow the 6.172 measurement discipline through the shared contract rather than activating two competing parents by default.

## Graphify and ICM roles

Graphify is an authoring and maintenance tool. It maps the research corpus, reveals cross-source hubs, and tests whether the proposed module edges reflect the evidence. It does not select runtime modules and is not required on the user's machine.

ICM Architect supplies the information-architecture checks: one catalog, one home per shared fact, bounded cold-start navigation, explicit dependencies, and no cyclic shelf structure. It does not become a runtime dependency. A normal phase reaches its technical guidance from `SKILL.md` in at most two additional reads.

## Provenance pipeline

1. Record current institutional, vendor, protocol, and primary-research sources in dated dossiers.
2. Separate observed source claims from derived engineering guidance and note currentness or licensing limits.
3. Use Graphify to extract relationships from the research corpus.
4. Translate recurring decisions into modules; do not reproduce the source table of contents.
5. Apply the ICM cold-walk and single-home checks.
6. Test activation, non-activation, module routing, multi-module order, safety, and structural links.

The dated design and verification record is in [`evaluations/low-latency-quant-systems-2026-09-26`](../../../evaluations/low-latency-quant-systems-2026-09-26/). Rebuild that evidence when sources or module boundaries materially change.
