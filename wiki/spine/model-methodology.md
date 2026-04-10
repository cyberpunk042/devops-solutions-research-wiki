---
title: "Model: Methodology"
type: concept
domain: cross-domain
layer: spine
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
  - id: src-openarms-methodology-evolution
    type: documentation
    file: raw/articles/openarms-methodology-evolution-2026-04-09.md
    title: "OpenArms Methodology Evolution — 7 Bugs, 6 Versions"
    ingested: 2026-04-09
  - id: src-openarms-integration-sprint
    type: documentation
    file: raw/articles/openarms-integration-sprint-learnings.md
    title: "OpenArms Integration Sprint Learnings"
    ingested: 2026-04-09
tags: [methodology, model, stage-gate, task-types, composable, backlog, execution-modes, framework, spine, flexible, multi-track, multi-model]
---

# Model: Methodology

## Summary

The Methodology model defines a flexible FRAMEWORK for defining, selecting, composing, and adapting work processes. It is NOT one fixed pipeline — it is a system that CONTAINS multiple named methodology models (Feature Development, Research, Knowledge Evolution, Hotfix, Documentation, and more), selects between them based on conditions (task type, project phase, domain, scale, urgency), composes them (sequentially, nested, conditionally, in parallel), and adapts them per-instance through overrides. Three parallel tracks run on every project simultaneously: execution (how things get built), PM (what gets tracked), and knowledge (what gets learned). Where the [[Model: LLM Wiki]] defines WHAT the wiki IS, this model defines HOW all work proceeds. The canonical definition lives in [[Methodology Framework]]. The executable configuration lives in `wiki/config/methodology.yaml` and `wiki/config/agent-directive.md`.

## Key Insights

- **Multiple models, not one pipeline.** Feature Development has 5 stages. Research has 2. Knowledge Evolution has 4 with different stage names. Hotfix has 2. These are INDEPENDENT models, not subsets of one sequence. A project may use all of them at different times for different work.

- **Conditions select which model runs.** Task type is one condition. But also: project phase (Foundation emphasizes Document+Design; Features emphasizes Implement+Test), domain (code vs knowledge vs infrastructure), scale (single function vs new module), urgency (critical bug → Hotfix model), current state (greenfield vs legacy). Selection is multi-dimensional — all conditions evaluate simultaneously.

- **Models compose at every scale.** SFIF runs at project level. Inside each SFIF stage, task-level models run. Inside a task, stages execute. This is fractal — the same vocabulary (stages, gates, artifacts, readiness) at every level. Plus: three tracks run in PARALLEL on every project (execution, PM, knowledge) — not one sequence.

- **Stage boundaries are enforced, not suggested.** ALLOWED and FORBIDDEN artifact lists per stage. Document may not produce code. Scaffold may not implement business logic. Implement MUST wire into the runtime. This was learned from real failures — OpenArms Bug 5 (scaffold produced 135 lines of business logic) and Bug 6 (2,073 lines of orphaned code nobody imported).

- **The quality dimension is an explicit parameter.** Skyscraper (full process), Pyramid (deliberate compression), Mountain (accidental chaos). The choice is made per-situation, not accidentally.

- **The methodology was hardened by 7 real bugs in one day of autonomous operation.** Every design decision traces to a failure that proved it necessary. This is not theory — it is battle-tested from OpenArms' first autonomous agent run.

## Deep Analysis

### What Is a Methodology Model

A methodology model is a named, first-class entity defined in configuration (not hardcoded in logic). Every model has:

| Component | What it defines | Example |
|-----------|----------------|---------|
| **Name** | Unique identifier | `feature-development`, `research`, `hotfix` |
| **Stages** | Ordered sequence of phases | document → design → scaffold → implement → test |
| **Artifacts** | What each stage must produce | Wiki page, spec, type definitions, working code, passing tests |
| **Gates** | Transition rules between stages | Automatic, human-reviewed, score-based |
| **Protocols** | Per-stage ALLOWED and FORBIDDEN lists | Scaffold ALLOWED: types, schemas. FORBIDDEN: business logic. |
| **Parameters** | Configurable values | Readiness ranges, max retries, commit style |

A model is DATA. It is defined in `methodology.yaml`, not embedded in code. This means models can be created, versioned, compared across projects, and selected at runtime.

For the full structural definition, see [[Methodology Framework]].

### The Model Catalog

Nine named methodology models. Each is a DIFFERENT stage sequence solving a different problem. Each entry shows: what it is, its stages with per-stage artifacts, when it's selected, and a real instance from the ecosystem.

---

#### Feature Development

> [!info] **Stages:** document → design → scaffold → implement → test
> The full 5-stage model for complex work. Used when the solution isn't already known and needs to be designed, scaffolded, built, and verified.

| Stage | What you produce | Gate |
|-------|-----------------|------|
| document | Wiki page mapping existing code + gap analysis | Page exists with Summary + gaps identified |
| design | Spec or design decision document, type sketches IN DOCS | Spec reviewed and approved |
| scaffold | Type definitions, schemas, .env entries, empty test files | Types compile, no business logic in diff |
| implement | Working code wired into runtime, wiki pages, skills | Code compiles, lint passes, ≥1 runtime file imports new code |
| test | All tests pass, manual verification | 0 test failures, health check clean |

> [!abstract] **Selected when**
> task_type = `epic`, `module`, or `refactor`. Any complex work where the solution isn't already known.

> [!example]- **Real instance: Building the wiki backlog system**
> 1. **Document** — Read OpenArms methodology model, understand what we need, map the gap between our wiki and OpenArms' backlog structure
> 2. **Design** — Brainstorm with user (5 design sections, each approved), spec written to `docs/superpowers/specs/`
> 3. **Scaffold** — Schema changes (4 new types, 7 new statuses, 5 new enums), directory structure (`wiki/backlog/`, `wiki/log/`, `wiki/config/`), methodology.yaml created
> 4. **Implement** — Python validation, pipeline `backlog` command, `/backlog` + `/log` slash commands, `wiki_backlog` + `wiki_log` MCP tools
> 5. **Test** — `pipeline chain health` clean, `pipeline backlog` shows 2 epics + 1 task, 0 validation errors

---

#### Research

> [!info] **Stages:** document → design
> Investigation without implementation. Produces understanding and options, never code. Capped at 50% readiness — 50% IS completion.

| Stage | What you produce | Gate |
|-------|-----------------|------|
| document | Wiki page synthesizing findings, source mapping | Page with Summary + Key Insights |
| design | Options document, decision recommendation, implications | Options presented to operator |

> [!abstract] **Selected when**
> task_type = `spike` or `research`. Investigation needed, no code output expected.

> [!example]- **Real instance: Researching second brain / PKM methodologies**
> 1. **Document** — Read Zettelkasten + PARA + hybrid approaches from web research. Created [[Second Brain Architecture]] with full mapping of PARA buckets and Zettelkasten principles to wiki structure.
> 2. **Design** — Proposed how wiki maps to both methodologies. Identified 5 gaps: FAQs per domain, comparison matrices, review cadence, personal annotations, task management integration.

> [!tip] **Why it stops at design**
> Research produces UNDERSTANDING, not implementation. If the research leads to building something, that becomes a NEW task using a different model (Feature Development or Documentation). The research model's output becomes the next model's input — this is sequential composition.

---

#### Knowledge Evolution

> [!info] **Stages:** document → implement
> Generate higher-layer pages (lessons, patterns, decisions) from existing wiki knowledge. No scaffold or design — the "design" is the existing knowledge being distilled.

| Stage | What you produce | Gate |
|-------|-----------------|------|
| document | Cross-reference existing pages, identify convergence / insight | Candidate identified with source pages listed |
| implement | Complete evolved page (lesson, pattern, or decision) | Page passes validation, ≥0.25 ratio to sources, real evidence |

> [!abstract] **Selected when**
> task_type = `evolve`. Existing pages converge on an insight worth distilling.

> [!example]- **Real instance: Generating "CLI Tools Beat MCP for Token Efficiency" lesson**
> 1. **Document** — Cross-reference accuracy tips source, harness engineering source, Playwright comparison. Identify the convergence: three independent sources all say CLI beats MCP.
> 2. **Implement** — Write the 122-line lesson page with 8 evidence items from 4 independent sources. Each evidence item has a bold source label, a specific claim with data, and a sourcing parenthetical.

---

#### Documentation

> [!info] **Stages:** document
> Single-stage model. Done when the document is written and passes quality gates.

| Stage | What you produce | Gate |
|-------|-----------------|------|
| document | Wiki page, guide, spec, directive log entry | Passes quality gates (Summary ≥30 words, frontmatter valid) |

> [!abstract] **Selected when**
> task_type = `docs`. Writing or updating documentation only.

> [!example]- **Real instance: Logging an operator directive**
> User says something → create `wiki/log/` entry with verbatim quote + interpretation → validate frontmatter → commit. One stage, one artifact.

---

#### Bug Fix

> [!info] **Stages:** document → implement → test
> Restore correct behavior. No design stage — bug fixes should NOT introduce new architecture.

| Stage | What you produce | Gate |
|-------|-----------------|------|
| document | Understanding of what's broken and why | Root cause identified in writing |
| implement | The fix — code change, config change, or content correction | Fix applied, compiles/validates |
| test | Verification the fix works AND nothing else broke | Health check clean, regression-free |

> [!abstract] **Selected when**
> task_type = `bug`. Something is broken and needs to be restored to correct behavior.

> [!example]- **Real instance: Fixing the sync service startup**
> 1. **Document** — Sync daemon crashes on start. Root cause: `cmd.exe` not available in systemd environment, `get_win_user()` fails silently.
> 2. **Implement** — Add `WIKI_SYNC_TARGET` env var to service template, resolve at install time instead of runtime auto-detection.
> 3. **Test** — Reinstall service via `setup.py --services wiki-sync`, verify `systemctl --user status wiki-sync` shows active, verify files synced to Windows.

---

#### Refactor

> [!info] **Stages:** document → scaffold → implement → test
> Restructure without changing behavior. Skips design — the target structure is defined in the document stage.

| Stage | What you produce | Gate |
|-------|-----------------|------|
| document | Current structure mapped, target structure defined | Gap between current and target documented |
| scaffold | New directory structure, new type definitions, empty files | Structure exists, no logic moved yet |
| implement | Code/content moved into new structure | Everything compiles/validates in new structure |
| test | Behavior unchanged, all tests pass | Regression suite clean |

> [!abstract] **Selected when**
> task_type = `refactor`. Restructuring without changing behavior.

> [!example]- **Real instance: Renaming `config/schema.yaml` → `config/wiki-schema.yaml`**
> 1. **Document** — Identify all references: tools/pipeline.py, tools/validate.py, tools/common.py, CLAUDE.md
> 2. **Scaffold** — Create the new file name via `mv`
> 3. **Implement** — Update all references with sed, verify pipeline still finds the schema
> 4. **Test** — `pipeline post` passes, no broken imports, validation clean

---

#### Hotfix

> [!info] **Stages:** implement → test
> Emergency fix when the problem and solution are already understood. Skip all other stages.

| Stage | What you produce | Gate |
|-------|-----------------|------|
| implement | The fix | Applied and compiles/validates |
| test | Verification | Works and no regressions |

> [!warning] **Selected when**
> Urgency = critical AND the problem and solution are already understood. This is an EXPLICIT choice to operate at Pyramid tier — you're skipping stages knowingly, not accidentally.

> [!example]- **Real instance: Fixing the argparse `--top` / `--topic` prefix collision**
> The bug was immediately clear — argparse abbreviation matching consumed `--top` as `--topic`.
> 1. **Implement** — Add `allow_abbrev=False` to the ArgumentParser constructor
> 2. **Test** — Verify `--top 2` now scaffolds exactly 2 candidates, not 10
>
> Two commits, no documentation needed. The fix was obvious; the process was correctly compressed.

---

#### Ingestion Pipeline

> [!info] **Stages:** ingest → synthesize → cross-reference → evolve
> The knowledge track's model. **Completely different stage names** — this is NOT a subset of the 5-stage Feature Development model.

| Stage | What you produce | Gate |
|-------|-----------------|------|
| ingest | Raw file saved to raw/ | File exists in raw/articles/ or raw/transcripts/ |
| synthesize | Source-synthesis page in wiki/sources/ | Page ≥0.25 ratio to raw, passes validation |
| cross-reference | Updated relationships, new connections identified | pipeline crossref shows 0 missing backlinks |
| evolve | Higher-layer pages (lessons, patterns, decisions) | Evolved pages pass quality gates |

> [!abstract] **Selected when**
> domain = knowledge, operation = ingestion. Runs on the knowledge track.

> [!example]- **Real instance: Ingesting the context-mode repo**
> 1. **Ingest** — `pipeline fetch` saved 1,057-line README to `raw/articles/`
> 2. **Synthesize** — Read FULL source with multiple offsets. Created 254-line source-synthesis page covering all 12 platforms, FTS5/BM25 knowledge base, session continuity, benchmarks.
> 3. **Cross-reference** — Updated MCP vs CLI decision, CLI lesson, context-aware loading pattern with new evidence.
> 4. **Evolve** — Not triggered this cycle (synthesis was the primary output).

> [!warning] **Depth verification applies here**
> During the synthesize stage, you MUST read the actual THING, not just the description. The first attempt at context-mode produced a 60-line shallow page from the first chunk. The rewrite (after depth verification) produced a 254-line deep synthesis. See [[Never Synthesize from Descriptions Alone]].

---

#### Project Lifecycle (SFIF)

> [!info] **Stages:** scaffold → foundation → infrastructure → features
> The project-level MACRO model. Other models run INSIDE its stages. See [[Scaffold → Foundation → Infrastructure → Features]].

| Stage | What you produce | Gate |
|-------|-----------------|------|
| scaffold | Project structure, tech stack, AI config files | Directory exists, CLAUDE.md written, schema defined |
| foundation | Core modules, design system, build entry point | Single entry point works, architecture documented |
| infrastructure | Common components others depend on, basic interface | Build produces output, base is ready for features |
| features | Specialized product features | Features work end-to-end |

> [!abstract] **Selected when**
> scale = project. This runs at macro level; task-level models run inside.

> [!example]- **Real instance: This research wiki's own lifecycle**
> 1. **Scaffold** — CLAUDE.md, raw/, wiki/, tools/ directories, Python venv, tech stack chosen
> 2. **Foundation** — tools/common.py, config/wiki-schema.yaml, config/templates/, validation tooling
> 3. **Infrastructure** — tools/pipeline.py (13 chains), MCP server (17 tools), sync service, watcher daemon, evolve engine
> 4. **Features** — Evolution pipeline, backlog system, model-building skill, 14 named models, standards documents

> [!tip] **The recursive property**
> Inside the Infrastructure stage, building the backlog system ran the Feature Development model. Inside that, individual tasks ran their subset models. Three levels of nesting, each with its own methodology model. This is [[Methodology Framework]]'s fractal property in practice.

### Model Selection — How Conditions Pick a Model

Selection is not a lookup table — it's a multi-dimensional evaluation. Here's how it works in practice:

**The 5 condition dimensions:**

| Dimension | What it evaluates | How it affects selection |
|-----------|------------------|------------------------|
| **Task type** | What kind of work is this? | `spike` → Research model. `docs` → Documentation model. `module` → Feature Development model. |
| **Project phase** | Where is the project in its lifecycle? | Foundation phase → emphasize Document + Design. Features phase → emphasize Implement + Test. |
| **Domain** | What kind of system is this? | Code domain → Feature Development family. Knowledge domain → Ingestion Pipeline family. |
| **Scale** | How big is this change? | Single function → skip Document (context already known). New subsystem → full model + design review gate. |
| **Urgency/State** | How urgent? What's the current codebase state? | Critical production bug → Hotfix model. Legacy codebase at Mountain tier → Pyramid quality target. |

> [!example]- **Worked example: "Research how OpenArms does methodology enforcement"**
> **Evaluating conditions:**
> | Dimension | Value | Why |
> |-----------|-------|-----|
> | task_type | `research` | No code output expected |
> | phase | Foundation | Wiki is still building its knowledge base |
> | domain | knowledge-systems | Wiki research, not code |
> | scale | single topic | One investigation |
> | urgency | normal | Not blocking anything |
>

> [!success] **Result → Research model** (document → design)
> The agent reads OpenArms sources (document stage), produces a wiki page synthesizing findings (document artifact), then proposes design implications for the wiki's own methodology (design stage). Stops at 50% readiness. Does NOT scaffold, implement, or test anything.

> [!example]- **Another example: "Build the backlog system for this wiki"**
> | Dimension | Value | Why |
> |-----------|-------|-----|
> | task_type | `epic` | Large initiative |
> | phase | Infrastructure | Wiki has its foundation, adding infra |
> | domain | tools-and-platforms | Python tooling |
> | scale | new subsystem | Schema, directories, pipeline, commands, MCP |
> | urgency | normal | Not a hotfix |
>
> [!success] **Result → Feature Development model** (all 5 stages)
> Document → Design (brainstorm → spec) → Scaffold (schema changes, directory structure) → Implement (Python code, commands, MCP tools) → Test (pipeline health check). Each stage with its own commit, artifacts, and gate.

### Model Composition — How Models Chain, Nest, and Branch

Real work never runs one model in isolation. Four composition modes:

> [!info] **Composition modes at a glance**
> | Mode | How it works | Example |
> |------|-------------|---------|
> | **Sequential** | One model's output feeds the next model's input | Research → Feature Development |
> | **Nested** | Models run inside other models' stages | SFIF → Feature Dev → task subsets |
> | **Conditional** | Conditions branch to completely different models | `bug` → Bug Fix, `spike` → Research |
> | **Parallel** | Multiple tracks run simultaneously | Execution + PM + Knowledge |

**Sequential:** Research model runs first, produces a spec. Feature Development model runs next, consuming the spec. The "Build the backlog system" example above ACTUALLY ran this way — first a research phase (reading OpenArms methodology), then a brainstorm/spec phase, then implementation.

**Nested:** SFIF runs at project level. Inside SFIF's Infrastructure stage, the backlog system epic ran the Feature Development model. Inside that epic, individual tasks ran subset models (task = scaffold+implement+test). Three levels of nesting, each with its own model.

**Conditional:** An agent picks up a backlog task. task_type=`bug` → Bug Fix model. task_type=`spike` → Research model. task_type=`module` → Feature Development model. The condition BRANCHES to completely different models, not different subsets of one pipeline.

**Parallel (multi-track):** Three tracks running simultaneously on THIS project RIGHT NOW:

| Track | Model | What it does | Artifacts |
|-------|-------|-------------|-----------|
| **Execution** | Brainstorm → Spec → Plan → Implementation | HOW things get built | Specs, plans, code, wiki pages |
| **PM** | Epics → Modules → Tasks with stage gates | WHAT gets tracked | Backlog entries, readiness scores |
| **Knowledge** | Ingest → Synthesize → Cross-Reference → Evolve | WHAT gets learned | Source pages, concept pages, lessons, patterns |

These interact but never merge: PM triggers execution, execution feeds knowledge, knowledge informs PM.

### Stage Boundaries — ALLOWED and FORBIDDEN

Stage names alone do not prevent violations. Each stage needs explicit ALLOWED and FORBIDDEN artifact lists. This was proven by OpenArms Bug 5: the agent produced 135 lines of business logic during the scaffold stage because nothing explicitly said "business logic is FORBIDDEN in scaffold."

#### Scaffold

> [!success] **ALLOWED**
> Type definitions, static constants, schema objects, `.env` entries, empty test files with placeholder assertions.

> [!warning] **FORBIDDEN**
> Business logic (parsers, resolvers, evaluators), env var readers with parsing logic, functions beyond stub bodies, real test implementations.

#### Implement

> [!success] **ALLOWED**
> Business logic, helper functions, modifying existing files to import new code.

> [!tip] **REQUIRED**
> ==At least one existing runtime file must import the new code.== (OpenArms Bug 6: 2,073 lines orphaned because nothing imported them.)

> [!warning] **FORBIDDEN**
> Modifying test files, writing test assertions.

#### Test

> [!success] **ALLOWED**
> Fill scaffolded tests, add edge cases.

> [!tip] **REQUIRED**
> 0 test failures before marking done.

> [!warning] **FORBIDDEN**
> Proceeding with failing tests.

These lists are defined in `methodology.yaml` per stage. They adapt per domain — a wiki project's "implement" ALLOWED list includes "wiki pages, skills, commands" instead of "business logic functions."

### What Goes Wrong Without This — 7 Bugs From Real Operation

Every design decision in this model traces to a real failure. These 7 bugs were found during OpenArms' first day of autonomous agent operation (2026-04-09). Each bug led to a methodology version bump:

> [!bug]- **Bug 1: Binary status** → Design input: stage-level tracking (v2)
> Tasks were done/not-done. No stage tracking. Agent checked "Done When" boxes without verification and skipped from "active" to "done" after one stage.
> **Fix:** Added `task_type`, `current_stage`, `readiness`, `stages_completed` to frontmatter. Reset 22 tasks. 6 moved from "done" back to "in-progress."

> [!bug]- **Bug 2: Epic status manual** → Design input: computed hierarchy (v3)
> Epics could be marked "done" with zero children complete.
> **Fix:** Status/readiness computed from children. Max agent-settable = "review." Human confirms "done."

> [!bug]- **Bug 3: Rogue task creation** → Design input: operator-only task creation (v3)
> Agent ignored existing tasks and created its own, reusing IDs (T026-T029). Naming collisions and diverged backlog.
> **Fix:** "Pick from existing tasks ONLY. Do NOT create new task files." Task creation is operator responsibility.

> [!bug]- **Bug 4: Lost files** → Design input: commit immediately (v3)
> Write tool succeeded but files vanished — destructive `git revert` killed untracked files in shared workspace.
> **Fix:** "Commit immediately after creating files. Never destructive git without git status."

> [!bug]- **Bug 5: Stage boundary violation** → Design input: ALLOWED/FORBIDDEN (v4)
> Scaffold produced 135-line env reader with business logic. Test marked done with 1 failing test.
> **Fix:** Added explicit ALLOWED/FORBIDDEN lists per stage. Gate requires passing commands.

> [!bug]- **Bug 6: Orphaned implementation** → Design input: integration requirement (v5)
> 2,073 lines of production code — network rules, cost tracking, hook events. None imported by runtime. Tests pass ≠ feature works.
> **Fix:** Implement MUST wire into runtime. Done When must name the specific consumer file.

> [!bug]- **Bug 7: Unreadable logs** → Design input: observability tooling (v5)
> Raw JSON stream events (95% token chunks). Impossible to monitor live or produce reports.
> **Fix:** Built `agent-report.py` (stream aggregation, stage tracking, compliance checking, cost per stage).

> [!abstract] **Methodology version history**
> v1 (initial) → v2 (stage tracking) → v3 (hierarchy + no rogue tasks) → v4 (ALLOWED/FORBIDDEN) → v5 (integration requirement) → v6 (bridge pattern + compliance). **Six versions in one day** — each hardened by a real failure.

### Model Adaptation — Overrides Per Instance

Every model definition is a template. Every execution is an instance with potential overrides:

**Stage overrides:** Hotfix skips Document and Design. Security-sensitive work adds a Security Review stage. Research may run Design before Document.

**Artifact overrides:** Research produces wiki pages, not code. A small task needs only a summary, not a full gap analysis. Compliance-sensitive work adds a risk assessment at every stage.

**Readiness overrides:** Spike caps at 50%. POC caps at 80%. MVP targets 95%. Production targets 100%.

**Gate overrides:** Code projects: compilation + lint + tests. Wiki projects: validation + links + word count. Infrastructure: provisioning + health checks. Same gate STRUCTURE, domain-specific CONDITIONS.

**Protocol overrides:** OpenArms: one-commit-per-stage. OpenFleet: MCP tool blocking. This wiki: post-chain validation. Each project adapts enforcement to its tooling.

### The Quality Dimension

Every model instance has a quality target. The choice is EXPLICIT — made per-situation, never accidental.

> [!success] **Skyscraper** — the full process
> Every stage runs, every artifact produced, every gate checked. For complex or high-stakes work. This is the default expectation for epics and new subsystems.

> [!warning] **Pyramid** — deliberate compression
> Stages may be compressed, artifacts lighter, gates softer. Deviations are DELIBERATE and documented. For pragmatic delivery under constraints. A hotfix at Pyramid tier is a valid, honest choice.

> [!bug]- **Mountain** — accidental chaos (the anti-pattern)
> Stages skipped accidentally, artifacts missing, gates ignored. Not a choice — a failure mode. The difference between Pyramid and Mountain is INTENT: Pyramid documents why stages were skipped; Mountain doesn't notice they were skipped.

==The failure mode is not choosing Pyramid — it is accidentally producing Mountain-tier work because quality level was never an explicit decision.==

See [[Skyscraper, Pyramid, Mountain]].

### How to Adopt

> [!info] **What you need**
> 1. `methodology.yaml` — defines your models (stages, task types, modes, end conditions). Start by copying from `wiki/config/methodology.yaml` and adapting.
> 2. `agent-directive.md` — defines the work loop, stage enforcement rules, git management, quality gates. Start by copying from `wiki/config/agent-directive.md` and adapting commands for your project.

> [!warning] **INVARIANT — never change these**
> - Stage boundaries are hard (ALLOWED/FORBIDDEN enforced)
> - Readiness derived from stage completion, not subjective assessment
> - Backlog hierarchy: epic → module → task, readiness flows upward
> - One commit per stage
> - Models are DATA defined in config, not CODE

> [!tip] **PER-PROJECT — always adapt these**
> - Which models exist and their stage sequences
> - Per-stage artifact requirements (code vs wiki pages vs Terraform)
> - Gate mechanisms (hooks vs CI vs manual review vs post-chain)
> - Which task types exist
> - Execution mode defaults and end conditions

> [!bug]- **What goes wrong if you skip this**
> See the 7 bugs above. Every one was found within hours of starting autonomous agent operation. Without explicit methodology: binary status (Bug 1), unchecked epics (Bug 2), rogue tasks (Bug 3), lost files (Bug 4), stage violations (Bug 5), orphaned code (Bug 6), invisible work (Bug 7). The methodology exists because these failures HAPPENED.

### Real Example: End-to-End Task Execution

Here's how a single task flows through the methodology, from selection to completion.

> [!info] **Task: "Tune the evolution scorer"** (from this wiki's actual history)
> task_type=`task`, domain=tools, scale=focused change in one file. Conditions select the **Feature Development model**, subset for task scale: scaffold → implement → test.

> [!example]- **Scaffold stage**
> | | |
> |---|---|
> | **ALLOWED** | Modify the signal weights dict, add the `_GENERIC_TAGS` set, change the tag co-occurrence threshold |
> | **FORBIDDEN** | Rewrite the scoring algorithm, add new signal functions |
> | **Artifact** | Modified `SIGNAL_WEIGHTS` in evolve.py, added `_GENERIC_TAGS` filter |
> | **Gate** | `pipeline evolve --score` still runs without errors |
> | **Commit** | `feat(evolve): tune scorer weights and add generic tag filter` |

> [!example]- **Implement stage**
> | | |
> |---|---|
> | **ALLOWED** | Update the deduplication logic, change overlap thresholds |
> | **REQUIRED** | The scorer produces different output (verified by running `--score`) |
> | **Artifact** | Rewritten `_deduplicate()` function with source overlap check |
> | **Gate** | `pipeline evolve --score --top 10` shows diverse candidates (not all tag-pair patterns) |
> | **Commit** | `feat(evolve): improve dedup — check source overlap with evolved pages` |

> [!example]- **Test stage**
> | | |
> |---|---|
> | **Run** | `pipeline evolve --score --top 10` — verify diverse candidates |
> | **Run** | `pipeline post` — verify 0 validation errors |
> | **Verify** | Candidates include convergence lessons, hub pages, open-question decisions (not just tag pairs) |
> | **Commit** | `feat: tune evolution scorer — better weights, dedup, and generic tag filter` |

> [!success] **Completion**
> `stages_completed=[scaffold, implement, test]`, `readiness=100`, `status=done`. Parent epic readiness recalculated from children.

### Relationship to Other Models

> [!abstract] **Governance, not peer relationship**
> The Methodology model GOVERNS all other models in the wiki. Every other model operates WITHIN this framework. This is the super-model.

| Model | What it defines | How Methodology governs it |
|-------|----------------|---------------------------|
| [[Model: LLM Wiki]] | WHAT the wiki IS | HOW wiki work proceeds through stages |
| [[Model: Claude Code]] | The agent's capabilities | How those capabilities are sequenced and gated |
| [[Model: Skills, Commands, and Hooks]] | The tooling | WHEN each tool is permitted (per-stage protocols) |
| [[Model: Ecosystem Architecture]] | The project topology | How work flows through that topology |

## Open Questions

> [!question] **Should model selection be declarative or dynamic?**
> Currently selection is implicit in task_type mapping. Could it be encoded as a declarative config (condition → model lookup table)? Or does the multi-dimensional evaluation require dynamic logic? (Requires: testing a formal selection engine)

> [!question] **Can stage gates be fully automated?**
> OpenArms' autonomous agent run suggests yes for routine tasks but no for architectural decisions. Where is the boundary between human-gated and auto-gated stages? (Requires: more autonomous operation data)

> [!question] **What is the minimum viable methodology?**
> A project that just wants stage tracking without the full framework — what subset works? `methodology.yaml` with 2 models (Feature Dev + Hotfix), `agent-directive.md` with the work loop, and done? (Requires: a minimal adoption test)

## Relationships

- GOVERNS: [[Model: LLM Wiki]], [[Model: Claude Code]], [[Model: Ecosystem Architecture]], [[Model: Skills, Commands, and Hooks]], [[Model: Second Brain]]
- BUILDS ON: [[Methodology Framework]]
- BUILDS ON: [[Stage-Gate Methodology]]
- BUILDS ON: [[Task Type Artifact Matrix]]
- BUILDS ON: [[Backlog Hierarchy Rules]]
- BUILDS ON: [[Execution Modes and End Conditions]]
- BUILDS ON: [[Skyscraper, Pyramid, Mountain]]
- RELATES TO: [[Spec-Driven Development]]
- RELATES TO: [[Scaffold → Foundation → Infrastructure → Features]]
- RELATES TO: [[Adoption Guide — How to Use This Wiki's Standards]]
- IMPLEMENTS: wiki/config/methodology.yaml, wiki/config/agent-directive.md

## Backlinks

[[Model: LLM Wiki]]
[[Model: Claude Code]]
[[Model: Ecosystem Architecture]]
[[Model: Skills, Commands, and Hooks]]
[[Model: Second Brain]]
[[Methodology Framework]]
[[Stage-Gate Methodology]]
[[Task Type Artifact Matrix]]
[[Backlog Hierarchy Rules]]
[[Execution Modes and End Conditions]]
[[Skyscraper, Pyramid, Mountain]]
[[Spec-Driven Development]]
[[Scaffold → Foundation → Infrastructure → Features]]
[[Adoption Guide — How to Use This Wiki's Standards]]
[[wiki/config/methodology.yaml]]
[[wiki/config/agent-directive.md]]
[[Methodology Standards — What Good Execution Looks Like]]
[[Model Registry]]
[[Model: Wiki Design]]
[[Wiki Design Standards — What Good Styling Looks Like]]
