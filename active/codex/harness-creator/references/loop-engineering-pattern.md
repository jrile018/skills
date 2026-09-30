# Loop Engineering Pattern

Read this module when the user wants an agent to keep working without a human prompting every step. A loop builds on a working harness; it does not repair missing instructions, state, or verification by itself.

## Choose the Loop Type

| Shape | Trigger | State progression | Stop condition | Good fit |
|---|---|---|---|---|
| Finite goal loop | One explicit start | Accumulates toward an end state | Verified goal, budget exhausted, or blocker | A bounded implementation or cleanup goal |
| Scheduled monitor | Timer | Runs are usually independent | Manual disable, no-op exit, or per-run timeout | CI, dependency, or status checks |
| Event-driven handler | External event | One state transition per event | Event handled or retry/escalation limit | PR, issue, webhook, or incident response |

Do not use a stateless scheduled monitor for work that must accumulate toward a finish. Do not automate a task whose success cannot be tested, side effects cannot be bounded, or required permissions are unresolved.

## Minimal Loop Contract

Define these before scheduling or dispatching unattended work:

1. **Goal** — an observable end state, not merely an activity.
2. **Starting state** — repository revision, active item, required context, and known constraints.
3. **Maker** — the role permitted to change artifacts.
4. **Checker** — an independent context that can reject the maker's output.
5. **Verification** — deterministic commands or observable checks; prefer these to model judgment where possible.
6. **Persistent state** — current round, evidence, failures, next action, and ownership outside the conversation.
7. **Stop conditions** — success plus hard limits for rounds, time, cost, repeated failure, and blocked dependencies.
8. **Escalation** — what requires a human, the evidence to present, and whether the loop pauses, rejects, or rolls back.
9. **Permissions** — permitted paths, commands, external systems, and forbidden mutations.

The maker may run basic checks, but it does not certify its own work. The checker should receive the goal, diff or artifacts, acceptance criteria, and verification surface—not the maker's self-justification as ground truth.

## Round Protocol

Each round should be replayable:

1. Read the persisted goal and prior state.
2. Select one bounded next action.
3. Let the maker change the isolated work surface.
4. Run deterministic verification and independent review.
5. Persist artifacts, commands, results, failures, and the proposed next action.
6. Stop, escalate, or begin another round according to explicit routing rules.

Switch approach or escalate when the same failure recurs without material progress. A hard retry limit is mandatory for unattended mutations.

## State Record

At minimum, persist:

```markdown
# Loop State

- Goal:
- Started:
- Current round:
- Status: in_progress | completed | blocked | failed | stopped
- Budget used / remaining:
- Current revision or worktree:

## Latest round
- Maker action:
- Files or systems changed:
- Commands run:
- Checker result: pass | fail | partial
- Evidence:
- Failure signature:
- Next route:
- Human decision required:

## Recurring failures
- Failure, first seen, rounds seen, attempted approaches
```

## Add Primitives Only as Needed

- **Automation** wakes the loop by timer or event.
- **Isolation** uses a branch, worktree, sandbox, or other separate write surface.
- **Skills** preserve reusable methodology and local conventions.
- **Connectors** expose external state or actions under explicit permissions.
- **Subagents** separate maker, checker, and independent research.
- **External state** carries memory across every run and is the foundation for the other primitives.

Start with a finite goal and persisted state. Add a schedule only after one manual round succeeds. Add parallelism only when work units and ownership are truly independent.

## Risks to Measure

- **Verification debt:** output grows faster than trustworthy checks.
- **Comprehension rot:** maintainers no longer understand the generated system.
- **Cognitive surrender:** automation substitutes for judgment instead of amplifying it.
- **Context or token blowout:** every round reloads or accumulates unbounded history.

Track completion rate, false passes, repeated failures, human interventions, time/cost per accepted result, and review backlog. Stop expanding autonomy when review capacity becomes the bottleneck.

## Acceptance Checklist

- The goal is machine-checkable or tied to a named human decision.
- Maker and checker are separated for stopping decisions.
- State survives session loss and records verification evidence.
- Every mutation has a bounded permission surface.
- Success, blocked, repeated-failure, time, cost, and cancellation exits are defined.
- One observed manual round passes before scheduling or self-feeding begins.
