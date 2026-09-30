# Temporal data and lineage

## Loading boundary

Use for historical truth, reproducibility, schema identity, and research-to-production data contracts—not for statistical modeling itself.

## Temporal contract

For each record define event time, source-publish time, receipt time, effective interval, ingestion time, and revision/supersession link as applicable. Make the consumer's as-of rule explicit. Preserve original vendor payloads or immutable normalized facts when licensing and storage policy permit.

Represent security, venue, account, strategy, and corporate-action identities with stable internal identifiers plus dated mappings. Never join solely on a reused ticker. Record calendar, timezone, daylight-saving, session, and timestamp-resolution rules.

## Lineage record

A reproducible output names input snapshots, schema versions, transformation code, configuration, reference data, model version, environment, and run identifier. Validate row counts, uniqueness, ranges, referential integrity, temporal monotonicity, and reconciliation totals at boundaries.

For point-in-time research, test later corrections, delistings, additions/removals, adjusted/unadjusted prices, publication lags, and vendor restatements. A current database snapshot is not a historical information set.

