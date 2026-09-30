# Evidence-Backed Codex Skill Authoring

Research synthesis and reusable prompt patterns for creating high-quality `SKILL.md` files. Source review current as of 2026-09-25.

## Bottom Line

The most reliable workflow is:

1. Start from a real, repeatable user goal and actual source material.
2. Use Codex's current bundled `$skill-creator` for scaffolding and structural guidance.
3. Keep the description short enough to discriminate rather than attract every related request.
4. Put only essential shared procedure in `SKILL.md`; route conditional detail to references.
5. Use scripts only where deterministic execution or repeated code materially improves reliability.
6. Test activation separately from output quality.
7. Revise from observed traces, false activations, missed activations, and output failures.
8. For a non-obvious parent-to-module tree, use Graphify to establish relationships and ICM Architect to make the reviewed graph navigable.

Do not ask Codex to “write a comprehensive skill.” Ask it to create the shortest skill that reliably changes the right decisions.

## Authority Order

When guidance conflicts, use this order:

1. The `$skill-creator` installed in the active Codex environment. It governs the runtime's actual authoring and validation behavior.
2. Current official OpenAI guidance: the general [Build Skills guide](https://learn.chatgpt.com/docs/build-skills) and, for plugin packaging, the [plugin Build Skills guide](https://developers.openai.com/plugins/build/skills).
3. The portable [Agent Skills specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx).

A remote repository's `main` branch is a useful source mirror, not a replacement for the installed `$skill-creator` when their details differ.

## Repository and Example Catalog

Use these sources as examples, implementation references, or evaluation tools—not as a single ranked authority list.

| Source | Use |
|---|---|
| [Codex skill-creator source](https://github.com/openai/codex/tree/main/codex-rs/skills/src/assets/samples/skill-creator) | Inspect upstream implementation and changes; prefer the installed copy for current runtime behavior. |
| [OpenAI Plugins](https://github.com/openai/plugins) | Current first-party production-style skill and plugin examples. |
| [Agent Skills best practices](https://github.com/agentskills/agentskills/blob/main/docs/skill-creation/best-practices.mdx) | Grounding, context economy, defaults, control calibration, and iteration. |
| [OpenAI Cookbook workflow example](https://github.com/openai/openai-cookbook/blob/main/examples/codex/iterating-development-workflows-with-codex.md) | A detailed real prompt for asking `$skill-creator` to build a complex skill. |
| [Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Useful evaluation and human-review loop; adapt Claude-specific activation advice before using it with Codex. |
| [Awesome Agent Skills](https://github.com/khasky/awesome-agent-skills) | Community examples and overlap comparisons; not an authority. |
| [skill-optimizer](https://github.com/fastxyz/skill-optimizer) | Docker-based cross-model agent evaluation when its dependencies and cost are justified. |
| [SkillBenchmark](https://github.com/TiesPetersen/SkillBenchmark) | Experimental text-output comparison; its system-prompt injection and single-turn scope do not faithfully reproduce Codex skill activation. |

The former [openai/skills](https://github.com/openai/skills) catalog is deprecated and points to `openai/plugins`. Its contents can provide historical examples, but do not treat them as the current baseline when they conflict with the bundled Codex skill creator or newer OpenAI guidance.

## Current OpenAI Direction

OpenAI's [Rethinking skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) guidance highlights four current concerns:

- Long or overlapping descriptions consume catalog context and may be shortened, making routing worse.
- A description should make the true activation boundary clear without over-emphasizing unrelated keywords.
- Large skills should use progressive disclosure, while the entrypoint acts as a minimal router.
- Elaborate itineraries can overconstrain capable models; specify exact procedures only where deviation creates a concrete problem.

This supersedes the tendency in some older or model-specific guides to make descriptions deliberately broad or “pushy.”

## What Makes a Skill Worth Creating

A skill is justified when it captures one coherent capability that is both reusable and materially helpful. Strong inputs include:

- A successful hands-on workflow, including the steps that mattered.
- Corrections the user repeatedly made.
- Project-specific schemas, APIs, conventions, and ownership boundaries.
- Incident reports, failure cases, review comments, and their verified resolutions.
- Repeated helper code that agents otherwise recreate on every run.
- A stable output contract or template that must be followed.

Do not create a new skill for:

- Generic advice the model already follows.
- A one-time fact or isolated incident.
- A single rule better placed in repository instructions.
- A workflow already cleanly owned by an existing skill.
- A procedure whose inputs, success criteria, or safe boundaries remain unknowable.

## Activation Design

The model sees the skill name and description before it sees the body. Treat the description as a routing contract, not a summary of every feature.

### Strong description shape

```yaml
description: <Do the bounded workflow>. Use when <specific user goal or conditions>; do not use for <nearby task only when confusion is likely>.
```

Example:

```yaml
description: Create and validate Postgres schema migrations. Use when adding or changing a migration, or reviewing its rollout.
```

Avoid:

```yaml
description: Help with databases, queries, models, persistence, schemas, migrations, and backend development.
```

The second version activates too broadly and competes with unrelated database skills.

### Trigger test set

Before finalizing a description, write realistic prompts in these classes:

| Class | Purpose |
|---|---|
| Direct positive | Clearly names the intended workflow. |
| Indirect positive | Expresses the same goal in casual or domain language. |
| Incomplete positive | Should activate, then request one necessary missing input. |
| Near-miss negative | Shares vocabulary but belongs to ordinary agent behavior or another skill. |
| Boundary negative | Would cause scope expansion, an unsafe action, or the wrong artifact type. |

Run each query more than once when measuring probabilistic activation. Record whether the skill was actually loaded rather than assuming keyword presence equals activation.

## Progressive Disclosure

| Location | Put here | Keep out |
|---|---|---|
| Frontmatter | Required name and concise description; supported optional metadata only when needed. | Detailed procedures, examples, broad keyword inventories. |
| `SKILL.md` | Shared purpose, essential workflow, decision criteria, real constraints, and explicit routes to resources. | Copied manuals, every variant, exhaustive examples, speculative edge cases. |
| `references/` | Schemas, policies, detailed variants, substantial examples, API notes, evaluation methods. | Duplicate copies of entrypoint instructions. |
| `scripts/` | Repeated transformations, deterministic checks, reliable API/file operations. | Code added merely because scripts are possible. |
| `assets/` | Templates, starter files, fonts, images, or boilerplate used in outputs. | Instructional prose the model must read. |
| `agents/openai.yaml` | Codex UI metadata, invocation policy, and MCP dependencies. | The skill's core procedural instructions. |

Link each reference from the point where its loading condition becomes relevant. “Read `references/api-errors.md` after a non-2xx response” is useful; “see the references folder” is not.

The Agent Skills specification recommends keeping the body below 5,000 tokens and 500 lines. Treat these as compatibility ceilings, not quality targets.

For multi-capability or course-derived designs, use [modular-skill-architecture.md](modular-skill-architecture.md) to decide whether each proposed "sub-skill" is a supporting module, a separate discoverable skill, or a runtime subagent. Do not copy the source material's chapter structure into the skill architecture without applying those decision tests.

When dependencies, overlap, or change impact remain unclear, use [skill-tree-networking.md](skill-tree-networking.md). It owns the Graphify-to-classification-to-ICM-review sequence and the boundary between architecture work and ordinary runtime navigation.

## Calibrating Control

Use high freedom when the task is open-ended and several approaches can succeed:

```markdown
Identify the smallest design that satisfies the user's stated outcome and local conventions. Explain material tradeoffs.
```

Use a default with an escape hatch when one approach usually works:

```markdown
Use pdfplumber for text extraction. For scanned pages requiring OCR, fall back to pdf2image with pytesseract.
```

Use low freedom only when order or exactness matters:

```markdown
Run the read-only validation command before any write. Stop if it reports an unresolved target path.
```

Absolute words such as `always`, `never`, `mandatory`, and `exactly` should correspond to an actual invariant, permission boundary, safety risk, or fragile interface.

## Minimal Prompt for Codex

Use this when the workflow is already understood:

```text
Use `$skill-creator` to create `<skill-name>`.

Goal: <one repeatable user goal>.
Should trigger for: <two or three realistic requests>.
Should not trigger for: <two nearby but different requests>.
Successful output: <observable result and quality criteria>.
Sources of truth: <files, docs, examples, or completed workflow>.
Constraints: <scope, non-goals, and authorization boundaries>.

Keep SKILL.md limited to essential, non-obvious guidance. Move conditional detail
to directly linked references, use scripts only for deterministic or repeatedly
recreated work, create no unnecessary files, run quick_validate.py, and propose
positive and negative behavioral tests.
```

## Full Prompt for a Substantial Skill

```markdown
Use `$skill-creator` to create or update a Codex skill named `<skill-name>`.

## Goal

The skill should help Codex:

<Describe one coherent, repeatable user goal in one to three sentences.>

## Destination

Create or update the skill at `<path>`.

Inspect the destination first. Do not overwrite an existing skill or discard useful
content without identifying the existing files and intended changes.

## Sources of truth

Ground the skill in:

- `<relevant file, documentation, schema, example, or completed workflow>`
- `<known correction, failure, or local convention>`

Do not replace source-specific knowledge with generic best-practice advice.

## Trigger boundary

Requests that should trigger the skill:

- `<realistic direct request>`
- `<indirect or casually phrased request>`
- `<another distinct positive example>`

Requests that should not trigger it:

- `<nearby but different task>`
- `<task owned by another skill or ordinary Codex behavior>`

Write a concise, discriminating description that states what the skill does and
when it applies. Do not turn the examples into an exhaustive keyword list.

## Expected behavior

Inputs: `<inputs>`

Successful outputs: `<observable outputs and acceptance criteria>`

Important decisions and defaults: `<decision rules>`

Constraints and non-goals:

- `<scope boundary>`
- `<authorization or safety boundary>`
- `<things the skill must not create, modify, or assume>`

## Skill design

Assume Codex already understands ordinary software and general problem-solving.
Include only guidance that changes its decisions or materially improves reliability.

Decide what belongs in SKILL.md, references, scripts, assets, and agents/openai.yaml.
Create only resources with a concrete purpose. Do not create a README, changelog,
installation guide, empty directories, duplicated content, or placeholder examples.

Keep SKILL.md as short as the workflow permits. Link every supporting reference
and state exactly when it should be read. Give Codex freedom where multiple
approaches are valid; use exact sequences only for fragile, safety-critical,
permission-sensitive, or mechanically constrained behavior.

Preserve explicit user choices and authorization boundaries.

When the workflow contains multiple capabilities, make an explicit architecture decision among a self-contained skill, a thin parent with supporting modules, separate discoverable skills, and selective subagents. Define every module's loading condition, owned decision, evidence, output or invariant, and behavioral tests. Do not use nested SKILL.md files for supporting modules or spawn one subagent per topic by default.

If those capabilities have non-obvious dependencies or overlap, implement the approved derived architecture map and ICM-informed catalog review from the design brief. Do not rebuild its source graph during ordinary runtime navigation.

## Validation

After creating or updating the skill:

1. Run the bundled quick_validate.py.
2. Run every new or changed deterministic helper script.
3. Check relative links, unfinished placeholders, and unnecessary files.
4. Check that agents/openai.yaml, if present, agrees with SKILL.md.
5. Inspect the final diff for unrelated changes.
6. Propose tests for direct, indirect, incomplete, negative, and edge-case requests.
7. When behavioral testing is authorized, compare observed results with and without
   the skill or against the previous version.

Finish with the skill path, changed files, triggering description, validation
results, untested behavior, and remaining assumptions.
```

## Evaluation Framework

Evaluate two different systems:

### 1. Activation quality

Measure whether the model loads the skill for the right requests. Include both `should_trigger: true` and `should_trigger: false` cases. False positives matter because loading an irrelevant skill consumes context and can distort behavior.

Example dataset:

```json
[
  {"query": "Create a rollout-safe migration for this column change", "should_trigger": true},
  {"query": "Why is this SELECT query slow?", "should_trigger": false}
]
```

### 2. Output quality

Compare the same realistic task:

- With the candidate skill.
- Without the skill, or with a snapshot of the previous version.

Use observable assertions where possible: files created, commands used, required fields, valid schemas, safe side effects, or verified transformations. Add human review for judgment that cannot be captured mechanically.

Do not grade only whether the answer copied the skill's headings or exact wording. That rewards imitation rather than improved task performance.

### Evaluation loop

1. Start with two or three representative tasks and one meaningful edge case.
2. Capture outputs, execution traces, tool calls, duration, and token usage when available.
3. Record failed assertions and specific human feedback.
4. Diagnose whether the failure came from activation, unclear instructions, irrelevant instructions, missing context, or a nondeterministic operation that should become a script.
5. Make the smallest general correction.
6. Rerun the whole set against a clean workspace.
7. Expand the test set only after the first loop provides useful signal.

Stop when acceptance criteria are met, feedback is consistently empty, or further changes no longer produce meaningful improvement.

## Recommended Tests for This Skill

Use the following cases to verify that `research-to-skill` complements rather than competes with `$skill-creator`:

| Request | Expected behavior |
|---|---|
| “Turn these incident reports and repeated reviewer corrections into a reusable Codex skill.” | Activate; synthesize evidence and produce a bounded brief before implementation. |
| “Compare current skill-authoring repositories and design an evaluation plan for our proposed skill.” | Activate; research sources and produce comparative tests. |
| “Create a PDF skill with this complete specification and these exact files.” | Do not activate; route routine, fully specified creation directly to `$skill-creator`. |
| “Rewrite this generic system prompt to be clearer.” | Do not activate unless the user explicitly wants a skill design. |
| “Evaluate this model response for factual accuracy.” | Do not activate; this is ordinary response evaluation, not skill evaluation. |
| “Fix this typo in an existing `SKILL.md`.” | Do not activate; this is a narrow edit with no research or boundary-design need. |

For positive cases, also test an indirect phrasing and a version missing one essential input. For negative cases, confirm that shared words such as “prompt,” “evaluate,” or “skill” do not cause activation by themselves.

## Common Failure Modes

| Failure | Better response |
|---|---|
| Generic “best practices” skill | Ground it in real artifacts, corrections, and domain-specific decisions. |
| Description is an exhaustive capability list | State the bounded user goal and a meaningful activation condition. |
| Skill triggers for every related noun | Add the actual workflow boundary or near-miss exclusion. |
| `SKILL.md` contains a copied manual | Keep shared procedure in the entrypoint and route to focused references. |
| Every possible edge case becomes a rule | Let the model use judgment; add rules only from demonstrated failures or real risk. |
| Many equal tool choices | Choose a default and state the condition for an alternative. |
| Repeated code is regenerated on every run | Bundle and test a deterministic helper script. |
| Validator passes, so the skill is declared good | Test activation and observable output behavior separately. |
| One successful run is treated as proof | Repeat representative cases and compare with a baseline. |
| A community skill is copied directly | Inspect provenance, permissions, scripts, dependencies, and product-specific assumptions. |
| A new skill overlaps an existing one | Tighten ownership, update the existing skill, or define an explicit routing boundary. |

## Completion Checklist

- The skill owns one coherent repeatable goal.
- Its description is concise, discriminating, and tested against near misses.
- The body contains only essential shared guidance.
- Each reference and script has a stated loading or execution condition.
- Each proposed sub-skill is classified as a supporting module or separate skill using an explicit trigger and success-contract test.
- Non-obvious modular trees have a reviewed Graphify source graph, a separately derived architecture map, an ICM-informed navigability review, acyclic route and dependency edges, and a passing cold-walk test.
- Modular parents define positive, negative, multi-module, and ambiguous routing cases.
- Subagents, if proposed, have an independent bounded assignment and measured value over a single-agent baseline.
- Detail is not duplicated across files.
- Prescriptiveness matches fragility and risk.
- User intent, permissions, and local conventions remain authoritative.
- Structural validation passes.
- Helper scripts, if any, have actually run.
- Activation tests include positive and negative cases.
- Output tests measure meaningful behavior, not wording.
- The final file list and diff contain no unrelated or placeholder artifacts.
- Limitations and untested behavior are reported honestly.
