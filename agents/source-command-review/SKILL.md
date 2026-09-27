---
name: "source-command-review"
description: "Review uncommitted changes for correctness, security, and style"
---

# source-command-review

Use this skill when the user asks to run the migrated source command `review`.

## Command Template

Review the current uncommitted changes with fresh eyes.

1. `git diff HEAD` to see all changes (staged + unstaged)
2. If the diff is large (>500 lines), ask the user which files to focus on rather than trying to review everything

Then assess across three dimensions:

**Correctness** — logic bugs, off-by-one errors, missed edge cases, race conditions, null/undefined handling, error paths.

**Security** — SQL injection, XSS, command injection, path traversal, unsafe deserialization, hardcoded secrets, missing auth checks, dependency vulnerabilities.

**Style & maintainability** — violations of project conventions (check neighboring files), unnecessary abstraction, missing validation at system boundaries, comments that explain WHAT instead of WHY.

Reference `path/to/file.ext:line_number` for every finding. Severity prefix: `[HIGH]`, `[MED]`, `[LOW]`. If the diff is clean, say so in one sentence and stop. No nitpicks, no restating the diff.
