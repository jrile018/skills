---
name: stanford-cs106l-cpp-memory
description: Diagnose, repair, and teach modern C++ ownership and object-lifetime correctness using Stanford CS106L. Use for RAII, smart pointers, special member functions, move semantics, leaks, dangling or use-after-free errors, double deletion, storage duration, or explicit CS106L study; not for C memory management, atomic memory ordering, virtual-memory systems, or allocation performance without a lifetime question.
---

# Stanford CS106L C++ Memory Management

Make ownership and lifetime explicit before changing pointer syntax. The goal is not to replace every raw pointer with a smart pointer; it is to establish who owns each resource, when each object is alive, how ownership moves, and how the result is verified.

## Establish the memory contract

For the affected resource or object graph, identify:

- the resource being managed and its acquisition/release pair;
- each owner, borrower, observer, alias, and nullable edge;
- storage duration separately from object lifetime;
- copy, move, destruction, exception, and early-return paths;
- API, ABI, real-time, or interoperability constraints; and
- the strongest available reproducer, test, or sanitizer trace.

If code is available, inspect the declarations, construction sites, transfers, and destruction sites together. Do not diagnose lifetime from one dereference in isolation.

## Diagnose and repair

1. Reproduce the failure or state the unverified symptom. Pin the compiler, language mode, build type, platform, and relevant sanitizer configuration.
2. Draw a compact ownership graph and a lifetime timeline. Distinguish “storage exists,” “an object is alive in that storage,” “a pointer is reachable,” and “a pointer owns the object.”
3. Classify the defect: leak, dangling borrow, use after scope/free/destruction, double or mismatched deletion, invalidated iterator/reference, uninitialized read, shared-ownership cycle, alignment/storage reuse error, or broken copy/move operation.
4. Prefer value semantics and the Rule of Zero. Otherwise use an RAII resource handle whose type expresses exclusive, shared, weak, or borrowed access. Do not introduce `shared_ptr` merely to make deletion disappear.
5. Make special-member behavior explicit only when defaults are wrong. Check copy independence, move transfer, moved-from validity, self-assignment where relevant, destruction, and exception paths.
6. Verify the smallest repair with focused tests plus appropriate compiler diagnostics or sanitizers. A clean sanitizer run is evidence for the exercised paths, not proof that all lifetime behavior is correct.

Read [references/course-guide.md](references/course-guide.md) when choosing an ownership model, interpreting a memory diagnostic, teaching the CS106L sequence, checking course provenance, or running the behavioral cases.

## Invariants

- A raw pointer or reference does not acquire ownership unless an explicit legacy contract says it does.
- `unique_ptr` expresses exclusive ownership; moving transfers that ownership and copying is unavailable.
- `shared_ptr` is for genuinely shared lifetime, not general pointer safety; use `weak_ptr` or another non-owning edge to break ownership cycles.
- Resource release must occur on ordinary return, exceptions, and partial construction. Prefer RAII over paired cleanup calls.
- A moved-from standard-library object must remain valid, but its otherwise unspecified state must not be invented.
- Deallocation must match allocation, and polymorphic destruction must follow the base-class contract.
- Container growth, erase, move, and destruction can invalidate pointers, references, and iterators even when no explicit `delete` appears.
- Placement construction, unions, custom allocators, and reused storage require object-lifetime and alignment reasoning, not only byte-count reasoning.

## Performance and systems handoff

This skill owns lifetime correctness. Use `mit-6172-performance-engineering` when the requested result is a measured non-trading allocation, locality, cache, or throughput improvement. Use `low-latency-quant-systems` for a measured trading-system path. When both apply, establish and test the ownership/lifetime contract first, then let the performance owner optimize without weakening it.

## Boundaries

Do not activate for ordinary C++ syntax, generic refactoring, C `malloc`/`free` work, garbage-collected-language memory, operating-system paging or virtual memory, or C++ atomic ordering without an ownership/lifetime problem. Sanitizer runtimes and exact flags are toolchain- and platform-specific; verify current compiler documentation before prescribing them. This skill can review or change code when requested, but it does not authorize deployment or production mutation.
