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

- How does the pattern handle multi-modal sources (images, audio) beyond the workaround of having the LLM view images separately? (Requires: external research on multimodal ingestion pipelines; existing wiki pages document images via local download and LLM viewing but do not address audio/video as first-class source types)
- How does the pattern handle source authority -- should a peer-reviewed paper carry more weight than a blog post during lint? (Requires: external research or implementation experience; the existing wiki pages do not define a source-authority scoring mechanism, though the LLM Wiki Pattern documents multi-source corroboration as the mechanism for confidence — more sources = higher confidence regardless of individual source type)

### Answered Open Questions

**Q: How does the schema document evolve in practice -- are there examples of mature schemas after months of use?**

Cross-referencing `LLM Wiki Pattern`: the LLM Wiki Pattern page documents this project's own CLAUDE.md as a concrete example of a mature schema. It started as a simple set of frontmatter fields and was progressively extended to include explicit page types (concept, source-synthesis, comparison, reference, deep-dive, index, lesson, pattern, decision, domain-overview, learning-path, evolution), a defined status lifecycle (raw → processing → synthesized → verified → stale), confidence levels, maturity levels (seed → growing → mature → canonical), an ingestion mode system (auto, guided, smart), and relationship verb conventions. The LLM Wiki Pattern page states: "This is a concrete example of a mature schema: it started as a simple set of frontmatter fields and was progressively extended to encode evolved page types, relationship verb conventions, and quality gates. The schema co-evolution described in the LLM Wiki v2 document is clearly visible by comparing early Karpathy prompts (minimal structure) with this project's current CLAUDE.md (comprehensive operational knowledge)." The operational CLAUDE.md in this repository is itself the evidence of how a schema evolves — from minimal to comprehensive over time, with each addition encoding a lesson learned from operating the wiki.

**Q: What is the practical upper bound of index-driven navigation before search tooling like qmd becomes necessary?**

Cross-referencing `LLM Wiki vs RAG` and `LLM Wiki Pattern`: both pages document the boundary at approximately 200 pages / 500K words. The `LLM Wiki vs RAG` comparison matrix states the scale ceiling for the LLM Wiki Pattern is "~200 pages / ~500K words" and that below this "wiki navigation is cheaper and more accurate" while above it "vector search is necessary." The `LLM Wiki Pattern` page confirms: "The LLM Wiki v2 document identifies the boundary at ~100-200 pages for index-only navigation and proposes hybrid search (BM25 + vector + graph traversal) as the solution." The practical answer: qmd (or equivalent hybrid search) becomes necessary when the wiki exceeds approximately 200 pages — at that point the master index itself becomes too large to fit in a context window for single-pass navigation, requiring either hierarchical sub-indexes (which this wiki implements via per-domain `_index.md` files) or a vector search pre-filter. Hierarchical sub-indexes extend the ceiling: a master index pointing to domain indexes, each scannable independently, pushes the effective ceiling considerably beyond 200 flat pages.

**Q: Is there a recommended approach for merging multiple single-user wikis into a shared team wiki?**

Cross-referencing `LLM Wiki Pattern`: the LLM Wiki Pattern page documents the state of this question: "The v2 document proposes mesh sync with last-write-wins, but details are sparse. Requires: external research or implementation experience." The LLM Wiki Pattern page also notes that Karpathy mentions "multiple vaults for different purposes" but frames these as separate rather than merged. The `Knowledge Evolution Pipeline` page's scored evolution mechanism provides a partial answer for the internal case: pages from different source wikis could be ingested as raw sources, then the evolution pipeline would synthesize canonical cross-source pages through the seed → growing → mature → canonical promotion path. This treats merging as a re-ingestion problem rather than a file merge problem. For true bidirectional team merges with concurrent edits, the wiki pages do not document a canonical approach — the existing architecture assumes WSL2 as a single source of truth with the `--reverse` flag for one-off reverse syncs.

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
[[Lesson: Schema Is the Real Product — Not the Content]]
