---
name: "source-command-commit"
description: "Create a well-formatted commit from staged changes (matches repo style)"
---

# source-command-commit

Use this skill when the user asks to run the migrated source command `commit`.

## Command Template

Create a commit from currently staged changes.

Run in parallel:
1. `git status` — confirm what's staged
2. `git diff --cached` — see the actual changes
3. `git log --oneline -10` — match the repo's commit style

Rules:
- Do NOT run `git add` unless the user explicitly asks. Only commit what's already staged.
- If nothing is staged, tell the user and stop — don't stage things yourself.
- If the repo uses Conventional Commits (feat:/fix:/docs:/refactor:/chore:/test:), use the same prefix. If it doesn't, match the existing style.
- Title under 70 chars. Focus on the "why," not a restated diff.
- Body only if the change is non-trivial — skip for trivial changes.
- Never use `--amend` unless the user explicitly asks.
- Never use `--no-verify` unless the user explicitly asks.

Pass the message via HEREDOC to preserve formatting:
```bash
git commit -m "$(cat <<'EOF'
<title>

<body if needed>
EOF
)"
```

After committing, run `git status` and report the new HEAD in one line.
