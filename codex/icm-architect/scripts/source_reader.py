#!/usr/bin/env python3
"""Read a bounded, explicitly selected source range with truthful metadata.

This reader reports syntactic or explicit ranges.  It does not establish that
any consumer read the returned text, resolve names semantically, or understand
the surrounding codebase.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import os
import re
import stat
import sys
import tokenize
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


MAX_SOURCE_BYTES = 4 * 1024 * 1024
MAX_REQUEST_LINES = 1000
MAX_REQUEST_CHARS = 100_000
DEFAULT_MAX_LINES = 160
DEFAULT_MAX_CHARS = 20_000
_SHA256 = re.compile(r"[0-9a-fA-F]{64}\Z")
_REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
_WINDOWS_DEVICES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "CLOCK$",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}
LIMITATIONS = [
    "completeness covers only the selected syntactic or explicit range",
    "no semantic resolution, codebase understanding, or consumer receipt is proven",
    "file identity is a best-effort check, not an atomic snapshot against concurrent mutation",
]


class SourceReaderError(ValueError):
    """A safe, categorized error suitable for the public result."""

    def __init__(self, category: str, message: str, **extra: Any) -> None:
        super().__init__(message)
        self.category = category
        self.message = message
        self.extra = extra


class _JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        del message
        raise SourceReaderError(
            "invalid_input", "invalid or incomplete command-line arguments"
        )


def _error_result(error: SourceReaderError) -> dict[str, Any]:
    result: dict[str, Any] = {
        "ok": False,
        "error": {"category": error.category, "message": error.message},
        "transport_status": "unknown",
        "limitations": LIMITATIONS,
    }
    result.update(error.extra)
    return result


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_link_or_reparse(info: os.stat_result) -> bool:
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & _REPARSE
    )


def _metadata(info: os.stat_result) -> tuple[int, ...]:
    return (
        int(info.st_mode),
        int(info.st_size),
        int(info.st_mtime_ns),
        int(info.st_ctime_ns),
        int(info.st_dev),
        int(info.st_ino),
    )


def _validate_bounds(
    *,
    line: object,
    symbol: object,
    start: object,
    end: object,
    max_lines: object,
    max_chars: object,
    expected_sha256: object,
) -> tuple[str, int | None, str | None, int | None, int | None, int, int, str | None]:
    if not _is_int(max_lines) or not 1 <= max_lines <= MAX_REQUEST_LINES:
        raise SourceReaderError(
            "invalid_input", f"max_lines must be an integer from 1 to {MAX_REQUEST_LINES}"
        )
    if not _is_int(max_chars) or not 1 <= max_chars <= MAX_REQUEST_CHARS:
        raise SourceReaderError(
            "invalid_input", f"max_chars must be an integer from 1 to {MAX_REQUEST_CHARS}"
        )

    has_line = line is not None
    has_symbol = symbol is not None
    has_range = start is not None or end is not None
    if sum((has_line, has_symbol, has_range)) != 1:
        raise SourceReaderError(
            "invalid_input", "exactly one of line, symbol, or start/end is required"
        )

    if has_line:
        if not _is_int(line) or line < 1:
            raise SourceReaderError("invalid_input", "line must be a positive integer")
        mode = "line"
    elif has_symbol:
        if (
            not isinstance(symbol, str)
            or not symbol
            or any(not part.isidentifier() for part in symbol.split("."))
        ):
            raise SourceReaderError(
                "invalid_input", "symbol must be a dotted qualified Python name"
            )
        mode = "symbol"
    else:
        if (
            not _is_int(start)
            or not _is_int(end)
            or start < 1
            or end < start
        ):
            raise SourceReaderError(
                "invalid_input", "start and end must be positive integers with start <= end"
            )
        mode = "range"

    normalized_hash: str | None = None
    if expected_sha256 is not None:
        if not isinstance(expected_sha256, str) or not _SHA256.fullmatch(expected_sha256):
            raise SourceReaderError(
                "invalid_input", "expected_sha256 must be a 64-character hexadecimal digest"
            )
        normalized_hash = expected_sha256.lower()

    return (
        mode,
        line if isinstance(line, int) else None,
        symbol if isinstance(symbol, str) else None,
        start if isinstance(start, int) else None,
        end if isinstance(end, int) else None,
        max_lines,
        max_chars,
        normalized_hash,
    )


def _normalize_relative_path(value: object) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise SourceReaderError("invalid_path", "path must be a non-empty relative string")
    windows = PureWindowsPath(value)
    slash_value = value.replace("\\", "/")
    posix = PurePosixPath(slash_value)
    if windows.is_absolute() or windows.drive or posix.is_absolute():
        raise SourceReaderError("invalid_path", "absolute, drive, and UNC paths are not allowed")
    raw_parts = slash_value.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        raise SourceReaderError("invalid_path", "path traversal and path aliases are not allowed")
    for part in raw_parts:
        if ":" in part or part.rstrip(" .") != part:
            raise SourceReaderError(
                "invalid_path", "alternate-stream and Win32 alias syntax is not allowed"
            )
        stem = part.split(".", 1)[0].upper()
        if stem in _WINDOWS_DEVICES:
            raise SourceReaderError("invalid_path", "reserved device path aliases are not allowed")
    return posix.as_posix()


def _checked_root(root: object) -> Path:
    try:
        raw = os.fspath(root)  # type: ignore[arg-type]
    except TypeError as exc:
        raise SourceReaderError("invalid_root", "root must identify a local directory") from exc
    if not isinstance(raw, (str, bytes)) or (isinstance(raw, str) and "\x00" in raw):
        raise SourceReaderError("invalid_root", "root must identify a local directory")
    try:
        path = Path(os.path.abspath(raw))
        info = path.lstat()
    except (OSError, ValueError) as exc:
        raise SourceReaderError("invalid_root", "root cannot be inspected") from exc
    if _is_link_or_reparse(info):
        raise SourceReaderError("invalid_root", "root must not be a symlink or reparse point")
    if not stat.S_ISDIR(info.st_mode):
        raise SourceReaderError("invalid_root", "root is not a directory")
    try:
        return path.resolve(strict=True)
    except OSError as exc:
        raise SourceReaderError("invalid_root", "root cannot be resolved") from exc


def _checked_source(root: Path, relative: str) -> Path:
    current = root
    parts = PurePosixPath(relative).parts
    for index, part in enumerate(parts):
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError as exc:
            raise SourceReaderError("not_found", "source path does not exist") from exc
        except OSError as exc:
            raise SourceReaderError("unreadable", "source path cannot be inspected") from exc
        if _is_link_or_reparse(info):
            raise SourceReaderError(
                "invalid_path", "source path components must not be symlinks or reparse points"
            )
        if index < len(parts) - 1 and not stat.S_ISDIR(info.st_mode):
            raise SourceReaderError("invalid_path", "a source path component is not a directory")
    try:
        resolved = current.resolve(strict=True)
        if os.path.commonpath((str(root), str(resolved))) != str(root):
            raise SourceReaderError("invalid_path", "source path escapes root")
        final_info = current.lstat()
    except SourceReaderError:
        raise
    except (OSError, ValueError) as exc:
        raise SourceReaderError("unreadable", "source path cannot be resolved") from exc
    if not stat.S_ISREG(final_info.st_mode):
        raise SourceReaderError("invalid_path", "source path is not a regular file")
    return current


def _read_raw(path: Path) -> bytes:
    try:
        before = path.lstat()
        if before.st_size > MAX_SOURCE_BYTES:
            raise SourceReaderError(
                "source_too_large", f"source exceeds the {MAX_SOURCE_BYTES}-byte limit"
            )
        with path.open("rb") as handle:
            opened = os.fstat(handle.fileno())
            if _metadata(opened) != _metadata(before):
                raise SourceReaderError("source_changed", "source changed while being opened")
            payload = handle.read(MAX_SOURCE_BYTES + 1)
            after_handle = os.fstat(handle.fileno())
        after_path = path.lstat()
    except SourceReaderError:
        raise
    except OSError as exc:
        raise SourceReaderError("unreadable", "source file cannot be read") from exc
    if len(payload) > MAX_SOURCE_BYTES:
        raise SourceReaderError(
            "source_too_large", f"source exceeds the {MAX_SOURCE_BYTES}-byte limit"
        )
    if (
        len(payload) != before.st_size
        or _metadata(after_handle) != _metadata(before)
        or _metadata(after_path) != _metadata(before)
    ):
        raise SourceReaderError("source_changed", "source changed while being read")
    if b"\x00" in payload:
        raise SourceReaderError("binary", "binary or NUL-containing source is not supported")
    return payload


def _is_python(relative: str) -> bool:
    return PurePosixPath(relative).suffix.casefold() in {".py", ".pyi", ".pyw"}


def _decode_source(payload: bytes, *, python_source: bool) -> str:
    try:
        if python_source:
            encoding, _ = tokenize.detect_encoding(io.BytesIO(payload).readline)
        else:
            encoding = "utf-8"
        source = payload.decode(encoding)
    except (LookupError, SyntaxError, UnicodeError) as exc:
        raise SourceReaderError("decode_error", "source encoding cannot be decoded safely") from exc
    allowed_controls = {"\t", "\n", "\r", "\f"}
    if any(
        unicodedata.category(character) == "Cc" and character not in allowed_controls
        for character in source
    ):
        raise SourceReaderError(
            "binary", "source contains control characters outside the text policy"
        )
    return source


def _split_physical_lines(source: str) -> list[str]:
    """Split only on the newline sequences used for Python line positions."""

    lines: list[str] = []
    start = 0
    index = 0
    while index < len(source):
        character = source[index]
        if character == "\n":
            index += 1
            lines.append(source[start:index])
            start = index
        elif character == "\r":
            index += 1
            if index < len(source) and source[index] == "\n":
                index += 1
            lines.append(source[start:index])
            start = index
        else:
            index += 1
    if start < len(source):
        lines.append(source[start:])
    return lines


def _decorator_tokens(source: str) -> list[tuple[int, int]]:
    """Return leading decorator ``@`` positions, excluding operators in expressions."""

    positions: list[tuple[int, int]] = []
    bracket_depth = 0
    logical_start = True
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source, newline=None).readline)
        for token in tokens:
            token_type = token.type
            token_text = token.string
            if token_type in {tokenize.INDENT, tokenize.DEDENT}:
                continue
            if token_type == tokenize.NEWLINE:
                logical_start = True
                continue
            if token_type == tokenize.NL:
                if bracket_depth == 0:
                    logical_start = True
                continue
            if token_type in {tokenize.COMMENT, tokenize.ENDMARKER}:
                continue
            if token_text == "@" and logical_start and bracket_depth == 0:
                positions.append(token.start)
            logical_start = False
            if token_text in {"(", "[", "{"}:
                bracket_depth += 1
            elif token_text in {")",
                "]",
                "}",
            } and bracket_depth:
                bracket_depth -= 1
    except (IndentationError, tokenize.TokenError):
        return []
    return positions


def _node_start(node: ast.AST, decorator_tokens: list[tuple[int, int]]) -> int:
    declaration_start = int(getattr(node, "lineno"))
    decorators = getattr(node, "decorator_list", [])
    if not decorators:
        return declaration_start
    column = int(getattr(node, "col_offset"))
    candidates = [
        line
        for line, token_column in decorator_tokens
        if token_column == column and line < declaration_start
    ]
    if len(candidates) >= len(decorators):
        return candidates[-len(decorators)]
    return min(
        [declaration_start]
        + [
            int(decorator.lineno)
            for decorator in decorators
            if hasattr(decorator, "lineno")
        ]
    )


def _named_nodes(tree: ast.AST, source: str) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    decorator_tokens = _decorator_tokens(source)

    def visit(node: ast.AST, parents: tuple[str, ...]) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                qualified = ".".join((*parents, child.name))
                end = getattr(child, "end_lineno", None)
                if end is not None:
                    found.append(
                        {
                            "start": _node_start(child, decorator_tokens),
                            "end": int(end),
                            "symbol": qualified,
                            "depth": len(parents),
                        }
                    )
                visit(child, (*parents, child.name))
            else:
                visit(child, parents)

    visit(tree, ())
    return found


def _unit(start: int, end: int, symbol: str | None) -> dict[str, Any]:
    return {"start": start, "end": end, "symbol": symbol}


def _choose_selection(
    *,
    relative: str,
    source: str,
    lines: list[str],
    mode: str,
    line: int | None,
    symbol: str | None,
    start: int | None,
    end: int | None,
) -> tuple[str, str, dict[str, Any]]:
    total_lines = len(lines)
    if mode == "range":
        assert start is not None and end is not None
        if end > total_lines:
            raise SourceReaderError("invalid_input", "requested range is outside the source file")
        return "explicit_range", "not_requested", _unit(start, end, None)

    python_source = _is_python(relative)
    if not python_source:
        if mode == "symbol":
            raise SourceReaderError(
                "unsupported", "symbol selection requires syntactically valid Python source"
            )
        assert line is not None
        if line > total_lines:
            raise SourceReaderError("invalid_input", "line is outside the source file")
        return "fallback_range", "non_python", _unit(line, total_lines, None)

    try:
        tree = ast.parse(source, filename=relative, type_comments=True)
    except (SyntaxError, ValueError):
        if mode == "symbol":
            raise SourceReaderError(
                "unsupported", "symbol selection requires syntactically valid Python source"
            )
        assert line is not None
        if line > total_lines:
            raise SourceReaderError("invalid_input", "line is outside the source file")
        return "fallback_range", "syntax_error", _unit(line, total_lines, None)

    candidates = _named_nodes(tree, source)
    if mode == "symbol":
        assert symbol is not None
        matches = [candidate for candidate in candidates if candidate["symbol"] == symbol]
        public_matches = [
            _unit(match["start"], match["end"], match["symbol"]) for match in matches
        ]
        if not matches:
            raise SourceReaderError("not_found", "qualified symbol was not found")
        if len(matches) > 1:
            raise SourceReaderError(
                "ambiguity", "qualified symbol has multiple definitions", candidates=public_matches
            )
        match = matches[0]
        return "python_syntax", "parsed", _unit(
            match["start"], match["end"], match["symbol"]
        )

    assert line is not None
    if line > total_lines:
        raise SourceReaderError("invalid_input", "line is outside the source file")
    containing = [
        candidate
        for candidate in candidates
        if candidate["start"] <= line <= candidate["end"]
    ]
    if not containing:
        return "fallback_range", "parsed_no_named_unit", _unit(line, total_lines, None)
    match = min(
        containing,
        key=lambda candidate: (
            candidate["end"] - candidate["start"],
            -candidate["depth"],
            candidate["start"],
        ),
    )
    return "python_syntax", "parsed", _unit(
        match["start"], match["end"], match["symbol"]
    )


def _page(
    lines: list[str],
    *,
    selected_start: int,
    selected_end: int,
    max_lines: int,
    max_chars: int,
    digest: str,
) -> dict[str, Any]:
    rendered: list[str] = []
    returned_end: int | None = None
    used_chars = 0
    for number in range(selected_start, selected_end + 1):
        numbered = f"{number}: {lines[number - 1]}"
        if len(rendered) >= max_lines or used_chars + len(numbered) > max_chars:
            break
        rendered.append(numbered)
        used_chars += len(numbered)
        returned_end = number

    if returned_end is None:
        remaining = [{"start": selected_start, "end": selected_end}]
        returned = None
        next_start = selected_start
        budget_error = (
            "the first whole numbered line exceeds max_chars; no source line was returned"
        )
    else:
        returned = {"start": selected_start, "end": returned_end}
        next_start = returned_end + 1
        remaining = (
            [{"start": next_start, "end": selected_end}]
            if next_start <= selected_end
            else []
        )
        budget_error = None

    continuation = (
        {
            "start": remaining[0]["start"],
            "end": selected_end,
            "expected_sha256": digest,
        }
        if remaining
        else None
    )
    result: dict[str, Any] = {
        "returned": returned,
        "remaining": remaining,
        "complete": not remaining,
        "text": "".join(rendered),
        "continuation": continuation,
    }
    if budget_error is not None:
        result["budget_error"] = budget_error
    return result


def read_source(
    root: str | os.PathLike[str],
    path: str,
    *,
    line: int | None = None,
    symbol: str | None = None,
    start: int | None = None,
    end: int | None = None,
    max_lines: int = DEFAULT_MAX_LINES,
    max_chars: int = DEFAULT_MAX_CHARS,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    """Read one bounded selection and return JSON-serializable metadata."""

    try:
        (
            mode,
            checked_line,
            checked_symbol,
            checked_start,
            checked_end,
            checked_max_lines,
            checked_max_chars,
            checked_hash,
        ) = _validate_bounds(
            line=line,
            symbol=symbol,
            start=start,
            end=end,
            max_lines=max_lines,
            max_chars=max_chars,
            expected_sha256=expected_sha256,
        )
        relative = _normalize_relative_path(path)
        root_path = _checked_root(root)
        source_path = _checked_source(root_path, relative)
        payload = _read_raw(source_path)
        digest = hashlib.sha256(payload).hexdigest()
        if checked_hash is not None and digest != checked_hash:
            raise SourceReaderError(
                "hash_mismatch", "source hash does not match expected_sha256"
            )
        decoded = _decode_source(payload, python_source=_is_python(relative))
        lines = _split_physical_lines(decoded)
        selection_kind, parser_status, unit = _choose_selection(
            relative=relative,
            source=decoded,
            lines=lines,
            mode=mode,
            line=checked_line,
            symbol=checked_symbol,
            start=checked_start,
            end=checked_end,
        )
        page = _page(
            lines,
            selected_start=unit["start"],
            selected_end=unit["end"],
            max_lines=checked_max_lines,
            max_chars=checked_max_chars,
            digest=digest,
        )
        return {
            "ok": True,
            "path": relative,
            "sha256": digest,
            "selection_kind": selection_kind,
            "parser_status": parser_status,
            "unit": unit,
            **page,
            "limitations": LIMITATIONS,
            "transport_status": "unknown",
        }
    except SourceReaderError as exc:
        return _error_result(exc)
    except (OSError, TypeError, ValueError, RecursionError):
        return _error_result(
            SourceReaderError("internal_error", "source request could not be completed safely")
        )


def _parser() -> argparse.ArgumentParser:
    parser = _JsonArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--root", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--line", type=int)
    parser.add_argument("--symbol")
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--max-lines", type=int, default=DEFAULT_MAX_LINES)
    parser.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--log")
    return parser


def _prescan_option(argv: list[str], option: str) -> tuple[str | None, bool]:
    """Find a named option value without validating unrelated arguments."""

    requested = False
    destinations: list[str] = []
    index = 0
    while index < len(argv):
        argument = argv[index]
        if argument == "--":
            break
        if argument == option:
            requested = True
            if index + 1 < len(argv) and not argv[index + 1].startswith("--"):
                destinations.append(argv[index + 1])
                index += 2
                continue
        elif argument.startswith(option + "="):
            requested = True
            destination = argument.partition("=")[2]
            if destination:
                destinations.append(destination)
        index += 1
    return (destinations[-1] if destinations else None), requested


def _invalid_parse_namespace(path: str | None) -> argparse.Namespace:
    return argparse.Namespace(
        path=path,
        line=None,
        symbol=None,
        start=None,
        end=None,
        max_lines=None,
        max_chars=None,
        expected_sha256=None,
        arguments_valid=False,
    )


def _event_record(args: argparse.Namespace, result: dict[str, Any]) -> dict[str, Any]:
    error = result.get("error")
    return {
        "format": "icm-source-reader-event",
        "schema_version": 1,
        "event_id": uuid.uuid4().hex,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "transport_status": "unknown",
        "identity": {
            "path": result.get("path", args.path),
            "sha256": result.get("sha256"),
        },
        "request": {
            "path": args.path,
            "line": args.line,
            "symbol": args.symbol,
            "start": args.start,
            "end": args.end,
            "max_lines": args.max_lines,
            "max_chars": args.max_chars,
            "expected_sha256": args.expected_sha256,
            "arguments_valid": getattr(args, "arguments_valid", True),
        },
        "spans": {
            "selection_kind": result.get("selection_kind"),
            "unit": result.get("unit"),
            "returned": result.get("returned"),
            "remaining": result.get("remaining"),
            "continuation": result.get("continuation"),
        },
        "completeness": {
            "ok": result.get("ok", False),
            "complete": result.get("complete", False),
            "parser_status": result.get("parser_status"),
            "limitations": result.get("limitations", LIMITATIONS),
            "error": error,
        },
    }


def _write_event(directory: str, event: dict[str, Any]) -> Path:
    if not isinstance(directory, str) or not directory or "\x00" in directory:
        raise SourceReaderError("log_error", "log directory is invalid")
    event_directory = Path(directory)
    try:
        event_directory.mkdir(parents=True, exist_ok=True)
        directory_info = event_directory.lstat()
        if _is_link_or_reparse(directory_info) or not stat.S_ISDIR(directory_info.st_mode):
            raise SourceReaderError("log_error", "log target is not a safe directory")
        event_name = (
            f"source-read-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}-"
            f"{uuid.uuid4().hex}.json"
        )
        event_path = event_directory / event_name
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        descriptor = os.open(event_path, flags, 0o444)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
                json.dump(event, handle, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
        except Exception:
            try:
                event_path.unlink()
            except OSError:
                pass
            raise
        return event_path
    except SourceReaderError:
        raise
    except (OSError, ValueError) as exc:
        raise SourceReaderError("log_error", "event log could not be created safely") from exc


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    prescanned_log, log_requested = _prescan_option(raw_argv, "--log")
    prescanned_path, _ = _prescan_option(raw_argv, "--path")
    try:
        try:
            args = _parser().parse_args(raw_argv)
        except SourceReaderError as exc:
            result = _error_result(exc)
            if prescanned_log is not None:
                try:
                    _write_event(
                        prescanned_log,
                        _event_record(_invalid_parse_namespace(prescanned_path), result),
                    )
                except SourceReaderError as log_exc:
                    result = _error_result(log_exc)
            elif log_requested:
                result["logging_status"] = "not_written"
                result["logging_error"] = {
                    "category": "log_error",
                    "message": "explicit log directory could not be determined",
                }
            code = 2
        else:
            result = read_source(
                args.root,
                args.path,
                line=args.line,
                symbol=args.symbol,
                start=args.start,
                end=args.end,
                max_lines=args.max_lines,
                max_chars=args.max_chars,
                expected_sha256=args.expected_sha256,
            )
            if args.log is not None:
                try:
                    _write_event(args.log, _event_record(args, result))
                except SourceReaderError as exc:
                    result = _error_result(exc)
            code = 0 if result["ok"] else 2
    except SourceReaderError as exc:
        result = _error_result(exc)
        if prescanned_log is not None:
            try:
                _write_event(
                    prescanned_log,
                    _event_record(_invalid_parse_namespace(prescanned_path), result),
                )
            except SourceReaderError as log_exc:
                result = _error_result(log_exc)
        code = 2
    except (OSError, TypeError, ValueError, RecursionError):
        result = _error_result(
            SourceReaderError("internal_error", "command could not be completed safely")
        )
        code = 2

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="strict")
        except (AttributeError, OSError):
            pass
    json.dump(result, sys.stdout, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
