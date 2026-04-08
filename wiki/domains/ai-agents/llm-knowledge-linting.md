---
title: "LLM Knowledge Linting"
type: concept
domain: ai-agents
status: synthesized
confidence: medium
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-karpathy-claude-code-10x
    type: youtube-transcript
    file: raw/transcripts/karpathy-claude-code-10x.txt
    title: "Andrej Karpathy Just 10x'd Everyone's Claude Code"
    ingested: 2026-04-08
tags: [linting, knowledge-quality, health-check, llm-agent, wiki-maintenance, data-integrity]
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

## Deep Analysis

Knowledge linting addresses the long-term maintenance problem that plagues any knowledge management system. Wikis — whether human-maintained or LLM-generated — tend to accumulate inconsistencies over time as new information is added without reviewing how it interacts with existing content. In a traditional wiki, this requires dedicated human editors. In the LLM Wiki pattern, the LLM itself serves as the editor.

The concept is directly analogous to code linting. Just as ESLint scans JavaScript for style violations and potential bugs, an LLM linting pass scans the wiki for knowledge violations: contradictions, gaps, stale data, and structural problems. The difference is that knowledge linting requires semantic understanding rather than syntactic pattern matching, which is why it needs an LLM rather than a rule-based tool.

The missing data imputation capability is particularly interesting because it makes the wiki self-improving. When the LLM identifies a gap and fills it via web search, the wiki grows without the user manually providing new sources. This creates a feedback loop: ingestion produces pages, linting identifies gaps, gap-filling produces more content, and the next linting pass checks the new content.

The transcript treats linting as a relatively lightweight concept — Karpathy mentions it briefly and the presenter spends only a few sentences on it. However, it may be the most critical component for long-term wiki health. Without linting, a wiki that grows through automated ingestion will inevitably accumulate quality debt, much like a codebase without CI/CD accumulates technical debt.

The confidence level for this page is set to medium because the transcript provides limited detail on linting implementation — it describes what linting does but not how it is structured as a prompt or workflow.

## Open Questions

- What does a linting prompt look like in practice — does it scan the full wiki or sample pages?
- How does linting handle the cost of reading the entire wiki for each health check pass?
- Can linting be scoped to only check pages modified since the last lint, similar to incremental builds?
- How does the LLM decide whether to auto-fix an inconsistency or flag it for human review?
- Could linting be combined with the ingestion pipeline (lint-on-ingest) to catch issues earlier?

## Relationships

- DERIVED FROM: src-karpathy-claude-code-10x
- BUILDS ON: LLM Wiki Pattern
- BUILDS ON: Wiki Ingestion Pipeline
- RELATES TO: Obsidian Knowledge Vault

## Backlinks

[[src-karpathy-claude-code-10x]]
[[LLM Wiki Pattern]]
[[Wiki Ingestion Pipeline]]
[[Obsidian Knowledge Vault]]
[[Synthesis: Karpathy LLM Wiki Method via Claude Code]]
