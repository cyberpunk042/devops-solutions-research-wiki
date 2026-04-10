---
title: "Task Lifecycle Stage-Gating"
type: concept
layer: 2
maturity: growing
domain: ai-agents
status: synthesized
confidence: authoritative
created: 2026-04-09
updated: 2026-04-10
sources:
  - id: src-openfleet-methodology-scan
    type: documentation
    file: raw/articles/openfleet-methodology-scan.md
    title: "OpenFleet Methodology Scan — Deep Research Findings"
    ingested: 2026-04-09
  - id: src-openarms-methodology-scan
    type: documentation
    file: raw/articles/openarms-methodology-scan.md
    title: "OpenArms Methodology Scan — Deep Research Findings"
    ingested: 2026-04-09
tags: [stage-gating, task-lifecycle, methodology, phase-boundaries, anti-corruption, mcp-tools, sfif, openfleet, openarms, autonomous-agents, readiness-score, one-commit-per-stage, work-modes]
---

# Task Lifecycle Stage-Gating

## Summary

Task lifecycle stage-gating is the practice of partitioning autonomous agent work into sequential, bounded phases with hard boundaries between them — where the agent cannot proceed to the next phase without producing a concrete artifact that proves the current phase was completed. Surveyed across OpenFleet's 5-stage CONVERSATION→ANALYSIS→INVESTIGATION→REASONING→WORK model (enforced via MCP tool blocking), OpenArms' 5-stage Document→Design→Scaffold→Implement→Test model (enforced via protocol instructions and one-commit-per-stage), and the SFIF recursive pattern, the core insight is identical: **the primary failure mode of autonomous agents is phase conflation, not incompetence.** Agents that are allowed to jump between phases produce coherent but misaligned work. Structural stage gates make the failure mode impossible rather than merely discouraged.

> [!info] Enforcement Comparison Reference Card
>
> | Mechanism | OpenFleet | OpenArms | Strength |
> |-----------|----------|----------|----------|
> | MCP tool blocking | Primary (fleet_commit blocked by stage) | N/A | Impossible to violate |
> | Protocol instructions | Supplementary | Primary (CLAUDE.md MUST/MUST NOT) | Works with any runtime |
> | One-commit-per-stage | Not used | Core convention | Immutable audit trail |
> | Immune system teaching | 3-strike + teaching.py | N/A | Self-correcting |
> | Human review gate | fleet-ops 7-step | Optional (`--review`) | Highest fidelity |

## Key Insights

> [!warning] Phase conflation is the root failure mode — not incompetence
> Without stage gates, agents implement while still understanding, or reason while still analyzing. The result is not bad code — it is good code that implements the wrong thing. OpenFleet's disease catalogue documents this as "scope_creep", "abstraction", "code_without_reading" — all forms of phase conflation. The gate makes this failure mode structurally impossible rather than merely discouraged.

> [!abstract] Two enforcement strategies, same goal
>
> | Strategy | How It Works | Trade-off |
> |----------|-------------|-----------|
> | **Structural** (OpenFleet) | MCP tools blocked outside valid stages | Impossible to violate; requires custom infrastructure |
> | **Protocol** (OpenArms) | CLAUDE.md MUST/MUST NOT + one-commit-per-stage | Portable, works immediately; can degrade with context |
>
> **Practical recommendation:** Start with protocol enforcement. Add structural when infrastructure investment is justified. The combination provides defense in depth.

**Readiness score is a continuous gate.** 0-25 = Document, 25-50 = Design, 50-80 = Scaffold, 80-95 = Implement, 95-100 = Test. Readiness 100 = done only if all required stages are in `stages_completed`. The human gate (PO confirmation at readiness 99) is built into the score model, not added on top.

**Stage boundaries are file-system boundaries.** Document stage = wiki pages only (no src/). Design = type sketches in docs only. Scaffold = types and empty tests, zero business logic. These are observable in the file system — a commit touching src/ during Document is visibly wrong.

**Task types select stage subsets.** `docs` = Document only. `spike` = Document + Design. `task` = Scaffold + Implement + Test. `epic/module` = all five. This prevents over-process for simple work while enforcing full staging for complex work.

**Autonomy is parametric, not binary.** Full-autonomous (skip document, no human review) to plan-only (design doc, stop). The stage-gating framework is adoptable at different maturity levels.

## Deep Analysis

### OpenFleet: 5-Stage CONVERSATION→WORK Model

OpenFleet's methodology is the most formally specified of the surveyed systems. Every task progresses through exactly these stages:

**1. CONVERSATION** (understand the requirement)
- MUST: Discuss, ask specific questions, identify gaps, propose understanding
- MUST NOT: Write code, commit, create PRs, produce finished deliverables
- Advance when: PO confirms understanding, verbatim requirement is populated
- Gate: `fleet_commit` is blocked in this stage only

**2. ANALYSIS** (examine what exists)
- MUST: Read and examine codebase, produce analysis document with file references
- MUST NOT: Produce solutions (that is REASONING's job), write implementation code
- Produces: Analysis documents, current state assessments, gap analysis

**3. INVESTIGATION** (research what's possible)
- MUST: Research solutions, explore MULTIPLE options (minimum 3), cite sources
- MUST NOT: Decide on approach (that is REASONING), write implementation code
- Produces: Research findings, option comparisons with tradeoffs

**4. REASONING** (plan the approach)
- MUST: Decide approach from all inputs, produce plan referencing verbatim
- Required: Specialist contributions arrive here before WORK
- MUST NOT: Start implementing, commit code
- Quality check: `plan_quality.py` validates plan at this stage

**5. WORK** (execute the confirmed plan)
- Required tool sequence: `fleet_read_context → fleet_task_accept → fleet_commit(s) → fleet_task_complete`
- MUST NOT: Deviate from plan, add unrequested scope, skip tests
- Gate: `fleet_task_complete` is blocked in all stages except WORK

The MCP tool blocking architecture ensures these constraints are structural, not advisory. An agent cannot call `fleet_task_complete` unless the task is in WORK stage — the tool will reject the call. This makes stage compliance a property of the infrastructure, not a property of the agent's behavior.

#### The Contribution Model — Parallelism Within Stage-Gating

OpenFleet's multi-agent system introduces a sophisticated parallelism: while the primary agent progresses linearly through stages, specialist agents contribute asynchronously. The brain creates contribution subtasks when a task enters REASONING:

- QA provides predefined test criteria (TC-001 format) BEFORE the engineer implements
- Architect provides design input when the task enters REASONING
- DevSecOps provides security requirements (phase-appropriate: POC basic, production full)
- DevOps provides deployment manifest
- UX provides UX spec (all states: loading, error, empty, success, partial)

This contribution model means REASONING is a convergence point — it cannot complete until all required specialist contributions have arrived. The stage gate is not just "plan exists" but "plan exists with all required perspectives."

### OpenArms: 5-Stage Document→Test Model

OpenArms adapts OpenFleet's model for a solo agent without a PO or a live agent fleet. The key differences:

| OpenFleet Stage | OpenArms Stage | Key Difference |
|----------------|----------------|----------------|
| CONVERSATION | (merged into Document) | No PO — operator directives are pre-written in wiki/log/ |
| ANALYSIS | Document | Read code, map existing state → wiki page |
| INVESTIGATION | Design | Explore options, make decisions → design doc |
| REASONING | Scaffold | OpenArms adds scaffolding as an explicit stage |
| WORK | Implement + Test | Split into two stages: code then verify |

The critical addition is the split of WORK into Implement and Test. This prevents "I'll clean up the tests later" — Test is a mandatory stage with its own artifact requirement (passing test suite, no regressions).

#### Stage Enforcement via Commit Convention

OpenArms' one-commit-per-stage rule transforms git into an enforcement mechanism:

```
feat(wiki): T023 document — document network rules evaluation engine
feat(wiki): T023 design — design NetworkRulesConfig shape and decisions
feat(wiki): T023 scaffold — scaffold NetworkRulesConfig types and empty tests
feat(wiki): T023 implement — implement network rules evaluation logic
feat(wiki): T023 test — all tests passing, no regressions
```

If a commit titled `implement` touches wiki pages instead of src/ files, the violation is visible in the diff. If a commit titled `document` touches src/ files, the violation is visible. The stage name in the commit message creates an implicit contract about what files should be changed.

#### The Task Frontmatter as State Machine

OpenArms' task frontmatter fields form a complete state machine without any external board or MCP tool:

```yaml
status: in-progress
current_stage: implement
stages_completed: [document, design, scaffold]
readiness: 82
artifacts:
  - wiki/domains/architecture/network-rules-config-design.md
  - src/types/network-rules.ts
  - src/network-rules.test.ts
```

The `readiness` field is derived from `stages_completed` and the task type's required stages. Setting `readiness: 100` with missing `stages_completed` entries is an absolute prohibition. The frontmatter itself is the gate: you cannot claim completion without the evidence in the file.

### The Auto-Loop: Stage-Gating as Recursive Self-Application

OpenArms' infinite auto-loop is the most elegant demonstration of stage-gating: the agent uses the methodology to build the features that make the methodology better. The loop:

1. Read CLAUDE.md → methodology.yaml → agent-directive.md → backlog/_index.md
2. Pick highest priority task (filter: epic/module scope, priority, dependencies; skip: done/archived/blocked)
3. Determine next required stage from methodology.yaml task_types
4. Read stage protocol from methodology.yaml
5. Execute ONLY that stage — produce ONLY the artifacts for that stage
6. Update task frontmatter (current_stage, stages_completed, readiness, artifacts, status)
7. Git: stage and commit ALL changed files — ONE COMMIT PER STAGE
8. VERIFY: re-read task file, confirm frontmatter is correct
9. If more stages remain, go to step 3
10. When all stages complete: set status "done", readiness 100

The loop is self-referential: the agent applies the same stage protocol to tasks that improve the stage protocol. This is the clearest expression of stage-gating as a methodology, not just a process.

### Comparison: Structural vs. Protocol Enforcement

The most important architectural question in stage-gating is **enforcement mechanism**:

| Enforcement Type | OpenFleet | OpenArms | Strength | Weakness |
|-----------------|-----------|----------|----------|---------|
| MCP tool blocking | Yes | No | Makes violation impossible | Requires custom MCP infrastructure |
| Protocol instructions (CLAUDE.md) | Yes (supplementary) | Yes (primary) | Works with any agent runtime | Agent can violate if context is degraded |
| One-commit-per-stage | No | Yes | Creates auditable trail | Requires commit discipline |
| Immune system teaching | Yes | No | Self-correcting | Requires disease detection infrastructure |
| Human review gate | Yes (fleet-ops) | Optional | Highest fidelity | Removes autonomy |

The practical conclusion: structural enforcement (MCP blocking) is the gold standard but requires infrastructure investment. Protocol enforcement (CLAUDE.md instructions) is the pragmatic baseline that works immediately. The combination produces defense in depth — multiple layers catch what the others miss.

### Relationship to the Scaffold → Foundation → Infrastructure → Features

The SFIF (Scaffold → Foundation → Infrastructure → Features) pattern from OpenFleet's PO requirements applies stage-gating at the architectural level, not just the task level. It is not a contradiction of the task-level model — it is the same principle applied recursively. Just as a task cannot be "Implement" until "Document" and "Design" are complete, a system cannot be "Features" until "Scaffold", "Foundation", and "Infrastructure" are in place. Stage-gating composes fractally: stages within tasks, stages within projects, stages within architectures.

### The Disease Catalogue as Stage-Gating Failure Modes

> [!bug]- Stage-gating failures mapped to OpenFleet diseases
>
> | Disease | Stage Violation | What Happened |
> |---------|----------------|---------------|
> | `abstraction` | Planning during WORK | Reasoning at the wrong level |
> | `code_without_reading` | WORK without ANALYSIS | Skipped understanding phase |
> | `scope_creep` | WORK exceeding REASONING | Added scope not in verbatim |
> | `cascading_fix` | No gate to pause and re-plan | Fix breaks thing, fix that, spiral |
> | `context_contamination` | Stage boundary not cleaned | Previous task's context bleeds in |
> | `not_listening` | MUST NOT instructions ignored | Protocol enforcement failing |
> | `compression` | Interpretation entering reproduction | Paraphrasing verbatim (stage-crossing) |
> | `contribution_avoidance` | WORK without specialist inputs | Skipped REASONING convergence |
> | `synergy_bypass` | Same as above | Not waiting for contributions |
>
> Each disease is a case study in what stage gates prevent. The teaching system re-enforces the gate after violation — gates are not just structural, they are learned.

## Open Questions

- What is the minimum viable stage-gating system for a solo developer with no MCP infrastructure? OpenArms' protocol-based approach is the clearest answer, but it depends on agent context quality. When context is compressed or degraded, does the protocol hold?
- Can readiness scores be computed automatically from artifact inspection rather than agent self-report? An agent that marks readiness 82 when the design doc does not exist is the primary failure mode. Static analysis of the artifacts field against the filesystem would catch many violations.
- At what task complexity does the overhead of stage-gating become net-negative? OpenArms acknowledges this with the `full-autonomous` mode (skip document stage on tasks, no human review). The crossover point between "stage gating adds more value than friction" and "stage gating is overkill" is empirically unknown.
- How should stage-gating handle tasks that require discovery? Some tasks cannot be fully specified in REASONING because the implementation reveals requirements. The SFIF pattern handles this at the architectural level; it is less clear how the task-level model handles it.

## Relationships

- BUILDS ON: [[Rework Prevention]] (stage gates prevent the root causes of rework)
- BUILDS ON: [[Spec-Driven Development]] (specs are the artifact produced at stage boundaries)
- IMPLEMENTS: [[Plan Execute Review Cycle]] (stage-gating is the implementation of phase separation)
- RELATES TO: [[Immune System Rules]] (disease catalogue documents stage-gating failure modes)
- RELATES TO: [[OpenFleet]] (primary source — 5-stage model, MCP blocking, teaching system)
- RELATES TO: [[Agent Orchestration Patterns]] (multi-agent systems require stage-gating to coordinate contribution flow)
- RELATES TO: [[Scaffold → Foundation → Infrastructure → Features]] (stage-gating applied at architectural scale)
- FEEDS INTO: [[Wiki Backlog Pattern]] (task frontmatter as state machine is the wiki implementation of stage-gating)
- FEEDS INTO: [[Spec-Driven Development]] (stages enforce spec phase before implementation phase)
- CONTRADICTS: [[Task Lifecycle Stage-Gating]] (unstructured iterative coding without phase checkpoints)

## Backlinks

[[Rework Prevention]]
[[Spec-Driven Development]]
[[Plan Execute Review Cycle]]
[[Immune System Rules]]
[[OpenFleet]]
[[Agent Orchestration Patterns]]
[[Scaffold → Foundation → Infrastructure → Features]]
[[Wiki Backlog Pattern]]
[[Task Lifecycle Stage-Gating]]
[[Execution Modes and End Conditions]]
[[Hooks Lifecycle Architecture]]
[[Methodology Framework]]
[[Per-Role Command Architecture]]
[[Stage-Gate Methodology]]
[[Task Type Artifact Matrix]]
