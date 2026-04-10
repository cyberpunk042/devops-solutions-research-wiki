---
title: "Research Pipeline Orchestration"
type: concept
layer: 2
maturity: growing
domain: automation
status: synthesized
confidence: medium
created: 2026-04-08
updated: 2026-04-10
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

> [!info] Three operation modes that compose
>
> | Mode | How It Works | When to Use |
> |------|-------------|-------------|
> | **Chain/Sequence** | A → B → C, each step feeds the next | Dependent steps (extract before analyze) |
> | **Group/Parallel** | A + B + C simultaneously, results merged | Independent inputs (12 URLs at once) |
> | **Tree** | Branch into parallel paths, merge at synthesis | Topic → 3 sources → merge into synthesis |

> [!abstract] Five pipeline types
>
> | Pipeline | Stages |
> |----------|--------|
> | **Online Research** | web_search → fetch → save_raw → extract → synthesize → integrate |
> | **Local Ingestion** | scan_project → extract_docs → classify → create_pages → integrate |
> | **Cross-Reference** | load_manifest → gap_analysis → relationship_discovery → integrate |
> | **Deepening** | lint_report → identify_thin → research_gaps → enrich → integrate |
> | **Ecosystem Sync** | detect_changes → diff → update_or_create → cross_reference → integrate |

**Multi-pass ingestion is fundamental.** The user directive: "ingestion is multi-pass, not one-shot" — extract → cross-reference → identify gaps → deepen. The current 2-pass implementation is the beginning, not the end.

**Research lists as input.** Submit URLs, topics, or local paths. The system classifies (URL → online research, path → local ingestion, topic → web search + ingest) and routes to the right chain automatically.

**Offload repetitive work.** "Offload as much as possible the repetitive task." Auto-validate, auto-index, auto-manifest, auto-stale-check — all currently manual post-ingestion steps become pipeline stages.

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

- How to handle pipeline failures mid-chain (e.g., one URL fails to fetch — skip or retry)? (Requires: external research on asyncio error handling patterns and retry strategies; not directly covered in existing wiki pages)
- How does the pipeline interact with NotebookLM's research agent (notebooklm source add-research)? (Requires: external research on notebooklm-py API specifics; not covered in existing wiki pages)

### Answered Open Questions

> [!example]- Python CLI or MCP server for the pipeline engine?
> CLI Python script (tools/pipeline.py) is correct. MCP schema overhead is paid on every message even in conversations not involving the pipeline; CLI invokes zero overhead when not called. An MCP wrapper can be added later for cross-conversation discoverability without changing the CLI-primary model.

> [!example]- Right granularity for parallelism?
> **Parallel per-URL** during fetch+extract (each source is independent). **Sequential** within cross-reference and integration phases (dependencies between pages). Not per-page (cross-referencing introduces dependencies). Not per-domain (requires knowledge of all domain pages). OpenFleet caps parallel dispatch at 2 per cycle; similar cap recommended.

> [!example]- Can subagents do parallel page synthesis?
> Yes, with explicit scope boundaries. Each subagent receives one raw source file, produces one wiki page — well-bounded. Parent validates each page via `tools/validate.py` before integration. Use CLI tools (not MCP) in subagents — fresh context windows don't need MCP schema overhead.

## Relationships

- BUILDS ON: [[Wiki Ingestion Pipeline]]
- BUILDS ON: [[Wiki Event-Driven Automation]]
- ENABLES: [[LLM Wiki Pattern]]
- RELATES TO: [[AI-Driven Content Pipeline]]
- RELATES TO: [[Claude Code Scheduling]]
- RELATES TO: [[MCP Integration Architecture]]
- RELATES TO: [[Obsidian CLI]]
- RELATES TO: [[notebooklm-py CLI]]

## Backlinks

[[Wiki Ingestion Pipeline]]
[[Wiki Event-Driven Automation]]
[[LLM Wiki Pattern]]
[[AI-Driven Content Pipeline]]
[[Claude Code Scheduling]]
[[MCP Integration Architecture]]
[[Obsidian CLI]]
[[notebooklm-py CLI]]
[[Agent Orchestration Patterns]]
[[Always Plan Before Executing]]
[[Automated Knowledge Validation Prevents Silent Wiki Decay]]
[[Context-Aware Tool Loading]]
[[Cross-Domain Patterns]]
[[Decision: Local Model vs Cloud API for Routine Operations]]
[[Decision: MCP vs CLI for Tool Integration]]
[[Decision: Polling vs Event-Driven Change Detection]]
[[Decision: Wiki-First with LightRAG Upgrade Path]]
[[Deterministic Shell, LLM Core]]
[[Gateway-Centric Routing]]
[[Harness Engineering]]
[[Knowledge Evolution Pipeline]]
[[Lesson: Agent Orchestration Is the Highest-Connected Concept in the Wiki]]
[[Lesson: Automation Is the Bridge Between Knowledge and Action]]
[[Lesson: Knowledge Systems Is the Foundational Domain for the Entire Wiki]]
[[Model: Automation and Pipelines]]
[[Multi-Channel AI Agent Access]]
[[Multi-Stage Ingestion Beats Single-Pass Processing]]
[[OpenArms]]
[[PARA Methodology]]
[[Plan Execute Review Cycle]]
[[Rework Prevention]]
[[Second Brain Architecture]]
[[Synthesis: Context Mode — MCP Sandbox for Context Saving]]
[[Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py]]
[[Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens]]
[[Synthesis: Superpowers Plugin — End of Vibe Coding (Full Tutorial)]]
[[WSL2 Development Patterns]]
[[Wiki Backlog Pattern]]
