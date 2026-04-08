---
title: "Synthesis: Karpathy's LLM Wiki Idea File"
type: source-synthesis
domain: knowledge-systems
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-karpathy-llm-wiki-idea-file
    type: documentation
    url: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
    file: raw/articles/karpathy-llm-wiki-idea-file.md
    title: "Karpathy LLM Wiki Idea File"
    ingested: 2026-04-08
tags: [karpathy, llm-wiki, knowledge-base, memex, markdown, second-brain, architecture, primary-source]
---

# Synthesis: Karpathy's LLM Wiki Idea File

## Summary

This is Andrej Karpathy's original idea file for the LLM Wiki pattern, published as a GitHub Gist and designed to be copy-pasted into any LLM agent (Claude Code, OpenAI Codex, OpenCode/Pi, etc.) as a foundational prompt. Unlike the YouTube commentary that previously served as the wiki's primary source, this document is the authoritative first-party description of the pattern. It defines the core insight (stop re-deriving knowledge via RAG, start compiling it into a persistent wiki), the three-layer architecture (raw sources, wiki, schema), the three core operations (ingest, query, lint), the indexing and logging infrastructure, optional CLI tooling, and a rich set of practical tips. Karpathy explicitly connects the pattern to Vannevar Bush's 1945 Memex vision and frames the LLM as the missing piece that makes persistent personal knowledge bases viable by eliminating the maintenance burden that causes humans to abandon wikis.

## Key Insights

- **Core thesis stated directly**: "Instead of just retrieving from raw documents at query time, the LLM incrementally builds and maintains a persistent wiki." The wiki is a "persistent, compounding artifact" where cross-references, contradictions, and synthesis are pre-computed rather than re-derived on every query.

- **LLM as librarian, human as curator**: The human's job is to curate sources, direct analysis, ask good questions, and think about meaning. The LLM does "everything else" -- summarizing, cross-referencing, filing, bookkeeping. Karpathy uses Claude Code on one side and Obsidian on the other, describing it as: "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

- **Three-layer architecture defined**: (1) Raw sources -- immutable, curated documents the LLM reads but never modifies. (2) The wiki -- LLM-generated markdown files that the LLM owns entirely. (3) The schema -- a configuration document (CLAUDE.md or AGENTS.md) that encodes wiki structure, conventions, and workflows, co-evolved by the human and LLM over time.

- **Three core operations**: Ingest (process a new source, update 10-15 pages per source, interactive or batch), Query (search wiki, synthesize answers, file good answers back as new pages), and Lint (periodic health checks for contradictions, stale claims, orphan pages, missing concepts, data gaps).

- **Filing answers back into the wiki**: A key compounding mechanism -- when a query produces a valuable comparison, analysis, or connection, it should be saved as a new wiki page so explorations compound just like ingested sources do.

- **Index-driven navigation at moderate scale**: index.md as a content-oriented catalog works "surprisingly well at moderate scale (~100 sources, ~hundreds of pages)" and avoids the need for embedding-based RAG infrastructure. The index is how the LLM finds relevant pages.

- **Log as parseable timeline**: log.md is an append-only chronological record with consistent prefixes (e.g., `## [2026-04-02] ingest | Article Title`) that makes it parseable with simple Unix tools like grep.

- **Use cases span personal to enterprise**: Personal (goals, health, self-improvement), Research (papers, articles, evolving thesis), Reading a book (characters, themes, plot threads -- "think of fan wikis like Tolkien Gateway"), Business/team (Slack threads, meeting transcripts, customer calls with humans reviewing updates), and various others (competitive analysis, due diligence, trip planning, course notes).

- **Optional CLI tools for scale**: qmd (hybrid BM25/vector search with LLM re-ranking, CLI + MCP server) is recommended when the wiki outgrows index.md. But Karpathy notes you can also "vibe-code a naive search script" with the LLM's help.

- **Memex lineage**: Karpathy explicitly connects the pattern to Vannevar Bush's 1945 Memex -- "private, actively curated, with the connections between documents as valuable as the documents themselves. The part he couldn't solve was who does the maintenance. The LLM handles that."

- **Intentionally abstract**: The document deliberately avoids prescribing specific directory structures, page formats, or tooling. "The document's only job is to communicate the pattern. Your LLM can figure out the rest."

- **Practical Obsidian tips**: Web Clipper for source ingestion, downloading images locally to a fixed directory, graph view for seeing wiki shape, Marp for slide decks, Dataview plugin for querying YAML frontmatter, and Git for version history.

## Deep Analysis

This document is the definitive primary source for the LLM Wiki pattern. The earlier YouTube transcript (src-karpathy-claude-code-10x) was a third-party commentary on Karpathy's ideas; this is Karpathy's own words, providing significantly more depth and nuance.

Several details emerge that were absent or underemphasized in the YouTube transcript. First, the explicit framing of the schema document as a co-evolved artifact -- Karpathy describes it not as a static configuration but as something "you and the LLM co-evolve over time as you figure out what works for your domain." This positions the schema as a living document that captures accumulated operational knowledge about how the wiki should work.

Second, the emphasis on filing query results back into the wiki is stated more forcefully here than in the commentary. Karpathy frames this as a fundamental compounding mechanism: "your explorations compound in the knowledge base just like ingested sources do." This means the wiki grows not only through deliberate ingestion but also through the user's day-to-day interactions with it.

Third, the business/team use case is described in meaningful detail -- "an internal wiki maintained by LLMs, fed by Slack threads, meeting transcripts, project documents, customer calls. Possibly with humans in the loop reviewing updates." This suggests the pattern is not limited to solo knowledge workers but extends to organizational knowledge management.

Fourth, the "why this works" section provides the clearest articulation of the core insight: "Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass." This frames the LLM not as an intelligence amplifier but as a maintenance eliminator.

The document's deliberate abstraction is itself a design choice. By refusing to prescribe implementation details, Karpathy ensures the pattern remains portable across LLM providers, tooling ecosystems, and domain contexts. The LLM itself fills in the specifics during instantiation, making each wiki adapted to its user's needs.

## Open Questions

- How does the schema document evolve in practice -- are there examples of mature schemas after months of use?
- What is the practical upper bound of index-driven navigation before search tooling like qmd becomes necessary?
- How does the pattern handle multi-modal sources (images, audio) beyond the workaround of having the LLM view images separately?
- Is there a recommended approach for merging multiple single-user wikis into a shared team wiki?
- How does the pattern handle source authority -- should a peer-reviewed paper carry more weight than a blog post during lint?

## Relationships

- DERIVED FROM: src-karpathy-llm-wiki-idea-file
- ENABLES: LLM Wiki Pattern
- ENABLES: Wiki Ingestion Pipeline
- ENABLES: LLM Knowledge Linting
- ENABLES: Obsidian Knowledge Vault
- RELATES TO: LLM Wiki vs RAG
- SUPERSEDES: src-karpathy-claude-code-10x

## Backlinks

[[src-karpathy-llm-wiki-idea-file]]
[[LLM Wiki Pattern]]
[[Wiki Ingestion Pipeline]]
[[LLM Knowledge Linting]]
[[Obsidian Knowledge Vault]]
[[LLM Wiki vs RAG]]
[[src-karpathy-claude-code-10x]]
