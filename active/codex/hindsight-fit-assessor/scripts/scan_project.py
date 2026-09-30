#!/usr/bin/env python3
"""Collect read-only repository signals for a Hindsight fit assessment.

This script deliberately does not decide whether to adopt Hindsight. It emits
paths and line numbers that an assessor must verify in project context.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "target",
    ".next",
    ".turbo",
    "coverage",
    "__pycache__",
    "graphify-out",
}

SKIP_FILES = {
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "uv.lock",
    "poetry.lock",
    "cargo.lock",
    "go.sum",
}

TEXT_SUFFIXES = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".rb",
    ".php",
    ".cs",
    ".scala",
    ".md",
    ".mdx",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
    ".ini",
    ".cfg",
    ".conf",
    ".txt",
    ".sql",
}

SPECIAL_TEXT_FILES = {
    "dockerfile",
    "makefile",
    "procfile",
    "gemfile",
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "go.mod",
    "cargo.toml",
    "pom.xml",
    "build.gradle",
}

MANIFEST_NAMES = {
    "pyproject.toml",
    "package.json",
    "requirements.txt",
    "go.mod",
    "cargo.toml",
    "pom.xml",
    "build.gradle",
    "docker-compose.yml",
    "docker-compose.yaml",
    "dockerfile",
}

SIGNAL_PATTERNS: dict[str, tuple[str, ...]] = {
    "llm_or_ai": (
        r"\bopenai\b",
        r"\banthropic\b",
        r"\bgoogle[-_ ]?genai\b",
        r"\blitellm\b",
        r"\blangchain\b",
        r"\bllamaindex\b",
        r"\bvercel[/_-]?ai\b",
        r"\bchat\.completions\b",
        r"\bgenerate(text|content)\b",
    ),
    "agent_or_tool_use": (
        r"\btool[_ -]?call",
        r"\bfunction[_ -]?call",
        r"\bmcp\b",
        r"\bmodel context protocol\b",
        r"\b(pydantic[_ -]?ai|crewai|autogen|langgraph|openai[_ -]?agents)\b",
        r"\bagent[_ -]?(loop|runner|executor|workflow)\b",
    ),
    "conversation_or_session": (
        r"\b(conversation|chat|message|thread)[_ -]?(history|store|repository|session)\b",
        r"\bsession[_ -]?(id|history|state)\b",
        r"\bchat[_ -]?messages\b",
    ),
    "durable_memory": (
        r"\blong[-_ ]?term[_ -]?memory\b",
        r"\b(memory|memories)[_ -]?(store|bank|repository|service)\b",
        r"\bremember[_ -]?(user|project|preference|context)\b",
        r"\buser[_ -]?(preference|profile|memory)\b",
        r"\bproject[_ -]?memory\b",
    ),
    "retrieval_or_vector_search": (
        r"\b(pgvector|pinecone|weaviate|qdrant|chroma|milvus|faiss)\b",
        r"\b(vector|semantic)[_ -]?(search|store|index|retrieval)\b",
        r"\bembedding(s)?\b",
        r"\bbm25\b",
        r"\brerank(er|ing)?\b",
        r"\bretrieval augmented generation\b",
        r"\brag\b",
    ),
    "persistence": (
        r"\b(postgres(ql)?|sqlite|mysql|mariadb|mongodb|dynamodb|redis)\b",
        r"\b(sqlalchemy|prisma|drizzle|typeorm|sequelize|django\.db)\b",
        r"\b(database|db)[_ -]?(url|pool|session|connection)\b",
    ),
    "background_work": (
        r"\b(celery|bullmq|sidekiq|rq|temporal\.io|inngest|trigger\.dev)\b",
        r"\b(background|async)[_ -]?(job|task|worker|queue)\b",
        r"\b(job|task)[_ -]?(queue|scheduler|poller)\b",
        r"\bcron(job)?\b",
    ),
    "document_ingestion": (
        r"\b(pdf|docx|pptx|markdown)[_ -]?(loader|parser|ingest|upload)\b",
        r"\b(document|file)[_ -]?(upload|ingest|chunk|parser)\b",
        r"\bchunk[_ -]?(text|document|size|overlap)\b",
    ),
    "identity_or_multitenancy": (
        r"\b(user|tenant|account|organization|workspace|project)[_ -]?id\b",
        r"\bmulti[-_ ]?tenant\b",
        r"\b(auth0|clerk|nextauth|supabase[_ -]?auth)\b",
    ),
    "realtime_or_latency_sensitive": (
        r"\b(websocket|webrtc|voice[_ -]?agent|speech[_ -]?to[_ -]?speech)\b",
        r"\breal[-_ ]?time\b",
        r"\bstreaming[_ -]?(response|audio|tokens)\b",
        r"\blatency[_ -]?(budget|slo|p95|p99)\b",
    ),
    "privacy_or_governance": (
        r"\b(pii|personally identifiable|data residency|retention policy)\b",
        r"\b(redact|redaction|anonymi[sz]e|right to delete)\b",
        r"\b(audit[_ -]?log|tenant[_ -]?isolation|row level security|rls)\b",
    ),
    "hindsight_existing": (
        r"\bhindsight[-_ ]?(api|client|all|litellm|mcp)\b",
        r"\bvectorize[-_ ]?io[/_-]?hindsight\b",
        r"\bHINDSIGHT_API_[A-Z0-9_]+\b",
    ),
}

COMPILED = {
    name: tuple(re.compile(pattern, re.IGNORECASE) for pattern in patterns)
    for name, patterns in SIGNAL_PATTERNS.items()
}


def is_text_candidate(path: Path) -> bool:
    name = path.name.lower()
    return path.suffix.lower() in TEXT_SUFFIXES or name in SPECIAL_TEXT_FILES or name.startswith("requirements")


def iter_files(root: Path, max_files: int):
    yielded = 0
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith(".cache"))
        for filename in sorted(files):
            if yielded >= max_files:
                return
            path = Path(current) / filename
            if filename.lower() in SKIP_FILES or not is_text_candidate(path):
                continue
            yielded += 1
            yield path


def language_label(path: Path) -> str:
    name = path.name.lower()
    if name in SPECIAL_TEXT_FILES:
        return name
    return path.suffix.lower().lstrip(".") or "other"


def scan(root: Path, max_files: int, max_bytes: int, evidence_limit: int) -> dict:
    counts: Counter[str] = Counter()
    manifests: list[str] = []
    hits = {name: 0 for name in COMPILED}
    evidence: dict[str, list[str]] = {name: [] for name in COMPILED}
    files_scanned = 0
    truncated = False

    for path in iter_files(root, max_files + 1):
        if files_scanned >= max_files:
            truncated = True
            break
        files_scanned += 1
        rel = path.relative_to(root).as_posix()
        counts[language_label(path)] += 1
        if path.name.lower() in MANIFEST_NAMES:
            manifests.append(rel)
        try:
            if path.stat().st_size > max_bytes:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            for signal, patterns in COMPILED.items():
                if any(pattern.search(line) for pattern in patterns):
                    hits[signal] += 1
                    if len(evidence[signal]) < evidence_limit:
                        evidence[signal].append(f"{rel}:{line_no}")

    signals = {
        name: {"hit_count": hits[name], "evidence": evidence[name]}
        for name in COMPILED
    }
    return {
        "project_root": str(root),
        "files_scanned": files_scanned,
        "scan_truncated": truncated,
        "language_file_counts": dict(counts.most_common()),
        "manifests": sorted(set(manifests)),
        "signals": signals,
        "interpretation": (
            "Pattern hits are discovery hints only. Verify each important signal in project context "
            "before applying the Hindsight decision rubric."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--max-files", type=int, default=15_000)
    parser.add_argument("--max-bytes", type=int, default=512_000)
    parser.add_argument("--evidence-limit", type=int, default=8)
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"project root is not a directory: {root}")
    if args.max_files <= 0 or args.max_bytes <= 0 or args.evidence_limit <= 0:
        parser.error("limits must be positive")

    print(json.dumps(scan(root, args.max_files, args.max_bytes, args.evidence_limit), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
