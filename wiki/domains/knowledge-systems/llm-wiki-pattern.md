---
title: "LLM Wiki Pattern"
type: concept
domain: knowledge-systems
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-karpathy-claude-code-10x
    type: youtube-transcript
    file: raw/transcripts/karpathy-claude-code-10x.txt
    title: "Andrej Karpathy Just 10x'd Everyone's Claude Code"
    ingested: 2026-04-08
tags: [llm-wiki, knowledge-base, markdown, karpathy, second-brain, index-files]
---

# LLM Wiki Pattern

## Summary

The LLM Wiki Pattern is Andrej Karpathy's approach to building personal knowledge bases using LLMs and plain markdown files. Rather than relying on vector databases and embedding pipelines, you maintain a structured folder of markdown files with indexes and interlinks that an LLM can read, navigate, and maintain. The LLM ingests raw source documents, autonomously creates wiki pages with summaries and relationship links, and maintains a master index. This makes knowledge compound over time — unlike ephemeral chat conversations — while keeping the infrastructure as simple as a folder of text files.

## Key Insights

- **Folder structure**: A top-level vault contains a `raw/` folder for source material and a `wiki/` folder for LLM-generated pages. The wiki folder includes an `index.md` (master navigation), a `log.md` (operation history), and a `CLAUDE.md` (project instructions for the LLM).
- **Index-driven navigation**: The LLM maintains index files with links to every concept, tool, person, comparison, and source. This replaces the similarity-search mechanism of traditional RAG with explicit structural navigation.
- **Compounding knowledge**: Normal AI chats are ephemeral — context vanishes after the conversation. The wiki pattern makes knowledge persist and accumulate, so each new source enriches the existing graph of relationships.
- **Automatic relationship discovery**: When Claude Code processes a new source document, it does not simply create a single page — it may produce 5, 10, or 25 pages depending on content density, and it automatically discovers and creates cross-links between them.
- **Customizable structure**: Karpathy intentionally left the prompt vague so each user can adapt the wiki to their needs. Some vaults use flat file structures; others use subfolders organized by domain. The LLM adapts its organization based on the project context.
- **Multiple vaults for different purposes**: You can maintain separate vaults (e.g., one for research, one for personal knowledge) and connect them to different AI agents that need specific context.
- **Token efficiency**: Converting scattered files into a structured wiki dramatically reduces token consumption when querying. One user reported a 95% token reduction after migrating 383 files into the wiki format.

## Deep Analysis

The LLM Wiki Pattern represents a shift in how we think about AI knowledge management. Traditional approaches treat the knowledge retrieval problem as a search problem — embed everything into vectors and find the nearest neighbors. Karpathy's insight is that at small to medium scale (up to hundreds of pages, roughly half a million words), a well-organized set of markdown files with explicit indexes is both simpler and more effective.

The pattern works because modern LLMs with large context windows can read an index, identify which pages are relevant, follow links to those pages, and synthesize answers with full contextual understanding. This is fundamentally different from vector similarity search, which retrieves chunks based on surface-level semantic similarity without understanding the structural relationships between documents.

The architecture also has a self-improving quality: each time a new document is ingested, the LLM updates the index, creates new cross-references, and may even restructure existing pages. Over time, the wiki becomes a denser, more interconnected knowledge graph — without any manual curation beyond feeding in raw sources.

A practical advantage is portability and simplicity. There are no databases to manage, no embedding models to run, no infrastructure to maintain. The entire knowledge base is just files on disk that can be version-controlled with Git, synced with any file sync tool, or pointed at from any Claude Code project via a path reference in CLAUDE.md.

The pattern's main limitation is scale. At hundreds of pages it works well, but at millions of documents the index becomes too large to fit in context, and the sequential link-following approach becomes slow and expensive compared to vector search. The presenter suggests that for enterprise-scale use cases, traditional RAG or knowledge graph solutions are still necessary — at least given 2026-era model capabilities.

## Open Questions

- At what exact scale does the wiki pattern start to degrade compared to vector-based RAG? Is the boundary sharp or gradual?
- How does the pattern handle conflicting information from different sources? Does the LLM flag contradictions during ingestion?
- Can the wiki structure be automatically migrated to a graph database or RAG pipeline when scale demands it, preserving the relationships?
- How does the pattern perform with multi-modal sources (images, audio, video) beyond text transcripts and articles?
- What is the optimal index granularity — one master index, or hierarchical sub-indexes by domain?

## Relationships

- DERIVED FROM: src-karpathy-claude-code-10x
- COMPARES TO: LLM Wiki vs RAG
- ENABLES: Wiki Ingestion Pipeline
- USED BY: Obsidian Knowledge Vault
- FEEDS INTO: LLM Knowledge Linting

## Backlinks

[[src-karpathy-claude-code-10x]]
[[LLM Wiki vs RAG]]
[[Wiki Ingestion Pipeline]]
[[Obsidian Knowledge Vault]]
[[LLM Knowledge Linting]]
[[Synthesis: Karpathy LLM Wiki Method via Claude Code]]
