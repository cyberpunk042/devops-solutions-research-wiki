---
title: "Stage-Gate Methodology"
type: concept
layer: 2
domain: devops
status: synthesized
confidence: authoritative
created: 2026-04-09
updated: 2026-04-10
maturity: growing
derived_from:
  - "Task Lifecycle Stage-Gating"
  - "Spec-Driven Development"
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
tags: [stage-gate, methodology, openarms, openfleet, document, design, scaffold, implement, test, hard-boundaries, artifacts, quality-gates, readiness, work-modes, knowledge-work, devops, autonomous-agents]
---

# Stage-Gate Methodology

## Summary

Stage-Gate Methodology is the 5-stage sequential system — Document → Design → Scaffold → Implement → Test — that governs all task execution in the OpenArms project and maps directly onto OpenFleet's CONVERSATION → ANALYSIS → INVESTIGATION → REASONING → WORK model. The core invariant is that stages have HARD BOUNDARIES: an agent executing the Document stage may not produce implementation artifacts, and an agent in the Scaffold stage may not implement business logic. This is not a guideline — it is a structural constraint enforced by protocol, commit convention, and MCP tooling depending on the system. The methodology applies universally: code, knowledge work, research, infrastructure planning, wiki pages, and documentation.

> [!info] Stage System Reference Card
>
> | Stage | Readiness | Required Artifacts | Forbidden | Quality Gate |
> |-------|-----------|-------------------|-----------|-------------|
> | **Document** | 0–25% | Wiki page, infrastructure map, gap analysis | Implementation code, new src/ files, design decisions | Wiki page with Summary (≥30 words) + gap analysis |
> | **Design** | 25–50% | Decision doc, config shape, type sketches in docs | Implementation code, source files | Decision doc exists, path forward unambiguous |
> | **Scaffold** | 50–80% | Type definitions, .env.example, empty test files | Business logic, test implementations | Types compile, project structure reflects design |
> | **Implement** | 80–95% | Implementation filling scaffolded stubs, passing lint | Restructuring scaffold, scope additions | Code compiles, type checks pass, lint clean |
> | **Test** | 95–100% | Test implementations, passing suite, no regressions | Skipping to "done" | All tests pass, no regressions, readiness = 100 |

## Key Insights

> [!warning] Stages have HARD boundaries, not soft guidance
> The Document stage explicitly prohibits writing implementation code. The Design stage prohibits code (type sketches in docs only). The Scaffold stage prohibits business logic. These are not stylistic preferences — violation produces a fundamentally different artifact category that corrupts the stage system. **The primary failure mode of autonomous agents is phase conflation, not incompetence.** An agent allowed to produce implementation during Document will write coherent-looking code that solves the wrong problem — it was solving while still understanding.

> [!abstract] Readiness is a gate, not a metric
> Each stage has an explicit readiness range. A task with `stages_completed: [document, design]` cannot report readiness above 50% regardless of how much additional work was done. Readiness is derived from stage completion evidence, not subjective assessment.

**One commit per stage transforms git into a ledger.** The conventional commit format `feat(wiki): T0XX stage-name — description` makes stage boundaries visible in version control. A commit titled `implement` that touches wiki pages instead of src/ files is visibly wrong in the diff. Stages are not just tracked in frontmatter — they are embedded in the repository's DNA.

**Quality gates are transition requirements, not post-hoc checks.** Each stage gate must pass before advancing. Gates are verified by rereading the task file after stage completion, not by automated tooling alone. Max 2 retries per stage before escalating to human review — preventing infinite loops on failing stages.

> [!tip] This methodology applies to knowledge work, not just code
> Wiki ingestion follows the same stages. Research follows the same stages. Infrastructure planning follows the same stages. The hard boundary principle holds universally: decisions cannot be made before understanding is complete, skeletons cannot be built before decisions are made, implementation cannot begin before the skeleton defines the contract.

## Deep Analysis

### The Five Stages — Detailed Reference

> [!example]- Stage 1: Document (Readiness 0–25%)
>
> **Purpose:** Understand the problem before making any decisions about solutions.
>
> | Aspect | Details |
> |--------|---------|
> | **Required** | Wiki page, infrastructure map, gap analysis |
> | **Forbidden** | Implementation code, new src/ files, design decisions |
> | **Permitted** | Wiki/doc files, reading code, identifying gaps, asking questions |
> | **Gate** | Wiki page with Summary ≥30 words + gap analysis, reachable from _index.md |
>
> **OpenFleet mapping:** CONVERSATION + ANALYSIS. OpenFleet separates PO conversation from codebase analysis; OpenArms merges them because PO directives are pre-written in wiki/log/.
>
> **Key distinction:** This stage builds a model of reality — what exists and what is missing. Not a proposal for what should exist.

> [!example]- Stage 2: Design (Readiness 25–50%)
>
> **Purpose:** Make decisions. Explore options and commit to one.
>
> | Aspect | Details |
> |--------|---------|
> | **Required** | Decision doc, config shape, type sketches in documentation |
> | **Forbidden** | Implementation code, source files, proceeding without committed decision |
> | **Permitted** | Type sketches in docs, comparing approaches, referencing architecture |
> | **Gate** | Decision doc exists, config shape defined, path forward unambiguous |
>
> **OpenFleet mapping:** INVESTIGATION + REASONING. OpenFleet requires all specialist contributions (QA, architect, security) before plan finalization.
>
> **Key distinction:** Making decisions under uncertainty, not eliminating uncertainty. "We will use X because Y" is complete. "We could use X or Y" is incomplete.

> [!example]- Stage 3: Scaffold (Readiness 50–80%)
>
> **Purpose:** Create the skeleton. Zero behavior.
>
> | Aspect | Details |
> |--------|---------|
> | **Required** | Compiling type definitions, .env.example, empty test files with describe blocks |
> | **Forbidden** | Business logic, test implementations, anything beyond defining shapes |
> | **Permitted** | Types, interfaces, empty stubs, test structure, config entries |
> | **Gate** | Types compile, .env entries added, empty tests exist, zero behavior |
>
> **OpenFleet mapping:** Implicit in REASONING plan. OpenArms makes skeleton creation an explicit stage because it is a distinct activity from design.
>
> **Key distinction:** Shape without substance. After scaffold, you know exactly what to implement (signatures and test cases exist) but nothing works yet. This transforms a design decision into an implementation contract.

> [!example]- Stage 4: Implement (Readiness 80–95%)
>
> **Purpose:** Write the code. Fill in the logic.
>
> | Aspect | Details |
> |--------|---------|
> | **Required** | Implementation filling scaffolded stubs, passing type checks, passing lint |
> | **Forbidden** | Restructuring scaffold, scope additions, marking done before Test |
> | **Constraint** | Build on scaffold, follow design doc, keep changes additive |
> | **Gate** | Code compiles, type checks pass, lint clean |
>
> **OpenFleet mapping:** WORK (fleet_read_context → fleet_task_accept → fleet_commit(s) → fleet_task_complete). The key addition: fleet_task_accept — plan submission before commits allowed.
>
> **Key distinction:** First stage producing executable code. Everything before was groundwork. "Build on scaffold, follow design doc" is why earlier stages exist — they are the contract Implement fulfills.

> [!example]- Stage 5: Test (Readiness 95–100%)
>
> **Purpose:** Write tests. Verify behavior. Ensure no regressions.
>
> | Aspect | Details |
> |--------|---------|
> | **Required** | Test implementations in scaffolded files, passing suite, no regressions |
> | **Constraint** | Fill scaffolded test files (not create new ones), fix all failures |
> | **Gate** | All tests pass, no regressions, all stages in stages_completed, readiness = 100 |
>
> **OpenFleet mapping:** Part of WORK, but QA criteria are provided by the QA agent BEFORE the engineer implements (plan_quality.py).
>
> **Key distinction:** Test is mandatory, not optional cleanup. Scaffold creates empty test files deliberately so Test has a defined scope — the test cases defined in Scaffold constrain what implementation is required.

### Cross-System Stage Mapping

> [!info] OpenArms ↔ OpenFleet Comparison
>
> | OpenArms | Readiness | OpenFleet | Key Difference |
> |----------|-----------|-----------|---------------|
> | Document | 0–25% | CONVERSATION + ANALYSIS | OpenFleet separates PO conversation from codebase analysis |
> | Design | 25–50% | INVESTIGATION + REASONING | OpenFleet adds multi-agent contribution convergence |
> | Scaffold | 50–80% | (implicit in REASONING) | OpenArms makes skeleton creation explicit |
> | Implement | 80–95% | WORK | Both require code + lint passing |
> | Test | 95–100% | (part of WORK) | OpenArms makes test a mandatory separate stage |
>
> **Key structural difference:** OpenFleet uses MCP tool blocking as infrastructure-level enforcement (fleet_commit blocked in CONVERSATION). OpenArms uses protocol-level enforcement (MUST NOT) + commit convention as audit trail. OpenFleet's approach is stronger (impossible to violate) but requires custom tooling infrastructure.

### Hard Boundaries as File-System Observable Categories

> [!abstract] Each stage's output is categorically different
>
> | Stage | Output Category | Violation Detection |
> |-------|----------------|-------------------|
> | Document | `.md` files only (wiki, docs) | Commit touching src/ = visible violation |
> | Design | `.md` files only (type sketches as documentation) | Source files = visible violation |
> | Scaffold | Type files, empty tests, .env, stubs — zero behavior | Business logic functions = visible violation |
> | Implement | Implementation code, scaffolded stubs filled | Restructuring scaffold = visible violation |
> | Test | Test implementations in scaffolded test files | Skipping = incomplete stages_completed |

### Universality: Beyond Code

> [!example]- Stage gates applied to three non-code domains
>
> **Wiki ingestion task:**
>
> | Stage | Action |
> |-------|--------|
> | Document | Read source, understand domain, map to existing wiki knowledge |
> | Design | Decide pages to create, relationships to draw, synthesis approach |
> | Scaffold | Page skeletons with frontmatter and headers, no content |
> | Implement | Fill in content — Deep Analysis, Key Insights, Relationships |
> | Test | Validate frontmatter, cross-references, run pipeline post |
>
> **Infrastructure planning:**
>
> | Stage | Action |
> |-------|--------|
> | Document | Understand current infra, map what exists, identify gaps |
> | Design | Decide target architecture, document the decision |
> | Scaffold | IaC file structure, empty modules, placeholder configs |
> | Implement | Write IaC, fill in module logic |
> | Test | Apply in test environment, verify behavior |
>
> **Team process improvement:**
>
> | Stage | Action |
> |-------|--------|
> | Document | Understand current process, map pain points |
> | Design | Decide process change, document new procedure |
> | Scaffold | Template documents, checklists, empty workflows |
> | Implement | Run new process on real task, fill templates |
> | Test | Retrospect — did the process improve outcomes? |

### Enforcement Mechanisms — Comparative

> [!info] Defense in depth across implementations
>
> | Mechanism | OpenArms | OpenFleet | Strength |
> |-----------|----------|-----------|---------|
> | Protocol instructions (CLAUDE.md) | Primary | Supplementary | Works immediately; can degrade with context |
> | MCP tool blocking | N/A | Primary for CONVERSATION/WORK | Structural — impossible to violate |
> | One-commit-per-stage | Core convention | Not used | Creates auditable git ledger |
> | Immune system detection | N/A | 4/11 diseases implemented | Self-correcting after violation |
> | Readiness range enforcement | Core protocol | Readiness score drives gates | Observable in task frontmatter |
> | Quality gates per stage | Verified post-stage | plan_quality.py at accept | Prevents advancement without evidence |
>
> **Practical recommendation:** Start with protocol enforcement (CLAUDE.md MUST/MUST NOT) and one-commit-per-stage. Add MCP tool blocking when infrastructure investment is justified. The combination provides defense in depth.

## Open Questions

- What is the minimum viable quality gate for each stage in a low-tooling context? The current quality gates assume a wiki and git history. For teams without this infrastructure, what observable evidence proves each stage was completed?
- How should stages handle tasks that require discovery? Some implementations reveal requirements that invalidate the design. The methodology allows max 2 retries per stage, but does not specify what happens when the design must be fundamentally revised after implementation begins. Does this require returning to Design stage?
- Can the stage-gate system be applied retroactively to partially-complete work? If a task exists that was implemented without a design stage, is it better to document retroactively (creating the artifact after the fact) or to treat the existing work as a "Document" artifact and re-plan from Design?
- How does the readiness range interact with partial stage completion? If a design doc exists but the config shape is still undefined, is the task at 26% (Document complete, Design begun) or still at 25% (Design not yet complete enough to cross the threshold)?

## Relationships

- DERIVED FROM: [[Task Lifecycle Stage-Gating]] (this page operationalizes the stage-gating concept for the devops domain)
- DERIVED FROM: [[Spec-Driven Development]] (stages enforce the spec-before-implementation principle)
- BUILDS ON: [[Plan Execute Review Cycle]] (stage gates implement the phase separation that PER describes)
- IMPLEMENTS: [[Scaffold → Foundation → Infrastructure → Features]] (SFIF is the architectural expression of the same staged progression principle)
- USED BY: [[Task Type Artifact Matrix]] (each task type selects a subset of stages based on complexity)
- USED BY: [[Backlog Hierarchy Rules]] (tasks are the unit that stages apply to; epics and modules aggregate stage completion upward)
- USED BY: [[Execution Modes and End Conditions]] (execution modes control which stages run and in what order)
- RELATES TO: [[Wiki Backlog Pattern]] (the wiki IS the Document/Design stage artifact system)
- RELATES TO: [[Four-Project Ecosystem]] (all four projects in the ecosystem apply this methodology)
- FEEDS INTO: [[Immune System Rules]] (violations of stage hard boundaries are the diseases the immune system detects)

## Backlinks

[[Task Lifecycle Stage-Gating]]
[[Spec-Driven Development]]
[[Plan Execute Review Cycle]]
[[Scaffold → Foundation → Infrastructure → Features]]
[[Task Type Artifact Matrix]]
[[Backlog Hierarchy Rules]]
[[Execution Modes and End Conditions]]
[[Wiki Backlog Pattern]]
[[Four-Project Ecosystem]]
[[Immune System Rules]]
[[Adoption Guide — How to Use This Wiki's Standards]]
[[Decision: Execution Mode Edge Cases]]
[[Decision: Hooks Design Decisions]]
[[Decision: Methodology Framework Design Decisions]]
[[Decision: Stage-Gate Operational Decisions]]
[[Decision: Task Type Edge Cases]]
[[Infrastructure Must Be Reproducible, Not Manual]]
[[LLM Wiki Standards — What Good Looks Like]]
[[Methodology Framework]]
[[Methodology Is a Framework, Not a Fixed Pipeline]]
[[Model: Methodology]]
[[Never Skip Stages Even When Told to Continue]]
[[Never Synthesize from Descriptions Alone]]
[[Shallow Ingestion Is Systemic, Not Isolated]]
[[The Agent Must Practice What It Documents]]
