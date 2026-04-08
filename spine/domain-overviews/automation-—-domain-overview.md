---
title: "Automation — Domain Overview"
type: domain-overview
domain: automation
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-08
updated: 2026-04-08
sources: []
tags: [domain-overview, automation]
---

# Automation — Domain Overview

## Summary

The automation domain covers scheduling, pipeline orchestration, workflow automation, event-driven patterns, and service architecture for the research wiki and broader ecosystem. Five concept pages document the current and target automation state: Claude Code Scheduling (cron + remote task mechanisms), Wiki Event-Driven Automation (hook-based reactive processing), MCP Integration Architecture (the service layer evolution target), Research Pipeline Orchestration (the multi-pass automated ingestion vision), and AI-Driven Content Pipeline (the Claude + NotebookLM content generation pattern). The domain sits at the intersection of vision and implementation — several pages document what the automation should become rather than what it currently is. Confidence is medium for most pages, reflecting that these are architectural visions grounded in real sources but not yet fully implemented. MCP Integration Architecture and Research Pipeline Orchestration are the most forward-looking; Claude Code Scheduling is the most operational.

## State of Knowledge

**Strong coverage:**
- Claude Code Scheduling — two concrete mechanisms (local cron, Anthropic Cloud remote tasks) are well-documented with operational detail. Confidence: high.
- MCP Integration Architecture — the three MCP server designs and two service daemon designs are specified in detail, grounded in user directives and existing tooling. Confidence: medium (architecture is clear; implementation has not started).
- Research Pipeline Orchestration — the three operation modes (chain, group, tree) and five pipeline types are well-specified. The gap between current CLI tools and the pipeline engine vision is clearly articulated. Confidence: medium.
- Wiki Event-Driven Automation — six automation hooks are defined with clear trigger semantics. Grounded in LLM Wiki v2 and Obsidian + Claude Code source. Confidence: medium.

**Thin coverage:**
- AI-Driven Content Pipeline — the Claude + NotebookLM content generation loop is documented but primarily from a content team use case, not yet mapped to the wiki's specific research needs.
- Service daemon implementation — tools/watcher.py and tools/sync.py exist (documented in CLAUDE.md) but no wiki page covers their architecture, change detection strategy, or bidirectional sync protocol.
- Error handling and retry logic — the pipeline orchestration vision doesn't address failure modes (URL fetch failures, validation errors, partial ingestion).
- Pipeline monitoring and observability — no coverage of how to track pipeline runs, report progress, or alert on anomalies.

## Maturity Map

**Established content (pre-maturity system):**
- Claude Code Scheduling — operational, two mechanisms documented with concrete examples
- MCP Integration Architecture — architectural specification, high implementation priority
- Research Pipeline Orchestration — vision document with implementation gap analysis
- Wiki Event-Driven Automation — pattern specification, six trigger points defined
- AI-Driven Content Pipeline — synthesized from content team use case

## Gaps

- **Watcher service documentation**: tools/watcher.py is mentioned in CLAUDE.md but has no wiki page. Change detection strategy (polling vs inotify), event debouncing, and the trigger → post-chain flow deserve documentation.
- **rsync daemon architecture**: tools/sync.py is mentioned but not documented as a wiki concept. The WSL↔Windows bidirectional sync pattern, conflict resolution, and daemon lifecycle management need coverage.
- **Pipeline failure handling**: The Research Pipeline Orchestration page identifies the pipeline vision but doesn't address how to handle partial failures — which is the critical operational concern for autonomous pipelines.
- **Cron vs remote task decision criteria**: When to use local cron vs Anthropic Cloud remote tasks is documented in Claude Code Scheduling but no decision framework exists for choosing between them for wiki operations specifically.
- **End-to-end integration test**: No documentation exists for how to verify the full pipeline from URL input through post-ingestion chain and sync. This is the acceptance test for the automation vision.
- **OpenFleet orchestrator as model**: The deterministic 30-second orchestrator in OpenFleet is the most mature automation implementation in the ecosystem, but its patterns haven't been applied or extracted as a model for the wiki's pipeline design.

## Priorities

1. **Watcher service page** — Document tools/watcher.py architecture, change detection, and event-to-pipeline mapping
2. **rsync daemon page** — Document tools/sync.py bidirectional sync, conflict handling, daemon lifecycle
3. **Pipeline failure handling** — Design and document retry logic, partial failure recovery, error reporting
4. **OpenFleet orchestrator as automation model** — Extract the deterministic 30s cycle as a transferable pattern for pipeline scheduling
5. **End-to-end integration specification** — Document the complete automation path from input to sync-confirmed output

## Key Pages

1. **[MCP Integration Architecture](../../domains/automation/mcp-integration-architecture.md)** — The architectural target: three MCP servers, two service daemons, bidirectional sync. The "Claude becomes replaceable" vision in concrete form.
2. **[Research Pipeline Orchestration](../../domains/automation/research-pipeline-orchestration.md)** — The automated research vision: chain/group/tree operations, five pipeline types, multi-pass ingestion. The gap analysis between current CLI tools and the target pipeline engine.
3. **[Wiki Event-Driven Automation](../../domains/automation/wiki-event-driven-automation.md)** — Six automation hooks that replace manual wiki operations. The reactive processing model.
4. **[Claude Code Scheduling](../../domains/automation/claude-code-scheduling.md)** — The most operational page: local cron and remote Anthropic Cloud task scheduling with concrete setup examples.
5. **[AI-Driven Content Pipeline](../../domains/automation/ai-driven-content-pipeline.md)** — Claude + NotebookLM content generation loop. Relevant to the wiki's own output generation for research summaries and audio overviews.

## FAQ

### Q: What is the difference between local cron scheduling and Anthropic Cloud remote tasks?
Local cron runs Claude Code on a schedule via system crontab — zero cost beyond API usage, works offline, but requires the machine to be running. Anthropic Cloud remote tasks are triggered by Anthropic's infrastructure and can wake sleeping machines, but require an active cloud account and incur scheduling overhead. Use local cron for the wiki's daily pipeline; use remote tasks for fleet-wide coordination. See [[Claude Code Scheduling]].

### Q: What are the six wiki automation hooks and when do they fire?
The six hooks are: on-ingest (new raw file dropped), on-validate (schema check), on-post (post-ingestion chain), on-sync (WSL↔Windows sync), on-gap (orphan detection), and on-evolve (maturity promotion trigger). They convert the manual pipeline steps into reactive event-driven operations. See [[Wiki Event-Driven Automation]].

### Q: What is the MCP Integration Architecture's target state?
The target is three MCP servers (wiki, OpenFleet, AICP) plus two service daemons (watcher, sync) — replacing the current manual CLI workflow with always-on reactive automation. The watcher detects wiki changes and triggers the post-chain; the sync daemon pushes to Windows/Obsidian automatically. See [[MCP Integration Architecture]].

### Q: What is the Research Pipeline Orchestration vision and where are we now?
The vision is chain/group/tree operation modes for multi-pass automated ingestion — queue a research topic, the pipeline fetches sources, synthesizes pages, cross-references, and identifies gaps without manual steps. Currently, the tools exist as individual CLI commands; the pipeline engine that composes them is the gap. See [[Research Pipeline Orchestration]].

### Q: How does OpenFleet's orchestrator model apply to the wiki's pipeline?
OpenFleet's deterministic 30-second orchestrator is the most mature automation pattern in the ecosystem: a state-machine loop with zero LLM calls for coordination, deterministic task dispatch, and LLM calls only for actual reasoning work. The wiki's pipeline should adopt the same pattern — deterministic shell for scheduling, LLM only for ingestion and synthesis. See [[Research Pipeline Orchestration]] and [[OpenFleet]].

## Relationships

- IMPLEMENTS: Knowledge Systems
- USED BY: AI Agents
- BUILDS ON: Tools And Platforms
- RELATES TO: Devops
- EXTENDS: AI Models
- BRIDGES: Cross-Domain

## Backlinks

[[Knowledge Systems]]
[[AI Agents]]
[[Tools And Platforms]]
[[Devops]]
[[AI Models]]
[[Cross-Domain]]
