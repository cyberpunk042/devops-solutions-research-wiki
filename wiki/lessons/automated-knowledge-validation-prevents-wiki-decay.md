---
title: "Automated Knowledge Validation Prevents Silent Wiki Decay"
type: lesson
domain: knowledge-systems
layer: 4
status: synthesized
confidence: high
maturity: growing
created: 2026-04-08
updated: 2026-04-10
derived_from:
  - "LLM Knowledge Linting"
  - "Knowledge Evolution Pipeline"
sources:
  - id: src-karpathy-claude-code-10x
    type: youtube-transcript
    file: raw/transcripts/karpathy-claude-code-10x.txt
    title: "Andrej Karpathy Just 10x'd Everyone's Claude Code"
  - id: src-karpathy-llm-wiki-idea-file
    type: documentation
    url: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
    title: "Karpathy LLM Wiki Idea File"
  - id: src-pipeline-tooling
    type: documentation
    file: tools/pipeline.py
    title: "Wiki Pipeline Tool"
tags: [linting, validation, wiki-decay, knowledge-quality, post-chain, automation, maintenance]
---

# Automated Knowledge Validation Prevents Silent Wiki Decay

## Summary

Wikis without automated validation decay silently: pages go stale, relationships break, orphaned concepts accumulate, and contradictions persist unnoticed until the knowledge base becomes untrustworthy. Running a post-ingestion validation chain on every change — schema validation, manifest regeneration, wikilink checking, and lint health checks — closes the quality gap before it opens rather than cleaning up accumulated debt later.

## Context

This lesson applies to any knowledge base that receives regular automated ingestion. The triggering condition is scale: once a wiki grows past a few dozen pages edited by an automated pipeline, manual inspection of each change becomes impractical. The failure mode is insidious — individual pages look fine but the graph as a whole drifts into inconsistency. The Karpathy LLM Wiki pattern explicitly identifies lint as one of three core operations (Ingest, Query, Lint) precisely because he had seen this decay pattern in practice.

## Insight

> [!warning] Decay Is Cheaper to Prevent Than to Fix
> Running a 6-step validation chain immediately after each ingestion costs roughly the same as running it once, but prevents the compounding accumulation that makes periodic cleanup expensive. Structural violations can be auto-blocked; semantic violations require human review.

Knowledge decay is not a dramatic event — it is a slow accumulation of small inconsistencies that compound. A page that references a concept which was renamed creates a broken wikilink. An ingested source that contradicts an earlier synthesis creates a silent factual conflict. A new domain page that never gets added to its `_index.md` becomes an orphan. None of these failures are individually critical, but collectively they erode the trust and navigability of the entire knowledge base. The key insight is that decay is cheaper to prevent than to fix: running a 6-step validation chain immediately after each ingestion costs roughly the same as running it once, but prevents the compounding accumulation that makes periodic cleanup expensive.

The automation threshold matters. Structural violations (broken links, missing frontmatter fields, pages not reachable from domain index) have unambiguous correct states and can be auto-fixed or auto-blocked. Semantic violations (contradictions between page claims, stale facts) require LLM judgment or human review. The correct architecture separates these: structural validation runs in the post-chain as a blocking gate (errors prevent completion); semantic linting runs as a recommendation layer (surfaced for review, not auto-corrected).

The LLM Knowledge Linting page captures Karpathy's original scope: "contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search." The LLM Wiki v2 extension promotes lint from passive health check to active self-healing: orphan pages get linked or flagged, stale claims get marked, broken cross-references get repaired automatically.

## Evidence

This wiki's post-chain (`python3 -m tools.pipeline post`) implements the prevention model directly. The Knowledge Evolution Pipeline page documents the 6 automated steps triggered after every ingestion:

1. Rebuild affected `_index.md` files (including layer indexes)
2. Regenerate `manifest.json` with layer and maturity stats
3. Validate all pages — errors block completion
4. Regenerate wikilinks via `obsidian.py`
5. Run lint checks and report summary
6. Rebuild layer indexes (lessons/, patterns/, decisions/, spine/)

Step 3 is the blocking gate: validation failures halt the post-chain, preventing a broken page from entering the wiki. Step 5 is the advisory layer: lint reports issues without blocking, surfacing semantic quality signals for human review.

The Knowledge Evolution Pipeline's answered question on incremental linting confirms the architectural choice: "The pipeline post command runs validate + lint after every ingestion as step 5 of the 6-step post-chain. This is lint-on-ingest for the pages created in that ingestion run." The LLM Knowledge Linting page documents the remaining gap: cross-page semantic linting (checking new pages for contradictions with existing pages) is not yet fully automated and requires the incremental approach — identifying pages that reference the same concepts, then running targeted consistency checks on that subset.

The LLM Knowledge Linting page also documents the self-healing extension from LLM Wiki v2: "The wiki should tend toward health on its own. Lint triggers confidence decay for unconfirmed facts, identifies candidates for promotion between consolidation tiers, flags stale content for supersession review, and automatically repairs structural issues like broken cross-references and orphan pages."

## Applicability

This lesson applies to:

- **Any automated ingestion pipeline**: The moment content enters a wiki without human review of every change, automated validation is mandatory. This is not optional infrastructure — it is the maintenance mechanism that makes automation safe.
- **The four-project ecosystem** (openfleet, AICP, DSPD, devops-control-plane): Each project that syncs knowledge from this wiki benefits from the guarantee that only validated content is exported. The `tools/export.py` path only reaches content that has passed the post-chain.
- **LightRAG integration**: When the wiki is synced to LightRAG via `kb_sync.py`, entity and relationship consistency depends on wiki structural validity. A wiki with broken wikilinks produces a knowledge graph with dangling edges.
- **Team wikis at any scale**: The post-chain pattern scales from single-author to multi-author wikis because validation is deterministic and machine-enforced — not dependent on reviewer discipline.

## Relationships

- DERIVED FROM: [[LLM Knowledge Linting]]
- DERIVED FROM: [[Knowledge Evolution Pipeline]]
- BUILDS ON: [[LLM Wiki Pattern]]
- ENABLES: [[Knowledge Evolution Pipeline]]
- FEEDS INTO: [[Wiki Knowledge Graph]]
- RELATES TO: [[LLM Wiki vs RAG]]
- RELATES TO: [[Research Pipeline Orchestration]]

## Backlinks

[[LLM Knowledge Linting]]
[[Knowledge Evolution Pipeline]]
[[LLM Wiki Pattern]]
[[Wiki Knowledge Graph]]
[[LLM Wiki vs RAG]]
[[Research Pipeline Orchestration]]
[[Shallow Ingestion Is Systemic, Not Isolated]]
