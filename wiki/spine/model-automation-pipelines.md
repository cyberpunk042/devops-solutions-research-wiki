---
title: "Model: Automation + Pipelines"
type: learning-path
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [model, learning-path, spine, automation, pipelines, orchestration]
---

# Model: Automation + Pipelines

## Summary

The Automation + Pipelines model describes how this wiki transforms knowledge work from manual operations into automated, composable pipelines. At its core, tools/pipeline.py is a Python orchestrator that chains six deterministic steps after every change: rebuild indexes, regenerate manifest, validate, regenerate wikilinks, lint, and rebuild layer indexes. Beyond post-ingestion maintenance, the model extends to event-driven hooks that fire on file changes, schedule-triggered research loops, and multi-pass ingestion with parallel subagents. The goal is to offload every repeatable task to tooling so human attention is reserved for judgment-level decisions.

## Prerequisites

- Familiarity with Python CLI tools and how they chain together
- Understanding of what wiki pages contain (frontmatter, sections, relationships)
- Basic exposure to event-driven architecture (hooks, watchers, daemons)

## Sequence

### Layer 2 — Core Concepts

1. **Research Pipeline Orchestration** ([[Research Pipeline Orchestration]])
   Entry point. Defines the architectural vision: sequence/chain, group (parallel), and tree operations. Explains pipeline types — online research, local ingestion, cross-reference, deepening, ecosystem sync. Shows how `tools/pipeline.py` is the Python orchestrator that composes existing tools.

2. **Wiki Event-Driven Automation** ([[Wiki Event-Driven Automation]])
   The six automation hooks: on new source, on session start, on session end, on query, on memory write, on schedule. Explains crystallization (capturing session reasoning before it disappears) and quality-gated auto-filing. Maps each hook to a concrete Claude Code implementation (watcher.py, Stop hook, PostToolUse hook, systemd timer).

3. **AI-Driven Content Pipeline** ([[AI-Driven Content Pipeline]])
   Automation for content generation — how Claude Code + NotebookLM produce slide decks, audio, and reports from source sets. Complements the wiki pipeline with multi-format output.

4. **Claude Code Scheduling** ([[Claude Code Scheduling]])
   Two scheduling modes: local cron (systemd timer) and remote tasks. The infrastructure layer for any on-schedule automation hook.

### Layer 5 — Patterns

5. **Plan Execute Review Cycle** ([[Plan Execute Review Cycle]])
   The structural backbone behind every pipeline: discrete planning, bounded execution, mandatory review gate. Each stage of the ingestion pipeline (EXTRACT → ANALYZE → SYNTHESIZE → WRITE → INTEGRATE + 6-step post-chain) is an instance of this pattern.

### Layer 4 — Lessons

6. **Multi-Stage Ingestion Beats Single-Pass Processing** ([[Multi-Stage Ingestion Beats Single-Pass Processing]])
   Distilled lesson: ingestion is multi-pass by design (extract → cross-reference → gaps → deepen). Single-pass produces thin pages with weak relationships.

7. **Automated Knowledge Validation Prevents Silent Wiki Decay** ([[Automated Knowledge Validation Prevents Silent Wiki Decay]])
   Distilled lesson: running `tools/validate.py` and `tools/lint.py` on every change catches schema drift, orphan pages, and relationship gaps before they accumulate into systemic debt.

### Layer 6 — Decisions

8. **Decision: Polling vs Event-Driven Change Detection** ([[Decision: Polling vs Event-Driven Change Detection]])
   Why tools/watcher.py uses filesystem polling rather than inotify. The tradeoff between simplicity, portability (WSL2 constraints), and latency.

9. **Decision: MCP vs CLI for Tool Integration** ([[Decision: MCP vs CLI for Tool Integration]])
   Why pipeline operations are CLI-first (invoked via Bash, no schema overhead) rather than MCP-first. Directly affects how automation chains are built.

## Outcomes

After completing this path you understand:

- How `pipeline.py` post-chain works and why all six steps are mandatory
- The six event-driven hooks and how each maps to a Claude Code primitive
- Why multi-pass ingestion with parallel subagents is the target architecture
- The Plan → Execute → Review enforcement mechanism that prevents silent failures
- When to use local cron vs remote scheduling vs filesystem events

## Relationships

- BUILDS ON: [[Research Pipeline Orchestration]]
- BUILDS ON: [[Wiki Event-Driven Automation]]
- RELATES TO: [[Model: Knowledge Evolution]]
- RELATES TO: [[Model: Quality + Failure Prevention]]
- FEEDS INTO: Model: Local AI ($0 Target)
- RELATES TO: [[Model: NotebookLM]]

## Backlinks

[[Research Pipeline Orchestration]]
[[Wiki Event-Driven Automation]]
[[Model: Knowledge Evolution]]
[[Model: Quality + Failure Prevention]]
[[Model: Local AI ($0 Target)]]
[[Model: NotebookLM]]
[[Model: Design.md + IaC]]
[[Model: Quality and Failure Prevention]]
