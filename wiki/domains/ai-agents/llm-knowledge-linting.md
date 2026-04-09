---
title: "LLM Knowledge Linting"
type: concept
domain: ai-agents
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
tags: [linting, knowledge-quality, health-check, llm-agent, wiki-maintenance, data-integrity, self-healing, contradiction-resolution]
---

# LLM Knowledge Linting

## Summary

LLM Knowledge Linting is the practice of running periodic LLM-driven health checks over a wiki knowledge base to find and fix quality issues. As described by Karpathy and elaborated in the transcript, this involves using the LLM to identify inconsistent data across pages, impute missing data by conducting web searches, discover interesting connections between existing pages, and suggest new article candidates to fill gaps in the knowledge graph. This linting process is the maintenance layer that keeps the wiki scalable, accurate, and well-structured over time, analogous to code linting but applied to a knowledge base.

## Key Insights

- **Inconsistency detection**: The LLM scans across wiki pages to find contradictory information — facts stated differently on different pages, outdated claims, or broken relationships.
- **Missing data imputation**: When the LLM identifies gaps in a wiki page (e.g., a concept mentioned but never explained, or a relationship referenced but not fleshed out), it can conduct web searches to fill in the missing information.
- **Connection discovery**: The linting pass looks for implicit connections between pages that were not established during initial ingestion — concepts that should be linked but are not.
- **New article suggestions**: The LLM may recommend new sources to ingest based on gaps it identifies, telling the user "I don't fully understand this — can you give me more info or grab some more articles?"
- **Flexible scheduling**: Linting can run daily, weekly, or on-demand depending on how actively the wiki is being updated. The transcript does not prescribe a specific cadence.
- **Scalability maintenance**: As the wiki grows, linting ensures the structure remains navigable and the index stays accurate. Without it, organic growth could lead to orphaned pages, stale links, and redundant entries.
- **Primary source details (Karpathy idea file)**: Karpathy defines lint as looking for: "contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search." He adds: "The LLM is good at suggesting new questions to investigate and new sources to look for."
- **Self-healing lint (from v2)**: The LLM Wiki v2 document argues lint should go beyond suggesting fixes to automatically implementing them — orphan pages get linked or flagged, stale claims get marked, broken cross-references get repaired. The wiki should "tend toward health on its own."
- **Contradiction resolution (from v2)**: Beyond flagging contradictions, the LLM should propose which claim is more likely correct based on source recency, source authority, and supporting observation count. The human can override, but the default behavior should usually be right.
- **Quality scoring (from v2)**: Every piece of LLM-generated content should receive a quality score assessing structure, citation quality, and consistency with the rest of the wiki. Content below a threshold gets flagged for review or automatically rewritten.

## Deep Analysis

Knowledge linting addresses the long-term maintenance problem that plagues any knowledge management system. Wikis — whether human-maintained or LLM-generated — tend to accumulate inconsistencies over time as new information is added without reviewing how it interacts with existing content. In a traditional wiki, this requires dedicated human editors. In the LLM Wiki pattern, the LLM itself serves as the editor.

The concept is directly analogous to code linting. Just as ESLint scans JavaScript for style violations and potential bugs, an LLM linting pass scans the wiki for knowledge violations: contradictions, gaps, stale data, and structural problems. The difference is that knowledge linting requires semantic understanding rather than syntactic pattern matching, which is why it needs an LLM rather than a rule-based tool.

The missing data imputation capability is particularly interesting because it makes the wiki self-improving. When the LLM identifies a gap and fills it via web search, the wiki grows without the user manually providing new sources. This creates a feedback loop: ingestion produces pages, linting identifies gaps, gap-filling produces more content, and the next linting pass checks the new content.

The transcript treats linting as a relatively lightweight concept — Karpathy mentions it briefly and the presenter spends only a few sentences on it. However, it may be the most critical component for long-term wiki health. Without linting, a wiki that grows through automated ingestion will inevitably accumulate quality debt, much like a codebase without CI/CD accumulates technical debt.

The confidence level for this page has been upgraded from medium to high now that Karpathy's primary source and the LLM Wiki v2 document both provide substantial detail on linting scope and implementation.

### Self-Healing and Lifecycle Integration (from v2)

The LLM Wiki v2 document significantly expands the role of linting from a passive health check to an active self-healing mechanism. In this expanded model, lint is the engine that drives the entire memory lifecycle: it triggers confidence decay for unconfirmed facts, identifies candidates for promotion between consolidation tiers (working to episodic to semantic to procedural memory), flags stale content for supersession review, and automatically repairs structural issues like broken cross-references and orphan pages.

This transforms lint from a periodic maintenance task into a continuous quality assurance system. The key architectural implication is that lint becomes tightly coupled with confidence scoring and memory lifecycle management — it is both the sensor that detects knowledge decay and the actuator that triggers remediation.

## Open Questions

- What does a linting prompt look like in practice — does it scan the full wiki or sample pages? (Requires: implementation detail not documented in existing wiki pages; the architecture is described but no concrete prompt template for linting has been synthesized)

## Answered Open Questions

### How does linting handle the cost of reading the entire wiki for each health check pass?

Cross-referencing `Context-Aware Tool Loading` and `Wiki Knowledge Graph`: the context cost of reading the full wiki for each lint pass is a real constraint. The `Context-Aware Tool Loading` pattern documents that "external knowledge bases larger than what a context window can hold" require deferred/selective loading rather than full pre-load. The `LLM Wiki vs RAG` page establishes the wiki's scale ceiling at ~200 pages / ~500K words for index-only navigation. A full lint pass that reads every page would exceed a single context window beyond ~50-100 pages. The architectural solution from existing wiki knowledge: lint should use the same index-navigation approach as the LLM Wiki Pattern — read the manifest/index first, identify candidate pages (via structural signals like relationship count, last-updated date, or stale flag), then read only those pages in targeted passes. The `Wiki Knowledge Graph` page's answered question on incremental processing is relevant: LightRAG supports "incremental updates without full reconstruction," confirming the field-wide recognition that full-corpus processing is impractical at scale and incremental passes are the standard approach.

### Can linting be scoped to only check pages modified since the last lint, similar to incremental builds?

Cross-referencing `Knowledge Evolution Pipeline` and `Agent Orchestration Patterns`: yes — incremental scoping is both architecturally feasible and the correct default approach. The `Knowledge Evolution Pipeline` documents a deterministic scoring system using signals including "page age (days since created)" and existing maturity level — this scoring infrastructure already identifies which pages warrant attention. The same signals can scope linting: pages modified since the last lint run, pages with recently changed relationship targets, or pages whose source documents have been updated. The `Agent Orchestration Patterns` page documents OpenFleet's parallel: "incremental updates without full reconstruction" is cited for LightRAG's graph updates, and the 12-step orchestrator cycle "evaluates only changed tasks, not the full task board, on each cycle." The practical implementation for this wiki: the watcher daemon already tracks file modification times (via `tools.watcher`); a lint-on-change trigger would naturally scope to modified pages. The `pipeline post` chain runs validate and lint after every ingestion — this is already a form of lint-on-ingest for newly ingested pages.

### How does the LLM decide whether to auto-fix an inconsistency or flag it for human review?

Cross-referencing `Knowledge Evolution Pipeline` and `Agent Orchestration Patterns`: the decision framework for auto-fix vs. human review is documented across two sources. The `Knowledge Evolution Pipeline` page establishes the human-in-the-loop gate at the `growing → mature` transition: "the `--review` flag surfaces seed pages that have accumulated enough relationships to warrant human review before promotion. This is the human-in-the-loop checkpoint in an otherwise automated pipeline, placed at the transition between growing and mature — the point where LLM-generated content may benefit from curator validation." Applied to linting: structural fixes (broken wikilinks, missing frontmatter fields, orphaned pages, formatting violations) can be auto-fixed because they have unambiguous correct states. Semantic inconsistencies (contradictions between page claims, stale facts, divergent confidence assessments) require human review because the correct resolution is not deterministic. The `Agent Orchestration Patterns` page's deterministic brain pattern supports the same split: "every control decision made by a deterministic rule rather than an LLM call saves inference cost" — structural lint fixes are rule-based and should be auto-applied; semantic fixes require LLM judgment and the human review gate.

### Could linting be combined with the ingestion pipeline (lint-on-ingest) to catch issues earlier?

Cross-referencing `Wiki Knowledge Graph` and `Knowledge Evolution Pipeline`: this is already partially implemented. The `pipeline post` command runs validate + lint after every ingestion as step 5 of the 6-step post-chain. This is lint-on-ingest for the pages created in that ingestion run. The remaining gap is cross-page linting: a single ingestion creates new pages that may contradict or under-link to existing pages, but the post-chain lint only checks structural validity (schema compliance, wikilinks), not semantic consistency with the rest of the wiki. Full lint-on-ingest — scanning all existing pages for interactions with newly ingested content — would require the incremental approach described above: identify pages that reference the same concepts as the new pages, then run a targeted consistency check on that subset. The `Knowledge Evolution Pipeline`'s "loop compounds" insight is relevant: every ingestion changes the relationship landscape, and a lightweight incremental lint pass after each ingestion would catch cross-page issues before they accumulate into the kind of quality debt that requires a full-wiki lint pass.

## Relationships

- DERIVED FROM: src-karpathy-claude-code-10x
- DERIVED FROM: src-karpathy-llm-wiki-idea-file
- DERIVED FROM: src-llm-wiki-v2-agentmemory
- BUILDS ON: LLM Wiki Pattern
- BUILDS ON: Wiki Ingestion Pipeline
- ENABLES: Memory Lifecycle Management
- RELATES TO: Obsidian Knowledge Vault
- RELATES TO: Wiki Event-Driven Automation
- CONSTRAINED BY: Claude Code Context Management
- RELATES TO: Wiki Knowledge Graph
- ENABLED BY: Claude Code Scheduling

## Backlinks

[[src-karpathy-claude-code-10x]]
[[src-karpathy-llm-wiki-idea-file]]
[[src-llm-wiki-v2-agentmemory]]
[[LLM Wiki Pattern]]
[[Wiki Ingestion Pipeline]]
[[Memory Lifecycle Management]]
[[Obsidian Knowledge Vault]]
[[Wiki Event-Driven Automation]]
[[Claude Code Context Management]]
[[Wiki Knowledge Graph]]
[[Claude Code Scheduling]]
[[Automated Knowledge Validation Prevents Silent Wiki Decay]]
[[LLM-Maintained Wikis Outperform Static Documentation]]
[[Multi-Stage Ingestion Beats Single-Pass Processing]]
[[OpenClaw]]
[[Synthesis: Karpathy LLM Wiki Method via Claude Code]]
[[Synthesis: Karpathy's LLM Wiki Idea File]]
[[Synthesis: LLM Wiki v2 -- Extending Karpathy's Pattern with Agentmemory Lessons]]
[[The Wiki Maintenance Problem Is Solved by LLM Automation]]
