---
name: parallelize
description: Pressure-test parallel-work proposals against Brooks's Law and Parnas information hiding before splitting. Use when proposing to run multiple Claude tabs on one task, staff multiple engineers on one project, or carve architecture into parallel workstreams — surfaces contract leaks, coordination tax, and the often-correct "fewer humans, wider lanes" inversion.
---

# Parallelize

Pressure-test plans to split work across parallel streams — whether agent tabs in your session or engineers in an org. Most parallelization proposals fail one of two tests: the contract between streams isn't actually stable (Parnas), or the coordination tax exceeds the parallel throughput (Brooks). This skill forces both tests before you commit.

## When to invoke

The user is proposing to:
- Run multiple Claude/agent sessions on parts of one task
- Staff multiple engineers on one project, each potentially running agents
- Decompose an architecture into parallel workstreams
- Add headcount or agent capacity to "go faster"

## Step 1 — Establish the proposal and altitude

One sentence: *what is being split, into how many streams, and who/what runs each stream?*

Then force the altitude:

- **Tactical (code-level):** one human, multiple agent tabs/sessions, hours-to-days horizon. Cost of a bad split = your context-switching tax and a messy merge.
- **Strategic (system-level):** multiple engineers, each potentially orchestrating agents inside their lane, weeks-to-quarters horizon. Cost of a bad split = headcount waste, integration hell, Conway-mismatch architecture.

The altitude determines which fallacies dominate. Don't proceed until it's named explicitly. If the user is operating at both altitudes, run the skill twice — once per altitude — rather than blending.

## Step 2 — Map the work and locate the contract

Force a complete enumeration of:
- The work to be done (every component, surface, or step — not just the parts being split)
- For each proposed stream: what it owns, what it depends on, what it produces
- Shared resources across streams: state, infra, review queues, integration points, design decisions still in flight

Then run **the Parnas test**: *write the contract between streams on a single index card, right now.* If you can't, the seam isn't found yet — you have a hope, not a contract. Refuse to proceed past Step 2 until the contract is on the card.

A real contract specifies: inputs each stream consumes, outputs each produces, *what is hidden inside each stream and won't change*, and the merge protocol. If any of those is "we'll figure it out as we go," it's not a contract — it's a coordination meeting that hasn't happened yet.

## Step 3 — Compute coordination tax

For each pair of streams, enumerate required coordination:
- Merge events (rebases, integration PRs, conflict resolution)
- Sync points (design alignment, blocking decisions, review handoffs)
- Shared-resource contention (one staging env, one reviewer, one infra change)

Sum the wall-clock cost. Compare to the single-stream estimate.

**Brooks's test:** at what stream count does marginal coordination tax exceed marginal throughput? For human↔human splits, the break-even is often surprisingly low (2–3 streams). For human-orchestrating-agents splits inside one lane, it's much higher (often 3–4 agents per human, before the human's mental-model budget runs out). Quantify both — they're different curves.

## Step 4 — Adversarial interrogation

Walk these branches one at a time. For each, recommend an answer, then make the user disagree if they want to.

1. **Subdivision premium** — Are you assuming any split helps? Sometimes one focused stream beats two distracted ones. The default isn't "split"; the default is "one stream until proven otherwise."
2. **False fork** — Does the split look parallel but contain hidden serialization? Shared review, shared infra change, shared design decision, shared integration point. If yes, you don't have N streams, you have one stream pretending.
3. **Span overflow** *(strategic)* — Is any single human's lane wider than they can keep mental model on? If an engineer can't summarize what their 3 agents are doing in two sentences, the lane is too wide.
4. **More-engineers fallacy** *(strategic)* — Are you adding headcount because more humans = more throughput? Brooks: communication cost grows quadratically. Three engineers on three lanes is rarely 3×; often 1.5–2×.
5. **Conway mismatch** — Does the split follow natural module boundaries, or does it cut across them? If the latter, integration time will eat the parallel savings.
6. **Coordination amnesia** — Did the up-front estimate include the merge cost, or just the parallel work? Most proposals only count the parallel part.
7. **Contract leak** — Will the contract change during execution? If yes (and the user is uncertain), you're betting the coordination cost will be small. It usually isn't.
8. **Headcount one-way ratchet** *(strategic)* — Are you proposing to *add* humans because that's the visible/legible move? Going from 4 engineers to 2-with-agents is harder to propose but often the right answer.

See `references/fallacies.md` for the full catalog with telltales, counter-questions, and recommended frames.

## Step 5 — Choose the lane shape

For each lane, force the call:

- **Single-thread**: one operator, no internal parallelism. Lowest coordination cost, narrowest throughput.
- **Wide lane with agents**: one operator orchestrating 2–4 agents inside the lane. Higher throughput, requires the operator to be a competent orchestrator and the lane's *internal* contracts to also pass the Parnas test.
- **Pipeline**: streams operate sequentially with handoff. Not parallel — but sometimes the honest answer when the contract isn't stable enough for true parallelism.

Default to **the narrowest lane count that passes the Parnas test, with agents pushed inside lanes rather than across them**. Adding agents inside a lane has a much lower coordination cost than adding lanes across operators. See `references/mental-model.md`.

## Step 6 — Recommend a plan

Output a concrete recommendation in one of these shapes:

- **Don't split** — single stream wins; here's why and here's the timeline.
- **Split into N streams with this contract** — index-card contract, merge protocol, expected coordination tax.
- **Fewer operators, wider lanes** — *the high-value inversion.* Concretely: "you proposed 4 engineers; analysis says 2 engineers with 2–3 agents each beats it because the inter-engineer coordination tax on 4 lanes exceeds intra-lane orchestration cost on 2." Always at least *consider* this shape before recommending more lanes.
- **Asymmetric split** — some lanes wide with agents, others single-thread, based on internal Parnas-cleanness per area.

For whichever shape: name the contract, the merge protocol, each lane's width, and the expected coordination tax as a fraction of total work. If the user's original proposal still wins after the gauntlet, say so and explain why.

## Core stance

- **Splitting is not the default.** The default is one stream. Splitting earns its place by passing both Parnas and Brooks.
- **Contracts are written, not assumed.** If it's not on the index card, it's not a contract.
- **Agents inside lanes beat lanes across operators.** Push parallelism down, not out, until the contract really demands an operator boundary.
- **Visible moves aren't always right moves.** Adding headcount is legible; widening lanes with agents is invisible. Don't optimize for legibility.
- **Estimate, don't measure.** Order-of-magnitude coordination tax beats no analysis; precision can come later.
