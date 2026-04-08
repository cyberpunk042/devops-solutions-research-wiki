---
title: "Research Pipeline Orchestration"
type: concept
domain: automation
status: synthesized
confidence: medium
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-user-directive-ecosystem
    type: notes
    file: raw/notes/2026-04-08-user-directive-ecosystem-connections.md
    title: "User Directive — Ecosystem Connections & Automation Vision"
    ingested: 2026-04-08
  - id: src-user-directive-integration
    type: notes
    file: raw/notes/2026-04-08-user-directive-integration-vision.md
    title: "User Directive — Integration Vision & Service Architecture"
    ingested: 2026-04-08
tags: [pipeline, orchestration, automation, chain-operations, group-operations, tree-operations, research-automation, ingestion, multi-pass]
---

# Research Pipeline Orchestration

## Summary

Research Pipeline Orchestration is the architectural vision for automating the research wiki's knowledge acquisition process from manual ingestion to autonomous chain/group/tree operations. The user directive states: "I should be able to add a list of things to research online and/or local in order to automate my needs, however many pipelines or pipelines options we need. And we need to automate what can be automated and group them and make sequence / chain and group call / trees operations in order to always move toward the targets and offload as much as possible the repetitive task." This vision transforms the wiki from a manually-fed knowledge base into a self-extending research engine with multiple pipeline types, parallel execution, and iterative deepening.

## Key Insights

- **Three operation modes**: Sequence/Chain (A → B → C, each step feeds the next), Group (A + B + C in parallel, results merged), Tree (branch into parallel paths, merge at synthesis points). These compose to create complex research workflows.

- **Multiple pipeline types**: Online research (web search → fetch → ingest → synthesize), Local ingestion (project scan → extract → create pages), Cross-referencing (gap analysis → relationship discovery → update pages), Deepening (identify thin pages → research gaps → enrich content).

- **Multi-pass ingestion is fundamental**: The user directive "ingestion is multi-pass, not one-shot" means each source goes through: extract → cross-reference → identify gaps → deepen. The current 2-pass implementation (Pass 1 extract, Pass 2 cross-reference) is the beginning, not the end.

- **Research lists as input**: Submit a list of URLs, topics, or local paths. The system processes them through the appropriate pipeline automatically. Entry points: Claude Code conversation, CLI (tools/ingest.py), future MCP server, future web UI.

- **Automated pipeline selection**: Given an input, the system classifies it (URL → online research pipeline, local path → local ingestion pipeline, topic → web search + ingest pipeline) and routes to the right chain of operations.

- **Offload repetitive work**: The directive emphasizes "offload as much as possible the repetitive task or even enhance or encapsulate one." This means: auto-validate after every page write, auto-update indexes, auto-regenerate manifest, auto-check for stale pages — all currently manual post-ingestion steps should become pipeline stages.

- **Current implementation baseline**: tools/ingest.py handles URL fetching (YouTube, GitHub, web). The wiki-agent skill defines the 5-stage pipeline (EXTRACT → ANALYZE → SYNTHESIZE → WRITE → INTEGRATE). Post-ingestion has 6 steps. But these require human initiation — the vision is autonomous execution.

## Deep Analysis

### Pipeline Architecture Vision

```
Input Layer:
  URL list, topic list, local paths, Obsidian web clips, NotebookLM exports

Routing:
  classify_input() → select_pipeline() → configure_chain()

Pipeline Types:
  1. ONLINE RESEARCH:     web_search → fetch → save_raw → extract → analyze → synthesize → write → integrate
  2. LOCAL INGESTION:     scan_project → extract_docs → classify → create_pages → cross_reference → integrate
  3. CROSS-REFERENCE:     load_manifest → gap_analysis → relationship_discovery → update_pages → integrate
  4. DEEPENING:           lint_report → identify_thin → research_gaps → enrich → validate → integrate
  5. ECOSYSTEM SYNC:      detect_changes → diff → update_or_create → cross_reference → integrate

Execution Modes:
  - Sequential:  for dependent steps (extract must finish before analyze)
  - Parallel:    for independent inputs (ingest 12 URLs simultaneously)
  - Tree:        for branching research (topic → 3 sources → merge into synthesis)

Post-Pipeline (always):
  update_indexes → regenerate_manifest → validate → regenerate_wikilinks → report
```

### Integration with Existing Tools

| Pipeline Stage | Current Tool | Enhancement Needed |
|---------------|-------------|-------------------|
| Fetch URLs | tools/ingest.py | Already automated |
| Fetch topics | WebSearch + WebFetch | Needs pipeline wrapper |
| Scan local projects | Agent (Explore) | Needs automated trigger |
| Extract pages | Claude Code (manual) | Needs skill-driven automation |
| Validate | tools/validate.py | Already automated |
| Manifest | tools/manifest.py | Already automated |
| Wikilinks | tools/obsidian.py | Already automated |
| Lint/gaps | tools/lint.py | Already automated |
| Export | tools/export.py | Already automated |
| Cross-reference | Claude Code (manual) | Needs Pass N automation |

### From CLI Tools to Pipeline Engine

The gap between current state and the vision:
1. **Current**: Each tool is a standalone CLI command. The wiki-agent skill describes the workflow. Claude Code executes it manually.
2. **Target**: A pipeline engine that chains tools automatically: `pipeline run online-research --input urls.txt` → fetch all → ingest all → cross-reference → validate → report.
3. **Implementation path**: Python orchestrator (tools/pipeline.py) that composes existing tools into chains, with parallel execution via asyncio and progress tracking.

## Open Questions

- Should the pipeline engine be a Python script (tools/pipeline.py) or an MCP server that Claude Code invokes?
- How to handle pipeline failures mid-chain (e.g., one URL fails to fetch — skip or retry)?
- What is the right granularity for parallelism — per-URL, per-page, per-domain?
- Can subagents be used for parallel page synthesis (one subagent per source)?
- How does the pipeline interact with NotebookLM's research agent (notebooklm source add-research)?

## Relationships

- BUILDS ON: Wiki Ingestion Pipeline
- BUILDS ON: Wiki Event-Driven Automation
- ENABLES: LLM Wiki Pattern
- RELATES TO: AI-Driven Content Pipeline
- RELATES TO: Claude Code Scheduling
- RELATES TO: MCP Integration Architecture
- RELATES TO: Obsidian CLI
- RELATES TO: notebooklm-py CLI

## Backlinks

[[Wiki Ingestion Pipeline]]
[[Wiki Event-Driven Automation]]
[[LLM Wiki Pattern]]
[[AI-Driven Content Pipeline]]
[[Claude Code Scheduling]]
[[MCP Integration Architecture]]
[[Obsidian CLI]]
[[notebooklm-py CLI]]
[[Always Plan Before Executing]]
[[Context-Aware Tool Loading]]
[[Decision: MCP vs CLI for Tool Integration]]
[[Harness Engineering]]
[[Multi-Stage Ingestion Beats Single-Pass Processing]]
[[Plan Execute Review Cycle]]
[[Second Brain Architecture]]
[[Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py]]
[[Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens]]
[[Synthesis: Superpowers Plugin — End of Vibe Coding (Full Tutorial)]]
