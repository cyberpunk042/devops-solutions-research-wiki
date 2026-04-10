---
title: "Scaffold → Foundation → Infrastructure → Features"
type: pattern
domain: cross-domain
layer: 5
status: synthesized
confidence: authoritative
maturity: growing
derived_from:
  - "Four-Project Ecosystem"
  - "Progressive Distillation"
instances:
  - page: "Research Wiki"
    context: "Scaffold (CLAUDE.md, directory structure, tech stack) → Foundation (tools/common.py, schema.yaml, config/) → Infrastructure (pipeline.py, MCP server, 15 tools) → Features (evolve pipeline, sync service, watcher daemon)."
  - page: "OpenFleet"
    context: "Scaffold (monorepo layout, agent identity model) → Foundation (orchestrator, agent base model, SOUL.md template) → Infrastructure (board sync, doctor.py, immune system rules) → Features (10 specialized agents, Mission Control UI, Open Gateway)."
  - page: "AICP"
    context: "Scaffold (venv, profile system, CLAUDE.md) → Foundation (backend router, circuit breaker, complexity scorer) → Infrastructure (MCP tools, guardrails pipeline, path protection) → Features (backend routing, voice pipeline, 5-stage LocalAI independence roadmap)."
  - page: "Front-Middleware-Backend"
    context: "Each layer (frontend, middleware, backend) independently traverses SFIF. The frontend has its own scaffold (design system decisions) → foundation (component library, routing) → infrastructure (auth, state management) → features (screens, flows). Same for middleware and backend."
created: 2026-04-09
updated: 2026-04-10
sources:
  - id: src-four-project-ecosystem
    type: documentation
    file: wiki/domains/devops/four-project-ecosystem.md
    title: "Four-Project Ecosystem"
  - id: src-user-articulation
    type: note
    file: raw/notes/scaffold-foundation-infrastructure-features.md
    title: "User articulation of SFIF build lifecycle pattern"
tags: [scaffold, foundation, infrastructure, features, build-lifecycle, architecture, cross-domain, sfif, recursive, poc, mvp, project-structure, design-lifecycle]
---

# Scaffold → Foundation → Infrastructure → Features

## Summary

Scaffold → Foundation → Infrastructure → Features (SFIF) is the universal 4-stage build lifecycle that repeats at every scale of software construction — at the project level, the feature level, the design level, and the sub-component level. Each stage has a distinct exit criterion: scaffold defines direction, foundation establishes the single entry point, infrastructure puts the necessary base in place without special behavior, and features deliver the specialized value. The pattern is recursive: each layer of a system independently traverses all four stages, sometimes top-down, sometimes bottom-up, sometimes parallel across sub-components.

> [!info] SFIF Stage Reference Card
>
> | Stage | Purpose | Exit Criterion | Key Artifacts |
> |-------|---------|---------------|--------------|
> | **Scaffold** | Define direction | Intent documented, stack decided, anyone can understand without reading code | CLAUDE.md, DESIGN.md, README, directory skeleton |
> | **Foundation** | Single entry point | Build, run, understand from one place; design system established | pipeline.py, common.py, schema.yaml, base classes |
> | **Infrastructure** | Common dependencies in place | Components can depend on it; reliably present, nothing remarkable | MCP server, router, pipeline chains, lint, validate |
> | **Features** | Specialized value | Ongoing — each feature follows SFIF recursively within its scope | Evolve pipeline, sync service, watcher daemon |

## Pattern Description

SFIF is recognizable by its stage boundary conditions. A stage is complete when its exit criterion is met — not when the code is written, but when the structural commitment is established and the next stage has a stable base to build on.

### Stage 1 — Scaffold

**What it is:** Core config files, project structure, tech stack choice, AI configuration (CLAUDE.md, DESIGN.md), READMEs. The scaffolding phase answers: "Where is this project headed?"

**Exit criterion:** The project's direction is decided and documented. Anyone joining the project can understand the intent, the stack, and the conventions without reading code.

**Key artifacts:** `CLAUDE.md`, `DESIGN.md`, `README.md`, `.gitignore`, `pyproject.toml` or equivalent, directory skeleton, initial CI configuration stubs.

**Anti-patterns:** Treating scaffold as a formality and skipping it (POC behavior). Writing code before the tech stack decision is finalized. Generating scaffold artifacts after the foundation is already built (retroactive documentation that immediately drifts).

### Stage 2 — Foundation

**What it is:** Modules/packages, design system, project spine/column structure, diagrams, architecture documentation, compilation/execution methods. Ends when there is a single entry point to manage everything, build, and update.

**Exit criterion:** The project can be built, run, and understood from a single entry point. The design system or shared model is established so all future code has a consistent base to extend.

**Key artifacts:** `tools/pipeline.py`, `tools/common.py`, `schema.yaml`, the design system's base components, the orchestrator's base class, the router's base contract. The "spine" that everything else hangs from.

**Anti-patterns:** Building features before the single entry point exists. Having three different ways to run the project. Designing the architecture after the modules are already written (foundation debt).

### Stage 3 — Infrastructure

**What it is:** Common components that others depend on. A solution that doesn't do anything special — it is simply in place and established. Basic functionalities, basic interface, development guidelines. Examples: an Excel module that provides read/write capability; an MCP server that calls a tool; a router that selects backends.

**Exit criterion:** The infrastructure is present and other components can depend on it. It does not need to do anything remarkable — it needs to be reliably there.

**What makes something infrastructure vs. feature:** Infrastructure enables things. Features use what infrastructure enables. An MCP server with tool registration and call dispatch is infrastructure. The specific tool that analyzes code quality is a feature. A routing layer that selects between backends is infrastructure. The voice pipeline that routes to a specific model is a feature.

**Anti-patterns:** Skipping infrastructure and building features directly on the foundation (produces brittle features with hardcoded dependencies). Building feature-level complexity into infrastructure (premature specialization). Treating infrastructure as "done" when it handles only one consumer.

### Stage 4 — Features

**What it is:** Specialized product features built on the established base. Advanced or specialized behaviors in the interface or the backend. The differentiated value that justifies the project's existence.

**Exit criterion:** There is no terminal exit criterion — features are the ongoing work of the project. But each feature follows SFIF recursively within its own scope.

**Anti-patterns:** Building features on unstable infrastructure (produces rework when infrastructure changes). Adding feature-level complexity to the infrastructure layer (pollutes the base). Treating POC features as production features without running the full SFIF lifecycle for the feature itself.

## The Recursive Property

SFIF is fractal. The same four stages apply at every granularity:

- **Project level**: the full project traverses scaffold → foundation → infrastructure → features
- **Feature level**: each major feature traverses scaffold (design doc) → foundation (data model) → infrastructure (API contract) → features (UI, edge cases, specializations)
- **Sub-component level**: each module or service traverses the same stages internally
- **Design level**: UI design traverses scaffold (wireframes) → foundation (design system) → infrastructure (component library) → features (specialized screens)

The traversal order is not always top-down. A system may scaffold all layers before building the foundation of any. Or it may complete Layer A's full SFIF before beginning Layer B's scaffold. Sometimes design X must precede design Y because Y depends on X's infrastructure. The recursion allows each sub-scope to advance at its own pace while the overall project follows the same lifecycle.

## POC and MVP

> [!warning] POC — deliberately skips stages (Mountain tier)
> A POC's goal is proving a concept quickly, not building correctly. Scaffold minimally, skip foundation, treat everything as infrastructure, produce one feature as proof. POC code must be **rewritten, not extended**, when moving to production.

> [!tip] MVP — completes SFIF properly but minimally (Pyramid tier)
> At least 3+ proper features on a solid foundation, ready to scale without major structural problems. Pragmatic compromises, but with the right structural bones. Features added after MVP extend the existing SFIF structure rather than fighting it.

> [!bug]- The failure pattern: POC-as-MVP
> Treating a POC as an MVP (extending mountain code into production), or treating an MVP as a target state (stopping before the skyscraper refactor when scale requires it). Both are scale-mismatch errors.

## Instances

### Research Wiki

The wiki's build history directly follows SFIF:

- **Scaffold**: `CLAUDE.md` (project intent and conventions), `wiki/` directory structure, domain registry, schema choice (YAML frontmatter + markdown)
- **Foundation**: `tools/common.py` (shared utilities), `config/schema.yaml` (validation contract), `tools/validate.py` (single quality gate), `wiki/manifest.json` (single index of truth)
- **Infrastructure**: `tools/pipeline.py` with the `post` chain (6-step orchestration), the MCP server (15 tools, basic interface), `tools/lint.py`, `tools/obsidian.py`, `tools/manifest.py` — all of these just work and other parts depend on them
- **Features**: `pipeline evolve` (evolution scoring and generation), `tools/watcher.py` (change-triggered post-chain), `tools/sync.py` (WSL↔Windows bidirectional sync), `tools/export.py` (LightRAG and AICP export profiles)

### OpenFleet

- **Scaffold**: Monorepo layout, agent identity model (SOUL.md + HEARTBEAT.md per agent), `CLAUDE.md` conventions
- **Foundation**: Deterministic orchestrator (base class, 30-second cycle logic), agent base model (execution contract), fleet state machine
- **Infrastructure**: Board sync (Plane integration), `doctor.py` immune system (24 rules, 3-strike), IRC channel routing, Open Gateway WebSocket — all of these are simply present and operational
- **Features**: 10 specialized agents (fleet-ops, project-manager, architect, software-engineer, qa-engineer, etc.), Mission Control UI (FastAPI + Next.js dashboard), AICP circuit breaker integration

### AICP

- **Scaffold**: Virtual environment structure, profile system design, `CLAUDE.md`, dependency management
- **Foundation**: Backend router (LocalAI vs Claude selection logic), circuit breaker (CLOSED/OPEN/HALF_OPEN state machine), complexity scorer
- **Infrastructure**: MCP tools (basic call dispatch), guardrails pipeline (path protection, response filtering, pre/post execution hooks) — established and depended upon
- **Features**: Voice pipeline (specialized routing to voice-capable models), 5-stage LocalAI independence roadmap features, 78 skills in `.claude/skills/`

### Front ↔ Middleware ↔ Backend

Each architectural layer traverses SFIF independently. The frontend scaffolds its design language before building its component foundation. The backend scaffolds its data model before building its service foundation. The middleware scaffolds its routing contract before building its gateway foundation. This independence means layers can be at different SFIF stages simultaneously — a mature backend infrastructure hosting a still-scaffolding frontend is a normal and healthy state.

## When To Apply

SFIF applies everywhere software is built from scratch or significantly refactored:

- **Starting a new project**: follow the four stages sequentially, resist the urge to write features before the foundation is solid
- **Evaluating a project's structural health**: audit which stage each component actually belongs to; infrastructure masquerading as features (or features embedded in infrastructure) signals structural debt
- **Planning a refactor**: identify which SFIF stage broke down, then refactor to that stage's exit criterion before continuing forward
- **Onboarding contributors**: the scaffold artifacts (CLAUDE.md, DESIGN.md, README) are the correct entry point; if they are absent, the project has scaffold debt
- **Scoping an MVP**: define 3+ features that fully exercise the infrastructure layer; anything that can be built without touching infrastructure is a viable MVP scope

## When Not To

- **POCs**: deliberately skip stages; the speed benefit is the point, and the rewrite cost is accepted upfront
- **Hotfixes**: emergency fixes go directly to the affected layer; applying full SFIF to a one-line security patch is overhead
- **Purely exploratory scripts**: one-off scripts and research code that will never be maintained do not benefit from SFIF scaffolding

## Relationships

- RELATES TO: [[Skyscraper, Pyramid, Mountain]]
- BUILDS ON: [[Progressive Distillation]]
- IMPLEMENTED BY: Research Wiki
- IMPLEMENTED BY: [[OpenFleet]]
- IMPLEMENTED BY: [[AICP]]
- RELATES TO: [[Four-Project Ecosystem]]
- RELATES TO: [[Deterministic Shell, LLM Core]]
- RELATES TO: [[Plan Execute Review Cycle]]
- FEEDS INTO: [[Knowledge Evolution Pipeline]]
- RELATES TO: [[Infrastructure as Code Patterns]]

## Backlinks

[[Skyscraper, Pyramid, Mountain]]
[[Progressive Distillation]]
[[Research Wiki]]
[[OpenFleet]]
[[AICP]]
[[Four-Project Ecosystem]]
[[Deterministic Shell, LLM Core]]
[[Plan Execute Review Cycle]]
[[Knowledge Evolution Pipeline]]
[[Infrastructure as Code Patterns]]
[[Evolution Standards — What Good Knowledge Promotion Looks Like]]
[[Methodology Framework]]
[[Model: Methodology]]
[[Model: SFIF and Architecture]]
[[Models Are Built in Layers, Not All at Once]]
[[Plannotator — Interactive Plan & Code Review for AI Agents]]
[[Stage-Gate Methodology]]
[[Task Lifecycle Stage-Gating]]
[[Wiki Design Standards — What Good Styling Looks Like]]
