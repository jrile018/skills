# The Six Forms

One skeleton, six jobs. Every form obeys the invariants in SKILL.md. These are examples to adapt, not mandatory scaffolds. Apply the freshness, completion, and isolation rules in [runtime-model.md](runtime-model.md) to every form; single-run layouts below are illustrative.

Contents: Selection · 1 Pipeline · 2 Umbrella · 3 Record library · 4 Knowledge bundle · 5 Context map · 6 System map · Composing forms

## Selection

Ask one question first: **what is the repeating unit of work?**

| The unit is… | Form |
|---|---|
| a run (same stages, new deliverable each time) | Pipeline |
| several kinds of runs sharing one identity | Umbrella |
| a record that accumulates (person, client, session) | Record library |
| the knowledge itself (claims, notes, evidence) | Knowledge bundle |
| an organization (teams, processes, data, handoffs) | Context map |
| a folder later agents must edit (code, markdown, or mixed) | System map |

## 1. Pipeline — the production line

The paper's canonical shape. A sequence runs with different input and produces a deliverable. Preserve the user's explicit review gates; authorized automation can continue between gates.

```
workspace/
├─ CLAUDE.md               identity + routing table
├─ CONTEXT.md              the pipeline in one screen
├─ stages/
│  ├─ 01_research/   {CONTEXT.md, references/}
│  ├─ 02_script/     {CONTEXT.md, references/}
│  └─ 03_production/ {CONTEXT.md, references/}
├─ runs/<run-id>/          products and completion sidecars, isolated for every run
├─ _shared/                factory: voice.md, design-system.md
└─ setup/questionnaire.md  configures the factory once
```

**Defining moves:**
- Handoff = a validated same-run output becomes the next stage's input. Human edits are new versions requiring revalidation.
- Each contract carries a "load this / do NOT load that" inputs table.
- `status` comes from version-bound completion sidecars and acceptance checks, never file existence alone. Every repeatable run uses a fresh `runs/<run-id>/<stage>/`, even sequential runs.
- Stage boundaries sit where the human naturally pauses to check — surfacing the judgment call (an outline, a structural plan) as an editable file *before* the expensive downstream work is the whole trick. Correction is cheapest at the earliest gate.

Design direction-setting and final outputs to be easy to inspect/edit. Measure actual review needs; do not assume a universal pattern of human intervention.

**Watch for:** stages that do two jobs (split them); contracts that restate reference material (point instead); pipelines built before the process has actually repeated (don't).

## 2. Umbrella — a portfolio of pipelines

Several distinct production lines share one brand, voice, and reference layer. The root is a map, not a sequence.

```
workspace/
├─ CLAUDE.md               the map: what lives where, which pipeline for which job
├─ 01-pillars/             shared factory: positioning, pillars
├─ 02-brand-voice/         shared factory: voice, style
├─ 03-video-production/    a full Pipeline workspace (own CLAUDE.md)
├─ 04-scene-generation/    a full Pipeline workspace (own CLAUDE.md)
└─ 05-animation-studio/    a full Pipeline workspace (own CLAUDE.md)
```

**Defining moves:**
- Each sub-pipeline is self-contained with its own entry file — "they don't share state" except through the root reference layers.
- The root entry file routes by task ("making a talking-head video → 03; animating a diagram → 05") and holds nothing else.
- A pipeline may host sibling *patterns* (two variants of the same line, e.g. record-then-cut vs animation-first) — the routing move recursing one level down.

**Watch for:** the root map going stale as pipelines evolve (the map states only what rarely changes; details live in each pipeline); shared reference duplicated into sub-pipelines (link up instead).

## 3. Record library — the unit is a record

Nothing "runs" to completion; records (people, clients, sessions, deals) get created, accumulate, and are looked up. The structure optimizes retrieval and uniform shape.

```
workspace/
├─ 00_START-HERE.md        the map (identity + routing in one file)
├─ _index/                 catalog: log.md — one line per record, id + status
├─ _templates/
│  └─ record-template/     the stamp: every record starts as a copy of this
├─ 01_reference/           factory: the method, rules, shared knowledge
└─ records/
   ├─ acme-corp/           each record the same internal shape
   └─ jane-doe/
```

**Defining moves:**
- **A new record is a copy, not a blank page.** The template *is* the schema.
- Records and their lifecycle evidence are authoritative. The index is a derived catalog with generation scope/version, one line per record, and a small lifecycle (`briefed → active → archived`). Rebuild after relevant changes.
- Naming convention doubles as an id scheme (`ht10-second-brain`: type + counter + slug).
- Records can recurse: each record may internally be a mini knowledge bundle or pipeline (a person-record holding its own layered brain; a session-record holding its own six-stage line). Uniformity across records is what makes the library queryable.

**Watch for:** records drifting from the template shape (re-stamp them); the index log absorbing content (it's a catalog line, not the record); half-created records with only one file (finish the stamp or archive it).

## 4. Knowledge bundle — the product is the knowledge

The deliverable is a navigable body of knowledge: a brain, a domain wiki, a model of a person or subject. Often emitted by an extraction pipeline (factory and product as two separate top-level trees).

```
workspace/
├─ CLAUDE.md
├─ corpus/                 raw sources + _index.md checkbox manifest (state surface)
├─ extraction/             the factory: an ICM Pipeline whose output is the bundle
└─ bundle/                 the product:
   ├─ index.md             what's in here, layer by layer
   ├─ voice/  (layer A)    always-load essentials
   ├─ dispositions/ (B)    load-by-task
   └─ episodes/ (C)        evidence, loaded last, access-tiered
```

**Defining moves:**
- Every note carries typed YAML frontmatter (`type:`, `layer:`, `access_tier:`, `strength:`) — labels make it queryable, links make it a graph.
- Notes cross-link by relative path or wikilink. Mark proposed/unwritten links explicitly; unresolved evidence links are errors, not evidence of a fact.
- Layered loading is the reading protocol: always-load layer first, task-relevant nodes second, evidence only when needed. Never slurp the bundle.
- `access_tier` documents sensitivity but does not enforce access control. Derived patterns can disclose private information too; retain source sensitivity and require authorization before export.
- Regenerating the bundle is an authorized factory run; write run-local change records, or serialize an explicitly owned shared log. Do not let workers append concurrently without a supported coordination mechanism.

**Watch for:** the bundle read as a search index instead of a model (it answers "how does this think," not "find me the file"); frontmatter fields nobody queries (cut them); extraction runs that edit the product by hand (fix the factory).

## 5. Context map — the organization as a graph

The subject is a company or team: who does what, what data moves where, what's ripe for automation. Nodes + labels + links rather than stages.

```
workspace/
├─ AGENTS.md               existing host entry; preserve unrelated instructions
├─ FILE-MAP.md             derived index — check freshness and coverage
├─ _meta/                  the rules: schema.md, maturity-levels.md, ritual docs
├─ teams/
│  └─ marketing/
│     ├─ Marketing.md      node card: In / Movement / Out / Edges
│     ├─ governance.md
│     ├─ jobs/             outcome nodes
│     ├─ processes/        workflow nodes (the workhorses)
│     └─ data/             data-<thing>.md asset nodes
├─ patterns/               cross-team patterns, written bottom-up only
└─ dashboards/             00-tracker.md … live queries over frontmatter
```

**Defining moves:**
- A closed set of node types (team, job, process, data-asset, governance, pattern) defined once in `_meta/schema.md`; every node declares its `type:` in frontmatter.
- Process nodes carry the scoring frontmatter: owner, ai-level (L0 manual → L3 integrated), frequency, value 1–5, pain 1–5, `consumes:`/`produces:` as wikilinks to data assets. The links draw the org graph on their own; high value + high pain = pilot candidate.
- **The workshop is the data event.** Map live with the team; every session ends in clean node files, not slides. "You don't point an agent at a legacy mess — you clean the shelf first."
- The librarian ritual per team: inventory → single source of truth → give it shape → catalogue → shelve by sensitivity → connect the agent. The human stays the approval gate; the agent drafts and proposes.
- Repeated independent evidence strengthens a pattern; record its sample and counterexamples. Three occurrences may be a useful heuristic, not a proof or universal threshold.

**Watch for:** schema mandating names the files stopped using (reconcile immediately); duplicate entry files drifting; instance data tangled into the reusable method (extract the blank starter kit early); node types multiplying past what anyone queries.

## 6. System map — a body of work as an edit graph

The subject is a tree someone will change: a repository, a markdown vault, or both. The map exists so a later agent can answer “what is this” and “what else moves” without slurping the tree. Nouns are object cards; verbs are process cards; `effects/` is only an index into those cards.

```
subject/
├─ AGENTS.md                 existing host entry — authorized routing link to map/
└─ map/
   ├─ CONTEXT-catalog.md     small catalog; no duplicate instruction files required
   ├─ CONTEXT.md             universes + name collisions
   ├─ _meta/schema.md
   ├─ _templates/            object.md, process.md
   ├─ objects/               record library of nouns
   ├─ processes/             real movements only
   └─ effects/CONTEXT.md     if you change X, open these cards
```

**Defining moves:**
- The subject remains authoritative. Cards cite paths/symbols and source/configuration identity. Unresolved wiring is `unknown`; search misses do not establish deadness.
- Build useful slices: inventory → catalog → objects/processes → impact → reverify. Do not create empty speculative shelves or require artificial per-slice approval pauses.
- Impact distinguishes direct, transitive, conditional, and unknown paths. Negative claims need a bounded search envelope and evidence.
- Compose with Record library (the cards) inside this form. Do not confuse this with Context map (an org) or Knowledge bundle (how something thinks).

**Watch for:** copying behaviour into cards; mapping intent docs as live; two hand-edited entry files; marking `verified` without a citation.

The audit pipeline, card sections, and walk test for this form: [system-map.md](system-map.md).

## Composing forms

The forms nest, because the invariants are recursive:

- A **record library** whose records are **knowledge bundles** (a cohort of people, each carrying a layered brain).
- A **pipeline** that emits into a **record library** (each run becomes a session record with the pipeline folded inside it).
- An **umbrella** over pipelines that all draw on one **knowledge bundle** as their factory layer.
- A **context map** whose per-team folders each grow a small **pipeline** for their pilot process.
- An **umbrella** or repo whose `developer-docs/` (or vault root) hosts a **system map** of the subject beside a setup **pipeline**.

When composing, keep one rule absolute: each level has its own small catalog, and no level's catalog describes the internals of the level below — it links down and stops.
