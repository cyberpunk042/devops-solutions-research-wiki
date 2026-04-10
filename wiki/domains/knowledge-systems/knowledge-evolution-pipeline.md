---
title: "Knowledge Evolution Pipeline"
type: concept
layer: 2
maturity: growing
domain: knowledge-systems
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-10
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

> [!tip] The loop compounds — evolution has increasing returns to wiki density
> Every evolved page makes future evolution better. A promoted pattern page links back to its source concepts, increasing their relationship density, which improves their scoring in future runs. A well-linked wiki evolves faster than a sparse one. This is the mechanism that makes the wiki self-improving rather than merely accumulating.

> [!warning] Maturity is a lifecycle, not a tag
> seed → growing → mature → canonical is a defined promotion path. Pages are not born canonical; they earn maturity through scoring criteria measuring relationship density, cross-domain instances, source diversity, and age. Forcing premature canonicalization produces false authority; neglecting promotion produces orphaned seeds. The `--review` flag is the human gate placed at growing → mature — the transition where curator validation is most valuable.

**Deterministic scoring prevents LLM bias.** The scorer uses 6 signals (relationship count, cross-domain refs, source count, age, type weight, current maturity) — no LLM inference. Rankings are reproducible, auditable, immune to hallucination.

**Prompt assembly is the high-value step.** The builder pulls the candidate page + all referenced pages + all referencing pages + domain context. This context assembly is where the pipeline's intelligence lives: a well-assembled prompt produces a canonical pattern; a poorly assembled one produces a restatement. Quality scales with wiki density.

> [!info] Three backends for three contexts
>
> | Backend | Mode | When to Use |
> |---------|------|-------------|
> | `claude-code` | Prompt queue for session execution | High-complexity evolution, full reasoning |
> | `openai` / LocalAI | Direct API call | Batch evolution of lower-complexity pages, $0 target |
> | AICP | Routes through control platform | Fleet agent integration, sprint tasks |

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

### The Outer Loop

> [!abstract] Evolution is phase 2 of a 4-phase research loop
>
> 1. **Ingest** — Process raw sources into synthesized wiki pages (enter as `seed` maturity)
> 2. **Evolve** — Score all seeds + growing pages, promote top candidates to patterns/lessons/decisions
> 3. **Gaps** — `pipeline gaps` finds orphans, thin pages, missing backlinks, under-covered domains
> 4. **Research** — Queue new sources to fill gaps. Fetch → ingest → repeat
>
> Each cycle deepens the wiki. The second iteration produces better evolution candidates because the first iteration's promoted pages create new relationship edges that improve neighbor scores.

### Relationship to Second Brain Architecture

The evolution pipeline is the mechanism that distinguishes this wiki from a static documentation site. Tiago Forte's PARA method includes progressive summarization (raw → bold highlights → executive summary) as a manual process. Zettelkasten promotes "literature notes" to "permanent notes" through deliberate human processing. The evolution pipeline automates both: the maturity ladder is progressive summarization implemented as code, and the scored evolution queue is a Zettelkasten "inbox review" run by the scoring engine rather than a human.

The pipeline does not replace human judgment — it handles the bookkeeping that historically causes humans to abandon wikis, freeing curator attention for the genuinely high-value decisions (approving mature → canonical promotions, resolving contradictions, annotating with first-person reactions).

## Open Questions

- Can the scorer incorporate "how recently this page was referenced in a conversation" as a signal (LRU-style relevance weighting)? (Requires: implementation of conversation history tracking per page; AICP documents "memory relevance scoring" as a pattern but the specific mechanism for capturing session-level page access frequency is not covered in existing wiki pages)
- Is there a quantitative metric for "wiki evolution velocity" that tracks improvement rate over time? (Requires: definition of a formal velocity metric and implementation in `tools/stats.py`; the manifest.json tracks maturity distribution at a point in time but no per-period promotion-rate metric is defined in existing wiki pages)

### Answered Open Questions

> [!example]- Should evolved pages replace or coexist with source pages?
> Coexist. The source is preserved but marked `status: stale`. The promoted page carries `derived_from` frontmatter pointing back, plus a `SUPERSEDES` relationship. Both remain queryable and provenance is preserved. This matches PARA's Archive bucket (not deleted, moved out of active layer) and Zettelkasten's "literature notes" → "permanent notes" preservation.

> [!example]- Optimal frequency for the evolve loop?
> Weekly scheduled runs + threshold-triggered after ingestion sessions adding 5+ pages. The scorer is deterministic (same wiki state → identical rankings), so daily runs are safe but wasteful. `pipeline chain review` (post → review → gaps → crossref) is the natural weekly trigger point for adding `evolve --score` to the chain. This approximates PARA's weekly review cadence.

> [!example]- How are contradictions between canonical pages resolved?
> Link conflicting pages with `CONTRADICTS` (bidirectional). The linting pipeline surfaces the conflict with a recommended resolution based on source recency, authority, and supporting observation count. The `--review` human gate approves or overrides. The losing page is not deleted — it retains its `CONTRADICTS` backlink so contradiction history is preserved. This follows Zettelkasten's principle: preserve contradictions, link them explicitly.

## Relationships

- ENABLES: [[Second Brain Architecture]]
- IMPLEMENTS: [[Memory Lifecycle Management]]
- BUILDS ON: [[Wiki Ingestion Pipeline]]
- BUILDS ON: [[LLM Wiki Pattern]]
- FEEDS INTO: [[Wiki Knowledge Graph]]
- RELATES TO: [[Research Pipeline Orchestration]]
- RELATES TO: [[Obsidian Knowledge Vault]]
- RELATES TO: [[AICP]]
- COMPARES TO: [[LLM Wiki vs RAG]]

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
[[Execution Modes and End Conditions]]
[[Lesson: Automation Is the Bridge Between Knowledge and Action]]
[[Lesson: Knowledge Systems Is the Foundational Domain for the Entire Wiki]]
[[Lesson: Schema Is the Real Product — Not the Content]]
[[Local Inference Engine (Subsystem 3)]]
[[Model: Knowledge Evolution]]
[[Model: LLM Wiki]]
[[Never Skip Stages Even When Told to Continue]]
[[PARA Methodology]]
[[Progressive Distillation]]
[[Scaffold → Foundation → Infrastructure → Features]]
[[Shallow Ingestion Is Systemic, Not Isolated]]
[[Skyscraper, Pyramid, Mountain]]
[[The Agent Must Practice What It Documents]]
[[The Wiki Maintenance Problem Is Solved by LLM Automation]]
[[Wiki Backlog Pattern]]
[[Zettelkasten Methodology]]
