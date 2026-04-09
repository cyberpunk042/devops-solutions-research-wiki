---
title: "Knowledge Evolution Pipeline"
type: concept
domain: knowledge-systems
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-pipeline-tooling
    type: documentation
    file: tools/pipeline.py
    title: "Wiki Pipeline Tool — evolve command"
    ingested: 2026-04-08
  - id: src-claude-md
    type: documentation
    file: CLAUDE.md
    title: "Wiki Project Instructions"
    ingested: 2026-04-08
tags: [evolution, knowledge-systems, pipeline, maturity, scoring, second-brain, llm-automation, seed, growing, mature, canonical, wiki-evolution]
---

# Knowledge Evolution Pipeline

## Summary

The knowledge evolution pipeline is the mechanism by which this wiki promotes raw synthesized pages through increasing levels of maturity — from seed observations to canonical patterns and decisions — using a deterministic scoring engine that identifies high-value evolution candidates, a prompt builder that assembles generation context from existing wiki relationships, and LLM backends that generate evolved content. The pipeline operationalizes the insight that a second brain must not just accumulate knowledge but continuously distill it: ingest → synthesize → evolve → gap-analyze → research → repeat. This loop is the automated maintenance mechanism that prevents wiki decay and enables compounding knowledge value.

## Key Insights

- **Maturity is a lifecycle, not a tag**: seed → growing → mature → canonical is a defined promotion path. Pages are not born canonical; they earn maturity through scoring criteria that measure relationship density, cross-domain instances, source diversity, and age. Forcing premature canonicalization produces false authority; neglecting promotion produces orphaned seeds.

- **Deterministic scoring prevents LLM bias in candidate selection**: The evolve scorer uses 6 deterministic signals — relationship count, cross-domain references, source count, page age, type weight (patterns and lessons score higher than raw concepts), and existing maturity level — to rank evolution candidates. No LLM inference in the scoring phase means rankings are reproducible, auditable, and immune to hallucination.

- **Prompt engineering is the high-value step**: The prompt builder assembles generation context by pulling the candidate page, all pages it references, all pages that reference it, and domain context. This context assembly is where the "intelligence" of the pipeline lives: a well-assembled prompt produces a canonical pattern page; a poorly assembled one produces a restatement. The builder is deterministic but its output quality scales with wiki density.

- **Three backends for three contexts**: The pipeline supports Claude Code (write a prompt queue for session execution), OpenAI/LocalAI (direct API generation), and AICP (route through the devops AI control platform). The backend choice depends on cost tolerance, model capability, and integration context — not on the evolution logic itself.

- **The loop compounds**: every evolved page makes future evolution better. A promoted pattern page links back to its source concepts, increasing their relationship density, which improves their scoring in future runs. A well-linked wiki evolves faster than a sparse one — the pipeline has increasing returns to wiki density.

- **Evolution gates quality**: the `--review` flag surfaces seed pages that have accumulated enough relationships to warrant human review before promotion. This is the human-in-the-loop checkpoint in an otherwise automated pipeline, placed at the transition between growing and mature — the point where LLM-generated content may benefit from curator validation.

## Deep Analysis

### The Six Scoring Signals

The `evolve --score` command computes a composite score for each eligible page using these deterministic signals:

| Signal | Rationale |
|--------|-----------|
| Relationship count | Pages with more relationships have more context for evolution; they sit at network junctions |
| Cross-domain reference count | Pages referenced by other domains have demonstrated generality — the hallmark of a canonical pattern |
| Source count | Multi-source synthesis is more reliable than single-source summary |
| Page age (days since created) | Older pages have had time to accumulate references; young pages may be premature |
| Type weight | `pattern` and `lesson` types score higher because they represent distilled cross-domain knowledge |
| Current maturity | `seed` pages score higher than `growing` pages (more room for evolution); `mature` pages are excluded unless specifically targeted |

The composite score is deterministic: run the scorer twice on the same wiki state and get identical rankings. This is a deliberate design choice — reproducible scoring enables the pipeline to be run on a schedule without producing random output, and it makes the evolution queue a reliable work item rather than a surprise.

### The Generation Loop

```
1. SCORE      → rank all pages by evolution potential
2. SELECT     → top N candidates (--top N flag, default 1)
3. ASSEMBLE   → pull candidate + related pages + domain context into prompt
4. GENERATE   → send to LLM backend (claude-code | openai | aicp)
5. WRITE      → save evolved page (new type, higher maturity layer)
6. POST-CHAIN → validate → manifest → lint → index
7. REVIEW     → human checkpoint for maturity promotion
8. LOOP       → re-score (evolved pages change neighbor scores)
```

Steps 1-3 and 6 are deterministic Python. Steps 4-5 involve LLM inference. Step 7 is the optional human gate. Step 8 closes the feedback loop.

### Maturity Levels and Promotion Criteria

| Level | Meaning | Promotion Trigger |
|-------|---------|-------------------|
| `seed` | Initial synthesis, single source, minimal relationships | Created at ingestion; auto-assigned |
| `growing` | Multiple sources, 3+ relationships, cross-referenced | Scorer selects for evolution; LLM promotes |
| `mature` | Canonical within domain, 5+ relationships, verified | Human review gate (`--review` flag) |
| `canonical` | Cross-domain authority, instances documented, verified | Reserved for proven patterns with 3+ real instances |

Pages do not self-promote. Promotion happens when the scorer selects a page and the pipeline generates a higher-maturity version. The original page is preserved (or marked `status: stale`) and the promoted page carries a `derived_from` frontmatter field pointing back.

### The Outer Loop: Ingest → Evolve → Gaps → Research

Evolution is not a standalone operation. It is the second phase of a research loop:

1. **Ingest**: Process raw sources (transcripts, articles, GitHub READMEs) into synthesized wiki pages. These enter as `seed` maturity.
2. **Evolve**: Score all seeds + growing pages, promote top candidates to patterns/lessons/decisions.
3. **Gaps**: Run `pipeline gaps` to find orphans, thin pages, missing backlinks, and under-covered domains.
4. **Research**: Queue new sources to fill identified gaps. Fetch → ingest → repeat.

Each full loop cycle deepens the wiki. The second iteration produces better evolution candidates because the first iteration's promoted pages have created new relationship edges that improve neighbor scores.

### Backend Integrations

**Claude Code backend** (`--backend claude-code`): Writes a prompt queue file with fully assembled generation prompts. The user runs these prompts in a Claude Code session. Appropriate for high-complexity evolution tasks where the full Claude reasoning capability is needed and cost is acceptable.

**OpenAI/LocalAI backend** (`--backend openai`): Direct API call with assembled context. Appropriate for batch evolution of lower-complexity pages. LocalAI runs locally with hermes-3b for routine inference, avoiding cloud API cost.

**AICP backend**: Routes through the devops AI control platform, enabling integration with the OpenFleet agent fleet. An AICP agent can run evolution as part of a sprint task.

### Relationship to Second Brain Architecture

The evolution pipeline is the mechanism that distinguishes this wiki from a static documentation site. Tiago Forte's PARA method includes progressive summarization (raw → bold highlights → executive summary) as a manual process. Zettelkasten promotes "literature notes" to "permanent notes" through deliberate human processing. The evolution pipeline automates both: the maturity ladder is progressive summarization implemented as code, and the scored evolution queue is a Zettelkasten "inbox review" run by the scoring engine rather than a human.

The pipeline does not replace human judgment — it handles the bookkeeping that historically causes humans to abandon wikis, freeing curator attention for the genuinely high-value decisions (approving mature → canonical promotions, resolving contradictions, annotating with first-person reactions).

## Open Questions

- Can the scorer incorporate "how recently this page was referenced in a conversation" as a signal (LRU-style relevance weighting)? (Requires: implementation of conversation history tracking per page; AICP documents "memory relevance scoring" as a pattern but the specific mechanism for capturing session-level page access frequency is not covered in existing wiki pages)
- Is there a quantitative metric for "wiki evolution velocity" that tracks improvement rate over time? (Requires: definition of a formal velocity metric and implementation in `tools/stats.py`; the manifest.json tracks maturity distribution at a point in time but no per-period promotion-rate metric is defined in existing wiki pages)

### Answered Open Questions

**Q: Should evolved pages replace their source pages (marking source `status: stale`) or coexist as separate maturity layers?**

Cross-referencing `Second Brain Architecture` and `PARA Methodology`: both coexist, with the source preserved but marked `status: stale`. This wiki's own `Knowledge Evolution Pipeline` Deep Analysis section documents the mechanism explicitly: "The original page is preserved (or marked `status: stale`) and the promoted page carries a `derived_from` frontmatter field pointing back." The `Second Brain Architecture` page maps `status: stale` pages to PARA's Archive bucket — the knowledge is not deleted but moved out of the active layer. The `PARA Methodology` page confirms: "Archives are not deleted — they are available for search but do not appear in active views." The `Memory Lifecycle Management` page's supersession principle is also aligned: "The new claim should explicitly supersede it with linked timestamps, preserving the old version but marking it stale." Together, these sources give the canonical answer: evolved pages coexist with their source pages; the source is marked `status: stale` with a `derived_from` reference in the promoted page, and a `SUPERSEDES` relationship pointing from promoted to source. Both remain queryable and provenance is preserved.

**Q: What is the optimal frequency for running the full evolve loop on a growing wiki — daily, weekly, or triggered by relationship count thresholds?**

Cross-referencing `Second Brain Architecture`, `PARA Methodology`, and `Research Pipeline Orchestration`: the answer is weekly triggered runs, supplemented by relationship-threshold-based triggering. The `Second Brain Architecture` page explicitly documents: "Both PARA and Zettelkasten prescribe periodic review: weekly review of active projects, quarterly review of areas, annual review to archive. This wiki has no scheduled review mechanism. A weekly `pipeline gaps` scan and stale-page audit would approximate this." The `PARA Methodology` page confirms weekly review as the PARA cadence for active items. The evolution pipeline's scorer is deterministic (running it twice produces identical rankings on the same wiki state), so daily runs are safe but wasteful — the ranking does not change unless new pages are ingested or relationships are added. The practical recommendation from cross-referencing: run the full evolve loop weekly as a scheduled chain (approximating PARA's weekly review), and trigger an additional run after any ingestion session that adds 5+ new pages (threshold-based, because new pages change neighbor scores). The `Research Pipeline Orchestration` page's `pipeline chain review` command is the concrete implementation: it runs `post → review → gaps → crossref` as a weekly health check, which is the natural trigger point for adding `evolve --score` to the chain.

**Q: How should contradictions between promoted pages be surfaced? If two pattern pages reach `canonical` maturity with conflicting recommendations, what resolves the conflict?**

Cross-referencing `Zettelkasten Methodology`, `Wiki Knowledge Graph`, and `LLM Knowledge Linting`: contradictions between canonical pages are surfaced via the `CONTRADICTS` typed relationship verb and resolved through the linting pipeline's contradiction resolution step. The `Zettelkasten Methodology` page establishes the philosophical position: "Zettelkasten traditionally preserves contradictions and links them" — the network should include contradictory nodes, with explicit links encoding the nature of the disagreement. The `Wiki Knowledge Graph` page confirms that `CONTRADICTS` is one of the typed relationship verbs used in this wiki's implementation and enables the query "What contradicts this claim?" via typed traversal. The `LLM Knowledge Linting` page documents the resolution mechanism: "Beyond flagging contradictions, the LLM should propose which claim is more likely correct based on source recency, source authority, and supporting observation count. The human can override, but the default behavior should usually be right." The operational answer: when two canonical pages contradict each other, link them with `CONTRADICTS` (bidirectional), run the lint pass to surface the conflict with a recommended resolution, and use the `--review` human gate to approve or override. The losing page is not deleted — it is marked `status: stale` (or retains its status with a `CONTRADICTS` backlink) so the contradiction history is preserved for future analysis.

## Relationships

- ENABLES: Second Brain Architecture
- IMPLEMENTS: Memory Lifecycle Management
- BUILDS ON: Wiki Ingestion Pipeline
- BUILDS ON: LLM Wiki Pattern
- FEEDS INTO: Wiki Knowledge Graph
- RELATES TO: Research Pipeline Orchestration
- RELATES TO: Obsidian Knowledge Vault
- RELATES TO: AICP
- COMPARES TO: LLM Wiki vs RAG

## Backlinks

[[Second Brain Architecture]]
[[Memory Lifecycle Management]]
[[Wiki Ingestion Pipeline]]
[[LLM Wiki Pattern]]
[[Wiki Knowledge Graph]]
[[Research Pipeline Orchestration]]
[[Obsidian Knowledge Vault]]
[[AICP]]
[[LLM Wiki vs RAG]]
[[Automated Knowledge Validation Prevents Silent Wiki Decay]]
[[Cross-Domain Patterns]]
[[Decision: Local Model vs Cloud API for Routine Operations]]
[[Decision: Wiki-First with LightRAG Upgrade Path]]
[[Lesson: Automation Is the Bridge Between Knowledge and Action]]
[[Lesson: Knowledge Systems Is the Foundational Domain for the Entire Wiki]]
[[Lesson: Schema Is the Real Product — Not the Content]]
[[PARA Methodology]]
[[Progressive Distillation]]
[[The Wiki Maintenance Problem Is Solved by LLM Automation]]
[[Zettelkasten Methodology]]
