# Repository instructions

## Source of truth

- Edit intentional local skills only under `owned/`.
- Treat `active/`, `managed/`, `catalog.json`, and `manifest.json` as generated output.
- Do not patch generated third-party snapshots. Patch or update their source, then run `python3 scripts/sync_skills.py`.
- Preserve the three-layer model: live direct installs in `active/`, platform/plugin material in `managed/`, and local overlays in `owned/`.

## Required checks

After any skill or inventory change, run:

```bash
python3 scripts/sync_skills.py
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
git diff --check -- . ':(exclude)active/**' ':(exclude)managed/**'
```

Confirm that a second sync produces no diff before committing generated changes.

The whitespace check excludes generated snapshots because source bytes are preserved verbatim. Do not normalize third-party files to satisfy repository style checks.

## Safety

- Never add credentials, session transcripts, `.env` files, dependency directories, virtual environments, or Git histories.
- Keep provenance in catalog metadata or an owned skill's `source.json`.
- Profiles are usage guidance only; they do not override skill triggers, user instructions, safety rules, or permissions.
