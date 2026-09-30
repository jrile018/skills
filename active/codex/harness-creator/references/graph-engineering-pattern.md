# Graph Engineering Pattern

Read this module when a reliable loop is no longer sufficient because the work contains meaningful branches, rollback, parallel fan-out/fan-in, checkpoints, or human approval.

## Adoption Test

A graph is usually justified when at least three of these are true:

1. The task decomposes into independently ownable work units.
2. Branch or rollback paths affect where execution must return.
3. Intermediate state is valuable enough to checkpoint and resume.
4. Every node can produce explicitly verifiable output.
5. Coordination savings exceed state, merge, review, and recovery overhead.

Many steps alone are not a reason to create a graph. Keep a linear deterministic sequence as a script or workflow. Keep a single maker-checker retry as a loop unless its routing becomes difficult to observe or repair.

## Graph Contract

Describe the executable structure in a `graph.md` or equivalent specification.

### Nodes

For each node record:

- Identifier and responsibility.
- Kind: deterministic function, tool, agent, or human gate.
- Required inputs and exact outputs.
- State fields it may read and write.
- Verification and timeout.
- Permission and isolation boundary.
- Idempotency or compensation behavior.

An agent node should contain the loop contract: goal, verification, persistent state, and stop conditions.

### Edges

For each edge record source, destination, trigger or predicate, payload, and whether it is a normal handoff, failure route, rollback, retry, fan-out, or fan-in. Avoid decisions that exist only inside an agent prompt when they determine system routing.

### Shared State

Define a schema and one owner for each field. Include requirements, artifact locations, revision/worktree, verification results, decisions, attempts, budgets, approvals, and timestamps as applicable. Persist a checkpoint after every state-changing node so interrupted work can resume without replaying unsafe effects.

### Routing

Express routes as testable predicates. Include success, partial success, retry, rollback to the node that introduced the failure, blocked, timeout, cancellation, and escalation paths. Define fan-in semantics explicitly: all, quorum, first-valid, or adjudicated merge.

### Anchors

Tie graph success to reality: executable tests, ground-truth datasets, production-safe observations, business outcomes, or human spot checks. Internal metrics alone can be optimized while the actual objective degrades.

## Design Sequence

1. Draw the current loop and expose every implicit decision edge.
2. Split nodes only where responsibility, context, permissions, or verification meaningfully differ.
3. Define the shared-state schema and field ownership before parallel execution.
4. Add rollback to the producing layer, not automatically to the latest node.
5. Add fan-out only for independent tasks and an explicit fan-in standard.
6. Add a human gate before irreversible, high-impact, ambiguous, or policy-sensitive actions.
7. Add checkpoints, replay keys, retry limits, compensation, and observability.
8. Run one path at a time, then failure paths, then parallel paths. Compare the live trace with the written graph.

## Structural Failure Checks

- **Metric gaming:** Can a node improve its score while harming the real outcome?
- **Upward blindness:** Which node can question the goal or frozen assumptions?
- **Loop conflict:** Can two optimizing loops change the same state or pursue incompatible targets?
- **State races:** Can parallel writers update one field without arbitration?
- **Dead routes:** Is every emitted state accepted by at least one outgoing edge?
- **Unbounded cycles:** Does every cycle have progress evidence and a hard exit?
- **Review overload:** Does fan-out create more accepted work than humans can understand and integrate?

## Minimal Specification Shape

```markdown
# Graph

## State schema
| Field | Type | Owner | Readers | Persistence |

## Nodes
| Node | Kind | Input | Output | Verification | Timeout |

## Edges
| From | To | Predicate | Payload | Route type |

## Safety and recovery
- Budgets:
- Retry limits:
- Checkpoint key:
- Rollback or compensation:
- Human approval gate:
- Cancellation behavior:

## Anchors and observability
- Ground-truth checks:
- Per-node events and artifacts:
- End-to-end success measure:
```

## Acceptance Checklist

- Every route endpoint exists and every cycle is bounded.
- Shared-state writers, merge semantics, and concurrency constraints are explicit.
- Failure returns to the responsible layer when possible.
- Checkpoints allow safe resume; retries cannot duplicate irreversible effects.
- Human approval includes evidence, choices, consequences, timeout, and default action.
- At least one anchor measures the real outcome rather than an internal proxy.
- Recorded traces match the declared nodes and edges.
- Added coordination demonstrably earns its orchestration cost.
