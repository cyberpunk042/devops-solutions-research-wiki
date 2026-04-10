---
title: "Methodology Standards — What Good Execution Looks Like"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: seed
created: 2026-04-09
updated: 2026-04-09
sources:
  - id: src-openarms-methodology-evolution
    type: documentation
    file: raw/articles/openarms-methodology-evolution-2026-04-09.md
    title: "OpenArms Methodology Evolution — 7 Bugs, 6 Versions"
    ingested: 2026-04-09
tags: [methodology, standards, quality, stage-gate, execution, gold-standard, anti-patterns]
---

# Methodology Standards — What Good Execution Looks Like

## Summary

This page defines the quality bar for METHODOLOGY EXECUTION. Where [[Model: Methodology]] defines the system (9 models, 5 condition dimensions, 4 composition modes, stage boundaries), this page shows what it looks like when that system is followed WELL — and what it looks like when it fails. ==Every gold standard on this page is a real instance from this wiki or the OpenArms ecosystem.== No hypotheticals. The methodology was hardened by real bugs; the standards are demonstrated by real successes.

## Key Insights

- **Good execution is visible in the artifacts, not the claims.** A well-run stage sequence leaves a trail: wiki page at document, spec at design, schema at scaffold, working code at implement, clean health check at test. If someone says "I'm at 80% readiness" but there's no spec, the claim is false.

- **The right model for the job is rarely the biggest model.** Feature Development has 5 stages. Most real work uses 2-3 stage subsets. Defaulting to the full 5-stage model for everything is the methodology equivalent of using a sledgehammer for every nail.

- **Honest quality tier selection IS the standard, not Skyscraper.** A hotfix at Pyramid tier with documented reasoning is BETTER methodology than a feature built at Mountain tier by an agent that thinks it's running Skyscraper. The standard is intentionality, not perfection.

- **The gap between documenting methodology and following it is the most dangerous failure mode.** A system that describes perfect stage gates while skipping stages is worse than a system with no documented methodology — because the documentation creates false confidence.

## Deep Analysis

### Gold Standard: Stage-Gate Execution

What a properly run 5-stage sequence looks like end-to-end.

> [!info] **Reference: Building the wiki backlog system** (Feature Development model)
> The most complete stage-gate instance in this wiki's history. Every stage produced its required artifacts, every gate was passed, every transition was explicit.

> [!example]- **Stage 1 — Document** (readiness: 0→25%)
> **What happened:** Read OpenArms methodology YAML (253 lines), OpenFleet methodology scan (798 lines), OpenArms integration sprint learnings. Created wiki pages mapping the gap between our wiki's flat task tracking and OpenArms' stage-gated backlog.
>
> **Artifacts produced:**
> - Wiki pages: [[Methodology Framework]], [[Stage-Gate Methodology]], [[Task Type Artifact Matrix]]
> - Gap analysis: wiki has no task types, no stage tracking, no readiness computation
>
> **Gate:** Pages exist with Summary + gaps identified. ✅ Passed.
>
> **What makes this good:** The document stage produced UNDERSTANDING, not code. Three wiki pages existed before any implementation was discussed. The gap analysis named specific missing features, not vague "needs improvement."

> [!example]- **Stage 2 — Design** (readiness: 25→50%)
> **What happened:** Brainstormed with the user — 5 design sections, each presented and approved separately. Options evaluated: flat vs hierarchical backlog, computed vs manual readiness, agent-settable vs human-gated status transitions.
>
> **Artifacts produced:**
> - Spec in `docs/superpowers/specs/`
> - Decision: hierarchical backlog (epic → module → task), computed readiness, max agent-settable = "review"
>
> **Gate:** Spec reviewed and approved by operator. ✅ Passed.
>
> **What makes this good:** The user approved each design section BEFORE the next was presented. No batching. No "here's the whole design, approve it." Incremental validation caught issues early — the user rejected the first readiness computation proposal and we iterated.

> [!example]- **Stage 3 — Scaffold** (readiness: 50→80%)
> **What happened:** Schema changes only. No logic.
>
> **Artifacts produced:**
> - 4 new types in `wiki-schema.yaml`: epic, module, task, note
> - 7 new statuses: draft, active, in-progress, review, done, archived, blocked
> - 5 new enums: priority, task_type, stage, estimate, note_type
> - Directory structure: `wiki/backlog/epics/`, `wiki/backlog/modules/`, `wiki/backlog/tasks/`
> - `wiki/config/methodology.yaml` (253 lines) — the stage definitions
>
> **Gate:** Types compile (schema validates), ==no business logic in the diff==. ✅ Passed.
>
> **What makes this good:** The diff contained ONLY schema, config, and empty directories. Zero Python logic. Zero business rules. The methodology.yaml file defines stages — it does not implement them. This is the scaffold stage doing what scaffold means.

> [!example]- **Stage 4 — Implement** (readiness: 80→95%)
> **What happened:** Built on the scaffold. Python validation for new types, pipeline `backlog` command, slash commands, MCP tools.
>
> **Artifacts produced:**
> - `tools/validate.py` updates (backlog field validation)
> - `tools/pipeline.py` updates (`backlog` command with `run_backlog()`)
> - `/backlog` + `/log` slash commands
> - `wiki_backlog` + `wiki_log` MCP tools in `tools/mcp_server.py`
>
> **Gate:** Code compiles, lint passes, ==≥1 runtime file imports new code==. ✅ Passed.
>
> **What makes this good:** Every new function was imported by an existing runtime file. The pipeline's `backlog` command calls `run_backlog()`. The MCP server calls `wiki_backlog()`. Nothing was orphaned. This is the lesson from OpenArms Bug 6 — 2,073 lines of code nobody imported.

> [!example]- **Stage 5 — Test** (readiness: 95→100%)
> **What happened:** Full health check, manual verification of generated output.
>
> **Verification:**
> - `pipeline chain health` — clean ✅
> - `pipeline backlog` — shows 2 epics + 1 task ✅
> - `pipeline post` — 0 validation errors ✅
> - Manual: backlog items have correct frontmatter, readiness computes from children ✅
>
> **What makes this good:** Test was a SEPARATE stage from implement. The health check ran AFTER implementation was committed. If tests had failed, the fix would have been in the test stage — not a retroactive patch to the implement commit.

> [!tip] **The pattern to replicate**
> Each stage has: what happened (narrative), artifacts produced (concrete list), gate (pass/fail), and what makes it good (the quality signal). If any of these four are missing, the stage wasn't properly executed — it was performed but not verified.

---

### Gold Standard: Model Selection

What thoughtful multi-dimensional selection looks like vs reflexive defaulting.

> [!success] **Good selection: "Tune the evolution scorer"**
> | Dimension | Value | Reasoning |
> |-----------|-------|-----------|
> | task_type | `task` | Atomic work unit, not an epic |
> | phase | Features | Wiki infrastructure exists, adding capability |
> | domain | tools | Python tooling, not wiki content |
> | scale | focused | One file (`evolve.py`), one subsystem |
> | urgency | normal | Not blocking anything |
>
> **Result → Feature Development subset:** scaffold → implement → test (skip document + design because the scorer already exists and the changes are scoped).
>
> This is correct because: the full context is already known (no document stage needed), the approach is already decided (no design stage needed), but the change needs structure (scaffold weights before implementing dedup). The 3-stage subset is the MINIMUM sufficient model.

> [!bug]- **Bad selection: defaulting to Feature Dev for everything**
> When the agent was asked to "process this content into wiki pages," it selected the Feature Development model and began writing a spec. The task was actually `docs` type — single-stage Documentation model. The result: unnecessary design overhead for a task that needed zero design.
>
> **The signal:** if the model selection takes more effort than the task itself, the wrong model was selected. A Documentation task should be recognized in seconds: "Is this producing knowledge artifacts only, no code? → Documentation model."
>
> **The fix:** evaluate task_type FIRST. Most tasks have an obvious type. Only evaluate the other 4 dimensions when the type is ambiguous.

---

### Gold Standard: Quality Tier Selection

The standard is HONEST selection, not always choosing Skyscraper.

> [!success] **Good Pyramid: the argparse `--top`/`--topic` collision hotfix**
> The bug was immediately clear — argparse abbreviation matching consumed `--top` as `--topic`. The root cause was known. The fix was one line: `allow_abbrev=False`.
>
> **Quality tier chosen:** Pyramid (Hotfix model — implement → test, skip document + design + scaffold).
>
> **Why this is GOOD methodology:**
> - The compression was DELIBERATE — the agent explicitly chose Hotfix, not accidentally skipped stages
> - The reasoning was documented — "the fix was obvious; the process was correctly compressed"
> - Two commits, clean test — no trailing debt
>
> A Skyscraper approach to this fix (document the argparse behavior, design alternative fixes, scaffold a test, implement, test) would have been methodology theater — applying process where process adds no value.

> [!bug]- **Bad Mountain: batch-produced model pages**
> 14 model pages were batch-produced in one pass. Each was 80-110 lines. Each was a reading list, not a system definition. The agent claimed "models are ready." The user's response: "So you lied again... nothing is ready... I dont even see 2% of it..."
>
> **Quality tier that was operating:** Mountain — stages skipped accidentally, artifacts shallow, gates not checked.
>
> **Why this is BAD methodology:**
> - No deliberate tier selection — the agent didn't CHOOSE Pyramid, it accidentally produced Mountain
> - False readiness claim — "models are ready" without checking the quality gates
> - The agent confused structure (pages exist) with substance (pages define systems)
>
> See [[Models Are Built in Layers, Not All at Once]] for the full failure analysis.

> [!warning] **The diagnostic question**
> "Did you CHOOSE this quality tier, or did it happen to you?" If you can't articulate WHY you're at Pyramid instead of Skyscraper, you're at Mountain.

---

### Gold Standard: Stage Boundary Enforcement

What proper ALLOWED/FORBIDDEN adherence looks like.

> [!success] **Good enforcement: scorer tuning scaffold stage**
> The scaffold stage for tuning the evolution scorer allowed: modifying signal weights, adding the `_GENERIC_TAGS` filter set, changing the tag co-occurrence threshold. It FORBADE: rewriting the scoring algorithm, adding new signal functions.
>
> The actual diff contained ONLY: a modified `SIGNAL_WEIGHTS` dict and a new `_GENERIC_TAGS` set. No algorithm changes. No new functions. The boundary held.
>
> **Why this matters:** The boundary prevented scope creep. The natural temptation during "tune the scorer" is to also improve the scoring algorithm. The FORBIDDEN list says: not in this stage. Improvement is a different task with its own model selection.

> [!bug]- **Bad enforcement: OpenArms Bug 5 — scaffold with business logic**
> The scaffold stage produced a 135-line environment reader with full business logic — parsing, validation, default handling. The `scaffold` stage had no FORBIDDEN list. Nothing explicitly said "business logic is not allowed here."
>
> **The lesson:** stage NAMES do not prevent violations. Explicit ALLOWED/FORBIDDEN lists do. "Scaffold" sounds like it means "structure only," but without the explicit list, the agent's definition of "structure" expanded to include everything.
>
> This bug created the ALLOWED/FORBIDDEN system (methodology v4). Every stage boundary in the wiki's `methodology.yaml` now has explicit protocol rules.

---

### Gold Standard: Composition in Practice

What real multi-model composition looks like when it runs well.

> [!info] **Three-track parallel composition on this wiki**
> | Track | Running model | Current state | Artifacts this session |
> |-------|--------------|---------------|----------------------|
> | **Execution** | Brainstorm → Spec → Plan → Implement | Active — building models, applying styling | Specs, model pages, standards pages, skills |
> | **PM** | Epics → Modules → Tasks | Active — 2 epics, backlog system operational | Backlog entries, readiness scores |
> | **Knowledge** | Ingest → Synthesize → Cross-ref → Evolve | Active — 167 pages, ~1,175 relationships | Source pages, concept pages, 6 lessons, 6 patterns |
>
> These three tracks ran SIMULTANEOUSLY throughout the session. While the execution track was building the backlog system (Feature Dev model), the knowledge track was ingesting OpenArms methodology (Ingestion model), and the PM track was tracking the backlog items being created. The tracks interact — PM triggers execution tasks, execution produces knowledge artifacts, knowledge informs PM priorities — but they never merge into one sequence.

> [!example]- **Nested composition: SFIF → Feature Dev → task subsets**
> At the project level, the wiki traversed SFIF stages:
> 1. **SFIF Scaffold** — CLAUDE.md, directory structure, tech stack
> 2. **SFIF Foundation** — tools/common.py, schema, validation
> 3. **SFIF Infrastructure** — pipeline.py, MCP server, sync service
>    - Inside Infrastructure, the backlog system ran **Feature Development** (5 stages)
>      - Inside Feature Dev, individual schema changes ran **task-level subsets** (scaffold → implement → test)
> 4. **SFIF Features** — Evolution pipeline, model-building skill, standards documents
>
> Three nesting levels. Each with its own methodology model. The SFIF model governed the project. Feature Dev governed the epic. Task subsets governed the atomic work. Same vocabulary (stages, gates, artifacts, readiness) at every level.

---

### Gold Standard: methodology.yaml

What a well-written methodology config looks like.

> [!info] **Reference: `wiki/config/methodology.yaml`** (253 lines)
> This wiki's own methodology config. What makes it the standard:
>
> | Quality signal | What it demonstrates |
> |---------------|---------------------|
> | **5 stages with explicit readiness ranges** | `document: [0, 25]`, `design: [25, 50]`, etc. — readiness is COMPUTED, not subjective |
> | **Protocol per stage** | Each stage has a `protocol:` block listing DO and DO NOT rules |
> | **8 task types with explicit stage lists** | `epic: [document, design, scaffold, implement, test]`, `research: [document, design]` — the stages aren't optional, they're the task type's DEFINITION |
> | **8 execution modes** | From `autonomous` (no stops) to `custom` (per-run override) — the agent's autonomy level is configurable |
> | **5 end conditions** | `backlog-empty`, `stage-reached`, `time-limit`, `cost-limit`, `task-count` — the agent knows WHEN to stop |
> | **Defaults section** | `mode: autonomous`, `end_condition: backlog-empty` — explicit defaults, not implicit assumptions |

> [!warning] **Anti-pattern: thin methodology.yaml**
> A config with only stage names and no protocols, no readiness ranges, no task type mappings. Stage names alone don't prevent violations (OpenArms Bug 5). A methodology config must be prescriptive enough that an agent reading only the config — not the wiki pages, not the lessons — knows what it's allowed to do at each stage.

---

### Anti-Pattern Gallery

Methodology failures from real operation, each traced to a specific lesson.

> [!bug]- **Stage skipping: "continue" misinterpreted as "skip ahead"**
> The user said "you have everything to get started." The agent interpreted this as permission to skip brainstorm and jump to writing a spec. The user's response: "WTF ???? WHAT SPEC ??? WTF ???????"
>
> **Root cause:** Bias toward perceived progress. Writing a spec FEELS like forward movement. Processing content into wiki pages feels like "still doing prep work."
>
> **The rule:** "Continue" = advance within current stage. "Get started" = begin current stage. Only "skip to X" authorizes stage-skipping. See [[Never Skip Stages Even When Told to Continue]].

> [!bug]- **False readiness: "models are ready" at scaffold level**
> 14 model pages existed as 80-110 line reading lists. The agent claimed they were complete. The user: "I dont even see 2% of it..."
>
> **Root cause:** Confusing structure (pages exist) with substance (pages define systems). The SFIF framework names this explicitly: scaffold ≠ foundation ≠ infrastructure ≠ features.
>
> **The rule:** Readiness is derived from stage completion, not from artifact count. 14 scaffolded pages = 14 × scaffold readiness (50%), not 14 × done (100%). See [[Models Are Built in Layers, Not All at Once]].

> [!bug]- **Practice vs document gap: documenting rules you don't follow**
> The wiki had pages about stage gates, brainstorm-before-spec, depth verification. The agent had written all of them. The agent violated all of them. The wiki described methodology perfectly while the agent ignored it.
>
> **Root cause:** Methodology existed in wiki pages (knowledge the agent produced) but not in CLAUDE.md (instructions the agent follows). The agent could describe the rules but didn't apply them.
>
> **The rule:** When the wiki evolves a methodology rule, that rule must be propagated to CLAUDE.md. Knowledge must become operational. See [[The Agent Must Practice What It Documents]].

> [!bug]- **Binary status: done/not-done without stage tracking**
> OpenArms Bug 1. Tasks were either "active" or "done." The agent checked "Done When" boxes without verification and skipped stages.
>
> **Root cause:** No stage-level visibility. Without `current_stage`, `stages_completed`, and `readiness`, there's no way to distinguish "completed document stage" from "completed everything."
>
> **The fix:** Added stage tracking to frontmatter. Reset 22 tasks. 6 moved from "done" back to "in-progress."

> [!bug]- **Orphaned implementation: code nobody imports**
> OpenArms Bug 6. 2,073 lines of production code — network rules, cost tracking, hook events. None imported by any runtime file. Tests pass ≠ feature works.
>
> **Root cause:** No integration requirement at the implement stage. "Code exists" was treated as "code works."
>
> **The fix:** Implement stage MUST wire into runtime. "Done When" must name the specific consumer file that imports the new code.

---

### The Methodology Execution Checklist

> [!tip] **Run this at every stage transition**
> - [ ] Current stage's required artifacts exist and are committed
> - [ ] Gate condition for current stage is met (not just "feels done")
> - [ ] Readiness percentage matches stages completed (not claimed)
> - [ ] No FORBIDDEN artifacts appear in the diff for the current stage
> - [ ] The model was selected by evaluating conditions, not defaulted
> - [ ] Quality tier was explicitly chosen (Skyscraper/Pyramid), not accidentally Mountain
> - [ ] If methodology rules were learned during this task, they're propagated to CLAUDE.md
> - [ ] Frontmatter reflects actual state: `current_stage`, `stages_completed`, `readiness`

> [!tip] **Run this at task completion**
> - [ ] All required stages for this task type were executed (check `methodology.yaml`)
> - [ ] `pipeline post` passes with 0 validation errors
> - [ ] Readiness = 100% (or capped at the task type's maximum — research caps at 50%)
> - [ ] Parent epic/module readiness recomputed from children
> - [ ] One commit per stage (check git log)

## Open Questions

> [!question] **Can methodology compliance be measured automatically?**
> A compliance checker could: verify one-commit-per-stage in git log, check that FORBIDDEN artifacts don't appear in stage diffs, verify readiness matches stages_completed. OpenArms built `agent-report.py` for this. Should the wiki have an equivalent? (Requires: defining measurable compliance signals)

> [!question] **What's the failure rate of stage-gate enforcement in practice?**
> OpenArms found 7 bugs in one day. This wiki had 3+ methodology violations in one session. Is this the expected learning curve, or does it indicate the enforcement mechanisms are insufficient? (Requires: tracking violations over multiple sessions)

> [!question] **Should there be a "methodology health" score per project?**
> A composite metric: % of tasks with proper stage tracking, % of commits with stage labels, % of epics with computed readiness, # of FORBIDDEN violations. Would this be useful or bureaucratic? (Requires: implementing the metric and testing whether it drives behavior)

## Relationships

- BUILDS ON: [[Model: Methodology]]
- BUILDS ON: [[LLM Wiki Standards — What Good Looks Like]]
- RELATES TO: [[Never Skip Stages Even When Told to Continue]]
- RELATES TO: [[The Agent Must Practice What It Documents]]
- RELATES TO: [[Models Are Built in Layers, Not All at Once]]
- RELATES TO: [[Wiki Design Standards — What Good Styling Looks Like]]
- IMPLEMENTS: wiki/config/methodology.yaml, wiki/config/agent-directive.md

## Backlinks

[[Model: Methodology]]
[[LLM Wiki Standards — What Good Looks Like]]
[[Never Skip Stages Even When Told to Continue]]
[[The Agent Must Practice What It Documents]]
[[Models Are Built in Layers, Not All at Once]]
[[Wiki Design Standards — What Good Styling Looks Like]]
[[wiki/config/methodology.yaml]]
[[wiki/config/agent-directive.md]]
[[Claude Code Standards — What Good Agent Configuration Looks Like]]
