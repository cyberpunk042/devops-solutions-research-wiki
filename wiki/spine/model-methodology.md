---
title: "Model: Methodology"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: authoritative
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources:
  - id: src-openarms-methodology
    type: documentation
    file: raw/articles/openarms-methodology-yaml-full.md
    title: "OpenArms Methodology YAML + Agent Directive"
    ingested: 2026-04-09
  - id: src-openfleet-methodology-scan
    type: documentation
    file: raw/articles/openfleet-methodology-scan.md
    title: "OpenFleet Methodology Deep Scan"
    ingested: 2026-04-09
tags: [methodology, model, stage-gate, task-types, composable, backlog, execution-modes, framework, spine]
---

# Model: Methodology

## Summary

The Methodology model defines the composable, selectable, nestable system of work processes that governs HOW all work is done across the DevOps ecosystem. Where the [[Model: LLM Wiki]] defines WHAT the wiki IS, this model defines HOW work proceeds — through named stage sequences with hard artifact gates, typed tasks that select which stages run, a backlog hierarchy that structures scope, and execution modes that control autonomy. It is not a single process; it is a framework for defining, composing, and adapting processes. The ground truth lives in `wiki/config/methodology.yaml` and `wiki/config/agent-directive.md` — this page defines the model those files implement.

## Key Insights

- **This is a FRAMEWORK, not a PROCESS**: A process is a fixed sequence you follow. This model defines a vocabulary (stages, gates, artifacts, types, modes) and composition rules that let you BUILD processes per-situation. Every specific workflow — wiki ingestion, feature development, research spikes, bug fixes — is an instance composed from the same primitives.

- **Stages are hard boundaries enforced by artifact category**: The Document stage may not produce implementation code. The Scaffold stage may not implement business logic. These are not guidelines — violation produces the wrong artifact category, which corrupts the stage system. See [[Never Skip Stages Even When Told to Continue]].

- **Task type selects the stage subset**: Not every task runs all 5 stages. A `docs` task runs only Document. A `research` task runs Document + Design. A `task` skips Document and Design entirely. Type selection is a complexity judgment that shapes the entire execution path.

- **Models compose at every scale**: SFIF (Scaffold, Foundation, Infrastructure, Features) runs at the project level. The 5-stage model runs at the task level inside each SFIF phase. A research model runs first, then feeds a feature model. This is not one level of process — it is fractal.

- **The quality dimension is an explicit parameter, not an accident**: [[Skyscraper, Pyramid, Mountain]] defines three quality targets. Skyscraper means full process. Pyramid means deliberate compression. Mountain means accidental chaos. The methodology makes the choice visible and intentional.

## Deep Analysis

### What a Methodology Model IS

A methodology model is a first-class, named entity with a precise definition. It is not a vague set of habits — it is a configuration object defined in YAML that governs execution. Every model consists of:

| Component   | Definition                                                                 |
|-------------|---------------------------------------------------------------------------|
| **Name**    | Unique identifier referenced in config and selection rules                |
| **Stages**  | Ordered sequence of phases, each with artifacts, protocols, and gates     |
| **Gates**   | Transition rules between stages (automatic, human-reviewed, score-based)  |
| **Protocols** | Per-stage rules: what is permitted, what is prohibited                  |
| **Parameters** | Configurable values: readiness ranges, max retries, commit style       |

Models are defined in `wiki/config/methodology.yaml` and can be created, modified, and versioned independently of the systems that execute them. The [[Methodology Framework]] page covers the full meta-system in detail.

### The 5-Stage System

Every methodology instance in this ecosystem is built from the same 5 stages. The sequence is invariant — stages always run in this order. Task types select WHICH stages run, but never reorder them.

| Stage       | Readiness | Produces                                         | Prohibits                                    |
|-------------|-----------|--------------------------------------------------|----------------------------------------------|
| **Document**  | 0-25%   | Wiki pages, gap analysis, source mapping         | Implementation code, tools, scripts          |
| **Design**    | 25-50%  | Specs, decision records, type sketches in docs   | Implementation code, file scaffolding        |
| **Scaffold**  | 50-80%  | Directory structure, empty files, config changes | Business logic, content beyond skeleton      |
| **Implement** | 80-95%  | Working code, filled wiki pages, tools           | Must follow design doc, no breaking changes  |
| **Test**      | 95-100% | Clean validation, manual review, no regressions  | No new features, fix-only                    |

**Stage boundaries are hard, not soft.** A commit titled `implement` that touches only wiki pages instead of source files is visibly wrong in the diff. The commit history IS the audit trail — one conventional commit per stage makes stage transitions visible in version control.

**Readiness is derived from stage completion, not subjective assessment.** A task with `stages_completed: [document, design]` cannot report readiness above 50% regardless of how much additional work was done. Readiness flows upward: task readiness aggregates into module readiness, module into epic.

**Max 2 retries per stage before escalation.** If a stage fails twice, it is blocked — not retried forever. This prevents infinite loops and surfaces structural problems for human review.

For full stage detail — per-stage artifacts, gate conditions, and the OpenFleet parallel model — see [[Stage-Gate Methodology]].

### The 8 Task Types

Task types are the selection mechanism that maps work to stage subsets. Choosing a type is a complexity judgment that determines the entire execution path.

| Type        | Stages Required                          | When to Use                                           |
|-------------|------------------------------------------|-------------------------------------------------------|
| **epic**    | document, design, scaffold, implement, test | Large cross-cutting initiative spanning modules       |
| **module**  | document, design, scaffold, implement, test | Scoped deliverable within an epic                     |
| **task**    | scaffold, implement, test                | Atomic work unit — the thing you actually do           |
| **research** | document, design                        | Investigation only — no code, no content creation     |
| **evolve**  | document, implement                      | Promote existing wiki content to higher maturity       |
| **docs**    | document                                 | Documentation only — wiki pages, specs, guides         |
| **bug**     | document, implement, test                | Fix broken tools, invalid pages, pipeline failures     |
| **refactor** | document, scaffold, implement, test     | Restructure without changing behavior                  |

Key design principles behind the type system:

- **Epic and module always require all 5 stages.** There is no shortcut for complex work. Skipping Document or Design on an epic produces implementation that does not fit the architecture.
- **Research is formalized as "investigation without implementation."** A research task is capped at Design — it produces understanding and options, never code. This prevents "quick research" from sliding into implementation.
- **Bug skips Design but keeps Document.** A bug fix should not introduce new architecture — it restores correct behavior within the existing design.
- **Task skips Document and Design.** Atomic work units operate within an already-documented, already-designed module. The parent module owns the understanding; the task owns the execution.

For the full artifact matrix with per-type exit criteria, see [[Task Type Artifact Matrix]].

### Composability

Methodology models are composable. This is what makes the system a FRAMEWORK rather than a fixed PROCESS. There are four composition modes:

**Sequential composition** chains models end-to-end. A research model runs first, producing a spec. A feature-development model runs next, consuming the spec as input. The output of model A feeds the input of model B.

**Nested composition** runs one model inside another's stage. At the project level, [[Scaffold, Foundation, Infrastructure, Features|SFIF]] runs as the macro lifecycle. Within each SFIF phase, the 5-stage micro model runs for individual tasks. Within Foundation phase, every task runs document → design → scaffold → implement → test. The macro model provides context; the micro model provides execution.

**Conditional composition** branches on type or context. If the task is a spike, run the research model. If it is a module, run the full model. If the project is in Foundation phase, emphasize Document and Design stages. The [[Task Type Artifact Matrix]] is itself a conditional composition table — task type selects stage subset.

**Parallel composition** runs multiple models on different tracks simultaneously. The execution track (code/wiki work) runs the 5-stage model. The PM track (backlog management) runs epic → module → task decomposition. The knowledge track (wiki evolution) runs ingest → synthesize → evolve → cross-reference. These are distinct models operating on different material at different cadences on the same project.

The recursive property: zoom into any level — project, epic, module, task — and you find the same structural vocabulary (stages, artifacts, gates, readiness) instantiated with different content. This is the fractal property described in [[Methodology Framework]].

### Backlog Hierarchy

Work is structured in a 3-level hierarchy. This is not optional organization — it is how readiness flows upward and scope flows downward.

```
EPIC (E001-name.md)        ← Cross-cutting initiative, all 5 stages
  └── MODULE (M001-name.md)  ← Scoped deliverable, all 5 stages
        └── TASK (T001-name.md)  ← Atomic work unit, type-selected stages
```

**You work on tasks, not epics.** Epics and modules are containers that track aggregate readiness. Tasks are the atomic units where stage-gated execution happens.

**Readiness flows upward.** A module's readiness is the aggregate of its tasks' readiness. An epic's readiness is the aggregate of its modules'. You never set epic readiness directly — it is computed.

**Status flows upward.** When all tasks in a module are done, the module is done. When all modules in an epic are done, the epic is done.

**A flat backlog is an anti-pattern.** Without hierarchy, you cannot distinguish scope (epic) from deliverable (module) from work unit (task). Priority becomes a single flat list with no structural relationship between items.

For full hierarchy rules — promotion rules, numbering conventions, and the relationship between hierarchy and stage gates — see [[Backlog Hierarchy Rules]].

### Execution Modes

Execution modes control how the agent progresses through work. They determine autonomy level, stop points, and end conditions.

| Mode              | Stops At   | Human Review | End Condition   | Use When                              |
|-------------------|-----------|--------------|-----------------|---------------------------------------|
| **autonomous**    | (none)    | No           | backlog-empty   | Default. Routine work, trusted agent  |
| **full-autonomous** | (none)  | No           | backlog-empty   | Skip Document on tasks (not epics)    |
| **semi-autonomous** | (none)  | After each task | backlog-empty | Sensitive or high-stakes work         |
| **document-only** | document  | No           | backlog-empty   | Exploration. Produce understanding only |
| **design-only**   | design    | No           | backlog-empty   | Planning. Produce specs only           |
| **scaffold-only** | scaffold  | No           | backlog-empty   | Structure. Produce skeleton only       |
| **plan**          | design    | No           | backlog-empty   | Alias for design-only                  |
| **custom**        | (configurable) | (configurable) | (configurable) | Per-run override             |

End conditions determine when the agent stops working entirely:

- **backlog-empty** — all tasks done or archived
- **stage-reached** — current task hit the stop stage
- **time-limit** — wall-clock hours exceeded
- **cost-limit** — API spend exceeded
- **task-count** — N tasks completed

For the full execution model — the 14-step work loop, the "never" list, and escalation rules — see [[Execution Modes and End Conditions]] and `wiki/config/agent-directive.md`.

### The Quality Dimension

Every methodology instance has a quality target. This is not aspirational — it is a parameter that governs how strictly stages and gates are enforced.

- **Skyscraper** — full process. Every stage runs, every artifact is produced, every gate is checked. The ideal for complex or high-stakes work.
- **Pyramid** — adapted process. Stages may be compressed, artifacts lighter, gates softer. But deviations are deliberate and documented, not accidental.
- **Mountain** — no process. Stages are skipped accidentally, artifacts missing, gates ignored. This is the anti-pattern.

The framework does not mandate Skyscraper rigor for everything. It mandates that the quality level is an EXPLICIT choice, made per-situation, not an accidental outcome of time pressure. See [[Skyscraper, Pyramid, Mountain]] for the full model.

### How to Adopt

The methodology is designed to be portable across projects. Adoption requires two files:

1. **`methodology.yaml`** — Copy from `wiki/config/methodology.yaml`. Adapt task types, artifact requirements, and stage protocols for your project's domain. Code projects reference source files; wiki projects reference wiki pages; infrastructure projects reference Terraform plans.

2. **`agent-directive.md`** — Copy from `wiki/config/agent-directive.md`. Adapt the work loop, the "never" list, and the escalation rules. This is the document the agent reads at the start of every session.

What is invariant (never change):
- The 5-stage sequence and its ordering
- Hard stage boundaries (Document cannot produce implementation)
- Readiness derived from stage completion
- The backlog hierarchy (epic → module → task)

What is per-project variable (always adapt):
- Which task types exist and their stage subsets
- Per-stage artifact requirements (wiki pages vs source files vs Terraform)
- Gate mechanisms (MCP tools vs CI checks vs manual review)
- Execution mode defaults
- End condition parameters

For the full adoption guide including integration levels (CLI, Skills, MCP, Export), see [[Adoption Guide — How to Use This Wiki's Standards]].

### Relationship to Other Models

The Methodology model is the governance layer — it defines HOW work is done. Every other model in the wiki operates WITHIN this framework:

- [[Model: LLM Wiki]] defines WHAT the wiki IS. The Methodology model defines how wiki work proceeds through stages.
- [[Model: Claude Code]] defines the agent's capabilities. The Methodology model defines how those capabilities are sequenced and gated.
- [[Model: Ecosystem Architecture]] defines the project topology. The Methodology model defines how work flows through that topology.
- [[Model: Skills + Commands + Hooks]] defines the tooling surface. The Methodology model defines when each tool is permitted (per-stage protocols).
- [[Model: Second Brain]] defines the knowledge vision. The Methodology model defines the ingest-synthesize-evolve pipeline that realizes it.

This is not a peer relationship — it is a governance relationship. The Methodology model is the super-model. All others are subject to its stage gates, type system, and execution modes.

## Open Questions

- Should the methodology model define a formal composition algebra (A ; B for sequential, A | B for parallel, A(B) for nested) or is the current prose description sufficient?
- How should stage gates differ between fully automated pipelines (CI/CD) and agent-assisted workflows? Currently the model assumes an agent is present.
- What is the minimum viable methodology for a project that only needs 3 stages (Document, Implement, Test)? Is that a valid model instance or a violation?

## Relationships

- GOVERNS: [[Model: LLM Wiki]], [[Model: Claude Code]], [[Model: Ecosystem Architecture]], [[Model: Skills + Commands + Hooks]], [[Model: Second Brain]]
- BUILDS ON: [[Methodology Framework]]
- BUILDS ON: [[Stage-Gate Methodology]]
- BUILDS ON: [[Task Type Artifact Matrix]]
- BUILDS ON: [[Backlog Hierarchy Rules]]
- BUILDS ON: [[Execution Modes and End Conditions]]
- BUILDS ON: [[Skyscraper, Pyramid, Mountain]]
- RELATES TO: [[Spec-Driven Development]]
- RELATES TO: [[Scaffold, Foundation, Infrastructure, Features]]
- RELATES TO: [[Adoption Guide — How to Use This Wiki's Standards]]
- IMPLEMENTS: wiki/config/methodology.yaml, wiki/config/agent-directive.md

## Backlinks

[[Model: LLM Wiki]]
[[Model: Claude Code]]
[[Model: Ecosystem Architecture]]
[[Model: Skills + Commands + Hooks]]
[[Model: Second Brain]]
[[Methodology Framework]]
[[Stage-Gate Methodology]]
[[Task Type Artifact Matrix]]
[[Backlog Hierarchy Rules]]
[[Execution Modes and End Conditions]]
[[[[Skyscraper]]
[[Pyramid]]
[[Mountain]]]]
[[Spec-Driven Development]]
[[[[Scaffold]]
[[Foundation]]
[[Infrastructure]]
[[Features]]]]
[[Adoption Guide — How to Use This Wiki's Standards]]
[[wiki/config/methodology.yaml]]
[[wiki/config/agent-directive.md]]
