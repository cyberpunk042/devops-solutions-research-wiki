---
title: "Methodology Framework"
type: concept
layer: 2
domain: cross-domain
status: synthesized
confidence: authoritative
maturity: growing
created: 2026-04-09
updated: 2026-04-09
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

## Key Insights

- **A methodology model is a named, composable sequence**: A model is not a vague process. It is a named entity with a defined set of stages, per-stage artifact requirements, gate conditions between stages, readiness ranges that map to completion, and protocols governing what is permitted and prohibited at each stage. "Feature-development" is a model. "Research" is a model. "Spike" is a model. Each is defined with the same structural vocabulary but differs in content. Models are not hardcoded in instructions — they are defined in configuration (methodology.yaml) and can be created, modified, and versioned independently of the systems that execute them.

- **Models are selected per-condition, not hardcoded per-project**: The choice of which model to run is driven by conditions: task type, project phase, domain, scale, and current system state. The Task Type Artifact Matrix already implements one selection axis — mapping task type to stage subsets. But selection also operates on project phase: during the Foundation phase of SFIF, the active methodology model emphasizes Document and Design stages; during the Features phase, it emphasizes Implement and Test. Selection can be multi-dimensional: a research task during infrastructure phase in the wiki domain selects a different model than a feature task during features phase in the code domain.

- **Models compose — sequentially, nested, conditionally, and in parallel**: A full project does not run a single model from start to finish. It runs SFIF at the macro level (Scaffold, Foundation, Infrastructure, Features), and WITHIN each SFIF stage, the 5-stage methodology runs for individual tasks. This is nested composition. Sequential composition chains models end-to-end: research model runs first, then feature-development model runs on the research output. Conditional composition branches: if the task is a spike, run the spike model; if it is a module, run the full model. Parallel composition runs multiple models on different tracks simultaneously.

- **Models are adapted per-instance through overrides**: No model runs identically every time. Adaptation mechanisms include: stage overrides (skip Design for hotfixes), artifact overrides (research tasks produce wiki pages, not code), readiness range overrides (a spike maxes at 50% readiness by design), and gate overrides (code projects check compilation and lint; wiki projects check validation and link integrity). The model provides the default; the instance provides the delta. This prevents both over-process on simple work and under-process on complex work.

- **The framework is recursive — the same structure applies at every scale**: At the project level, SFIF is the active model. At the epic level, a scoping model runs. At the module level, the full 5-stage model runs. At the task level, a subset model runs based on task type. At the sub-task level, the same pattern can recurse again. The framework does not change between levels — only the model selection changes. This is the fractal property: zoom in on any level, and you find the same structural vocabulary (stages, artifacts, gates, readiness) instantiated with different content.

- **Multiple methodology tracks coexist on the same project**: A project does not have one methodology — it has several running simultaneously on different tracks. The execution track (superpowers/Claude Code) runs brainstorm, spec, plan, implementation — this is HOW things get built. The PM/observability track (backlog system) runs epics, modules, tasks with stage gates — this is WHAT gets tracked and measured. The knowledge track (wiki) runs ingest, synthesize, evolve, cross-reference — this is WHAT gets learned and retained. These are distinct methodology models operating on different material, at different cadences, with different artifacts, but on the same project. The framework must accommodate all three without forcing them into a single sequence.

- **The quality dimension makes rigor an explicit choice**: Every methodology model has a quality target. The Skyscraper target means full process: every stage runs, every artifact is produced, every gate is checked. The Pyramid target means adapted process: stages may be compressed, artifacts may be lighter, gates may be softer — but the deviations are deliberate and documented. The Mountain anti-pattern means no process: stages are skipped accidentally, artifacts are missing, gates are ignored. The framework does not mandate Skyscraper rigor for everything — it mandates that the quality level is an EXPLICIT parameter, chosen per-situation, not an accidental outcome of time pressure.

- **The wiki defines the framework; projects consume it as instances**: This wiki page is the canonical definition of the meta-system. Each project in the ecosystem adapts it into a concrete configuration: OpenArms has methodology.yaml with task types, stages, and execution modes; OpenFleet has SPEC-TO-CODE and stage-gating via MCP tools; AICP has routing profiles and complexity scoring; the wiki itself has the ingest-synthesize-evolve pipeline. These are all instances of models defined within this framework. Changes to the framework propagate to projects; project-specific adaptations do not change the framework.

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

Real work rarely runs a single model in isolation. Models compose in four ways:

#### Sequential Composition

Model A runs to completion, then Model B starts. The output of Model A becomes the input context for Model B.

Example: A new feature starts with the Research model (understand the domain, survey existing solutions, document findings). When research completes, the Feature Development model starts (design the solution, scaffold the structure, implement the logic, test the result). The research model's wiki pages become input artifacts for the feature development model's Document stage.

Sequential composition is the simplest form. It requires only that models define clear entry conditions (what context they need) and exit conditions (what they produce).

#### Nested Composition

Model A contains Model B as a sub-process within one of its stages.

Example: SFIF runs at the project level. During the Infrastructure stage of SFIF, multiple individual tasks are executed. Each task runs the 5-stage methodology (Document, Design, Scaffold, Implement, Test). The 5-stage model is nested inside one stage of the SFIF model.

Nested composition is the fractal property in action. The outer model defines the macro rhythm; the inner model defines the micro rhythm. The inner model's completion contributes to the outer model's stage exit criteria.

This is where the recursive property becomes concrete. Consider a project that runs:
- **Project level**: SFIF (Scaffold → Foundation → Infrastructure → Features)
  - **Infrastructure stage**: contains 5 modules
    - **Module level**: Full 5-stage model (Document → Design → Scaffold → Implement → Test)
      - **Task level within module**: Task type selects a sub-model (task=3-stage, spike=2-stage, docs=1-stage)

Three levels of nesting, each with its own model, each contributing to the level above.

#### Conditional Composition

The active model is selected by evaluating a condition at a branch point.

Example: An agent evaluates a task. If the task is labeled `bug`, the Bug model runs (skip Document if reproduction steps exist, skip Design, go straight to Scaffold + Implement + Test). If labeled `spike`, the Spike model runs (Document + Design only). If labeled `module`, the Full model runs.

Conditional composition is what makes the framework adaptive. Rather than prescribing one sequence for all situations, the framework defines a decision tree of models and the conditions that select between them.

Conditional composition can also operate mid-model. Within the 5-stage model, a gate between Design and Scaffold might evaluate: "Is this a pure architecture change? If yes, skip Scaffold and Implement, go directly to Test (architecture review)." This is intra-model conditional branching.

#### Parallel Composition (Multi-Track)

Multiple models run simultaneously on different tracks, against different material, at different cadences.

This is not a theoretical possibility — it is the actual operating condition of every project in the ecosystem. On any given project, RIGHT NOW:

- The **execution track** runs the superpowers model: Brainstorm → Spec → Plan → Implementation. This governs how work gets built.
- The **PM track** runs the backlog model: Epics → Modules → Tasks, with stage gates and readiness scores. This governs what work gets tracked.
- The **knowledge track** runs the wiki model: Ingest → Synthesize → Cross-Reference → Evolve. This governs what gets learned.

These three tracks interact but do not merge. A task in the PM track triggers execution in the execution track. A finding in the execution track feeds the knowledge track. A synthesis in the knowledge track informs the PM track's next sprint. The interactions are FEEDS INTO relationships, not sequential dependencies.

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

The single biggest error in thinking about methodology is assuming a project has ONE methodology. Every non-trivial project has at least three concurrent methodology tracks:

#### Execution Track

**Model**: Brainstorm → Spec → Plan → Implementation (superpowers model)
**Material**: Code, configurations, infrastructure
**Artifacts**: Brainstorm documents, spec files, implementation plans, pull requests
**Cadence**: Per-feature or per-task, driven by the backlog
**Enforcement**: CLAUDE.md instructions, plan file checksums, verification gates
**Purpose**: HOW things get built — the craft of producing correct, high-quality output

This track answers: "Given a thing to build, what is the process for building it well?"

#### PM / Observability Track

**Model**: Epics → Modules → Tasks with stage gates and readiness (backlog model)
**Material**: Work items, status, dependencies, progress
**Artifacts**: Backlog entries, status reports, stage-gate transitions, readiness scores
**Cadence**: Continuous, updated on every state change
**Enforcement**: Backlog hierarchy rules, status propagation, readiness aggregation
**Purpose**: WHAT gets tracked — the structure that makes work visible and measurable

This track answers: "What is the state of the project, what is done, what is next, what is blocked?"

#### Knowledge Track

**Model**: Ingest → Synthesize → Cross-Reference → Evolve (wiki model)
**Material**: Research, documentation, patterns, lessons, decisions
**Artifacts**: Wiki pages, cross-domain connections, pattern instances, evolved knowledge
**Cadence**: Periodic, triggered by new information or gaps
**Enforcement**: Post-chain validation, quality gates, lint checks, overlap detection
**Purpose**: WHAT gets learned — the intelligence layer that informs all other tracks

This track answers: "What do we know, what are the patterns, what should we do differently?"

#### Track Interactions

The tracks are not independent silos. They interact through defined interfaces:

- **PM → Execution**: A task in the backlog triggers an execution cycle. The PM track defines WHAT; the execution track defines HOW.
- **Execution → Knowledge**: A finding during implementation (a pattern discovered, a decision made, a lesson learned) feeds into the knowledge track for synthesis.
- **Knowledge → PM**: A gap analysis from the knowledge track generates new backlog items. A pattern recognition changes the priority of existing items.
- **Knowledge → Execution**: A synthesized best practice changes the execution model. A documented anti-pattern adds a new prohibited action to a stage.

These interactions are FEEDS INTO relationships. They are not sequential dependencies (you do not wait for knowledge synthesis before executing the next task). They are continuous flows of information between concurrent processes.

### The Quality Dimension

The Skyscraper, Pyramid, Mountain analogy is not just an architectural quality assessment — it is a methodology parameter. Every model execution has a quality target, and that target affects every aspect of the model.

**Skyscraper execution**: Full process. Every stage runs. Every artifact is produced to spec. Every gate is checked against full criteria. Readiness targets 100%. This is appropriate for: core infrastructure, production-critical features, foundational decisions, canonical documentation. The cost is time and thoroughness. The benefit is structural integrity that compounds — future work builds on a solid base.

**Pyramid execution**: Adapted process. Stages may be compressed (Document and Design merge into a single design sketch). Artifacts may be lighter (a bullet-point summary instead of a full wiki page). Gates may be softer (self-review instead of peer review). Readiness targets 85-95%. This is appropriate for: most everyday work, features built on established infrastructure, well-understood domains, time-constrained delivery. The cost is some structural debt. The benefit is pragmatic delivery that still maintains enough structure to remain maintainable.

**Mountain execution (the anti-pattern)**: No process. Stages are skipped accidentally, not deliberately. Artifacts are missing or incomplete. Gates are ignored. Readiness is not tracked. This is appropriate for: NOTHING, ever. The mountain is not a valid quality target — it is what happens when no target is set. The framework exists precisely to prevent mountain execution by making the quality choice explicit.

The critical innovation is that the quality dimension is a PARAMETER on model execution, not a separate assessment performed afterward. Before executing a model, the quality target is declared:

- "This module is core infrastructure. Skyscraper."
- "This bug fix is straightforward. Pyramid."
- "This spike is exploration. Pyramid with 50% readiness cap."

The declaration happens BEFORE work begins and shapes the entire execution. It is not a retrospective judgment.

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

- How should the selection engine be formalized? Is a simple condition-to-model lookup table sufficient, or does multi-dimensional selection require a scoring/priority system?
- Should model composition be declarative (defined in configuration) or imperative (defined in code that evaluates conditions at runtime)?
- How do models handle mid-execution changes? If a task initially selected as a `task` type reveals module-level complexity during the Document stage, can the model be re-selected without losing progress?
- What is the right granularity for the quality dimension? Is skyscraper/pyramid/mountain sufficient, or should there be intermediate levels (e.g., "reinforced pyramid" for work that is mostly adapted but with specific skyscraper-grade stages)?
- How do parallel tracks synchronize on milestone boundaries? Should there be explicit sync points where all three tracks must align before the project advances to the next SFIF phase?
- Can the framework itself be described as a model? Is there a meta-meta level where the framework definition process follows its own stages (Document the framework → Design the vocabulary → Scaffold the configuration schema → Implement the selection engine → Test against real projects)?
- How should model versioning work? When a project evolves its methodology.yaml, should there be a compatibility check against the framework version?

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
- IMPLEMENTS: Flexible Methodology Framework directive (raw/notes/2026-04-09-user-directive-flexible-methodology-framework.md)
- IMPLEMENTS: [[Scaffold → Foundation → Infrastructure → Features]] (raw/notes/2026-04-09-user-directive-raw-idea-flow-patterns-standards.md)

## Backlinks

[[[[Stage-Gate Methodology]] (the 5-stage model is an instance within this framework)]]
[[[[Task Type Artifact Matrix]] (task-type-to-model selection is one selection axis)]]
[[[[Execution Modes and End Conditions]] (execution modes are model parameters)]]
[[[[Scaffold → Foundation → Infrastructure → Features]] (SFIF is the project-level model)]]
[[[[Spec-Driven Development]] (SDD is the execution track's methodology model)]]
[[[[Skyscraper]]
[[Pyramid]]
[[Mountain]] (the quality dimension of model execution)]]
[[[[Task Lifecycle Stage-Gating]] (stage-gating is the enforcement mechanism for models)]]
[[[[Backlog Hierarchy Rules]] (the PM track model that structures work items)]]
[[[[LLM Wiki Pattern]] (the knowledge track model for wiki-based knowledge management)]]
[[[[Second Brain Architecture]] (the knowledge track operates within the second brain structure)]]
[[[[Progressive Distillation]] (maturity progression is a model within the knowledge track)]]
[[[[Four-Project Ecosystem]] (the ecosystem is the highest-level instance of the framework)]]
[[[[Wiki Backlog Pattern]] (PM track methodology feeds backlog structure)]]
[[Flexible Methodology Framework directive (raw/notes/2026-04-09-user-directive-flexible-methodology-framework.md)]]
[[[[Scaffold → Foundation → Infrastructure → Features]] (raw/notes/2026-04-09-user-directive-raw-idea-flow-patterns-standards.md)]]
[[Adoption Guide — How to Use This Wiki's Standards]]
[[Infrastructure Must Be Reproducible, Not Manual]]
[[LLM Wiki Standards — What Good Looks Like]]
[[Model: Methodology]]
[[Never Skip Stages Even When Told to Continue]]
[[The Agent Must Practice What It Documents]]
