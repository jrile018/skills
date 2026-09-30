#!/usr/bin/env python3
"""Validate catalog, profiles, hashes, and Codex-compatible skill packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


SNAPSHOT_ROOTS = ("active", "managed", "owned")
DEFAULT_QUICK_VALIDATOR = (
    Path(__file__).resolve().parents[1]
    / "managed/codex-system/skill-creator/scripts/quick_validate.py"
)
DEFAULT_VALIDATOR_EXCEPTIONS = (
    Path(__file__).resolve().parents[1] / "validator-exceptions.json"
)
SENSITIVE_NAMES = {
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
SECRET_PATTERNS = {
    "AWS access key": re.compile(rb"AKIA[0-9A-Z]{16}"),
    "GitHub token": re.compile(rb"gh[pousr]_[A-Za-z0-9_]{30,}"),
    "OpenAI key": re.compile(rb"sk-(?:proj-)?[A-Za-z0-9_-]{32,}"),
    "private key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Slack token": re.compile(rb"xox[baprs]-[A-Za-z0-9-]{20,}"),
}


def _load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"cannot read {path.name}: {error}")
        return None


def _actual_files(repository: Path) -> set[str]:
    paths: set[str] = set()
    for root_name in SNAPSHOT_ROOTS:
        root = repository / root_name
        if root.is_dir():
            paths.update(
                path.relative_to(repository).as_posix()
                for path in root.rglob("*")
                if path.is_file()
            )
    return paths


def _safe_snapshot_path(repository: Path, relative: str) -> Path | None:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    if not candidate.parts or candidate.parts[0] not in SNAPSHOT_ROOTS:
        return None
    resolved = (repository / candidate).resolve()
    try:
        resolved.relative_to(repository)
    except ValueError:
        return None
    return resolved


def validate_repository(
    repository: Path,
    run_skill_validator: bool = True,
    quick_validator: Path = DEFAULT_QUICK_VALIDATOR,
    validator_exceptions: Path = DEFAULT_VALIDATOR_EXCEPTIONS,
) -> list[str]:
    repository = repository.resolve()
    errors: list[str] = []
    catalog = _load_json(repository / "catalog.json", errors)
    profiles = _load_json(repository / "profiles.json", errors)
    manifest = _load_json(repository / "manifest.json", errors)
    if not isinstance(catalog, list) or not isinstance(manifest, list):
        return errors

    catalog_paths: set[str] = set()
    for entry in catalog:
        if not isinstance(entry, dict):
            errors.append("catalog entry is not an object")
            continue
        path_text = entry.get("path")
        name = entry.get("name")
        if not isinstance(path_text, str) or not isinstance(name, str):
            errors.append(f"catalog entry lacks string name/path: {entry!r}")
            continue
        if _safe_snapshot_path(repository, path_text) is None:
            errors.append(f"unsafe catalog path: {path_text}")
            continue
        if path_text in catalog_paths:
            errors.append(f"duplicate catalog path: {path_text}")
        catalog_paths.add(path_text)
        skill_path = repository / path_text / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"catalog path lacks SKILL.md: {path_text}")

    if isinstance(profiles, dict):
        for profile_name, profile in profiles.get("profiles", {}).items():
            if not isinstance(profile, dict):
                errors.append(f"profile is not an object: {profile_name}")
                continue
            references = profile.get("skill_paths")
            if not isinstance(references, list):
                errors.append(f"profile {profile_name} lacks skill_paths list")
                continue
            for path_text in references:
                if path_text not in catalog_paths:
                    errors.append(
                        f"profile {profile_name} references missing skill path: {path_text}"
                    )

    manifest_paths: set[str] = set()
    for entry in manifest:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            errors.append(f"invalid manifest entry: {entry!r}")
            continue
        relative = entry["path"]
        if relative in manifest_paths:
            errors.append(f"duplicate manifest path: {relative}")
            continue
        manifest_paths.add(relative)
        path = _safe_snapshot_path(repository, relative)
        if path is None:
            errors.append(f"unsafe manifest path: {relative}")
            continue
        if not path.is_file():
            errors.append(f"manifest path is missing: {relative}")
            continue
        data = path.read_bytes()
        if entry.get("bytes") != len(data):
            errors.append(f"manifest size mismatch: {relative}")
        if entry.get("sha256") != hashlib.sha256(data).hexdigest():
            errors.append(f"manifest hash mismatch: {relative}")

    actual_files = _actual_files(repository)
    for relative in sorted(actual_files - manifest_paths):
        errors.append(f"file missing from manifest: {relative}")
    for relative in sorted(manifest_paths - actual_files):
        errors.append(f"manifest includes non-snapshot file: {relative}")

    actual_skill_paths = {
        (path.parent.relative_to(repository).as_posix())
        for root_name in SNAPSHOT_ROOTS
        for path in (repository / root_name).rglob("SKILL.md")
        if path.is_file()
    }
    for path_text in sorted(actual_skill_paths - catalog_paths):
        errors.append(f"skill missing from catalog: {path_text}")
    for path_text in sorted(catalog_paths - actual_skill_paths):
        errors.append(f"catalog entry is not a discovered skill: {path_text}")

    for relative in sorted(actual_files):
        path = repository / relative
        if path.is_symlink():
            errors.append(f"snapshot contains symlink: {relative}")
            continue
        lowered = path.name.lower()
        if lowered in SENSITIVE_NAMES or lowered.endswith((".key", ".p12", ".pem", ".pfx")):
            errors.append(f"snapshot contains sensitive filename: {relative}")
            continue
        data = path.read_bytes()
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(data):
                errors.append(f"snapshot contains possible {label}: {relative}")

    if run_skill_validator and not quick_validator.is_file():
        errors.append(f"skill validator is unavailable: {quick_validator}")
    elif run_skill_validator:
        exception_data = _load_json(validator_exceptions, errors)
        exceptions = exception_data if isinstance(exception_data, dict) else {}
        seen_exceptions: set[str] = set()
        for entry in catalog:
            completed = subprocess.run(
                ["python3", str(quick_validator), str(repository / entry["path"])],
                check=False,
                capture_output=True,
                text=True,
            )
            if completed.returncode:
                if entry["path"] in exceptions:
                    seen_exceptions.add(entry["path"])
                    continue
                detail = (completed.stdout + completed.stderr).strip().replace("\n", " | ")
                errors.append(f"skill validation failed: {entry['path']}: {detail}")
            elif entry["path"] in exceptions:
                errors.append(f"stale validator exception now passes: {entry['path']}")
        for path_text in sorted(set(exceptions) - seen_exceptions):
            if path_text not in catalog_paths:
                errors.append(f"validator exception is not in catalog: {path_text}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--quick-validator", type=Path, default=DEFAULT_QUICK_VALIDATOR)
    parser.add_argument(
        "--validator-exceptions", type=Path, default=DEFAULT_VALIDATOR_EXCEPTIONS
    )
    parser.add_argument("--skip-skill-validator", action="store_true")
    args = parser.parse_args()
    errors = validate_repository(
        args.repository,
        run_skill_validator=not args.skip_skill_validator,
        quick_validator=args.quick_validator.expanduser(),
        validator_exceptions=args.validator_exceptions,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Validation failed with {len(errors)} error(s).")
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
