---
title: "Synthesis: LLM Wiki v2 -- Extending Karpathy's Pattern with Agentmemory Lessons"
type: source-synthesis
domain: knowledge-systems
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-llm-wiki-v2-agentmemory
    type: documentation
    url: "https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2"
    file: raw/articles/llm-wiki-v2-extending-karpathys-llm-wiki-pattern-with-lessons-from-building-agen.md
    title: "LLM Wiki v2 -- Extending Karpathy's LLM Wiki Pattern with Lessons from Building Agentmemory"
    ingested: 2026-04-08
tags: [llm-wiki-v2, agentmemory, memory-lifecycle, knowledge-graph, confidence-scoring, automation, multi-agent, scaling]
---

# Synthesis: LLM Wiki v2 -- Extending Karpathy's Pattern with Agentmemory Lessons

## Summary

This document by Rohit Ghumare extends Karpathy's original LLM Wiki pattern with lessons learned from building agentmemory, a persistent memory engine for AI coding agents built on the iii-engine. It validates the original pattern's core insight ("stop re-deriving, start compiling") and three-layer architecture while identifying six major gaps exposed by production use: (1) missing memory lifecycle management (confidence scoring, supersession, forgetting, consolidation tiers), (2) flat page structure that misses opportunities for typed knowledge graphs, (3) search that breaks beyond ~100-200 pages, (4) manual operations that should be event-driven, (5) insufficient quality controls and self-correction, and (6) no support for multi-agent or collaborative use. The document proposes an implementation spectrum from minimal viable wiki to full collaborative system, framing the schema document as "the real product" of the pattern.

## Key Insights

- **Memory lifecycle is the missing layer**: The original treats all wiki content as equally valid forever. In practice, knowledge has a lifecycle -- confidence should decay with time and strengthen with reinforcement, new claims should explicitly supersede old ones, and rarely-accessed facts should gradually deprioritize (Ebbinghaus forgetting curve applied to knowledge management).

- **Four-tier consolidation pipeline**: Working memory (recent observations) feeds into episodic memory (session summaries), which consolidates into semantic memory (cross-session facts), which distills into procedural memory (workflows and patterns). Each tier is more compressed, more confident, and longer-lived.

- **Typed knowledge graph over flat pages**: Entity extraction during ingestion (people, projects, libraries, concepts) with typed relationships ("uses," "depends on," "contradicts," "caused," "supersedes") enables graph traversal for queries rather than keyword search, catching structural connections that text search misses.

- **Hybrid search at scale**: Three-stream search combining BM25 (keyword), vector search (semantic similarity), and graph traversal (relationship walking), fused with reciprocal rank fusion. The index.md approach breaks beyond ~100-200 pages.

- **Event-driven automation hooks**: On new source (auto-ingest), on session start (load relevant context), on session end (compress and file insights), on query (auto-file quality answers), on memory write (check contradictions), on schedule (lint, consolidation, decay). The bookkeeping that makes people abandon wikis should be fully automated.

- **Self-healing lint**: The original's lint should go beyond suggestion to automatic correction -- orphan pages get linked, stale claims get marked, broken cross-references get repaired. Contradiction resolution should propose which claim is more likely correct based on source recency, authority, and supporting observation count.

- **Crystallization as a compounding mechanism**: Completed chains of work (research threads, debugging sessions, analyses) should be automatically distilled into structured digests that become first-class wiki pages, with extracted lessons strengthening existing knowledge.

- **The schema is the real product**: The schema document (CLAUDE.md, AGENTS.md) is more important than any individual wiki page -- it encodes entity types, relationship types, ingestion workflows, quality standards, contradiction handling, consolidation schedules, and privacy scoping. It is transferable across users in the same domain.

- **Multi-agent mesh sync**: Multiple agents working in parallel need merge strategies for shared wikis -- last-write-wins for most cases, timestamp-based resolution for conflicts, and scoping between private observations and shared knowledge.

- **Privacy and governance**: Automatic stripping of sensitive data on ingest (API keys, PII), full audit trails for all wiki operations, and reversible bulk operations for mature wikis.

- **Implementation spectrum**: Minimal (raw + wiki + index + schema), add lifecycle (confidence, supersession, decay), add structure (entities, typed relationships, graph), add automation (hooks, auto-lint), add scale (hybrid search, consolidation tiers), add collaboration (mesh sync, scoping). Pick the entry point that fits your needs.

## Deep Analysis

This document represents the most significant extension of the LLM Wiki pattern to date. Where Karpathy's original intentionally stays abstract and implementation-agnostic, this document fills in the production engineering concerns that emerge when the pattern runs at scale across many sessions.

The memory lifecycle concept is the most important addition. It transforms the wiki from a flat knowledge store (all facts equally weighted) into a probabilistic knowledge model (facts carry confidence scores that evolve over time). This directly addresses a weakness in the original pattern -- without lifecycle management, a wiki that grows through automated ingestion inevitably accumulates stale and contradictory information with no mechanism to surface or resolve these issues beyond manual linting.

The four-tier consolidation pipeline (working, episodic, semantic, procedural) maps directly to how human memory works and provides a principled answer to the question of what level of detail to preserve. Raw observations are ephemeral; patterns extracted from many observations are durable. This prevents the "junk drawer" failure mode where every observation is treated as equally important.

The event-driven automation hooks represent a shift from the original's manual-first philosophy to an automation-first one. Karpathy's original explicitly says "Personally I prefer to ingest sources one at a time and stay involved." This document pushes toward removing the human from routine operations entirely, keeping them only for curation and strategic direction. Both approaches are valid -- the right choice depends on whether the user values hands-on engagement or operational efficiency.

The emphasis on the schema as "the real product" is a meta-insight that reframes the entire pattern. The wiki pages are valuable but replaceable (they can be regenerated from raw sources). The schema -- which encodes domain-specific operational knowledge about how to process, organize, and maintain knowledge -- is the irreplaceable artifact. This is analogous to how in software, the build system and CI/CD pipeline are often more valuable than any individual source file.

## Open Questions

- What does the agentmemory implementation look like in practice -- is there a working open-source reference? (Requires: external research on the iii-engine and agentmemory GitHub repositories; not covered in existing wiki pages)
- How does mesh sync handle semantic conflicts (two agents writing contradictory facts) versus structural conflicts (two agents editing the same page)? (Requires: external research on distributed wiki merge strategies; existing wiki pages only document last-write-wins as a v2 proposal without implementation details)

### Answered Open Questions

**Q: How does confidence scoring work in practice -- is it metadata in YAML frontmatter, inline annotations, or a separate data structure?**

Cross-referencing the `Knowledge Evolution Pipeline` page and this wiki's own CLAUDE.md schema: this wiki's implementation of confidence scoring uses YAML frontmatter metadata. The `confidence` field in every page's frontmatter accepts `low`, `medium`, `high`, or `authoritative` levels. The `Knowledge Evolution Pipeline` page documents that confidence evolves through the maturity ladder — a `seed` page carries `low` or `medium` confidence by default, while a `canonical` page requires `high` or `authoritative` confidence as part of its promotion criteria. The LLM Wiki v2 document proposes Ebbinghaus-style decay over time, but the current implementation uses discrete levels rather than a continuous decay function. The pattern from existing wiki pages is: frontmatter is the correct data structure for confidence metadata because it is machine-parseable (the scorer reads it), human-visible (editors see it in YAML), and compatible with the Obsidian graph view (filterable by frontmatter field). Inline annotations and separate data structures would break the manifest regeneration pipeline.

**Q: What is the computational cost of the four-tier consolidation pipeline, and how often should promotion between tiers occur?**

Cross-referencing the `Knowledge Evolution Pipeline` page: the pipeline's scoring step is fully deterministic (pure Python, zero LLM calls), making its computational cost negligible. The expensive step is generation — sending assembled prompts to an LLM backend. The `Knowledge Evolution Pipeline` documents three backends: Claude Code (highest capability, highest cost), OpenAI/LocalAI (mid-tier, can use local hermes-3b for free), and AICP (routes through the fleet). For tier promotion, the page establishes that: (1) the scorer produces identical rankings on the same wiki state (deterministic), so running it multiple times without new ingestion is wasteful; (2) the recommended cadence from cross-referencing `Second Brain Architecture` and `PARA Methodology` is weekly triggered runs supplemented by threshold-based triggering after 5+ new pages are ingested. The practical cost model: scoring costs nothing; generation costs depend on the backend chosen; the full evolve loop should run weekly, not continuously.

**Q: Does the knowledge graph layer require a separate graph database, or can it be embedded in the markdown files?**

Cross-referencing the `LLM Wiki vs RAG` and `LLM Wiki Pattern` pages, plus the `Four-Project Ecosystem` page: the current implementation confirms that the knowledge graph layer is fully embedded in the markdown files via the `## Relationships` section. The `Four-Project Ecosystem` page documents that `kb_sync.py` parses these sections — specifically the regex `^([A-Z][A-Z /\-]+?):\s*(.+)$` — and builds 2,295 explicit relationships from 219 KB entries into LightRAG without any separate graph database. The `LLM Wiki Pattern` page states: "The wiki's explicit typed relationships enable multi-hop reasoning that RAG cannot replicate." A separate graph database (Neo4j, etc.) becomes necessary only when the wiki grows beyond the scale where link-following in markdown files is computationally expensive — the `LLM Wiki vs RAG` comparison sets that ceiling at ~200 pages for index-only navigation. At this wiki's current scale, the markdown-embedded graph layer is both sufficient and preferred for its zero-infrastructure cost.

**Q: How does mesh sync handle semantic conflicts (two agents writing contradictory facts) versus structural conflicts (two agents editing the same page)?**

Partially answerable from existing wiki knowledge: structural conflicts (two agents editing the same page) are handled by the post-chain's validation step — `python3 -m tools.validate` runs after every write and returns exit code 1 on schema errors, blocking malformed pages. The `Knowledge Evolution Pipeline` documents that `CONTRADICTS` typed relationships plus the lint pipeline's contradiction resolution step handle semantic conflicts: conflicting claims are linked bidirectionally with `CONTRADICTS`, the lint pass surfaces them with a recommended resolution (favoring higher source recency and authority), and the `--review` human gate is the final arbiter. The LLM Wiki v2's "last-write-wins for most cases, timestamp-based resolution for conflicts" proposal maps to git's merge semantics already built into this wiki (it is a git repo). Full mesh sync between multiple live agents simultaneously writing to the same markdown file still requires: external research on distributed wiki merge strategies; the existing wiki pages only document single-writer operation.

## Relationships

- DERIVED FROM: src-llm-wiki-v2-agentmemory
- BUILDS ON: LLM Wiki Pattern
- BUILDS ON: src-karpathy-llm-wiki-idea-file
- EXTENDS: LLM Knowledge Linting
- EXTENDS: Wiki Ingestion Pipeline
- RELATES TO: LLM Wiki vs RAG

## Backlinks

[[src-llm-wiki-v2-agentmemory]]
[[LLM Wiki Pattern]]
[[src-karpathy-llm-wiki-idea-file]]
[[LLM Knowledge Linting]]
[[Wiki Ingestion Pipeline]]
[[LLM Wiki vs RAG]]
