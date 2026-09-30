---
name: investment-firm-systems
description: Map and improve the operating architecture of a hedge fund, asset manager, or quantitative investment firm across front, middle, and back office. Use for trade lifecycle, ownership, service-provider boundaries, reconciliation, valuation dependencies, controls, incidents, and operational readiness. Not for legal conclusions, regulatory compliance sign-off, investment recommendations, or live operations.
---

# Investment Firm Systems

Turn a proposed investment workflow into an auditable operating model with owners, artifacts, reconciliations, exceptions, and recovery paths. Treat course material as structural guidance and verify current legal or regulatory requirements from authoritative sources when they matter.

## Establish the operating scope

Identify entity and strategy type, jurisdictions, asset classes, trading frequency, investors and reporting obligations, internal roles, external providers, systems of record, critical deadlines, and the specific decision or workflow being designed. Ask for professional legal, tax, audit, or compliance review when the answer depends on a binding obligation.

## Route narrowly

| Observable request | Read |
|---|---|
| Organization design, front/middle/back-office boundaries, service providers, trade lifecycle, books and records, valuation/NAV dependencies, or system-of-record mapping | [operating-model.md](references/operating-model.md) |
| Preventive/detective controls, reconciliations, approvals, access, incidents, changes, business continuity, vendor risk, or operational readiness | [controls-and-resilience.md](references/controls-and-resilience.md) |
| Verification, source/course status, current-authority refresh, evaluation cases, or maintaining this skill | [validation-and-sources.md](references/validation-and-sources.md) |

Load only the module that owns the requested artifact. Use both when a new workflow needs an operating map and a control design.

## Workflow

1. Draw actors, systems, data, cash, positions, orders, trades, valuations, and reports from initiation through final accounting.
2. Assign one owner and one system of record for every critical state; identify independent calculation or verification points.
3. Define reconciliations, tolerances, approvals, evidence, escalation, and exception aging.
4. Model failures of people, systems, data, counterparties, and vendors; specify fallback and recovery objectives.
5. Separate a course-derived control pattern from a current legal requirement. Browse regulators and governing agreements for the latter.
6. Return a prioritized gap register with severity, owner, evidence, dependency, and acceptance test.

## Invariants and boundaries

- Outsourcing an activity does not eliminate oversight, data, reconciliation, or continuity obligations.
- A policy without an owner, evidence artifact, exception path, and test is not an operating control.
- Risk analytics, accounting, and investor reporting may use different views; reconcile them rather than silently forcing equality.
- Never infer current compliance from a historical syllabus or a generic industry pattern.
- Do not expose credentials, investor information, or confidential counterparty terms.

Use `reliable-quant-data-systems` for detailed data/transaction architecture, `market-microstructure-execution` for execution policy, and `ingenius-quant-finance` for models and risk analytics. This skill does not provide legal, tax, audit, or investment advice and does not authorize operational or production changes.
