# Mental Model

The math and intuition behind the skill. Three frames, in order of load-bearing-ness.

---

## Brooks's Law (1975)

> "Adding manpower to a late software project makes it later." — Fred Brooks, *The Mythical Man-Month*

The point isn't that parallel work is always bad. It's that **coordination cost grows superlinearly** in the number of streams. With *n* streams, the number of pairwise communication paths is *n(n−1)/2*. Three streams have 3 paths. Four streams have 6. Six streams have 15.

Practical implication: the throughput curve from adding parallel streams isn't linear, and it isn't monotonic. There's a stream-count at which adding one more *reduces* aggregate throughput because the added coordination cost exceeds the marginal parallel work.

The break-even point is not the same across split types:

| Split type | Typical break-even | Why |
|---|---|---|
| Cross-engineer (humans on separate lanes) | 2–3 streams | Calendars, design syncs, reviewer queues, merge conflicts on shared code |
| Cross-agent within one human's lane | 3–4 streams | One mental model, one reviewer, no calendar tax — but human attention is finite |
| Cross-tab within one Claude Code session | 2–3 streams | Your context-switching tax + integration time at the end |

These are estimates, not laws. Specific work can move them. But the curve is the curve — adding more is not free.

---

## Parnas's Information Hiding (1972)

> "We propose instead that one begins with a list of difficult design decisions or design decisions which are likely to change. Each module is then designed to hide such a decision from the others." — David Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules*

The original paper isn't about parallel work. It's about modularity. But the criterion it gives — *hide the decisions likely to change* — is exactly the criterion for a good parallel-work contract.

A contract between streams is good iff:

1. The interface is small (fits on an index card)
2. The interface is *stable* — it doesn't have to change as either stream learns more
3. Each stream can make implementation decisions without consulting the others
4. The merge protocol is unambiguous

If any of these fail, the streams aren't really parallel — they're sequential streams with a coordination meeting hiding inside them.

**The index-card test.** Force the user to write the contract on a single index card. If they can't, the seam isn't found. Don't accept hand-waving like "we'll align as we go" — that's the *opposite* of a Parnas contract; that's the contract changing during execution, which is the most expensive failure mode.

---

## Conway's Law (1967)

> "Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure." — Melvin Conway

Stated as a consequence: if your stream split *doesn't* match the natural module boundaries, the system you build will fight you at integration time. Streams will produce code that needs to talk across module boundaries the architecture didn't intend.

For parallel-work design, this means: **start from the architecture's natural seams and ask what stream split they imply, not the other way around.** Going the other direction — picking a stream split that's convenient and forcing the architecture to follow — is the Conway-mismatch fallacy and produces systems that look like the org chart at the moment of decomposition rather than the problem.

---

## The Agent Multiplier (the new piece)

Brooks, Parnas, and Conway predate agents. The new wrinkle they don't directly address: when one operator can run multiple agents inside their lane, the cost curves change.

- **Cross-operator coordination cost is unchanged** — humans still talk to humans through calendars and reviews and shared infra.
- **Intra-lane coordination cost is much lower** — one human↔many agents goes through a single mental model, no calendar, no reviewer queue. The "communication path" cost approaches zero per added agent until the human's working memory budget is exhausted.

This produces an asymmetry: **adding an agent inside a lane is much cheaper than adding a lane across operators.** Which means the often-correct answer to "we need more parallelism" is *not* "add another engineer with a lane" but "give the existing engineer a wider lane and 2–3 agents inside it."

The upper bound on lane width is span-of-control: how many parallel agent streams can one human keep coherent mental model on? Empirically, somewhere in the 2–4 range — past that, the human stops being a coherent orchestrator and starts being a confused reviewer.

---

## Worked examples

### 1. Tactical: 3 Claude tabs on one feature

Proposal: split a feature into "frontend tab," "backend tab," "tests tab," each running a separate Claude Code session.

**Parnas test.** Can the contract between these three be written on an index card? Frontend ↔ backend = an API spec; backend ↔ tests = the same API spec plus test data shapes. *If the API spec is finalized*, yes — 3 tabs is fine. *If you're going to discover the API as you go*, no — the contract is going to leak repeatedly and you'll spend more time syncing tabs than working.

**Brooks test.** Coordination tax = 3 paths × cost-per-rebase × number-of-rebases. If the API churns 3× during the work, that's 9 sync events. Likely worse than 1 tab doing all three sequentially.

**Recommendation shape.** *If the API is stable*, run 3 tabs with the spec on the card. *If not*, run 1 tab end-to-end through the unstable parts, then split the stable parts.

### 2. Strategic: 4 engineers staffed on a refactor vs 2 with agents

Proposal: 4 engineers, each owns one module of the refactor.

**Parnas test.** Modules need stable interfaces between them mid-refactor — but mid-refactor is exactly when interfaces are most likely to move. Likely contract leak across all 4 boundaries.

**Brooks test.** 4 engineers = 6 communication paths. If the refactor surfaces 5 cross-module interface decisions, that's 5 × 6 = 30 sync events.

**Agent multiplier check.** What if 2 engineers each took 2 modules with 2 agents per engineer? Now you have 1 cross-engineer path and 4 intra-lane orchestrations. The intra-lane orchestrations are cheap (one mental model). The cross-engineer path is the only place where Brooks bites.

**Recommendation.** 2 engineers, each with 2 modules and 2–3 agents inside. Index-card contract specifies: which 2 modules each owns, and the one cross-engineer interface they jointly own. Total throughput likely matches or beats 4 engineers, with half the headcount.

### 3. Genuine wide split

Proposal: build 6 unrelated dashboards for 6 unrelated teams.

**Parnas test.** Trivial — the contract between dashboards is "they all use the same dashboard framework." Modules are entirely independent.

**Brooks test.** Coordination paths: 0 (none of the dashboards depend on each other). Shared resources: the framework itself, but it's stable.

**Recommendation.** 6 streams, no analysis needed. This is embarrassingly parallel. The skill should validate quickly and not push back artificially.

---

## Single-thread vs wide-lane vs cross-operator

| Lane shape | Coordination cost | Throughput ceiling | When to choose |
|---|---|---|---|
| Single-thread | 0 | 1× | Contract isn't stable; work is small enough; or operator is the rate-limit and adding agents won't help |
| Wide lane with 2–4 agents | Low (one mental model) | 2–3× | Internal contracts are Parnas-clean; operator is a competent orchestrator |
| Cross-operator split | High (Brooks) | N× minus tax | Architecture genuinely separates; cross-operator contract is rock-stable; work is large enough to amortize coordination tax |

Default to the narrowest lane count that passes Parnas. Push parallelism down (more agents inside a lane) before pushing it out (more lanes across operators).
