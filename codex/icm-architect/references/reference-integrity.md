# Reference integrity — the move-safety gate

Restructure's walk test proves the *result* is navigable. It does not prove the *move* was safe. Before proposing a move, enumerate what points at the file. Apparent disuse is not proof.

## What to search

1. **In-vault** — other files in this workspace that name the path.
2. **Sibling-path** — relative `../` references. These break when you regroup folders even if nothing "outside" is involved.
3. **Symlink** — a moved target orphans the link; a moved link disappears.
4. **External** — other repos, deploy scripts, jobs, issue trackers, agent configs that hardcode a path in. Search only an authorized bounded scope; ask the owner when unknown consumers affect the decision. Record what they name on the migration map.
5. **Outbound/path-sensitive** — relative imports/links inside the moved file, package identity, loader roots, glob discovery, generated manifests, and runtime lookup based on location. Content parity does not prove these still work.
6. **Metadata/link semantics** — executable modes, ACLs/xattrs where relevant, symlink/reparse identity and targets, and ownership. Preserve them or document an explicitly approved transformation; a dereferenced copy is not necessarily equivalent to its link.

A file with a live referrer is **held**, or moved only if every referrer is updated in the same change. It is not Dead until this comes back clean.

## Destination collision

Before copying or renaming, check exact and case-folded destination collisions and the actual filesystem's case/normalization behavior. Common Windows/macOS volumes are case-insensitive, but this is configurable; do not infer behavior only from the OS. Never overwrite an existing destination without resolving its ownership and approved treatment first. A parity check after overwriting cannot recover what was there before.

## Copy, verify, then remove

1. Copy to the new home.
2. Verify parity — file count and byte-for-byte content hashes for every copied file, including archives/office files. A pure copy must preserve bytes; format-aware equivalence is relevant only for a separately authorized transformation.
3. Wire approved inbound/outbound references, then run relevant navigation/import/build/discovery checks in the copied layout. If parity, metadata, or behavior cannot be verified, retain the source and report the gap.
4. Remove the original only after all relevant checks pass, within approved scope. Leave a compatible pointer only where that mechanism is valid; a Markdown pointer does not repair a code import or loader path.

## Durability

Confirm the workspace root is tracked or backed up before reorganizing inside it. Reorganizing files that live only in a temp dir or a gitignored path is rearranging deck chairs.
