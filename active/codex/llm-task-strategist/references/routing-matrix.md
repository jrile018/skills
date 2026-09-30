# LLM task routing matrix

Use this matrix only when more than one route is plausible.

| Observable need | Primary capability | Add when needed | Common mistake | Verification |
|---|---|---|---|---|
| Stable, common, low-stakes explanation | Direct generation | Supplied context for user-specific details | Browsing without need | Basic plausibility check |
| Current, obscure, disputed, or quote-sensitive facts | Search/retrieval | Deeper research for many claims or sources | Trusting trained knowledge or uncited synthesis | Open supporting sources; prefer primary evidence |
| Difficult math, code diagnosis, or multi-step planning | Higher reasoning effort | Deterministic tools for exact results | Assuming longer reasoning fixes missing facts | Test, recompute, or check invariants |
| Arithmetic, statistics, plots, or data transformation | Code/calculator runtime | Reasoning to select the method | Letting the model calculate from token patterns | Inspect inputs, code, assumptions, and outputs |
| Questions about a particular paper, book, transcript, or policy | Source in context or retrieval | OCR/vision for non-text content | Asking from vague model recollection | Cite page, section, line, figure, or excerpt |
| Large repository or multi-file change | Code-aware agent with repository context | Search, tests, and version control | Copying isolated snippets without project context | Review diff, commands, dependencies, and tests |
| Repeated fixed workflow | Saved prompt or specialized assistant | Durable memory only for stable user facts | Saving transient or sensitive content as memory | Test positive, negative, and ambiguous cases |
| Speech is faster than typing | Speech-to-text | Native audio when tone/timing matters | Assuming transcription preserves names or numbers | Display and correct transcription |
| Screenshot, label, diagram, or visual question | Vision/OCR | Source study or calculation after extraction | Reasoning over an unverified transcription | Confirm extracted text and values first |
| High-stakes medical, legal, financial, or safety decision | Source-grounded research plus expert review | Deterministic checks and audit trail | Treating a polished answer as professional advice | Primary evidence and qualified human judgment |

## Combining routes

Order capabilities by dependency, not novelty. For example:

1. extract a table from an image;
2. confirm the transcription;
3. compute results with code;
4. reason about the verified output;
5. audit any high-impact conclusion.

For research with supplied documents, establish the supplied source first, then search only to fill explicit gaps or verify external claims. For agent actions, plan and inspect before allowing mutation.
