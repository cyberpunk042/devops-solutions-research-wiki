---
title: "Task Type Artifact Matrix"
type: concept
layer: 2
domain: devops
status: synthesized
confidence: authoritative
created: 2026-04-09
updated: 2026-04-09
maturity: growing
derived_from:
  - "Stage-Gate Methodology"
  - "Task Lifecycle Stage-Gating"
sources:
  - id: src-openarms-methodology-yaml-full
    type: documentation
    file: raw/articles/openarms-methodology-yaml-full.md
    title: "OpenArms Methodology YAML + Agent Directive — Full Reference"
    ingested: 2026-04-09
  - id: src-openfleet-methodology-scan
    type: documentation
    file: raw/articles/openfleet-methodology-scan.md
    title: "OpenFleet Methodology Scan — Deep Research Findings"
    ingested: 2026-04-09
tags: [task-types, artifact-matrix, epic, module, task, bug, spike, docs, refactor, stage-requirements, exit-criteria, methodology, openarms, per-type, complexity-scaling]
---

# Task Type Artifact Matrix

## Summary

The Task Type Artifact Matrix defines the 7 distinct task types in the OpenArms methodology — epic, module, task, bug, spike, docs, refactor — and maps each to its required stages, artifact requirements, and exit criteria. This is the "per-case, per-size, per-type" flexibility layer that sits on top of the 5-stage system: not every task requires all five stages. A `docs` task requires only the Document stage; a `spike` requires Document + Design with no code produced at all; a `task` skips the design stage entirely. The matrix prevents over-process on simple work while enforcing full staging on complex work.

## Key Insights

- **Type selection is a complexity judgment, not a formality**: Choosing `task` instead of `module` is not just labeling — it determines which stages the agent is required to complete. Choosing `spike` instead of `task` means the agent is forbidden from producing any implementation code. Type selection shapes the entire execution path.

- **Spike is the formalization of "research without implementation"**: A spike is capped at Design stage — it produces Document (understanding) and Design (options + decision) artifacts only. It never produces code. This formally prevents the pattern where a "quick research spike" slides into implementation. The type system enforces the boundary.

- **Docs tasks enforce the principle that documentation IS the work**: A `docs` task requires only the Document stage. But the Document stage requires a complete wiki page with gap analysis — not a stub. This prevents documentation from being treated as a lesser task while also preventing over-engineering of pure documentation work.

- **Bug type skips Design but keeps Document**: A bug fix requires understanding the problem (Document) and then fixing it (Implement + Test) but does not require a design document. This is correct: a bug fix should not introduce new architecture — it should restore correct behavior within the existing design. Adding a Design requirement to bug fixes would create pressure to over-architect repairs.

- **Refactor type skips Design but adds Document**: A refactor requires understanding the current state (Document), creating the skeleton (Scaffold), implementing the transformation (Implement), and verifying nothing broke (Test). It does not require a separate design document because the refactor's "design" is captured in the Document stage: this is what exists, this is how it should be restructured.

- **Epic and Module always require all 5 stages**: There is no shortcut for complex work. An epic or module that attempts to skip the Document or Design stage will produce implementation that does not fit the existing architecture. The 5-stage requirement for epics/modules is not overhead — it is the minimum viable process for non-trivial scope.

- **Exit criteria are the observable proof that a type is done**: Each type has specific "Done When" conditions that go beyond stage completion. A `task` is done when: all required stages in `stages_completed`, all Done When items verified, `readiness = 100`. The type definition is what determines what those Done When items are.

## Deep Analysis

### The 7 Task Types — Complete Reference

#### Type: `epic`

**What it is:** A large, strategic deliverable that spans multiple modules and often multiple sprints. An epic represents a meaningful capability — something the system can do after completion that it could not do before. Epics are containers: they define scope and acceptance criteria, but the actual work happens in their children (modules and tasks).

**When to use it:** When a feature or deliverable is large enough to require decomposition into multiple scoped sub-deliverables, each of which could be developed independently. Rule of thumb: if the work cannot be described in a single design document, it is an epic.

**Required stages:** document, design, scaffold, implement, test (all five)

**Required artifacts per stage:**
- Document: wiki page documenting the epic's scope, mapping of all affected systems, gap analysis
- Design: decision document, target config shape, interface/type sketches (high-level)
- Scaffold: top-level type definitions, .env.example for epic-level config, empty test files for acceptance tests
- Implement: implementation across all child modules (via child task completion)
- Test: acceptance tests passing, integration verified across child modules

**Exit criteria:** ALL child modules/tasks are `done` or `archived`. Acceptance criteria documented in the epic's design doc are met. All five stages appear in `stages_completed`. Readiness = 100. Status moved to `review` (never directly to `done` — human confirmation required).

**Critical rule:** Epics are NEVER manually marked `done`. The maximum automated status is `review`. Only after human review confirms the acceptance criteria are met can the status be advanced. This is because epic completion is a strategic decision, not just a mechanical stage completion.

---

#### Type: `module`

**What it is:** A scoped deliverable within an epic. A module represents one coherent subsystem or component — it is deliverable independently but exists in service of the parent epic. Modules are the unit of meaningful code review and integration.

**When to use it:** When a feature has been scoped to a specific subsystem (e.g., "implement the authentication service," "build the routing layer," "create the testing infrastructure"). A module is small enough to fit in a single sprint but too complex to skip design.

**Required stages:** document, design, scaffold, implement, test (all five)

**Required artifacts per stage:** Same as epic but scoped to the module's specific domain. The design document addresses only this module's decisions, not the broader epic.

**Exit criteria:** All tasks within the module are `done` or `archived`. All five stages in `stages_completed`. The module's acceptance criteria (defined in its design doc) are met. Status = `review` (never `done` — same rule as epic). Human review required before closing.

**Critical rule:** Same as epic — maximum automated status is `review`. A module completed without human review is incomplete. This rule exists because module boundaries often affect other systems, and automated verification cannot check cross-system compatibility.

---

#### Type: `task`

**What it is:** The atomic work unit. A task is a self-contained piece of implementation that can be fully specified, staged, and completed without requiring decomposition. Tasks are what agents actually execute.

**When to use it:** When the work is concrete enough to be described in a scaffold (type definitions + empty tests) before implementation begins. If you can write the function signature and test case before writing the implementation, it is a task.

**Required stages:** scaffold, implement, test

**Notice what is absent:** Document and Design stages are NOT required for standard tasks. This is deliberate — tasks within an epic/module inherit their design context from the parent. The task's design decisions were made at the module level. A task requires only: skeleton creation, implementation, and verification.

**Required artifacts per stage:**
- Scaffold: type definitions for the task's scope, empty test files with describe blocks
- Implement: implementation code, passing type checks, lint clean
- Test: test implementations, passing test suite, no regressions

**Exit criteria:** All three stages in `stages_completed`. All Done When items verified (defined per-task in frontmatter). Readiness = 100.

**Important nuance:** If a task requires making a design decision (choosing between approaches), it should be promoted to a `module` or given a `spike` to precede it. A task that sneaks design work into its implementation stage is a stage violation.

---

#### Type: `bug`

**What it is:** A defect fix that restores correct behavior without introducing new architecture. Bugs are not new features — they are corrections to existing functionality.

**When to use it:** When behavior diverges from specification and the fix is restorative (returning to the specified behavior) rather than additive (adding new behavior). If the fix requires a new design decision, it should be a `task` or `module` instead.

**Required stages:** document, implement, test

**Notice what is absent:** Design and Scaffold stages are NOT required. This is the correct behavior for a bug fix:
- Document: understand what the bug is, where it is, what the expected behavior is (the Document stage produces the bug analysis)
- Implement: fix the bug within the existing architecture
- Test: verify the bug is fixed, verify no regressions

**Required artifacts per stage:**
- Document: bug analysis document — what is broken, why it breaks, what the correct behavior is, which files are affected
- Implement: the fix, passing type checks, lint clean
- Test: test proving the bug is fixed, full regression suite passing

**Exit criteria:** The specific bug behavior no longer occurs. All three stages in `stages_completed`. Existing tests still pass. Readiness = 100.

**Why no Design stage:** Adding a design document to a bug fix creates architectural pressure — the agent may be tempted to redesign the affected area rather than fix the defect. The Document stage is sufficient to capture the understanding needed. The fix should be surgical, not expansive.

---

#### Type: `spike`

**What it is:** A time-boxed research task that produces knowledge artifacts only — no implementation code. A spike answers a question. It does not build anything.

**When to use it:** When a decision cannot be made without research. Examples: "Which of these three libraries should we use for X?", "Is approach A or approach B more compatible with our architecture?", "What are the performance characteristics of Y at our scale?"

**Required stages:** document, design (research only — no code)

**Required artifacts:**
- Document: research scope, existing state assessment, the specific question being answered
- Design: research findings with multiple options (minimum 3), tradeoffs documented, a recommendation with rationale

**Exit criteria:** The research question has a documented answer. The recommended approach is documented with enough specificity that a `task` or `module` can be created to implement it. The spike itself produces NO code.

**Critical constraint:** The word "research only" in the type definition is an absolute prohibition on code production. An agent that writes implementation code during a spike is violating the stage gate regardless of how small or exploratory that code appears. Exploratory code during a spike is the entry point to unplanned scope.

**Downstream:** A spike always exists in service of something that comes after. The spike's Design artifact (recommendation document) becomes the input to the Document stage of whatever task/module implements the recommendation. Spikes are NEVER the final word — they are always followed by implementation work that cites them.

---

#### Type: `docs`

**What it is:** A pure documentation task. It produces only documentation artifacts — wiki pages, design docs, reference docs, how-to guides.

**When to use it:** When the deliverable is documentation and nothing else. Examples: synthesizing a wiki page from research, writing an architecture document, creating a how-to guide, updating an existing doc to reflect current state.

**Required stages:** document (documentation only)

**Required artifacts:**
- Document: the documentation itself — a complete wiki page, design doc, or reference document meeting the quality gates (30+ word Summary, at least 1 relationship, reachable from domain _index.md)

**Exit criteria:** The documentation artifact exists and passes validation. Schema validation passes. Readiness = 100.

**Why only one stage:** Documentation IS the work. A `docs` task that has its Document stage complete has finished. There is no implementation to scaffold, no code to write, no tests to run. The Document stage quality gate is the complete quality gate for this type.

**Important nuance:** A `docs` task must still meet the Document stage quality gate. A stub page with no Summary, no Relationships, and no gap analysis is NOT a completed Document stage — it is an incomplete one. The single stage requirement does not lower the bar for that stage.

---

#### Type: `refactor`

**What it is:** A structural transformation of existing code that improves quality without changing behavior. A refactor changes HOW the system works internally while keeping WHAT it does externally constant.

**When to use it:** When code needs to be restructured, renamed, reorganized, or simplified, but the external behavior should remain unchanged. Examples: extracting a function, splitting a module, renaming for clarity, simplifying logic.

**Required stages:** document, scaffold, implement, test

**Notice what is absent:** Design stage is NOT required. This is because the refactor's "design" is captured in the Document stage: the Document artifact describes the current state and the target state. The transformation is the implementation, not a design decision.

**Required artifacts per stage:**
- Document: current state description (what exists and why it's being changed), target state description (what it should look like), affected files list
- Scaffold: create the new structure (new file if extracting, renamed stubs, empty modules)
- Implement: move/transform the code, maintaining all existing behavior
- Test: verify all existing tests still pass, add tests for any new structural contracts

**Exit criteria:** All four stages in `stages_completed`. External behavior unchanged (all existing tests pass). New structural clarity is demonstrable from the Document artifact description. Readiness = 100.

**Critical rule:** A refactor that changes external behavior is not a refactor — it is a bug or a feature. If the refactor reveals that behavior needs to change, that work must be tracked as a separate `task` or `bug`. Combining refactor and behavior change in one task is a scope violation.

---

### Stage Requirement Matrix

| Task Type | Document | Design | Scaffold | Implement | Test | Total Stages |
|-----------|----------|--------|----------|-----------|------|--------------|
| epic | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | 5 |
| module | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | 5 |
| task | — | — | REQUIRED | REQUIRED | REQUIRED | 3 |
| bug | REQUIRED | — | — | REQUIRED | REQUIRED | 3 |
| spike | REQUIRED | REQUIRED (research only) | — | — | — | 2 |
| docs | REQUIRED | — | — | — | — | 1 |
| refactor | REQUIRED | — | REQUIRED | REQUIRED | REQUIRED | 4 |

**Design principle behind the matrix:** The required stages track with the type's need for explicit decision-making and the risk of incorrect implementation:
- Epic/Module: highest risk, most stages — full planning before any execution
- Refactor: needs to understand before transforming, no new decisions required
- Task: inherits design from parent, needs skeleton + execution only
- Bug: needs to understand the defect, no new architecture, just correct the divergence
- Spike: needs to understand and decide, forbidden from producing code
- Docs: pure artifact production, Document stage IS the deliverable

---

### Choosing the Right Type

The choice of task type is a judgment call that shapes the entire execution path. Common errors:

**Calling an epic a task:** Results in design decisions being made during the Scaffold or Implement stage — where they belong in Document/Design. Produces architecture-without-understanding.

**Calling a task a spike:** Results in a task that produces a research document but no code — if code was needed, this is an incomplete deliverable.

**Calling a bug a task:** Results in a bug fix that includes a design document — creates architectural pressure to expand the fix into a redesign.

**Calling a module a task:** Skips the Document and Design stages for work that requires explicit design decisions. Produces implementation without understanding the broader system impact.

**Calling a spike a task:** Results in a spike that skips the Design stage (the research output). A spike without a Design artifact has no output — it produces nothing actionable.

The decision rule: if you are uncertain about scope, choose the type with MORE required stages. Over-process on a small task wastes one stage's worth of effort. Under-process on a complex task produces rework.

---

### Relationship to Readiness Scores

The task type determines which stages must appear in `stages_completed` to reach readiness milestones:

For a `task` (requires scaffold, implement, test):
- Readiness 0-49: no stages completed yet
- Readiness 50-79: scaffold complete
- Readiness 80-94: scaffold + implement complete
- Readiness 95-100: scaffold + implement + test complete

For an `epic` (requires all 5 stages):
- Readiness = AVERAGE of children's readiness (never set manually)
- Readiness 100 requires ALL children at 100 AND acceptance criteria verified

For a `docs` task (requires document only):
- Readiness 0-99: document stage incomplete
- Readiness 100: document stage complete, all quality gates passed

The readiness calculation is always derived from stage completion evidence, never from subjective assessment.

## Open Questions

- How should the type system handle tasks that start as one type and evolve? A spike that reveals the answer is obvious and implementation should begin immediately — does this become a `module` or does the spike complete and a new `module` task get created?
- Is there a case for a `spike+implement` type that allows code production after the research phase is committed? The current system requires a separate task to avoid commingling research and implementation. Is this overhead justified in all cases?
- The `refactor` type lacks a Design stage, which means the "target state" is captured in the Document stage. Is a single Document artifact sufficient to capture both "current state" and "target state" analysis? Or should refactors use a two-document approach (current state in Document, target state in Design)?
- How does the matrix interact with the `full-autonomous` execution mode that skips Document on non-epic/module tasks? A `task` type with `full-autonomous` would skip Document (already not required) and run scaffold → implement → test directly. But a `bug` type with `full-autonomous` would skip Document — which IS required for bugs. Is this a mode interaction bug in the methodology design?

## Relationships

- DERIVED FROM: [[Stage-Gate Methodology]] (the type matrix selects stage subsets from the full 5-stage system)
- BUILDS ON: [[Task Lifecycle Stage-Gating]] (per-type stage selection is the flexibility layer of stage gating)
- USED BY: [[Backlog Hierarchy Rules]] (epics and modules follow the full 5-stage path; tasks use the 3-stage path)
- USED BY: [[Execution Modes and End Conditions]] (execution modes interact with type requirements — e.g., full-autonomous behavior differs by type)
- RELATES TO: [[Spec-Driven Development]] (spike type formalizes research-without-implementation; docs type formalizes documentation-as-work)
- RELATES TO: [[Wiki Backlog Pattern]] (all 7 types appear in wiki backlog; type determines which stages are tracked in frontmatter)
- RELATES TO: [[Four-Project Ecosystem]] (all four projects use task types — spike for research, docs for wiki, task/module/epic for features)
- FEEDS INTO: [[Immune System Rules]] (type violations — e.g., code produced during a spike — are detectable diseases)

## Backlinks

[[[[Stage-Gate Methodology]] (the type matrix selects stage subsets from the full 5-stage system)]]
[[[[Task Lifecycle Stage-Gating]] (per-type stage selection is the flexibility layer of stage gating)]]
[[[[Backlog Hierarchy Rules]] (epics and modules follow the full 5-stage path; tasks use the 3-stage path)]]
[[[[Execution Modes and End Conditions]] (execution modes interact with type requirements — e.g., full-autonomous behavior differs by type)]]
[[[[Spec-Driven Development]] (spike type formalizes research-without-implementation; docs type formalizes documentation-as-work)]]
[[[[Wiki Backlog Pattern]] (all 7 types appear in wiki backlog; type determines which stages are tracked in frontmatter)]]
[[[[Four-Project Ecosystem]] (all four projects use task types — spike for research, docs for wiki, task/module/epic for features)]]
[[[[Immune System Rules]] (type violations — e.g., code produced during a spike — are detectable diseases)]]
[[Adoption Guide — How to Use This Wiki's Standards]]
[[Model: Methodology]]
