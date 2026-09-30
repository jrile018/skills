# Formulation and solver

## Loading boundary

Use when translating a decision into an optimization problem or verifying its solver. Do not load for a purely statistical fit with no optimization decision.

## Formulation record

Write:

- variables, dimensions, units, and domains;
- objective terms and their business meaning;
- equality and inequality constraints;
- deterministic parameters and estimated inputs;
- convexity status and constraint qualification assumptions;
- scale, sparsity, update frequency, and acceptable accuracy.

Normalize only with a reversible mapping. Distinguish an infeasible requirement, an unbounded objective, numerical failure, and an unsupported solver status.

## Solver and certificate ladder

Prefer a convex formulation when it faithfully expresses the problem. Match LP/QP/SOCP/SDP or smooth/nonsmooth structure to a suitable method. Use decomposition when separability or coupling justifies it, not merely because the problem is large.

Verify by independently rebuilding the objective and constraints from the returned variables. For convex differentiable problems, examine primal and dual residuals, stationarity, complementarity, and the duality gap. For mixed-integer or global methods, record incumbent, bound, gap, and time limit. For local nonconvex methods, use multiple starts or structural bounds and label the result local.

