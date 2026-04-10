---
title: "Decision: Wiki-First with LightRAG Upgrade Path"
type: decision
domain: cross-domain
layer: 6
status: synthesized
confidence: high
maturity: growing
derived_from:
  - "LLM Wiki vs RAG"
  - "LightRAG"
  - "Knowledge Evolution Pipeline"
reversibility: moderate
created: 2026-04-08
updated: 2026-04-10
sources:
  - id: src-karpathy-llm-wiki-idea-file
    type: documentation
    url: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
    title: "Karpathy LLM Wiki Idea File"
  - id: src-lightrag-docs
    type: documentation
    url: "https://github.com/HKUDS/LightRAG"
    title: "LightRAG — Graph-Based RAG Framework"
tags: [decision, rag, lightrag, llm-wiki, knowledge-systems, scale, infrastructure, architecture]
---

# Decision: Wiki-First with LightRAG Upgrade Path

## Summary

This wiki operates in wiki-first mode — pure structured markdown with index navigation — until it approaches 200 pages, at which point LightRAG integration activates as an additive query layer. No RAG infrastructure is built prematurely. The wiki's existing `## Relationships` sections are already formatted for direct insertion into LightRAG via `kb_sync.py`, making the upgrade path low-friction when the scale trigger is reached.

> [!tip] Premature Infrastructure Is Overhead Without Value
> A wiki that works well at 90 pages with zero infrastructure overhead is better than a wiki that works identically at 90 pages but carries the operational burden of an embedding pipeline, graph database, and LightRAG service. Build the upgrade path when the scale problem actually exists.

## Decision

Operate with pure wiki navigation (current state) until total page count approaches 200 or any single domain's `_index.md` becomes too large to navigate in one context pass. At that threshold, activate LightRAG in JSON storage mode (zero database dependencies) as an additive query layer — the wiki files remain unchanged, LightRAG is added on top. Do not deploy vector search infrastructure, embedding pipelines, or RAG tooling before this threshold.

The trigger conditions for activation are:
- Total wiki pages exceeds 175 (approaching the ~200-page index navigation ceiling)
- Any domain has more than 50 pages in its `_index.md`
- A query consistently requires reading 5+ domain indexes to find relevant pages

## Alternatives

**Alternative 1 — Pure RAG from day one**: Deploy a vector database and embedding pipeline immediately, index all wiki content, and use similarity search for all queries. Rejected because: (a) at 90 pages and growing, wiki navigation is simpler, cheaper, and more accurate — the `LLM Wiki vs RAG` comparison matrix explicitly documents "wiki navigation is cheaper and more accurate" below ~200 pages; (b) embedding pipelines require re-indexing on every content change, adding overhead to every ingestion; (c) RAG chunks lose the typed relationship structure (`BUILDS ON`, `ENABLES`, `COMPARES TO`) that is this wiki's primary analytical value — a RAG chunk cannot answer "what does X enable?" with the same precision as traversing ENABLES edges.

**Alternative 2 — Hybrid from day one**: Deploy both wiki navigation and LightRAG simultaneously, running both on every query and combining results. Rejected because: (a) unnecessary complexity at current scale — the problem this solves (index too large for context) does not yet exist; (b) LightRAG requires a minimum 32B parameter model and 32KB context for its indexing pipeline, which is infrastructure this project does not currently operate; (c) the added operational burden (keeping LightRAG's graph in sync with wiki edits, managing embedding model, handling service failures) is not justified when wiki navigation alone handles all current query patterns effectively.

**Alternative 3 — Wiki-only forever**: Never activate LightRAG or any RAG layer regardless of scale. Rejected because: (a) the `LLM Wiki vs RAG` comparison matrix documents a hard ceiling at ~200 pages for flat index navigation; (b) the existing `kb_sync.py` integration (already proven in OpenFleet with 1,545 entities and 2,295 relationships) provides a well-tested upgrade path; (c) refusing to plan the upgrade path is not a strategy — it is a debt that will need to be paid in a more disruptive way later.

## Rationale

The scale ceiling for wiki-first navigation is well-documented across multiple sources. The `LLM Wiki vs RAG` comparison matrix gives the quantitative boundary: ~200 pages / ~500K words. Karpathy's primary source confirms this: index-driven navigation "works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)" — the qualifier "moderate" is intentional. Below this ceiling, wiki navigation has structural advantages that RAG cannot replicate: typed relationships, pre-synthesized content (not raw chunks), progressive distillation through maturity layers, and zero infrastructure overhead.

The current wiki stands at approximately 90 pages with domain sub-indexes extending the effective ceiling. Hierarchical sub-indexes (each domain's `_index.md` separately navigable) push the practical ceiling considerably beyond 200 flat pages, meaning the threshold for activation is not imminent but is predictable.

LightRAG is the correct upgrade target rather than a generic vector store because the wiki's `## Relationships` sections are already formatted for direct deterministic insertion via `kb_sync.py`. OpenFleet already operates this architecture at production scale (1,545 entities, 2,295 relationships, 219 KB entries), and that experience documents the bypass of LightRAG's LLM-based entity extraction in favor of deterministic parsing — which is exactly how this wiki's relationship format was designed. The upgrade is additive: wiki files remain unchanged, LightRAG activates as an additional query layer without disrupting the authoring workflow.

The decision to defer activation rather than build it now reflects the LLM Wiki Pattern's core maintenance-economics insight: premature infrastructure is overhead without value. A wiki that works well at 90 pages with zero infrastructure overhead is better than a wiki that works identically at 90 pages but carries the operational burden of an embedding pipeline, graph database, and LightRAG service. Build the upgrade path when the scale problem actually exists.

## Reversibility

Moderate. Activating LightRAG is additive — it does not change wiki files, so deactivating it means simply stopping the LightRAG service and kb_sync synchronization. The wiki continues to function without it. However, if query patterns adapt to LightRAG's capabilities (natural language graph traversal, global relationship queries), reverting to pure wiki navigation may require users to adapt their query workflows. Data stored in LightRAG (entity metadata, vector embeddings) is not preserved in the wiki files and would need to be regenerated if LightRAG is redeployed after decommission.

## Dependencies

- **wiki/manifest.json**: LightRAG activation uses `manifest.json` as the machine-readable page inventory for `kb_sync.py` ingestion. Manifest must be kept current (already enforced by post-chain).
- **`## Relationships` section format**: The upgrade path depends on the wiki's relationship format remaining compatible with `kb_sync.py`'s regex parser (`^([A-Z][A-Z /\-]+?):\s*(.+)$`). Any change to relationship verb formatting would require updating the sync parser.
- **OpenFleet LightRAG service**: The production LightRAG instance in OpenFleet (port 9621) could serve as a shared backend when this wiki activates integration, avoiding duplicate service deployment. This introduces a runtime dependency on OpenFleet's availability.
- **Hardware requirements**: LightRAG's indexing pipeline (if using LLM-based extraction rather than kb_sync bypass) requires minimum 32B parameter model with 32KB context. JSON storage backend (`--storage-type json`) avoids the Neo4j/PostgreSQL database dependency, enabling zero-database-dependency deployment.

## Relationships

- DERIVED FROM: [[LLM Wiki vs RAG]]
- DERIVED FROM: [[LightRAG]]
- DERIVED FROM: [[Knowledge Evolution Pipeline]]
- COMPARES TO: [[LLM Wiki vs RAG]]
- ENABLES: [[Wiki Knowledge Graph]]
- RELATES TO: [[LLM Wiki Pattern]]
- RELATES TO: [[Research Pipeline Orchestration]]

## Backlinks

[[LLM Wiki vs RAG]]
[[LightRAG]]
[[Knowledge Evolution Pipeline]]
[[Wiki Knowledge Graph]]
[[LLM Wiki Pattern]]
[[Research Pipeline Orchestration]]
[[Ecosystem Integration Interfaces]]
[[Model: Knowledge Evolution]]
