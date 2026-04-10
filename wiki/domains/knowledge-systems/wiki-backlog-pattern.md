---
title: "Wiki Backlog Pattern"
type: concept
layer: 2
maturity: growing
domain: knowledge-systems
status: synthesized
confidence: authoritative
created: 2026-04-09
updated: 2026-04-10
sources:
  - id: src-openarms-methodology-scan
    type: documentation
    file: raw/articles/openarms-methodology-scan.md
    title: "OpenArms Methodology Scan — Deep Research Findings"
    ingested: 2026-04-09
  - id: src-openfleet-methodology-scan
    type: documentation
    file: raw/articles/openfleet-methodology-scan.md
    title: "OpenFleet Methodology Scan — Deep Research Findings"
    ingested: 2026-04-09
tags: [wiki-backlog, frontmatter-state-machine, auto-loop, pm-in-wiki, epics, tasks, llm-wiki, knowledge-base, project-management, autonomous-agents, operator-directives, verbatim-log, second-brain, openarms, openfleet]
---

# Wiki Backlog Pattern

## Summary

The Wiki Backlog Pattern is an approach to project management where the wiki knowledge base also serves as the complete task tracking system: epics, modules, tasks, and issues live as typed wiki pages with YAML frontmatter that encodes status, stage, readiness, and artifact provenance. An autonomous agent can read the wiki, determine the highest-priority unblocked task, execute the next required stage, update the frontmatter, commit, and loop — indefinitely, without any external board, ticket system, or human coordination. The wiki IS the control surface. This pattern is fully implemented in OpenArms (22 tasks, 8 epics, infinite auto-loop), partially in OpenFleet (wiki/backlog/ with 17 epics), and is the target architecture for this research wiki's own evolution pipeline.

## Key Insights

> [!tip] The wiki and the backlog are the same file system
> No separate "wiki" and "task board." Domain knowledge pages and task pages coexist in the same vault with different `type` values. An agent reading `wiki/backlog/tasks/T023.md` and `wiki/domains/architecture/design-doc.md` is reading the same system. The task links to the knowledge page it produced. The knowledge page links to the epic that motivated it.

> [!warning] Frontmatter as state machine — the gate IS the file
> Task frontmatter fields form a complete, inspectable, auditable state machine without external dependencies. Setting `readiness: 100` while `stages_completed` is missing entries is an absolute prohibition. You cannot claim completion without the evidence in the file.
>
> | Field | What It Tracks |
> |-------|---------------|
> | `status` | draft → active → in-progress → blocked → done → archived |
> | `current_stage` | document / design / scaffold / implement / test |
> | `stages_completed` | Evidence of completion (list) |
> | `readiness` | 0-100 (derived from stages, not subjective) |
> | `artifacts` | File paths proving work was done |
> | `depends_on` / `blocked_by` | Dependency graph for task selection |

> [!abstract] The infinite auto-loop makes the wiki self-executing
> Read config → pick highest-priority unblocked task → determine next stage → execute → produce artifact → update frontmatter → one commit → verify → loop. Continues until end condition met (backlog-empty, time-limit, cost-limit). Not a cron job — the agent reads the wiki and does the next thing. No external scheduler required.

**Operator directives are sacrosanct verbatim log entries.** Both OpenArms and OpenFleet store founding directives as dated files that are never paraphrased, compressed, or overridden. All design decisions trace back to verbatim quotes. The log has higher authority than config.

**Priority and dependency structure in frontmatter.** `priority` (P0-P3), `epic`, `depends_on`, `blocked_by`. The agent reads YAML to determine what to do next — no PM tool required.

**Commit log as stage audit trail.** `feat(wiki): T023 document — ...` turns git history into a stage-gating ledger. A task without a scaffold commit is visibly incomplete.

> [!question] This wiki's adoption status
>
> | Component | Current State | Target (from OpenArms reference) |
> |-----------|--------------|----------------------------------|
> | `wiki/backlog/` | Exists (epics + tasks) | Full backlog with _index.md dashboard |
> | `wiki/log/` | Exists (directives + sessions) | Sacrosanct directive chain |
> | Backlog schema | Partial in schema.yaml | Full epic/module/task types with stage fields |
> | Auto-loop | `pipeline chain continue` (partial) | Full 14-step agent-directive loop |
> | Task stage-gating | Not fully implemented | readiness + stages_completed in frontmatter |

## Deep Analysis

### Full Schema: Knowledge + Backlog Types

The Wiki Backlog Pattern requires a unified schema that covers both knowledge pages and operational/project pages:

**Knowledge types** (standard wiki):
- `concept`: Summary, Key Insights, Deep Analysis, Relationships
- `reference`: Summary, Reference Data, Relationships
- `decision`: Summary, Context, Decision, Consequences, Relationships
- `pattern`: Summary, Problem, Solution, Examples, Relationships
- `lesson`: Summary, Context, Insight, Application, Relationships

**Backlog types** (project management layer):
- `epic`: Summary, Goals, Modules, Success Criteria, Relationships
- `module`: Summary, Details, Done When, Relationships (sub-unit of an epic)
- `task`: Summary, Details, Done When, Relationships (executable unit)
- `note`: Unstructured capture (session log, finding, retrospective)

**Task-specific required frontmatter** (not in knowledge pages):
```yaml
task_type: task | bug | spike | docs | refactor | epic/module
current_stage: document | design | scaffold | implement | test
readiness: 0-100
stages_completed: [document, design]
artifacts:
  - wiki/domains/architecture/design-doc.md
  - src/types/config.ts
  - src/config.test.ts
depends_on: [T019, T020]
blocked_by: []
epic: E003
priority: P1
estimate: 4h
assignee: solo-agent
```

### The Backlog Directory Structure

OpenArms' production implementation:

```
wiki/
  config/
    schema.yaml         — page type definitions, status lifecycles, quality gates
    methodology.yaml    — 5 stages, task types, modes, end conditions
    agent-directive.md  — solo agent bootstrap: 14-step work loop
    modes.yaml          — autonomy spectrum documentation
  domains/              — knowledge pages by domain (same as this wiki)
  backlog/
    _index.md           — overview table: 8 epics, status, task counts
    epics/
      E001.md           — Solo Agent Mode (P1), phases, modules, success criteria
      E002.md           — Network Rules Engine (P1)
      ...E008.md
    modules/            — mid-level groupings within epics
    tasks/
      _index.md         — full task table: ID, epic, status, stage, readiness
      T001.md → T022.md — individual task files with full frontmatter
  log/
    2026-04-08-initial-vision.md   — founding directives (sacrosanct, verbatim)
    2026-04-09-first-agent-run-findings.md  — retrospective + findings
```

The `backlog/_index.md` is the critical dashboard. It shows at a glance: which epics are active, which tasks are in-progress, which tasks are blocked. The agent reads this first on every loop iteration.

### OpenFleet's Parallel Implementation

OpenFleet implements a similar pattern but with key structural differences:

- `wiki/backlog/_index.md` — 17 epics (E001-E017) with modules and tasks
- `wiki/log/` — PO directives verbatim, chronological
- `wiki/domains/` — knowledge pages by domain

The key difference: OpenFleet has an external board (Plane/DSPD) as the authoritative task tracker. The wiki backlog is a "first brain" — it exists to give agents context, but Plane is the source of truth for task state. OpenArms eliminates this duality — the wiki IS the board, no external system required.

The advantage of OpenArms' approach: zero external dependencies for task tracking. The disadvantage: no human-facing project management UI (Plane provides Gantt charts, burndown, sprint views). The tradeoff is clear: wiki-only is optimal for solo-agent systems; external board is optimal when humans need visibility.

### The Auto-Loop Algorithm in Detail

OpenArms' 14-step agent work loop (from `wiki/config/agent-directive.md`) is the reference implementation:

1. Read CLAUDE.md → methodology.yaml → agent-directive.md → backlog/_index.md
2. Pick highest priority task (filter: epic/module scope if restricted, priority P0→P3, dependencies resolved; skip: done/archived/blocked)
3. Determine next required stage from methodology.yaml based on task_type
4. Read stage protocol from methodology.yaml (full MUST/MUST NOT/CAN list for that stage)
5. Execute ONLY that stage — produce ONLY the artifacts defined for that stage
6. Update task frontmatter: `current_stage`, `stages_completed`, `readiness`, `artifacts`, `status`
7. Git: stage ALL changed files and commit — ONE COMMIT PER STAGE (conventional commit format)
8. VERIFY: re-read task file, confirm frontmatter matches actual state
9. If more stages remain for this task, go to step 3
10. When all required stages are completed: set `status: done`, `readiness: 100`
11. Update backlog `_index.md` (move task to Completed section)
12. Write log entry to `wiki/log/` (what was done, what was found, what was deferred)
13. Check end condition (backlog-empty? time-limit? cost-limit? task-count?) — if not met, go to step 1
14. Final: commit remaining changes, print session summary

This loop is self-contained. It does not require a human to push tasks onto the agent — the agent reads the backlog and determines its own next action. The human's role shifts from "task assignment" to "backlog curation and end-condition configuration."

### The Log Directory as Operator Directive Chain

The `wiki/log/` directory in both OpenArms and OpenFleet stores operator directives as dated files treated with the same immutability as source control history. The rules:

1. **Verbatim, never paraphrased**: Operator words are logged character-for-character. OpenFleet: "Do not minimize or compact or compress or conflate anything I said, quote me verbatim." OpenArms: "Quote verbatim from wiki/log/. Never paraphrase." This research wiki's own MEMORY.md enforces the same rule.

2. **Never overridden**: Directives in `wiki/log/` supersede all other instructions. A new CLAUDE.md cannot contradict a founding directive in `wiki/log/`. The log has higher authority than the config.

3. **Date-stamped and cumulative**: Each session or founding event produces a new log file. The log is an append-only record. The full history of operator intent is recoverable.

4. **Referenced by tasks and designs**: Every task that implements a founding directive includes a direct quote. Every design doc that addresses a directive references it by log file and date. The chain from intent to implementation is traceable through the wiki's own structure.

### This Wiki's Path to Full Wiki Backlog Pattern

This research wiki (`devops-solutions-research-wiki`) currently implements the **knowledge side** of the pattern fully: domain pages, YAML frontmatter, typed relationships, quality gates, evolution pipeline, manifest generation. What is not yet implemented:

| Component | Current State | Target State |
|-----------|--------------|--------------|
| `wiki/backlog/` | Not present | epics/ + tasks/ + _index.md |
| `wiki/log/` | `raw/notes/` (raw, not wiki-typed) | Dated wiki-typed log pages |
| Backlog schema | Not in config/schema.yaml | epic/module/task types with stage fields |
| Auto-loop | `pipeline chain continue` (partial) | Full 14-step agent-directive loop |
| Task stage-gating | Not implemented | readiness + stages_completed in frontmatter |
| Operator directive chain | MEMORY.md (external) | wiki/log/ as primary source of truth |

The OpenArms implementation (`/home/jfortin/openarms/wiki/`) is the direct reference for this adoption. The wiki/config/schema.yaml, wiki/config/methodology.yaml, and wiki/config/agent-directive.md files are the templates.

### Relationship to PM Tools

> [!abstract] When wiki-backlog wins vs when PM tools win
>
> | Scenario | Winner | Why |
> |----------|--------|-----|
> | Solo agent, single operator | Wiki backlog | No external dependencies, agent reads YAML directly |
> | Multi-stakeholder team | PM tool (Plane, Linear) | Humans need burndown, Gantt, assignment tracking |
> | Agent cannot read the board | Wiki backlog | Tasks require LLM context; board state drifts from code |
> | Compliance reporting | PM tool | External audit requirements need structured export |
> | Hybrid (OpenFleet approach) | Both | Wiki as "first brain" for agents + Plane for human visibility |

### The "Wiki IS the Task Queue" Insight

> [!tip] The wiki and the task queue are ontologically identical
> A "task" to write documentation for feature X IS a knowledge page about feature X at readiness 0. When the agent completes the task, the same file becomes a knowledge page at readiness 100 with `status: done`. The artifact IS the task, proven done. This eliminates the most common PM failure mode: tasks marked "done" whose artifacts are missing or don't match what was requested. You cannot mark done without the artifact in the `artifacts` field — and it is inspectable in the same wiki.

## Open Questions

- What is the migration path from an external task board (Plane, Linear, Jira) to the Wiki Backlog Pattern? OpenFleet maintains both systems — is there value in keeping both, or does the duality create drift?
- How does the Wiki Backlog Pattern handle tasks that require human input mid-execution? OpenFleet's solution is `fleet_request_input` (an MCP tool that is not yet built). OpenArms' solution is the `semi-autonomous` mode (pause after each task). What is the wiki-native solution for asynchronous human gating?
- Can the knowledge evolution pipeline (`pipeline evolve --score`) be extended to also score backlog tasks by priority and dependency order? The scorer currently ranks knowledge pages by maturity/insight density. A unified scorer that ranks both knowledge gaps and backlog tasks would make the pipeline fully self-directing.
- The sacrosanct verbatim log principle means that directives cannot be changed after they are written. How should conflicting directives be handled? OpenFleet's approach: newer directives take precedence, but old directives are never deleted. Is this sufficient, or do wikis need a directive supersession mechanism?

## Relationships

- BUILDS ON: [[LLM Wiki Pattern]] (extends Karpathy's wiki pattern with project management types and an auto-loop)
- BUILDS ON: [[Task Lifecycle Stage-Gating]] (the frontmatter state machine is the wiki implementation of stage gates)
- BUILDS ON: [[Second Brain Architecture]] (the wiki-as-backlog is a second-brain that also executes)
- IMPLEMENTS: [[Knowledge Evolution Pipeline]] (the auto-loop operationalizes the evolution pipeline)
- ENABLES: [[Spec-Driven Development]] (when wiki pages are spec artifacts, the wiki-as-backlog makes SDD self-executing)
- RELATES TO: [[OpenFleet]] (17 epics in wiki/backlog/, verbatim PO log pattern)
- RELATES TO: [[Memory Lifecycle Management]] (wiki/log/ as sacrosanct directive store is a memory management strategy)
- RELATES TO: [[Research Pipeline Orchestration]] (the auto-loop is an orchestration pattern applied to knowledge work)
- COMPARES TO: [[PARA Methodology]] (wiki-backlog is PARA + task execution in one system)
- FEEDS INTO: [[Progressive Distillation]] (completed tasks produce knowledge pages that enter the distillation pipeline)

## Backlinks

[[LLM Wiki Pattern]]
[[Task Lifecycle Stage-Gating]]
[[Second Brain Architecture]]
[[Knowledge Evolution Pipeline]]
[[Spec-Driven Development]]
[[OpenFleet]]
[[Memory Lifecycle Management]]
[[Research Pipeline Orchestration]]
[[PARA Methodology]]
[[Progressive Distillation]]
[[Backlog Hierarchy Rules]]
[[Execution Modes and End Conditions]]
[[Methodology Framework]]
[[Stage-Gate Methodology]]
[[Task Type Artifact Matrix]]
