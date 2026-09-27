# <Stage> — <one job>

## Inputs

- Source: <exact paths/symbols and source/config identity>.
- Working: <same-run upstream artifact and validated completion record>.
- Reference: <stable rules used by this stage>.
- Discovery scope: <directories/configuration where new or removed files affect this task>.
- Exclude: <irrelevant or sensitive material; never exclude decisive evidence just for brevity>.

## Process

1. Validate input identity/freshness and relevant constraints.
2. <Perform one coherent transformation or analysis>.
3. Check acceptance; record evidence, limitations, and unresolved paths.

## Outputs and acceptance

- Candidate: <runs/run-id/stage/artifact>; owner: <one writer>.
- Acceptance: <concrete checks; distinguish not-run, failed, passed>.
- Completion record: <run/stage, input/output hashes, checks, approval if required>.
- Retry/recovery: <checkpoint and side-effect/idempotency policy>.

## Human decision and boundaries

<Required review of this exact version, or continue within authorized scope>.
<Allowed reads/writes; external/destructive actions need appropriate authority>.
Human edits produce a new version and invalidate affected downstream results.
