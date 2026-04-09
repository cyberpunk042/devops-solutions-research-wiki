---
title: "Adoption Guide — How to Use This Wiki's Standards"
type: deep-dive
domain: cross-domain
layer: spine
status: synthesized
confidence: authoritative
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [adoption, transferable, methodology, standards, ecosystem, guide]
---

# Adoption Guide — How to Use This Wiki's Standards

## Summary

This guide explains how any project in the ecosystem (or outside it) picks up the methodology, stage-gate system, backlog structure, and knowledge architecture that this wiki defines and uses. The system is designed to be transferable: the wiki is the canonical definition, each project is an instance that adapts the framework to its own tech stack and domain. A project lead reads this page and walks away knowing exactly what to copy, what to adapt, and what to leave alone.

## Key Insights

- **The wiki is the definition; your project is an instance.** The methodology framework, stage-gate system, and knowledge architecture are defined here once and adapted per-project by changing only the artifact bindings and quality gate commands. The structural invariants (stage sequence, hierarchy rules, readiness ranges, work loop) never change.

- **Copy two files and you have the core system.** `methodology.yaml` gives you stages, task types, modes, and end conditions. `agent-directive.md` gives you the 14-step work loop, enforcement rules, and the "never" list. Everything else builds on top of these two.

- **Adapt the variables, keep the invariants.** Stage artifacts, quality gate commands, commit scopes, and directory paths are project-specific variables. Stage sequence, hierarchy rules, readiness ranges, and the work loop structure are ecosystem-wide invariants. The line between these two categories is precise and documented.

- **Three reference implementations prove transferability.** OpenArms adopted the full stack for a TypeScript project. OpenFleet implemented infrastructure-level enforcement via MCP tool stage-gating. The Research Wiki runs the framework on knowledge work. Same structural vocabulary, different domain bindings.

- **Four integration levels exist at increasing depth.** CLI commands are the simplest adoption. Skills add conversation-level intelligence. MCP tools provide programmatic access with stage-gating. Export enables file-based transfer between projects. Start with CLI; add depth as your project matures.

- **The framework is recursive and composable.** Models compose sequentially, in nested fashion, conditionally, and in parallel. The same structural vocabulary applies at every scale from ecosystem to sub-task. You learn it once and apply it everywhere.

## Deep Analysis

### What You Get (The Transferable Standards)

Adopting this system gives your project a complete, composable methodology stack. Here is what transfers:

**Methodology Framework** — A super-model that defines what a methodology model IS, how models are selected per-condition, how they compose (sequential, nested, conditional, parallel), and how they adapt per-instance. You do not hardcode a single process for your project. You define models in configuration and select them at runtime based on task type, project phase, domain, and scale. See: [[Methodology Framework]].

**Stage-Gate System** — Five stages with hard boundaries: Document, Design, Scaffold, Implement, Test. Each stage has required artifacts, permitted actions, prohibited actions, and exit criteria. Stages are not guidelines. They are structural constraints. An agent in the Document stage may not produce implementation code. Period. See: [[Stage-Gate Methodology]].

**8 Task Types with Per-Type Stage Requirements** — Not every task runs all 5 stages. The task type determines which stages are required:

| Task Type | Required Stages |
|-----------|----------------|
| epic | document, design, scaffold, implement, test |
| module | document, design, scaffold, implement, test |
| task | scaffold, implement, test |
| research | document, design |
| evolve | document, implement |
| docs | document |
| bug | document, implement, test |
| refactor | document, scaffold, implement, test |

**Backlog Structure** — Three-level hierarchy: Epic > Module > Task. Epics are containers. Modules are scoped deliverables within epics. Tasks are the atomic work units that go through stages. Readiness flows upward (task readiness aggregates to module, module to epic). Status flows upward. You work on tasks, never on epics directly. Each item has a YAML frontmatter state machine tracking status, current_stage, stages_completed, readiness, priority, and artifacts.

**Quality Gates Per Stage** — Each stage transition requires passing a gate. Document gate: wiki page exists with Summary and gap analysis. Design gate: spec or decision doc exists, trade-offs documented. Scaffold gate: structure created, validation passes. Implement gate: content/code complete, lint and validate pass. Test gate: full health chain clean, no regressions.

**14-Step Work Loop** — The exact execution sequence for autonomous agent operation: find next task, read task file, determine next stage, read stage protocol, execute stage, update frontmatter, commit, verify, check remaining stages, mark complete, update index, report, check end condition, wrap up. Every step is mandatory. No skipping, no reordering.

**8 Execution Modes** — Control how the agent progresses: autonomous (no stops), full-autonomous (skip document on tasks), semi-autonomous (human review after each task), document-only, design-only, scaffold-only, plan (alias for design-only), custom (per-run overrides).

**Knowledge Layer Architecture** — Six layers of increasing abstraction: raw material (Layer 0), source synthesis (Layer 1), concept pages (Layer 2), comparisons (Layer 3), lessons and patterns (Layer 4), decisions and principles (Layer 5). Each layer builds on the layers below. The evolution pipeline promotes content upward through the layers.

**Evolution Pipeline** — Deterministic scorer ranks candidates for promotion to higher layers. Prompt builder generates structured prompts. LLM backend (local or API) generates evolved pages. Review cycle promotes seed pages to growing/mature/canonical maturity. This is how knowledge improves continuously without manual curation.

### Step-by-Step Adoption

#### Step 1: Copy and adapt `methodology.yaml`

Copy `wiki/config/methodology.yaml` into your project. This file defines stages, task types, execution modes, end conditions, and defaults.

**What to adapt:**

- **Stage artifacts** — The wiki's Document stage produces wiki pages and gap analyses. Your TypeScript project's Document stage might produce a README section and dependency audit. Your infrastructure project's Document stage might produce a runbook and topology diagram. Change `required_artifacts` per stage to match your domain.
- **Stage protocols** — The wiki's Implement stage runs `python3 -m tools.pipeline post`. Your project's Implement stage runs `pnpm build && pnpm lint` or `terraform plan` or whatever your stack requires. Change the `protocol` commands.
- **Task types** — Add or remove types to match your work. A frontend project might add a `component` type (scaffold, implement, test). A data project might add a `migration` type (document, scaffold, implement, test). Remove types you will never use.
- **Execution modes** — Keep all 8 or trim to the ones you use. Most projects start with autonomous + semi-autonomous + custom.
- **End conditions** — Keep as-is unless you have domain-specific stopping criteria.

**What to keep exactly as-is:**

- Stage names (document, design, scaffold, implement, test) — changing these breaks the shared vocabulary.
- Readiness ranges (0-25, 25-50, 50-80, 80-95, 95-100) — these are calibrated and consistent across the ecosystem.
- Stage ordering — the sequence is invariant.
- Max retries default (2).

#### Step 2: Copy and adapt `agent-directive.md`

Copy `wiki/config/agent-directive.md` into your project. This file tells the agent HOW to operate: the 14-step work loop, enforcement rules, commit conventions, quality gates, and the "never" list.

**What to adapt:**

- **Quality gate commands** — Replace `python3 -m tools.validate` with your project's equivalent (`pnpm tsgo`, `cargo check`, `terraform validate`, etc.).
- **Commit message format** — Keep conventional commits but change the scope. `feat(wiki): T0XX` becomes `feat(api): T0XX` or `feat(infra): T0XX`.
- **Backlog paths** — If your backlog lives at a different path, update all references.
- **Operator directive location** — Change `wiki/log/` to wherever your project stores operator directives.

**What to keep exactly as-is:**

- The 14-step work loop structure — this is the execution engine. Do not add steps, remove steps, or reorder steps.
- The enforcement rules (stages are mandatory, one commit per stage, verify after each step).
- The "never" list — all 14 items apply universally.
- The hierarchy rules (epic > module > task, readiness flows up, status flows up).

#### Step 3: Create the backlog structure

Create the directory structure for your project's backlog:

```
your-project/
  wiki/
    backlog/
      epics/
        _index.md
      modules/
        _index.md
      tasks/
        _index.md
```

Each index file tracks the items in that level. Each item is a markdown file with YAML frontmatter containing: status, task_type, current_stage, readiness, priority, stages_completed, artifacts, and a description with "Done When" criteria.

#### Step 4: Create the operator log

Create `wiki/log/` (or your equivalent path) for operator directives. This is where human instructions are stored verbatim. The agent reads these before acting. They override methodology defaults.

#### Step 5: Add methodology rules to CLAUDE.md

Your project's CLAUDE.md needs to reference the methodology. Add a section that points to your methodology.yaml and agent-directive.md. Example:

```markdown
## Methodology

This project uses the stage-gate methodology defined in:
- `wiki/config/methodology.yaml` — stages, task types, modes, end conditions
- `wiki/config/agent-directive.md` — work loop, enforcement, quality gates

The agent MUST follow the 14-step work loop. Stage boundaries are hard.
See the agent directive for the complete execution protocol.
```

#### Step 6: Adapt quality gates to your tech stack

This is where adoption becomes project-specific. Map each stage's quality gate to your project's tooling:

| Stage | Wiki (reference) | TypeScript project | Infrastructure project |
|-------|------------------|-------------------|----------------------|
| document | `tools.validate` on wiki pages | README section exists, dependencies audited | Runbook drafted, topology documented |
| design | Spec exists, trade-offs documented | ADR exists, API contract defined | Design doc exists, blast radius assessed |
| scaffold | `pipeline post` clean | `pnpm tsgo` passes on empty types | Terraform modules scaffolded, plan succeeds |
| implement | `pipeline post` + `tools.lint` | `pnpm build && pnpm lint` passes | `terraform apply` succeeds in staging |
| test | `pipeline chain health` | `pnpm test` passes, coverage threshold met | Smoke tests pass, monitoring confirms health |

### What to Keep vs What to Adapt

#### KEEP as-is (the invariants)

These are structural properties of the system. Changing them breaks the model:

- **Hierarchy rules** — Epic > Module > Task. Readiness flows up. Status flows up. You work on tasks, not epics.
- **Stage gates** — Hard boundaries between stages. No producing artifacts for future stages. No skipping required stages.
- **Stage sequence** — Document before Design before Scaffold before Implement before Test. Always.
- **Maturity lifecycle** — seed > growing > mature > canonical. Content evolves through these levels.
- **Work loop structure** — 14 steps in order. Find task, read task, determine stage, read protocol, execute, update, commit, verify, check remaining, mark complete, update index, report, check end condition, wrap up.
- **Readiness ranges** — 0-25, 25-50, 50-80, 80-95, 95-100. These are calibrated.
- **Frontmatter state machine** — status, task_type, current_stage, readiness, priority, stages_completed, artifacts. All required.
- **Commit discipline** — One commit per stage. Conventional format. Validate before committing.
- **Enforcement rules** — The 14 "never" items from the agent directive.

#### ADAPT per project (the variables)

These are the domain-specific bindings that make the framework concrete for your context:

- **Stage artifacts** — What each stage produces. Wiki pages vs TypeScript modules vs Terraform configs vs Kubernetes manifests.
- **Quality gate commands** — The specific CLI commands that verify stage completion. `tools.validate` vs `pnpm tsgo` vs `terraform plan` vs `kubectl apply --dry-run`.
- **Task types** — Add types your project needs (component, migration, deployment). Remove types it does not use.
- **Execution modes** — Which modes are relevant. A solo developer may only need autonomous + custom. A team project needs semi-autonomous and human-review gates.
- **Commit scope** — `feat(wiki)` vs `feat(api)` vs `feat(infra)`.
- **Directory layout** — Where the backlog, logs, and configs live. The structure matters; the exact paths are flexible.
- **Operator directive conventions** — How human instructions are captured. The principle (log verbatim, directives override methodology) is invariant; the mechanism adapts.

### Available Models

The framework defines composable models. Each is a named sequence of stages with specific behavior:

#### Feature Development (Full Model)

**Stages:** Document > Design > Scaffold > Implement > Test
**Use when:** Building a new capability, adding a module, implementing a planned feature.
**Readiness range:** 0% to 100%.

This is the default model for epics and modules. Every stage runs. Every artifact is produced. Every gate is checked. Use this for anything that matters enough to get right.

#### Research

**Stages:** Document > Design (stop)
**Use when:** Investigating a question, surveying options, producing analysis without implementation.
**Readiness cap:** 50%.
**Output:** Wiki pages, comparison documents, decision records.

Research stops at Design because its purpose is understanding, not building. The output feeds future feature development.

#### Evolution

**Stages:** Document > Implement
**Use when:** Promoting existing content or code to a higher maturity level. Refining what already exists.
**Skips:** Design and Scaffold (the structure already exists from a prior cycle).

#### Hotfix / Bug

**Stages:** Document > Implement > Test
**Use when:** Fixing something broken. The design is "make it not broken." Scaffold is unnecessary because the structure exists.
**Skips:** Design and Scaffold.

#### Docs

**Stages:** Document (stop)
**Use when:** Writing documentation, capturing knowledge, logging decisions.
**Readiness cap:** 25%.
**Output:** Documentation artifacts only.

#### Task (Lightweight)

**Stages:** Scaffold > Implement > Test
**Use when:** Atomic work units where the problem is already understood and designed.
**Skips:** Document and Design (covered at the module or epic level).

#### Custom

**Stages:** Define your own sequence.
**Use when:** None of the above fit. Specify stop stage, review gates, and end condition at invocation time. Ephemeral, per-run configuration.

### Integration Interfaces

The methodology system exposes four integration levels. Adopt whichever matches your project's tooling maturity:

#### CLI (Pipeline Commands)

The simplest integration. Your project defines pipeline commands that map to methodology operations:

- `pipeline chain continue` — Resume the mission: run diagnostics, show state, present options.
- `pipeline chain health` — Full validation + lint + manifest check.
- `pipeline post` — Post-change validation chain.
- `pipeline evolve --score` — Rank evolution candidates.

Your project adapts these to its own tooling. An OpenArms equivalent might be `pnpm methodology:status`. An infrastructure project might be `make health-check`.

#### Skills (Conversation Commands)

Claude Code skills provide conversation-level access to methodology operations. Skills like `continue`, `evolve`, `status`, `gaps` wrap the pipeline commands with context and intelligence.

Your project defines its own skills in `skills/` that wrap its own methodology operations. The skill structure (SKILL.md with trigger conditions, instructions, and tool access) is shared across the ecosystem.

#### MCP (Tool-Level Access)

MCP tools provide programmatic access. The wiki exposes 15 tools: `wiki_status`, `wiki_search`, `wiki_evolve`, etc. These are the finest-grained interface.

Your project defines its own MCP tools that expose methodology state. OpenFleet uses MCP tool stage-gating: the tool itself checks which stage the current task is in and refuses to execute if the stage is wrong. This is infrastructure-layer enforcement.

#### Export (File-Based Transfer)

The wiki exports knowledge to sister projects via file-based transfer profiles. Export transforms YAML frontmatter to markdown headers for compatibility with downstream systems.

Your project can consume wiki exports (methodology definitions, patterns, lessons) and produce its own exports for other consumers. The export mechanism is defined in `config/export-profiles.yaml`.

### Reference Implementations

#### OpenArms (Fullest Adoption)

OpenArms is the reference implementation. It adopted the complete stack:

- `wiki/config/methodology.yaml` — 8 task types, 5 stages, 8 execution modes, 5 end conditions.
- `wiki/config/agent-directive.md` — Full 14-step work loop with TypeScript-specific quality gates.
- `wiki/backlog/` — Full epic > module > task hierarchy with frontmatter state machines.
- `wiki/log/` — Operator directives logged verbatim.
- CLAUDE.md references the methodology and agent directive.

OpenArms adapted the artifacts: its Document stage produces TypeScript interface sketches in documentation files; its Implement stage runs `pnpm build && pnpm lint`; its Test stage runs `pnpm test` with coverage thresholds. But the stage sequence, hierarchy rules, readiness ranges, and work loop are identical to the wiki's definition.

**What makes it the reference:** OpenArms proved that a code project (TypeScript, React, Express) can adopt the same methodology framework as a knowledge project (Python, wiki pages, research pipeline) by changing only the artifact bindings and quality gate commands.

#### OpenFleet (Structural Enforcement)

OpenFleet took a different adaptation path. Instead of protocol-level enforcement (agent reads the rules and follows them), OpenFleet implemented infrastructure-level enforcement:

- MCP tool stage-gating: tools check the current task's stage and refuse to execute if the operation belongs to a different stage.
- SPEC-TO-CODE pattern: a 5-stage model (CONVERSATION, ANALYSIS, INVESTIGATION, REASONING, WORK) that maps to the same Document-Design-Scaffold-Implement-Test structure.
- Disease catalogue: documented anti-patterns with detection heuristics.

OpenFleet's adaptation shows that the same framework principles can be enforced through tooling rather than instructions, which is more robust for multi-agent systems where agents may not reliably follow protocol documents.

#### Research Wiki (The Canonical Source)

This wiki is both the definition and an instance. It defines the framework (the methodology-framework page, the stage-gate-methodology page, this adoption guide). It also runs the framework on itself:

- Knowledge stages: Ingest > Synthesize > Cross-Reference > Evolve (mapped to Document > Implement > Test > Evolve).
- Quality gates: `pipeline post`, `tools.validate`, `tools.lint`.
- Evolution pipeline: scorer > prompt builder > LLM backend.
- Backlog system: epics, modules, tasks with frontmatter state machines.

The wiki proves that knowledge work and code work can share the same methodology vocabulary. The stages have different artifacts (wiki pages vs source files), different gate commands (validate vs compile), and different evolution mechanisms (layer promotion vs version releases) — but the structural principles are identical.

## Relationships

- BUILDS ON: [[Methodology Framework]]
- BUILDS ON: [[Stage-Gate Methodology]]
- BUILDS ON: [[Four-Project Ecosystem]]
- RELATES TO: [[Task Type Artifact Matrix]]
- RELATES TO: [[Methodology Execution Modes]]
- ENABLES: methodology adoption across ecosystem projects
- FEEDS INTO: project-specific methodology.yaml instances

## Backlinks

[[Methodology Framework]]
[[Stage-Gate Methodology]]
[[Four-Project Ecosystem]]
[[Task Type Artifact Matrix]]
[[Methodology Execution Modes]]
[[methodology adoption across ecosystem projects]]
[[project-specific methodology.yaml instances]]
[[Model: Methodology]]
