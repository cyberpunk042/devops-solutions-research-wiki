---
title: "Model: LLM Wiki"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: authoritative
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources:
  - id: src-karpathy-llm-wiki-idea-file
    type: documentation
    file: raw/articles/karpathy-llm-wiki-idea-file.md
    title: "Karpathy LLM Wiki Idea File"
    ingested: 2026-04-08
  - id: src-llm-wiki-v2-agentmemory
    type: documentation
    file: raw/articles/llm-wiki-v2-extending-karpathys-llm-wiki-pattern-with-lessons-from-building-agen.md
    title: "LLM Wiki v2 — Extending Karpathy's Pattern with Agentmemory Lessons"
    ingested: 2026-04-08
tags: [llm-wiki, model, knowledge-system, schema, ingestion, evolution, standards, transferable]
---

# Model: LLM Wiki

## Summary

The LLM Wiki model defines a knowledge system where an LLM agent maintains a structured markdown wiki — ingesting sources, synthesizing pages, cross-referencing relationships, evolving insights through density layers, and linting for quality. The model solves the wiki maintenance problem: wikis historically die because humans abandon upkeep. With an LLM handling all mechanical operations, the wiki compounds knowledge instead of decaying. This model is technology-agnostic — it defines structure and rules, not tools.

## Key Insights

- Maintenance economics: wikis fail from abandoned upkeep, not lack of content. Making the LLM handle ALL bookkeeping eliminates this structurally.
- Three operations: **Ingest** (source → structured pages), **Query** (navigate via indexes + relationships), **Lint** (validate, detect orphans, flag contradictions).
- The schema is the real product — content is regenerable from raw sources; the schema that constrains content encodes irreplaceable operational knowledge.
- Knowledge compounds through density layers — each layer denser and more actionable than the previous.
- This model is technology-agnostic. It defines WHAT and HOW, not which tools.

## Deep Analysis

### Core Architecture

An LLM Wiki has three layers:

1. **Raw layer** — unprocessed source material. Never modified after ingestion. Permanent provenance.
2. **Wiki layer** — structured markdown pages with YAML frontmatter, typed relationships, quality gates.
3. **Meta layer** — schema, templates, validation rules. Defines how the wiki works.

### Repository Structure

```
{project-root}/
├── raw/                          # Raw layer
│   ├── articles/                 # Web content, READMEs, docs
│   ├── transcripts/              # Video/audio transcripts
│   └── notes/                    # Legacy notes
├── wiki/                         # Wiki layer
│   ├── domains/{domain}/         # L2 concept pages by domain
│   ├── sources/                  # L1 source-synthesis pages
│   ├── comparisons/              # L3 comparison pages
│   ├── lessons/                  # L4 codified experience
│   ├── patterns/                 # L5 recurring structures
│   ├── decisions/                # L6 choice frameworks
│   ├── spine/                    # Navigation: model guides, overviews
│   ├── backlog/                  # PM: epics/modules/tasks
│   ├── log/                      # Operator directives, session logs
│   └── config/                   # Methodology files
├── config/                       # Meta layer
│   ├── wiki-schema.yaml          # Page validation schema
│   └── templates/                # Scaffolding templates per type
└── {project-specific}/           # Whatever else the project needs
```

### Naming Conventions

- **Filenames**: kebab-case always (`claude-code-best-practices.md`, not `ClaudeCodeBestPractices.md`)
- **Source pages**: prefixed with `src-` (`src-karpathy-claude-code-10x.md`)
- **Backlog IDs**: sequential numbering (`E001-name.md` for epics, `M001-name.md` for modules, `T001-name.md` for tasks)
- **Domain folders**: kebab-case, grow organically as needed
- **Index files**: `_index.md` in every directory, auto-maintained by the pipeline
- **One concept per page**: never combine unrelated topics. If a page covers two concepts, split it.

### Domain Growth Rules

Domains are knowledge categories. They grow organically:

- **When to create a new domain**: when 3+ pages cluster around a topic not covered by existing domains. Don't create a domain for one page.
- **Domain naming**: use kebab-case, keep it broad enough to hold 5-15 pages. `ai-agents` not `claude-code-specific`.
- **Domain field must match folder path**: a page in `wiki/domains/ai-agents/` must have `domain: ai-agents`.
- **Every domain gets an `_index.md`**: auto-generated, lists all pages with summaries.
- **Domain overviews** (in `wiki/spine/domain-overviews/`): curated summary of each domain's state — what's known, what's thin, priorities, FAQ.

### Knowledge Layers

| Layer | Directory | Type | Purpose | Created by |
|-------|-----------|------|---------|-----------|
| L0 | raw/ | — | Unprocessed evidence | Fetch / drop |
| L1 | wiki/sources/ | source-synthesis | One synthesis per source | Ingestion |
| L2 | wiki/domains/ | concept | One concept per page | Ingestion + manual |
| L3 | wiki/comparisons/ | comparison | Structured comparisons | Cross-reference |
| L4 | wiki/lessons/ | lesson | Codified experience | Evolution |
| L5 | wiki/patterns/ | pattern | Recurring structures (2+ instances) | Evolution |
| L6 | wiki/decisions/ | decision | Choice frameworks with alternatives | Evolution |
| Spine | wiki/spine/ | various | Navigation, model guides | Curation |

This IS [[Progressive Distillation]]: raw → synthesis → concept → lesson → pattern → decision.

### Complete Page Type Catalog

16 page types. Each has a purpose, required sections, and guidance on when to use it:

**Knowledge page types:**

| Type | Purpose | Required sections | When to use |
|------|---------|------------------|-------------|
| **concept** | Core knowledge — one idea per page | Summary, Key Insights, Deep Analysis, Relationships | Most pages. Any topic that needs structured explanation. |
| **source-synthesis** | Extraction from one source | Summary, Key Insights, Relationships | After ingesting a URL, transcript, or document. One per source. |
| **comparison** | Structured comparison with matrix | Summary, Comparison Matrix, Key Insights, Deep Analysis, Relationships | When 2+ alternatives need side-by-side evaluation. The matrix is a TABLE, not prose. |
| **reference** | Quick-reference page | Summary, Relationships | Cheat sheets, lookup tables, reference cards. Minimal depth, maximum utility. |
| **deep-dive** | Extended analysis | Summary, Key Insights, Deep Analysis, Relationships | When a concept needs more depth than a standard concept page. Model guides use this. |
| **index** | Navigation page | (none required) | `_index.md` files. Auto-generated. Don't create manually. |
| **lesson** | Codified experience (L4) | Summary, Context, Insight, Evidence, Applicability, Relationships | When multiple sources converge on the same insight, or a failure teaches something. Requires evidence — not opinions. |
| **pattern** | Recurring structure (L5) | Summary, Pattern Description, Instances, When To Apply, When Not To, Relationships | When the same structure appears in 2+ independent contexts. Must have concrete instances. |
| **decision** | Choice framework (L6) | Summary, Decision, Alternatives, Rationale, Reversibility, Dependencies, Relationships | When a choice between alternatives needs to be documented with evidence-backed rationale. |
| **domain-overview** | Domain state summary | Summary, State of Knowledge, Maturity Map, Gaps, Priorities, Key Pages, Relationships | One per domain in wiki/spine/domain-overviews/. Curated assessment of domain health. |
| **learning-path** | Ordered reading guide | Summary, Prerequisites, Sequence, Outcomes, Relationships | For guiding someone through a topic in the right order. Model entry points can use this. |
| **evolution** | How a concept changed over time | Summary, Timeline, Key Shifts, Current State, Relationships | For tracking how understanding of a concept has evolved across sessions. |

**Backlog page types:**

| Type | Purpose | Required sections | When to use |
|------|---------|------------------|-------------|
| **epic** | Large initiative spanning modules | Summary, Goals, Done When, Relationships | A body of work that takes weeks and has multiple deliverables. |
| **module** | Scoped deliverable within an epic | (same as epic) | A coherent component within an epic. |
| **task** | Atomic work unit | Summary, Done When | A single focused piece of work, completable in one session. |
| **note** | Log entry | Summary | Operator directives (verbatim), session summaries, completion notes. |

### Required Frontmatter Fields

Every page must have these 9 fields:

| Field | Type | What it defines |
|-------|------|----------------|
| `title` | string | Must match the `# Heading`. The page's identity. |
| `type` | enum | One of the 16 types above. Determines required sections. |
| `domain` | string | Knowledge domain. Must match the folder path. |
| `status` | enum | Lifecycle stage. |
| `confidence` | enum | How certain: `low` (speculation), `medium` (partially sourced), `high` (well-sourced), `authoritative` (primary source or direct experience). |
| `created` | date | When the page was created (YYYY-MM-DD). |
| `updated` | date | When last modified. Used for staleness detection. |
| `sources` | list | Provenance chain — where this knowledge came from. |
| `tags` | list | For discovery and cross-referencing. Use kebab-case. |

### Optional Frontmatter Fields

| Field | Used by | What it defines |
|-------|---------|----------------|
| `layer` | All knowledge pages | Knowledge layer number (1-6) or `spine`. Determines where in the density hierarchy this page sits. |
| `maturity` | All knowledge pages | `seed` (exists, unvalidated) → `growing` (reviewed, quality gates pass) → `mature` (stable 30+ days, cross-referenced) → `canonical` (authoritative, manual). |
| `derived_from` | L4-L6 pages | List of page titles this was distilled from. The evolution provenance chain. |
| `instances` | Patterns (L5) | List of `{page, context}` entries — concrete occurrences with how each shows the pattern. |
| `reversibility` | Decisions (L6) | `easy` (swap a config), `moderate` (refactor needed), `hard` (architectural change), `irreversible` (can't undo). |
| `complexity` | Any page | Reader skill level: `beginner`, `intermediate`, `advanced`, `expert`. Use when pages vary in required background knowledge. Helps sequence learning paths. |
| `subdomain` | Concepts | Finer categorization within a domain. Use when a domain grows large and needs internal structure. |
| `aliases` | Any page | Alternative names for the concept. Use when the same thing is known by different names across sources (e.g., "SFIF" vs "Scaffold-Foundation-Infrastructure-Features"). |
| `priority` | Backlog items | `P0` (critical), `P1` (high), `P2` (medium), `P3` (low). |
| `task_type` | Backlog items | Determines required stages: `epic`, `module`, `task`, `research`, `evolve`, `docs`, `bug`, `refactor`. |
| `current_stage` | Backlog items | Which stage the item is in: `document`, `design`, `scaffold`, `implement`, `test`. |
| `readiness` | Backlog items | 0-100 percentage. Computed from stages completed vs required. |
| `stages_completed` | Backlog items | List of stages actually finished with artifacts verified. |
| `artifacts` | Backlog items | File paths produced as evidence of stage completion. |
| `estimate` | Backlog items | Effort: `XS` (minutes), `S` (hour), `M` (half-day), `L` (day), `XL` (multi-day). |
| `epic` | Modules/tasks | Parent epic ID (e.g., `E001`). |
| `module` | Tasks | Parent module ID (e.g., `M001`). |
| `depends_on` | Tasks | List of task IDs that must complete before this one starts. |
| `note_type` | Log entries | `directive` (operator instruction), `session` (work summary), `completion` (task done report). |

Note: `resolution` is reserved for future use (how thoroughly a topic is covered) but not yet formally defined in the schema.

### Status Lifecycle

Two separate lifecycles coexist:

**Knowledge pages**: `raw` → `processing` → `synthesized` → `verified` → `stale`
- `raw`: just created, not yet reviewed
- `processing`: being worked on
- `synthesized`: complete, passes quality gates
- `verified`: human-confirmed accurate
- `stale`: sources have been updated since this page was last revised

**Backlog items**: `draft` → `active` → `in-progress` → `review` → `done` → `archived`
- `draft`: planned but not started
- `active`: ready to be picked up
- `in-progress`: someone is working on it
- `review`: work done, awaiting human review
- `done`: confirmed complete
- `archived`: no longer relevant
- `blocked`: cannot proceed (dependency or external blocker)

### Maturity Lifecycle

| Level | Meaning | How you get there |
|-------|---------|-------------------|
| `seed` | Exists but unvalidated | Auto-generated or scaffolded |
| `growing` | Human-reviewed, real derived_from, passes quality gates | Review confirms quality |
| `mature` | Cross-referenced by others, stable 30+ days | Time + inbound references |
| `canonical` | Authoritative reference for its domain | Marked manually |

No auto-promotion. The system SUGGESTS promotions but a human must confirm.

### Source Provenance

Every `sources` entry requires:
- `id` — unique identifier (e.g., `src-karpathy-claude-code-10x`)
- `type` — one of 8 source types: `article`, `youtube-transcript`, `paper`, `documentation`, `notes`, `paste`, `book`, `podcast-transcript`
- At least one of: `url` (web source) or `file` (local file path)

Optional: `title`, `ingested` (date).

### Relationship System

Relationships are explicit, typed, and bidirectional via auto-generated backlinks:

```markdown
## Relationships

- BUILDS ON: [[Page Title]]
- ENABLES: [[Another Page]]
- CONTRADICTS: [[Some Assumption]]
```

**Complete verb catalog (17 verbs):**

| Verb | Meaning |
|------|---------|
| BUILDS ON | This page extends or depends on the target |
| ENABLES | This page makes the target possible |
| COMPARES TO | Direct comparison exists |
| CONTRADICTS | This page disagrees with the target |
| USED BY | The target consumes this page's knowledge |
| RELATES TO | General connection (use sparingly — prefer specific verbs) |
| FEEDS INTO | This page's output flows into the target |
| DERIVED FROM | This page was synthesized from the target (evolution provenance) |
| SUPERSEDES | This page replaces the target |
| IMPLEMENTS | This page is a concrete implementation of the target |
| EXTENDS | This page adds to the target |
| CONSTRAINS | This page limits the target |
| CONSTRAINED BY | This page is limited by the target |
| PARALLELS | Similar structure or approach |
| SYNTHESIZES | This page combines multiple targets |
| ENABLED BY | Inverse of ENABLES |
| CONTRASTS WITH | Different approach to same problem |

Format: `- VERB: [[Target]]` — one relationship per line. The regex `^([A-Z][A-Z /\-]+?):\s*(.+)$` extracts verb and target.

### Page Templates

Templates live in `config/templates/` with `{{placeholder}}` variables. Six templates exist for the evolved page types:

**lesson.md** (L4):
```markdown
---
title: "{{title}}"
type: lesson
domain: {{domain}}
layer: 4
maturity: seed
derived_from:
  - "{{derived_page_1}}"
---

# {{title}}

## Summary
<!-- 2-3 sentences: the lesson stated clearly -->

## Context
<!-- When and where does this lesson apply? What triggers it? -->

## Insight
<!-- The core learning. Min 50 words. State it plainly. -->

## Evidence
<!-- Specific examples from derived_from pages. Quote or reference directly. -->

## Applicability
<!-- Which domains, projects, situations benefit? -->

## Relationships
- DERIVED FROM: {{derived_page_1}}
```

**pattern.md** (L5):
```markdown
---
title: "{{title}}"
type: pattern
domain: cross-domain
layer: 5
maturity: seed
derived_from:
  - "{{derived_page_1}}"
  - "{{derived_page_2}}"
instances:
  - page: "{{instance_1}}"
    context: "{{how_instance_1_shows_this_pattern}}"
  - page: "{{instance_2}}"
    context: "{{how_instance_2_shows_this_pattern}}"
---

# {{title}}

## Summary
<!-- 2-3 sentences: what recurs and why it matters -->

## Pattern Description
<!-- What is this pattern? How do you recognize it? Min 100 words. -->

## Instances
<!-- 2+ specific examples from the wiki. Reference pages directly. -->

## When To Apply
<!-- Conditions that make this pattern appropriate -->

## When Not To
<!-- Anti-patterns, conditions where this fails -->

## Relationships
- DERIVED FROM: {{derived_page_1}}
- DERIVED FROM: {{derived_page_2}}
```

**decision.md** (L6):
```markdown
---
title: "Decision: {{title}}"
type: decision
domain: {{domain}}
layer: 6
maturity: seed
derived_from:
  - "{{derived_page_1}}"
reversibility: moderate
---

# Decision: {{title}}

## Summary
<!-- 2-3 sentences: the decision and recommendation -->

## Decision
<!-- Clear statement of what to do -->

## Alternatives
<!-- Min 2 alternatives with brief rationale for rejection -->

## Rationale
<!-- Why this choice. Evidence from derived_from pages. Min 100 words. -->

## Reversibility
<!-- How hard to undo. Downstream impact if reversed. -->

## Dependencies
<!-- What this decision affects. -->

## Relationships
- DERIVED FROM: {{derived_page_1}}
```

Templates for domain-overview, learning-path, and evolution follow similar patterns. The placeholder `{{variable}}` syntax is filled by the scaffold command.

### Quality Gates

Every page must pass:

1. Valid frontmatter per wiki-schema.yaml (all required fields present, enums match)
2. All required sections for the page type present (per the catalog above)
3. Summary ≥ 30 words
4. At least 1 relationship (unless first page in a new domain)
5. Title field matches # Heading exactly
6. Domain field matches folder path
7. Source provenance (at least one source with url or file)
8. No > 70% concept overlap with existing pages (update the existing page instead)
9. Source-synthesis pages must have depth proportional to the raw source (not just the first few paragraphs)

Backlog items additionally: warn if `task_type` missing, warn if `readiness` > 0 but `stages_completed` empty.

### Three Core Operations

**Ingest**:
1. Source arrives (URL, file, paste)
2. Save to raw/ (permanent provenance — never deleted)
3. Read the COMPLETE source before synthesizing — not just the beginning, the entire content
4. **Depth verification**: if the source DESCRIBES a format, tool, or pattern, examine a real INSTANCE of that thing before synthesizing. A README about DESIGN.md files is Layer 0 (description). An actual DESIGN.md file is Layer 1 (instance). You must reach Layer 1.
5. Create source-synthesis page in wiki/sources/ (one per source, prefixed `src-`)
6. Create/update concept pages in wiki/domains/
7. Validate all pages against schema

**Query**:
- Navigate via domain `_index.md` files and relationship links
- The LLM reads the index, follows links, reads content
- No vector database needed below ~200 pages
- Above ~200 pages: add graph-enhanced retrieval as an additive layer (see Scale Boundary)

**Lint**:
- Validate all pages against schema
- Detect orphaned relationship targets (referenced pages that don't exist)
- Flag stale content (source page updated after the derived page was last touched)
- Report gaps: weak domains (few pages), thin pages (short analysis), unanswered open questions
- Surface contradictions between pages

### Backlog and Stage-Gate System

The wiki manages its own work through a backlog with stage-gate methodology:

**Hierarchy**: EPIC → MODULE → TASK
- Work on TASKS, not epics. To advance an epic, pick a child task.
- Readiness flows UPWARD: epic readiness = average of children's readiness.
- Status flows UPWARD: any child in-progress → parent in-progress. All children done → parent moves to "review" (never "done" directly).

**Task types and their required stages:**

| task_type | Required stages | What it means |
|-----------|----------------|---------------|
| epic | document, design, scaffold, implement, test | Full lifecycle for large initiatives |
| module | document, design, scaffold, implement, test | Full lifecycle for scoped deliverables |
| task | scaffold, implement, test | Focused work — design inherited from parent |
| research | document, design | Investigation only — no implementation |
| evolve | document, implement | Generate evolved pages from existing knowledge |
| docs | document | Documentation only |
| bug | document, implement, test | Fix something broken |
| refactor | document, scaffold, implement, test | Restructure without changing behavior |

**What each stage means for a wiki:**

| Stage | What you do | What you produce | What you do NOT do |
|-------|------------|-----------------|-------------------|
| document | Read sources, understand the topic | Wiki page, gap analysis | Write implementation code |
| design | Brainstorm, make decisions, write spec | Spec, design notes | Implement or scaffold |
| scaffold | Create skeleton structure | Config changes, empty scaffolds, schema updates | Implement logic or fill content |
| implement | Write the code or content | Tools, wiki pages, skills | Skip validation |
| test | Verify everything works | Health check passing, manual review | Leave broken state |

Each stage has a quality gate. Do not advance until the gate passes.

### Evolution Pipeline

1. **Score** — 6 deterministic signals: tag co-occurrence, cross-source convergence, relationship hubs, domain layer gaps, open question density, orphaned references
2. **Scaffold** — create page stubs from templates with `{{placeholder}}` variables
3. **Generate** — fill pages from source material (any LLM — session, local model, API)
4. **Validate** — run quality gates
5. **Review** — maturity promotion: seed → growing → mature → canonical (never auto-promoted)

### Scale Boundary

Below ~200 pages: index-driven navigation is cheaper and more accurate than vector search.

Above ~200 pages: add graph-enhanced retrieval (e.g., LightRAG with BM25 + vector + graph traversal) as an ADDITIVE layer. The wiki structure stays the same — the retrieval layer indexes it.

See [[Decision: Wiki-First with LightRAG Upgrade Path]].

### How to Adopt

1. **Create the repository structure** — raw/, wiki/ (with all subdirectories), config/
2. **Define your schema** — copy `config/wiki-schema.yaml` as a starting point. For a code project, you may add types like `api-spec` or `architecture`. For a research project, the default types work well. Start with the types you need NOW; add more as the wiki grows.
3. **Create page templates** — one per evolved type (lesson, pattern, decision at minimum). Templates define the section structure. Use `{{placeholder}}` variables for scaffolding.
4. **Write agent instructions** — your CLAUDE.md (or equivalent) must include: the schema conventions, naming rules, quality gates, and the three operations (ingest, query, lint).
5. **Adapt quality gates for your tech stack** — a Python project validates with `python3 -m tools.validate`. A TypeScript project might use a custom linter. The GATES are universal; the COMMANDS are project-specific.
6. **Start ingesting sources** — the wiki grows from ingestion. Start with 5-10 sources to build the initial knowledge base.
7. **Evolve periodically** — after the wiki has 20+ pages, run the evolution pipeline to generate lessons, patterns, and decisions from what's already there.

Full guide: [[Adoption Guide — How to Use This Wiki's Standards]]

### Examples — What Each Type Looks Like

#### Concept example: [[Methodology Framework]]

```yaml
---
title: "Methodology Framework"
type: concept
domain: cross-domain
layer: 2
maturity: growing
status: synthesized
confidence: authoritative
---
```

347 lines. Sections: Summary → Key Insights (8 bullets on composable models) → Deep Analysis (8 subsections: model definition, selection, composition, adaptation, recursion, multi-track, quality dimension, transferability) → Open Questions → Relationships. The deepest concept page demonstrates full expected depth.

#### Lesson example: [[Context Management Is the Primary LLM Productivity Lever]]

```yaml
---
title: "Context Management Is the Primary LLM Productivity Lever"
type: lesson
domain: ai-agents
layer: 4
maturity: growing
derived_from:
  - "Claude Code Best Practices"
  - "Synthesis: Claude Code Accuracy Tips"
  - "Synthesis: Claude Code Harness Engineering"
---
```

102 lines. Sections: Summary → Context (when this lesson applies) → Insight (context is the variable you control, not model capability) → Evidence (4 independent sources converging: Boris Cherny's 95% confidence rule, degradation curve quantification, harness engineering guardrails, shanraisshan's CLAUDE.md architecture) → Applicability → Relationships. Evidence section references specific data points from multiple sources — not vague claims.

#### Pattern example: [[Scaffold → Foundation → Infrastructure → Features]]

```yaml
---
title: "Scaffold → Foundation → Infrastructure → Features"
type: pattern
domain: cross-domain
layer: 5
maturity: growing
instances:
  - page: "Research Wiki"
    context: "Scaffold (CLAUDE.md, dirs) → Foundation (common.py, schema) → Infrastructure (pipeline, MCP) → Features (evolve, sync)"
  - page: "OpenFleet"
    context: "Scaffold (monorepo) → Foundation (orchestrator) → Infrastructure (board sync, doctor.py) → Features (10 agents)"
  - page: "AICP"
    context: "Scaffold (venv, profiles) → Foundation (router, breaker) → Infrastructure (MCP, guardrails) → Features (routing, voice)"
---
```

176 lines. Sections: Summary → Pattern Description (what it is, exit criteria per stage) → Instances (4 detailed examples) → When To Apply → When Not To → Relationships. The `instances` frontmatter field lists concrete occurrences — a pattern without instances is just a hypothesis.

#### Decision example: [[Decision: MCP vs CLI for Tool Integration]]

```yaml
---
title: "Decision: MCP vs CLI for Tool Integration"
type: decision
domain: tools-and-platforms
layer: 6
maturity: growing
reversibility: easy
---
```

121 lines. Sections: Summary → Decision ("CLI+Skills for project-internal tooling, MCP for external service bridges") → Alternatives (3 rejected with reasons) → Rationale (12x cost differential, Playwright proof video, Google Trends) → Reversibility → Dependencies → Relationships. `reversibility: easy` means the choice can be reversed by swapping a config — no architectural change.

#### Source-synthesis example: [[Synthesis: Context Mode — MCP Sandbox for Context Saving]]

```yaml
---
title: "Synthesis: Context Mode — MCP Sandbox for Context Saving"
type: source-synthesis
domain: ai-agents
layer: 1
maturity: growing
sources:
  - id: src-context-mode
    type: documentation
    url: "https://github.com/mksglu/context-mode"
    file: raw/articles/mksglucontext-mode.md
---
```

254 lines from a 1,057-line raw source. Sections: Summary → Key Insights (11 subsections: sandbox tools, FTS5/BM25 knowledge base, session continuity, 12-platform matrix, benchmarks, Think in Code paradigm) → Open Questions → Relationships. This demonstrates DEEP source synthesis — the raw file was examined completely, AND an actual instance (the tool's output) was tested, not just the README.

#### Comparison example: [[Cross-Domain Patterns]]

```yaml
---
title: "Cross-Domain Patterns"
type: comparison
domain: cross-domain
layer: 3
maturity: growing
---
```

189 lines. Sections: Summary → Comparison Matrix (6-row TABLE: pattern name, domains, instances, underlying constraint) → Key Insights → Deep Analysis (per-pattern deep dives) → Open Questions → Relationships. The Comparison Matrix is a structured table — not prose paragraphs.

#### Epic example: [[Local Inference Engine (Subsystem 3)]]

```yaml
---
title: "Local Inference Engine (Subsystem 3)"
type: epic
domain: backlog
status: draft
priority: P1
task_type: epic
current_stage: document
readiness: 10
stages_completed: [document]
artifacts:
  - wiki/domains/tools-and-platforms/aicp.md
  - wiki/decisions/local-model-vs-cloud-api-for-routine-operations.md
---
```

Sections: Summary → Goals → Done When (checkbox list) → Blocked → Relationships. The epic tracks `readiness: 10` (document stage = 0-25% range), lists artifacts produced so far, and has `task_type: epic` which requires all 5 stages. Epics are NEVER marked "done" directly — readiness is computed from child tasks.

#### Task example: [[Test OpenAI backend with LocalAI]]

```yaml
---
title: "Test OpenAI backend with LocalAI"
type: task
domain: backlog
status: blocked
priority: P1
epic: E001
task_type: task
current_stage: scaffold
readiness: 0
stages_completed: []
estimate: M
---
```

Sections: Summary → Done When (checkbox list). `task_type: task` requires stages: scaffold, implement, test. `epic: E001` links to parent. `estimate: M` = half-day effort. `status: blocked` + empty `stages_completed` = hasn't started. Each stage completion gets its own git commit.

#### Note (directive) example: [[Never Stop at Surface — Depth Verification Rule]]

```yaml
---
title: "Never Stop at Surface — Depth Verification Rule"
type: note
domain: log
note_type: directive
status: active
---
```

Sections: Summary → Operator Directive (verbatim quote) → Interpretation. Directives are NEVER paraphrased — the operator's exact words are preserved. `note_type: directive` distinguishes from `session` (work summary) and `completion` (task done report).

#### Backlog hierarchy in practice

```
E001-local-inference-engine (epic, P1, readiness=10%)
  └── T001-test-openai-backend (task, P1, blocked, readiness=0%)

E002-ecosystem-integration (epic, P2, readiness=15%)
  └── (tasks to be created)
```

### Reference Implementation

This research wiki is the reference implementation. Project-specific implementation details (Python tooling, CLI commands, MCP tools, sync services, slash commands) are documented in the project's CLAUDE.md. They are NOT part of the universal model.

### Key Pages

| Page | Role in the model |
|------|-------------------|
| [[LLM Wiki Pattern]] | Karpathy's original design — the foundational pattern |
| [[Wiki Ingestion Pipeline]] | How sources become structured pages |
| [[Wiki Knowledge Graph]] | How relationships create a queryable graph |
| [[LLM Knowledge Linting]] | How quality is maintained automatically |
| [[Knowledge Evolution Pipeline]] | How pages evolve through density layers |
| [[Progressive Distillation]] | The pattern: raw → synthesis → lesson → pattern → decision |
| [[LLM Wiki vs RAG]] | When wiki navigation outperforms vector search |
| [[Decision: Wiki-First with LightRAG Upgrade Path]] | The scale decision |
| [[Second Brain Architecture]] | PKM theory (PARA, Zettelkasten) mapped to this model |
| [[Wiki Backlog Pattern]] | How the wiki tracks its own work |

### Lessons Learned

From building with this model — validated experience, not theory:

| Lesson | What was learned |
|--------|-----------------|
| [[LLM-Maintained Wikis Outperform Static Documentation]] | Maintenance economics is the differentiator |
| [[Lesson: Schema Is the Real Product — Not the Content]] | Schema survives; content is regenerable |
| [[Multi-Stage Ingestion Beats Single-Pass Processing]] | Each pass discovers what the previous missed |
| [[Never Synthesize from Descriptions Alone]] | Read the THING, not the description of the thing |
| [[Shallow Ingestion Is Systemic, Not Isolated]] | One defect = audit ALL similar artifacts |
| [[Automated Knowledge Validation Prevents Silent Wiki Decay]] | Without linting, wikis decay silently |

## Open Questions

- What is the minimum viable wiki for a new project? The smallest structure that demonstrates value and justifies the setup cost. (Requires: empirical testing with a new project adopting the model from scratch)
- How should multi-author editing work? When multiple agents or humans contribute to the same wiki, how are conflicts resolved? The current model assumes a single agent + single operator. (Requires: testing with OpenFleet's multi-agent architecture)
- What is the optimal schema complexity for a new adopter? Start minimal (5 types) and grow, or start comprehensive (all 16)? (Requires: adoption experience from 2+ projects)
- How does this model interact with existing documentation systems (Confluence, Notion, Google Docs) in an organization? (Requires: enterprise adoption research)

## Relationships

- FEEDS INTO: [[Model: Second Brain]]
- FEEDS INTO: [[Model Guide: Ecosystem Architecture]]
- ENABLES: [[Model Guide: Claude Code]]
- BUILDS ON: [[LLM Wiki Pattern]]
- BUILDS ON: [[Wiki Ingestion Pipeline]]
- BUILDS ON: [[Knowledge Evolution Pipeline]]
- RELATES TO: [[Model Guide: Methodology]]
- RELATES TO: [[Model: Knowledge Evolution]]

## Backlinks

[[Model: Second Brain]]
[[Model Guide: Ecosystem Architecture]]
[[Model Guide: Claude Code]]
[[LLM Wiki Pattern]]
[[Wiki Ingestion Pipeline]]
[[Knowledge Evolution Pipeline]]
[[Model Guide: Methodology]]
[[Model: Knowledge Evolution]]
