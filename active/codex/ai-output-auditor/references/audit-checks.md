# AI output audit checks

Apply only checks relevant to the artifact and its risk.

## Claims and research

- Does every consequential factual claim have an appropriate source?
- Does the cited source directly support the wording, scope, date, and population?
- Are primary evidence and secondary commentary distinguished?
- Were major counterexamples, alternatives, or contradictory findings omitted?
- Are facts, inference, prediction, and opinion visibly different?
- Could several citations trace back to the same unverified upstream claim?

## Calculations, data, and charts

- Are inputs, units, denominators, date ranges, and definitions correct?
- Were missing values dropped, imputed, or replaced without disclosure?
- Does the selected method match the data and question?
- Can the result be reproduced independently?
- Do labels, written conclusions, plotted values, and raw variables agree?
- Are extrapolations presented with assumptions and uncertainty?

## Code and tool actions

- Does the change match the requested scope and preserve unrelated work?
- Are commands and external mutations authorized and reversible?
- Are packages, downloads, URLs, and generated assets from known sources with acceptable licenses?
- Could untrusted content influence tool calls or reveal secrets?
- Are authentication, tenant boundaries, input validation, and error paths preserved?
- Do targeted tests cover the claimed behavior, and was their output actually observed?
- Is there a rollback or recovery path for material changes?

## OCR and multimodal input

- Were names, symbols, decimal points, signs, dates, units, and table alignment confirmed?
- Is the visible crop complete enough to support the conclusion?
- Could tone, timing, or nonverbal context have been lost in transcription?
- Is the model inferring unseen content beyond the image, audio, or video sample?

## Privacy and high-stakes use

- Was sensitive information necessary, minimized, and handled in an authorized environment?
- Could durable memory or logs retain material the user expects to be temporary?
- Does the result require qualified medical, legal, financial, security, or safety review?
- Is the recommendation reversible, and are failure consequences explicit?

## Severity guide

- **Critical:** likely harmful action, security/privacy breach, or decision-changing falsehood.
- **High:** material unsupported conclusion, incorrect computation, or unsafe dependency/action.
- **Medium:** important caveat, scope mismatch, or incomplete verification that could mislead.
- **Low:** localized clarity or traceability issue with little effect on the decision.
