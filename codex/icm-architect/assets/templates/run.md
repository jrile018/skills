---
run_id: <fresh collision-resistant ID; create-new-only directory>
stage: <stage>
status_hint: planned
source_identity: <root/revision and relevant dirty/untracked inputs>
configuration: <build/runtime variant>
owner: <single writer/coordinator>
---

# <Question and scope>

Authorization: <allowed reads/writes/actions; approval gates>.
Budget: <time/tools/context as useful; not a correctness waiver>.
Acceptance: <observable bounded completion conditions>.

## Inputs and dependencies

<Exact source/reference/upstream paths, hashes, directory discovery scope, tool/schema versions>.

## Separate artifacts

- `report.md`: free-form evidence ledger, findings, coverage, and checks; no separate report template is required.
- `completion.md`: sidecar created from the completion template and published last.
- <other delivered output paths>.

Report evidence: <question → source-backed path → observed/inferred/hypothesis → frontier>.
Finding: <ID; impact and confidence separately; trigger/path/invariant; expected vs actual;
benign explanation considered; verification and limits>.

## Recovery

<Last validated checkpoint; outstanding acceptance; source changes since checkpoint>.
An existing report or editable status hint is not completion.
The separate completion sidecar hashes this run contract, the report, and other delivered outputs.
A human edit invalidates their old hashes and any dependent completion record.
