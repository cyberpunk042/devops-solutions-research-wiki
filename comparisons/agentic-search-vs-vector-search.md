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

- Has anyone empirically benchmarked agentic search vs. vector search vs. hybrid at the 200-500 page range where the transition is expected to occur?
- Can the wiki index itself serve as the structural search layer in a hybrid system (vector search over index entries, then agent navigation to specific pages)?
- How does the cost comparison work in practice -- agentic search costs tokens per navigation step, while vector search costs compute per embedding and query. At what scale does the token cost exceed the infrastructure cost?
- Does GraphRAG (building a knowledge graph from documents and using graph traversal for retrieval) converge with the LLM Wiki v2 hybrid approach from the opposite direction?
- Can the LLM Wiki's confidence scoring (from Memory Lifecycle Management) improve vector search relevance by weighting embeddings by confidence?

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
