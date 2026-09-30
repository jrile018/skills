# Delegation routing

## Use workers only for a real task graph

Keep one agent when diagnosis is short, evidence is shared, or decisions are tightly coupled. Delegate when workstreams are independent enough to produce separate evidence records, or when a downstream task consumes a verified upstream artifact.

Examples:

- Run network-path measurement and numerical-kernel validation in parallel when neither changes the other's inputs.
- Have a correctness checker challenge a proposed low-level optimization independently.
- Complete the numerical algorithm/error contract before handing its kernel and benchmark artifact to a CPU specialist.
- Establish a timestamp/queue map before handing a network candidate to a system-architecture comparison.

Do not spawn one worker per module, duplicate the same open-ended prompt across agents, or treat consensus as validation.

## Worker contract

Assign each worker:

1. one decision or artifact;
2. exact input paths or captured evidence;
3. the one or two reference modules it must read;
4. semantic, numerical, temporal, and authorization boundaries;
5. a result schema: finding, evidence, uncertainty, rejected explanations, and next dependency;
6. a stopping condition.

A worker must not broaden permissions, mutate live systems, or substitute a synthetic benchmark without disclosure.

## Parent synthesis

The parent owns routing and the final answer. It checks that worker workloads and clocks are comparable, resolves contradictions from primary evidence or deterministic tests, enforces dependency order, and reports unresolved uncertainty. Do not average incompatible measurements.

Retain delegation only when a comparison against a single-agent run shows better error isolation, quality, or wall-clock time sufficient to justify extra context and synthesis risk.
