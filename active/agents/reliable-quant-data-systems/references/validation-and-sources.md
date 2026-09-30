# Validation and sources

## Loading boundary

Use for architecture acceptance, course study, provenance, or skill maintenance.

## Advanced elective evidence

- [MIT 6.5840 Distributed Systems, Spring 2026](https://pdos.csail.mit.edu/6.824/): graduate abstractions and implementation techniques for fault tolerance, replication, and consistency, with programming labs and case studies.
- [CMU 15-445/645 Database Systems, Spring 2025](https://15445.courses.cs.cmu.edu/spring2025/syllabus.html): upper-level, project-heavy study of storage, indexes, concurrency control, recovery, and OLTP/OLAP tradeoffs.
- [CMU Database Group course catalog](https://db.cs.cmu.edu/courses/): routes advanced learners to 15-721 and current special-topics offerings when a deeper DBMS implementation lens is required.
- [Stanford CS244B Distributed Systems](https://www.scs.stanford.edu/17au-cs244b/): transactions, consistency, storage, failure, and distributed state; the linked public materials are historical and must be labeled accordingly.

## Acceptance checks

- point-in-time query prevents a deliberately introduced look-ahead record;
- duplicate and reordered events preserve business invariants;
- concurrent transactions exercise the named isolation anomaly;
- a crash/restart test preserves or reconciles every visible effect;
- backup restoration meets the recorded RPO/RTO on representative data;
- lineage reproduces a prior consumer output from pinned inputs and code.

