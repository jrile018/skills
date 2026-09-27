# Completion sidecar — publish last, keep separate from report

Run/stage: <exact identity>.
Source/config identity: <root/revision/dirty inputs/build variant>.
Input dependencies: <paths and fingerprints; include run contract>.
Delivered outputs: <every output path and SHA-256, including report.md>.
Acceptance: <each predicate with actual check/result; source-only vs executed>.
Approval: <not-required, or actual approval bound to this exact version>.
Coverage/frontier: <bounded scope and limitations>.
Published at: <timestamp with timezone>.

Do not hash this sidecar into itself. Publish from a private candidate after validation.
Treat the published record as immutable; never edit an approval into existence.
Consumability is derived by verifying identities, fingerprints, acceptance, and required
approval, not by trusting this filename or a status label. A mismatch means stale/partial.
This convention is not tamper-proof authentication or a multi-file atomic transaction.
