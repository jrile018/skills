# Evaluation plan

## When to run it

Run this plan after changing the skill description, parent routing table, shared workflow, module boundaries, delegation rules, or safety boundary. Structural checks are necessary but not sufficient; behavior must be compared with and without the skill on held-out prompts.

## Structural checks

- Frontmatter name matches the directory and the description states both positive and negative activation boundaries.
- Every parent link resolves, every routed module exists, and no nested `SKILL.md` appears below `references/`.
- Every technical module has a purpose/loading boundary, correctness or evidence rules, and an acceptance condition.
- Shared rules such as the ordinary baseline, end-to-end proof, and live-system authorization have one canonical owner in `SKILL.md`; modules add only decision-specific checks.
- The route/dependency graph is acyclic and an ordinary phase needs no more than `SKILL.md` plus two selected modules.
- The discovery descriptions of this skill and `mit-6172-performance-engineering` state their mutual boundary.
- `agents/openai.yaml` gives a concise display name, description, and explicit `$low-latency-quant-systems` invocation.

## Behavioral suite

Test at least these groups:

1. **Direct positives:** feed handler latency, order-book replay, execution gateway, pricing/risk kernel, network path, and CPU/GPU/FPGA placement.
2. **Implicit positives:** a trading path described through symptoms such as open-auction jitter or unexplained tail latency without naming the skill.
3. **Near misses:** generic refactoring, conceptual finance, strategy profitability, and non-trading performance work.
4. **Incomplete requests:** activate when the objective is clearly a trading-system performance problem, then ask only for facts that change the investigation.
5. **Safety cases:** analysis may proceed, but live order submission, production deployment, credentials, purchases, and infrastructure mutation require separate explicit authority.
6. **Module isolation:** one case for every technical module where unrelated modules should remain unloaded.
7. **Composed routes:** numerical then CPU; concurrency plus networking; trading correctness plus measurement; network evidence into architecture.
8. **Delegation:** compare a single-agent control against conditional workers; require a concrete quality, error-isolation, or wall-clock benefit.

## Scoring record

For each case record:

- expected activation and actual activation;
- expected module set and actual module set;
- dependency order and worker topology, if any;
- correctness and authorization boundaries preserved;
- unsupported or overconfident claims;
- outcome, failure reason, and proposed smallest fix;
- prompt, response, model/tool versions, date, and available token/latency measurements.

Do not report exact token savings unless the runtime exposes comparable usage. File counts or word counts are structural context proxies, not billed-token measurements.

## Acceptance

Do not install a revision if any hard case loses trading correctness, numerical acceptance, timestamp comparability, or authorization boundaries. Prefer the smallest prompt change that fixes a repeated, attributable failure. Reject rewrites that merely change wording without improving held-out behavior.
