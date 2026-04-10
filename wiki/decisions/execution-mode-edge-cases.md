---
title: "Decision: Execution Mode Edge Cases"
type: decision
domain: devops
layer: 6
status: synthesized
confidence: medium
maturity: seed
derived_from:
  - "Execution Modes and End Conditions"
  - "Stage-Gate Methodology"
  - "Task Type Artifact Matrix"
reversibility: easy
created: 2026-04-10
updated: 2026-04-10
sources: []
tags: [execution-modes, quality-gates, cost-limit, stage-failure, completion-log, edge-cases, design-decisions]
---

# Decision: Execution Mode Edge Cases

## Summary

Five open questions from the Execution Modes page resolved by cross-referencing the stage-gate methodology, task type artifact matrix, and rework prevention principles. These are operational edge cases that arise during autonomous execution — what happens when quality gates fail permanently, when cost limits hit mid-stage, when stages don't apply, and how completion should be logged.

> [!success] Resolved decisions
>
> | Question | Decision | Confidence |
> |----------|----------|------------|
> | Quality gate fails after max retries | Create a `bug` task describing the failure, set parent to `blocked` | High — follows backlog hierarchy pattern |
> | Cost limit hit mid-stage | Complete current stage, commit, then stop. Never abandon mid-stage. | High — partial commits corrupt the audit trail |
> | Conditional document stage | Keep `full-autonomous` as-is. Document skip is per task type, not per topic. | Medium — simplest rule, may need revision |
> | Stage gates that don't apply (N/A) | Task frontmatter can declare `skip_gates: [types_compile]` | Medium — convention, not enforced |
> | Log format (structured vs prose) | Structured YAML frontmatter + prose body. Both queryable and readable. | High — matches wiki page schema pattern |

## Decision

**Failed quality gates → create a bug task.** When a stage's quality gate fails after max retries (default 2), the agent creates a `bug` task with: the failed gate name, the error output, the parent task ID, and the stage that was blocked. The parent task moves to `blocked` with `blocked_by: [T0XX]`. This makes the failure a trackable work item rather than a silent dead end. Cross-referencing Rework Prevention: "the correct response to an incompleteness signal is to CREATE NEW TASKS to cover the gap."

**Cost limit mid-stage → finish the stage, then stop.** The agent completes the current stage (including the commit), then stops — even if this slightly exceeds the cost limit. The alternative (abandoning mid-stage) leaves code in an inconsistent state and corrupts the one-commit-per-stage audit trail. The cost limit is a soft boundary, not a hard kill. Cross-referencing the compound cost model: rework from an inconsistent state costs more than slightly exceeding the budget.

**Keep document skip as-is.** `full-autonomous` mode skips Document on `task`, `bug`, `refactor` types — this is a type-based decision, not a content-based one. Adding a "conditional-document" mode that checks wiki coverage introduces an LLM judgment call into what should be a deterministic mode selection. If a task needs Document, use `autonomous` mode (which includes it) or promote the task to a `module` (which requires all 5 stages).

**N/A gates declared in frontmatter.** A task working on a pure shell script adds `skip_gates: [types_compile]` to its frontmatter. The work loop reads this and skips the listed gate checks. This is explicit and auditable — the skip is declared, not silently assumed. The gate still appears in `stages_completed` but the quality check is waived.

> [!tip] Log format: structured frontmatter + prose body
> Completion logs use the wiki's own page schema: YAML frontmatter (queryable by tooling) with a prose body (readable by humans). A `note` type page with `note_type: completion` in frontmatter. The pipeline can query all completion notes via frontmatter; the operator can read them as narrative.

## Alternatives

### Alternative: Hard-kill on cost limit (abandon mid-stage)

> [!warning] Rejected — violates the one-commit-per-stage invariant
> Abandoning mid-stage means uncommitted changes exist on disk without a stage checkpoint. The next session starts with an inconsistent state — the task shows `current_stage: implement` but the code is half-written. Rework cost exceeds the cost savings from stopping immediately.

### Alternative: LLM-based conditional document (check wiki coverage before deciding)

> [!warning] Rejected — introduces non-deterministic mode behavior
> Execution modes must be deterministic: given a mode + task type, the stages are known. Adding an LLM judgment ("does the wiki cover this topic?") makes the stage sequence depend on context window quality, model capability, and wiki state — all of which vary between sessions.

## Rationale

The decisions follow a consistent principle: **deterministic rules over judgment calls, explicit declarations over silent assumptions.** Failed gates create explicit bug tasks (not silent blocks). Cost limits respect stage boundaries (not arbitrary kill points). Gate skips are declared in frontmatter (not assumed from context). Log format uses the existing schema (not a new format).

## Reversibility

All easy. Frontmatter conventions, mode behavior, and log format can all be changed without data migration. The bug-task-on-failure pattern is additive — it creates information, doesn't destroy any.

## Dependencies

- [[Execution Modes and End Conditions]] — these decisions complete the open questions
- [[Stage-Gate Methodology]] — one-commit-per-stage invariant drives the cost limit decision
- [[Rework Prevention]] — compound cost model drives the "finish the stage" decision
- [[Backlog Hierarchy Rules]] — blocked_by pattern drives the bug task creation

## Relationships

- DERIVED FROM: [[Execution Modes and End Conditions]]
- BUILDS ON: [[Stage-Gate Methodology]]
- BUILDS ON: [[Rework Prevention]]
- RELATES TO: [[Backlog Hierarchy Rules]]
- RELATES TO: [[Task Type Artifact Matrix]]

## Backlinks

[[Execution Modes and End Conditions]]
[[Stage-Gate Methodology]]
[[Rework Prevention]]
[[Backlog Hierarchy Rules]]
[[Task Type Artifact Matrix]]
[[Decision: Stage-Gate Operational Decisions]]
