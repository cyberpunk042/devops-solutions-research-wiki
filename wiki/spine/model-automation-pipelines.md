---
title: "Model: Automation and Pipelines"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [model, concept, spine, automation, pipelines, orchestration, event-driven, post-chain]
---

# Model: Automation and Pipelines

## Summary

The Automation and Pipelines model describes how this wiki transforms knowledge work from manual operations into automated, composable pipelines. The central mechanism is `tools/pipeline.py` — a Python orchestrator that chains six deterministic steps after every change: rebuild indexes, regenerate manifest, validate, regenerate wikilinks, lint, and rebuild layer indexes. Beyond post-ingestion maintenance, the model extends to event-driven hooks that fire on file system changes, schedule-triggered research loops, and multi-pass ingestion with parallel subagents. The goal is to offload every repeatable task to tooling so human attention is reserved for judgment-level decisions.

## Key Insights

- **The post-chain is the quality enforcement mechanism.** Every wiki change — whether a new ingestion, a page edit, or a relationship addition — must pass through the 6-step post-chain. The chain is not optional; it is the gate that prevents schema drift, orphan pages, and broken wikilinks from accumulating silently. Running `python3 -m tools.pipeline post` is the canonical way to close any change.

- **Three execution patterns compose into complex workflows.** Sequence/Chain (A → B → C, each step feeds the next), Group/Parallel (A + B + C run simultaneously, results merged), and Tree (branch into parallel paths, merge at synthesis points). These three primitives cover every research automation need: a single URL ingestion is a sequence; a batch of 12 URLs is a group; a topic research run with deepening passes is a tree.

- **Multi-pass ingestion is architecturally fundamental.** Single-pass ingestion produces thin pages with weak relationships. The correct model is: Extract → Cross-reference → Identify gaps → Deepen. Each pass adds structural density. The current implementation executes two passes; the target architecture adds a third deepening pass with parallel subagents per source cluster.

- **Event-driven hooks fire at six trigger points.** On new source (auto-ingest + entity extraction), on session start (load relevant context), on session end (compress and file session reasoning), on query (quality-gated auto-filing), on memory write (contradiction check), and on schedule (periodic lint + retention decay). The watcher daemon (`tools/watcher.py`) implements the filesystem-triggered subset of this.

- **The pipeline is the product.** The wiki's value is not only the pages it contains but the automated system that keeps those pages valid, linked, and current. A wiki with 500 pages but no pipeline degrades; a wiki with 100 pages and a functioning pipeline compounds.

## Deep Analysis

### The Post-Chain: Six Non-Negotiable Steps

The post-chain (`python3 -m tools.pipeline post`) runs six steps in sequence, each producing input for the next:

1. **Rebuild `_index.md` files** — Scans all domain and layer folders, regenerates the index pages that make every page reachable from its domain root.
2. **Regenerate `manifest.json`** — Rebuilds the full page inventory with layer/maturity stats, used by the gaps and crossref tools.
3. **Validate all pages** — Schema validation against `config/schema.yaml`. Errors block completion; the chain halts on any schema violation.
4. **Regenerate wikilinks** — Runs `tools/obsidian.py` to rewrite `[[wikilinks]]` across the vault, keeping the Obsidian graph accurate.
5. **Lint checks** — Runs `tools/lint.py` to catch structural problems: missing sections, thin summaries, broken relationships, orphan pages.
6. **Rebuild layer indexes** — Regenerates the `lessons/`, `patterns/`, `decisions/`, and `spine/` layer indexes.

Every step is mandatory because each catches a different failure mode. Skipping step 3 allows invalid pages to accumulate; skipping step 4 breaks the Obsidian graph; skipping step 5 allows orphan pages to escape review.

### The Three Execution Patterns

[[Research Pipeline Orchestration]] defines the three fundamental operation modes:

**Sequential chains** — Steps execute in dependency order. The canonical example is the post-chain itself: indexes before manifest, manifest before validation, validation before obsidian, obsidian before lint. Each step's output is the next step's input.

**Parallel groups** — Independent operations run concurrently. A batch ingestion of 12 URLs runs them as a parallel group: each URL fetches, parses, and writes its raw file independently. Results merge at the post-chain step.

**Tree operations** — Branch into parallel paths, merge at synthesis. A topic research run: (1) identify subtopics → (2) research each subtopic in parallel → (3) cross-reference across subtopics → (4) synthesize into a deep-dive page. The tree pattern enables multi-hop research that would take hours manually.

These three patterns are not just theoretical. They are implemented via `python3 -m tools.pipeline chain <name>`:

- `ingest` — Sequential chain for single source ingestion
- `analyze` — Parallel group for gap and crossref analysis
- `full` — Full tree: fetch + ingest + post + gaps + crossref
- `health` — Weekly health check tree
- `evolve` — Evolution scoring + scaffolding + review

### Event-Driven Automation

[[Wiki Event-Driven Automation]] describes the six hooks that extend the pipeline beyond manual invocation:

| Hook | Trigger | Implementation |
|------|---------|----------------|
| On new source | File dropped in `raw/` | `tools/watcher.py` → post-chain |
| On session start | Claude Code conversation open | Load context skill |
| On session end | Stop hook | Crystallize session into wiki page |
| On query | PostToolUse hook | Quality-score the answer, auto-file if threshold met |
| On memory write | Memory tool call | Contradiction check against existing pages |
| On schedule | systemd timer | Periodic lint + consolidation |

The watcher daemon (`python -m tools.watcher --watch`) covers the filesystem-triggered hooks. It polls for changes (not inotify — see [[Decision: Polling vs Event-Driven Change Detection]] for the WSL2 portability rationale), detects new files in `raw/`, and fires the post-chain automatically.

**Crystallization** is the most powerful of these hooks: a completed debugging session, research thread, or analysis becomes a structured wiki page automatically — capturing the reasoning before the session context evaporates.

### The Quality Enforcement Loop

The post-chain and event hooks together form a quality enforcement loop:

```
Human action → change in wiki/ or raw/
  → watcher detects change
  → post-chain fires automatically
  → validation blocks if schema invalid
  → lint reports structural issues
  → wikilinks regenerated
  → graph stays coherent
```

This loop means the wiki degrades gracefully under load. A burst of 50 new pages triggers one post-chain run, not 50. Errors surface immediately rather than accumulating over days.

### Automation Boundaries

The automation model deliberately does not automate judgment. The pipeline handles:
- Mechanical validation (schema, structure, relationships)
- Graph maintenance (indexes, manifests, wikilinks)
- Quality reporting (lint scores, gap analysis, orphan detection)
- Content generation scaffolding (templates, evolution prompts)

It does NOT automate:
- The decision to ingest a source (quality gate is human-set)
- Cross-domain synthesis (requires reasoning, not just pattern matching)
- Relationship semantics (BUILDS ON vs RELATES TO is a judgment call)
- Evolution decisions (which pages to promote from seed to canonical)

These boundary conditions are intentional. The pipeline is a force multiplier for human judgment, not a replacement for it.

## Open Questions

- **Parallel post-chain**: Can the 6 steps be partially parallelized (e.g., lint and obsidian run concurrently after manifest)? Current implementation is purely sequential.
- **Failure recovery**: If step 3 (validation) fails, should the chain attempt partial repair or halt completely? Current behavior is halt.
- **Crystallization threshold**: What quality score should trigger auto-filing from session hooks? No formal threshold is implemented yet.
- **Tree depth limits**: How many deepening passes before diminishing returns? The target architecture mentions 3 passes but no empirical data supports this number.

## Relationships

- BUILDS ON: [[Research Pipeline Orchestration]]
- BUILDS ON: [[Wiki Event-Driven Automation]]
- RELATES TO: [[Model: Knowledge Evolution]]
- RELATES TO: [[Model: Quality and Failure Prevention]]
- FEEDS INTO: [[Model: Local AI ($0 Target)]]
- RELATES TO: [[Model: NotebookLM]]
- IMPLEMENTS: [[Plan Execute Review Cycle]]
- ENABLES: [[Decision: Polling vs Event-Driven Change Detection]]

## Backlinks

[[Research Pipeline Orchestration]]
[[Wiki Event-Driven Automation]]
[[Model: Knowledge Evolution]]
[[Model: Quality and Failure Prevention]]
[[Model: Local AI ($0 Target)]]
[[Model: NotebookLM]]
[[Plan Execute Review Cycle]]
[[Decision: Polling vs Event-Driven Change Detection]]
[[Model: Design.md and IaC]]
[[Model: Second Brain]]
