---
title: "Stage-Gate Methodology"
type: concept
layer: 2
domain: devops
status: synthesized
confidence: authoritative
created: 2026-04-09
updated: 2026-04-09
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

Stage-Gate Methodology is the 5-stage sequential system — Document → Design → Scaffold → Implement → Test — that governs all task execution in the OpenArms project and maps directly onto OpenFleet's CONVERSATION → ANALYSIS → INVESTIGATION → REASONING → WORK model. The core invariant is that stages have HARD BOUNDARIES: an agent executing the Document stage may not produce implementation artifacts, and an agent in the Scaffold stage may not implement business logic. This is not a guideline — it is a structural constraint enforced by protocol, commit convention, and MCP tooling depending on the system. Critically, this methodology applies universally: it governs code, knowledge work, research, infrastructure planning, wiki pages, and documentation with equal force.

## Key Insights

- **Stages have hard boundaries, not soft guidance**: The Document stage explicitly prohibits writing implementation code or creating new source files. The Design stage explicitly prohibits writing implementation code (type sketches are permitted only inside documentation files). The Scaffold stage prohibits implementing business logic. These prohibitions are not stylistic preferences — violation produces a fundamentally different artifact category that corrupts the stage system.

- **Readiness is a gate, not a metric**: Each stage has an explicit readiness range (Document: 0-25%, Design: 25-50%, Scaffold: 50-80%, Implement: 80-95%, Test: 95-100%). The readiness value must correspond to the highest completed stage — a task with `stages_completed: [document, design]` cannot report readiness above 50 regardless of how much additional work was done. Readiness is derived from stage completion evidence, not from subjective assessment.

- **Each stage has required artifacts that prove completion**: Saying a stage is done is not sufficient. Document requires: wiki page documenting the concept, mapping of existing infrastructure, gap analysis. Design requires: decision document, target config shape, interface/type sketches. Scaffold requires: type definitions, .env.example entries, example config snippets, empty test files with describe blocks. Implement requires: implementation code, passing type checks, passing lint. Test requires: test implementations, passing test suite, verification existing tests still pass.

- **The methodology applies to knowledge work, not just code**: A wiki ingestion task follows the same stages — Document (understand the source, map existing knowledge), Design (decide synthesis approach, plan page structure), Scaffold (create page skeleton with frontmatter and headers), Implement (fill in content), Test (validate schema, cross-references, relationships). Research, infrastructure planning, and architectural decisions follow the same pattern.

- **OpenFleet's 5-stage model is a parallel architecture for the same principle**: CONVERSATION (understand requirement, no code) = Document. ANALYSIS (examine codebase, produce analysis doc) = a deeper Document. INVESTIGATION (research options, no code) = Design exploration. REASONING (decide approach, produce plan) = Design finalization + Scaffold. WORK (execute confirmed plan, full tool sequence) = Implement + Test combined. The key addition in OpenArms is the explicit separation of Test as its own stage — preventing "I'll clean up the tests later."

- **One commit per stage transforms git into a stage-gating ledger**: The conventional commit format `feat(wiki): T0XX stage-name — description` makes the stage boundary visible in version control. A commit titled `implement` that touches wiki pages instead of src/ files is visibly wrong in the diff. The commit history is the audit trail — stages are not just tracked in frontmatter but embedded in the repository's DNA.

- **Quality gates are stage transition requirements, not post-hoc checks**: Each stage has a specific quality gate that must pass before advancing. Document gate: wiki page exists with Summary and gap analysis. Design gate: decision doc exists, config shape defined, types sketched in docs. Scaffold gate: types compile, .env entries added, empty test files exist. Implement gate: code compiles, lint passes. Test gate: scoped tests pass, no regressions. These gates are verified by rereading the task file after stage completion, not by automated tooling alone.

- **Max 2 retries per stage before escalating**: The default configuration allows a maximum of 2 stage retries before a stage is considered blocked. This prevents infinite loops on failing stages and surfaces systemic problems for human review.

## Deep Analysis

### The Five Stages — Complete Reference

#### Stage 1: Document (Readiness 0–25%)

**Purpose:** Understand the problem before making any decisions about solutions. Read existing code. Write wiki documentation. Map existing infrastructure. Identify gaps.

**Required artifacts:**
- Wiki page documenting the concept or feature
- Mapping of existing infrastructure that will be affected
- Gap analysis: what exists, what is missing, what is unclear

**What the protocol forbids:**
- Writing implementation code (any code in src/)
- Creating new source files
- Making design decisions

**What is permitted:**
- Creating wiki pages and documentation files
- Reading any existing code (required)
- Identifying gaps and open questions
- Asking clarifying questions

**Quality gate:** Wiki page exists with Summary (minimum 30 words) and gap analysis. The page must be reachable from the domain _index.md.

**OpenFleet mapping:** CONVERSATION (understand the requirement, ask questions, extract knowledge) + ANALYSIS (examine codebase, produce analysis document with file references). OpenFleet separates these into two stages because the multi-agent context requires a dedicated conversation phase with the PO. In OpenArms' solo-agent context, the PO directives are pre-written in wiki/log/ — there is no live conversation, so the understanding and analysis phases collapse into one.

**Key distinction:** This stage is about building a model of reality. The output is a structured representation of what exists and what is missing — not a proposal for what should exist.

---

#### Stage 2: Design (Readiness 25–50%)

**Purpose:** Make decisions. Write design docs. Define config shape. Explore multiple options and commit to one.

**Required artifacts:**
- Design decision document (in wiki/docs, not src/)
- Target config shape (what configuration values are needed, their types and defaults)
- Interface/type sketches in documentation (NOT in code files)

**What the protocol forbids:**
- Writing implementation code
- Creating source files
- Proceeding to scaffold without a committed design decision

**What is permitted:**
- Writing type sketches in documentation files
- Comparing multiple approaches with tradeoffs
- Referencing existing architecture docs

**Quality gate:** Decision doc exists. Config shape is defined. Types are sketched inside documentation files (not code). The path forward is unambiguous.

**OpenFleet mapping:** INVESTIGATION (research what's possible, explore multiple options, cite sources) + REASONING (plan the approach, create implementation plan, receive specialist contributions). OpenFleet's REASONING stage requires all specialist contributions to arrive (QA test criteria, architect design input, security requirements) before the plan is finalized. OpenArms implements this implicitly by requiring the design doc to reference all known constraints before advancing.

**Key distinction:** This stage is about making decisions under uncertainty, not eliminating uncertainty. A design doc that says "we will use X because Y and Z" is complete. A design doc that says "we could use X or Y" is incomplete.

---

#### Stage 3: Scaffold (Readiness 50–80%)

**Purpose:** Create the skeleton. Types, examples, .env entries, empty test files with describe blocks. No business logic.

**Required artifacts:**
- Type definitions (compiling)
- .env.example entries for all new configuration values
- Example config snippets
- Empty test files with describe blocks (but no implementation)

**What the protocol forbids:**
- Implementing business logic
- Filling in test implementations
- Writing code that does anything beyond defining shapes

**What is permitted:**
- Type definitions and interfaces
- Empty function stubs with correct signatures
- Test file structure (describe blocks, empty it() calls)
- .env.example entries

**Quality gate:** Types compile. .env entries are added. Empty test files exist. The project structure reflects the design decision. Running the code at this stage produces zero behavior (types only).

**OpenFleet mapping:** Partially REASONING (plan exists), but OpenArms adds the Scaffold stage explicitly because skeleton creation is a distinct activity from design decision. The skeleton is what makes the design real — it creates the file-system structure that subsequent stages build on. OpenFleet's WORK stage handles both scaffold and implementation as one unit; OpenArms' separation is the more disciplined approach.

**Key distinction:** Scaffold creates shape without substance. After scaffold, you know exactly what you will implement (the function signatures and test cases exist) but nothing works yet. This is the stage that transforms a design decision into a concrete implementation contract.

---

#### Stage 4: Implement (Readiness 80–95%)

**Purpose:** Write the code. Fill in the logic. Make it work.

**Required artifacts:**
- Implementation code (filling in the scaffolded stubs)
- Passing type checks
- Passing lint

**What the protocol requires:**
- Build on the scaffold (do not restructure)
- Follow the design document (do not deviate)
- Keep changes additive (do not remove scaffold artifacts)

**What the protocol forbids:**
- Restructuring the scaffold
- Adding scope not defined in the design doc
- Marking done before Test stage

**Quality gate:** Code compiles. Type checks pass. Lint passes. The scaffolded stubs are filled in.

**OpenFleet mapping:** WORK stage (execute the confirmed plan). In OpenFleet: `fleet_read_context → fleet_task_accept → fleet_commit(s) → fleet_task_complete`. The key OpenFleet addition is `fleet_task_accept` — submitting the plan before commits are allowed. OpenArms enforces this via the design doc requirement: you cannot reach Implement without a design doc, which serves the same purpose.

**Key distinction:** Implement is the first stage that produces executable code. Everything before this stage was groundwork. The constraint "build on the scaffold, follow the design doc" is why the earlier stages exist — they are the contract that Implement is bound to fulfill.

---

#### Stage 5: Test (Readiness 95–100%)

**Purpose:** Write tests. Verify behavior. Ensure nothing broken.

**Required artifacts:**
- Test implementations (filling in the scaffolded empty test files)
- Passing test suite
- Verification that existing tests still pass (no regressions)

**What the protocol requires:**
- Fill in the scaffolded test files (not create new ones from scratch)
- Fix all failures before marking complete
- Verify regressions explicitly

**Quality gate:** Scoped tests pass. No regressions in existing suite. All required stages in `stages_completed`. Readiness = 100.

**OpenFleet mapping:** Part of WORK stage, but OpenFleet separates this via the `plan_quality.py` QA test criteria provided by the QA agent BEFORE the engineer implements. OpenArms combines this into the final stage, which works in a solo context.

**Key distinction:** Test is a mandatory stage, not an optional cleanup. The Scaffold stage creates empty test files deliberately — they exist before implementation specifically so that Test has a defined scope. The test cases defined in Scaffold constrain what implementation is required.

---

### OpenFleet 5-Stage Mapping Table

| OpenArms Stage | Readiness | OpenFleet Stage(s) | Primary Difference |
|---------------|-----------|-------------------|-------------------|
| Document | 0-25% | CONVERSATION + ANALYSIS | OpenFleet separates PO conversation from codebase analysis; OpenArms merges them |
| Design | 25-50% | INVESTIGATION + REASONING | OpenFleet adds multi-agent contribution convergence at REASONING |
| Scaffold | 50-80% | (implicit in REASONING plan) | OpenArms makes skeleton creation an explicit stage |
| Implement | 80-95% | WORK | Both require code compiles, tests referenced |
| Test | 95-100% | (part of WORK) | OpenArms makes test a mandatory separate stage |

The key structural difference: OpenFleet uses MCP tool blocking as infrastructure-level enforcement (fleet_commit blocked in CONVERSATION). OpenArms uses protocol-level enforcement (MUST NOT write code) + commit convention as audit trail. Both achieve the same goal; OpenFleet's approach is stronger (impossible to violate) but requires custom tooling infrastructure.

---

### Hard Boundaries as a Design Principle

The hard boundary principle means that the OUTPUT of each stage is categorically different from the output of other stages:

- Document outputs: `.md` files only (wiki pages, docs)
- Design outputs: `.md` files only (with type sketches as documentation, not code)
- Scaffold outputs: type definition files, empty test files, `.env.example`, config stubs — all producing zero behavior
- Implement outputs: implementation code files, updates to scaffolded stubs
- Test outputs: test implementations in the scaffolded test files

These are file-system-observable differences. A commit in the Document stage that touches `src/` files is visibly a stage violation. A commit in the Scaffold stage that contains business logic functions (not just type signatures) is visibly a stage violation. The hard boundary is not just a rule — it is a category distinction.

This matters because **the primary failure mode of autonomous agents is phase conflation, not incompetence**. An agent that is allowed to produce implementation artifacts during the Document stage will produce coherent-looking code that solves the wrong problem — it was solving while still understanding. The hard boundary makes this failure mode structurally impossible.

---

### Universality: Beyond Code

The stage-gate system is not a code development methodology. It is a knowledge work methodology that happens to apply to code. Consider:

**Research/ingestion task:**
- Document: Read the source, understand its domain, map to existing wiki knowledge
- Design: Decide which pages to create, what relationships to draw, what synthesis to perform
- Scaffold: Create page skeletons with frontmatter and headers, no content
- Implement: Fill in the content — Deep Analysis, Key Insights, Relationships
- Test: Validate frontmatter, check cross-references, run pipeline post

**Infrastructure planning:**
- Document: Understand current infrastructure, map what exists, identify gaps
- Design: Decide on the target architecture, document the decision
- Scaffold: Create IaC file structure, empty module definitions, placeholder configs
- Implement: Write the actual IaC, fill in the module logic
- Test: Apply infrastructure in a test environment, verify behavior

**Team process improvement:**
- Document: Understand how the team currently works, map pain points
- Design: Decide on the process change, document the new procedure
- Scaffold: Create template documents, checklists, empty workflows
- Implement: Run the new process on a real task, fill in the templates
- Test: Retrospect — did the process improve the outcome?

In every domain, the hard boundary principle holds: decisions cannot be made before understanding is complete, skeletons cannot be built before decisions are made, implementation cannot begin before the skeleton defines the contract.

---

### Stage Enforcement Mechanisms — Comparative

| Mechanism | OpenArms | OpenFleet | Strength |
|-----------|----------|-----------|---------|
| Protocol instructions (CLAUDE.md) | Primary enforcement | Supplementary | Works immediately, can degrade with context |
| MCP tool blocking | Not applicable | Primary for CONVERSATION/WORK | Structural — impossible to violate |
| One-commit-per-stage | Core convention | Not used | Creates auditable git ledger |
| Immune system detection | Not applicable | 4/11 diseases implemented | Self-correcting after violation |
| Readiness range enforcement | Core protocol | Readiness score drives gates | Observable in task frontmatter |
| Quality gates per stage | Verified post-stage | plan_quality.py at task accept | Prevents advancement without evidence |

The practical recommendation: start with protocol enforcement (CLAUDE.md MUST/MUST NOT) and one-commit-per-stage. Add MCP tool blocking when infrastructure investment is justified. The combination provides defense in depth.

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
- CONTRADICTS: Vibe Coding (unstructured generation without stage boundaries — the failure mode this methodology exists to prevent)

## Backlinks

[[[[Task Lifecycle Stage-Gating]] (this page operationalizes the stage-gating concept for the devops domain)]]
[[[[Spec-Driven Development]] (stages enforce the spec-before-implementation principle)]]
[[[[Plan Execute Review Cycle]] (stage gates implement the phase separation that PER describes)]]
[[[[Scaffold → Foundation → Infrastructure → Features]] (SFIF is the architectural expression of the same staged progression principle)]]
[[[[Task Type Artifact Matrix]] (each task type selects a subset of stages based on complexity)]]
[[[[Backlog Hierarchy Rules]] (tasks are the unit that stages apply to; epics and modules aggregate stage completion upward)]]
[[[[Execution Modes and End Conditions]] (execution modes control which stages run and in what order)]]
[[[[Wiki Backlog Pattern]] (the wiki IS the Document/Design stage artifact system)]]
[[[[Four-Project Ecosystem]] (all four projects in the ecosystem apply this methodology)]]
[[[[Immune System Rules]] (violations of stage hard boundaries are the diseases the immune system detects)]]
[[Vibe Coding (unstructured generation without stage boundaries — the failure mode this methodology exists to prevent)]]
[[Adoption Guide — How to Use This Wiki's Standards]]
[[LLM Wiki Standards — What Good Looks Like]]
[[Model: Methodology]]
[[Never Skip Stages Even When Told to Continue]]
[[The Agent Must Practice What It Documents]]
