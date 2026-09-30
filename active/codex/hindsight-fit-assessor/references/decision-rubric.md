# Hindsight adoption decision rubric

Use this rubric after inspecting the project. Hindsight is an external, persistent memory subsystem: retain turns inputs into structured memories, recall performs selective hybrid retrieval, reflect reasons over stored knowledge, and background work can consolidate facts into observations and refresh mental models or knowledge pages. It does not update the base model's weights.

## Gates

At least one primary need must be present:

- cross-session user or agent continuity;
- a long-running agent that should learn from prior work;
- durable project, customer, or organizational knowledge that changes over time;
- accumulated events that must become higher-level observations or standing summaries.

If none is present, the verdict cannot exceed **Skip for now**.

Use **Do not adopt** when any unresolved blocker applies:

- the project has no LLM or agent behavior;
- policy prohibits storing or processing the relevant memory content;
- neither self-hosted nor managed deployment can satisfy data residency or security requirements;
- the team cannot operate or purchase the necessary database/model services;
- a hard real-time path cannot tolerate external retrieval and no asynchronous design is possible.

## Positive score: 0–20

Score only supported evidence. Use the lower value when evidence is ambiguous.

### 1. Durable continuity: 0–4

- 0: one-shot or stateless requests.
- 1: conversation history within one session.
- 2: cross-session preferences or history would help.
- 3: continuity is a named product requirement.
- 4: long-lived agents materially fail without accumulated memory.

### 2. Memory transformation: 0–4

- 0: exact records or raw chat history are enough.
- 1: simple summarization or preferences are enough.
- 2: facts/entities/dates must be extracted from unstructured input.
- 3: beliefs must be consolidated, revised, or grounded in evidence.
- 4: evolving observations plus standing mental models/knowledge pages are central.

### 3. Retrieval and context pressure: 0–3

- 0: all relevant state fits comfortably in the prompt.
- 1: occasional retrieval from a small corpus.
- 2: growing history makes selective retrieval important.
- 3: semantic, keyword, temporal, or graph signals must be combined under strict token budgets.

### 4. Provenance and reasoning: 0–3

- 0: generated answers need no durable evidence trail.
- 1: source documents should be retrievable.
- 2: derived claims should link to raw facts or chunks.
- 3: the agent must reason over summaries while checking freshness and source evidence.

### 5. Integration fit: 0–2

- 0: no practical REST, MCP, SDK, or framework insertion point.
- 1: integration is possible but requires custom bridging.
- 2: the project already uses a compatible API, MCP, supported client language, or agent framework.

### 6. Operational readiness: 0–2

- 0: the team requires a dependency-free component and cannot use managed infrastructure.
- 1: a pilot can support a database plus model/embedding calls.
- 2: production already operates equivalent databases, queues/workers, observability, and model providers.

### 7. Governance value: 0–2

- 0: persistence creates more risk than value.
- 1: isolation, self-hosting, deletion, or auditability would help.
- 2: per-user/project isolation, provenance, retention controls, or self-hosting are explicit requirements.

## Penalties

Subtract each applicable penalty, then clamp the score to 0–20:

- −4: the existing memory/search layer already meets the stated requirements.
- −4: required LLM extraction, embeddings, or persistent storage are unacceptable.
- −3: the critical path has incompatible latency or availability requirements.
- −3: deterministic exact records are required and derived memory would add risk.
- −2: the need is only a small editable preference/profile list.
- −2: likely memory volume or usage does not justify another service.
- −2: data sensitivity makes durable unstructured memory unusually risky, even if not an absolute blocker.

Do not double-penalize the same underlying constraint.

## Decision bands

- **16–20 — Adopt:** strong fit; propose a staged integration.
- **11–15 — Pilot:** plausible value, but validate quality, latency, cost, and operations first.
- **6–10 — Skip for now:** a simpler mechanism is currently adequate; name the trigger for reconsideration.
- **0–5 — Do not adopt:** architectural mismatch or unresolved blocker.

A gate or blocker overrides the numeric band. A high score with weak evidence should become **Pilot**, not Adopt.

## Pilot shape

Prefer one reversible workflow and one isolated bank boundary. Examples include one support agent, one project-memory bank, or one cohort of opted-in users. Do not migrate the system of record.

Measure:

- retrieval precision and missed-memory rate;
- answer quality on a fixed before/after evaluation set;
- retain, recall, and reflect latency separately;
- model, embedding, reranking, and storage cost;
- incorrect durable memories and correction rate;
- source/provenance usefulness;
- operator effort and failure recovery;
- privacy, deletion, and tenant-isolation behavior.

Define an exit criterion before the pilot. Recommend adoption only when the memory quality gain exceeds the additional cost and operational burden.
