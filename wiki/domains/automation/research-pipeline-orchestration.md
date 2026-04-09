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

- How to handle pipeline failures mid-chain (e.g., one URL fails to fetch — skip or retry)? (Requires: external research on asyncio error handling patterns and retry strategies; not directly covered in existing wiki pages)
- How does the pipeline interact with NotebookLM's research agent (notebooklm source add-research)? (Requires: external research on notebooklm-py API specifics; not covered in existing wiki pages)

### Answered Open Questions

**Q: Should the pipeline engine be a Python script (tools/pipeline.py) or an MCP server that Claude Code invokes?**

Cross-referencing `Decision: MCP vs CLI for Tool Integration`: the decision is clear and directly applicable. The decision page states: "Wiki pipeline operations (ingest, validate, lint, export, gaps) → CLI tools invoked via Bash, guided by skills loaded on demand" and "MCP servers for external service bridges and tool discovery." The pipeline engine is exactly the category of operational tooling that belongs as a CLI Python script. The rationale: MCP schema overhead is paid on every message even in conversations not involving the pipeline; CLI invokes zero overhead when not called. The decision page also notes: "For routine operation within a dedicated wiki conversation, invoking CLI directly via Bash is lower-overhead and produces higher accuracy per the measured degradation curve." The existing `tools/pipeline.py` is the correct implementation pattern — an MCP wrapper can be added later for cross-conversation discoverability without changing the CLI-primary model.

**Q: What is the right granularity for parallelism — per-URL, per-page, per-domain?**

Cross-referencing `Agent Orchestration Patterns`: the orchestration patterns page documents the appropriate parallelism model. OpenFleet caps parallel dispatch at 2 tasks per 30-second cycle "to prevent runaway parallel execution." The sub-agent dispatch model states: "dispatch multiple sub-agents for independent tasks, but cap concurrency." For the research pipeline, the natural parallelism boundary is per-URL/per-source (each URL fetch and initial extraction is independent), not per-page (cross-referencing introduces dependencies between pages) and not per-domain (domain-level operations require knowledge of all pages in the domain). The `Knowledge Evolution Pipeline` page reinforces that "sequential: for dependent steps (extract must finish before analyze)" and "parallel: for independent inputs (ingest 12 URLs simultaneously)." The recommended granularity: parallel per-URL during the fetch+extract phase, sequential within the cross-reference and integration phases.

**Q: Can subagents be used for parallel page synthesis (one subagent per source)?**

Cross-referencing `Agent Orchestration Patterns`: yes, with explicit scope boundaries. The orchestration patterns page documents the sub-agent dispatch model: "Define the task boundary explicitly: what the sub-agent receives, what it produces, what it must not do. Initialize fresh context: do not pass the full conversation history. Collect output, validate, integrate: the parent agent receives the sub-agent's output and validates it before incorporating it." For page synthesis, each subagent receives a single raw source file and produces a single wiki page — a well-bounded task. The parent pipeline validates each page (via `tools/validate.py`) before integration. The decision page adds: "When subagents execute wiki operations in parallel, CLI invocation is preferable to MCP because each subagent gets a fresh context window. Routing subagent work through MCP adds schema overhead to each fresh context unnecessarily." Subagents are appropriate for parallel page synthesis as long as each one uses CLI tools and starts with a clean context scoped to one source.

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
[[Multi-Channel AI Agent Access]]
[[Multi-Stage Ingestion Beats Single-Pass Processing]]
[[OpenArms]]
[[PARA Methodology]]
[[Plan Execute Review Cycle]]
[[Rework Prevention]]
[[Second Brain Architecture]]
[[Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py]]
[[Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens]]
[[Synthesis: Superpowers Plugin — End of Vibe Coding (Full Tutorial)]]
[[WSL2 Development Patterns]]
