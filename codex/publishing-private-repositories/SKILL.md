---
name: publishing-private-repositories
description: Use when the user explicitly asks to create, publish, push, or transfer a project to a private GitHub or other private Git repository.
---

# Publishing Private Repositories

## Principle

Publish the intended source and deliverables, not the entire surrounding machine context. “Private” reduces exposure but does not make secrets, credentials, or unrelated personal files safe to commit.

## Preflight Contract

Before the first commit or push, establish:

- exact source root and intended repository name;
- private visibility;
- destination account or organization;
- intended author identity;
- whether existing Git history should be preserved;
- generated, downloaded, personal, and secret-bearing files that do not belong.

Inspect the actual payload, including hidden files, large files, nested repositories, environment files, databases, logs, exports, screenshots, resumes, and cached credentials. Use ignore rules for recurring exclusions and remove already tracked sensitive files from the index before publication.

Run available secret scanning and inspect suspicious filenames and diffs. Never print secret values while checking them. If a credential has entered Git history, stop: excluding it in a later commit is not sufficient; report the need for rotation and history cleanup.

## Publication Contract

1. Preserve unrelated local changes and existing history unless the user requested replacement.
2. Verify the configured author and ensure no unwanted coauthor trailers.
3. Commit only the reviewed payload with a meaningful message.
4. Create or select the exact private remote authorized by the user.
5. Push the intended branch without force unless force-push was explicitly requested and its impact verified.
6. Verify remote visibility, default branch, latest commit, author, and repository URL from the hosting service.
7. Report excluded material by category, not by revealing sensitive contents.

## Quick Reference

| Finding | Action |
|---|---|
| Secret in working tree, untracked | Exclude it before committing |
| Secret in history | Stop, rotate, and clean history with explicit approval |
| Nested `.git` directory | Confirm whether it is a submodule or accidental repository |
| Personal artifact unrelated to project | Exclude by default |
| User explicitly includes a sensitive artifact | Confirm the exact file and consequence before publishing |

## Example

When publishing a hardware project, include source, schematics, reproducible build files, and documentation. Exclude local virtual environments, instrument logs, credentials, caches, and unrelated personal exports.

## Common Mistakes

- Assuming private visibility makes secrets acceptable.
- Running a broad add command before reviewing the file inventory.
- Rewriting history or force-pushing without explicit authorization.
- Claiming publication before verifying the remote state.
