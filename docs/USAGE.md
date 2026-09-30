# Using the skills portfolio

## Start with a workflow, not the whole catalog

`profiles.json` is the shortest route to the useful subset for a task. Choose one primary profile, then add a cross-cutting policy only when it fits:

- `core-development`: implementation, debugging, tests, verification, and review.
- `research-and-audit`: current research, repository mapping, source study, and answer auditing.
- `agent-systems`: skills, harnesses, memory, reusable prompts, and self-improvement.
- `quant-research`: the Ingenius router and specialist quantitative-finance skills.
- `web-and-artifacts`: web applications, browser verification, documents, PDFs, slides, and spreadsheets.

The Ponytail-derived `minimal-correct-change` policy belongs on bounded implementation or refactoring work. The Caveman-derived `context-efficient-output` policy belongs where compact context and output are valuable. Neither replaces domain reasoning, security review, or explicit user requirements.

## How routing works

Codex initially matches the request against skill frontmatter descriptions, explicit skill names, and applicable `AGENTS.md` instructions. The installed `skill-router` handles cases where several matches are plausible. It chooses one primary skill for the deliverable and adds only the supporting workflow or policy skills that have a distinct role.

Profiles use exact catalog paths rather than names because plugin caches can contain multiple skills with the same name. The routing order is user and safety instructions, repository instructions, primary domain skill, supporting workflow skills, then optional policies. Explicitly naming a skill remains the most reliable override.

For consistently good routing:

1. State the desired deliverable and constraints, not only the broad topic.
2. Name a skill when you already know the intended workflow.
3. Use `skill-router` or ask “which skills should handle this?” for cross-domain work.
4. Keep descriptions distinct and run validation after every skill update.
5. Prefer one primary skill and at most two supporting skills; more instructions usually create conflicts rather than better results.

## Keep the live setup current

After adding or updating skills:

```bash
cd /path/to/skills
python3 scripts/sync_skills.py
python3 scripts/validate_repository.py
git status --short
```

Review `catalog.json` for the new name and source, then run sync a second time. A clean second run proves the generated snapshot is stable.

## Restore a skill

Copy a complete folder from `active/` or `owned/` into the matching local skills directory. Plugin snapshots may depend on their original plugin runtime or MCP tools, so restore those through the plugin manager rather than copying only a skill folder.

## Update an owned overlay

1. Compare it with the upstream commit recorded in `source.json`.
2. Apply the smallest compatibility change under `owned/`.
3. Update the commit and overlay explanation in `source.json`.
4. Run the repository validator and the upstream tests relevant to the change.
