---
title: "Knowledge Systems — Domain Overview"
type: domain-overview
domain: knowledge-systems
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-08
updated: 2026-04-08
sources: []
tags: [domain-overview, knowledge-systems]
---

# Knowledge Systems — Domain Overview

## Summary

The knowledge-systems domain covers the theory and architecture of building LLM-powered knowledge bases, from Karpathy's original wiki pattern through graph-enhanced RAG and structured ingestion pipelines. It is the intellectual foundation for this wiki's own design — the domain documents the patterns the wiki itself implements. Six concept pages cover the LLM Wiki Pattern (the Karpathy origin), LightRAG (graph-based RAG framework used in OpenFleet), the Wiki Ingestion Pipeline (the operational workflow), Memory Lifecycle Management (knowledge validity over time), the Wiki Knowledge Graph (typed relationship extensions), and the LLM Wiki vs RAG comparison. Confidence is high across the board, anchored by primary source documentation from Karpathy directly and the LightRAG EMNLP 2025 paper. This domain feeds every other domain: ai-agents use the wiki as their knowledge backbone, automation tools implement the ingestion pipeline, and tools-and-platforms provide the frontend layers (Obsidian, NotebookLM).

## State of Knowledge

**Strong coverage:**
- LLM Wiki Pattern — primary source (Karpathy's idea file gist), two YouTube transcripts, LLM Wiki v2 extension document. The theoretical foundation is well-established. Confidence: high.
- LightRAG — sourced from the official GitHub documentation and OpenFleet's live integration. Four query modes, indexing pipeline, kb_sync bypass, OpenFleet's 1,545 entities / 2,295 relationships. Confidence: high.
- Wiki Ingestion Pipeline — three-phase workflow well documented from multiple Karpathy sources plus this project's own implementation. Confidence: high.
- LLM Wiki vs RAG — dedicated comparison page synthesizing the two approaches with decision criteria.
- Wiki Knowledge Graph — architectural extension proposal from LLM Wiki v2. Medium confidence (proposed, not yet fully implemented in this wiki).

**Thin coverage:**
- Memory Lifecycle Management — concept page exists but lacks implementation depth: how to implement staleness detection, which sources decay fastest, automation strategies.
- Agentic Search vs Vector Search — lives in the comparisons domain rather than here; only weakly cross-referenced.
- No coverage of vector database selection, embedding model tradeoffs, or BM25 implementation details for hybrid search.
- Obsidian graph integration with typed relationships — mentioned as a gap in Wiki Knowledge Graph but not investigated.

## Maturity Map

**Established content (pre-maturity system):**
- LLM Wiki Pattern — core concept, authoritative, the origin point for this entire project
- LightRAG — well-sourced, production-tested in OpenFleet
- Wiki Ingestion Pipeline — operational, the actual process used to build this wiki
- LLM Wiki vs RAG — synthesized comparison, decision-quality
- Wiki Knowledge Graph — synthesized from LLM Wiki v2, architectural vision
- Memory Lifecycle Management — concept-level, needs implementation depth

**Lessons (evolved layer):**
- Lesson: Convergence on LLM Wiki Pattern — cross-source validation of the core pattern
- Lesson: Convergence on Wiki Ingestion Pipeline — operational validation

## Gaps

- **Hybrid search implementation**: BM25 + vector + graph fusion (reciprocal rank fusion) is described in Wiki Knowledge Graph but no implementation guidance exists. This is the scaling path for the wiki beyond ~200 pages.
- **Entity extraction quality**: The wiki pages describe entity extraction as a desirable ingestion step but there is no evaluation of how well Claude Code performs this task across different source types.
- **Memory lifecycle automation**: The Memory Lifecycle Management concept lacks a concrete mechanism — how should staleness be detected, what triggers a review, what does deprecation look like in practice?
- **LightRAG for this wiki**: The research wiki does not yet have its own LightRAG instance; the integration path is documented in the LightRAG page but not implemented.
- **Embedding model selection**: AICP runs bge-m3 for embeddings, LightRAG recommends bge-m3 or text-embedding-3-large, but there is no structured comparison of options with latency/quality tradeoffs.
- **Chunking strategies**: Wiki pages are already section-structured (Summary, Key Insights, Deep Analysis). How this maps to optimal chunk boundaries for RAG ingestion is unexplored.

## Priorities

1. **LightRAG integration for this wiki** — Deploy a local LightRAG instance, wire kb_sync-style export, enable natural language queries against the wiki graph
2. **Hybrid search design** — Specify BM25 + vector + graph fusion architecture as a concrete implementation plan
3. **Memory lifecycle automation** — Design the staleness detection mechanism and deprecation workflow
4. **Embedding model evaluation** — Structured comparison of bge-m3, nomic-embed, text-embedding-3-large for wiki-sized documents
5. **Entity extraction validation** — Evaluate Claude Code's entity extraction quality against structured test cases

## Key Pages

1. **[LLM Wiki Pattern](../../domains/knowledge-systems/llm-wiki-pattern.md)** — The origin. Karpathy's three-operation model (Ingest, Query, Lint) and the "Obsidian is the IDE, LLM is the programmer, wiki is the codebase" framing.
2. **[Wiki Ingestion Pipeline](../../domains/knowledge-systems/wiki-ingestion-pipeline.md)** — The operational implementation of the LLM Wiki Pattern. How raw sources become interlinked pages, including batch ingestion and entity extraction.
3. **[LightRAG](../../domains/knowledge-systems/lightrag.md)** — The graph-based RAG layer that extends the wiki into a queryable knowledge graph. Production-deployed in OpenFleet; integration path for this wiki is documented here.
4. **[Wiki Knowledge Graph](../../domains/knowledge-systems/wiki-knowledge-graph.md)** — The typed-relationship extension to flat wikilinks. Describes entity extraction, graph traversal for impact analysis, and the scaling path beyond 200 pages.
5. **[LLM Wiki vs RAG](../../domains/knowledge-systems/llm-wiki-vs-rag.md)** — Side-by-side comparison; decision criteria for choosing the wiki approach over traditional vector RAG.

## FAQ

### Q: What is the LLM Wiki Pattern and how is it different from RAG?
The LLM Wiki Pattern (originated by Karpathy) stores synthesized knowledge in structured markdown with explicit interlinks; the LLM navigates by reading indexes and following links rather than doing similarity search. RAG embeds documents into a vector store and retrieves chunks by cosine similarity on every query. The wiki accumulates and compounds knowledge; RAG rediscovers from scratch each time. See [[LLM Wiki vs RAG]].

### Q: At what scale should I switch from pure wiki navigation to hybrid search?
Karpathy's sources suggest pure index navigation works well up to ~200 pages (roughly 500K words). Beyond that, the index becomes too large for one-pass reading and a three-stream hybrid (BM25 + vector + graph traversal with reciprocal rank fusion) is recommended. See [[Wiki Knowledge Graph]] and [[LLM Wiki vs RAG]].

### Q: What is LightRAG and how does it relate to the wiki?
LightRAG is a graph-based RAG framework that builds a knowledge graph from documents and uses graph traversal for multi-hop retrieval. OpenFleet uses it in production with 1,545 entities and 2,295 relationships. The wiki's ## Relationships sections are designed to be compatible with LightRAG's entity extraction. See [[LightRAG]].

### Q: How does memory lifecycle management prevent the wiki from going stale?
Memory lifecycle uses confidence scoring and status fields (raw → synthesized → stale) to track page freshness. Periodic linting detects pages not updated recently or contradicted by newer sources. The goal is to promote durable insights to canonical status while deprecating outdated claims. See [[Memory Lifecycle Management]].

### Q: What is the ingestion pipeline's three-phase model?
Phase 1 is extraction (source → summary + key insights), Phase 2 is cross-referencing (new page → existing pages → relationship mapping), Phase 3 is deepening (gap analysis → follow-up questions → next ingestion targets). The pipeline is multi-pass, not one-shot. See [[Wiki Ingestion Pipeline]].

## Relationships

- FEEDS INTO: AI Agents
- FEEDS INTO: Automation
- FEEDS INTO: Tools And Platforms
- ENABLES: Cross-Domain
- BUILDS ON: AI Models
- RELATES TO: Devops

## Backlinks

[[AI Agents]]
[[Automation]]
[[Tools And Platforms]]
[[Cross-Domain]]
[[AI Models]]
[[Devops]]
