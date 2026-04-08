---
title: "Memory Lifecycle Management"
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
tags: [memory-lifecycle, confidence-scoring, supersession, forgetting, consolidation, knowledge-decay, ebbinghaus]
---

# Memory Lifecycle Management

## Summary

Memory Lifecycle Management is the practice of treating knowledge in an LLM-maintained wiki as having variable validity over time rather than being equally weighted forever. Proposed in the LLM Wiki v2 document as the critical missing layer in Karpathy's original pattern, it encompasses four mechanisms: confidence scoring (tracking how many sources support a fact and how recently it was confirmed), supersession (new claims explicitly replacing old ones with linked timestamps), forgetting (deprioritizing facts that have not been accessed or reinforced, following Ebbinghaus's forgetting curve), and consolidation tiers (promoting observations through working memory, episodic memory, semantic memory, and procedural memory as evidence accumulates). Together, these mechanisms transform a flat knowledge store into a probabilistic model where the system can express "I'm fairly sure about X but less sure about Y."

## Key Insights

- **Confidence scoring**: Every fact should carry a confidence score derived from source count, recency of last confirmation, and presence of contradicting evidence. A claim supported by two sources and confirmed three weeks ago at confidence 0.85 is qualitatively different from one mentioned once six months ago. Confidence decays with time and strengthens with reinforcement.

- **Supersession over annotation**: When new information contradicts existing claims, the old claim should not just receive an appended note. The new claim should explicitly supersede it with linked timestamps, preserving the old version but marking it stale. This is "version control for knowledge, not just for files."

- **Ebbinghaus forgetting curve applied to knowledge**: Facts that were important once but have not been accessed or reinforced in months should gradually deprioritize -- not deleted, but moved to a "bottom drawer." Each access or confirmation from a new source resets the decay curve. Architecture decisions decay slowly; transient bugs decay fast.

- **Four-tier consolidation pipeline**: (1) Working memory -- recent observations, not yet processed. (2) Episodic memory -- session summaries, compressed from raw observations. (3) Semantic memory -- cross-session facts, consolidated from episodes. (4) Procedural memory -- workflows and patterns, extracted from repeated semantics. Each tier is more compressed, more confident, and longer-lived.

- **Promotion is evidence-driven**: Information moves up the consolidation tiers as evidence accumulates. A single observation stays in working memory. A pattern observed across multiple sessions promotes to semantic memory. A workflow validated through repeated use becomes procedural memory. The LLM manages this promotion process.

- **Prevents the junk drawer problem**: Without lifecycle management, a wiki that grows through automated ingestion inevitably accumulates stale, contradictory, and low-value information with no mechanism for cleanup beyond manual linting. Lifecycle management provides automated self-maintenance.

## Deep Analysis

Memory Lifecycle Management addresses the fundamental tension in any growing knowledge base: comprehensiveness versus signal quality. A wiki that never forgets becomes noisy; a wiki that aggressively prunes loses context. The lifecycle approach resolves this by introducing a gradient rather than a binary -- facts do not switch from "in" to "out" but rather shift along a confidence continuum.

The four-tier consolidation model mirrors established cognitive science models of human memory (Atkinson-Shiffrin, Tulving's episodic/semantic distinction). Applying these models to LLM-maintained knowledge is a meaningful conceptual contribution. It provides a principled answer to the design question: "what level of detail should the wiki preserve?" The answer is all levels, but with different retention characteristics at each tier.

The confidence scoring mechanism has practical implications for query answering. An LLM responding from a wiki with confidence metadata can qualify its answers -- "Based on two sources from last month (confidence 0.85), Project X uses Redis for caching" versus "Based on a single mention from six months ago (confidence 0.4), the team was considering PostgreSQL for this." This transforms the wiki from an assertion engine into a nuanced knowledge model.

The main implementation challenge is deciding what metadata to track and where to store it. YAML frontmatter on each wiki page is one approach (source count, last confirmed date, confidence score as page-level metadata). Inline annotations within page content would provide claim-level granularity but add complexity. The LLM Wiki v2 document does not prescribe a specific approach, leaving this as an implementation detail.

The connection to Karpathy's original lint operation is direct: lint can serve as the mechanism that triggers confidence decay, identifies candidates for tier promotion, and flags stale content for supersession review. This makes lint not just a quality check but the engine that drives the entire lifecycle.

## Open Questions

- What metadata schema best supports confidence scoring -- page-level YAML, inline annotations, or a separate metadata store?
- How frequently should the consolidation pipeline run, and what is the computational cost per pass?
- How should confidence thresholds be calibrated -- what confidence score triggers "stale" flagging vs. active deprioritization?
- Can the forgetting curve parameters be tuned per domain (e.g., slower decay for legal facts, faster for technology trends)?
- How does lifecycle management interact with the Git version history -- should superseded content be preserved in Git history rather than in the wiki itself?
- Cross-source insight: The four-tier consolidation pipeline (working, episodic, semantic, procedural memory) maps to the skill complexity spectrum identified in Skills Architecture Patterns. Procedural memory ("workflows and patterns extracted from repeated semantics") is essentially what skills encode. Could the consolidation pipeline automatically generate or refine skills from repeated wiki query patterns -- promoting semantic knowledge to procedural skills?
- Cross-source insight: Claude Code Context Management's "lost in the middle" problem directly impacts how memory lifecycle management should structure its output. High-confidence, frequently-accessed knowledge should be placed at the beginning or end of relevant pages, while low-confidence or less-accessed content can occupy the middle. Memory lifecycle metadata could drive page layout optimization for LLM attention patterns.

## Relationships

- DERIVED FROM: src-llm-wiki-v2-agentmemory
- EXTENDS: LLM Wiki Pattern
- ENABLES: LLM Knowledge Linting
- RELATES TO: Wiki Ingestion Pipeline
- RELATES TO: LLM Wiki vs RAG
- RELATES TO: Claude Code Context Management
- RELATES TO: Wiki Knowledge Graph
- RELATES TO: Wiki Event-Driven Automation

## Backlinks

[[src-llm-wiki-v2-agentmemory]]
[[LLM Wiki Pattern]]
[[LLM Knowledge Linting]]
[[Wiki Ingestion Pipeline]]
[[LLM Wiki vs RAG]]
[[Claude Code Context Management]]
[[Wiki Knowledge Graph]]
[[Wiki Event-Driven Automation]]
[[Agentic Search vs Vector Search]]
[[LLM-Maintained Wikis Outperform Static Documentation]]
[[Multi-Stage Ingestion Beats Single-Pass Processing]]
[[Second Brain Architecture]]
[[Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py]]
