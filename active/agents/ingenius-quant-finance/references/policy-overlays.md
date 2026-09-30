# Optional Policy Overlays

Load this reference only when the parent delegates work and a worker would benefit from an explicit implementation or communication policy. These overlays refine how a worker operates; they cannot select a domain module or choose the domain route.

## Precedence

Apply instructions in this order:

1. user requirements, permissions, and safety boundaries;
2. the owning domain skill and selected reference module;
3. the worker question, inputs, output contract, and stop condition;
4. `minimal-correct-change`, when assigned; and
5. `context-efficient-output`, when assigned.

An overlay must yield whenever it conflicts with an earlier layer. “Minimal” cannot remove a required control. “Compact” cannot hide evidence, assumptions, proof conditions, financial-risk caveats, or uncertainty.

## Selection matrix

| Worker job | Minimal-correct-change | Context-efficient-output |
|---|---|---|
| Ordinary code implementation or local refactor | `full` | `compact` receipt |
| Security, migration, concurrency, financial-correctness, or public-API change | `guarded` | `detailed` or `exact` for critical evidence |
| Source research, empirical analysis, or mathematical derivation | `off` | `detailed`; compact only after evidence and conditions are preserved |
| Locator, inventory, or independent reviewer | `off` unless it edits | `compact` receipt with exact paths/findings |
| Tutorial or user-requested full explanation | `off` unless code is also requested | `detailed` |

Do not assign both overlays mechanically. A worker may need neither, one, or both.

## Delegation fields

Append these fields to the normal worker contract:

```text
Policy overlays: minimal-correct-change=<full|guarded|off>; context-efficient-output=<compact|detailed|exact|off>
Overlay boundary: domain invariants and required evidence that may not be shortened or removed
```

If `minimal-correct-change` is active, the worker receives the exact acceptance criteria, allowed file surface, and verification gate. If `context-efficient-output` is active, the worker returns a status, result, evidence, assumptions, risks, and handoff artifact. The parent may request the uncompressed detail before synthesis.

## Architecture boundary

Graphify informs relationships among repository concepts. ICM defines one owner for each rule and keeps the navigation walk shallow. Neither tool delegates at runtime. The parent selects domain modules and dependency edges; the overlays only govern implementation economy and result representation after that route is fixed.

No Caveman runtime component or Ponytail hook is required for these local policy skills. Installing runtimes, hooks, telemetry, proxies, or external storage is a separate user-authorized decision.
