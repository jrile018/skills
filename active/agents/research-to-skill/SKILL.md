---
name: research-to-skill
description: Produce research-backed Codex skill briefs and evaluation plans. Use when creation requires source synthesis, difficult activation boundaries, or a non-obvious tree spanning multiple courses or repositories; not for routine creation, simple module splits, or edits.
---

# Research to Skill

Turn source material, observed work, and failures into a bounded skill design. Use `$skill-creator` for implementation after the evidence and behavioral contract are clear.

## Scope

Use this skill for research-heavy skill design, overlap or justification decisions, difficult trigger analysis, and comparative evaluation. For a fully specified routine creation or edit, defer directly to `$skill-creator`. For general questions about Codex skills that need no design artifact, consult current official documentation.

Determine the requested mode before proceeding: design-only, audit, create or update, or evaluation.

## Establish the Evidence

Collect only what bears on the proposed skill:

- The single repeatable goal and its expected inputs and outputs.
- Real examples, user corrections, incidents, and verified failures.
- Authoritative files, documentation, schemas, tests, and local conventions.
- Observable success criteria, non-goals, permissions, and safety boundaries.
- Existing skills that may already own or overlap the workflow.

Inspect the target and neighboring skills before recommending a new one. Prefer improving the existing owner over creating competing activation rules.

When repository selection, current guidance, reusable authoring prompts, or non-routine comparative evaluation design is needed, read [references/skill-authoring-research.md](references/skill-authoring-research.md). Do not load it for a narrow task whose evidence and boundaries are already established.

## Map and Navigate Complex Skill Trees

Use this integration when the user explicitly asks to use Graphify or ICM Architect, an existing graph-backed tree needs impact analysis, or a prospective parent has several capabilities whose overlap, dependencies, or ownership are not obvious. A request for a parent, tree, or "sub-skills" alone does not force the integration when the split is small and obvious. Do not merely recommend the named skills in the design brief; invoke them while doing qualifying architecture work.

Read [references/skill-tree-networking.md](references/skill-tree-networking.md) and follow its Graphify-to-classification-to-ICM-review procedure. That reference owns the source-graph schema boundary, derived architecture map, isolation requirements, compatibility checks, and walk test. The procedure must actually invoke `$graphify` and `$icm-architect` when their respective boundaries are met.

Make the resulting parent `SKILL.md` the stable navigation catalog. At ordinary runtime it routes to the smallest sufficient module set; it returns to Graphify only for a graph-backed change, unclear impact path, or architecture audit.

Unless the user explicitly requested the named integrations, skip both for one short, bounded skill or an obvious small module split. If Graphify is unavailable, its runtime or installation is unauthorized, or its orchestration API is incompatible, state the limitation and derive the evidence map manually. For a still-complex architecture, continue with the ordinary modular tests and an ICM-informed navigability review when ICM Architect is available; do not describe the result as graph-backed. If ICM Architect is unavailable, perform and disclose a manual cold walk.

## Choose the Architecture

Do not mirror a source's chapters, departments, or document tree automatically. Organize around user goals and behavioral boundaries.

- Use one self-contained skill when one trigger and one success contract cover the workflow without substantial conditional detail.
- Use a thin parent skill with supporting modules when the modules share one trigger and owner but need different procedures or references after activation.
- Use separate discoverable skills when capabilities have meaningfully different triggers, inputs, outputs, or success criteria.
- Use subagents only as an execution strategy for independent, bounded workstreams; do not create one agent per topic or module.

For a proposed skill with multiple capabilities, course-derived sections, or a requested sub-skill hierarchy, read [references/modular-skill-architecture.md](references/modular-skill-architecture.md). Use its decision tests, module contract, routing matrix, and evaluation requirements. Treat "sub-skill" as an informal design term until the brief classifies it as either a supporting module or a separate skill.

Use this skill's own catalog the same way: authoring-source or evaluation questions route to `skill-authoring-research.md`; modular-boundary questions route to `modular-skill-architecture.md`; graph construction, dependency edges, and parent-to-module navigation route to `skill-tree-networking.md`. Load only the references needed for the current decision.

## Produce the Design Brief

Include:

- Goal, owner, justification, and explicit non-goals.
- An evidence map connecting each material instruction to its source or observed failure.
- The architecture decision: self-contained skill, parent with modules, separate skills, or selective subagents, including why simpler options are insufficient.
- For modular designs, a module map that gives each module's loading condition, owned decision, output or invariant, evidence, and tests.
- For networked designs, a reviewed source graph, derived node-and-edge map, routing catalog with an ICM-informed navigability review, dependency order, and explicit handling for no-match, multi-match, and stale-map cases.
- Direct, indirect, and incomplete positive activation examples.
- Near-miss and boundary negative examples.
- A concise candidate description whose primary use case appears first.
- The minimal resource plan for `SKILL.md`, references, scripts, assets, and optional UI metadata.
- Acceptance criteria, unresolved assumptions, limitations, and an activation and output test plan.

Assume a capable agent. Capture non-obvious, evidence-backed decisions rather than generic advice, and do not turn one incident into a universal rule.

## Hand Off Implementation

When the user requests creation or modification, finish the evidence and design phase, then hand the established brief to `$skill-creator` and preserve its scope. No second approval is required unless a material unresolved choice would change the result. Let that built-in skill own scaffolding, file structure, metadata generation, and structural validation; do not duplicate those procedures here.

For an audit or evaluation request, do not modify the target unless the user also asks for changes.

## Evaluate Behavior

Evaluate activation separately from output quality. Compare the same realistic task using the candidate skill against no skill or the previous version. Check observable invariants and use human judgment for quality that cannot be measured mechanically; do not reward merely copying headings or wording.

Run costly, delegated, or externally mutating tests only when authorized. Revise narrowly from observed traces and failures, then rerun affected cases.

## Deliver by Mode

- **Design-only:** Provide the brief, evidence map, resource plan, authoring prompt, and test plan.
- **Audit:** Provide prioritized findings, supporting evidence, recommended changes, and confirmation of what should remain unchanged.
- **Create or update:** Report paths, final activation boundary, architecture and routing decisions, validation and tests run, and limitations.
- **Evaluation:** Report the baseline comparison, observed failures, evidence for each revision, and remaining uncertainty.

In every mode, distinguish verified results from proposed or untested behavior.
