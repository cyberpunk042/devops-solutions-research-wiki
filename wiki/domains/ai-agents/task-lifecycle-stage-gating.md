---
title: "Task Lifecycle Stage-Gating"
type: concept
domain: ai-agents
status: synthesized
confidence: authoritative
created: 2026-04-09
updated: 2026-04-09
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

## Key Insights

- **Phase conflation is the root failure mode**: Without stage gates, agents begin implementing while still understanding the problem, or begin reasoning while still in an analysis phase. The result is not bad code — it is good code that implements the wrong thing. OpenFleet's disease catalogue documents this as "scope_creep", "abstraction", and "code_without_reading" — all forms of phase conflation.

- **Two enforcement strategies, same goal**: OpenFleet enforces stage gates at the infrastructure layer — MCP tools (`fleet_commit`, `fleet_task_complete`) are programmatically blocked outside their valid stages. OpenArms enforces at the protocol layer — CLAUDE.md instructions define what is produced at each stage, and the one-commit-per-stage rule creates a verifiable audit trail. Infrastructure blocking is stronger (impossible to violate); protocol blocking is more portable (works without custom tooling).

- **The readiness score is a continuous gate**: OpenFleet's task readiness score (0-100) drives stage progression. Critically, the REASONING→WORK transition requires PO confirmation at readiness 99 — the human gate is built into the score model, not added on top. OpenArms uses the same model: readiness 0-25 = Document, 25-50 = Design, 50-80 = Scaffold, 80-95 = Implement, 95-100 = Test. Readiness 100 = done, but only if all required stages are in `stages_completed`.

- **One commit per stage creates an immutable audit trail**: OpenArms' commit convention (`feat(wiki): T0XX stage-name — description`) transforms git history into a stage-gating ledger. Each commit is a stage checkpoint. If a task is reviewed and found incomplete, the stage regression is visible in git. This is stage-gating that persists in the repository's DNA, not just in a task board state.

- **Stage-specific MUST/MUST NOT/CAN lists are injected into agent context**: OpenFleet's brain injects stage-specific behavioral constraints into every agent context file on every 30-second cycle. The agent does not need to "remember" what it is allowed to do in ANALYSIS — it is told explicitly. This is the autocomplete chain principle applied to stage compliance: the correct behavior is the natural continuation of the context.

- **Stage boundaries are file-system boundaries in OpenArms**: In the Document stage, the agent produces wiki pages ONLY — no src/ files. In the Design stage, type sketches go in documentation files, not in code. In the Scaffold stage, the agent creates types and empty test files but writes no business logic. These are not conventions — they are observable in the file system. A commit that touches src/ during the Document stage is visibly wrong.

- **Different task types require different stage subsets**: OpenArms' methodology maps task types to required stages. A `docs` task requires only Document. A `spike` requires Document + Design. A standard `task` requires Scaffold + Implement + Test (no design stage for low-complexity implementation). An `epic/module` requires all five stages. This tiered approach prevents over-process for small work while ensuring complex work is fully staged.

- **The triple anti-corruption system**: OpenFleet deploys three lines of defense against stage violations. Line 1: MCP tool blocking (structural — impossible to commit in CONVERSATION stage). Line 2: Immune system teaching (when disease detected, inject corrective lesson via `teaching.py`). Line 3: Fleet-ops review (7-step human review against verbatim requirements). Each line catches what the previous one missed.

- **Autonomy mode controls how strictly stages are enforced**: OpenArms defines an autonomy spectrum from full-autonomous (skip document stage, no human review, backlog-empty end condition) to plan-only (produce design doc, stop). The stage-gating is not binary — it is parametric. A solo developer can choose to operate with less stage friction for simple tasks and full staging for complex ones. This makes the framework adoptable at different maturity levels.

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

### Relationship to the SFIF Pattern

The SFIF (Scaffold → Foundation → Infrastructure → Features) pattern from OpenFleet's PO requirements applies stage-gating at the architectural level, not just the task level. It is not a contradiction of the task-level model — it is the same principle applied recursively. Just as a task cannot be "Implement" until "Document" and "Design" are complete, a system cannot be "Features" until "Scaffold", "Foundation", and "Infrastructure" are in place. Stage-gating composes fractally: stages within tasks, stages within projects, stages within architectures.

### The Disease Catalogue as Stage-Gating Failure Modes

OpenFleet's immune system documents exactly what happens when stage gating fails. The 11 disease categories are a taxonomy of stage violations:

- `abstraction` — reasoning at the wrong level (stage conflation: planning during work)
- `code_without_reading` — WORK stage without completing ANALYSIS
- `scope_creep` — adding scope not in verbatim (WORK exceeding REASONING)
- `cascading_fix` — fixing one thing breaks another, fix that, spiral (no stage gate to pause and re-plan)
- `context_contamination` — previous task's context affecting current task (stage boundary not cleaned)
- `not_listening` — ignoring MUST NOT instructions (protocol enforcement failing)
- `compression` — paraphrasing verbatim (a form of stage-crossing: interpretation entering where only reproduction should be)
- `contribution_avoidance` — skipping the REASONING convergence point (advancing to WORK without specialist inputs)
- `synergy_bypass` — not waiting for contributions (same as above)

Each disease is a case study in what stage gates prevent. The teaching system's role is to re-enforce the stage gate after a violation — the gate is not just structural, it is learned.

## Open Questions

- What is the minimum viable stage-gating system for a solo developer with no MCP infrastructure? OpenArms' protocol-based approach is the clearest answer, but it depends on agent context quality. When context is compressed or degraded, does the protocol hold?
- Can readiness scores be computed automatically from artifact inspection rather than agent self-report? An agent that marks readiness 82 when the design doc does not exist is the primary failure mode. Static analysis of the artifacts field against the filesystem would catch many violations.
- At what task complexity does the overhead of stage-gating become net-negative? OpenArms acknowledges this with the `full-autonomous` mode (skip document stage on tasks, no human review). The crossover point between "stage gating adds more value than friction" and "stage gating is overkill" is empirically unknown.
- How should stage-gating handle tasks that require discovery? Some tasks cannot be fully specified in REASONING because the implementation reveals requirements. The SFIF pattern handles this at the architectural level; it is less clear how the task-level model handles it.

## Relationships

- BUILDS ON: Rework Prevention (stage gates prevent the root causes of rework)
- BUILDS ON: Spec-Driven Development (specs are the artifact produced at stage boundaries)
- IMPLEMENTS: Plan Execute Review Cycle (stage-gating is the implementation of phase separation)
- RELATES TO: Immune System Rules (disease catalogue documents stage-gating failure modes)
- RELATES TO: OpenFleet (primary source — 5-stage model, MCP blocking, teaching system)
- RELATES TO: Agent Orchestration Patterns (multi-agent systems require stage-gating to coordinate contribution flow)
- RELATES TO: Scaffold → Foundation → Infrastructure → Features (stage-gating applied at architectural scale)
- FEEDS INTO: Wiki Backlog Pattern (task frontmatter as state machine is the wiki implementation of stage-gating)
- FEEDS INTO: Spec-Driven Development (stages enforce spec phase before implementation phase)
- CONTRADICTS: Continuous Implementation (unstructured iterative coding without phase checkpoints)

## Backlinks

[[Rework Prevention (stage gates prevent the root causes of rework)]]
[[Spec-Driven Development (specs are the artifact produced at stage boundaries)]]
[[Plan Execute Review Cycle (stage-gating is the implementation of phase separation)]]
[[Immune System Rules (disease catalogue documents stage-gating failure modes)]]
[[OpenFleet (primary source — 5-stage model, MCP blocking, teaching system)]]
[[Agent Orchestration Patterns (multi-agent systems require stage-gating to coordinate contribution flow)]]
[[Scaffold → Foundation → Infrastructure → Features (stage-gating applied at architectural scale)]]
[[Wiki Backlog Pattern (task frontmatter as state machine is the wiki implementation of stage-gating)]]
[[Spec-Driven Development (stages enforce spec phase before implementation phase)]]
[[Continuous Implementation (unstructured iterative coding without phase checkpoints)]]
[[Hooks Lifecycle Architecture]]
[[Per-Role Command Architecture]]
