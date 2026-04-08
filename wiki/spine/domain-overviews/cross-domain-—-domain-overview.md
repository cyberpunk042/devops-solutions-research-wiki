---
title: "Cross-Domain — Domain Overview"
type: domain-overview
domain: cross-domain
layer: spine
status: synthesized
confidence: medium
maturity: seed
created: 2026-04-08
updated: 2026-04-08
sources: []
tags: [domain-overview, cross-domain]
---

# Cross-Domain — Domain Overview

## Summary

The cross-domain area is not a subject-matter domain but a structural layer — it holds comparisons, patterns, decisions, and lessons that emerge from synthesizing across two or more subject domains. Currently it contains two comparison pages (Agentic Search vs Vector Search, Skills Architecture Patterns), two lesson pages (Always Plan Before Executing, CLI Tools Beat MCP for Token Efficiency), one pattern page (Plan Execute Review Cycle), and one decision page (Decision: MCP vs CLI for Tool Integration). While small in page count, the cross-domain content represents the highest synthesis quality in the wiki — these pages document the convergences, tradeoffs, and durable principles that no single-domain page can capture. The domain is deliberately sparse: cross-domain synthesis should be selective, representing only insights with multi-source validation. Coverage will grow as the evolved layers (lessons → patterns → decisions → principles) are populated through continued ingestion.

## State of Knowledge

**Strong coverage:**
- Skills Architecture Patterns — synthesized from 8 sources across 3 ecosystems (Claude Code, Obsidian, NotebookLM). Identifies convergent design principles (SKILL.md as universal format, three-layer stratification, complexity spectrum). Confidence: high.
- Plan Execute Review Cycle — pattern with 4 documented instances (OpenFleet orchestrator, Harness Engineering, Claude Code, Research Pipeline Orchestration). Cross-validated, growing maturity. Confidence: high.
- Decision: MCP vs CLI for Tool Integration — derived from 4 sources, reversibility rated easy, decision clear. Confidence: high.
- CLI Tools Beat MCP for Token Efficiency — lesson with multi-source convergence from harness engineering, Karpathy, and token optimization sources.
- Always Plan Before Executing — lesson with convergence across harness engineering, superpowers, and OpenFleet.

**Thin coverage:**
- Agentic Search vs Vector Search — medium confidence comparison; the source set is adequate but the decision criteria for "which to use when" could be sharper.
- No cross-domain synthesis exists yet for the "deterministic brain vs LLM-driven orchestration" pattern despite it appearing in OpenFleet, devops-control-plane, and harness engineering.
- No principles page yet — the highest evolved layer (abstract, context-free principles derived from multiple patterns) has not been populated.

## Maturity Map

**Comparison pages:**
- Agentic Search vs Vector Search — synthesized, medium confidence, cross-domain
- Skills Architecture Patterns — synthesized, high confidence, 8-source validation

**Pattern pages (layer 5):**
- Plan Execute Review Cycle — growing maturity, 4 instances, cross-validated

**Lesson pages (layer 4):**
- Always Plan Before Executing — synthesized, multi-source convergence
- CLI Tools Beat MCP for Token Efficiency — synthesized, clear actionable lesson

**Decision pages (layer 6):**
- Decision: MCP vs CLI for Tool Integration — seed maturity, high confidence, actionable

**Lesson archive (lessons/ directory):**
- Lesson: Convergence on Claude Code Best Practices
- Lesson: Convergence on Claude Code Skills
- Lesson: Convergence on LLM Wiki Pattern
- Lesson: Convergence on Obsidian Knowledge Vault
- Lesson: Convergence on Wiki Ingestion Pipeline

## Gaps

- **Deterministic vs LLM-driven orchestration pattern**: The pattern of using a deterministic state machine (zero LLM calls) for operational mechanics while reserving LLM calls for reasoning appears in OpenFleet's orchestrator, devops-control-plane's architecture, and harness engineering's guardrail hierarchy — but has not been extracted as a cross-domain pattern.
- **Local-first inference as ecosystem principle**: The "local inference when adequate, cloud inference when necessary" principle appears in AICP, OpenFleet, Local LLM Quantization, and Claude Code scheduling — a candidate for a principles page.
- **The compounding knowledge principle**: Karpathy's insight that filing query answers back into the wiki compounds knowledge over time appears in LLM Wiki Pattern, Wiki Event-Driven Automation, and Memory Lifecycle Management. A cross-domain synthesis would make this actionable.
- **More lessons from ingestion**: Five convergence lessons were created but the underlying cross-source analyses for most topics have not been promoted to lessons or patterns.
- **Principles layer (layer 7)**: The highest evolved layer is completely empty. Principles like "make intelligence persistent, not ephemeral" and "enforce at runtime, not by prompt" should be extractable from current content.

## Priorities

1. **Deterministic vs LLM-driven orchestration pattern** — Extract from OpenFleet + devops-control-plane + harness engineering; high reuse value
2. **Local-first inference principle** — Synthesize from AICP + OpenFleet + Local LLM Quantization as a first principles page
3. **Promote agentic search comparison** — Sharpen decision criteria for Agentic Search vs Vector Search; promote to decision page
4. **Compounding knowledge pattern** — Extract the file-answers-back pattern from LLM Wiki Pattern + Wiki Event-Driven Automation + Memory Lifecycle
5. **First principles page** — Begin the principles layer with 2-3 abstract, durable insights from current patterns

## Key Pages

1. **[Skills Architecture Patterns](../../comparisons/skills-architecture-patterns.md)** — Cross-ecosystem synthesis across Claude Code, Obsidian, and NotebookLM. The convergence on SKILL.md as universal format and three-layer stratification.
2. **[Plan Execute Review Cycle](../../patterns/plan-execute-review-cycle.md)** — The most-validated pattern in the wiki. Four independent instances across OpenFleet, harness engineering, Claude Code, and the research pipeline.
3. **[Decision: MCP vs CLI for Tool Integration](../../decisions/mcp-vs-cli-for-tool-integration.md)** — Concrete decision with clear rationale. CLI + Skills beats MCP for token efficiency in interactive contexts.
4. **[Agentic Search vs Vector Search](../../comparisons/agentic-search-vs-vector-search.md)** — Comparison of multi-tool agentic retrieval vs pure vector similarity for knowledge base queries.

## Relationships

- SYNTHESIZES FROM: AI Agents
- SYNTHESIZES FROM: Knowledge Systems
- SYNTHESIZES FROM: Tools And Platforms
- SYNTHESIZES FROM: Automation
- SYNTHESIZES FROM: Devops
- SYNTHESIZES FROM: AI Models

## Backlinks

[[AI Agents]]
[[Knowledge Systems]]
[[Tools And Platforms]]
[[Automation]]
[[Devops]]
[[AI Models]]
