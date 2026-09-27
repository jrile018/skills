# Optional source reader

Use `scripts/source_reader.py` when existing tools clip needed source or a version-bound continuation would help. It is a standard-library utility, not a required workflow or an established LLM-performance improvement. For exact literal discovery, ordinary search is often sufficient.

```text
python <skill>/scripts/source_reader.py --root <repo> --path src/service.py --symbol Service.handle
python <skill>/scripts/source_reader.py --root <repo> --path src/service.py --line 280
python <skill>/scripts/source_reader.py --root <repo> --path src/client.cpp --start 120 --end 350 --max-lines 160
```

Select exactly one of line anchor, qualified Python definition, or explicit range. Ambiguous qualified definitions return candidates; choose a line anchor. Decorators are included in Python syntax extents. Non-Python or parse-failed line selections are explicitly bounded text fallbacks, not semantic symbols.

Read `returned`, `remaining`, `complete`, and `limitations`, not just `text`. `complete` refers only to the selected syntax/range. If partial, use the returned continuation's `start`, `end` and `expected_sha256` as `--start`, `--end`, `--expected-sha256`. A changed file rejects the continuation; reacquire the needed evidence instead of stitching revisions. An overlong first line returns `ok: true` with no lines, `complete: false` and `budget_error`; it is not a completed read. Increase `max_chars` within the applicable budget or report the unread frontier—repeating the unchanged continuation and budget cannot make progress. Budgets limit numbered source text; metadata and tool transport have their own overhead.

The reader rejects paths outside the declared root, links/reparse source components, unsupported decoding, binary content, and oversized files. SHA-256 identifies the same raw bytes decoded for the result. Concurrent filesystem checks are best effort, not an atomic security boundary. Python AST spans do not resolve dispatch, decorators' behavior, globals, callers, or business policy.

Optional `--log <event-directory>` writes a distinct passive event per invocation. It records generated ranges and identities, not code payloads or a supported-claim verdict. Transport status remains unknown: local success cannot prove the host delivered all output. Use a separate directory per run; inspect explicit logging errors. Omit logging for a small answer when durable artifacts are neither needed nor authorized.
