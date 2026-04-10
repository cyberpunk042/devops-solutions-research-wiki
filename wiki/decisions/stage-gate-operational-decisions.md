---
title: "Decision: Stage-Gate Operational Decisions"
type: decision
domain: devops
layer: 6
status: synthesized
confidence: medium
maturity: seed
derived_from:
  - "Stage-Gate Methodology"
  - "Task Lifecycle Stage-Gating"
  - "Backlog Hierarchy Rules"
reversibility: easy
created: 2026-04-10
updated: 2026-04-10
sources: []
tags: [stage-gate, readiness, discovery, minimum-viable, retroactive, design-decisions]
---

# Decision: Stage-Gate Operational Decisions

## Summary

Eleven operational questions from Stage-Gate Methodology, Task Lifecycle Stage-Gating, and Backlog Hierarchy Rules — the mechanics of how stage gates work in edge cases. Minimum viable gating for solo developers, automatic readiness computation, discovery-driven tasks, retroactive staging, partial completion, sub-module readiness weighting, and epic review in solo context.

> [!success] Resolved decisions
>
> | Question | Decision | Source Page |
> |----------|----------|------------|
> | Minimum viable stage-gating (solo, no MCP) | CLAUDE.md MUST/MUST NOT + one-commit-per-stage. Protocol enforcement works immediately. | Stage-Gate Methodology |
> | Automatic readiness from artifacts | Yes — check `artifacts` field paths against filesystem. Flag mismatches. | Task Lifecycle Stage-Gating |
> | Discovery tasks (requirements emerge during implementation) | Return to Design stage. Max 2 retries applies. If design fundamentally changes, create new task. | Stage-Gate Methodology |
> | Retroactive staging on partial work | Document retroactively (create the artifact after the fact). Better late documentation than none. | Stage-Gate Methodology |
> | Partial stage completion (design doc exists but config shape undefined) | Still at previous stage threshold. 25% until Design is COMPLETE, not just started. | Stage-Gate Methodology |
> | Sub-module readiness weighting | Simple average — all tasks equal. Complexity is captured by having more tasks, not by weighting. | Backlog Hierarchy Rules |
> | Epic review trigger (solo context) | Agent sets to `review`, logs what was done, stops. Next session, operator reviews log and confirms. | Backlog Hierarchy Rules |
> | Weighted readiness for complex tasks | No weighting. More stages = more granular readiness already. | Backlog Hierarchy Rules |
> | New task reduces parent readiness | Yes — this is correct behavior. Honest readiness is better than inflated readiness. | Backlog Hierarchy Rules |
> | Spec quality automation | Partial — check for required fields (verbatim ref, acceptance criteria) via lint. Content quality requires human judgment. | Spec-Driven Development |
> | Minimum viable spec for small tasks | Task type determines spec scope. `task` type = scaffold IS the spec. `spike` = design doc. `module` = full spec. | Spec-Driven Development |

## Decision

**Minimum viable stage-gating: protocol + commits.** A solo developer with no MCP infrastructure uses CLAUDE.md MUST/MUST NOT rules and one-commit-per-stage. This is OpenArms' model. The audit trail is the git log — each commit named after its stage. When context degrades, the protocol may weaken, but the commit convention persists in the repository permanently.

**Readiness is computed, not self-reported.** An agent should not say `readiness: 82` — it should check: `stages_completed` has scaffold + implement → readiness is at least 80. The `artifacts` field lists file paths → check that those files exist on disk. If they don't, the readiness is a lie. A lint extension that compares `artifacts` paths against the filesystem would catch this automatically.

> [!tip] Discovery tasks: return to Design, don't force-fit
> When implementation reveals requirements that invalidate the design, the correct response is to return to the Design stage. The max-2-retries rule applies per stage. If the design changes fundamentally (not just a refinement), the task should be split: current task captures the discovery as a Document artifact, a new task implements the revised design.

**Retroactive staging is better than none.** If a task was implemented without a design stage, document retroactively — create the artifact after the fact. This is not ideal (the artifact is post-hoc rationalization, not pre-hoc guidance), but it's better than leaving the stage permanently empty. The retroactive document should be marked as such: `(retroactive — created after implementation)`.

**Simple average for readiness, no weighting.** Complex tasks should be decomposed into more sub-tasks, not given higher weight. If a module has one easy task and one hard task, the hard task should be 3 sub-tasks. The readiness average then naturally reflects the true state. Weighting adds complexity without adding information.

**Epic review in solo context: log + stop.** The agent sets the epic to `review`, writes a completion log to `wiki/log/`, and stops the session. The next session starts with the operator reading the log and deciding: confirm done, or identify gaps that need new tasks. The log IS the review artifact.

## Alternatives

### Alternative: Weighted readiness by task complexity

> [!warning] Rejected — complexity is captured by decomposition, not by weighting
> A weighting system requires defining "complexity" per task — which is subjective and adds metadata overhead. Better: decompose complex work into more tasks. A task estimated at XL should be a module with 3-5 tasks. The average then works correctly.

### Alternative: Skip retroactive staging on legacy work

> [!warning] Rejected — even post-hoc documentation has value
> Leaving stages permanently empty means the audit trail has gaps that can never be closed. Post-hoc documentation may not have guided the implementation, but it documents WHAT WAS BUILT and WHY — useful for future maintainers. Mark it as retroactive so the provenance is clear.

## Rationale

All decisions favor simplicity and honesty. Simple average over weighted. Computed readiness over self-reported. Return to Design over force-fitting. Retroactive documentation over permanent gaps. The stage-gate system's value comes from HONESTY about where work stands, not from sophisticated readiness calculations.

## Reversibility

All easy. These are interpretive guidelines for an existing system. None require schema changes or tooling modifications.

## Dependencies

- [[Stage-Gate Methodology]] — resolves 4 of its open questions
- [[Task Lifecycle Stage-Gating]] — resolves 3 of its open questions
- [[Backlog Hierarchy Rules]] — resolves 4 of its open questions
- [[Spec-Driven Development]] — resolves 2 of its open questions

## Relationships

- DERIVED FROM: [[Stage-Gate Methodology]]
- DERIVED FROM: [[Task Lifecycle Stage-Gating]]
- DERIVED FROM: [[Backlog Hierarchy Rules]]
- BUILDS ON: [[Spec-Driven Development]]
- RELATES TO: [[Decision: Execution Mode Edge Cases]]

## Backlinks

[[Stage-Gate Methodology]]
[[Task Lifecycle Stage-Gating]]
[[Backlog Hierarchy Rules]]
[[Spec-Driven Development]]
[[Decision: Execution Mode Edge Cases]]
