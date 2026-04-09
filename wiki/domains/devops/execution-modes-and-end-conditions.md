---
title: "Execution Modes and End Conditions"
type: concept
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
tags: [execution-modes, end-conditions, autonomous, full-autonomous, semi-autonomous, work-loop, git-management, quality-gates, openarms, backlog-empty, stage-reached, cost-limit, time-limit]
---

# Execution Modes and End Conditions

## Summary

Execution Modes and End Conditions define the operational envelope for autonomous agent execution in the OpenArms methodology. 8 execution modes — from `autonomous` (default, works through all stages) to `custom` (ephemeral per-run config) — determine which stages run and whether human review is required between tasks. 5 end conditions — from `backlog-empty` to `cost-limit` — determine when the agent stops. The 14-step work loop is the atomic execution unit that operates within this envelope, and git management rules (one commit per stage, conventional commit format) transform version control into the enforcement and audit layer.

## Key Insights

- **The default mode is fully autonomous — human review is opt-in, not default**: The `autonomous` mode works through all stages, picks the next task automatically, and stops only when the backlog is empty. Human review is NOT the default. This is a deliberate design choice: the stage gates, quality gates, and git audit trail provide sufficient safety that human review is not required for every task. Semi-autonomous mode (human review after each task) is available but not the default.

- **End conditions are separate from modes**: A mode defines HOW the agent executes (which stages, whether to pause for review). An end condition defines WHEN to stop. These are orthogonal dimensions. `autonomous` mode with `task-count: 5` stops after 5 tasks regardless of backlog state. `document-only` mode with `backlog-empty` runs document stage on every task until the backlog is empty.

- **The 14-step work loop is the invariant**: Every execution mode runs the same 14-step loop. Modes differ in which steps are present (semi-autonomous adds a review pause after step 11) and which stages are included (full-autonomous skips Document on tasks), but the loop structure is fixed. The loop is not optional — it is the execution contract.

- **One commit per stage is a quality gate, not a style preference**: The rule "ONE COMMIT PER STAGE, COMMIT IMMEDIATELY after creating files" makes the git history the stage audit trail. A task with 5 completed stages has exactly 5 commits. A task with a single "completed everything" commit violated the rule. The commit is the stage checkpoint — it is when the stage becomes real.

- **Quality gates are stage transition requirements, not post-hoc checks**: Each stage has a specific gate that must pass before advancing. The agent does not commit and then check the gate — the agent checks the gate and then commits. If the gate fails, the stage is not complete, and the commit does not happen. This ordering is critical: committing before the gate check corrupts the audit trail.

- **The `custom` mode is ephemeral**: Custom mode accepts per-run configuration that is not persisted. This is the escape hatch for unusual situations — when the standard modes do not fit the context. But unlike the named modes, custom mode configurations are not reusable and are not a pattern to build on.

- **VERIFY step in the loop prevents silent failures**: Step 8 of the 14-step loop explicitly requires re-reading the task file after updating frontmatter to confirm the update was written correctly. This is not paranoia — agents can fail to update files, write malformed YAML, or update the wrong field. The verification step catches these failures before proceeding to the next stage.

## Deep Analysis

### The 8 Execution Modes

#### Mode: `autonomous` (Default)

**Description:** The primary operation mode. Works through all required stages for each task type, picks the next task automatically after completion, and runs until the backlog is empty.

**Behavior:**
- All stages run (as required by task type)
- No human review between tasks
- Automatic task selection by priority (P0, P1, P2, P3)
- Continues until end condition is met

**Stop condition:** null (end condition determines stop)
**Human review:** false
**Default end condition:** backlog-empty

**When to use:** Standard development sessions where the backlog has been reviewed and tasks are well-defined. The default for all normal work.

**What it is NOT:** Autonomous mode does not mean unmonitored. The git history records every stage, every commit, every frontmatter update. The human can review the audit trail at any time.

---

#### Mode: `full-autonomous`

**Description:** Maximum autonomy. Skips the Document stage on non-epic/module tasks. Used for well-understood domains where understanding is pre-established.

**Behavior:**
- Document stage SKIPPED on `task`, `bug`, `refactor` types
- Document stage still REQUIRED on `epic`, `module` types
- No human review
- Automatic task selection

**Stop condition:** null
**Human review:** false
**Default end condition:** backlog-empty

**When to use:** When the domain is thoroughly documented and tasks are well-specified. When running a batch of implementation tasks in a context where the Document stage would be redundant (the information is already in the wiki).

**Risk:** Skipping the Document stage removes the understanding checkpoint. If any task requires genuine exploration of existing code or infrastructure, `full-autonomous` will produce misaligned implementation. Use with caution in unfamiliar domains.

---

#### Mode: `semi-autonomous`

**Description:** Autonomous execution with a human review pause after each task completes. The agent runs the full task lifecycle, then stops and presents the result for review before picking the next task.

**Behavior:**
- All stages run (as required by task type)
- After each task reaches `done`: STOP, present completion report, wait for human signal
- Resume on human confirmation
- Automatic task selection within each run

**Stop condition:** null (pauses after each task, resumes on signal)
**Human review:** true (after each task)
**Default end condition:** backlog-empty

**When to use:** When working in unfamiliar territory, when tasks have high risk, or when the human wants to review output before allowing the agent to continue. Also appropriate for onboarding — a new agent or developer can operate in semi-autonomous mode to build trust before switching to autonomous.

---

#### Mode: `document-only`

**Description:** Runs only the Document stage. Produces understanding and documentation artifacts without making any design decisions or writing any code.

**Behavior:**
- Only Document stage runs (for all task types)
- No design, scaffold, implement, or test
- Produces wiki pages, documentation, gap analyses

**Stop condition:** document (stops at document stage)
**Human review:** false
**Default end condition:** backlog-empty

**When to use:** At the start of a new domain or project. Run document-only across the backlog to build a comprehensive understanding of the space before committing to designs. Also useful for knowledge ingestion tasks where the goal is wiki population.

**Connection to SFIF:** Document-only mode corresponds to the early phase of SFIF's Scaffold stage — creating the understanding artifacts before any skeleton is built. It is the epistemic foundation of all subsequent work.

---

#### Mode: `design-only`

**Description:** Runs through the Design stage (inclusive). Produces Document + Design artifacts — understanding + decisions — without creating any scaffold or writing any code.

**Behavior:**
- Document and Design stages run
- No scaffold, implement, or test
- Produces wiki pages, design docs, config shape definitions, type sketches

**Stop condition:** design
**Human review:** false
**Default end condition:** backlog-empty

**When to use:** When the goal is to plan a feature or system without committing to implementation. Useful for sprint planning — run design-only on the next sprint's tasks to produce design artifacts before the sprint begins, so that implementation can start immediately.

---

#### Mode: `scaffold-only`

**Description:** Runs through the Scaffold stage (inclusive). Produces Document + Design + Scaffold artifacts — understanding, decisions, and skeleton — without writing any implementation.

**Behavior:**
- Document, Design, and Scaffold stages run
- No implement or test
- Produces wiki pages, design docs, type definitions, empty test files, .env entries

**Stop condition:** scaffold
**Human review:** false
**Default end condition:** backlog-empty

**When to use:** When preparing a codebase for a development sprint. Run scaffold-only on planned tasks to create the type definitions, file structures, and test scaffolds before implementation begins. This allows multiple developers or agents to implement in parallel against a shared skeleton.

**Connection to SFIF:** Scaffold-only mode directly maps to SFIF's Scaffold stage — it creates the project/feature skeleton that all subsequent implementation builds on.

---

#### Mode: `plan`

**Description:** Alias for `design-only`. Exists for semantic clarity — "plan this work" is more natural in some contexts than "design-only."

**Behavior:** Identical to `design-only`.

**Stop condition:** design
**Human review:** false
**Default end condition:** backlog-empty

---

#### Mode: `custom`

**Description:** Ephemeral per-run configuration. All parameters can be overridden for this run only.

**Behavior:** Defined per invocation — stop condition, human review, stages to run, and end condition are all specified at invocation time.

**Stop condition:** null (defined per invocation)
**Human review:** defined per invocation
**Default end condition:** null (defined per invocation)

**When to use:** One-off situations that don't fit any named mode. The configuration is not stored and not reusable.

**Warning:** Custom mode bypasses the protection provided by named modes. Use it only when the situation is genuinely unusual and the operator is present to monitor behavior.

---

### The 5 End Conditions

End conditions are independent from execution modes. They determine when the agent stops, regardless of which mode is active.

#### End Condition: `backlog-empty`

**Definition:** All tasks are `done` or `archived`. No runnable tasks remain.

**Behavior:** When the work loop reaches step 13 (check end condition), and the backlog contains no undone, unarchived, unblocked tasks, execution terminates.

**Default for:** All named modes except `custom`.

**Important nuance:** A backlog with tasks in `blocked` state is NOT empty. Blocked tasks remain in the backlog but cannot be executed. The agent should report blocked tasks at termination so the human can investigate dependencies.

---

#### End Condition: `stage-reached`

**Definition:** The current task has reached the specified stage. Stop after completing that stage on the current task.

**Behavior:** When a task completes its specified stage, execution terminates — even if more stages remain for the task and even if the backlog has other tasks.

**Example:** `stage-reached: design` — when the current task completes its Design stage, stop. The task is not finished; it has only reached the specified checkpoint.

**When to use:** When a human wants to review the design before implementation begins. The agent runs to `stage-reached: design`, produces the design artifact, and stops. The human reviews the design. If approved, the agent continues from scaffold.

---

#### End Condition: `time-limit`

**Definition:** Stop execution after N hours.

**Behavior:** The agent tracks elapsed time. When time-limit is reached, the agent completes the current stage (does not interrupt mid-stage), commits, and terminates cleanly.

**Example:** `time-limit: 2` — execute for 2 hours, then stop.

**When to use:** Session time-boxing. When the operator wants to run an autonomous session for a defined duration without monitoring it. The remaining work is left in the backlog for the next session.

---

#### End Condition: `cost-limit`

**Definition:** Stop execution when API call costs reach $N.

**Behavior:** The agent tracks accumulated API costs. When the cost-limit is reached, the agent completes the current stage, commits, and terminates cleanly.

**Example:** `cost-limit: 5` — stop when $5 USD in API costs has been spent.

**When to use:** Budget-conscious operation. Useful when running autonomous sessions with expensive models (Claude Opus) where runaway execution could be costly.

**OpenFleet analog:** OpenFleet's budget monitor reads real Claude OAuth quota before every dispatch cycle and pauses dispatch at 90% usage. The `cost-limit` end condition is the OpenArms equivalent — a hard stop rather than a rate reduction.

---

#### End Condition: `task-count`

**Definition:** Stop execution after N tasks are completed.

**Behavior:** The agent tracks completed task count. When N tasks have reached `done` status, execution terminates.

**Example:** `task-count: 3` — complete 3 tasks, then stop.

**When to use:** When the operator wants to review the output of a specific number of tasks before allowing more work. Useful for incremental sessions where each batch of completed tasks is reviewed before the next batch begins.

---

### The 14-Step Work Loop

The work loop is the atomic execution unit. Every task execution in every mode follows this exact sequence:

**Step 1: Read `wiki/backlog/tasks/_index.md`**
Find the highest priority undone task. Priority order: P0, P1, P2, P3. Skip: done, archived, blocked tasks.

**Step 2: Read task file**
Check `task_type`, `current_stage`, `stages_completed`, `readiness`. Understand exactly where this task is in its lifecycle.

**Step 3: Determine NEXT required stage**
Look up the task's `task_type` in `methodology.yaml` to find the required stages list. The next stage is the first stage in the required list that is NOT in `stages_completed`.

**Step 4: Read stage protocol**
Read the MUST/MUST NOT/CAN rules for the next stage. This step is mandatory — the agent must re-read the protocol before executing, not rely on remembered context from a previous iteration.

**Step 5: Execute ONLY that stage**
Produce ONLY the artifacts defined for that stage. No cross-stage artifact production. No "getting ahead" to the next stage. This is the stage gate in practice.

**Step 6: Update task frontmatter**
Update `current_stage`, `stages_completed`, `readiness`, `artifacts`, `status` in the task file. The frontmatter is the state machine — it must accurately reflect reality after every stage.

**Step 7: Git — stage and commit ALL changed files**
Stage all changed files. Commit with conventional format: `feat(wiki): T0XX stage-name — description`. This is ONE COMMIT for this stage. All files changed during this stage go in this commit. No partial commits.

**Step 8: VERIFY**
Re-read the task file. Confirm the frontmatter is correct: `current_stage` matches what was just completed, `stages_completed` contains all completed stages, `readiness` matches stage completion, `artifacts` lists all files created.

**Step 9: Check for more stages**
If more required stages remain (not all stages in task's required stage list are in `stages_completed`), go to step 3.

**Step 10: Mark task done when all stages complete**
When all required stages are in `stages_completed`: set `status = done`, set `readiness = 100`. Verify all "Done When" items documented in the task frontmatter are satisfied.

**Step 11: Update _index.md**
Move the task from the In Progress table to the Completed table in `wiki/backlog/tasks/_index.md`. If parent epic/module readiness should be updated, calculate and update.

**Step 12: Write completion report**
Write a completion note to `wiki/log/`. Format: task ID, completion timestamp, stages completed, artifacts produced, any deviations or issues.

**Step 13: Check end condition**
- `backlog-empty`: are all tasks done or archived? If yes → terminate. If no → go to step 1.
- `stage-reached`: was the specified stage reached on this task? If yes → terminate. If no → go to step 1.
- `time-limit`: has the time limit elapsed? If yes → terminate. If no → go to step 1.
- `cost-limit`: has the cost limit been reached? If yes → terminate. If no → go to step 1.
- `task-count`: has the task count been reached? If yes → terminate. If no → go to step 1.

**Step 14: Final commit and summary**
Commit any remaining uncommitted changes. Print session summary: tasks completed, stages completed per task, total commits, artifacts produced, remaining backlog state.

---

### Git Management Rules

Git management in the OpenArms methodology is not a style guide — it is a stage-enforcement mechanism.

**Rule: ONE COMMIT PER STAGE**
Each stage produces exactly one commit. If a stage produces 5 files, all 5 go in one commit. If a stage produces 1 file, that file goes in one commit. The commit is the stage checkpoint. Having multiple commits per stage obscures the stage boundary in git history.

**Rule: COMMIT IMMEDIATELY after creating files**
Do not accumulate uncommitted work. Each time files are created or modified as part of a stage, commit immediately. Uncommitted files are invisible to the audit trail and vulnerable to loss.

**Rule: NEVER destructive git commands without git status first**
Before any `git reset`, `git checkout .`, `git restore`, or `git clean`, run `git status` to understand what will be affected. This is a safety check — the methodology prioritizes auditability and recovery over speed.

**Rule: Conventional commit messages**
Format: `feat(wiki): T0XX stage-name — description`
- `feat`: conventional commit type (use `fix` for bugs, `docs` for documentation)
- `(wiki)`: scope (the project or subsystem)
- `T0XX`: task ID
- `stage-name`: the stage just completed (document, design, scaffold, implement, test)
- `description`: brief description of what was done

The stage name in the commit message is the key element. It creates a searchable git log by stage: `git log --oneline | grep "implement"` shows all implementation commits across all tasks.

---

### Quality Gates as Stage Transition Requirements

Each stage has a quality gate that must pass before the commit is made and before the agent advances:

**Document gate:**
- Wiki page exists with Summary (minimum 30 words)
- Gap analysis present
- Page reachable from domain _index.md

**Design gate:**
- Decision document exists
- Config shape defined
- Types sketched IN documentation (not in code)
- The decision is unambiguous (not "we might use X or Y")

**Scaffold gate:**
- Types compile without errors
- .env entries added to .env.example
- Empty test files exist with describe blocks (not just empty files)

**Implement gate:**
- Code compiles
- Type checks pass (tsc --noEmit or equivalent)
- Lint passes (no lint errors)

**Test gate:**
- Scoped tests pass (the tests for this task all pass)
- No regressions (existing test suite still passes)
- No "TODO: fix this later" patterns in test files

**What happens when a gate fails:**
The stage is not complete. The commit does not happen. The agent must fix the gate failure first. If the gate failure cannot be resolved within the max stage retries (default: 2), the task is flagged as blocked and the agent moves on. The blocking reason is recorded in the task frontmatter.

---

### Mode × End Condition Matrix

| Mode | Default End Condition | Can Override? | Typical Use Case |
|------|--------------------|--------------|-----------------|
| autonomous | backlog-empty | Yes | Standard development session |
| full-autonomous | backlog-empty | Yes | Batch implementation of well-understood tasks |
| semi-autonomous | backlog-empty | Yes | High-risk or unfamiliar work |
| document-only | backlog-empty | Yes | Knowledge ingestion, wiki population |
| design-only | backlog-empty | Yes | Sprint planning, design phase |
| scaffold-only | backlog-empty | Yes | Pre-sprint skeleton creation |
| plan | backlog-empty | Yes | Same as design-only |
| custom | null | Required | One-off unusual situations |

**Combining mode with end condition:**
- `autonomous` + `task-count: 3`: run 3 full tasks autonomously, then stop for review
- `design-only` + `stage-reached: design`: produce design docs for the first task only, then stop
- `document-only` + `time-limit: 1`: run document stage on tasks for 1 hour, then stop
- `full-autonomous` + `cost-limit: 10`: run full autonomy until $10 spent, then stop

---

### Relationship to OpenFleet's Work Mode System

OpenFleet implements a parallel system through its `work_mode` control axis:

| OpenFleet work_mode | OpenArms equivalent |
|--------------------|-------------------|
| normal-work | autonomous |
| full-autonomy | full-autonomous |
| finish-current-work | autonomous until current task completes, then stop |
| work-paused | — (OpenArms equivalent: no invocation) |

OpenFleet's budget monitor adds an additional layer: dispatch is paused at 90% OAuth quota, hard-stopped at 95%. OpenArms achieves the same via the `cost-limit` end condition.

The key architectural difference: OpenFleet's work_mode is a fleet-level control set by the PO via Mission Control, affecting all 10 agents simultaneously. OpenArms' execution mode is a per-invocation parameter for the single agent. In a fleet context, changing the mode requires updating a config — in a solo context, it is a parameter to the session call.

## Open Questions

- What is the correct behavior when a quality gate fails and max retries are exhausted? The current specification says the task becomes `blocked`. But should the agent create a new `bug` task describing the gate failure, so the blocker is tracked and eventually resolved?
- How should the cost-limit end condition interact with a task that is mid-stage? If cost limit is reached during the Implement stage, the agent cannot commit partial implementation (it would leave code in an inconsistent state). Should the agent abandon the in-progress stage, revert to pre-stage state, and commit the reversion?
- The `full-autonomous` mode skips Document on non-epic/module tasks. But the Document stage for tasks is often trivial (confirming existing wiki knowledge). Is there a `conditional-document` mode that runs Document only when no existing wiki page covers the topic?
- How should the work loop handle tasks where the next stage's quality gate will definitively fail? If a task's scaffold stage requires type definitions but there are no types to define (it is a pure shell script), the quality gate "types compile" does not apply. Is there a mechanism to mark stage gates as N/A for specific tasks?
- Should the completion log in `wiki/log/` be structured (YAML) or unstructured (prose)? Structured logs could be queried programmatically to produce session summaries and performance metrics. Prose logs are more readable for human review.

## Relationships

- DERIVED FROM: [[Stage-Gate Methodology]] (execution modes control which stages run; quality gates are stage transition requirements)
- DERIVED FROM: [[Task Lifecycle Stage-Gating]] (the work loop implements the stage-by-stage execution pattern)
- BUILDS ON: [[Backlog Hierarchy Rules]] (the work loop reads the hierarchy to find the next task)
- BUILDS ON: [[Task Type Artifact Matrix]] (type determines which stages the loop executes)
- IMPLEMENTS: [[Plan Execute Review Cycle]] (semi-autonomous mode implements review as a first-class phase; autonomous mode implements continuous execute cycle)
- RELATES TO: [[Infrastructure as Code Patterns]] (git management rules as infrastructure — the commit convention IS the enforcement layer)
- RELATES TO: [[Wiki Backlog Pattern]] (the work loop writes to the wiki backlog — step 6, 8, 11, 12)
- RELATES TO: [[Four-Project Ecosystem]] (OpenFleet uses work_mode + budget monitor as the parallel system; OpenArms uses execution modes + end conditions)
- FEEDS INTO: [[Immune System Rules]] (the work loop structure defines what "correct behavior" looks like; deviations are the diseases the immune system detects)
- ENABLES: [[Knowledge Evolution Pipeline]] (autonomous + backlog-empty enables the self-sustaining loop that continuously improves the system)

## Backlinks

[[[[Stage-Gate Methodology]] (execution modes control which stages run; quality gates are stage transition requirements)]]
[[[[Task Lifecycle Stage-Gating]] (the work loop implements the stage-by-stage execution pattern)]]
[[[[Backlog Hierarchy Rules]] (the work loop reads the hierarchy to find the next task)]]
[[[[Task Type Artifact Matrix]] (type determines which stages the loop executes)]]
[[[[Plan Execute Review Cycle]] (semi-autonomous mode implements review as a first-class phase; autonomous mode implements continuous execute cycle)]]
[[[[Infrastructure as Code Patterns]] (git management rules as infrastructure — the commit convention IS the enforcement layer)]]
[[[[Wiki Backlog Pattern]] (the work loop writes to the wiki backlog — step 6, 8, 11, 12)]]
[[[[Four-Project Ecosystem]] (OpenFleet uses work_mode + budget monitor as the parallel system; OpenArms uses execution modes + end conditions)]]
[[[[Immune System Rules]] (the work loop structure defines what "correct behavior" looks like; deviations are the diseases the immune system detects)]]
[[[[Knowledge Evolution Pipeline]] (autonomous + backlog-empty enables the self-sustaining loop that continuously improves the system)]]
[[Model: Methodology]]
