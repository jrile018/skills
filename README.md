# Skills

Private snapshot of locally installed Codex, Claude, and shared agent skills.

## Sources

| Folder | Skill folders | Original location |
| --- | ---: | --- |
| `agents/` | 131 | `~/.agents/skills` |
| `claude/` | 107 | `~/.claude/skills` |
| `claude-plugins/` | 64 | `~/.claude/plugins/cache` |
| `codex/` | 13 | `~/.codex/skills` |
| `codex-plugins/` | 122 | `~/.codex/plugins/cache` |

Original source folders and plugin versions are preserved to avoid name collisions. Duplicate installations are retained. Skill instructions, scripts, references, templates, images, and available license files are included.

`catalog.json` indexes every skill folder. `manifest.json` records SHA-256 hashes and sizes of copied source files. Git stores original file bytes without newline conversion.

This is a snapshot, not an automatic synchronization service. Copy a desired skill folder into your assistant's skills directory to restore it. Plugin skills may also need their original plugin runtime and tools installed. Third-party material retains its original licensing; no new license is asserted.

Excluded: Git histories, dependency directories, virtual environments, Python caches, and operating-system temporary files. App credentials, session history, and unrelated configuration are outside the copied source roots.
