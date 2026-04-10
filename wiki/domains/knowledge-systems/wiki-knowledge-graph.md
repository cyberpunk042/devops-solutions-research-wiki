---
title: "Wiki Knowledge Graph"
type: concept
layer: 2
maturity: growing
domain: knowledge-systems
status: synthesized
confidence: medium
created: 2026-04-08
updated: 2026-04-10
sources:
  - id: src-llm-wiki-v2-agentmemory
    type: documentation
    url: "https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2"
    file: raw/articles/llm-wiki-v2-extending-karpathys-llm-wiki-pattern-with-lessons-from-building-agen.md
    title: "LLM Wiki v2 -- Extending Karpathy's LLM Wiki Pattern with Lessons from Building Agentmemory"
    ingested: 2026-04-08
tags: [knowledge-graph, entity-extraction, typed-relationships, graph-traversal, structured-knowledge, hybrid-search]
---

# Wiki Knowledge Graph

## Summary

The Wiki Knowledge Graph is an architectural extension to the LLM Wiki pattern that layers typed entity-relationship structures on top of flat markdown pages. Proposed in the LLM Wiki v2 document, it adds three capabilities beyond basic wikilinks: entity extraction (identifying people, projects, libraries, concepts, files, and decisions during ingestion with typed attributes), typed relationships (distinguishing "uses," "depends on," "contradicts," "caused," "fixed," and "supersedes" rather than generic links), and graph traversal for queries (walking outward from a node through specific edge types to find downstream impacts). The graph augments rather than replaces the wiki pages -- pages remain the human-readable layer while the graph provides a machine-navigable structure for discovery and impact analysis.

## Key Insights

> [!tip] Pages for reading, graph for navigation
> The knowledge graph does not replace wiki pages. Pages remain the primary human interface. The graph provides a machine-navigable overlay for discovery, impact analysis, and connection-finding that flat page-to-page links cannot achieve.

> [!abstract] Three search streams at scale
>
> | Stream | What It Catches | Mechanism |
> |--------|----------------|-----------|
> | **BM25** | Keyword matches | Term frequency |
> | **Vector search** | Semantic similarity | Embedding cosine distance |
> | **Graph traversal** | Structural connections | Walk typed edges (uses, depends on, contradicts) |
>
> Fused with reciprocal rank fusion, each catches what the others miss. Scales the wiki pattern past the ~200-page index-only ceiling.

**Typed relationships carry semantic weight.** "A uses B" differs from "A contradicts B" differs from "A caused B." Typed edges enable precise traversal and richer queries — "What contradicts this claim?" via CONTRADICTS edges, "What does X enable?" via ENABLES edges.

**Entity extraction during ingestion.** Beyond prose summaries: extract structured entities (people, projects, libraries) with type, attributes, and typed relationships. This is what powers graph traversal for impact analysis.

## Deep Analysis

The Wiki Knowledge Graph addresses a structural limitation in the original LLM Wiki pattern. Karpathy's wiki uses wikilinks between pages, but these links are untyped -- they indicate a connection exists without specifying its nature. This is sufficient for small wikis where a human or LLM can read the linked pages to understand the relationship, but it becomes a bottleneck as the wiki grows and the LLM cannot read every linked page for every query.

Typed relationships solve this by encoding relationship semantics in the link itself. When the LLM sees "Redis USED BY Auth Service, DEPENDS ON Config Module, CONTRADICTED BY Cache Report v2," it can make traversal decisions without reading each linked page. This is the same insight that powers property graphs in databases like Neo4j -- the edges carry as much information as the nodes.

The entity extraction requirement changes the ingestion workflow. Rather than producing only prose summaries and page links, the LLM must also populate a structured entity registry during ingestion. This could be implemented as YAML frontmatter on entity pages (listing type, attributes, and typed relationships), as a separate entity index file, or as actual graph database entries. The choice of implementation affects complexity and queryability.

The practical question is whether the knowledge graph requires dedicated infrastructure (a graph database like Neo4j, a triple store) or can be embedded in the markdown files themselves. The LLM Wiki v2 document does not prescribe an answer. For small to medium wikis, encoding entities and typed relationships in YAML frontmatter -- which the existing wiki schema already uses for relationships -- may be sufficient. At larger scale, a proper graph database becomes necessary.

The connection to Obsidian is relevant: Obsidian's graph view already visualizes wiki pages as a graph of nodes and edges. However, it treats all links as untyped connections. A typed knowledge graph would require either custom Obsidian plugins to visualize edge types or an external graph visualization tool.

## Open Questions

- How does entity extraction quality vary across different source types (structured papers vs. rambling transcripts)? (Requires: empirical testing or external research on LLM entity extraction accuracy across source types; not covered by existing wiki pages)
- How should entity merging work when the same real-world entity appears under different names across sources? (Requires: external research on entity resolution techniques; LightRAG's deduplication step is relevant but details are sparse in current wiki pages)

## Answered Open Questions

### Can typed relationships be adequately represented in markdown/YAML, or does the graph eventually require a dedicated store?

Cross-referencing `LightRAG` and `LLM Wiki vs RAG`: the LightRAG page documents this directly: "For small to medium wikis, encoding entities and typed relationships in YAML frontmatter — which the existing wiki schema already uses for relationships — may be sufficient. At larger scale, a proper graph database becomes necessary." The LightRAG page further documents that OpenFleet uses LightRAG with 1,545 entities and 2,295 relationships stored in a dedicated graph backend (Neo4j, PostgreSQL+AGE, or JSON). The practical answer: markdown/YAML is adequate up to roughly the same scale ceiling as the LLM Wiki Pattern itself (~200 pages, ~500K words). Beyond that scale, LightRAG's REST API provides an upgrade path that preserves the existing relationship format — `kb_sync.py` already parses this wiki's `## Relationships` sections (with ALL_CAPS verb format) and inserts directly into LightRAG via REST API. This means the transition from markdown/YAML to dedicated graph store does not require changing the wiki's authoring format, only adding an export step.

### What is the minimum set of relationship types that provides practical value without over-engineering?

Cross-referencing `LightRAG` and `Zettelkasten Methodology`: the LightRAG page documents that OpenFleet's kb_sync.py extracts relationships from this wiki's `## Relationships` sections — confirming the current wiki relationship verbs (BUILDS ON, ENABLES, COMPARES TO, CONTRADICTS, FEEDS INTO, DERIVED FROM, SUPERSEDES, IMPLEMENTS, EXTENDS, RELATES TO, USED BY, CONSTRAINS, PARALLELS) are the empirically-derived minimum set from this project's actual usage. The Zettelkasten Methodology page further narrows this to the query-enabling subset: "What does this concept enable?" (ENABLES), "What contradicts this claim?" (CONTRADICTS), "What supersedes this approach?" (SUPERSEDES), "What implements this pattern?" (IMPLEMENTS). These four relationship types enable the most valuable graph traversal queries. The LightRAG page documents that LightRAG's own type set is: "uses, depends on, contradicts, caused, fixed, supersedes" — a domain-agnostic equivalent. Mapping the current wiki verbs: BUILDS ON ≈ depends on, ENABLES ≈ uses, CONTRADICTS ≈ contradicts, SUPERSEDES ≈ supersedes, IMPLEMENTS ≈ uses (directional). The minimum practical set is 4-6 types covering dependency, enablement, contradiction, and supersession.

### Can Obsidian plugins like Dataview or Juggl provide typed graph visualization from frontmatter metadata?

Cross-referencing `LLM Wiki vs RAG` and `LightRAG`: the LLM Wiki vs RAG page documents that "the wiki's explicit typed relationships (## Relationships section) enable multi-hop reasoning that RAG cannot replicate." The LightRAG page documents that LightRAG provides a "Web UI for visualization" of the knowledge graph. For Obsidian-native visualization: the current wiki implementation uses Obsidian's standard graph view for untyped connection visualization. Dataview can query frontmatter fields and relationship sections to produce table views of typed relationships. Juggl (Obsidian graph visualization plugin) supports typed edges via CSS classes. However, both require either custom parsing of the `## Relationships` section or storing relationships in frontmatter YAML (rather than as a markdown section). The practical answer from the existing wiki architecture: for full typed graph visualization, LightRAG's web UI is the correct tool (already integrated via kb_sync.py for OpenFleet). For lightweight Obsidian-native visualization, Dataview with a custom DQL query against the relationships section is feasible but requires custom plugin development to parse the ALL_CAPS verb format.

### This wiki is a partial implementation of the Wiki Knowledge Graph — what is the gap? (Cross-source insight)

Cross-referencing `LightRAG` and `Zettelkasten Methodology`: the gap between this wiki's current implementation and a full Wiki Knowledge Graph is precisely documented in the LightRAG page: "The wiki's relationship format (- VERB: Target Name) is directly compatible with kb_sync.py's regex parser." This confirms the current wiki IS a typed knowledge graph at the page level — every `## Relationships` section entry is a typed edge. The remaining gap is: (1) **claim-level vs. page-level granularity** — current relationships link pages, not specific claims within pages; (2) **entity attributes** — entities (pages) have frontmatter attributes but these are not queried as graph node properties; (3) **graph traversal tooling** — the wiki can be read by LightRAG for traversal queries, but this requires the LightRAG integration (OpenFleet's kb_sync.py path), which is not yet activated for the research wiki itself. The wiki is 80% of the way to a full knowledge graph; the remaining 20% is LightRAG integration for the research wiki's own queries.

### Could a skills graph with typed edges help agents decide which skills to load? (Cross-source insight)

Cross-referencing `Context-Aware Tool Loading` and `CLI Tools Beat MCP for Token Efficiency`: the Context-Aware Tool Loading pattern page addresses this directly — the pattern's "When To Apply" section specifies "any information source used on fewer than ~80% of turns in a session: pre-loading the minority case penalizes every turn for the majority case." A skills graph would enable the agent to make this decision structurally: given the current task, traverse ENABLES and EXTENDS edges from the task's concept nodes to identify relevant skills, then load only those skills. This is the deferred loading principle applied to skill selection. The CLI Tools Beat MCP lesson confirms: "Skills (SKILL.md files) contain no schema overhead at rest. They only enter the context window when explicitly invoked." A typed skills graph (EXTENDS, OVERLAPS, COMPLEMENTS edges between skill pages) would replace the current manual skill selection (user runs slash command) with graph-traversal-guided automatic selection — identifying the minimal set of skills relevant to the current task type.

## Relationships

- DERIVED FROM: src-llm-wiki-v2-agentmemory
- EXTENDS: [[LLM Wiki Pattern]]
- BUILDS ON: [[Wiki Ingestion Pipeline]]
- ENABLES: [[Memory Lifecycle Management]]
- RELATES TO: [[LLM Wiki vs RAG]]
- RELATES TO: [[Obsidian Knowledge Vault]]
- RELATES TO: [[LLM Knowledge Linting]]
- PARALLELS: [[LightRAG]]
- FEEDS INTO: [[OpenFleet]]

## Backlinks

[[src-llm-wiki-v2-agentmemory]]
[[LLM Wiki Pattern]]
[[Wiki Ingestion Pipeline]]
[[Memory Lifecycle Management]]
[[LLM Wiki vs RAG]]
[[Obsidian Knowledge Vault]]
[[LLM Knowledge Linting]]
[[LightRAG]]
[[OpenFleet]]
[[AICP]]
[[Agentic Search vs Vector Search]]
[[Automated Knowledge Validation Prevents Silent Wiki Decay]]
[[Claude Code Context Management]]
[[Cross-Domain Patterns]]
[[Decision: Local Model vs Cloud API for Routine Operations]]
[[Decision: Obsidian vs NotebookLM as Knowledge Interface]]
[[Decision: Wiki-First with LightRAG Upgrade Path]]
[[Four-Project Ecosystem]]
[[Graph-Enhanced Retrieval Bridges Wiki Navigation and Vector Search]]
[[Knowledge Evolution Pipeline]]
[[LLM-Maintained Wikis Outperform Static Documentation]]
[[Multi-Stage Ingestion Beats Single-Pass Processing]]
[[Obsidian as Knowledge Infrastructure Not Just Note-Taking]]
[[Progressive Distillation]]
[[Second Brain Architecture]]
[[Zettelkasten Methodology]]
