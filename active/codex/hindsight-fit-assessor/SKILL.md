---
name: hindsight-fit-assessor
description: Evaluate whether an existing or planned AI or agent project should adopt Hindsight for durable memory. Use when the user asks whether Hindsight fits a repository, product, agent workflow, or architecture, or wants an adoption, pilot, or alternatives recommendation. Do not use for unrelated code reviews or generic database selection that does not involve agent memory.
---

# Hindsight Fit Assessor

Decide whether Hindsight solves a real project need at acceptable cost. Produce an evidence-backed recommendation, not product advocacy.

## Assess the project

For a local project, inspect its own instructions and architecture before scoring. Run the read-only signal scanner when useful:

```bash
python <skill-directory>/scripts/scan_project.py <project-root>
```

Treat its output as leads, not conclusions. Verify important signals in source, manifests, and documentation. Identify:

- whether this is actually an LLM or agent product;
- what must persist across sessions, users, projects, or agent runs;
- current conversation, profile, retrieval, vector-search, and background-job mechanisms;
- context-window pressure and whether selective recall would help;
- the need for temporal memory, provenance, consolidated beliefs, or standing summaries;
- integration surface: REST, MCP, SDK language, or agent framework;
- latency, cost, privacy, deployment, and operational constraints;
- whether an existing simpler mechanism already satisfies the need.

For a planned project without a repository, score only stated facts. Mark all inferred facts and lower confidence rather than inventing implementation evidence.

If current Hindsight behavior, compatibility, licensing, or pricing affects the decision, inspect the pinned local version first. Otherwise verify unstable claims against the official Hindsight repository or documentation.

## Make the decision

Read [references/decision-rubric.md](references/decision-rubric.md) before assigning a verdict. Apply its gates, 20-point score, penalties, and decision bands.

Always compare Hindsight with the cheapest adequate alternative:

- ordinary conversation history or prompt context;
- a relational preferences/profile table;
- conventional vector RAG;
- the project's existing memory or search layer.

Do not recommend Hindsight merely because the project uses an LLM. It should earn its operational complexity through durable continuity, selective retrieval, consolidation, provenance, or evolving knowledge.

## Report

Lead with one verdict: **Adopt**, **Pilot**, **Skip for now**, or **Do not adopt**. Include:

1. confidence and the strongest project-specific reason;
2. an evidence table with criterion, repository evidence, and score;
3. the proposed architectural insertion point;
4. material costs and failure modes;
5. the simpler alternative and why it is or is not enough;
6. unknowns that could change the verdict;
7. for Adopt or Pilot, a small reversible pilot with success metrics.

Keep facts, inferences, and unknowns visibly distinct. Cite concrete local files and lines when available. Do not implement, install, deploy, or transmit project data unless the user separately asks.
