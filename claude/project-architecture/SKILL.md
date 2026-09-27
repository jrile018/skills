---
name: project-architecture
description: Maintain clean architecture in complex projects. Use when creating new modules, refactoring, planning features, or working on large codebases.
---

Before writing code in a large project:

1. Read the existing project structure first (Glob to map it)
2. Follow existing patterns — never introduce new conventions without discussion
3. Keep modules under 300 lines — if longer, split by responsibility
4. Every new module needs: single responsibility, typed interfaces, error handling
5. Write the interface/types FIRST, implementation second
6. If touching >3 files, create a brief plan before starting
7. After implementation, verify nothing is broken by running existing tests

For embedded/systems work (C, assembly):
- Document memory layout and register maps in comments
- Include hardware assumptions (clock speed, bus width, endianness) at top of modules
- Test against actual constraints (stack size, timing budgets)
- Be explicit about volatile access and interrupt safety

For Python projects:
- Use __init__.py to define clean public APIs
- Type hints everywhere
- Docstrings on public functions only

For large features:
- Break into vertical slices, not horizontal layers
- Each slice should be independently testable and mergeable
- Prefer many small PRs over one massive one
