---
title: "Methodology Framework"
type: concept
layer: 2
domain: cross-domain
status: synthesized
confidence: authoritative
maturity: growing
created: 2026-04-09
updated: 2026-04-10
sources:
  - id: src-openarms-methodology
    type: documentation
    file: raw/articles/openarms-methodology-yaml-full.md
    title: "OpenArms Methodology YAML + Agent Directive"
    ingested: 2026-04-09
  - id: src-openfleet-methodology-scan
    type: documentation
    file: raw/articles/openfleet-methodology-scan.md
    title: "OpenFleet Methodology Deep Scan"
    ingested: 2026-04-09
tags: [methodology, meta-methodology, stage-gate, composable, recursive, framework, transferable, multi-track, skyscraper, sfif]
---

# Methodology Framework

## Summary

The Methodology Framework is the meta-system that defines, selects, composes, and adapts methodology models across the entire DevOps ecosystem. It is not itself a methodology — it is the system that CONTAINS methodologies. Where Stage-Gate Methodology describes a specific 5-stage sequence, where SFIF describes a specific 4-stage build lifecycle, and where Task Type Artifact Matrix maps task types to stage subsets, this framework defines what a methodology model IS, how models are SELECTED for a given situation, how models COMPOSE into larger execution structures, how models are ADAPTED per-instance, and how the same framework applies recursively at every scale from project to task. It also defines the multi-track property — that execution, project management, and knowledge tracks each run their own methodology model simultaneously on the same project — and the quality dimension that makes the choice between skyscraper rigor and pyramid pragmatism explicit rather than accidental. Every specific methodology page in this wiki is an INSTANCE of a model defined within this framework.

> [!info] Framework Components Reference Card
>
> | Component | What It Is | Example |
> |-----------|-----------|---------|
> | **Model** | Named entity: stages + artifacts + gates + readiness + protocols | `feature-development`, `spike`, `research` |
> | **Selection** | Condition-driven model choice (type, phase, domain, scale, state) | task_type=spike → Document + Design only |
> | **Composition** | Models combining: sequential, nested, conditional, parallel | SFIF at macro → 5-stage at task → type-subset at sub-task |
> | **Adaptation** | Per-instance overrides (stages, artifacts, readiness, gates) | Hotfix skips Document+Design; spike caps at 50% readiness |
> | **Recursion** | Same vocabulary at every scale | Ecosystem → Project → Epic → Module → Task |
> | **Multi-Track** | Concurrent models on different material | Execution + PM + Knowledge tracks in parallel |
> | **Quality Target** | Explicit rigor parameter per execution | Skyscraper / Pyramid / Mountain (anti-pattern) |

## Key Insights

> [!tip] A model is DATA, not CODE
> A methodology model is a named, composable sequence with stages, artifacts, gates, readiness ranges, and protocols — defined in configuration (methodology.yaml), not embedded in code. Models can be created, versioned, compared, and validated against a schema. "Feature-development", "research", "spike" all share the same structural vocabulary with different content.

> [!abstract] Selection is multi-dimensional, not hardcoded
>
> | Dimension | What It Evaluates | Example |
> |-----------|------------------|---------|
> | Task type | Direct selector from artifact matrix | spike → 2-stage, module → 5-stage |
> | Project phase | Macro-level SFIF position | Foundation → emphasize Document/Design |
> | Domain | Natural model family | Code → 5-stage; Knowledge → Ingest-Synthesize-Evolve |
> | Scale | Blast radius + dependency count | Single function → skip Document; new module → full model |
> | Current state | Greenfield vs legacy, dev vs prod | Mountain codebase cannot absorb Skyscraper process |

> [!warning] Multiple tracks coexist — a project has three concurrent methodologies
>
> | Track | Model | Material | Purpose |
> |-------|-------|----------|---------|
> | **Execution** | Brainstorm → Spec → Plan → Implement | Code, config, infrastructure | HOW things get built |
> | **PM/Observability** | Epics → Modules → Tasks + stage gates | Work items, status, progress | WHAT gets tracked |
> | **Knowledge** | Ingest → Synthesize → Cross-Ref → Evolve | Research, patterns, lessons | WHAT gets learned |
>
> Interactions: PM → Execution triggers work. Execution → Knowledge captures findings. Knowledge → PM generates backlog items. These are FEEDS INTO relationships, not sequential dependencies.

**Models compose in four ways.** Sequential (research → feature-development). Nested (SFIF → 5-stage → type-subset). Conditional (bug → skip Design; spike → stop at Design). Parallel (three tracks simultaneously). Real work runs multiple compositions at once.

**Models adapt per-instance through overrides.** Stage overrides (skip Design for hotfixes), artifact overrides (wiki pages instead of code), readiness caps (spike maxes at 50%), gate overrides (code checks compilation; wiki checks validation). The model provides the default; the instance provides the delta.

**The framework is recursive.** Same vocabulary at every scale — ecosystem, project, epic, module, task, sub-task. Zoom in on any level and you find the same structure (stages, artifacts, gates, readiness) instantiated with different content.

**Quality is an explicit parameter, not an accident.** Skyscraper (full process), Pyramid (adapted, deliberate compressions), Mountain (no process — the anti-pattern). Declared BEFORE work begins, not assessed afterward.

**Wiki defines; projects consume.** This page is canonical. OpenArms (methodology.yaml), OpenFleet (SPEC-TO-CODE + MCP blocking), AICP (routing profiles), Wiki (ingest-synthesize-evolve) are instances. Changes flow wiki → projects.

## Deep Analysis

### What Is a Methodology Model

A methodology model is a first-class entity with a precise definition. It consists of:

**Name**: A unique identifier that can be referenced in configuration and selection rules. Examples: `feature-development`, `research`, `spike`, `hotfix`, `docs`, `refactor`, `full-project`.

**Stages**: An ordered sequence of named phases. Each stage has:
- A name (Document, Design, Scaffold, Implement, Test — or domain-specific equivalents)
- A readiness range (the band of completion percentage this stage covers)
- Required artifacts (what must be produced to prove stage completion)
- Permitted actions (what the agent or human is allowed to do during this stage)
- Prohibited actions (what is explicitly forbidden — the hard boundaries)
- Exit criteria (conditions that must be true before the gate opens)

**Gates**: Transition rules between stages. A gate may be:
- Automatic (proceed when artifacts exist and exit criteria are met)
- Human-reviewed (proceed only after explicit approval)
- Score-based (proceed when a readiness or quality score exceeds a threshold)
- Time-bounded (proceed after a waiting period, regardless of other conditions)

**Protocols**: Cross-cutting rules that apply across all stages:
- Commit conventions (one commit per stage, conventional commit format)
- Naming conventions (artifact file names, branch names)
- Audit requirements (what gets logged, what gets tracked)
- Escalation rules (when to switch from autonomous to guided execution)

**Parameters**: Configurable values that govern model behavior:
- Readiness ranges per stage
- Maximum time per stage
- Required vs optional artifacts
- Quality target (skyscraper, pyramid, mountain)
- Execution mode (autonomous, semi-autonomous, guided, custom)

The critical distinction is that a model is DATA, not CODE. It is defined in a configuration file (methodology.yaml, CLAUDE.md, or equivalent), not embedded in implementation logic. This means models can be:
- Created without changing any code
- Versioned alongside the project
- Compared across projects
- Validated against a schema
- Selected at runtime based on conditions

The 5-stage methodology (Document, Design, Scaffold, Implement, Test) is one model. The research pipeline (Ingest, Synthesize, Cross-Reference, Evolve) is another. The OpenFleet execution model (CONVERSATION, ANALYSIS, INVESTIGATION, REASONING, WORK) is another. They share the same structural vocabulary but differ in content.

### Model Selection

Model selection answers the question: given a specific situation, which model should run? The selection is driven by conditions evaluated against the current context.

**Condition dimensions:**

1. **Task type** — The most direct selector. A `spike` task type selects the spike model (Document + Design only). A `docs` task selects the docs model (Document only). A `module` task selects the full 5-stage model. This is what the Task Type Artifact Matrix already implements.

2. **Project phase** — The macro-level selector. During the Scaffold phase of SFIF, the emphasis is on Document and Design: understanding the landscape, choosing technologies, defining structure. During the Features phase, the emphasis shifts to Implement and Test: the structure is established, the work is execution. The same task type may select a different model depending on which SFIF phase the project is in.

3. **Domain** — Different domains have different natural models. Code domains use Document-Design-Scaffold-Implement-Test. Knowledge domains use Ingest-Synthesize-Cross-Reference-Evolve. Infrastructure domains use Plan-Provision-Configure-Verify. The domain dimension selects which family of models is available.

4. **Scale** — A single function change does not require the same model as a new module. Scale affects which stages are mandatory. Small changes may skip Document (the context is already understood). Large changes may add a Planning pre-stage. Scale is not just lines of code — it includes blast radius, dependency count, and team impact.

5. **Current state** — A greenfield project selects differently than a legacy codebase. A system in production selects differently than a system in development. A codebase at Skyscraper tier selects differently than one at Mountain tier. State-aware selection prevents applying Skyscraper-grade methodology to a Mountain codebase that cannot absorb it.

**Selection can be multi-dimensional.** A research spike during the foundation phase of a knowledge-systems project evaluates all five dimensions simultaneously: task_type=spike AND phase=foundation AND domain=knowledge-systems AND scale=small AND state=greenfield. The selection engine resolves this to a specific model, potentially with overrides.

**Selection can include inheritance.** A project defines base models, and task-level selections inherit from the project-level defaults. If the project default is "full 5-stage", a spike task inherits the base readiness ranges and commit conventions but overrides the stage list to Document + Design only.

### Model Composition

> [!info] Four composition patterns
>
> | Pattern | How Models Combine | Example |
> |---------|-------------------|---------|
> | **Sequential** | A completes → B starts (A's output = B's input) | Research model → Feature Development model |
> | **Nested** | B runs inside one of A's stages (fractal recursion) | 5-stage runs inside SFIF's Infrastructure stage |
> | **Conditional** | Branch selects which model runs | bug → skip Design; spike → stop at Design |
> | **Parallel** | Multiple models on different tracks simultaneously | Execution + PM + Knowledge tracks |

> [!example]- Nested composition in practice — three levels deep
>
> - **Project level:** SFIF (Scaffold → Foundation → Infrastructure → Features)
>   - **Infrastructure stage:** contains 5 modules
>     - **Module level:** Full 5-stage (Document → Design → Scaffold → Implement → Test)
>       - **Task level:** Type selects sub-model (task=3-stage, spike=2-stage, docs=1-stage)
>
> Three levels of nesting, each with its own model, each contributing to the level above. The outer model defines the macro rhythm; the inner model defines the micro rhythm.

Conditional composition can also operate mid-model — a gate between Design and Scaffold might evaluate: "Pure architecture change? Skip Scaffold + Implement, go directly to Test (architecture review)." This is intra-model branching.

Parallel composition is not theoretical — it is the actual operating condition. Every project runs execution, PM, and knowledge tracks simultaneously with FEEDS INTO interactions between them (see Multi-Track below).

### Model Adaptation

Every model definition is a template. Every execution of a model is an instance with potential overrides. The adaptation layer defines how instances diverge from templates.

**Stage overrides:**
- Skip stages: A hotfix model skips Document and Design because the problem is already understood and the fix is already designed — it goes straight to Implement and Test.
- Add stages: A security-sensitive model adds a Security Review stage between Design and Scaffold.
- Reorder stages: A research model may run Design before Document when the design space needs to be explored before the landscape is fully mapped.

**Artifact overrides:**
- Different output types: A research task produces wiki pages as artifacts, not code. A docs task produces documentation files. A spike produces a decision document. The stage names may be the same (Document, Design), but the artifacts are different.
- Reduced requirements: A small task may require only a summary artifact for the Document stage, not a full wiki page with gap analysis.
- Additional requirements: A compliance-sensitive task may require a risk assessment artifact at every stage.

**Readiness range overrides:**
- A spike is capped at 50% readiness by design — it covers Document (0-25%) and Design (25-50%) and stops. Readiness 50% IS completion for a spike.
- A POC may be capped at 80% — enough to prove the concept, not enough for production quality.
- An MVP targets 95% — functional and tested, but not fully polished.
- A production release targets 100%.

**Gate overrides:**
- Code projects check compilation, type checking, lint, and test suite at the Implement gate.
- Wiki projects check frontmatter validation, link integrity, summary word count, and relationship completeness at the equivalent gate.
- Infrastructure projects check provisioning success, configuration validation, and health check responses.
- The gate STRUCTURE is the same (evaluate conditions before proceeding), but the CONDITIONS are domain-specific.

**Protocol overrides:**
- OpenArms uses one-commit-per-stage as its git protocol.
- OpenFleet uses MCP tool blocking as its enforcement protocol.
- The wiki uses the post-chain (validate, lint, manifest) as its enforcement protocol.
- Each project adapts the enforcement mechanism to its tooling while preserving the structural principle.

### The Recursive Property

The framework's most powerful property is that it applies identically at every scale. There is no "project-level framework" and a separate "task-level framework." There is one framework, instantiated at multiple levels simultaneously.

**At the ecosystem level**: The four-project ecosystem (OpenArms, OpenFleet, AICP, Research Wiki) itself follows a model. The ecosystem has a Scaffold phase (establishing each project's identity and relationships), a Foundation phase (building shared infrastructure — the wiki, the methodology definitions), an Infrastructure phase (building integration points — kb_sync, export, MCP tools), and a Features phase (building specialized capabilities per project).

**At the project level**: Each project runs SFIF. The Research Wiki's SFIF progression is documented: Scaffold (CLAUDE.md, directory structure, tech stack) → Foundation (tools/common.py, schema.yaml, config/) → Infrastructure (pipeline.py, MCP server, 15 tools) → Features (evolve pipeline, sync service, watcher daemon).

**At the epic level**: An epic like "Build the Evolution Pipeline" runs its own model. Document the concept (what is evolution, what does the pipeline need to do), Design the pipeline (scorer, scaffold, auto-generate, review), Scaffold the components (evolve.py module structure), Implement the logic (scoring algorithm, template rendering), Test (validate output quality, run on real candidates).

**At the task level**: A single task like "Implement the scoring algorithm" runs a sub-model. The task-type selector chooses the appropriate stages. A `task` type runs Scaffold-Implement-Test. A `spike` would run Document-Design only.

**At the sub-task level**: Even within a single implementation task, the pattern can recurse. Understanding the existing codebase (Document), sketching the approach (Design), creating the function signatures (Scaffold), writing the logic (Implement), verifying correctness (Test).

The key insight is not that this recursion exists — any developer intuitively works in stages. The key insight is that the SAME STRUCTURAL VOCABULARY (model, stages, artifacts, gates, readiness) applies at every level, and the SAME SELECTION AND COMPOSITION MECHANISMS operate at every level. This makes the framework learnable once and applicable everywhere.

### Multi-Track Coexistence

> [!example]- The three tracks in detail
>
> **Execution Track**
> - **Model:** Brainstorm → Spec → Plan → Implementation (superpowers model)
> - **Material:** Code, configurations, infrastructure
> - **Artifacts:** Brainstorm documents, spec files, implementation plans, pull requests
> - **Cadence:** Per-feature or per-task, driven by the backlog
> - **Enforcement:** CLAUDE.md instructions, plan file checksums, verification gates
> - **Answers:** "Given a thing to build, what is the process for building it well?"
>
> **PM / Observability Track**
> - **Model:** Epics → Modules → Tasks with stage gates and readiness (backlog model)
> - **Material:** Work items, status, dependencies, progress
> - **Artifacts:** Backlog entries, status reports, stage-gate transitions, readiness scores
> - **Cadence:** Continuous, updated on every state change
> - **Enforcement:** Backlog hierarchy rules, status propagation, readiness aggregation
> - **Answers:** "What is the state of the project, what is done, what is next, what is blocked?"
>
> **Knowledge Track**
> - **Model:** Ingest → Synthesize → Cross-Reference → Evolve (wiki model)
> - **Material:** Research, documentation, patterns, lessons, decisions
> - **Artifacts:** Wiki pages, cross-domain connections, pattern instances, evolved knowledge
> - **Cadence:** Periodic, triggered by new information or gaps
> - **Enforcement:** Post-chain validation, quality gates, lint checks, overlap detection
> - **Answers:** "What do we know, what are the patterns, what should we do differently?"
>
> **Track Interactions:**
> - PM → Execution: task triggers execution cycle
> - Execution → Knowledge: findings feed synthesis
> - Knowledge → PM: gap analysis generates backlog items
> - Knowledge → Execution: best practices change the execution model

### The Quality Dimension

> [!success] Skyscraper — full process
> Every stage runs. Every artifact produced to spec. Every gate checked. Readiness targets 100%. **Appropriate for:** core infrastructure, production-critical features, foundational decisions, canonical documentation. The cost is time; the benefit is structural integrity that compounds.

> [!tip] Pyramid — adapted process
> Stages may be compressed (Document + Design merge). Artifacts may be lighter (bullet summary vs full wiki page). Gates may be softer (self-review vs peer review). Readiness targets 85–95%. **Appropriate for:** most everyday work, well-understood domains, time-constrained delivery. Some structural debt, but maintainable.

> [!bug]- Mountain — the anti-pattern
> No process. Stages skipped accidentally. Artifacts missing. Gates ignored. Readiness untracked. **Appropriate for: NOTHING.** The mountain is not a valid quality target — it is what happens when no target is set. The framework exists precisely to prevent this.

The critical innovation: quality is a PARAMETER on model execution, declared BEFORE work begins. "This module is core infrastructure. Skyscraper." "This bug fix is straightforward. Pyramid." "This spike is exploration. Pyramid with 50% readiness cap." Not assessed afterward — it shapes the entire execution.

### Transferability

The Methodology Framework exists in a defined hierarchy of authority:

**This wiki page** is the canonical definition. It defines the vocabulary (model, stage, artifact, gate, readiness, track, quality target), the composition rules (sequential, nested, conditional, parallel), and the adaptation mechanisms (overrides per dimension).

**Project configurations** are instances. Each project adapts the framework to its specific context:

- **OpenArms**: methodology.yaml defines 7 task types, 5 stages, 8 execution modes, 5 end conditions, per-type artifact matrices, readiness ranges, and commit conventions. This is the most fully elaborated instance.
- **OpenFleet**: SPEC-TO-CODE pattern with CONVERSATION→ANALYSIS→INVESTIGATION→REASONING→WORK stages, MCP tool blocking for gate enforcement, and a disease catalogue for anti-pattern detection. This instance emphasizes infrastructure-layer enforcement over protocol-layer enforcement.
- **AICP**: Routing profiles, complexity scoring, and circuit breaker patterns implement the methodology at the request-routing level. The "stages" are backend selection, complexity assessment, guardrail checking, and response delivery.
- **Research Wiki**: The ingest-synthesize-evolve pipeline, post-chain validation, and quality gates implement the methodology for knowledge work. The "stages" are raw ingestion, page synthesis, cross-referencing, and evolution.

**The transfer direction is defined**: wiki → projects. When the framework evolves (new composition patterns, new adaptation mechanisms, new quality dimensions), the wiki definition changes first. Projects then adapt their configurations to reflect the evolved framework. Projects do NOT change the framework — they instantiate it.

**The transfer mechanism is also defined**: project-specific configurations reference framework concepts by name. A methodology.yaml that defines `stages: [document, design, scaffold, implement, test]` is referencing the stage concept defined here. When the framework clarifies what "stage" means (adds a new required property, refines the readiness model), the project configuration can be validated against the updated definition.

This separation between definition and instance is what makes the framework sustainable. The framework can evolve without breaking projects. Projects can adapt without corrupting the framework. The wiki serves as the single source of truth, and the export/sync mechanism (LightRAG, kb_sync.py) propagates the definitions.

## Open Questions

All 7 original questions resolved in [[Decision: Methodology Framework Design Decisions]].

## Answered Open Questions

> [!example]- Selection engine formalization?
> Lookup table with fallback scoring. Simple first — upgrade to scoring when lookup fails 3+ times. See [[Decision: Methodology Framework Design Decisions]].

> [!example]- Declarative vs imperative composition?
> Declarative config for sequences, imperative only for conditional branches. Conditions declared in config; evaluation is code. See [[Decision: Methodology Framework Design Decisions]].

> [!example]- Mid-execution model change?
> Promote the task (e.g., task → module). Completed stages preserved. Restart from next required stage. See [[Decision: Methodology Framework Design Decisions]].

> [!example]- Quality dimension granularity?
> Three tiers sufficient. Per-stage overrides for mixed-rigor projects. See [[Decision: Methodology Framework Design Decisions]].

> [!example]- Track synchronization?
> Soft sync at SFIF phase boundaries. Not hard gates. See [[Decision: Methodology Framework Design Decisions]].

> [!example]- Framework as a model (meta-meta)?
> Yes — and this wiki already does it. The framework page IS the Document stage. See [[Decision: Methodology Framework Design Decisions]].

> [!example]- Model versioning?
> Semver on methodology.yaml. Manual compatibility check at current scale. See [[Decision: Methodology Framework Design Decisions]].

### Model Registry

The Methodology Framework is the super-model. These are the named sub-models it governs:

| Model | Lines | What it defines |
|-------|-------|----------------|
| [[Model: LLM Wiki]] | 444 | The wiki structure, schema, operations, evolution |
| [[Model: Methodology]] | 249 | The stage-gate system, task types, composability |
| [[Model: Claude Code]] | 230 | The agent platform, extensions, context discipline |
| [[Model: Skills, Commands, and Hooks]] | 229 | The extension hierarchy, hooks lifecycle |
| [[Model: Quality and Failure Prevention]] | 269 | The 3-layer defense, failure lessons, harness engineering |
| [[Model: MCP and CLI Integration]] | 180 | The two integration strategies, decision framework |
| [[Model: Ecosystem Architecture]] | 179 | The 5-project ecosystem, integration interfaces |
| [[Model: Knowledge Evolution]] | 185 | The evolution pipeline, maturity lifecycle |
| [[Model: Design.md and IaC]] | 174 | Markdown-as-AI-config, companion file ecosystem |
| [[Model: SFIF and Architecture]] | 170 | The 4-stage build lifecycle, quality tiers |
| [[Model: Second Brain]] | 163 | PKM theory, PARA + Zettelkasten, Obsidian |
| [[Model: Automation and Pipelines]] | 144 | Pipeline chains, event-driven automation |
| [[Model: NotebookLM]] | 172 | Grounded research engine, content pipeline |
| [[Model: Local AI ($0 Target)]] | 147 | AICP routing, local inference, $0 target |

Quality standard: [[LLM Wiki Standards — What Good Looks Like]]

When adding a new model: create the page via the model-builder skill (`/build-model`), then add it to this registry.

## Relationships

- CONTAINS: [[Stage-Gate Methodology]] (the 5-stage model is an instance within this framework)
- CONTAINS: [[Task Type Artifact Matrix]] (task-type-to-model selection is one selection axis)
- CONTAINS: [[Execution Modes and End Conditions]] (execution modes are model parameters)
- CONTAINS: [[Scaffold → Foundation → Infrastructure → Features]] (SFIF is the project-level model)
- CONTAINS: [[Spec-Driven Development]] (SDD is the execution track's methodology model)
- CONTAINS: [[Skyscraper, Pyramid, Mountain]] (the quality dimension of model execution)
- CONTAINS: [[Task Lifecycle Stage-Gating]] (stage-gating is the enforcement mechanism for models)
- ENABLES: [[Backlog Hierarchy Rules]] (the PM track model that structures work items)
- ENABLES: [[LLM Wiki Pattern]] (the knowledge track model for wiki-based knowledge management)
- ENABLES: [[Second Brain Architecture]] (the knowledge track operates within the second brain structure)
- BUILDS ON: [[Progressive Distillation]] (maturity progression is a model within the knowledge track)
- RELATES TO: [[Four-Project Ecosystem]] (the ecosystem is the highest-level instance of the framework)
- FEEDS INTO: [[Wiki Backlog Pattern]] (PM track methodology feeds backlog structure)
- IMPLEMENTS: [[Scaffold → Foundation → Infrastructure → Features]] (raw/notes/2026-04-09-user-directive-raw-idea-flow-patterns-standards.md)

## Backlinks

[[Stage-Gate Methodology]]
[[Task Type Artifact Matrix]]
[[Execution Modes and End Conditions]]
[[Scaffold → Foundation → Infrastructure → Features]]
[[Spec-Driven Development]]
[[Skyscraper, Pyramid, Mountain]]
[[Task Lifecycle Stage-Gating]]
[[Backlog Hierarchy Rules]]
[[LLM Wiki Pattern]]
[[Second Brain Architecture]]
[[Progressive Distillation]]
[[Four-Project Ecosystem]]
[[Wiki Backlog Pattern]]
[[Adoption Guide — How to Use This Wiki's Standards]]
[[Decision: Methodology Framework Design Decisions]]
[[Infrastructure Must Be Reproducible, Not Manual]]
[[LLM Wiki Standards — What Good Looks Like]]
[[Methodology Is a Framework, Not a Fixed Pipeline]]
[[Model: Methodology]]
[[Models Are Built in Layers, Not All at Once]]
[[Never Skip Stages Even When Told to Continue]]
[[Synthesis: awesome-design-md — 58 Design Systems for AI Agents]]
[[The Agent Must Practice What It Documents]]
