# icm-architect

ICM workspace design and evidence-backed large-codebase analysis. Preserve the original six forms while adding task-shaped code tracing, security/numeric audits, source freshness, run isolation, and honest coverage reporting.

The entry file routes to optional references rather than loading everything. Start with a concrete question: “Trace this amount from source to report,” “Audit invoice authorization,” “What would this schema change affect?”, or “Build a repeatable ICM workspace.”

## Design

- Small catalogs and explicit contracts; source remains authoritative.
- Lexical → syntax → symbol → flow → targeted verification, using available tools.
- Security paths include authorization, alternate handlers, and benign controls.
- Numeric paths include grain, units, join cardinality, routing, retries, and rounding.
- Cached knowledge has declared dependencies; a current hash is not proof of correctness.
- Run-specific outputs are isolated; completion is version-bound acceptance, not file existence.
- Performance claims require representative measurements; no universal token target or comprehensive vulnerability guarantee.

The [research rationale](references/design-evidence.md) separates published evidence from design analogies. [Evaluation guidance](references/evaluation.md) describes how to compare versions.

## Use and layout

Keep this directory in the skill location used by your agent host. For upgrades, back up the current copy and compare each file against the prior upstream version. Replace untouched upstream files; merge customized files with a three-way diff or ask the owner if their base is unknown. Validate links and behavior before promotion; never overwrite customizations because they differ. The optional `scripts/context_snapshot.py` helper requires Python 3.10+ and no third-party packages; it emits JSON to stdout and does not write to the repository. Read its limitations in [runtime-model.md](references/runtime-model.md).

```text
SKILL.md                 task router and invariants
references/              optional workflow, research, and evaluation details
assets/templates/        contracts, cards, and run-record starters
scripts/                 bounded dependency-freshness helper
```

Original method: [Interpretable Context Methodology](https://arxiv.org/abs/2603.16021), Jake Van Clief and David McDermott; [RinDig protocol](https://github.com/RinDig/Interpretable-Context-Methodology-ICM-). This skill's code-analysis/runtime extensions are adaptations, not measured claims from the paper. Original MIT license retained in LICENSE.
