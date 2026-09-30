---
name: skill-router
description: Use when a request spans multiple domains, could match several installed skills, explicitly asks which skill or workflow to use, or needs a minimal coordinated skill set. Selects one primary skill and only the necessary supporting skills using the private skills portfolio and exact-path profiles.
---

# Skill Router

Route ambiguous or multi-domain work without loading the whole skill portfolio.

## Precedence

Apply this order. A lower item never overrides a higher one:

1. User requirements and explicit skill names.
2. Safety, permissions, and system or developer instructions.
3. The closest repository `AGENTS.md` and required skills it names.
4. A primary domain or artifact skill.
5. Supporting workflow skills.
6. Optional implementation or output policies.

## Routing algorithm

1. If the user names a skill, use it and add only skills that its instructions require.
2. If one installed skill description clearly matches the deliverable, make it primary. Do not invoke this router again for a simple one-skill task.
3. For ambiguous work, read `profiles.json` in this repository. Select the profile whose purpose matches the requested outcome.
4. Use exact `skill_paths` to disambiguate duplicate names. Prefer `active/` or `owned/` paths over cache duplicates unless the profile deliberately selects a managed plugin.
5. Choose one primary skill responsible for the deliverable. Add no more than two supporting skills unless a selected skill explicitly requires more.
6. Announce the selected skills and why. Follow each selected `SKILL.md` completely, in precedence order.
7. Re-route only when the task materially changes, a required skill is missing, or a selected skill delegates to a specialist.

## Profile guide

| Requested outcome | Start with |
| --- | --- |
| Implement, debug, test, or review code | `core-development` |
| Research, compare evidence, map a repository, or audit an answer | `research-and-audit` |
| Create or improve skills, agents, memory, prompts, or harnesses | `agent-systems` |
| Analyze portfolios, execution, finance data, or quantitative systems | `quant-research` |
| Build web apps or create office artifacts | `web-and-artifacts` |

If none fits, match against `catalog.json` by `name`, `description`, and `source_group`. Read only the candidate skill files, not the entire catalog tree.

## Cross-cutting policies

- Add `minimal-correct-change` for bounded implementation or refactoring where the smallest correct diff is desirable.
- Add `context-efficient-output` when compact communication or context transfer is valuable.
- Do not apply either policy to compress proofs, high-stakes analysis, security review, or source-sensitive research unless the user explicitly requests it.
- Workflow skills such as testing, debugging, review, and verification support a primary skill; they do not replace it.

## Routing quality checks

Before acting, confirm:

- Every selected skill has a distinct job.
- The primary skill owns the final deliverable.
- Duplicate names resolve to an exact profile path.
- No optional policy weakens required rigor or verification.
- The set is minimal enough that its instructions do not conflict.
