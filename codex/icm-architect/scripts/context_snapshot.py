#!/usr/bin/env python3
"""Fingerprint declared paths for bounded, best-effort freshness checks.

This is not an atomic filesystem snapshot. It covers only declared paths and
does not establish semantic dependency completeness, permissions, acceptance,
or audit completion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Iterable


FORMAT = "icm-context-snapshot"
SCHEMA_VERSION = 1
DEFAULT_MAX_FILES = 10_000
DEFAULT_MAX_BYTES = 128 * 1024 * 1024
MAX_ENTRIES = 50_000
MAX_DEPTH = 128
MAX_MANIFEST_BYTES = 16 * 1024 * 1024
LIMITATIONS = [
    "best-effort metadata checks do not create an atomic snapshot",
    "only explicitly declared paths are covered",
    "semantic dependency completeness is not established",
    "permissions, acceptance, and audit completion are not established",
]
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


class SnapshotError(ValueError):
    """The requested snapshot operation is invalid or incomplete."""


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_link_or_reparse(info: os.stat_result) -> bool:
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & _REPARSE
    )


def _metadata(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_mode,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
        info.st_dev,
        info.st_ino,
    )


def _check_existing_component(path: Path) -> os.stat_result:
    try:
        info = path.lstat()
    except OSError as exc:
        raise SnapshotError(f"cannot inspect path: {path}") from exc
    if _is_link_or_reparse(info):
        raise SnapshotError(f"symlinks and reparse points are not allowed: {path}")
    return info


def _check_root(root: str | os.PathLike[str]) -> tuple[Path, dict[str, Any]]:
    raw = Path(os.path.abspath(os.fspath(root)))
    for component in list(reversed(raw.parents)) + [raw]:
        if component.exists() or component.is_symlink():
            _check_existing_component(component)
        else:
            raise SnapshotError(f"root does not exist: {raw}")
    resolved = raw.resolve(strict=True)
    info = _check_existing_component(resolved)
    if not stat.S_ISDIR(info.st_mode):
        raise SnapshotError(f"root is not a directory: {resolved}")
    return resolved, {
        "path": os.path.normcase(str(resolved)),
        "device": int(info.st_dev),
        "inode": int(info.st_ino),
    }


def _normalize_relative(value: object) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise SnapshotError("dependency paths must be non-empty strings")
    win = PureWindowsPath(value)
    posix = PurePosixPath(value.replace("\\", "/"))
    if win.is_absolute() or win.drive or posix.is_absolute():
        raise SnapshotError(f"absolute dependency path is not allowed: {value}")
    if any(part == ".." for part in posix.parts):
        raise SnapshotError(f"path traversal is not allowed: {value}")
    if any(":" in part for part in posix.parts):
        raise SnapshotError(f"alternate-stream path syntax is not allowed: {value}")
    if os.name == "nt" and any(part.rstrip(". ") != part for part in posix.parts):
        raise SnapshotError(f"Win32 path alias syntax is not allowed: {value}")
    normalized = posix.as_posix()
    if normalized in ("", "/"):
        raise SnapshotError("dependency path is empty")
    return normalized


def _under(parent: str, child: str) -> bool:
    return parent == "." or child == parent or child.startswith(parent + "/")


def _path_key(value: str) -> str:
    return value.casefold() if os.name == "nt" else value


def _normalize_selections(values: Iterable[str]) -> list[str]:
    selected = sorted(
        (_normalize_relative(value) for value in values), key=_path_key
    )
    if not selected:
        raise SnapshotError("at least one dependency path is required")
    for index, value in enumerate(selected):
        if index and _path_key(value) == _path_key(selected[index - 1]):
            raise SnapshotError(f"duplicate dependency path: {value}")
        for earlier in selected[:index]:
            if _under(_path_key(earlier), _path_key(value)):
                raise SnapshotError(
                    f"overlapping dependency paths are not allowed: {earlier}, {value}"
                )
    return selected


def _check_target_chain(
    root: Path,
    relative: str,
    *,
    allow_missing: bool,
    watched: dict[Path, tuple[int, ...]],
    traversal: _TraversalBudget,
) -> Path | None:
    current = root
    watched.setdefault(root, _metadata(_check_existing_component(root)))
    for part in PurePosixPath(relative).parts:
        if part == ".":
            continue
        current = current / part
        traversal.admit_path(root, current)
        try:
            info = current.lstat()
        except FileNotFoundError:
            if allow_missing:
                return None
            raise SnapshotError(f"cannot inspect path: {current}")
        except OSError as exc:
            raise SnapshotError(f"cannot inspect path: {current}") from exc
        if _is_link_or_reparse(info):
            raise SnapshotError(
                f"symlinks and reparse points are not allowed: {current}"
            )
        watched.setdefault(current, _metadata(info))
    return current


class _Budget:
    def __init__(self, max_files: int, max_bytes: int) -> None:
        if not _is_int(max_files) or max_files < 0:
            raise SnapshotError("max_files must be a non-negative integer")
        if not _is_int(max_bytes) or max_bytes < 0:
            raise SnapshotError("max_bytes must be a non-negative integer")
        self.max_files = max_files
        self.max_bytes = max_bytes
        self.files = 0
        self.bytes = 0

    def admit(self, size: int) -> None:
        if self.files + 1 > self.max_files:
            raise SnapshotError(f"file limit exceeded ({self.max_files})")
        if self.bytes + size > self.max_bytes:
            raise SnapshotError(f"byte limit exceeded ({self.max_bytes})")
        self.files += 1
        self.bytes += size


class _TraversalBudget:
    def __init__(self) -> None:
        self.entries = 0
        self.seen: set[str] = set()

    def admit_path(self, root: Path, path: Path) -> None:
        relative = path.relative_to(root)
        depth = len(relative.parts)
        if depth > MAX_DEPTH:
            raise SnapshotError(f"directory depth limit exceeded ({MAX_DEPTH})")
        key = _path_key(relative.as_posix())
        if key in self.seen:
            return
        self.seen.add(key)
        self.entries += 1
        if self.entries > MAX_ENTRIES:
            raise SnapshotError(f"directory entry limit exceeded ({MAX_ENTRIES})")


def _hash_file(root: Path, path: Path, budget: _Budget) -> dict[str, Any]:
    before = _check_existing_component(path)
    if not stat.S_ISREG(before.st_mode):
        raise SnapshotError(f"dependency is not a regular file: {path}")
    budget.admit(before.st_size)
    digest = hashlib.sha256()
    actual = 0
    try:
        with path.open("rb") as handle:
            opened = os.fstat(handle.fileno())
            if _metadata(opened) != _metadata(before):
                raise SnapshotError(f"file changed while being opened: {path}")
            while chunk := handle.read(1024 * 1024):
                actual += len(chunk)
                if budget.bytes - before.st_size + actual > budget.max_bytes:
                    raise SnapshotError(f"byte limit exceeded ({budget.max_bytes})")
                digest.update(chunk)
            after_fd = os.fstat(handle.fileno())
    except OSError as exc:
        raise SnapshotError(f"cannot read dependency: {path}") from exc
    after_path = _check_existing_component(path)
    if (
        actual != before.st_size
        or _metadata(after_fd) != _metadata(before)
        or _metadata(after_path) != _metadata(before)
    ):
        raise SnapshotError(f"file changed while being fingerprinted: {path}")
    return {
        "path": path.relative_to(root).as_posix(),
        "size": actual,
        "sha256": digest.hexdigest(),
    }


def _walk_directory(
    root: Path,
    directory: Path,
    budget: _Budget,
    traversal: _TraversalBudget,
    files: list[dict[str, Any]],
) -> None:
    before = _check_existing_component(directory)
    try:
        with os.scandir(directory) as iterator:
            for entry in iterator:
                path = Path(entry.path)
                traversal.admit_path(root, path)
                info = _check_existing_component(path)
                if stat.S_ISDIR(info.st_mode):
                    _walk_directory(root, path, budget, traversal, files)
                elif stat.S_ISREG(info.st_mode):
                    files.append(_hash_file(root, path, budget))
                else:
                    raise SnapshotError(f"unsupported dependency type: {path}")
    except OSError as exc:
        raise SnapshotError(f"cannot enumerate dependency directory: {directory}") from exc
    after = _check_existing_component(directory)
    if _metadata(after) != _metadata(before):
        raise SnapshotError(f"directory changed while being fingerprinted: {directory}")


def _scan(
    root: Path,
    selected: list[str],
    *,
    max_files: int,
    max_bytes: int,
    allow_missing: bool,
) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[str]]:
    budget = _Budget(max_files, max_bytes)
    selection_records: list[dict[str, str]] = []
    files: list[dict[str, Any]] = []
    missing: list[str] = []
    watched: dict[Path, tuple[int, ...]] = {}
    traversal = _TraversalBudget()
    physical_targets: set[str] = set()
    physical_ancestors: set[str] = set()
    physical_identities: set[tuple[int, int]] = set()
    try:
        for relative in selected:
            target = _check_target_chain(
                root,
                relative,
                allow_missing=allow_missing,
                watched=watched,
                traversal=traversal,
            )
            if target is None:
                missing.append(relative)
                continue
            info = _check_existing_component(target)
            canonical = Path(os.path.realpath(target))
            canonical_key = _path_key(str(canonical))
            parent_keys = {_path_key(str(parent)) for parent in canonical.parents}
            identity_key = (int(info.st_dev), int(info.st_ino))
            if (
                canonical_key in physical_targets
                or canonical_key in physical_ancestors
                or bool(parent_keys & physical_targets)
                or identity_key in physical_identities
            ):
                raise SnapshotError(f"physically overlapping dependency path: {relative}")
            physical_targets.add(canonical_key)
            physical_ancestors.update(parent_keys)
            physical_identities.add(identity_key)
            if stat.S_ISREG(info.st_mode):
                selection_records.append({"path": relative, "type": "file"})
                files.append(_hash_file(root, target, budget))
            elif stat.S_ISDIR(info.st_mode):
                selection_records.append({"path": relative, "type": "directory"})
                _walk_directory(root, target, budget, traversal, files)
            else:
                raise SnapshotError(f"unsupported dependency type: {target}")
    except RecursionError as exc:
        raise SnapshotError("directory traversal recursion limit exceeded") from exc
    for path, expected in watched.items():
        if _metadata(_check_existing_component(path)) != expected:
            raise SnapshotError(f"path changed while being fingerprinted: {path}")
    return selection_records, sorted(files, key=lambda item: item["path"]), missing


def capture_snapshot(
    root: str | os.PathLike[str],
    selected_paths: Iterable[str],
    *,
    max_files: int = DEFAULT_MAX_FILES,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> dict[str, Any]:
    root_path, identity = _check_root(root)
    selected = _normalize_selections(selected_paths)
    selection_records, files, missing = _scan(
        root_path,
        selected,
        max_files=max_files,
        max_bytes=max_bytes,
        allow_missing=False,
    )
    if missing:
        raise SnapshotError(f"missing capture targets: {', '.join(missing)}")
    return {
        "format": FORMAT,
        "schema_version": SCHEMA_VERSION,
        "root_identity": identity,
        "selected": selection_records,
        "files": files,
        "limitations": LIMITATIONS,
    }


def _validate_manifest(
    manifest: object, *, max_files: int, max_bytes: int
) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        raise SnapshotError("manifest must be a JSON object")
    required = {
        "format",
        "schema_version",
        "root_identity",
        "selected",
        "files",
        "limitations",
    }
    if set(manifest) != required:
        raise SnapshotError("manifest fields are missing or unsupported")
    if manifest["format"] != FORMAT:
        raise SnapshotError("unsupported manifest format")
    if (
        not _is_int(manifest["schema_version"])
        or manifest["schema_version"] != SCHEMA_VERSION
    ):
        raise SnapshotError("unsupported manifest schema version")
    if manifest["limitations"] != LIMITATIONS:
        raise SnapshotError("manifest limitations are missing or altered")
    identity = manifest["root_identity"]
    if (
        not isinstance(identity, dict)
        or set(identity) != {"path", "device", "inode"}
        or not isinstance(identity["path"], str)
        or not os.path.isabs(identity["path"])
        or not _is_int(identity["device"])
        or not _is_int(identity["inode"])
        or identity["device"] < 0
        or identity["inode"] < 0
    ):
        raise SnapshotError("invalid root identity")
    entries = manifest["selected"]
    if not isinstance(entries, list) or not entries:
        raise SnapshotError("selected must be a non-empty list")
    paths: list[str] = []
    types: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "type"}:
            raise SnapshotError("invalid selected entry")
        path = _normalize_relative(entry["path"])
        if (
            path != entry["path"]
            or not isinstance(entry["type"], str)
            or entry["type"] not in {"file", "directory"}
        ):
            raise SnapshotError("invalid selected path or type")
        paths.append(path)
        types[path] = entry["type"]
    if paths != sorted(paths, key=_path_key) or len({_path_key(path) for path in paths}) != len(paths):
        raise SnapshotError("selected paths must be unique and sorted")
    _normalize_selections(paths)
    records = manifest["files"]
    if not isinstance(records, list):
        raise SnapshotError("files must be a list")
    manifest_budget = _Budget(max_files, max_bytes)
    file_paths: list[str] = []
    for record in records:
        if not isinstance(record, dict) or set(record) != {"path", "size", "sha256"}:
            raise SnapshotError("invalid file record")
        path = _normalize_relative(record["path"])
        if (
            path != record["path"]
            or path == "."
            or not _is_int(record["size"])
            or record["size"] < 0
            or not isinstance(record["sha256"], str)
            or not _SHA256.fullmatch(record["sha256"])
        ):
            raise SnapshotError("invalid file fingerprint")
        manifest_budget.admit(record["size"])
        owners = [
            selected
            for selected in paths
            if (
                types[selected] == "file"
                and _path_key(selected) == _path_key(path)
            )
            or (
                types[selected] == "directory"
                and _path_key(selected) != _path_key(path)
                and _under(_path_key(selected), _path_key(path))
            )
        ]
        if len(owners) != 1:
            raise SnapshotError("file record is outside or incoherent with selection")
        file_paths.append(path)
    if file_paths != sorted(file_paths) or len({_path_key(path) for path in file_paths}) != len(file_paths):
        raise SnapshotError("file records must be unique and sorted")
    for path in paths:
        if types[path] == "file" and file_paths.count(path) != 1:
            raise SnapshotError("selected file lacks exactly one fingerprint")
    return manifest


def check_snapshot(
    root: str | os.PathLike[str],
    manifest: object,
    *,
    max_files: int = DEFAULT_MAX_FILES,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> dict[str, Any]:
    valid = _validate_manifest(
        manifest, max_files=max_files, max_bytes=max_bytes
    )
    root_path, identity = _check_root(root)
    if identity != valid["root_identity"]:
        raise SnapshotError("root identity does not match manifest")
    selected = [entry["path"] for entry in valid["selected"]]
    current_selected, current_files, missing = _scan(
        root_path,
        selected,
        max_files=max_files,
        max_bytes=max_bytes,
        allow_missing=True,
    )
    expected_types = {entry["path"]: entry["type"] for entry in valid["selected"]}
    current_types = {entry["path"]: entry["type"] for entry in current_selected}
    selection_changed = sorted(
        path for path in selected if expected_types[path] != current_types.get(path)
    )
    old = {item["path"]: item for item in valid["files"]}
    new = {item["path"]: item for item in current_files}
    added = sorted(new.keys() - old.keys())
    removed = sorted(old.keys() - new.keys())
    changed = sorted(path for path in old.keys() & new.keys() if old[path] != new[path])
    stale = bool(added or removed or changed or selection_changed or missing)
    return {
        "status": "stale" if stale else "current",
        "added": added,
        "removed": removed,
        "changed": changed,
        "selection_changed": selection_changed,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    capture = subparsers.add_parser("capture")
    capture.add_argument("--root", required=True)
    capture.add_argument("--path", action="append", required=True, dest="paths")
    check = subparsers.add_parser("check")
    check.add_argument("--root", required=True)
    check.add_argument("--manifest", required=True)
    for command in (capture, check):
        command.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES)
        command.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    return parser


def _read_manifest(path: str | os.PathLike[str]) -> object:
    manifest_path = Path(path)
    try:
        before = manifest_path.stat()
        if not stat.S_ISREG(before.st_mode):
            raise SnapshotError("manifest is not a regular file")
        if before.st_size > MAX_MANIFEST_BYTES:
            raise SnapshotError(
                f"manifest file limit exceeded ({MAX_MANIFEST_BYTES} bytes)"
            )
        with manifest_path.open("rb") as handle:
            opened = os.fstat(handle.fileno())
            if _metadata(opened) != _metadata(before):
                raise SnapshotError("manifest changed while being opened")
            payload = handle.read(MAX_MANIFEST_BYTES + 1)
            after_fd = os.fstat(handle.fileno())
        after_path = manifest_path.stat()
    except SnapshotError:
        raise
    except OSError as exc:
        raise SnapshotError("manifest cannot be read") from exc
    if len(payload) > MAX_MANIFEST_BYTES:
        raise SnapshotError(
            f"manifest file limit exceeded ({MAX_MANIFEST_BYTES} bytes)"
        )
    if (
        len(payload) != before.st_size
        or _metadata(after_fd) != _metadata(before)
        or _metadata(after_path) != _metadata(before)
    ):
        raise SnapshotError("manifest changed while being read")
    try:
        return json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise SnapshotError("manifest cannot be read as JSON") from exc


def main(argv: list[str] | None = None) -> int:
    try:
        args = _parser().parse_args(argv)
        if args.command == "capture":
            output = capture_snapshot(
                args.root,
                args.paths,
                max_files=args.max_files,
                max_bytes=args.max_bytes,
            )
            code = 0
        else:
            manifest = _read_manifest(args.manifest)
            output = check_snapshot(
                args.root,
                manifest,
                max_files=args.max_files,
                max_bytes=args.max_bytes,
            )
            code = 0 if output["status"] == "current" else 1
    except (SnapshotError, OSError, TypeError, RecursionError) as exc:
        output = {"status": "invalid", "error": str(exc)}
        code = 2
    json.dump(output, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
