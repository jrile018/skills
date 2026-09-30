# Gotchas

Failure modes of this skill itself. Highest-signal section per `/improve` best practices.

## Don't let Step 1 be ambiguous about altitude

If the user is mixing tactical (code-level, agent tabs) and strategic (system-level, engineers + agents) framing, force them to pick one. The fallacies that dominate, the cost curves, and the recommendation shapes are all different. If they genuinely have both problems, run the skill twice — once at each altitude — rather than blending. Blending produces mush.

## Don't let Step 2 be skipped

The end-to-end work map and the index-card contract are the foundation of the entire skill. Without them, the Parnas test is impossible, the coordination tax is ungrounded, and you're back to picking by feel. Common evasions:

- "The contract is obvious, we don't need to write it down" — write it down anyway. The act of writing surfaces ambiguity.
- "We'll align as we go" — that *is* the contract leaking; force the user to acknowledge it.
- "It's just an API spec" — fine, then write the spec on the card. Inputs, outputs, what's hidden, merge protocol.

If the user pushes hard on skipping, name the cost: "Without the contract on the card, I can only guess at coordination tax — which means we're picking the split by feel, which is the failure mode this skill exists to prevent."

## Don't accept hand-wave contracts

Watch for these phrases — they all mean *the contract isn't real*:
- "We'll figure out the interface as we go"
- "The team will sync regularly"
- "It's mostly stable"
- "We'll iterate on the contract"

Each is a contract leak in disguise. If the contract is going to change during execution, the streams aren't really parallel — they're sequential streams interrupted by sync meetings. Force the user to either lock the contract up front, or accept that the unstable part needs to run as a single stream first.

## Force the altitude-specific fallacies

The 8 fallacies aren't all equally relevant at every altitude. At tactical altitude, the dominant ones are subdivision premium, false fork, contract leak, coordination amnesia. At strategic altitude, add span overflow, more-engineers fallacy, Conway mismatch, headcount one-way ratchet. Don't waste time walking strategic fallacies on a tactical proposal or vice versa.

## Always consider the agent-multiplier inversion at strategic altitude

For *every* strategic proposal, before recommending the plan in Step 6, force the user to consider: "Could fewer humans with wider agent-augmented lanes do this?" Even if the answer is no, the question has to be asked. This is the single most common missed opportunity in the strategic mode and it's invisible by default — no one in the org chart is incentivized to propose fewer humans.

## Don't railroad to fewer-humans-wider-lanes

If the user has a real reason to staff more humans — onboarding goals, knowledge spreading, regulatory requirements, agent maturity in this domain not yet trustworthy — *accept it* and move on. The point is to surface the wider-lanes option explicitly, not to force one specific answer. Require the user to *name* the constraint rather than skipping the question.

## Don't accept "we don't have data" on coordination tax

Order-of-magnitude estimation is always possible. Use brackets: "Is the merge cost on this closer to 1 day, 1 week, or 1 month? How many merge events do you expect?" The skill is about the math, and the math doesn't need precision — it needs ranks.

## Don't let the user negotiate down the math

When the analysis says "you proposed 4 engineers, 2 with agents would beat it," don't soften it because the user pushes back. If they want to proceed with 4 anyway, they can — but they should do so knowing the analysis. Your job is to give them the number; their job is to react to it.

## Don't skip Step 6

Adversarial pressure-testing without a positive recommendation leaves the user worse off than when they started — they've abandoned a plan with no replacement. Always close with a concrete shape: don't-split / split-as-proposed / fewer-operators-wider-lanes / asymmetric. Even "your original plan still wins, here's why" is a valid Step 6 output — but Step 6 must close.

## Watch for the meta-fallacy

A user invoking this skill on their *own* proposal is self-selecting for openness to redirection. A user invoking it on someone *else's* proposal — particularly to argue against staffing decisions made above them — may be using it as ammunition. The skill works either way, but if the framing is adversarial-toward-a-third-party, surface the framing and ask whether the goal is collaboration or persuasion. They're different skills.

## Watch for the sunk-staff trap

Strategic-altitude version of the sunk-demo trap. If the user has *already* staffed N engineers on the project, the question shifts from "how many engineers?" to "given this team, what lanes shape?" That's a valid question, but it's a different question — and the wider-lanes inversion is mostly off the table once humans are staffed and committed. Surface the framing: "Are we designing the team, or designing the work given the team?"
