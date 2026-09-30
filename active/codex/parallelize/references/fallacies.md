# Parallelization Fallacies — A Catalog

Each entry has the same shape:
- **Definition** — what the fallacy is
- **Telltale signs** — how to spot it in a user's proposal
- **Counter-question** — what to ask
- **Recommended frame** — how to redirect

Some fallacies are tactical-altitude only, some strategic-altitude only, some apply at both.

---

## 1. Subdivision Premium

*(Both altitudes)*

**Definition.** Assuming that splitting work always helps. Treating "more parallel streams" as inherently better than "one focused stream."

**Telltale signs.** Proposal arrives as "let's split this into N streams" without ever interrogating whether 1 stream would be faster. The conversation skips straight to *how* to split.

**Counter-question.** "What would the timeline look like if you ran this as a single stream end-to-end? Walk me through it."

**Recommended frame.** The default is one stream. Splitting earns its place by passing both Parnas (stable contract) and Brooks (coordination tax < parallel throughput). One focused operator often beats two distracted ones — particularly when the work is small enough that the coordination tax dominates.

---

## 2. False Fork

*(Both altitudes)*

**Definition.** A split that *looks* parallel but contains hidden serialization. The streams appear independent but actually share a blocking resource — a reviewer, a shared infra change, a design decision still in flight, an integration point.

**Telltale signs.** "We'll have 3 streams running in parallel" — but on inspection, all 3 streams need the same person to review, or all 3 depend on a config change that hasn't been made, or 2 of them are blocked on the third.

**Counter-question.** "For each stream, list every external dependency it has — review, infra, design decisions, other streams' outputs. Now look at the union — what's actually shared?"

**Recommended frame.** If any shared dependency appears in ≥ 2 streams' lists, those streams aren't parallel — they're serial through that dependency. Either resolve the shared dependency *before* splitting, or restructure so each stream has its own (which often means fewer streams).

---

## 3. Span Overflow

*(Strategic)*

**Definition.** A lane wider than the operating engineer can keep mental model on. The engineer becomes a confused reviewer of agent output rather than a coherent orchestrator.

**Telltale signs.** Plan has 5+ agents working inside one engineer's lane. Engineer can't summarize what each is doing in two sentences. Decisions inside the lane start happening without the engineer noticing.

**Counter-question.** "If I asked you right now what each of your agents is currently working on and what decision is next, could you answer for all of them in 30 seconds?"

**Recommended frame.** Span of control for an operator running agents is roughly 2–4. Past that, lane width has overflowed and the operator is no longer providing coherent supervision — they're just rubber-stamping. If you need more agents, add another lane (with full coordination tax) — don't expand a single lane past human cognitive bandwidth.

---

## 4. More-Engineers Fallacy

*(Strategic)*

**Definition.** Treating "add headcount" as the lever for going faster. The classic Brooks failure mode, restated: communication cost grows superlinearly, so 3 engineers ≠ 3× throughput.

**Telltale signs.** Plan justifies its parallelism by counting humans rather than counting work. Phrases like "we need 4 engineers on this." No analysis of coordination tax, only of who is staffed.

**Counter-question.** "If you could only have N−1 engineers, how would you redesign the work to still hit the goal? And: would the answer to 'fewer engineers' include 'with agents inside their lanes'?"

**Recommended frame.** Brooks: communication paths grow as n(n−1)/2. The marginal throughput of the Nth engineer often goes negative past 3–4 on a single project. Before adding humans, exhaust the *agent-multiplier* path: can existing engineers run wider lanes with more agents inside?

---

## 5. Conway Mismatch

*(Both altitudes, especially strategic)*

**Definition.** Splitting work along a seam that doesn't match the natural architecture boundaries. The streams produce code that wants to talk across boundaries the architecture didn't intend, and integration time eats the parallel savings.

**Telltale signs.** Stream split picked for reasons other than module boundaries — "Alice knows the frontend so she'll take frontend, Bob knows the API so he'll take API" — when the actual change cuts vertically through both. Or: organizational convenience driving the split rather than architectural reality.

**Counter-question.** "Draw the module boundaries of the system. Now draw the proposed stream boundaries on top of them. Where do they cross?"

**Recommended frame.** Conway's Law: systems mirror the communication structure of the org that built them. If the stream split crosses module boundaries, you'll either build a system shaped like the temporary stream structure (bad, fossilizes accidental decisions) or pay heavy integration cost cleaning up the mismatch. Start from the architecture's natural seams and let them dictate the split.

---

## 6. Coordination Amnesia

*(Both altitudes)*

**Definition.** The up-front timeline estimate counts the parallel work but forgets the merge cost — rebases, integration testing, conflict resolution, design syncs.

**Telltale signs.** "If we split into 3 streams, this takes a third of the time." No line item for integration. No buffer for the discovery moments where streams realize they made incompatible assumptions.

**Counter-question.** "Walk me through the last week of this project — the part *after* all streams are 'done.' What happens? How long does it take?"

**Recommended frame.** The honest formula isn't *single-stream-time / N*. It's *single-stream-time / N + coordination-tax + integration-tax*. The integration tax especially is consistently underestimated; for non-trivial splits it's often 20–40% of the single-stream estimate, which can wipe out the parallel savings entirely.

---

## 7. Contract Leak

*(Both altitudes)*

**Definition.** The contract between streams keeps changing during execution. Each change is a sync event that costs more than it would have cost to just run the streams sequentially.

**Telltale signs.** User can't write the contract on an index card. User says things like "we'll align as we go" or "we'll figure out the interface in the first week." User describes the streams in implementation detail rather than interface terms.

**Counter-question.** "Write the contract between streams on one index card right now. Inputs each consumes, outputs each produces, what's hidden inside, merge protocol. Can you?"

**Recommended frame.** A contract that changes during execution isn't a contract — it's a coordination meeting that hasn't happened yet. Either invest the up-front time to lock the contract before splitting (the right call when the contract can be locked), or accept that this work isn't parallelizable yet and run it sequentially through the unstable parts. *The contract leaking is the most expensive failure mode of parallel work.*

---

## 8. Headcount One-Way Ratchet

*(Strategic)*

**Definition.** Staffing up is legible, visible, and feels like progress. Staffing down — even when agent multipliers make it correct — is invisible, hard to propose, and rarely happens.

**Telltale signs.** Proposal frames added headcount as the obvious move. The "could fewer humans with agents do this?" question is never raised. Existing org structure is treated as fixed input rather than as part of the design space.

**Counter-question.** "If your manager said you couldn't add anyone but could give existing engineers 2–3 agents each, what would the plan look like? Is that worse than the proposed plan, or actually better?"

**Recommended frame.** The agent multiplier reshapes the headcount math. Two engineers with 2–3 agents each is often equal-or-better throughput than 4 engineers with no internal parallelism — at half the coordination tax and half the burn rate. The legible move is "add humans"; the often-correct move is "widen lanes." Surface the wider-lanes option explicitly even if it goes against organizational defaults.
