# Wiki Backlog + Log Structure — Design Spec

## Problem

The wiki has 120 pages and 936 relationships but no project management or observability layer. Work gets done ad-hoc — there's no structured tracking of what epics exist, what stage each task is at, what's been completed, or what the operator directed. The raw/notes/ directory holds operator directives but they're not structured as a queryable log. There's no backlog to define what work exists and track it through stages.

OpenArms has proven the model: wiki/backlog/ with epics/modules/tasks as wiki pages with frontmatter state machines, and wiki/log/ for operator directives and session summaries. This project needs the same.

## Solution

Add three new wiki directories (wiki/backlog/, wiki/log/, wiki/config/) with schema extensions for backlog and log page types. Adopt the OpenArms methodology model adapted for a knowledge system.

## Directory Structure

```
wiki/
├── backlog/
│   ├── _index.md              # Overview table of all epics with status
│   ├── epics/                 # Large initiatives (E001, E002, ...)
│   ├── modules/               # Scoped deliverables (M001, M002, ...)
│   └── tasks/                 # Atomic work units (T001, T002, ...)
│       └── _index.md          # Task table sorted by priority/status
├── log/                       # Operator directives + session logs
│   └── _index.md              # Chronological log index
├── config/                    # Methodology definition files
│   ├── methodology.yaml       # Stage definitions, task types, modes, end conditions
│   └── agent-directive.md     # Work loop, rules, quality gates
├── domains/                   # (existing — unchanged)
├── sources/                   # (existing — unchanged)
├── comparisons/               # (existing — unchanged)
├── lessons/                   # (existing — unchanged)
├── patterns/                  # (existing — unchanged)
├── decisions/                 # (existing — unchanged)
└── spine/                     # (existing — unchanged)
```

## wiki/backlog/ — Backlog Items

### Epic Example (wiki/backlog/epics/E001-knowledge-deepening.md)

```yaml
---
title: "Knowledge Deepening"
type: epic
domain: backlog
status: in-progress
priority: P1
task_type: epic
current_stage: implement
readiness: 60
stages_completed: [document, design, scaffold]
artifacts:
  - wiki/patterns/progressive-distillation.md
  - wiki/domains/knowledge-systems/knowledge-evolution-pipeline.md
  - tools/evolve.py
created: 2026-04-08
updated: 2026-04-09
tags: [evolution, deepening, continuous-improvement]
---

# Knowledge Deepening

## Summary
...

## Goals
...

## Done When
- [ ] All domains have ≥5 pages
- [ ] Evolution pipeline produces quality candidates
- [ ] 200+ open questions answered from cross-referencing
```

### Task Example (wiki/backlog/tasks/T001-tune-evolution-scorer.md)

```yaml
---
title: "Tune evolution scorer"
type: task
domain: backlog
status: done
priority: P1
epic: E001
task_type: task
current_stage: test
readiness: 100
stages_completed: [scaffold, implement, test]
artifacts:
  - tools/evolve.py
created: 2026-04-09
updated: 2026-04-09
estimate: M
tags: [scorer, evolution, tuning]
---

# Tune evolution scorer

## Summary
...

## Done When
- [x] Generic tags filtered
- [x] Weights rebalanced
- [x] Dedup catches existing pages
- [x] Score output is diverse (not all tag-pair patterns)
```

### Item Hierarchy Rules

1. **EPIC** is a container. Never done by itself. Done ONLY when ALL children done AND acceptance criteria met.
2. **MODULE** is a scoped deliverable within an epic. Same rule.
3. **TASK** is the atomic work unit. Tasks go through stages. Done when all required stages complete.
4. **Readiness flows UPWARD.** Epic readiness = average of children's readiness. Never set manually.
5. **Status flows UPWARD.** Any child in-progress → parent in-progress. ALL children done → parent moves to review (not done). Parent done ONLY after human review.
6. **Work on TASKS, not epics.** To advance an epic, pick a task and complete the next stage.
7. **When epic has no tasks but isn't 100%, create new tasks** to cover the gap.

## wiki/log/ — Unified Log

Operator directives go directly to wiki/log/. No raw/notes/ intermediary for new content.

### Directive Entry Example

```yaml
---
title: "Flexible Methodology Framework"
type: note
domain: log
status: active
note_type: directive
created: 2026-04-09
updated: 2026-04-09
tags: [directive, methodology, flexibility]
---

# Flexible Methodology Framework

## Operator Directive (verbatim)

> The model is to be flexible...

## Interpretation

...
```

### Session Log Example

```yaml
---
title: "Session 2026-04-09"
type: note
domain: log
status: active
note_type: session
created: 2026-04-09
updated: 2026-04-09
tags: [session, progress]
---

# Session 2026-04-09

## Work Completed
- Created 4 methodology pages
- Answered 18 open questions (batch 6)
- ...

## Commits
- abc1234: feat: methodology pages
- ...
```

### Content Flow

```
External source      → raw/articles|transcripts/  → wiki/sources/ (synthesis needed)
Operator directive   → wiki/log/ directly (already structured, verbatim preserved)
Session summary      → wiki/log/ directly
Task completion      → wiki/log/ directly
```

`raw/notes/` becomes legacy. Existing files stay for provenance. New directives go to wiki/log/.

## wiki/config/ — Methodology Definition

### methodology.yaml

Defines the methodology models for this project:

**Stages** (adapted for knowledge system):

| Stage | Readiness | Required Artifacts (this wiki) | Quality Gate |
|-------|-----------|-------------------------------|-------------|
| document | 0-25% | Wiki page in wiki/domains/ OR wiki/log/ entry, gap analysis | Page with Summary + Key Insights |
| design | 25-50% | Spec in docs/superpowers/specs/ OR design notes | Spec approved by user |
| scaffold | 50-80% | config/ changes, empty page scaffolds, schema updates | `pipeline post` passes |
| implement | 80-95% | Python tools, wiki pages, skills, commands | `pipeline post` passes, pages ≥0.25 ratio |
| test | 95-100% | `pipeline chain health` clean, manual review | 0 validation errors, 0 orphans |

**Task Types** (knowledge system additions):

| Task Type | Required Stages | Use Case |
|-----------|----------------|----------|
| epic | document, design, scaffold, implement, test | Large initiative |
| module | document, design, scaffold, implement, test | Scoped deliverable |
| task | scaffold, implement, test | Focused unit of work |
| research | document, design | Ingest + synthesize sources. No code. |
| evolve | document, implement | Generate evolved pages from existing knowledge |
| docs | document | Documentation only |
| bug | document, implement, test | Fix broken tooling or incorrect content |
| refactor | document, scaffold, implement, test | Restructure tooling or organization |

**Execution Modes**: autonomous, full-autonomous, semi-autonomous, document-only, design-only, scaffold-only, plan, custom. (Carried over from OpenArms unchanged.)

**End Conditions**: backlog-empty, stage-reached, time-limit, cost-limit, task-count. (Carried over unchanged.)

### agent-directive.md

The work loop, stage enforcement rules, git management, quality gates. Adapted from OpenArms' agent-directive with wiki-specific commands (`pipeline post` instead of `pnpm tsgo`).

## Schema Changes

### New page types in config/schema.yaml

Add to the `type` enum:
- `epic`
- `module` (note: already exists as a concept — this is the backlog type, distinguished by `domain: backlog`)
- `task` (same distinction)
- `note`

### New domains

- `backlog`
- `log`

### New optional frontmatter fields

```yaml
# Backlog fields (for epic/module/task types with domain: backlog)
priority: P0|P1|P2|P3
task_type: epic|module|task|research|evolve|docs|bug|refactor
current_stage: document|design|scaffold|implement|test
readiness: 0-100
stages_completed: []
artifacts: []
estimate: XS|S|M|L|XL
epic: E001
module: M001
depends_on: []

# Log fields (for note type with domain: log)
note_type: directive|session|completion
```

### Validation additions

- Backlog items: warn if `task_type` missing, warn if `readiness` > 0 but `stages_completed` empty
- Log entries: warn if `note_type` missing

## Pipeline Integration

### Post-chain update

Add wiki/backlog/ and wiki/log/ to the index rebuilding step. Backlog indexes show tables of epics/tasks with status. Log indexes show chronological entries.

### New pipeline commands

- `pipeline backlog` — show backlog summary (epics, in-progress tasks, completion %)
- `pipeline backlog --epic E001` — show epic detail with children

### New /commands

- `/backlog` — show backlog state
- `/log` — add a log entry

### MCP tools

- `wiki_backlog` — query backlog state
- `wiki_log` — add/query log entries

## Migration

### Existing raw/notes/ files

Keep in place. Do not move. New directives go to wiki/log/. The 16 existing raw/notes/ files are historical provenance.

### Existing docs/SESSION-*.md

Keep as the cross-session resume artifact. wiki/log/ session entries are per-session; the SESSION artifact is the cumulative overview.

## Success Criteria

- `wiki/backlog/` exists with _index.md and epics/modules/tasks/ subdirectories
- `wiki/log/` exists with _index.md
- `wiki/config/methodology.yaml` defines stages, task types, modes for this project
- `wiki/config/agent-directive.md` defines the work loop for this project
- `config/schema.yaml` accepts the new types and fields
- `pipeline post` validates backlog and log pages
- `pipeline backlog` shows epic/task summary
- `/backlog` and `/log` commands work in conversation
- New operator directives go to wiki/log/ not raw/notes/
