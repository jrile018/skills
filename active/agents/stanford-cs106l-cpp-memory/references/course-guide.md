# CS106L memory-management guide

Read this reference for ownership-model selection, diagnostic routing, explicit Stanford CS106L study, provenance, and behavioral evaluation.

## Course-derived spine

The official Autumn 2025-26 CS106L schedule builds the relevant material in this order: pointers and iterators, classes, const correctness, special member functions, move semantics, type safety, then RAII and smart pointers. The public final assignment asks students to implement a simplified C++20 `unique_ptr`, delete copy operations, implement move transfer, and use RAII in a linked structure.

Use the course as a learning progression, not as proof that its teaching implementation is a production-ready smart pointer or allocator.

## Diagnostic routing

| Evidence or request | Primary reasoning | Verification focus |
|---|---|---|
| Leak or cleanup skipped on exception | Missing owner or non-RAII resource pair | Destructor/cleanup paths, exceptions, leak detector where supported |
| Dangling pointer or use after free/scope | Borrow outlives owner or invalidation event | Ownership graph, lifetime timeline, AddressSanitizer |
| Double free or shallow-copy corruption | More than one apparent exclusive owner | Copy operations, Rule of Zero/Five, destruction trace |
| Broken move constructor or assignment | Ownership transfer leaves two owners or loses the resource | Source/destination postconditions, destructor counts, self-move policy |
| `shared_ptr` leak | Strong-reference cycle or unintended retained ownership | Strong/weak edge graph and release test |
| Iterator/reference becomes invalid | Container operation changed storage or element lifetime | Container contract and focused invalidation test |
| Uninitialized read | Bytes exist but a value was never initialized | Initialization path and MemorySanitizer where fully supported |
| Alignment, union, placement construction, or arena bug | Storage and object lifetime were conflated | Alignment, construction/destruction, reuse, and standard-version rules |
| Custom allocator or `std::pmr` proposal | Correct lifetime may coexist with a performance hypothesis | Prove ownership first; then measure with the performance owner |

## Ownership-model decision

Prefer the first adequate model:

1. **Value member or return-by-value:** no independent heap lifetime is required.
2. **Standard container or RAII handle:** the member already manages its resource; use the Rule of Zero.
3. **`unique_ptr`:** exactly one owner must control a dynamic lifetime or polymorphic object.
4. **`shared_ptr` plus `weak_ptr`:** multiple parties truly co-own lifetime and the strong-edge graph is acyclic.
5. **Borrowed `T&`, `T*`, iterator, view, or span-like type:** the API does not participate in ownership and the lifetime precondition is explicit.
6. **Custom owner/allocator:** interoperability, layout, arena, or latency constraints justify it and its contract can be tested.

Do not select by habit. A `shared_ptr` parameter should communicate participation in lifetime management; an ordinary user of an already-live object normally takes a reference or non-owning pointer.

## Special-member review

For a resource-owning type, answer:

- Can all resource-owning members manage themselves? If yes, use the Rule of Zero.
- If copying is allowed, is it deep, shared, reference-like, or otherwise specified?
- If copying is forbidden, are both copy operations deleted?
- Does moving transfer every owned resource exactly once and leave destruction safe?
- Are defaulted or deleted operations visible enough for the API contract?
- Does a base used polymorphically have a safe destruction policy?
- Are assignment, partial construction, and exceptions leak-free?

Avoid teaching `std::move` as a move operation by itself. It permits move selection by casting the expression; the selected constructor or assignment operation performs the transfer.

## Tool-assisted verification

Use the tool that matches the suspected failure and verify availability against the installed compiler:

- AddressSanitizer: out-of-bounds, use-after-free/scope/return, invalid or double free, and supported leak detection.
- MemorySanitizer: uninitialized reads, but it generally requires comprehensive instrumentation of dependent code.
- UndefinedBehaviorSanitizer: selected undefined behaviors such as misalignment, null dereference, invalid object-size uses, and some invalid downcasts.
- LeakSanitizer or platform tools: leak-focused evidence where supported.
- Compiler warnings and static analysis: ownership smells, deleted operations, suspicious copies, and lifetime annotations where available.

Run focused semantic tests as well. Sanitizers observe executed paths and have platform, configuration, and instrumentation limits.

## Tutoring path

1. Diagnose the learner's model of pointer, object, storage, scope, and ownership.
2. Use a small value-semantic class before introducing manual dynamic allocation.
3. Contrast shallow copy, deep copy, deleted copy, and shared ownership.
4. Trace constructor, move, and destructor events on paper or with logging.
5. Refactor the exercise to Rule-of-Zero production style after the learner understands the mechanics.
6. Finish with a held-out bug or API-design problem rather than another near-copy of the course assignment.

## Source and date boundaries

- [Stanford CS106L Autumn 2025-26 schedule](https://web.stanford.edu/class/archive/cs/cs106l/cs106l.1262/) — official course sequence and materials.
- [CS106L Assignment 7: Unique Pointer](https://github.com/cs106l/cs106l-assignments/blob/main/assignment7/README.md) — public C++20 RAII, ownership-transfer, and smart-pointer exercise; repository `main` can change.
- [CS106L special member functions lecture](https://web.stanford.edu/class/archive/cs/cs106l/cs106l.1262/lectures/2025Fall-13-SpecialMemberFunctions.pdf) — copy/move/destruction and Rule-of-Zero teaching material.
- [MIT 6.096 memory-management lecture](https://ocw.mit.edu/courses/6-096-introduction-to-c-january-iap-2011/resources/lecture-8-notes-memory-management/) — historical manual-memory foundation, not current modern-C++ guidance.
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — living design guidance, not the normative language standard.
- [C++ draft: object lifetime](https://eel.is/c++draft/basic.life) and [storage duration](https://eel.is/c++draft/basic.stc.general) — language-semantics reference; verify the target standard and compiler.
- [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html), [MemorySanitizer](https://clang.llvm.org/docs/MemorySanitizer.html), and [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) — current tool behavior and limitations.

## Behavioral evaluation

| Request | Expected behavior |
|---|---|
| “This moved object double-frees; repair the class.” | Activate; trace owners and special members, then test transfer and destruction |
| “Should this API accept `shared_ptr`, `unique_ptr`, or `Widget&`?” | Activate; choose based on lifetime participation rather than convenience |
| “Teach me the CS106L RAII and move-semantics sequence.” | Activate; use the prerequisite-aware tutoring path |
| “ASan reports heap-use-after-free after vector growth.” | Activate; trace container invalidation and exercised lifetime |
| “Reduce allocator overhead in this JSON parser.” | Route to MIT 6.172 unless an ownership/lifetime change is also requested |
| “Reduce p99 allocation stalls in the order gateway.” | Route to low-latency quant systems; add this skill only for a lifetime contract |
| “Explain `memory_order_acquire`.” | Do not activate; atomic ordering is a concurrency-memory-model problem |
| “Fix this C `malloc`/`free` function.” | Do not activate; the course and ownership model here are C++ specific |
