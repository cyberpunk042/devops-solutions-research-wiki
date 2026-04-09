---
title: "Backlog Hierarchy Rules"
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
  - "Wiki Backlog Pattern"
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
tags: [backlog, epic, module, task, hierarchy, readiness, status-propagation, wiki-backlog, openarms, openfleet, task-management, decomposition, upward-aggregation]
---

# Backlog Hierarchy Rules

## Summary

The Backlog Hierarchy Rules define the three-level EPIC → MODULE → TASK structure used by the OpenArms project and mirrored in OpenFleet's Plane board. Eight rules govern how work is organized, how readiness propagates upward, how status flows upward, and when containers are considered done. The key operational principle: you work on TASKS, not epics or modules. To advance an epic, pick a task and complete its next stage. Epics are never manually marked done — they can reach a maximum of `review` status, requiring human confirmation before closure.

## Key Insights

- **Work happens at the task level, visibility lives at the epic level**: You never "work on an epic." You work on a task that is a child of a module that is a child of an epic. The epic is a coordination artifact — it holds acceptance criteria, tracks scope, and aggregates readiness. The task is the execution artifact — it has stages, frontmatter, and commits.

- **Readiness propagation eliminates false completion signals**: Epic readiness = AVERAGE of children's readiness. This cannot be overridden manually. An epic with 9 tasks at 100% and 1 task at 0% has 90% readiness — not 100%. This prevents the common failure mode of "marking an epic done because most of it is done."

- **Status propagation creates automatic visibility**: Any child in-progress → parent in-progress. ALL children done → parent moves to `review` (not `done`). The `review` ceiling for epics and modules means completion always requires a human confirmation step. The hierarchy does not need to be manually monitored — status flows upward automatically.

- **"No tasks remaining but not at 100%" is an incompleteness signal, not a stuck state**: When an epic has no undone tasks but readiness is below 100%, the correct response is to CREATE NEW TASKS to cover the gap. This is not a bug in the backlog — it is signal that the original decomposition was incomplete. The methodology requires acting on this signal rather than treating the epic as done.

- **Epics may stay in-progress for weeks — this is normal**: Long-running epics are a feature, not a problem. The hierarchy is designed for complex, multi-sprint work. An epic that has been in-progress for 3 weeks with consistent task completion is healthy. An epic that has been in-progress for 3 weeks with no task activity is stuck — and the watcher/health check should surface it.

- **The hierarchy maps to documentation layers**: In OpenFleet's implementation, epics correspond to major system areas, modules to subsystems, and tasks to implementation units. This is not coincidental — the hierarchy mirrors the architecture. When the architecture has a new layer, the backlog should have a new epic. When a subsystem is identified, a module should be created.

- **NEVER set epic readiness manually — it is derived, not declared**: This is one of the absolute prohibitions in the methodology. An agent that sets `readiness: 75` on an epic because "it feels about 75% done" is corrupting the readiness signal. Readiness on containers is always an aggregate of their children.

## Deep Analysis

### The Three Levels

#### Level 1: EPIC

An epic is a strategic container. It defines:
- A meaningful capability or deliverable at the product/system level
- Acceptance criteria that can only be verified when ALL children complete
- The scope boundary — everything that logically belongs to this delivery

**Epic characteristics:**
- Contains modules (and sometimes tasks directly, for small epics)
- Never worked on directly — only via its children
- Readiness = AVERAGE of all descendant task readiness (weighted or simple, depending on implementation)
- Status ceiling = `review` (never automatically moved to `done`)
- May contain its own YAML frontmatter with `epic_id`, `acceptance_criteria`, `dependencies`
- Example: E001 — Authentication System, E007 — Agent Fleet Elevation

**Epic lifecycle:**
```
created → draft → active → in-progress → review → done
```
The `in-progress` state is triggered by ANY child task becoming in-progress.
The `review` state is triggered by ALL child tasks reaching `done` or `archived`.
The `done` state requires human review confirming all acceptance criteria.

---

#### Level 2: MODULE

A module is a scoped deliverable within an epic. It defines:
- A coherent subsystem or component
- Its own acceptance criteria (more specific than the parent epic's)
- A bounded set of tasks that can be executed in roughly priority order

**Module characteristics:**
- Parent: always an epic
- Children: tasks (and sometimes sub-modules for very large modules)
- Readiness = AVERAGE of child task readiness
- Status ceiling = `review` (same rule as epics)
- Independently reviewable — a module can be reviewed and accepted before the parent epic is complete
- Example: M-SP01 (storm prevention subsystem), M-BM03 (budget mode implementation)

**When to create a module vs. a task:**
Create a module when:
1. The work requires full 5-stage execution (document → design → scaffold → implement → test)
2. The deliverable is independently reviewable and has its own acceptance criteria
3. The scope is too large to fit in a single sprint

Create a task when:
1. The work can be fully described in a scaffold (type definitions + empty tests)
2. The design decisions were made at the module level
3. The work can be completed within one session

---

#### Level 3: TASK

The task is the atomic unit of work. Tasks have:
- A specific `task_type` (epic/module/task/bug/spike/docs/refactor)
- A sequence of stages to complete based on type
- A `current_stage`, `stages_completed`, `readiness`, and `artifacts` in frontmatter
- One git commit per stage
- A definitive `done` state (readiness = 100, all required stages complete, all Done When items verified)

Tasks are what agents actually execute. The work loop (see Execution Modes and End Conditions) operates at the task level. Every agent action is: find the highest-priority undone task, determine its next required stage, execute that stage, update frontmatter, commit.

---

### The 8 Rules — Complete Reference

**Rule 1: An EPIC is a container. NEVER done by itself.**

An epic reaches `done` ONLY when ALL children are done AND acceptance criteria are met AND human review confirms. No amount of automated stage completion can close an epic. This rule prevents premature closure of strategic deliverables that appear complete on metrics but fail acceptance testing.

**Rule 2: A MODULE is a scoped deliverable within an epic. Same rule.**

Modules follow the same closure rule as epics. A module is never automatically moved to `done` — only to `review`. This is the correct behavior because modules often have cross-system impact that automated tests cannot verify. Human review is the gate.

**Rule 3: A TASK is the atomic work unit. Tasks go through stages. Done when all required stages complete.**

Tasks are the only items that can be automatically closed (status = `done`). When all required stages are in `stages_completed`, all Done When items are verified, and readiness = 100, the task can be marked `done` without human review. This is appropriate because tasks are scoped to be independently verifiable.

**Rule 4: READINESS flows UPWARD. Epic readiness = AVERAGE of children's readiness. Never set manually.**

This rule eliminates the "feel" from progress reporting. An epic's readiness is computed, not declared. The calculation:

```
epic_readiness = mean(all_task_readiness_in_epic)
```

Example: Epic E007 has 8 tasks with readiness [100, 100, 80, 50, 0, 0, 0, 0].
- Epic readiness = (100 + 100 + 80 + 50 + 0 + 0 + 0 + 0) / 8 = 41.25%
- Rounded to 41%

This forces honest reporting. If 4 tasks are done but 4 haven't started, the epic is 41% done — not "half done."

**Rule 5: STATUS flows UPWARD — any child in-progress → parent in-progress. ALL children done → parent moves to review (not done).**

Status propagation means the board state is always accurate without manual updates:
- Task moves to `in-progress` → its parent module becomes `in-progress` → its parent epic becomes `in-progress`
- All tasks in a module become `done` → module moves to `review`
- All modules in an epic become `done` or `review` → epic moves to `review`
- Human confirms review → epic moves to `done`

This propagation is implemented by the orchestrator's `_evaluate_parents()` step (in OpenFleet) or by the agent's post-task update (in OpenArms). The agent is responsible for updating _index.md when a task completes.

**Rule 6: You WORK ON TASKS, not epics. To advance an epic, pick a task and complete the next stage.**

This rule is the operational imperative. When an agent is given an epic to "work on," the correct behavior is:
1. Find the epic's undone tasks in priority order
2. Pick the highest priority undone task
3. Determine that task's next required stage
4. Execute that stage
5. Repeat

An agent that attempts to directly "work on an epic" without identifying a specific task has no clear artifact to produce and no stage to follow. The rule forces decomposition to the executable level before action begins.

**Rule 7: An epic may stay in-progress for weeks. Normal.**

This rule prevents false urgency. Long-running epics are not a problem to be resolved — they are the nature of complex work. The appropriate response to an epic that has been in-progress for 3 weeks is to check whether tasks are being completed consistently (healthy) or whether no tasks have been completed (stuck). The in-progress duration is not a quality signal by itself.

**Rule 8: When an epic has no tasks left but isn't at 100%, CREATE NEW TASKS to cover the gap.**

This rule addresses incomplete decomposition. If an epic's readiness is 80% and all tasks are `done`, the 20% gap must be covered by new tasks. The methodology does not allow "rounding up" — an epic cannot be closed if readiness is below 100%. The correct response to a gap is to identify what specific work fills it and create the task.

Examples of gaps that require new tasks:
- Integration testing between newly completed modules
- Documentation that was omitted from the original decomposition
- Performance testing that wasn't planned
- Edge cases discovered during implementation

---

### Readiness Calculation Example

Epic E007 has 2 modules, each with tasks:

**Module M-01 (5 tasks):**
- T001: readiness 100 (done)
- T002: readiness 100 (done)
- T003: readiness 80 (in scaffold stage)
- T004: readiness 0 (not started)
- T005: readiness 0 (not started)

Module M-01 readiness = (100 + 100 + 80 + 0 + 0) / 5 = 56%

**Module M-02 (3 tasks):**
- T006: readiness 100 (done)
- T007: readiness 50 (in design stage)
- T008: readiness 0 (not started)

Module M-02 readiness = (100 + 50 + 0) / 3 = 50%

**Epic E007 readiness:**
Option 1 (average of modules): (56 + 50) / 2 = 53%
Option 2 (average of all tasks): (100 + 100 + 80 + 0 + 0 + 100 + 50 + 0) / 8 = 53.75% ≈ 54%

The epic is approximately 53-54% done. An agent that claimed "the epic is mostly done" because 3 of 8 tasks are complete would be wrong — the quantitative measure provides precision that subjective assessment cannot.

---

### Connection to the Wiki Backlog Pattern

In the OpenArms project, the backlog lives in `wiki/backlog/`. Each level of the hierarchy corresponds to file types:

- `wiki/backlog/_index.md` — master view of all epics, with readiness rolled up
- `wiki/backlog/epics/E00X-name.md` — individual epic files with YAML frontmatter and module list
- `wiki/backlog/tasks/T00X-name.md` — individual task files with full task frontmatter (current_stage, stages_completed, readiness, artifacts)

The work loop reads `wiki/backlog/tasks/_index.md` to find the highest-priority undone task. After task completion, the agent updates:
1. The task file (status = done, readiness = 100)
2. The parent module/epic _index.md (move task to Completed table)
3. The master backlog _index.md (readiness aggregated upward)
4. A completion note in `wiki/log/`

This file-based hierarchy is the OpenArms adaptation of OpenFleet's Plane board + OCMC task system. The pattern is the same; the infrastructure differs.

---

### OpenFleet's Implementation

In OpenFleet, the hierarchy maps to Plane's issue structure:
- Epics = Plane Cycles or Groups
- Modules = Plane Modules
- Tasks = Plane Issues with task_type field

The orchestrator's `_evaluate_parents()` step runs on every 30-second cycle and checks whether all children of any parent are in done state. When triggered, the parent's status is updated to `review`. The fleet-ops agent handles the `review` state — it is the human-equivalent review gate in the fleet.

OpenFleet's `project-manager` agent is responsible for task assignment and sprint planning. It reads the backlog, identifies unassigned tasks, creates sprint plans, and assigns tasks to worker agents. This is the equivalent of a developer picking the next task in a solo context.

---

### Anti-Patterns and What They Signal

**Anti-pattern: Setting epic readiness manually**
Signal: The agent is trying to hide that many tasks are incomplete. Or the agent does not understand that readiness is derived. Either way, the readiness field has been corrupted and the dashboard is no longer reliable.

**Anti-pattern: Marking an epic `done` when modules are in `review`**
Signal: A review step was skipped. Either the human reviewer was bypassed or the status flow logic is broken. The maximum automated status for epics and modules is `review` — any `done` that appears without a review log entry is suspect.

**Anti-pattern: Creating tasks that are too large (should be modules)**
Signal: A "task" that requires both a design document and implementation code is actually a module. Breaking this pattern results in the Document and Design stages being skipped (tasks don't require them), producing implementation without design understanding.

**Anti-pattern: Leaving epic stale when readiness is 100% but status hasn't updated**
Signal: The status propagation logic failed to fire, or the agent forgot to update the parent after the last task completed. The agent should check parent status after every task completion.

**Anti-pattern: Closing an epic because all tasks are done, without checking acceptance criteria**
Signal: The acceptance criteria (documented in the epic's design stage) were never verified. Stage completion is necessary but not sufficient — the acceptance criteria are the final gate.

## Open Questions

- How should readiness be calculated when a module has sub-modules as well as direct tasks? Should sub-module readiness be averaged at the sub-module level first, or should all leaf tasks be averaged directly to the epic?
- What triggers the `review` state at the epic level in OpenArms' solo-agent context? In OpenFleet, fleet-ops is the reviewer. In a solo context, the agent moves the epic to `review` and then waits for the human. But without a notification mechanism, how does the human know a review is pending?
- The readiness average treats all tasks equally. Should higher-complexity tasks (those with more required stages) receive higher weight in the readiness calculation? A `docs` task reaching 100% is worth less work than a `module` reaching 100%.
- When a new task is created to cover a gap (Rule 8), how should the parent epic's readiness be recalculated? The act of creating a task reduces the epic's readiness (the denominator grows with readiness 0 in the new task). Is this the correct behavior, or should gap tasks be created with a flag that acknowledges they are gap-filling?

## Relationships

- DERIVED FROM: [[Stage-Gate Methodology]] (the hierarchy enforces stage-gating at the container level)
- BUILDS ON: [[Wiki Backlog Pattern]] (the file-based hierarchy IS the wiki backlog)
- IMPLEMENTS: [[Plan Execute Review Cycle]] (the review ceiling for epics/modules IS the review phase)
- USED BY: [[Task Type Artifact Matrix]] (epic and module types follow all 5 stages; the hierarchy rules define how they relate)
- USED BY: [[Execution Modes and End Conditions]] (the work loop picks tasks from the hierarchy; end conditions reference backlog-empty)
- RELATES TO: [[Four-Project Ecosystem]] (all four projects organize work in this hierarchy — Plane issues in OpenFleet, wiki backlog in OpenArms)
- RELATES TO: [[Spec-Driven Development]] (epics/modules always have design docs; their stage requirements enforce spec-first)
- FEEDS INTO: [[Immune System Rules]] (hierarchy violations — manual readiness, premature done status — are detectable anti-patterns)

## Backlinks

[[[[Stage-Gate Methodology]] (the hierarchy enforces stage-gating at the container level)]]
[[[[Wiki Backlog Pattern]] (the file-based hierarchy IS the wiki backlog)]]
[[[[Plan Execute Review Cycle]] (the review ceiling for epics/modules IS the review phase)]]
[[[[Task Type Artifact Matrix]] (epic and module types follow all 5 stages; the hierarchy rules define how they relate)]]
[[[[Execution Modes and End Conditions]] (the work loop picks tasks from the hierarchy; end conditions reference backlog-empty)]]
[[[[Four-Project Ecosystem]] (all four projects organize work in this hierarchy — Plane issues in OpenFleet, wiki backlog in OpenArms)]]
[[[[Spec-Driven Development]] (epics/modules always have design docs; their stage requirements enforce spec-first)]]
[[[[Immune System Rules]] (hierarchy violations — manual readiness, premature done status — are detectable anti-patterns)]]
[[Model: Methodology]]
