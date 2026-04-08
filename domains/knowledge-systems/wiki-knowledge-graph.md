---
title: "Wiki Knowledge Graph"
type: concept
domain: knowledge-systems
status: synthesized
confidence: medium
created: 2026-04-08
updated: 2026-04-08
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

- **Entity extraction during ingestion**: When the LLM ingests a source, it should extract structured entities -- people, projects, libraries, concepts, files, decisions -- each with a type, attributes, and relationships. "React" is a library. "Auth migration" is a project. "Sarah" is a person who owns the auth migration and has opinions about React. This goes beyond prose summarization.

- **Typed relationships carry semantic weight**: Not all connections are equal. "A uses B" differs from "A contradicts B" and "A caused B." A link that says "A relates to B" is less useful than "A caused B, confirmed by 3 sources, confidence 0.9." Typed relationships enable more precise traversal and richer query responses.

- **Graph traversal for impact analysis**: When asking "what is the impact of upgrading Redis?", the LLM starts at the Redis node, walks outward through "depends on" and "uses" edges, and finds everything downstream. This catches structural connections that keyword search and even semantic similarity search would miss.

- **Pages for reading, graph for navigation**: The knowledge graph does not replace wiki pages. Pages remain the primary interface for human consumption. The graph provides a machine-navigable overlay that supports discovery, impact analysis, and connection-finding that flat page-to-page links cannot achieve.

- **Hybrid search combines three streams**: At scale, the graph becomes one of three search modalities: BM25 for keyword matching, vector search for semantic similarity, and graph traversal for structural connections. Fused with reciprocal rank fusion, each stream catches things the others miss.

- **Scales the original pattern**: Karpathy's index.md approach works to ~100-200 pages. The knowledge graph, combined with hybrid search, extends the pattern's viability to much larger wikis by providing structured navigation paths that do not require reading the entire index.

## Deep Analysis

The Wiki Knowledge Graph addresses a structural limitation in the original LLM Wiki pattern. Karpathy's wiki uses wikilinks between pages, but these links are untyped -- they indicate a connection exists without specifying its nature. This is sufficient for small wikis where a human or LLM can read the linked pages to understand the relationship, but it becomes a bottleneck as the wiki grows and the LLM cannot read every linked page for every query.

Typed relationships solve this by encoding relationship semantics in the link itself. When the LLM sees "Redis USED BY Auth Service, DEPENDS ON Config Module, CONTRADICTED BY Cache Report v2," it can make traversal decisions without reading each linked page. This is the same insight that powers property graphs in databases like Neo4j -- the edges carry as much information as the nodes.

The entity extraction requirement changes the ingestion workflow. Rather than producing only prose summaries and page links, the LLM must also populate a structured entity registry during ingestion. This could be implemented as YAML frontmatter on entity pages (listing type, attributes, and typed relationships), as a separate entity index file, or as actual graph database entries. The choice of implementation affects complexity and queryability.

The practical question is whether the knowledge graph requires dedicated infrastructure (a graph database like Neo4j, a triple store) or can be embedded in the markdown files themselves. The LLM Wiki v2 document does not prescribe an answer. For small to medium wikis, encoding entities and typed relationships in YAML frontmatter -- which the existing wiki schema already uses for relationships -- may be sufficient. At larger scale, a proper graph database becomes necessary.

The connection to Obsidian is relevant: Obsidian's graph view already visualizes wiki pages as a graph of nodes and edges. However, it treats all links as untyped connections. A typed knowledge graph would require either custom Obsidian plugins to visualize edge types or an external graph visualization tool.

## Open Questions

- Can typed relationships be adequately represented in markdown/YAML, or does the graph eventually require a dedicated store?
- How does entity extraction quality vary across different source types (structured papers vs. rambling transcripts)?
- What is the minimum set of relationship types that provides practical value without over-engineering?
- How should entity merging work when the same real-world entity appears under different names across sources?
- Can Obsidian plugins like Dataview or Juggl provide typed graph visualization from frontmatter metadata?
- Cross-source insight: The typed relationships in the knowledge graph (uses, depends on, contradicts, supersedes) map directly to the relationship verbs used in this wiki's own pages (BUILDS ON, ENABLES, CONSTRAINS, CONTRASTS WITH). This wiki is itself a partial implementation of the Wiki Knowledge Graph pattern -- the gap is that its relationships are page-level rather than claim-level.
- Cross-source insight: The Obsidian Skills Ecosystem's three-layer architecture (format spec, content generation, programmatic control) demonstrates that knowledge graphs are not just for content -- they can model capability relationships between skills. A "skills graph" with typed edges (EXTENDS, OVERLAPS, COMPLEMENTS) could help agents decide which skills to load.

## Relationships

- DERIVED FROM: src-llm-wiki-v2-agentmemory
- EXTENDS: LLM Wiki Pattern
- BUILDS ON: Wiki Ingestion Pipeline
- ENABLES: Memory Lifecycle Management
- RELATES TO: LLM Wiki vs RAG
- RELATES TO: Obsidian Knowledge Vault
- RELATES TO: LLM Knowledge Linting
- PARALLELS: LightRAG
- FEEDS INTO: OpenFleet

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
[[Claude Code Context Management]]
[[LLM-Maintained Wikis Outperform Static Documentation]]
[[Multi-Stage Ingestion Beats Single-Pass Processing]]
[[Obsidian as Knowledge Infrastructure Not Just Note-Taking]]
[[Second Brain Architecture]]
