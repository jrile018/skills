#!/usr/bin/env python3
"""Create a deterministic, self-contained snapshot of installed skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Iterable


EXCLUDED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    ".ssh",
    "__pycache__",
    "node_modules",
    "sessions",
    "transcripts",
    "venv",
}
EXCLUDED_FILES = {".DS_Store", "Thumbs.db"}
ENV_EXAMPLES = {".env.example", ".env.sample", ".env.template"}
SENSITIVE_FILES = {
    ".netrc",
    ".npmrc",
    ".pypirc",
    "credentials.json",
    "credentials.yaml",
    "credentials.yml",
    "id_ed25519",
    "id_rsa",
    "secrets.json",
    "secrets.yaml",
    "secrets.yml",
}
SENSITIVE_SUFFIXES = (".key", ".p12", ".pem", ".pfx")
SNAPSHOT_ROOTS = ("active", "managed", "owned")


def is_excluded(path: Path) -> bool:
    """Return whether a relative path must never enter a snapshot."""
    if any(part.lower() in EXCLUDED_DIRECTORIES for part in path.parts):
        return True
    name = path.name
    lowered = name.lower()
    if name in EXCLUDED_FILES or lowered in SENSITIVE_FILES:
        return True
    if lowered.endswith(SENSITIVE_SUFFIXES):
        return True
    if lowered.endswith((".bak", ".orig", ".pyc", ".pyo", ".tmp", "~")):
        return True
    return lowered.startswith(".env") and lowered not in ENV_EXAMPLES


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def copy_skill(source: Path, destination: Path) -> None:
    """Copy one skill, dereferencing only symlinks contained by its root."""
    source = source.expanduser().resolve(strict=True)
    if not source.is_dir() or not (source / "SKILL.md").is_file():
        raise ValueError(f"not a skill directory: {source}")
    if destination.exists() or destination.is_symlink():
        if destination.is_dir() and not destination.is_symlink():
            shutil.rmtree(destination)
        else:
            destination.unlink()

    def copy_node(current: Path, target: Path, relative: Path, stack: set[Path]) -> None:
        if is_excluded(relative):
            return
        resolved = current.resolve(strict=True)
        if not _inside(resolved, source):
            raise ValueError(f"symlink points outside skill root: {current} -> {resolved}")
        resolved_relative = resolved.relative_to(source)
        if is_excluded(resolved_relative):
            return
        if resolved in stack:
            raise ValueError(f"symlink cycle in skill: {current}")
        if resolved.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            next_stack = stack | {resolved}
            for child in sorted(resolved.iterdir(), key=lambda item: item.name):
                copy_node(child, target / child.name, relative / child.name, next_stack)
        elif resolved.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(resolved, target)

    copy_node(source, destination, Path(), set())


def read_frontmatter(skill_file: Path) -> dict[str, str]:
    """Read the top-level name and description without a YAML dependency."""
    lines = skill_file.read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    result: dict[str, str] = {}
    index = 1
    while index < len(lines) and lines[index].strip() != "---":
        line = lines[index]
        if line and not line[0].isspace() and ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            if key in {"name", "description"}:
                if value in {">", ">-", "|", "|-"}:
                    continuation: list[str] = []
                    index += 1
                    while index < len(lines) and (
                        not lines[index] or lines[index][0].isspace()
                    ):
                        continuation.append(lines[index].strip())
                        index += 1
                    result[key] = " ".join(filter(None, continuation))
                    continue
                result[key] = value
        index += 1
    return result


def _run_git(path: Path, *args: str) -> str | None:
    completed = subprocess.run(
        ["git", "-C", str(path), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        return None
    return completed.stdout.strip()


def git_origin(path: Path, cache: dict[Path, dict[str, Any]]) -> dict[str, Any] | None:
    """Return concise provenance for a Git-backed source tree."""
    root_text = _run_git(path, "rev-parse", "--show-toplevel")
    if not root_text:
        return None
    root = Path(root_text).resolve()
    if root not in cache:
        remote = _run_git(root, "remote", "get-url", "origin")
        commit = _run_git(root, "rev-parse", "HEAD")
        dirty = bool(_run_git(root, "status", "--porcelain"))
        cache[root] = {
            "remote": remote,
            "commit": commit,
            "dirty": dirty,
        }
    return cache[root]


def _entry(
    path: Path,
    repository: Path,
    layer: str,
    source_group: str,
    source_label: str,
    origin: dict[str, Any] | None = None,
) -> dict[str, Any]:
    metadata = read_frontmatter(path / "SKILL.md")
    entry: dict[str, Any] = {
        "name": metadata.get("name", path.name),
        "description": metadata.get("description", ""),
        "layer": layer,
        "source_group": source_group,
        "path": path.relative_to(repository).as_posix(),
        "source": source_label,
    }
    if origin:
        entry["origin"] = origin
    return entry


def _direct_skills(root: Path) -> Iterable[Path]:
    if not root.is_dir():
        return ()
    return tuple(
        child
        for child in sorted(root.iterdir(), key=lambda item: item.name)
        if child.name != ".system" and (child.resolve() / "SKILL.md").is_file()
    )


def _snapshot_direct(
    repository: Path,
    source_root: Path,
    destination_root: Path,
    source_group: str,
    source_prefix: str,
    catalog: list[dict[str, Any]],
    git_cache: dict[Path, dict[str, Any]],
    owned_root: Path,
) -> None:
    for installed in _direct_skills(source_root):
        resolved = installed.resolve()
        if _inside(resolved, owned_root):
            continue
        destination = destination_root / installed.name
        copy_skill(resolved, destination)
        catalog.append(
            _entry(
                destination,
                repository,
                "active",
                source_group,
                f"{source_prefix}/{installed.name}",
                git_origin(resolved, git_cache),
            )
        )


def _snapshot_system(
    repository: Path,
    codex_root: Path,
    catalog: list[dict[str, Any]],
) -> None:
    source = codex_root / ".system"
    destination_root = repository / "managed" / "codex-system"
    for skill in _direct_skills(source):
        destination = destination_root / skill.name
        copy_skill(skill.resolve(), destination)
        catalog.append(
            _entry(
                destination,
                repository,
                "managed",
                "codex-system",
                f"~/.codex/skills/.system/{skill.name}",
            )
        )


def _snapshot_plugins(
    repository: Path,
    plugins_root: Path,
    catalog: list[dict[str, Any]],
) -> None:
    if not plugins_root.is_dir():
        return
    destination_root = repository / "managed" / "codex-plugins"
    skill_files = sorted(plugins_root.rglob("SKILL.md"))
    for skill_file in skill_files:
        if is_excluded(skill_file.relative_to(plugins_root)):
            continue
        skill = skill_file.parent
        relative = skill.relative_to(plugins_root)
        destination = destination_root / relative
        copy_skill(skill, destination)
        catalog.append(
            _entry(
                destination,
                repository,
                "managed",
                "codex-plugin",
                f"~/.codex/plugins/cache/{relative.as_posix()}",
            )
        )


def _catalog_owned(repository: Path, catalog: list[dict[str, Any]]) -> None:
    owned_root = repository / "owned"
    if not owned_root.is_dir():
        return
    for skill_file in sorted(owned_root.glob("*/SKILL.md")):
        catalog.append(
            _entry(
                skill_file.parent,
                repository,
                "owned",
                "owned",
                f"repository:{skill_file.parent.relative_to(repository).as_posix()}",
            )
        )


def _manifest(repository: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for root_name in SNAPSHOT_ROOTS:
        root = repository / root_name
        if not root.is_dir():
            continue
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            data = path.read_bytes()
            entries.append(
                {
                    "path": path.relative_to(repository).as_posix(),
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
    return entries


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _validate_stage(stage: Path, catalog: list[dict[str, Any]]) -> None:
    catalog_paths = {entry["path"] for entry in catalog}
    skill_paths = {
        path.parent.relative_to(stage).as_posix()
        for root_name in SNAPSHOT_ROOTS
        for path in (stage / root_name).rglob("SKILL.md")
        if path.is_file()
    }
    if catalog_paths != skill_paths:
        missing = sorted(skill_paths - catalog_paths)
        extra = sorted(catalog_paths - skill_paths)
        raise ValueError(f"staged catalog mismatch; missing={missing}, extra={extra}")
    manifest = json.loads((stage / "manifest.json").read_text(encoding="utf-8"))
    manifest_paths = {entry["path"] for entry in manifest}
    actual_paths = {
        path.relative_to(stage).as_posix()
        for root_name in SNAPSHOT_ROOTS
        for path in (stage / root_name).rglob("*")
        if path.is_file()
    }
    if manifest_paths != actual_paths:
        raise ValueError("staged manifest does not cover the generated snapshot")


def _required_root(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_dir():
        raise ValueError(f"{label} root is missing or not a directory: {resolved}")
    return resolved


def _replace_generated(repository: Path, stage: Path) -> None:
    """Replace generated outputs as one rollback-capable transaction."""
    names = ("active", "managed", "catalog.json", "manifest.json")
    backup_root = stage.parent / "backup"
    backup_root.mkdir()
    moved_old: list[tuple[Path, Path]] = []
    installed_new: list[Path] = []
    try:
        for name in names:
            current = repository / name
            replacement = stage / name
            backup = backup_root / name
            if current.exists() or current.is_symlink():
                backup.parent.mkdir(parents=True, exist_ok=True)
                os.replace(current, backup)
                moved_old.append((backup, current))
            os.replace(replacement, current)
            installed_new.append(current)
    except Exception:
        for current in reversed(installed_new):
            if current.is_dir() and not current.is_symlink():
                shutil.rmtree(current)
            elif current.exists() or current.is_symlink():
                current.unlink()
        for backup, current in reversed(moved_old):
            if backup.exists() or backup.is_symlink():
                os.replace(backup, current)
        raise


def sync_repository(
    repository: Path,
    agents_root: Path,
    codex_root: Path,
    plugins_root: Path,
) -> list[dict[str, Any]]:
    repository = repository.resolve()
    repository.mkdir(parents=True, exist_ok=True)
    agents_root = _required_root(agents_root, "agents")
    codex_root = _required_root(codex_root, "codex")
    plugins_root = _required_root(plugins_root, "plugins")
    owned_root = (repository / "owned").resolve()

    with tempfile.TemporaryDirectory(
        prefix=f".{repository.name}-sync-", dir=repository.parent
    ) as temporary:
        stage = Path(temporary) / "repository"
        for relative in (
            "active/agents",
            "active/codex",
            "managed/codex-system",
            "managed/codex-plugins",
            "owned",
        ):
            (stage / relative).mkdir(parents=True, exist_ok=True)

        if owned_root.is_dir():
            for skill_file in sorted(owned_root.glob("*/SKILL.md")):
                copy_skill(skill_file.parent, stage / "owned" / skill_file.parent.name)

        catalog: list[dict[str, Any]] = []
        git_cache: dict[Path, dict[str, Any]] = {}
        _snapshot_direct(
            stage,
            agents_root,
            stage / "active" / "agents",
            "agents",
            "~/.agents/skills",
            catalog,
            git_cache,
            owned_root,
        )
        _snapshot_direct(
            stage,
            codex_root,
            stage / "active" / "codex",
            "codex",
            "~/.codex/skills",
            catalog,
            git_cache,
            owned_root,
        )
        _snapshot_system(stage, codex_root, catalog)
        _snapshot_plugins(stage, plugins_root, catalog)
        _catalog_owned(stage, catalog)

        catalog.sort(key=lambda entry: entry["path"])
        _write_json(stage / "catalog.json", catalog)
        _write_json(stage / "manifest.json", _manifest(stage))
        _validate_stage(stage, catalog)
        _replace_generated(repository, stage)
    return catalog


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--agents-root", type=Path, default=Path("~/.agents/skills"))
    parser.add_argument("--codex-root", type=Path, default=Path("~/.codex/skills"))
    parser.add_argument("--plugins-root", type=Path, default=Path("~/.codex/plugins/cache"))
    args = parser.parse_args()
    catalog = sync_repository(
        args.repository,
        args.agents_root,
        args.codex_root,
        args.plugins_root,
    )
    counts: dict[str, int] = {}
    for entry in catalog:
        counts[entry["source_group"]] = counts.get(entry["source_group"], 0) + 1
    print(f"Synced {len(catalog)} skills: {json.dumps(counts, sort_keys=True)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
