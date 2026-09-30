# Modular Skill Architecture

Use this reference when a proposed skill spans multiple capabilities, operating modes, course topics, or a requested "sub-skill" hierarchy.

## Terminology

Use precise terms in the design brief:

- **Parent skill:** The discoverable skill whose `SKILL.md` owns the shared user goal and routes after activation.
- **Supporting module:** A focused reference, script, or asset loaded or executed only under a stated condition. It is not independently discoverable.
- **Separate skill:** A sibling skill with its own `SKILL.md`, description, activation boundary, and evaluation set.
- **Subagent:** A temporary worker with its own context. It is an execution choice, not a way to store curriculum or reference material.

"Sub-skill" is ambiguous. Replace it in final designs with either supporting module or separate skill. Do not place nested `SKILL.md` files inside a skill to represent modules. A skill bundle has one entrypoint; independently discoverable capabilities belong in separate skill directories.

## Start With the Smallest Shape

Use this decision sequence:

1. **Can one short `SKILL.md` handle the goal reliably?** Keep one self-contained skill.
2. **Does detail apply only after the same skill has already activated?** Keep a thin parent and move that detail into supporting modules.
3. **Would a user reasonably request the capability by itself, with a distinct success contract?** Consider a separate skill.
4. **Does the current task contain independent workstreams that benefit from separate contexts or parallel work?** Consider selective subagents at runtime.

Do not add a layer merely because the source material has one. Course weeks, book chapters, repository folders, and organizational departments are evidence structures, not automatic skill boundaries.

## Supporting Module Test

Make a capability a supporting module when most of these are true:

- It shares the parent's primary user goal and activation trigger.
- It is needed only after the parent has classified the request.
- Users rarely need to invoke it independently.
- Its details are large or conditional enough that loading them every time would waste context.
- It shares the parent's output contract, terminology, permissions, or evaluation policy.

Typical forms:

```text
skill-name/
|-- SKILL.md
|-- references/
|   |-- concept-map.md
|   |-- proof-review.md
|   `-- misconception-diagnosis.md
|-- scripts/
|   `-- verify_result.py
`-- assets/
    `-- response-template.md
```

The parent must link every module and state when to load or execute it. Avoid generic directions such as "consult references as needed."

## Separate Skill Test

Promote a capability to a separate skill only when it has a defensible discovery boundary. Strong evidence includes:

- A distinct user-facing goal that appears in realistic requests.
- Inputs, outputs, or success criteria different from the parent's.
- Useful invocation outside the parent domain or across several parent packages.
- A different permission, safety, or tool boundary.
- An evaluation set that can pass or fail independently.

Before promotion, check neighboring skill descriptions for overlap. If two descriptions would plausibly activate for the same ordinary request, either tighten ownership, keep the capability as a module, or define an explicit handoff boundary.

## Module Contract

Define every supporting module with the following fields. Prose is acceptable; use a table when comparing several modules.

| Field | Required question |
|---|---|
| Purpose | What decision or behavior does this module improve? |
| Load when | What observable request or intermediate condition requires it? |
| Do not load when | Which near-miss would waste context or distort the result? |
| Inputs and assumptions | What facts, artifacts, or prerequisites must already exist? |
| Owned guidance | Which decisions, procedure, or domain knowledge live here rather than in the parent? |
| Output or invariant | What must be produced, preserved, or verified? |
| Evidence | Which source, failure, correction, or benchmark justifies the guidance? |
| Verification | How can behavior be checked without grading copied wording? |
| Dependencies | Which tools or other modules are genuinely required? |

Keep shared rules in the parent only when every module needs them. Keep module-specific details in one module to prevent drift and conflicting instructions.

## Parent Router Contract

A modular parent `SKILL.md` should contain only:

- The shared goal and activation boundary.
- Inputs and outputs common to the whole workflow.
- A compact routing table from observable conditions to modules.
- Cross-cutting safety, permission, provenance, and verification rules.
- What to do when no module fits, several modules fit, or required evidence is missing.

Example routing table:

| Request condition | Load | Do not also load unless |
|---|---|---|
| The user asks whether a proof step is valid | `references/proof-review.md` | A prerequisite misconception must also be diagnosed |
| The user is learning and gives a mistaken explanation | `references/misconception-diagnosis.md` | The request also asks for a formal proof review |
| The result needs deterministic numerical checking | Run `scripts/verify_result.py` | The inputs satisfy the script's documented assumptions |

When several modules apply, load the smallest set that covers distinct decisions. State their order only when one module produces an input required by another.

## Course-Derived Packages

Treat a course as a source library, not as the routing hierarchy. First extract:

- Reusable capabilities and problem types.
- Prerequisites and misconception patterns.
- Stable methods, proof obligations, and verification checks.
- Source provenance, licensing conditions, exclusions, and edition or date.

Then map those capabilities through the supporting-module and separate-skill tests. Do not create one module per lecture or one agent per topic by default.

For tutoring, distinguish answer quality from teaching quality. Evaluate final correctness, reasoning validity, prerequisite diagnosis, hint progression, and transfer to unseen problems separately.

## Subagent Boundary

Use subagents when a real task can be divided into independent, bounded workstreams with clear expected results, such as:

- One worker proposes a solution while another searches for counterexamples.
- Separate workers review independent documents or source groups.
- One worker performs a technical derivation while another verifies provenance.

Keep short tasks, dependent reasoning steps, and one coherent tutoring conversation with the main agent. Do not spawn a subagent merely to read a module. Do not treat agreement among similar agents as proof; require evidence, deterministic checks, or an adjudication rule.

The design brief should state the runtime condition for delegation, the assignment given to each worker, the synthesis rule, and the stopping condition. If those cannot be stated concretely, omit the subagent layer.

## Routing and Behavior Evaluation

Test the architecture rather than only the prose.

### Parent activation

Include direct, indirect, incomplete, near-miss, and boundary-negative requests.

### Module routing

Include at least:

- One request for each module alone.
- One request that legitimately needs two modules.
- One request that activates the parent but needs no optional module.
- One near-miss for each module.
- One ambiguous request where the router should ask a question or state an assumption.

Record both required modules and forbidden unnecessary modules. A correct final answer does not excuse consistently wasteful or misleading routing.

For a graph-backed tree, also test that every route and dependency endpoint exists, no loading cycle is possible, shared rules have one canonical home, and a cold agent can reach the correct module from the parent in at most two reads.

### Separate-skill activation

Test the promoted skill against its former parent, neighboring skills, and ordinary agent behavior. Measure false activation as well as missed activation.

### Subagent value

Compare the same tasks with and without delegation. Keep subagents only when they improve meaningful quality, reduce serious errors, or shorten wall-clock time enough to justify added tokens, latency, and synthesis risk.

Use held-out or independently created tasks. Do not evaluate course-derived modules only on examples, assignments, or close paraphrases included in their source material.

## Architecture Findings to Report

For every modular design or audit, report:

1. The selected architecture and rejected simpler or more complex alternatives.
2. The parent goal and activation boundary.
3. The module contracts and routing matrix.
4. Any capabilities promoted to separate skills and their discovery boundaries.
5. Any permitted subagent pattern and the condition that justifies it.
6. Activation, routing, output, and baseline-comparison tests.
7. Remaining overlap, maintenance, source, licensing, and untested-behavior risks.
8. For comprehensive graph-backed work, the Graphify status, material derived edges, ICM-informed review result, walk-test result, and unresolved ambiguities. For a narrow audit, report only the affected path.
