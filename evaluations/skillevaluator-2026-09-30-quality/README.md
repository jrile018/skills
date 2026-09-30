# NVIDIA SkillEvaluator baseline — 2026-09-30

This baseline evaluates all 250 entries in `catalog.json` with NVIDIA SkillEvaluator 0.3.0 at commit `d0157411fe6c6eb949f832983bf671dfd1b9c701`. The portfolio was at commit `e149d47ade4c08956f2e6506d0ba49b70476882b` when the run started.

## Outcome

- Evaluated: 250/250
- Execution or report errors: 0
- Passed evaluator gates: 227
- Failed evaluator gates: 23
- Mean score: 86.46
- Median score: 86.8
- Grades: 4 A, 239 B, 7 C
- Owned skills: `skill-router` 84.2/B/pass; `skillopt-sleep` 88.5/B/pass

The evaluator's pass result is not the same thing as a numeric score of at least 70. Every one of the 23 failures scored above 70 but had at least one high-severity finding. Most were caused by a `SKILL.md` exceeding the evaluator's 5,000-token recommendation; `Zotero`, `Presentations`, and `Spreadsheets` also triggered its lowercase-name rule.

Each catalog path was evaluated independently with `quality-check --min-score 70 --report json`. The batch used eight workers and a five-minute per-skill timeout; no timeout was reached.

## Gate failures

| Layer | Skill | Score | Reason |
| --- | --- | ---: | --- |
| active | `executing-plans` | 83.8 | More than 5,000 tokens |
| active | `graphify` | 85.0 | More than 5,000 tokens |
| active | `hatch-pet` | 79.2 | More than 5,000 tokens |
| active | `subagent-driven-development` | 87.5 | More than 5,000 tokens |
| managed | `visualize` | 75.5 | More than 5,000 tokens |
| managed | `ai-elements` (remote Vercel) | 86.2 | More than 5,000 tokens |
| managed | `observability` (remote Vercel) | 86.2 | More than 5,000 tokens |
| managed | `workflow` (remote Vercel) | 86.2 | More than 5,000 tokens |
| managed | `finding-discovery` | 84.5 | More than 5,000 tokens |
| managed | `propose-security-hardening` | 82.5 | More than 5,000 tokens |
| managed | `track-findings` | 86.2 | More than 5,000 tokens |
| managed | `triage-finding` | 84.5 | More than 5,000 tokens |
| managed | `vulnerability-writeup` | 87.5 | More than 5,000 tokens |
| managed | `subagent-driven-development` (Superpowers) | 87.5 | More than 5,000 tokens |
| managed | `writing-skills` | 87.5 | More than 5,000 tokens |
| managed | `ai-elements` (curated Vercel) | 86.2 | More than 5,000 tokens |
| managed | `observability` (curated Vercel) | 86.2 | More than 5,000 tokens |
| managed | `workflow` (curated Vercel) | 86.2 | More than 5,000 tokens |
| managed | `Zotero` | 76.2 | Uppercase name |
| managed | `documents` | 77.2 | More than 5,000 tokens |
| managed | `Presentations` | 80.2 | Uppercase name and more than 5,000 tokens |
| managed | `excel-live-control` | 84.5 | More than 5,000 tokens |
| managed | `Spreadsheets` | 81.0 | Uppercase name and more than 5,000 tokens |

## How to interpret the findings

The most common recommendations were `version` and `metadata.tags` (250 each), `metadata.author` (249), and conventional sections such as Purpose, prerequisites, limitations, and troubleshooting. These are useful review prompts, not automatic edit instructions.

In particular, the installed Codex validator and NVIDIA SkillEvaluator do not use an identical schema. Adding a top-level `version` field solely to satisfy this report can make a skill fail the current Codex validator. Preserve Codex compatibility first, and apply cross-vendor recommendations only after checking both validators.

The 19 managed failures are generated or vendored plugin snapshots. Do not patch those copies directly; update their upstream source or create an intentional owned overlay. The four active failures can be refactored through progressive disclosure in a separate, reviewed change.

## Artifacts

- [`SUMMARY.md`](SUMMARY.md) is the compact generated overview.
- [`summary.json`](summary.json) contains all 250 results, dimensions, severity counts, and findings.
- Local `raw/` output is retained on the evaluation workstation but excluded from Git because it duplicates `summary.json` and contains absolute machine paths.
