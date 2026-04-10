---
title: "Memory Lifecycle Management"
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
tags: [memory-lifecycle, confidence-scoring, supersession, forgetting, consolidation, knowledge-decay, ebbinghaus]
---

# Memory Lifecycle Management

## Summary

Memory Lifecycle Management is the practice of treating knowledge in an LLM-maintained wiki as having variable validity over time rather than being equally weighted forever. Proposed in the LLM Wiki v2 document as the critical missing layer in Karpathy's original pattern, it encompasses four mechanisms: confidence scoring (tracking how many sources support a fact and how recently it was confirmed), supersession (new claims explicitly replacing old ones with linked timestamps), forgetting (deprioritizing facts that have not been accessed or reinforced, following Ebbinghaus's forgetting curve), and consolidation tiers (promoting observations through working memory, episodic memory, semantic memory, and procedural memory as evidence accumulates). Together, these mechanisms transform a flat knowledge store into a probabilistic model where the system can express "I'm fairly sure about X but less sure about Y."

## Key Insights

> [!info] Four-tier consolidation pipeline
>
> | Tier | What It Holds | Characteristics |
> |------|-------------|----------------|
> | **Working** | Recent observations, not yet processed | Short-lived, high volume |
> | **Episodic** | Session summaries, compressed from raw | Session-scoped, compressed |
> | **Semantic** | Cross-session facts, consolidated from episodes | Durable, multi-source validated |
> | **Procedural** | Workflows and patterns, extracted from repeated semantics | Longest-lived, highest confidence |
>
> Each tier is more compressed, more confident, and longer-lived. Promotion is evidence-driven: single observation → pattern across sessions → validated workflow.

> [!warning] Supersession over annotation
> When new information contradicts existing claims, the new claim explicitly supersedes the old with linked timestamps — preserving the old version but marking it stale. "Version control for knowledge, not just for files."

**Confidence scoring.** Every fact carries a confidence derived from source count, recency, and contradicting evidence. A claim at 0.85 from two recent sources is qualitatively different from 0.4 from one mention six months ago. Confidence decays with time, strengthens with reinforcement (Ebbinghaus curve).

**Prevents the junk drawer problem.** Without lifecycle management, automated ingestion accumulates stale, contradictory, low-value content with no cleanup mechanism. Lifecycle management provides automated self-maintenance.

## Deep Analysis

Memory Lifecycle Management addresses the fundamental tension in any growing knowledge base: comprehensiveness versus signal quality. A wiki that never forgets becomes noisy; a wiki that aggressively prunes loses context. The lifecycle approach resolves this by introducing a gradient rather than a binary -- facts do not switch from "in" to "out" but rather shift along a confidence continuum.

The four-tier consolidation model mirrors established cognitive science models of human memory (Atkinson-Shiffrin, Tulving's episodic/semantic distinction). Applying these models to LLM-maintained knowledge is a meaningful conceptual contribution. It provides a principled answer to the design question: "what level of detail should the wiki preserve?" The answer is all levels, but with different retention characteristics at each tier.

The confidence scoring mechanism has practical implications for query answering. An LLM responding from a wiki with confidence metadata can qualify its answers -- "Based on two sources from last month (confidence 0.85), Project X uses Redis for caching" versus "Based on a single mention from six months ago (confidence 0.4), the team was considering PostgreSQL for this." This transforms the wiki from an assertion engine into a nuanced knowledge model.

The main implementation challenge is deciding what metadata to track and where to store it. YAML frontmatter on each wiki page is one approach (source count, last confirmed date, confidence score as page-level metadata). Inline annotations within page content would provide claim-level granularity but add complexity. The LLM Wiki v2 document does not prescribe a specific approach, leaving this as an implementation detail.

The connection to Karpathy's original lint operation is direct: lint can serve as the mechanism that triggers confidence decay, identifies candidates for tier promotion, and flags stale content for supersession review. This makes lint not just a quality check but the engine that drives the entire lifecycle.

## Open Questions

- How frequently should the consolidation pipeline run, and what is the computational cost per pass? (Requires: empirical benchmarking against real wiki state; cost per pass depends on page count and LLM backend; no existing wiki page covers this)
- How should confidence thresholds be calibrated — what confidence score triggers "stale" flagging vs. active deprioritization? (Requires: empirical calibration from real-world usage; no existing wiki page prescribes specific threshold values)

## Answered Open Questions

### What metadata schema best supports confidence scoring -- page-level YAML, inline annotations, or a separate metadata store?

Cross-referencing `Second Brain Architecture` and `Knowledge Evolution Pipeline`: the Second Brain Architecture page documents that this wiki already uses page-level YAML frontmatter with `status`, `confidence`, and `maturity` fields — a practical subset of the full confidence scoring schema. The Knowledge Evolution Pipeline's scoring table documents the six deterministic signals used for evolution scoring (relationship count, cross-domain references, source count, page age, type weight, current maturity) — these are effectively a confidence proxy computed from page metadata rather than stored explicitly. The schema answer from existing implementation: page-level YAML frontmatter (`confidence: low|medium|high|authoritative`, `maturity: seed|growing|mature|canonical`, `updated: YYYY-MM-DD`) provides the structural foundation. The gap is: (1) source count is implicit (count `sources:` entries) rather than a scored field, (2) there is no explicit decay timestamp, (3) there is no per-claim confidence, only per-page. For the current wiki scale, page-level YAML is the right choice — inline claim-level annotations add complexity that only becomes necessary at canonical-level pages where specific claims need individual provenance tracking.

### Can the forgetting curve parameters be tuned per domain (e.g., slower decay for legal facts, faster for technology trends)?

Cross-referencing `Knowledge Evolution Pipeline`: the evolution pipeline's scoring already implements a primitive form of domain-aware decay through the "type weight" signal — `pattern` and `lesson` types score higher than raw concepts because they represent distilled cross-domain knowledge that decays slower. The scoring table documents this explicitly: "pattern and lesson types score higher because they represent distilled cross-domain knowledge." The practical answer: the `type` frontmatter field (concept, pattern, lesson, decision) is the current mechanism for domain-aware decay tuning. A `concept` page in the `automation` domain decays faster than a `lesson` page in any domain, because lessons encode validated patterns while concepts encode current observations. Extending this to domain-level tuning would require adding a `decay_rate: fast|normal|slow` field to the schema, defaulting by domain (e.g., `tools-and-platforms` → fast, `knowledge-systems` → slow). This is a schema extension, not an architectural change.

### How does lifecycle management interact with Git version history -- should superseded content be preserved in Git history rather than in the wiki itself?

Cross-referencing `Second Brain Architecture` and `Zettelkasten Methodology`: the Second Brain Architecture page maps `status: stale` to PARA's "Archives" bucket — stale pages are archived, not deleted. The Zettelkasten Methodology page notes: "Zettelkasten traditionally preserves contradictions and links them" rather than deleting them. These two sources converge on the same answer: superseded content should remain in the wiki as `status: stale` pages with a `SUPERSEDED BY: <new page>` relationship, rather than being deleted and relying solely on Git history for preservation. Git history provides file-level recovery; in-wiki preservation provides semantic context (the superseded claim, its sources, and the reason for supersession are visible to the LLM during ingestion of related topics). The LLM Wiki v2 source explicitly calls this "version control for knowledge, not just for files" — the wiki provides knowledge-level versioning while Git provides file-level versioning. Both are needed; they serve different audiences (LLM reading the wiki vs. human recovering lost content).

### Could the consolidation pipeline automatically generate skills from wiki query patterns? (Cross-source insight)

Cross-referencing `Knowledge Evolution Pipeline` and `Second Brain Architecture`: the Knowledge Evolution Pipeline's maturity ladder already implements the conceptual equivalent: semantic knowledge (concepts in `wiki/domains/`) promotes to procedural memory (patterns in `wiki/patterns/` and lessons in `wiki/lessons/`) through the evolution pipeline. The `--review` flag surfaces pages ready for this promotion. The Second Brain Architecture page maps this directly: "Evolution layers: raw → seed → growing → mature → canonical" corresponds to the four-tier consolidation model. The gap between the current implementation and auto-generating skills is that wiki `pattern` and `lesson` pages describe procedural knowledge in prose, while skills (SKILL.md files) are actionable prompts. The architectural bridge exists in principle: a `pattern` page that reaches `canonical` maturity could be passed to an evolution step that generates a corresponding SKILL.md file. This is a pipeline extension (add a `--target skill` flag to `pipeline evolve`) rather than a conceptual redesign.

### How should memory lifecycle management structure output given the "lost in the middle" LLM attention problem? (Cross-source insight)

Cross-referencing `Claude Code Context Management`: that page documents the lost-in-the-middle phenomenon explicitly: "models attend most strongly to the beginning and end of the context window, with reduced attention to content in the middle." The practical implication for memory lifecycle management page layout: high-confidence facts and recently-confirmed claims should be placed in `## Summary` and `## Key Insights` sections (which occupy the beginning of the page, receiving full attention), while low-confidence or less-accessed content belongs in `## Deep Analysis` or subsections (which may be in the "middle" of a long context). This wiki's section order (Summary → Key Insights → Deep Analysis → Open Questions → Relationships) already implements this principle correctly for high-value content: Summary and Key Insights are always at the top. The lifecycle metadata enhancement would be: when the evolution pipeline generates higher-maturity pages, it should also reorder content within sections to front-load the highest-confidence claims. A `confidence: high` bullet within Key Insights should appear before a `confidence: medium` bullet, even within the same section.

## Relationships

- DERIVED FROM: src-llm-wiki-v2-agentmemory
- EXTENDS: [[LLM Wiki Pattern]]
- ENABLES: [[LLM Knowledge Linting]]
- RELATES TO: [[Wiki Ingestion Pipeline]]
- RELATES TO: [[LLM Wiki vs RAG]]
- RELATES TO: [[Claude Code Context Management]]
- RELATES TO: [[Wiki Knowledge Graph]]
- RELATES TO: [[Wiki Event-Driven Automation]]

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
[[Knowledge Evolution Pipeline]]
[[LLM-Maintained Wikis Outperform Static Documentation]]
[[Multi-Stage Ingestion Beats Single-Pass Processing]]
[[PARA Methodology]]
[[Progressive Distillation]]
[[Second Brain Architecture]]
[[Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py]]
[[Wiki Backlog Pattern]]
[[Zettelkasten Methodology]]
