---
title: "LightRAG"
type: concept
domain: knowledge-systems
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-lightrag-docs
    type: documentation
    url: "https://github.com/HKUDS/LightRAG"
    title: "LightRAG — Graph-Based RAG Framework"
    ingested: 2026-04-08
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — LightRAG Integration"
    ingested: 2026-04-08
tags: [lightrag, rag, knowledge-graph, entity-extraction, graph-retrieval, vector-search, hybrid-search, mcp, openfleet]
---

# LightRAG

## Summary

LightRAG is a graph-based Retrieval-Augmented Generation framework from HKU Data Science (EMNLP 2025) that incorporates knowledge graph structures into text indexing and retrieval. Unlike traditional vector-only RAG that treats documents as isolated chunks, LightRAG extracts entities and relationships to build a knowledge graph, then retrieves via graph traversal. It provides four query modes (naive, local, global, hybrid/mix), supports incremental updates without full reconstruction, and runs as a REST API server with MCP integration. In OpenFleet, it serves as the knowledge graph backend (port 9621) with 1,545 entities and 2,295 relationships, indexed via kb_sync.py which bypasses LLM-based extraction in favor of explicit relationship parsing.

## Key Insights

- **Three-phase indexing pipeline**: (1) Entity & relationship extraction from document chunks via LLM, (2) LLM profiling to create key-value pairs with global themes, (3) Deduplication to merge identical entities across segments. Formula: `D_hat = Dedupe(Prof(Union(Recog(D_i))))`.

- **Four query modes**: Naive (chunks only), Local (entity-centric, specific queries), Global (relationship-centric, abstract queries), Hybrid/Mix (combines local + global with reranking, recommended default).

- **Dual-level retrieval**: LLM extracts local keywords (specific entities) and global keywords (broader concepts) from the query. Local keywords match entities, global keywords match relationships. One-hop graph traversal enriches context.

- **Incremental updates without full reconstruction**: For new document D', apply same indexing steps and combine via graph union. No full community hierarchy reconstruction required (unlike GraphRAG). Same token cost as processing new documents in isolation.

- **Performance dominance**: Agriculture domain: LightRAG 62.4% vs GraphRAG 43.6%. Legal domain: 54.3% vs 45.7%. Cost: <100 tokens + 1 API call per query vs GraphRAG's 610,000 tokens + hundreds of API calls.

- **OpenFleet's kb_sync bypass**: LightRAG's LLM-based entity extraction (hermes 7B) produced inconsistent results (32/0, 15/7, 21/21 entities/relations across runs). kb_sync extracts relationships from the KB's explicit `## Relationships` sections and inserts directly via REST API — zero randomness, deterministic.

- **REST API + MCP server**: Server at `localhost:9621` with endpoints for document insertion, querying, entity/relation CRUD, deletion. MCP server available via stdio and streamable-http transport. Web UI for visualization.

- **Storage backends**: Graph (Neo4j, PostgreSQL+AGE, JSON), Vector (embedding indices per model), Key-Value (LLM response cache, entity metadata). Embedding model must be locked before indexing — switching requires vector table recreation.

- **Model requirements**: Minimum 32B parameters, 32KB context (64KB recommended) for language model. Embedding: bge-m3 or text-embedding-3-large. Reranker: bge-reranker-v2-m3 (enables mix mode as default).

## Deep Analysis

### Knowledge Graph vs Vector-Only RAG

The fundamental insight: vector-only RAG treats documents as bags of chunks and loses the relationships between concepts. LightRAG's graph structure preserves these relationships explicitly. When asked "How does AI influence education?", vector RAG retrieves the most similar chunks about AI and education separately. LightRAG traverses the graph from AI entities through relationship edges to education entities, following the actual conceptual connections.

This maps directly to the research wiki's design philosophy. The wiki's `## Relationships` sections (BUILDS ON, ENABLES, COMPARES TO, etc.) are essentially a manually curated knowledge graph. LightRAG can ingest this graph directly (via kb_sync.py in OpenFleet) and make it queryable with natural language.

### OpenFleet Integration Architecture

In OpenFleet, LightRAG serves as the fleet's long-term memory:
- **Indexing**: kb_sync.py parses 219 KB entries, extracts 1,545 entities and 2,295 relationships, inserts via REST API
- **Querying**: Navigator (fleet/core/navigator.py) queries LightRAG graph for agent context assembly
- **LLM backend**: Indexing uses Claude (quality), querying uses LocalAI hermes-3b (cheap), embeddings use bge-m3 (local, free)
- **MCP**: daniel-lightrag-mcp exposes 22 tools for fleet agents

### Research Wiki Integration Path

The wiki's relationship format (`- VERB: Target Name`) is directly compatible with kb_sync.py's regex parser. Export to LightRAG would:
1. Parse wiki/manifest.json for pages + relationships
2. Create entities for each page (title, type, domain, description from Summary)
3. Create relationships from `## Relationships` sections
4. Enable natural language queries against wiki knowledge: "What contradicts the LLM Wiki Pattern?" → graph traversal through CONTRADICTS edges

## Open Questions

- How does query latency scale with graph size beyond 10K entities? (Requires: external benchmarking data or LightRAG documentation on graph traversal performance at scale; existing wiki pages document the current 1,545 entity / 2,295 relationship state in OpenFleet but do not project latency beyond 10K entities)

### Answered Open Questions

**Q: Should the research wiki maintain its own LightRAG instance separate from OpenFleet's, or share one?**

Cross-referencing `OpenFleet` and `AICP`: the OpenFleet page documents LightRAG running at port 9621 as part of the OpenFleet service stack, indexed with 1,545 entities and 2,295 relationships from 219 KB entries from OpenFleet's own knowledge base and AICP SKILL.md files. The research wiki's relationship format is compatible with `kb_sync.py`'s regex parser and could be loaded into the same instance. However, AICP documents a dual-machine target architecture where each machine runs its own LocalAI cluster and Mission Control stack — implying service separation rather than sharing. The `LightRAG` page itself documents that storage backends include JSON, making a lightweight per-project instance feasible without full Neo4j infrastructure. The practical answer from existing wiki knowledge: a shared instance is simpler operationally but couples the wiki's graph to OpenFleet's operational concerns (their entities, their KB structure). A separate wiki LightRAG instance allows independent indexing, independent query tuning, and clean separation of domains. The LightRAG `--storage-type json` backend makes a lightweight wiki-only instance viable with no database dependency — the same `kb_sync.py` approach works against any LightRAG instance.

**Q: Can LightRAG's incremental updates handle the wiki's update-in-place model (editing existing pages vs only adding new ones)?**

Cross-referencing `LightRAG` and `Wiki Knowledge Graph`: the LightRAG page documents that "incremental updates" work by processing new document D' and combining via graph union — "No full community hierarchy reconstruction required (unlike GraphRAG)." However, this describes the case of *adding* new documents. The wiki's update-in-place model (editing an existing page's relationships, updating its summary) is a different operation: it requires identifying that entity/relationship records already exist for that page, deleting the old records, and inserting the updated ones. The LightRAG page documents REST API endpoints for "entity/relation CRUD, deletion" — confirming that delete+reinsert is available. The `Wiki Knowledge Graph` page documents that kb_sync.py "inserts directly via REST API" — the implementation would need to first delete existing records for a changed page, then re-parse and re-insert. This is feasible using LightRAG's deletion API, though `kb_sync.py` as documented for OpenFleet appears to be a full-rebuild sync rather than incremental. The answer: LightRAG's API supports the update-in-place pattern via delete+reinsert, but kb_sync.py would need to be extended with change detection (comparing manifest.json timestamps) to avoid full rebuilds on every sync.

**Q: What is the optimal chunk size for wiki pages that are already structured with sections?**

Cross-referencing `LLM Wiki vs RAG` and `Wiki Knowledge Graph`: the LightRAG page documents that LightRAG's indexing pipeline extracts entities and relationships from document chunks via LLM — but critically, the OpenFleet integration bypasses this entirely via `kb_sync.py`, which "extracts relationships from the KB's explicit `## Relationships` sections and inserts directly via REST API." This bypass was adopted precisely because LLM-based extraction "produced inconsistent results (32/0, 15/7, 21/21 entities/relations across runs)." For wiki pages, which are already structured with sections and explicit relationship declarations, the answer is: chunking is largely irrelevant when using the `kb_sync.py` direct-insert approach. Each wiki page becomes one entity, and its `## Relationships` section provides the edges — no chunking or LLM extraction step is needed. If using LightRAG's native LLM extraction path (not recommended for structured wiki pages), the optimal chunk size would align with section boundaries (one section per chunk), preserving the `## Summary`, `## Key Insights`, and `## Deep Analysis` sections as coherent semantic units rather than splitting mid-section.

## Relationships

- USED BY: OpenFleet
- ENABLES: Wiki Knowledge Graph
- COMPARES TO: LLM Wiki vs RAG
- RELATES TO: Agentic Search vs Vector Search
- RELATES TO: Wiki Ingestion Pipeline
- USED BY: AICP
- RELATES TO: LLM Wiki Pattern

## Backlinks

[[OpenFleet]]
[[Wiki Knowledge Graph]]
[[LLM Wiki vs RAG]]
[[Agentic Search vs Vector Search]]
[[Wiki Ingestion Pipeline]]
[[AICP]]
[[LLM Wiki Pattern]]
[[Decision: Wiki-First with LightRAG Upgrade Path]]
[[Graph-Enhanced Retrieval Bridges Wiki Navigation and Vector Search]]
[[Local LLM Quantization]]
[[Synthesis: Gemma 4 + SearXNG for Free Private OpenClaw]]
[[Synthesis: TurboQuant 122B LLM on MacBook]]
