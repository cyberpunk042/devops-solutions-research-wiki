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
  - id: src-openarms-methodology-evolution
    type: documentation
    file: raw/articles/openarms-methodology-evolution-2026-04-09.md
    title: "OpenArms Methodology Evolution — 7 Bugs, 6 Versions"
    ingested: 2026-04-09
  - id: src-openarms-integration-sprint
    type: documentation
    file: raw/articles/openarms-integration-sprint-learnings.md
    title: "OpenArms Integration Sprint Learnings"
    ingested: 2026-04-09
tags: [methodology, model, stage-gate, task-types, composable, backlog, execution-modes, framework, spine]
---

# Model: Methodology

## Summary

The Methodology model defines the composable, selectable, nestable system of work processes that governs HOW all work is done across the DevOps ecosystem. Where the [[Model: LLM Wiki]] defines WHAT the wiki IS, this model defines HOW work proceeds — through named stage sequences with hard artifact gates, typed tasks that select which stages run, a backlog hierarchy that structures scope, and execution modes that control autonomy. It is not a single process; it is a framework for defining, composing, and adapting processes. The ground truth lives in `wiki/config/methodology.yaml` and `wiki/config/agent-directive.md` — this page defines the model those files implement.

## Key Insights

- **This is a FRAMEWORK containing MULTIPLE models, not a single process.** Feature development has 5 stages. Research has 2. Ingestion has 4 with completely different stage names. Hotfix has 2. A project runs several of these simultaneously on different tracks. The framework defines the VOCABULARY (stages, gates, artifacts, conditions) and COMPOSITION RULES (sequential, nested, conditional, parallel) that let you build ANY work process from the same primitives.

- **Conditions select which model runs — not just which stages.** Task type is ONE condition. But also: project phase, domain, scale, urgency, current state. A research spike during foundation phase of a knowledge project evaluates ALL conditions simultaneously. The result is a SPECIFIC MODEL with specific overrides — not a subset of one fixed pipeline.

- **Models compose at every scale — three tracks run in parallel on every project.** The execution track (brainstorm → spec → plan → implementation), the PM track (epics → modules → tasks), and the knowledge track (ingest → synthesize → evolve → cross-reference) are THREE DIFFERENT MODELS running simultaneously. They interact (PM triggers execution, execution feeds knowledge, knowledge informs PM) but never merge into one sequence.

- **Stages have hard boundaries with ALLOWED and FORBIDDEN artifact lists.** Document may not produce code. Scaffold may not implement business logic. Implement MUST wire into the runtime (OpenArms Bug 6: 2,073 lines of orphaned code). These are not suggestions — they are enforced by hooks, commit conventions, and quality gates. See [[Never Skip Stages Even When Told to Continue]].

- **The quality dimension is an explicit parameter.** [[Skyscraper, Pyramid, Mountain]] — Skyscraper = full process, Pyramid = deliberate compression, Mountain = accidental chaos. The methodology makes rigor an EXPLICIT CHOICE per situation, not an accidental outcome.

- **The framework is recursive.** Ecosystem level runs SFIF. Project level runs SFIF. Inside each SFIF stage, epics run their model. Inside epics, tasks run their model. The SAME vocabulary applies at every level — the only thing that changes is which model is selected and what the artifacts are.

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

### Multiple Methodology Models

The framework contains MULTIPLE named methodology models, not one fixed pipeline. Each model is a different stage sequence for a different situation:

| Model | Stages | When selected | Example |
|-------|--------|---------------|---------|
| **Feature Development** | document → design → scaffold → implement → test | task_type = epic, module | Building a new subsystem |
| **Research** | document → design | task_type = spike, research | Investigating a topic, no code output |
| **Knowledge Evolution** | document → implement | task_type = evolve | Generating lessons/patterns from existing knowledge |
| **Documentation** | document | task_type = docs | Writing wiki pages, guides, specs |
| **Bug Fix** | document → implement → test | task_type = bug | Restoring correct behavior |
| **Refactor** | document → scaffold → implement → test | task_type = refactor | Restructuring without behavior change |
| **Hotfix** | implement → test | urgency = critical | Emergency fix, understanding already exists |
| **Ingestion Pipeline** | ingest → synthesize → cross-reference → evolve | domain = knowledge | Wiki source processing |
| **Project Lifecycle (SFIF)** | scaffold → foundation → infrastructure → features | scale = project | Full project build cycle |

These are NOT subsets of one pipeline — they are INDEPENDENT models with different stage sequences. The "Feature Development" model has 5 stages. The "Research" model has 2 completely different stages. The "Ingestion Pipeline" has 4 stages with different names entirely.

### The 5 Common Stages (One Model, Not The Only Model)

The most frequently used model is the 5-stage Feature Development model. Its stages are:

| Stage       | Readiness | Produces                                         | Prohibits                                    |
|-------------|-----------|--------------------------------------------------|----------------------------------------------|
| **Document**  | 0-25%   | Wiki pages, gap analysis, source mapping         | Implementation code, tools, scripts          |
| **Design**    | 25-50%  | Specs, decision records, type sketches in docs   | Implementation code, file scaffolding        |
| **Scaffold**  | 50-80%  | Directory structure, empty files, config changes | Business logic, content beyond skeleton      |
| **Implement** | 80-95%  | Working code, filled wiki pages, tools           | Must follow design doc, no breaking changes  |
| **Test**      | 95-100% | Clean validation, manual review, no regressions  | No new features, fix-only                    |

This is the DEFAULT model for complex work. But it is not the ONLY model. A research task uses a completely different 2-stage sequence. An ingestion task uses a 4-stage sequence with different stage names. The framework accommodates all of them.

### Model Selection — How Conditions Choose Which Model Runs

Model selection is driven by conditions evaluated against the current context:

| Condition | What it determines | Example |
|-----------|-------------------|---------|
| **task_type** | Which stages are required | `spike` → Research model (2 stages) |
| **Project phase** | Which stages are emphasized | Foundation phase → emphasize Document + Design |
| **Domain** | Which family of models applies | Knowledge domain → Ingestion Pipeline model |
| **Scale** | Whether stages can be compressed | Single function change → skip Document |
| **Urgency** | Whether stages can be skipped | Critical production bug → Hotfix model |
| **Current state** | Which quality tier is realistic | Legacy codebase → Pyramid tier, not Skyscraper |

Selection can be multi-dimensional: task_type=spike AND phase=foundation AND domain=knowledge evaluates all conditions simultaneously to select the specific model and its overrides.

### Model Composition — How Models Chain, Nest, and Branch

Real work rarely runs a single model in isolation:

**Sequential**: Research model runs first (document + design), produces a spec. Feature Development model runs next (all 5 stages), consuming the spec. Output of model A becomes input of model B.

**Nested**: SFIF runs at the project level. Inside each SFIF stage, individual tasks run their own models. The Feature Development model is NESTED inside SFIF's Infrastructure stage. Three levels of nesting, each with its own model.

**Conditional**: An agent evaluates a task. If `bug` → Bug Fix model. If `spike` → Research model. If `module` → Feature Development model. The condition BRANCHES to different models, not different subsets of one model.

**Parallel (multi-track)**: Three tracks run simultaneously on every project:
- Execution track: brainstorm → spec → plan → implementation (how things get built)
- PM track: epics → modules → tasks with stage gates (what gets tracked)
- Knowledge track: ingest → synthesize → evolve → cross-reference (what gets learned)

These are different models on different tracks, interacting but not merging.

**Stage boundaries are hard, not soft.** The commit history IS the audit trail — one conventional commit per stage makes stage transitions visible in version control. A commit titled `scaffold` that contains business logic is visibly wrong in the diff.

**Each stage has ALLOWED and FORBIDDEN artifact lists.** This was learned from OpenArms' first autonomous agent run (Bug 5: "scaffold stage produced 135-line env reader with business logic"). Stage names alone are not enough — each stage needs explicit boundaries:

**Scaffold ALLOWED**: type definitions, static constants, Zod schemas, .env entries, empty test files with placeholder assertions.
**Scaffold FORBIDDEN**: business logic (parsers, resolvers, evaluators), env var readers with parsing logic, functions with more than a stub body, real test implementations.

**Implement ALLOWED**: business logic, helper functions, modifying existing runtime files to import new code.
**Implement REQUIRED**: at least one existing runtime file must import the new code. If nothing uses it, the code is orphaned and implement is NOT done. (Bug 6: "2,073 lines of production code — none imported by the runtime.")
**Implement FORBIDDEN**: modifying test files, writing test assertions.

**Test ALLOWED**: fill in scaffolded test files, add edge case tests.
**Test REQUIRED**: 0 test failures before marking done. Run tests, fix failures, run again, repeat until clean.
**Test FORBIDDEN**: proceeding with failing tests. (Bug 5: "test stage marked done with 1 failing test.")

**Readiness is derived from stage completion, not subjective assessment.** A task with `stages_completed: [document, design]` cannot report readiness above 50%. Readiness flows upward: task → module → epic.

**Max 2 retries per stage before escalation.** If a stage fails twice, it is blocked — not retried forever.

For full stage detail — per-stage artifacts, gate conditions, and the OpenFleet parallel model — see [[Stage-Gate Methodology]].

### The Bridge Module Pattern

Discovered during OpenArms' integration sprint: when wiring new code into the runtime during the implement stage, prefer creating a thin bridge/adapter module instead of making large changes to existing core files.

```
New module:    src/config/network-rules-resolver.ts  (standalone logic)
Bridge:        src/infra/net/network-rules-bridge.ts (thin adapter)
Consumer edit: src/infra/net/fetch-guard.ts          (one import line added)
```

The bridge module imports from the new module, exports a function shaped for the consumer's needs, and contains minimal logic. This keeps diffs small and separation clean. Agents naturally produce this pattern when "Done When" items name the specific consumer file.

### What Goes Wrong — 7 Bugs from Real Autonomous Operation

These bugs were found during OpenArms' first day of autonomous agent operation (2026-04-09). Each led to a methodology version bump:

| Bug | What happened | Fix | Version |
|-----|--------------|-----|---------|
| **Binary status** | Tasks were done/not-done. No stage tracking. Agent skipped stages. | Added task_type, current_stage, readiness, stages_completed to frontmatter. Reset 22 tasks. | v2 |
| **Epic status manual** | Epics manually set to "done" with zero children complete. | Status/readiness computed from children. Max agent-settable = "review". | v3 |
| **Rogue task creation** | Agent ignored existing tasks, created its own with colliding IDs. | "Pick from existing tasks ONLY. Do NOT create new task files." | v3 |
| **Lost files** | Write tool succeeded but files disappeared — destructive git revert killed untracked files. | "Commit immediately after creating files. Never destructive git without git status." | v3 |
| **Stage boundary violation** | Scaffold produced 135 lines of business logic. Test marked done with failures. | Added ALLOWED/FORBIDDEN lists per stage. Gates require passing commands. | v4 |
| **Orphaned implementation** | 2,073 lines of code that nothing imported. Tests pass ≠ feature works. | "At least one existing runtime file must import the new code." | v5 |
| **Unreadable logs** | Raw JSON stream events, 95% token chunks. Impossible to monitor or report. | Built agent-report.py (aggregation, compliance checking, cost per stage). | v5 |

**Methodology version history**: 6 versions in one day. Each version fixed real problems found in production. The methodology is not a design exercise — it is a LIVING document hardened by real failures.

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

### Real Example: Three Tracks Running on One Project

Here is how the methodology actually works on this research wiki project RIGHT NOW — three tracks running in parallel, each with its own model:

**Knowledge track** (wiki model: ingest → synthesize → cross-reference → evolve):
- User provides a URL → `pipeline fetch` saves to raw/ → agent reads the FULL source (depth verification: Layer 0 description is not enough, must reach Layer 1 instance) → creates source-synthesis page in wiki/sources/ → creates/updates concept pages in wiki/domains/ → `pipeline post` validates → `pipeline crossref` finds new connections → `pipeline evolve --score` identifies candidates for lessons/patterns/decisions

**PM track** (backlog model: epics → modules → tasks):
- E001 "Local Inference Engine" exists at readiness 10% (document stage done, blocked on hardware). T001 "Test OpenAI backend" is its child task, status=blocked. When hardware arrives, T001 moves to active, an agent picks it up, progresses through scaffold → implement → test stages, each with its own commit and frontmatter update. T001's completion bumps E001's readiness upward.

**Execution track** (superpowers model: brainstorm → spec → plan → sub-agent implementation):
- User says "build the backlog system" → brainstorm skill runs (questions, approaches, design sections) → spec written to docs/superpowers/specs/ → plan written to docs/superpowers/plans/ → sub-agents execute tasks from the plan → code reviewer validates → merge

These three tracks ran SIMULTANEOUSLY during this session. The knowledge track ingested OpenArms methodology evolution. The PM track has 2 epics and 1 task. The execution track produced the backlog system via spec → plan → implementation. They fed each other: the knowledge track's research on OpenArms informed the execution track's design, which created the PM track's infrastructure.

**This is what the methodology LOOKS LIKE in practice.** Not one pipeline — three concurrent models interacting through defined interfaces.

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
[[Model: Skills, Commands, and Hooks]]
