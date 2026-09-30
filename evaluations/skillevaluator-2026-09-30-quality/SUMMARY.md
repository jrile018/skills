# SkillEvaluator portfolio report

- Evaluator: NVIDIA SkillEvaluator skillevaluator, version 0.3.0 at `d0157411fe6c6eb949f832983bf671dfd1b9c701`
- Portfolio commit: `e149d47ade4c08956f2e6506d0ba49b70476882b`
- Evaluated: 250/250
- Passed evaluator gates (`--min-score 70`): 227
- Failed evaluator gates: 23
- Execution/report errors: 0
- Mean score: 86.46
- Median score: 86.8

All 23 gate failures scored above 70 but included at least one high-severity finding. See `README.md` for the failure list and compatibility guidance.

## Results by layer

| Layer | Count | Passed | Failed | Errors | Mean | Median | Min | Max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| active | 40 | 36 | 4 | 0 | 86.49 | 86.8 | 79.2 | 89.8 |
| managed | 208 | 189 | 19 | 0 | 86.45 | 86.8 | 75.5 | 91.0 |
| owned | 2 | 2 | 0 | 0 | 86.35 | 86.35 | 84.2 | 88.5 |

## Lowest scores

| Score | Grade | Layer | Skill | Path |
| ---: | --- | --- | --- | --- |
| 75.5 | C | managed | visualize | `managed/codex-plugins/openai-bundled/visualize/1.0.23/skills/visualize` |
| 76.2 | C | managed | Zotero | `managed/codex-plugins/openai-curated/zotero/1e285826/skills/zotero` |
| 77.2 | C | managed | documents | `managed/codex-plugins/openai-primary-runtime/documents/26.921.10847/skills/documents` |
| 77.8 | C | managed | bits-and-bolts | `managed/codex-plugins/mcp-extensions-early-access/bits-and-bolts/0.1.11/skills/bits-and-bolts` |
| 78.5 | C | managed | skill-installer | `managed/codex-system/skill-installer` |
| 79.2 | C | active | hatch-pet | `active/codex/hatch-pet` |
| 79.5 | C | managed | openai-docs | `managed/codex-system/openai-docs` |
| 80.2 | B | managed | Presentations | `managed/codex-plugins/openai-primary-runtime/presentations/26.921.10847/skills/presentations` |
| 80.2 | B | managed | plugin-creator | `managed/codex-system/plugin-creator` |
| 80.2 | B | managed | skill-creator | `managed/codex-system/skill-creator` |
| 80.8 | B | managed | imagegen | `managed/codex-system/imagegen` |
| 81.0 | B | managed | sites-hosting | `managed/codex-plugins/openai-bundled/sites/0.1.46/skills/sites-hosting` |
| 81.0 | B | managed | agent-browser | `managed/codex-plugins/openai-curated-remote/vercel/0.21.4/skills/agent-browser` |
| 81.0 | B | managed | agent-browser | `managed/codex-plugins/openai-curated/vercel/1e285826/skills/agent-browser` |
| 81.0 | B | managed | Spreadsheets | `managed/codex-plugins/openai-primary-runtime/spreadsheets/26.921.10847/skills/spreadsheets` |
| 81.5 | B | active | hindsight-fit-assessor | `active/codex/hindsight-fit-assessor` |
| 81.5 | B | managed | create-pet | `managed/codex-plugins/openai-curated-remote/work-pets/0.1.6/skills/create-pet` |
| 81.5 | B | managed | security-scan | `managed/codex-plugins/openai-curated/codex-security/1e285826/skills/security-scan` |
| 81.5 | B | managed | threat-model | `managed/codex-plugins/openai-curated/codex-security/1e285826/skills/threat-model` |
| 82.5 | B | managed | cloudflare | `managed/codex-plugins/openai-curated/cloudflare/1e285826/skills/cloudflare` |
| 82.5 | B | managed | propose-security-hardening | `managed/codex-plugins/openai-curated/codex-security/1e285826/skills/propose-security-hardening` |
| 82.8 | B | managed | brainstorming | `managed/codex-plugins/openai-curated/superpowers/1e285826/skills/brainstorming` |
| 83.0 | B | managed | artifact-template-project-kickoff | `managed/codex-plugins/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-project-kickoff` |
| 83.0 | B | managed | artifact-template-system-design | `managed/codex-plugins/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-system-design` |
| 83.0 | B | managed | plugin-management | `managed/codex-plugins/openai-curated-remote/plugin-management/0.1.0/skills/plugin-management` |
| 83.2 | B | active | harness-creator | `active/codex/harness-creator` |
| 83.5 | B | managed | artifact-template-team-alignment | `managed/codex-plugins/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-team-alignment` |
| 83.5 | B | managed | eve | `managed/codex-plugins/openai-curated-remote/vercel/0.21.4/skills/eve` |
| 83.5 | B | managed | eve | `managed/codex-plugins/openai-curated/vercel/1e285826/skills/eve` |
| 83.8 | B | active | executing-plans | `active/codex/executing-plans` |
| 84.0 | B | active | icm-architect | `active/codex/icm-architect` |
| 84.2 | B | active | mit-18642-quant-finance | `active/agents/mit-18642-quant-finance` |
| 84.2 | B | active | interactive-source-study | `active/codex/interactive-source-study` |
| 84.2 | B | managed | artifact-template-business-review | `managed/codex-plugins/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-business-review` |
| 84.2 | B | managed | artifact-template-design-report | `managed/codex-plugins/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-design-report` |
| 84.2 | B | managed | artifact-template-experiment-analysis | `managed/codex-plugins/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-experiment-analysis` |
| 84.2 | B | managed | artifact-template-investment-committee-memo | `managed/codex-plugins/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-investment-committee-memo` |
| 84.2 | B | managed | artifact-template-legal-memorandum | `managed/codex-plugins/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-legal-memorandum` |
| 84.2 | B | managed | artifact-template-market-trends-report | `managed/codex-plugins/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-market-trends-report` |
| 84.2 | B | managed | artifact-template-minimal-letterhead | `managed/codex-plugins/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-minimal-letterhead` |

## Most frequent findings

| Count | Severity | Finding |
| ---: | --- | --- |
| 250 | medium | SKILL_SPEC recommended field missing: 'version' |
| 250 | medium | SKILL_SPEC recommended field missing: 'metadata.tags' |
| 249 | medium | SKILL_SPEC recommended field missing: 'metadata.author' |
| 249 | low | No '## Purpose' section |
| 246 | low | No limitations documented |
| 243 | low | No prerequisites/requirements documented |
| 239 | low | No troubleshooting section documented |
| 81 | low | No examples provided |
| 53 | low | No mention of error handling or validation |
| 46 | low | Broad description without negative triggers may cause over-triggering |
| 12 | medium | No documented scripts in table format |
| 12 | medium | Instructions don't mention 'run_script' |
| 11 | low | Description doesn't mention WHEN to use this skill |
| 6 | low | Uses complex/corporate language |
| 6 | medium | Description uses first/second person |
| 5 | low | Description very long (225 chars, recommend 50-150) |
| 4 | low | Description very long (248 chars, recommend 50-150) |
| 4 | low | Description very long (243 chars, recommend 50-150) |
| 4 | low | Description very long (231 chars, recommend 50-150) |
| 3 | low | Description very long (289 chars, recommend 50-150) |
| 3 | low | Description very long (310 chars, recommend 50-150) |
| 3 | low | Description very long (435 chars, recommend 50-150) |
| 3 | low | Description very long (241 chars, recommend 50-150) |
| 3 | low | Description very long (239 chars, recommend 50-150) |
| 3 | low | Description very long (249 chars, recommend 50-150) |
| 3 | low | Description very long (236 chars, recommend 50-150) |
| 3 | low | Description very long (252 chars, recommend 50-150) |
| 3 | low | Description very long (246 chars, recommend 50-150) |
| 3 | low | Description very long (229 chars, recommend 50-150) |
| 3 | low | High line repetition detected |
