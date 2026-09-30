---
name: llm-task-strategist
description: Choose an appropriate LLM workflow—model capability, context, reasoning, search, computation, files, modalities, or agent tools—when the user asks how to approach an AI task or which mode or tool it needs. Do not activate for ordinary task execution when the required workflow is already clear.
---

# LLM Task Strategist

Translate the user's goal into the smallest adequate capability stack. Recommend capabilities before product names; verify current product support when a vendor-specific choice matters.

## Classify the task

Assess only dimensions that can change the route:

- **Freshness:** stable common knowledge, niche knowledge, or current/changing information.
- **Exactness:** approximate explanation versus exact arithmetic, transformation, or reproducible computation.
- **Reasoning:** direct response versus multi-step math, code, comparison, or planning.
- **Grounding:** model knowledge versus a supplied document, dataset, repository, or other source of truth.
- **Action:** answer generation versus browsing, code execution, file edits, or external operations.
- **Modality:** text, speech, image/OCR, audio, or video.
- **Risk:** consequence of a wrong result, sensitivity of inputs, and reversibility of actions.
- **Constraints:** privacy, latency, cost, availability, context size, and required audit trail.

Keep four layers distinct: model parameters provide fallible learned knowledge; context provides temporary working material; additional inference provides reasoning effort; tools provide external information, computation, or actions.

## Choose the workflow

Read [references/routing-matrix.md](references/routing-matrix.md) when the request has competing routes or combines several capabilities. Prefer the least complex stack that meets the actual need.

Do not recommend a reasoning model for a freshness problem, search for an arithmetic problem, or a larger context window when irrelevant context is the issue. Multiple model answers are useful comparisons, not independent verification.

Scale verification to risk:

- Low risk: plausibility check and a clearly labeled uncertainty.
- Medium risk: source inspection, deterministic recomputation, or a fixed evaluation example.
- High risk: primary sources, domain-expert review, reproducible checks, and an explicit statement of what remains unverified.

## Report

Give:

1. the recommended capability stack and why;
2. what information belongs in context;
3. which tool or modality is necessary and which is optional;
4. latency, cost, privacy, and failure tradeoffs;
5. the verification plan;
6. a simpler fallback when one exists.

If the user also asks for execution, use the smallest relevant workflow: grounded research for current or evidence-sensitive questions, interactive source study for a supplied work, AI-output auditing for an existing generated result, or reusable prompt design for repeated tasks. Tool choice never grants permission for external writes or irreversible actions.
