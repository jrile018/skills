from __future__ import annotations

import json
import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts import sync_skills
from scripts import validate_repository


SKILL = """---
name: {name}
description: Use when testing {name}.
---

# {name}
"""


class RepositoryToolTests(unittest.TestCase):
    def test_copy_skill_dereferences_safe_links_and_excludes_sensitive_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            destination = root / "destination"
            source.mkdir()
            (source / "SKILL.md").write_text(SKILL.format(name="sample"))
            (source / "reference.txt").write_text("safe")
            (source / "linked.txt").symlink_to(source / "reference.txt")
            (source / ".env").write_text("TOKEN=secret")
            (source / ".npmrc").write_text("//registry/:_authToken=secret")
            (source / "credentials.json").write_text('{"token": "secret"}')
            (source / "SKILL.md.bak").write_text("stale backup")
            (source / "node_modules").mkdir()
            (source / "node_modules" / "dependency.js").write_text("ignored")
            (source / "transcripts").mkdir()
            (source / "transcripts" / "session.jsonl").write_text("private")

            sync_skills.copy_skill(source, destination)

            self.assertEqual((destination / "linked.txt").read_text(), "safe")
            self.assertFalse((destination / "linked.txt").is_symlink())
            self.assertFalse((destination / ".env").exists())
            self.assertFalse((destination / ".npmrc").exists())
            self.assertFalse((destination / "credentials.json").exists())
            self.assertFalse((destination / "SKILL.md.bak").exists())
            self.assertFalse((destination / "node_modules").exists())
            self.assertFalse((destination / "transcripts").exists())

    def test_copy_skill_rejects_links_outside_skill_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            outside = root / "outside.txt"
            outside.write_text("do not copy")
            (source / "SKILL.md").write_text(SKILL.format(name="sample"))
            (source / "escape.txt").symlink_to(outside)

            with self.assertRaisesRegex(ValueError, "outside skill root"):
                sync_skills.copy_skill(source, root / "destination")

    def test_copy_skill_does_not_bypass_exclusions_through_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            hidden = source / ".git"
            hidden.mkdir(parents=True)
            (source / "SKILL.md").write_text(SKILL.format(name="sample"))
            (hidden / "config").write_text("credential = secret")
            (source / "safe-looking-config").symlink_to(hidden / "config")

            sync_skills.copy_skill(source, root / "destination")

            self.assertFalse((root / "destination" / "safe-looking-config").exists())

    def test_sync_captures_direct_system_plugin_and_owned_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repository = root / "repository"
            agents = root / "agents"
            codex = root / "codex"
            plugins = root / "plugins"
            owned = repository / "owned" / "owned-skill"

            for path, name in (
                (agents / "agent-skill", "agent-skill"),
                (codex / "codex-skill", "codex-skill"),
                (codex / ".system" / "system-skill", "system-skill"),
                (plugins / "publisher" / "plugin" / "1.2.3" / "skills" / "plugin-skill", "plugin-skill"),
                (owned, "owned-skill"),
            ):
                path.mkdir(parents=True)
                (path / "SKILL.md").write_text(SKILL.format(name=name))

            linked_owned = agents / "owned-skill"
            linked_owned.symlink_to(owned, target_is_directory=True)

            sync_skills.sync_repository(
                repository=repository,
                agents_root=agents,
                codex_root=codex,
                plugins_root=plugins,
            )

            catalog = json.loads((repository / "catalog.json").read_text())
            paths = {entry["path"] for entry in catalog}
            self.assertIn("active/agents/agent-skill", paths)
            self.assertIn("active/codex/codex-skill", paths)
            self.assertIn("managed/codex-system/system-skill", paths)
            self.assertIn(
                "managed/codex-plugins/publisher/plugin/1.2.3/skills/plugin-skill",
                paths,
            )
            self.assertIn("owned/owned-skill", paths)
            self.assertNotIn("active/agents/owned-skill", paths)

            first_snapshot = {
                path.relative_to(repository).as_posix(): path.read_bytes()
                for path in repository.rglob("*")
                if path.is_file()
            }
            sync_skills.sync_repository(repository, agents, codex, plugins)
            second_snapshot = {
                path.relative_to(repository).as_posix(): path.read_bytes()
                for path in repository.rglob("*")
                if path.is_file()
            }
            self.assertEqual(first_snapshot, second_snapshot)

    def test_sync_keeps_existing_snapshot_when_a_required_root_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repository = root / "repository"
            existing = repository / "active" / "agents" / "existing"
            existing.mkdir(parents=True)
            (existing / "SKILL.md").write_text(SKILL.format(name="existing"))
            codex = root / "codex"
            plugins = root / "plugins"
            codex.mkdir()
            plugins.mkdir()

            with self.assertRaisesRegex(ValueError, "agents root"):
                sync_skills.sync_repository(
                    repository,
                    root / "missing-agents",
                    codex,
                    plugins,
                )

            self.assertTrue((existing / "SKILL.md").is_file())

    def test_sync_rolls_back_when_staging_a_skill_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repository = root / "repository"
            existing = repository / "active" / "agents" / "existing"
            existing.mkdir(parents=True)
            (existing / "SKILL.md").write_text(SKILL.format(name="existing"))
            agents = root / "agents"
            broken = agents / "broken"
            broken.mkdir(parents=True)
            (broken / "SKILL.md").write_text(SKILL.format(name="broken"))
            outside = root / "private.txt"
            outside.write_text("private")
            (broken / "escape.txt").symlink_to(outside)
            codex = root / "codex"
            plugins = root / "plugins"
            codex.mkdir()
            plugins.mkdir()

            with self.assertRaisesRegex(ValueError, "outside skill root"):
                sync_skills.sync_repository(repository, agents, codex, plugins)

            self.assertTrue((existing / "SKILL.md").is_file())

    def test_validator_rejects_unknown_profile_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "catalog.json").write_text(
                json.dumps([{"name": "known", "path": "owned/known"}])
            )
            (root / "profiles.json").write_text(
                json.dumps({"profiles": {"test": {"skill_paths": ["owned/missing"]}}})
            )
            (root / "manifest.json").write_text("[]")

            errors = validate_repository.validate_repository(root, run_skill_validator=False)

            self.assertTrue(any("missing" in error for error in errors))

    def test_validator_rejects_uncataloged_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            unlisted = root / "owned" / "unlisted"
            unlisted.mkdir(parents=True)
            (unlisted / "SKILL.md").write_text(SKILL.format(name="unlisted"))
            (root / "catalog.json").write_text("[]")
            (root / "profiles.json").write_text('{"profiles": {}}')
            data = (unlisted / "SKILL.md").read_bytes()
            (root / "manifest.json").write_text(
                json.dumps(
                    [
                        {
                            "path": "owned/unlisted/SKILL.md",
                            "bytes": len(data),
                            "sha256": hashlib.sha256(data).hexdigest(),
                        }
                    ]
                )
            )

            errors = validate_repository.validate_repository(root, run_skill_validator=False)

            self.assertIn("skill missing from catalog: owned/unlisted", errors)

    def test_validator_fails_when_requested_validator_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "catalog.json").write_text("[]")
            (root / "profiles.json").write_text('{"profiles": {}}')
            (root / "manifest.json").write_text("[]")

            errors = validate_repository.validate_repository(
                root,
                run_skill_validator=True,
                quick_validator=root / "missing-validator.py",
            )

            self.assertTrue(any("validator is unavailable" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
