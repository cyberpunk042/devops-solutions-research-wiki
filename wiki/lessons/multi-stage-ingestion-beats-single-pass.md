---
title: "Multi-Stage Ingestion Beats Single-Pass Processing"
type: lesson
domain: knowledge-systems
layer: 4
status: synthesized
confidence: high
maturity: growing
created: 2026-04-08
updated: 2026-04-10
sources:
  - id: src-karpathy-llm-wiki-idea-file
    type: documentation
    url: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
    title: "Karpathy LLM Wiki Idea File"
  - id: src-llm-wiki-v2-agentmemory
    type: documentation
    url: "https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2"
    title: "LLM Wiki v2 — Extending Karpathy's LLM Wiki Pattern with Lessons from Building Agentmemory"
  - id: src-user-directive-ecosystem
    type: notes
    file: raw/notes/2026-04-08-user-directive-ecosystem-connections.md
    title: "User Directive — Ecosystem Connections & Automation Vision"
tags: [ingestion, multi-pass, pipeline, cross-reference, gap-analysis, deepening, orchestration, compounding-knowledge]
derived_from:
  - "Wiki Ingestion Pipeline"
  - "Research Pipeline Orchestration"
---

# Multi-Stage Ingestion Beats Single-Pass Processing

## Summary

Ingestion should be multi-pass — extract, then cross-reference, then identify gaps, then deepen — rather than one-shot. Each pass discovers relationships and gaps the previous one could not see, because relationships only become visible once enough context exists to recognize them. The wiki itself improves with each ingestion cycle, and single-pass ingestion systematically underproduces the relationship density that makes a wiki valuable.

## Context

This lesson applies when building any ingestion pipeline for structured knowledge: LLM wikis, RAG pipelines, knowledge graphs, or documentation systems. It is triggered the first time you ingest a batch of sources and notice that the resulting pages are mostly islands — well-summarized individually but weakly connected to each other.

Single-pass ingestion feels efficient on first encounter: drop in a source, get pages out, done. The failure mode only becomes visible when you ask a cross-cutting question and the wiki cannot answer it, or when you notice that two pages cover overlapping concepts without acknowledging each other, or when a domain has many pages but no synthesis page that connects them. These are multi-pass failures — artifacts that only a second pass through the knowledge base can discover and repair.

## Insight

> [!tip] Ingestion Is a Cycle, Not a Step
> A single pass over a source can extract content and create pages. It cannot discover cross-source relationships, identify contradictions, or recognize that the combination of three unconnected pages implies a fourth that should exist. The minimum viable cycle: extract, cross-reference, gap-analyze, deepen.

A single pass over a source can extract content and create pages. It cannot discover relationships with content that was processed in a different session, identify that a newly created page partially contradicts an existing one, or recognize that the combination of three previously unconnected pages implies a fourth page that should exist. These cross-source operations require at least a second pass over the accumulated knowledge base.

The implication for pipeline design: ingestion is not a pipeline step — it is a pipeline cycle. The minimum viable cycle is: (1) extract pages from the source, (2) cross-reference against the existing wiki to find missing backlinks and relationship gaps, (3) run gap analysis to identify thin pages and unanswered questions, (4) deepen by researching those gaps. The cycle repeats until diminishing returns.

This is why the devops-solutions-research-wiki post-ingestion pipeline runs 6 steps after every ingest: index rebuild, manifest regeneration, validation, wikilink regeneration, lint checks, and layer index rebuild. These are not cleanup tasks — they are second-pass operations that make the first pass's output useful by integrating it into the existing knowledge graph.

The Research Pipeline Orchestration page codifies this as three operation modes that compose into trees: Sequence/Chain (A → B → C, each step feeds the next), Group (A + B + C in parallel, results merged), and Tree (branch into parallel research paths, merge at synthesis points). The deepening pipeline explicitly operates on wiki state rather than source documents: it reads the lint report, identifies thin pages, researches gaps externally, then enriches the existing pages. This loop is only possible because earlier passes created the structure that makes gaps visible.

The user directive framing is precise: "ingestion is multi-pass, not one-shot — extract → cross-reference → identify gaps → deepen. The current 2-pass implementation (Pass 1 extract, Pass 2 cross-reference) is the beginning, not the end."

## Evidence

From the Wiki Ingestion Pipeline source page on entity extraction: "The LLM Wiki v2 document argues that ingestion should go beyond prose summaries to extract structured entities (people, projects, libraries, concepts) with typed attributes and relationships. This enables graph-based queries that catch connections prose summaries miss." — Typed entity extraction is a second-pass operation that requires understanding the full source before classifying entities.

From the Wiki Ingestion Pipeline on adaptive page generation: "The AI 2027 article produced 23 wiki pages including 1 source page, 6 person pages, 5 organization pages, 1 AI systems page, multiple concept pages, and an analysis page." — This level of decomposition requires the LLM to hold the full source in context, identify entities, and then decide how they relate to each other — a process that improves when the LLM can also reference what already exists in the wiki.

From the Research Pipeline Orchestration on pipeline types: "CROSS-REFERENCE: load_manifest → gap_analysis → relationship_discovery → update_pages → integrate" and "DEEPENING: lint_report → identify_thin → research_gaps → enrich → validate → integrate." — Both are explicitly second-pass pipelines that operate on the wiki state created by first-pass ingestion.

From the LLM Wiki Pattern (LLM Wiki Pattern source page): "Three core operations: Ingest (process a new source, touching 10-15 pages per source), Query (search wiki, synthesize answers, and critically file good answers back as new pages so explorations compound), and Lint (periodic health checks for contradictions, stale claims, orphan pages, missing concepts)." — All three are different passes over the knowledge base. Lint is explicitly a maintenance pass that repairs what ingest alone could not produce.

From the LLM Wiki Pattern on the compounding mechanic: "Filing answers back into the wiki: A key compounding mechanism described in the original idea file — when a query produces a valuable comparison, analysis, or connection, it should be saved as a new wiki page. 'Your explorations compound in the knowledge base just like ingested sources do.'" — This is multi-pass ingestion where the LLM's own reasoning becomes a source for the next pass.

## Applicability

- **devops-solutions-research-wiki**: The 6-step post-ingestion pipeline is a structural implementation of this lesson. Never skip it. Every step is a second-pass operation that the first pass could not do.
- **pipeline design**: When building the Research Pipeline Orchestration engine, implement the deepening pipeline explicitly. Schedule it to run after every batch ingestion cycle, not just on demand.
- **openfleet / AICP knowledge bases**: If sister projects adopt the LLM Wiki pattern, build the post-ingestion cycle into the ingestion tooling from the start. Single-pass ingestion pipelines will produce weaker knowledge artifacts.
- **Cross-source synthesis**: The cross-reference pipeline pass is especially valuable when sources were ingested in separate sessions — relationships between sessions are invisible to single-pass ingestion and only emerge from a cross-reference pass over the full manifest.

## Relationships

- DERIVED FROM: [[Wiki Ingestion Pipeline]]
- DERIVED FROM: [[Research Pipeline Orchestration]]
- BUILDS ON: [[LLM Wiki Pattern]]
- ENABLES: [[LLM Knowledge Linting]]
- ENABLES: [[Wiki Knowledge Graph]]
- ENABLES: [[Research Pipeline Orchestration]]
- RELATES TO: [[Wiki Event-Driven Automation]]
- RELATES TO: [[Memory Lifecycle Management]]
- FEEDS INTO: [[OpenFleet]]

## Backlinks

[[Wiki Ingestion Pipeline]]
[[Research Pipeline Orchestration]]
[[LLM Wiki Pattern]]
[[LLM Knowledge Linting]]
[[Wiki Knowledge Graph]]
[[Wiki Event-Driven Automation]]
[[Memory Lifecycle Management]]
[[OpenFleet]]
[[Model: Knowledge Evolution]]
[[Never Synthesize from Descriptions Alone]]
[[Progressive Distillation]]
[[Shallow Ingestion Is Systemic, Not Isolated]]
