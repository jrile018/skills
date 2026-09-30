# Skills Portfolio Optimization Implementation Plan

> **For John:** This plan is implemented inline in the current session because the request explicitly asks to update and organize the private repository.

**Goal:** Turn the private skills snapshot into a current, reproducible portfolio that captures every live Codex and shared-agent skill, highlights practical usage profiles, and validates itself before updates are pushed.

**Architecture:** Keep three explicit layers: `active/` contains dereferenced snapshots of directly installed skills, `managed/` contains versioned plugin-provided skills, and `owned/` contains intentional local overlays. Generate `catalog.json` and `manifest.json` from those layers with one deterministic sync command. Preserve the original snapshot through Git history and an annotated tag instead of carrying duplicate legacy trees forward.

**Tech Stack:** Python 3 standard library, Git, GitHub Actions, Codex `quick_validate.py`.

---

## Global constraints

- Preserve unrelated changes in Ingenius and other source repositories.
- Never copy credentials, `.env` files, dependency caches, Git histories, or virtual environments.
- Dereference installed skill symlinks so the private repository is independently recoverable.
- Treat plugin snapshots as vendored material; do not rewrite their contents.
- Preserve third-party license files bundled with each skill.
- Verify that `minimal-correct-change` and `context-efficient-output` are present as the Ponytail- and Caveman-derived additions.

### Task 1: Preserve and reshape the repository

**Files:**
- Modify: `README.md`
- Create: `AGENTS.md`
- Create: `docs/USAGE.md`
- Remove after tagging: `agents/`, `claude/`, `claude-plugins/`, `codex/`, `codex-plugins/`

1. Tag the current clean snapshot as `snapshot-2026-09-26`.
2. Replace the archival layout with `active/`, `managed/`, and `owned/` responsibilities.
3. Document daily skill selection and maintenance.

### Task 2: Add deterministic synchronization and validation

**Files:**
- Create: `scripts/sync_skills.py`
- Create: `scripts/validate_repository.py`
- Create: `tests/test_repository_tools.py`
- Create: `.github/workflows/validate.yml`

1. Write tests for source discovery, exclusions, profile references, and manifest integrity.
2. Implement idempotent synchronization from live install roots.
3. Implement repository validation and Codex skill validation.
4. Run tests, sync twice, and prove the second run is idempotent.

### Task 3: Repair the SkillOpt compatibility overlay

**Files:**
- Create: `owned/skillopt-sleep/SKILL.md`
- Create: `owned/skillopt-sleep/source.json`

1. Copy the current Microsoft SkillOpt skill without changing behavior.
2. Replace validator-invalid arrow characters in frontmatter prose only.
3. Validate the overlay and point the live installation to it with a recoverable backup.

### Task 4: Generate and verify the current portfolio

**Files:**
- Generate: `active/agents/**`
- Generate: `active/codex/**`
- Generate: `managed/codex-plugins/**`
- Generate: `catalog.json`
- Generate: `manifest.json`
- Create: `profiles.json`

1. Snapshot all live skills and current plugin versions.
2. Confirm Ponytail- and Caveman-derived skills appear in the catalog and appropriate profiles.
3. Run unit tests, repository validation, an authored-files-only `git diff --check`, and a bounded secret scan. Generated snapshots preserve upstream whitespace verbatim.
4. Review the complete diff, commit, and push the verified result.

### Task 5: Make routing explicit

**Files:**
- Create: `owned/skill-router/SKILL.md`
- Modify: `profiles.json`
- Modify: `docs/USAGE.md`

1. Add a compact router for ambiguous, cross-domain, and skill-selection requests.
2. Reference exact catalog paths in profiles so duplicate skill names cannot silently select stale copies.
3. Install the router as a live shared-agent skill and validate it.

## Review focus

- Missing or stale live skills after additions made during the run.
- Unsafe traversal of symlinks or copying outside a skill directory.
- Accidental capture of secrets, caches, or dependency trees.
- Non-idempotent generated output.
- Profiles that imply invocation or security policy changes rather than offering usage guidance.
