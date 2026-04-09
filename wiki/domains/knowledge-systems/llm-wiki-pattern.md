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
  - id: src-karpathy-llm-wiki-idea-file
    type: documentation
    url: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
    file: raw/articles/karpathy-llm-wiki-idea-file.md
    title: "Karpathy LLM Wiki Idea File"
    ingested: 2026-04-08
  - id: src-llm-wiki-v2-agentmemory
    type: documentation
    url: "https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2"
    file: raw/articles/llm-wiki-v2-extending-karpathys-llm-wiki-pattern-with-lessons-from-building-agen.md
    title: "LLM Wiki v2 -- Extending Karpathy's LLM Wiki Pattern with Lessons from Building Agentmemory"
    ingested: 2026-04-08
tags: [llm-wiki, knowledge-base, markdown, karpathy, second-brain, index-files, memex, schema, compounding-knowledge]
---

# LLM Wiki Pattern

## Summary

The LLM Wiki Pattern is Andrej Karpathy's approach to building personal knowledge bases using LLMs and plain markdown files. Rather than relying on vector databases and embedding pipelines, you maintain a structured folder of markdown files with indexes and interlinks that an LLM can read, navigate, and maintain. The LLM ingests raw source documents, autonomously creates wiki pages with summaries and relationship links, and maintains a master index. This makes knowledge compound over time — unlike ephemeral chat conversations — while keeping the infrastructure as simple as a folder of text files.

## Key Insights

- **Folder structure**: A top-level vault contains a `raw/` folder for source material and a `wiki/` folder for LLM-generated pages. The wiki folder includes an `index.md` (master navigation), a `log.md` (operation history), and a `CLAUDE.md` (project instructions for the LLM).
- **Index-driven navigation**: The LLM maintains index files with links to every concept, tool, person, comparison, and source. This replaces the similarity-search mechanism of traditional RAG with explicit structural navigation. Karpathy confirms this "works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)."
- **Compounding knowledge**: Normal AI chats are ephemeral — context vanishes after the conversation. The wiki pattern makes knowledge persist and accumulate, so each new source enriches the existing graph of relationships. Karpathy's original framing: "The wiki is a persistent, compounding artifact."
- **Three core operations (from primary source)**: Karpathy defines exactly three operations: *Ingest* (process a new source, touching 10-15 pages per source), *Query* (search wiki, synthesize answers, and critically file good answers back as new pages so explorations compound), and *Lint* (periodic health checks for contradictions, stale claims, orphan pages, missing concepts).
- **Filing answers back into the wiki**: A key compounding mechanism described in the original idea file — when a query produces a valuable comparison, analysis, or connection, it should be saved as a new wiki page. "Your explorations compound in the knowledge base just like ingested sources do."
- **The schema as co-evolved artifact**: The schema document (CLAUDE.md or AGENTS.md) is not a static configuration but something "you and the LLM co-evolve over time as you figure out what works for your domain." The LLM Wiki v2 document goes further, calling it "the most important file in the system" and "the real product" — encoding entity types, ingestion workflows, quality standards, and contradiction handling.
- **LLM as librarian, human as curator**: Karpathy's division of labor: "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else." He describes the workflow as: "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."
- **Automatic relationship discovery**: When Claude Code processes a new source document, it does not simply create a single page — it may produce 5, 10, or 25 pages depending on content density, and it automatically discovers and creates cross-links between them.
- **Customizable structure**: Karpathy intentionally left the prompt vague so each user can adapt the wiki to their needs. Some vaults use flat file structures; others use subfolders organized by domain. The LLM adapts its organization based on the project context.
- **Multiple vaults for different purposes**: You can maintain separate vaults (e.g., one for research, one for personal knowledge) and connect them to different AI agents that need specific context.
- **Token efficiency**: Converting scattered files into a structured wiki dramatically reduces token consumption when querying. One user reported a 95% token reduction after migrating 383 files into the wiki format.
- **Broad use case spectrum (from primary source)**: Personal (goals, health, self-improvement), Research (papers with evolving thesis), Reading a book (characters, themes — "think of fan wikis like Tolkien Gateway"), Business/team (Slack threads, meeting transcripts, customer calls with humans reviewing), and others (competitive analysis, due diligence, trip planning, course notes).
- **Memex lineage**: Karpathy explicitly connects the pattern to Vannevar Bush's 1945 Memex — "private, actively curated, with the connections between documents as valuable as the documents themselves. The part he couldn't solve was who does the maintenance. The LLM handles that."

## Deep Analysis

The LLM Wiki Pattern represents a shift in how we think about AI knowledge management. Traditional approaches treat the knowledge retrieval problem as a search problem — embed everything into vectors and find the nearest neighbors. Karpathy's insight is that at small to medium scale (up to hundreds of pages, roughly half a million words), a well-organized set of markdown files with explicit indexes is both simpler and more effective.

The pattern works because modern LLMs with large context windows can read an index, identify which pages are relevant, follow links to those pages, and synthesize answers with full contextual understanding. This is fundamentally different from vector similarity search, which retrieves chunks based on surface-level semantic similarity without understanding the structural relationships between documents.

The architecture also has a self-improving quality: each time a new document is ingested, the LLM updates the index, creates new cross-references, and may even restructure existing pages. Over time, the wiki becomes a denser, more interconnected knowledge graph — without any manual curation beyond feeding in raw sources.

A practical advantage is portability and simplicity. There are no databases to manage, no embedding models to run, no infrastructure to maintain. The entire knowledge base is just files on disk that can be version-controlled with Git, synced with any file sync tool, or pointed at from any Claude Code project via a path reference in CLAUDE.md. As Karpathy states: "The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free."

The core philosophical insight, stated most clearly in the primary source, is about maintenance economics: "Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass. The wiki stays maintained because the cost of maintenance is near zero." This frames the LLM not as an intelligence amplifier but as a maintenance eliminator — solving the specific problem that has killed every previous personal wiki attempt.

The pattern's main limitation is scale. At hundreds of pages it works well, but at millions of documents the index becomes too large to fit in context, and the sequential link-following approach becomes slow and expensive compared to vector search. The LLM Wiki v2 document identifies the boundary at ~100-200 pages for index-only navigation and proposes hybrid search (BM25 + vector + graph traversal) as the solution. For enterprise-scale use cases, traditional RAG or knowledge graph solutions may still be necessary.

### Evolution: LLM Wiki v2 Extensions

The LLM Wiki v2 document validates the core pattern while identifying production-scale gaps. The most significant additions are:

- **Memory lifecycle management**: Confidence scoring, supersession, forgetting (Ebbinghaus curve), and four-tier consolidation (working, episodic, semantic, procedural memory) transform the wiki from a flat knowledge store into a probabilistic model.
- **Typed knowledge graph**: Entity extraction and typed relationships ("uses," "depends on," "contradicts") layered on top of pages enable graph traversal for queries, catching structural connections that text search misses.
- **Event-driven automation**: Replacing manual operations with hooks (on-new-source, on-session-end, on-query, on-schedule) that automate bookkeeping while keeping the human in the strategic loop.
- **Self-healing lint**: Going beyond flagging issues to automatically fixing orphan pages, stale claims, and broken cross-references, with contradiction resolution proposing which claim is more likely correct.
- **The schema as the real product**: The schema document is "more important than any individual wiki page" because it encodes transferable domain operational knowledge.

These extensions represent the maturation path from a personal tool to a production knowledge management system. The LLM Wiki v2 proposes an implementation spectrum: start with the minimal viable wiki (Karpathy's original), then progressively add lifecycle, structure, automation, scale, and collaboration capabilities as needs grow.

## Open Questions

- At what exact scale does the wiki pattern start to degrade compared to vector-based RAG? Is the boundary sharp or gradual? (The v2 document suggests ~100-200 pages for index-only; the LLM Wiki vs RAG comparison page documents ~200 pages / ~500K words as the practical ceiling. Requires: empirical benchmarking to confirm whether degradation is sharp or gradual.)
- Can the wiki structure be automatically migrated to a graph database or RAG pipeline when scale demands it, preserving the relationships? (Requires: external research on graph DB migration tooling; the wiki documents the hybrid search destination but not the migration path.)
- Is there a recommended approach for merging multiple single-user wikis into a shared team wiki? (The v2 document proposes mesh sync with last-write-wins, but details are sparse. Requires: external research or implementation experience.)

## Answered Questions (moved from Open Questions)

### How does the pattern handle conflicting information from different sources?

Cross-referencing the Knowledge Evolution Pipeline page: the pipeline implements a maturity ladder (seed → growing → mature → canonical) where each promotion step requires multi-source synthesis. When two sources conflict, the scorer favors higher source counts and cross-domain references — the more corroborated claim naturally accumulates more relationships. The `--review` flag in the evolution pipeline surfaces candidates for human inspection before mature → canonical promotion, which is the explicit human checkpoint for contradiction resolution. The v2 document proposes confidence scoring and automated contradiction resolution; the wiki's current implementation handles this through promotion gates and the human review step rather than automated scoring. In practice this works by prioritizing which version of a claim has been validated by more diverse sources.

### What is the optimal index granularity — one master index, or hierarchical sub-indexes by domain?

Cross-referencing the Wiki Ingestion Pipeline and Second Brain Architecture pages: both document that this wiki uses hierarchical sub-indexes — each domain folder has its own `_index.md`, and a master `wiki/index.md` serves as the top-level navigation. This matches the PARA methodology's "Areas" structure documented in Second Brain Architecture. The ingestion pipeline automatically maintains both levels (domain index + master index) as part of the `post` chain. The practical answer from the wiki's own implementation: hierarchical sub-indexes by domain is the correct structure because the master index becomes too large for single-pass navigation beyond ~50 pages, while domain indexes remain scannable at all scales this wiki is likely to reach.

### How does the schema document (CLAUDE.md) evolve in practice?

Cross-referencing the Second Brain Architecture page and this project's own CLAUDE.md: the schema document in this wiki has evolved to include explicit page types (concept, source-synthesis, comparison, reference, deep-dive, index, lesson, pattern, decision, domain-overview, learning-path, evolution), a defined status lifecycle (raw → processing → synthesized → verified → stale), confidence levels, maturity levels (seed → growing → mature → canonical), and an ingestion mode system (auto, guided, smart). This is a concrete example of a mature schema: it started as a simple set of frontmatter fields and was progressively extended to encode evolved page types, relationship verb conventions, and quality gates. The schema co-evolution described in the LLM Wiki v2 document is clearly visible by comparing early Karpathy prompts (minimal structure) with this project's current CLAUDE.md (comprehensive operational knowledge).

### LLM Wiki Pattern and Skills Architecture are structurally parallel

Confirmed by cross-referencing Claude Code Best Practices: both patterns use markdown files as LLM-readable persistent artifacts that compound over time. Wiki pages accumulate synthesized knowledge; skill files (SKILL.md) accumulate operational knowledge about how to act. Both have an index structure (wiki has `_index.md` per domain; skills are listed in CLAUDE.md), both compound through iterative refinement, and both solve the same maintenance problem (LLM does the bookkeeping). The Claude Code Best Practices page explicitly notes: "Skills are folders with progressive disclosure" with a SKILL.md, references/, scripts/, and examples/ subdirectories — which mirrors the wiki's own page types and domain structure. This confirms the LLM Wiki Pattern is an instance of a more general "LLM-readable persistent artifact" pattern.

### Human-AI collaboration boundary is independently derived by three sources

Confirmed by cross-referencing Claude Code Best Practices and Harness Engineering: Karpathy's "LLM as librarian, human as curator" maps exactly to: (1) Claude Code Best Practices' "don't babysit, but do watch" (watch the first few steps, then let it run autonomously); (2) Harness Engineering's 5-verb workflow where the human approves the Plan step before Work begins; (3) Knowledge Evolution Pipeline's `--review` flag as the explicit human gate at the growing → mature transition. All three sources independently place the human-AI boundary at the same point: humans set direction and validate at critical transitions, AI executes all maintenance and bookkeeping. This convergence across independent sources strengthens the pattern's reliability.

## Relationships

- DERIVED FROM: src-karpathy-claude-code-10x
- DERIVED FROM: src-karpathy-llm-wiki-idea-file
- DERIVED FROM: src-llm-wiki-v2-agentmemory
- COMPARES TO: LLM Wiki vs RAG
- ENABLES: Wiki Ingestion Pipeline
- ENABLES: Memory Lifecycle Management
- ENABLES: Wiki Knowledge Graph
- ENABLES: Wiki Event-Driven Automation
- USED BY: Obsidian Knowledge Vault
- FEEDS INTO: LLM Knowledge Linting
- RELATES TO: Claude Code Context Management
- RELATES TO: NotebookLM
- RELATES TO: Skills Architecture Patterns
- RELATES TO: Agentic Search vs Vector Search
- CONTRASTS WITH: LightRAG
- USED BY: OpenFleet
- ENABLED BY: Claude Code

## Backlinks

[[src-karpathy-claude-code-10x]]
[[src-karpathy-llm-wiki-idea-file]]
[[src-llm-wiki-v2-agentmemory]]
[[LLM Wiki vs RAG]]
[[Wiki Ingestion Pipeline]]
[[Memory Lifecycle Management]]
[[Wiki Knowledge Graph]]
[[Wiki Event-Driven Automation]]
[[Obsidian Knowledge Vault]]
[[LLM Knowledge Linting]]
[[Claude Code Context Management]]
[[NotebookLM]]
[[Skills Architecture Patterns]]
[[Agentic Search vs Vector Search]]
[[LightRAG]]
[[OpenFleet]]
[[Claude Code]]
[[Automated Knowledge Validation Prevents Silent Wiki Decay]]
[[Claude Code Best Practices]]
[[Context-Aware Tool Loading]]
[[Cross-Domain Patterns]]
[[Decision: Wiki-First with LightRAG Upgrade Path]]
[[Graph-Enhanced Retrieval Bridges Wiki Navigation and Vector Search]]
[[Knowledge Evolution Pipeline]]
[[LLM-Maintained Wikis Outperform Static Documentation]]
[[Lesson: Automation Is the Bridge Between Knowledge and Action]]
[[Lesson: Knowledge Systems Is the Foundational Domain for the Entire Wiki]]
[[Lesson: Schema Is the Real Product — Not the Content]]
[[Multi-Stage Ingestion Beats Single-Pass Processing]]
[[NotebookLM Skills]]
[[NotebookLM as Grounded Research Engine Not Just Note Storage]]
[[Obsidian CLI]]
[[Obsidian Skills Ecosystem]]
[[Obsidian as Knowledge Infrastructure Not Just Note-Taking]]
[[PARA Methodology]]
[[Progressive Distillation]]
[[Research Pipeline Orchestration]]
[[Second Brain Architecture]]
[[Skill Specification Is the Key to Ecosystem Interoperability]]
[[Synthesis: Claude Code Best Practice (shanraisshan)]]
[[Synthesis: Karpathy LLM Wiki Method via Claude Code]]
[[Synthesis: Karpathy's LLM Wiki Idea File]]
[[Synthesis: LLM Wiki v2 -- Extending Karpathy's Pattern with Agentmemory Lessons]]
[[Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py]]
[[Synthesis: Obsidian + Claude Code Second Brain Setup]]
[[Synthesis: kepano/obsidian-skills]]
[[The Wiki Maintenance Problem Is Solved by LLM Automation]]
[[Zettelkasten Methodology]]
[[notebooklm-py CLI]]
