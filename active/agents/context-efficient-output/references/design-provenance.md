# Design Provenance

Load this reference only to audit, evaluate, or revise the policy.

## Source influence

The policy adapts selected context-economy ideas from [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) at reviewed commit `2fd153c67988e980fb0b2455c90832159a6a5a25`. The useful design ideas are:

- keep responses terse without damaging exact technical material;
- distinguish presentation compression from source-context transformation;
- retain recoverable originals when a lossy representation is used;
- fail open to the original material when transformation is unsupported or unverifiable; and
- evaluate net provider-billed savings rather than assuming shorter input wins.

This skill is an instruction-only adaptation. It does not copy or install Caveman's proxy, Engine, CCR SQLite store, middleware, hooks, or telemetry. Runtime components with different license terms remain outside this repository.

## Evidence and safety boundary

Caveman separates a response-style skill from runtime context processing. Ingenius preserves that separation. The local skill can govern how an agent writes and hands off results; it cannot honestly promise reversible context processing without an actual backing store and verified retrieval path.

Before adopting any future runtime integration:

1. review the exact component license and data flow;
2. resolve telemetry defaults from executable behavior rather than conflicting prose;
3. threat-model stored prompts, secrets, and recovered originals;
4. verify provider compatibility and byte-preserving failure behavior; and
5. run A/B trials that include transformation overhead, recovery failures, and answer quality.

No runtime-installation conclusion is implied by this policy skill.
