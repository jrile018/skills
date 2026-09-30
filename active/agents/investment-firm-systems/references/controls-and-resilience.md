# Controls and resilience

## Loading boundary

Use for control design, reconciliation, incidents, changes, access, vendor risk, and continuity. Current legal applicability requires authoritative verification and qualified review.

## Control record

For each material risk specify preventive or detective control, owner, frequency/trigger, input, procedure, evidence, tolerance, exception owner, escalation deadline, downstream dependency, and test. Prefer independent reconciliations for cash, positions, trades, prices, fees, collateral, and NAV inputs where material.

Separate:

- model approval from code deployment;
- maker from checker for sensitive changes and cash movement;
- risk limits from monitoring dashboards;
- incident containment from root-cause remediation;
- backup existence from tested recovery;
- provider attestation from the firm's own control responsibility.

For readiness, simulate unavailable broker/vendor/admin, corrupt data, delayed valuation, failed settlement, stale risk, credential compromise, key-person loss, and regional/system outage. Record RTO/RPO, manual capacity, decision authority, communications, and reconciliation after recovery.

