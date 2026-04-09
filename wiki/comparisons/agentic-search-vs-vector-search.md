---
title: "Agentic Search vs Vector Search"
type: comparison
domain: cross-domain
status: synthesized
confidence: medium
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-karpathy-claude-code-10x
    type: youtube-transcript
    file: wiki/sources/src-karpathy-claude-code-10x.md
    title: "Andrej Karpathy Just 10x'd Everyone's Claude Code"
  - id: src-karpathy-llm-wiki-idea-file
    type: documentation
    file: wiki/sources/src-karpathy-llm-wiki-idea-file.md
    title: "Karpathy LLM Wiki Idea File"
  - id: src-llm-wiki-v2-agentmemory
    type: documentation
    file: wiki/sources/src-llm-wiki-v2-agentmemory.md
    title: "LLM Wiki v2 -- Extending Karpathy's LLM Wiki Pattern with Lessons from Building Agentmemory"
  - id: src-shanraisshan-claude-code-best-practice
    type: documentation
    file: wiki/sources/src-shanraisshan-claude-code-best-practice.md
    title: "shanraisshan/claude-code-best-practice"
  - id: src-pleaseprompto-notebooklm-skill
    type: documentation
    file: wiki/sources/src-pleaseprompto-notebooklm-skill.md
    title: "PleasePrompto/notebooklm-skill"
tags: [agentic-search, vector-search, rag, hybrid-search, knowledge-retrieval, comparison, glob-grep, index-navigation]
---

# Agentic Search vs Vector Search

## Summary

A fundamental tension runs through the research wiki: multiple sources advocate for agent-driven navigation over structured files (agentic search) while others advocate for embedding-based similarity retrieval (vector search), and a third position argues for combining both (hybrid search). This comparison synthesizes the claims, identifies where they agree and conflict, and proposes a resolution framework based on domain characteristics.

## Comparison Matrix

| Criteria | Agentic Search (glob/grep/index nav) | Vector Search (embeddings + similarity) | Hybrid Search (BM25 + vector + graph) |
|----------|-------------------------------------|----------------------------------------|---------------------------------------|
| Scale | Small-medium (< 200 pages) | Any scale | Large (> 200 pages) |
| Infrastructure | None (just files) | Embedding model + vector DB | Full stack (DB + embeddings + index) |
| Token cost | Per navigation step | Per embedding + query | Combined (navigation + retrieval) |
| Content change tolerance | High — no re-indexing needed | Low — re-embedding required on change | Medium — partial re-indexing on change |
| Multi-hop reasoning | Excellent — follows explicit links | Poor — returns isolated chunks | Good — graph traversal stream |
| Structural organization required | Yes — needs indexes and interlinks | No — works on unstructured content | Partial — benefits from structure |
| Setup time | Minutes (just files + indexes) | Hours to days (pipeline + infra) | Days (full stack integration) |
| Hallucination risk | Low (reads exact page content) | Medium (chunk retrieval may miss context) | Low (multiple streams cross-validate) |
| Best for | Code, active wikis, known-structure KB | Enterprise document collections | Mature wikis scaling past 200 pages |

## Key Insights

- Agentic search (glob/grep/index navigation) excels for fast-changing, well-structured content like codebases
- Vector search excels for large, stable knowledge bases where structural organization is weak
- LLM Wiki v2 proposes hybrid: combine both with graph traversal as a third stream
- The choice is domain-dependent, not universal — contradictions between sources dissolve when context is considered
- Claude Code team "tried and discarded" vector databases for code; Karpathy never needed them for his wiki
- PleasePrompto relies on NotebookLM's vector grounding for per-query accuracy — different optimization target

## The Three Positions

### Position 1: Agentic Search Wins (Karpathy, Claude Code team)

Karpathy's LLM Wiki Pattern uses index-driven navigation: the LLM reads a master index, follows links to relevant pages, and synthesizes answers from the structural relationships it traverses. No embeddings, no vector database, no similarity search. It "works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)."

Claude Code Best Practices reports that Claude Code's development team "tried and discarded vector databases internally because code drifts out of sync and permissions are complex. Glob + grep (agentic search) is both more accurate and simpler for navigating codebases."

Core claim: structured files with explicit navigation outperform similarity search when the knowledge is well-organized and the scale is moderate.

### Position 2: Vector Search Has Unique Value (PleasePrompto, NotebookLM)

PleasePrompto's NotebookLM skill positions NotebookLM -- which uses source-grounded retrieval similar to RAG -- as "superior to local RAG and direct document feeding for reducing hallucinations." The skill provides a comparison table showing NotebookLM's grounded retrieval outperforming both raw document feeding and local vector RAG on accuracy.

Core claim: retrieval from a grounded source collection (even without structural navigation) provides accuracy benefits, especially for hallucination reduction.

### Position 3: Hybrid Search is Necessary at Scale (LLM Wiki v2)

The LLM Wiki v2 document argues that the binary choice is a false dichotomy. At ~100-200 pages, index navigation suffices. Beyond that, a three-stream hybrid search is needed: BM25 for keyword matching, vector search for semantic similarity, and graph traversal for structural connections, fused with reciprocal rank fusion. Each stream catches things the others miss.

Core claim: different search modalities have complementary strengths, and the optimal approach combines them with the mix shifting as scale increases.

## Deep Analysis

The three positions are not truly contradictory -- they operate at different scales and in different domains:

| Factor | Agentic Search Favored | Vector Search Favored | Hybrid Favored |
|---|---|---|---|
| Scale | Small-medium (< 200 pages) | Any scale | Large (> 200 pages) |
| Content change rate | High (code, active projects) | Low-medium (reference docs) | Mixed |
| Structural organization | Well-organized with indexes | Unstructured or loosely organized | Partially structured |
| Query type | Multi-hop reasoning, relationship tracing | Single-hop fact retrieval, similarity matching | Both |
| Infrastructure tolerance | Minimal (just files) | Database + embedding model acceptable | Full stack acceptable |
| Maintenance burden | LLM maintains structure | Re-embedding on content change | Both maintenance modes |

The key insight is that **the optimal search strategy is a function of three variables: scale, content change rate, and structural organization quality**.

For codebases (high change rate, well-structured by convention), agentic search with glob + grep wins because embeddings go stale faster than the code changes, and file/folder structure provides natural navigation.

For knowledge wikis at moderate scale (low change rate, explicitly structured by LLM), index-driven agentic search wins because the LLM-maintained structure is richer than what embeddings capture, and the entire index fits in context.

For large document collections (any change rate, loosely structured), vector search is necessary because no agent can read a million-entry index in one pass.

For production knowledge systems at scale (the LLM Wiki v2 target), hybrid search combines the structural advantages of agentic navigation with the scale advantages of vector retrieval, using each where it excels.

## The NotebookLM Paradox

Karpathy explicitly names NotebookLM as an example of the "retrieve-and-forget" pattern where "the LLM is rediscovering knowledge from scratch on every question." This is a critique of NotebookLM's lack of compounding -- each query is independent, no knowledge accumulates.

Yet PleasePrompto's NotebookLM skill successfully uses this same retrieve-and-forget pattern to improve coding accuracy. The resolution: Karpathy's critique is about knowledge management (compounding over time), while PleasePrompto's use case is about answer accuracy (getting the right answer right now). Both are valid goals, and they are not in conflict -- a system could use the LLM Wiki for compounding knowledge and NotebookLM for grounded fact-checking of specific claims.

This suggests a complementary architecture: the LLM Wiki as the long-term memory (compounding, structured, agent-navigated) and NotebookLM or similar tools as the fact-checking layer (grounded, retrieval-based, used for verification rather than accumulation).

## Open Questions

- Has anyone empirically benchmarked agentic search vs. vector search vs. hybrid at the 200-500 page range where the transition is expected to occur? (Requires: empirical testing or external research; the `LLM Wiki vs RAG` page documents the theoretical boundary at ~200 pages but notes "precise crossover point requires empirical measurement with real query frequency data")
- Can the LLM Wiki's confidence scoring (from Memory Lifecycle Management) improve vector search relevance by weighting embeddings by confidence? (Requires: implementation experimentation; no existing wiki page documents confidence-weighted embeddings in this context)

## Answered Open Questions

### Can the wiki index itself serve as the structural search layer in a hybrid system (vector search over index entries, then agent navigation to specific pages)?

Cross-referencing `LLM Wiki vs RAG`: this is directly answered. The `LLM Wiki vs RAG` page states: "the ingestion pipeline already produces a structured index of all pages with titles, types, domains, and relationship summaries. This index is exactly the kind of compact, semantically dense document that embeds well. The LLM Wiki v2 architecture proposes hybrid search as 'BM25 + vector + graph traversal with reciprocal rank fusion' — which means the wiki index (BM25/vector pass) plus link-following (graph traversal pass) is precisely the described architecture. The index file is small enough to embed cheaply and would serve as a first-pass filter before the LLM follows specific page links. This is technically feasible with existing wiki structure today."

### How does the cost comparison work in practice — at what scale does the token cost of agentic navigation exceed the infrastructure cost of RAG?

Cross-referencing `LLM Wiki vs RAG`: the comparison page addresses this directly: "the boundary is not purely about page count — it is about query frequency and context window size. The token cost of navigation scales with O(pages read per query × turns per session), while RAG infrastructure cost is roughly fixed (embedding model hosting + vector DB). For a personal wiki queried a few times per day, wiki navigation remains cheaper well past 200 pages. For high-frequency automated querying (e.g., an agent reading the wiki on every task), RAG amortizes faster." The practical inflection point for this wiki: the `Context-Aware Tool Loading` pattern confirms wiki pages should be loaded on-demand (deferred loading), not pre-loaded, which reduces the per-session token cost of navigation significantly. At moderate query frequency (~10 wiki queries per day), the token cost of index navigation remains below the infrastructure cost of running an embedding model and vector database.

### Does GraphRAG (knowledge graph from documents + graph traversal for retrieval) converge with the LLM Wiki v2 hybrid approach from the opposite direction?

Cross-referencing `Wiki Knowledge Graph` and `LightRAG`: yes, they converge substantially. The `LightRAG` page documents: "Unlike traditional vector-only RAG that treats documents as isolated chunks, LightRAG extracts entities and relationships to build a knowledge graph, then retrieves via graph traversal." LightRAG's four query modes (naive, local, global, hybrid/mix) with hybrid combining entity-centric and relationship-centric retrieval maps directly onto the LLM Wiki v2 three-stream hybrid (BM25 + vector + graph). The `Wiki Knowledge Graph` page confirms the convergence: "the wiki's relationship format (- VERB: Target Name) is directly compatible with kb_sync.py's regex parser" — meaning the LLM Wiki v2 approach can be implemented via LightRAG by exporting the wiki's typed relationships into LightRAG's graph backend. GraphRAG and LLM Wiki v2 arrive at the same architecture from opposite starting points: GraphRAG builds structure from unstructured documents; LLM Wiki v2 starts from structured markdown and adds retrieval infrastructure. LightRAG is the implementation bridge between them.

## Relationships

- SYNTHESIZES: LLM Wiki vs RAG
- SYNTHESIZES: Claude Code Best Practices
- RELATES TO: LLM Wiki Pattern
- RELATES TO: Wiki Knowledge Graph
- RELATES TO: NotebookLM
- RELATES TO: NotebookLM Skills
- RELATES TO: Memory Lifecycle Management

## Backlinks

[[LLM Wiki vs RAG]]
[[Claude Code Best Practices]]
[[LLM Wiki Pattern]]
[[Wiki Knowledge Graph]]
[[NotebookLM]]
[[NotebookLM Skills]]
[[Memory Lifecycle Management]]
[[LightRAG]]
[[NotebookLM as Grounded Research Engine Not Just Note Storage]]
