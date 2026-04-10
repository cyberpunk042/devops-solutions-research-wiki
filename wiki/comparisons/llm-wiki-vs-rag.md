---
title: "LLM Wiki vs RAG"
type: comparison
layer: 3
maturity: growing
domain: cross-domain
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-10
sources:
  - id: src-karpathy-claude-code-10x
    type: youtube-transcript
    file: wiki/sources/src-karpathy-claude-code-10x.md
    title: "Andrej Karpathy Just 10x'd Everyone's Claude Code"
  - id: src-karpathy-llm-wiki-idea-file
    type: documentation
    url: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
    file: raw/articles/karpathy-llm-wiki-idea-file.md
    title: "Karpathy LLM Wiki Idea File"
  - id: src-llm-wiki-v2-agentmemory
    type: documentation
    url: "https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2"
    file: raw/articles/llm-wiki-v2-extending-karpathys-llm-wiki-pattern-with-lessons-from-building-agen.md
    title: "LLM Wiki v2 -- Extending Karpathy's LLM Wiki Pattern with Lessons from Building Agentmemory"
tags: [llm-wiki, rag, comparison, knowledge-retrieval, hybrid-search, vector-search, knowledge-management, cross-domain]
---

# LLM Wiki vs RAG

## Summary

A direct comparison of Karpathy's LLM Wiki Pattern against traditional Retrieval-Augmented Generation (RAG). The wiki approach uses structured markdown with explicit interlinks that the LLM navigates by reading indexes and following links. Traditional RAG uses embedding models and vector similarity to retrieve chunks on every query. The wiki accumulates and compounds knowledge over time; RAG rediscovers from scratch on each query. At small to medium scale (< 200 pages), the wiki wins on simplicity, cost, and relationship quality. At enterprise scale, RAG remains necessary. LLM Wiki v2 proposes hybrid search as the bridge.

## Comparison Matrix

| Criteria | LLM Wiki Pattern | Traditional RAG | Hybrid Search (LLM Wiki v2) |
|----------|-----------------|----------------|----------------------------|
| Retrieval mechanism | Index navigation + link following | Cosine similarity over vector embeddings | BM25 + vector + graph traversal (reciprocal rank fusion) |
| Infrastructure required | None (markdown files only) | Embedding model + vector database + chunking pipeline | Full stack: files + vector DB + graph store |
| Setup time | 5 minutes (paste Karpathy's prompt) | Hours to days | Days to weeks |
| Ongoing compute cost | Tokens per query only | Embedding re-compute on content change + query inference | Both token cost and embedding maintenance |
| Scale ceiling | ~200 pages / ~500K words | Millions of documents | Designed for scaling past 200 pages |
| Knowledge accumulation | Yes — compounds over time, curated incrementally | No — retrieves and forgets on every query | Yes — wiki layer accumulates; vector layer retrieves |
| Multi-hop reasoning | Excellent — explicit typed relationship links | Poor — chunks are decontextualized | Good — graph traversal stream captures relationships |
| Maintenance model | Periodic linting + LLM-driven updates | Re-embed on change; schema migrations | Both linting and re-indexing required |
| Hallucination risk | Low (reads synthesized, curated pages) | Medium (chunk assembly may lose context) | Low (cross-stream validation reduces errors) |
| Content change tolerance | High — edit markdown, no pipeline | Low — re-embedding required on every change | Medium — markdown edits cheap; vector re-index periodic |
| Best for | Personal KB, team wikis, < 200 curated pages | Large document archives, enterprise search | Mature wikis scaling beyond 200 pages |

## Key Insights

> [!tip] Wiki compiles knowledge; RAG re-derives on every query
> Karpathy names NotebookLM, ChatGPT file uploads, and "most RAG systems" as the "retrieve-and-forget" anti-pattern. The wiki compiles knowledge once and keeps it current. RAG starts from zero synthesis depth on every query; the wiki starts from the accumulated height of all previous sessions.

> [!abstract] Scale boundary: ~200 pages / ~500K words
> Below this, wiki navigation is cheaper and more accurate. Above this, vector search becomes necessary. LLM Wiki v2 dissolves the binary: embed RAG as one stream in a three-stream hybrid (BM25 + vector + graph traversal) with reciprocal rank fusion.

**Typed relationships enable multi-hop reasoning RAG cannot replicate.** RAG returns isolated chunks; the wiki lets the LLM trace paths across connected concepts via BUILDS ON, ENABLES, CONTRADICTS edges. These carry edge-type semantics that decontextualized chunks lack.

**Zero infrastructure vs. full stack.** Wiki = markdown files only. RAG = embedding model + vector DB + chunking pipeline. Hybrid = both. The setup time difference is minutes vs. days.

## Deep Analysis

### Decision Criteria

> [!success] Choose LLM Wiki when:
> - Knowledge base < 200 pages and actively curated
> - Multi-hop reasoning across related concepts needed
> - Infrastructure budget is zero (personal project, small team)
> - Content changes frequently (edit files, no re-indexing)

> [!warning] Choose Traditional RAG when:
> - Millions of documents that cannot be curated manually
> - Query patterns are primarily single-hop factual retrieval
> - Existing infrastructure for embedding model serving
> - Non-technical users who cannot maintain structured wiki

> [!tip] Choose Hybrid Search when:
> - Wiki approaching or exceeding 200 pages
> - Need both structural reasoning (wiki nav) and broad recall (vector search)
> - Infrastructure budget for vector store alongside wiki
> - Long-term scaling is a requirement

### Can the wiki index be used as a first-pass vector search target?

Cross-referencing the Wiki Ingestion Pipeline page: the ingestion pipeline already produces a structured index of all pages with titles, types, domains, and relationship summaries. This index is exactly the kind of compact, semantically dense document that embeds well. The LLM Wiki v2 architecture proposes hybrid search as "BM25 + vector + graph traversal with reciprocal rank fusion" — which means the wiki index (BM25/vector pass) plus link-following (graph traversal pass) is precisely the described architecture. The index file is small enough to embed cheaply and would serve as a first-pass filter before the LLM follows specific page links. This is technically feasible with existing wiki structure today.

### Karpathy's NotebookLM critique vs. NotebookLM's per-query accuracy

Cross-referencing the Second Brain Architecture page and the Claude Code Accuracy Tips source: these are not in conflict — they target different goals. Karpathy's critique is about **knowledge compounding**: NotebookLM, like most RAG systems, retrieves answers per-query without accumulating a persistent, structured knowledge graph. The wiki accumulates; NotebookLM re-derives. The NotebookLM accuracy advantage is about **per-query grounding quality**: for a single factual question, NotebookLM's grounding in 250-300 source documents produces fewer hallucinations than a local RAG system with a smaller or lower-quality index. The distinction maps directly onto the comparison matrix: "knowledge accumulation = Yes (wiki) vs No (RAG/NotebookLM)" and "hallucination risk = Low (wiki) vs Medium (RAG)." The Claude Code Accuracy Tips source actually recommends using NotebookLM as an *external knowledge base complement* to the wiki — storing research sources in NotebookLM for per-query accuracy while the wiki accumulates synthesized patterns. These are complementary layers, not competing approaches.

### At what scale does wiki navigation token cost exceed RAG infrastructure cost?

Cross-referencing the LLM Wiki Pattern and Knowledge Evolution Pipeline pages: the boundary is not purely about page count — it is about query frequency and context window size. The LLM Wiki Pattern page documents the scale ceiling as ~200 pages / ~500K words for index-only navigation. Beyond that, the index itself becomes too large to fit in a context window in a single pass, requiring either hierarchical sub-indexes or vector search as a pre-filter. The Knowledge Evolution Pipeline adds a relevant data point: as a wiki matures, each evolved canonical page is denser and more interlinked, meaning 200 mature pages may have higher effective information density than 200 seed pages. The practical answer from existing wiki knowledge: the token cost of navigation scales with O(pages read per query × turns per session), while RAG infrastructure cost is roughly fixed (embedding model hosting + vector DB). For a personal wiki queried a few times per day, wiki navigation remains cheaper well past 200 pages. For high-frequency automated querying (e.g., an agent reading the wiki on every task), RAG amortizes faster.

## Open Questions

- Has hybrid search been empirically benchmarked against pure wiki navigation at the 200-500 page transition zone? (Requires: empirical testing or external research; the wiki only documents the theoretical boundary at ~200 pages)

### Answered Open Questions

> [!example]- Can the wiki index be embedded as a vector search first pass?
> Yes. `wiki/manifest.json` is compact, semantically dense, and embeds cheaply. The wiki index (BM25/vector pass) + LightRAG link-following (graph traversal pass) is precisely the LLM Wiki v2 three-stream architecture. Technically feasible with existing tooling today.

> [!example]- When does wiki navigation cost exceed RAG infrastructure cost?
> Token cost scales with O(pages read × turns per session); RAG cost is roughly fixed. For a personal wiki queried a few times daily, wiki navigation stays cheaper well past 200 pages. For high-frequency automated querying (agent on every task), RAG amortizes faster. The precise crossover needs empirical measurement.

> [!example]- Do mature pages push the scale ceiling higher?
> Yes. Canonical pages are denser and more interlinked — higher information value per token. 200 canonical pages operate well above the floor of 200 seed pages. The ceiling is not a fixed count but a function of page quality, relationship density, and whether LightRAG is active.

> [!example]- Do typed relationships give multi-hop capabilities RAG cannot replicate?
> Yes — the core advantage. Typed edges (BUILDS ON, CONTRADICTS, ENABLES) let the LLM trace paths like "what does X enable?" RAG chunks carry no edge-type semantics. LightRAG parses these into 1,545 entities / 2,295 relationships enabling graph traversal queries unavailable to flat vector similarity.

> [!example]- Compounding vs retrieve-and-forget — the practical difference?
> RAG retrieves the same chunk on every query — zero synthesis accumulates. The wiki promotes seed → growing → mature → canonical, each promotion enriching with cross-domain insights. Every query starts from accumulated synthesis height, not zero. This is the maturity ladder from the Knowledge Evolution Pipeline.

> [!example]- How do ## Relationships interact with LightRAG?
> kb_sync.py parses `## Relationships` sections directly via REST API — deterministic, zero randomness. The wiki IS the knowledge graph source; LightRAG is the query engine. LightRAG's local/global/hybrid modes map onto wiki navigation: local = entity-centric, global = relationship-centric.

> [!example]- At what page count does index navigation become impractical?
> ~200 pages for flat index. With domain sub-indexes: ~1,000+. With LightRAG graph traversal: indefinitely. OpenFleet's LightRAG already operates at 1,545 entities — far beyond context window index capacity.

> [!example]- Wiki ingestion vs RAG chunking pipeline?
> RAG chunks mechanically (fixed-size splits, no synthesis). Wiki ingestion produces a synthesized page per concept — written as "a complete thought with provenance" (Zettelkasten permanent note standard). The wiki's 5-stage pipeline does synthesis, relationship extraction, and maturity tracking that chunking cannot.

> [!example]- How do wiki quality gates prevent hallucination?
> Quality gates enforce synthesis completeness: frontmatter, ≥30-word summary, ≥1 relationship, domain reachability, source provenance. A RAG chunk passes if it exists; a wiki page passes only if all criteria are met. Typed relationships prevent the "isolated chunk" failure mode.

> [!example]- LightRAG hybrid mode vs LLM Wiki v2 three-stream proposal?
> LightRAG's mix mode IS the practical implementation. Mix combines local (entity-centric) + global (relationship-centric) with bge-reranker-v2-m3 reranking — mapping to vector+graph. BM25 can be added as parallel first-pass filter. The kb_sync.py → LightRAG path is already implemented.

> [!example]- Are wiki and NotebookLM complementary or competing?
> Complementary. Wiki accumulates synthesized patterns (low hallucination for structural claims). NotebookLM grounds per-query answers in raw sources (high accuracy for factual retrieval). These are different services in a layered knowledge architecture.

> [!example]- Migration path to hybrid search at 200+ pages?
> Additive, not disruptive. markdown files remain unchanged; LightRAG added as query layer. manifest.json + `## Relationships` provide all inputs. Trigger: when domain sub-indexes become too large for single-context navigation (~200+ per domain or 500+ total). `LightRAG --storage-type json` enables zero-database-dependency first deployment.

## Relationships

- COMPARES TO: [[LLM Wiki Pattern]]
- EXTENDS: [[Agentic Search vs Vector Search]]
- RELATES TO: [[Wiki Knowledge Graph]]
- RELATES TO: [[Wiki Ingestion Pipeline]]
- RELATES TO: [[LightRAG]]
- RELATES TO: [[Memory Lifecycle Management]]
- RELATES TO: [[NotebookLM]]

## Backlinks

[[LLM Wiki Pattern]]
[[Agentic Search vs Vector Search]]
[[Wiki Knowledge Graph]]
[[Wiki Ingestion Pipeline]]
[[LightRAG]]
[[Memory Lifecycle Management]]
[[NotebookLM]]
[[Automated Knowledge Validation Prevents Silent Wiki Decay]]
[[Decision: Obsidian vs NotebookLM as Knowledge Interface]]
[[Decision: Wiki-First with LightRAG Upgrade Path]]
[[Graph-Enhanced Retrieval Bridges Wiki Navigation and Vector Search]]
[[Knowledge Evolution Pipeline]]
[[LLM-Maintained Wikis Outperform Static Documentation]]
[[Lesson: Knowledge Systems Is the Foundational Domain for the Entire Wiki]]
[[Lesson: Schema Is the Real Product — Not the Content]]
[[Model: NotebookLM]]
[[Model: Second Brain]]
[[NotebookLM as Grounded Research Engine Not Just Note Storage]]
[[Second Brain Architecture]]
[[Synthesis: Karpathy LLM Wiki Method via Claude Code]]
[[Synthesis: Karpathy's LLM Wiki Idea File]]
[[Synthesis: LLM Wiki v2 -- Extending Karpathy's Pattern with Agentmemory Lessons]]
[[Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py]]
[[The Wiki Maintenance Problem Is Solved by LLM Automation]]
