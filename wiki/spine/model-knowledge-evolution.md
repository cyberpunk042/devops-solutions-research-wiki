---
title: "Model: Knowledge Evolution"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [model, spine, knowledge-evolution, maturity, progressive-distillation, wiki-lifecycle, scoring, evolution-pipeline, second-brain]
---

# Model: Knowledge Evolution

## Summary

The Knowledge Evolution model describes how raw sources become lessons, patterns, and decisions through a structured, automated promotion pipeline. Raw files enter as seed-maturity pages; a deterministic scorer ranks them by six signals (relationship density, cross-domain references, source count, age, type weight, current maturity); the prompt builder assembles generation context from wiki relationships; an LLM backend generates evolved content; and a human review gate validates promotion to mature and canonical tiers. The pipeline is self-compounding: promoted pages add relationship edges that improve neighbor scores in subsequent runs. The outer loop — ingest → evolve → gap-analyze → research → repeat — is the wiki's steady-state improvement mechanism, preventing knowledge decay while continuously increasing the density and applicability of what is stored.

## Key Insights

- **The scorer is deterministic; the generator is not**: ranking evolution candidates uses six reproducible signals with no LLM inference. This makes rankings auditable, schedulable, and immune to hallucination. The LLM is only invoked after a candidate is selected — for generation, not selection. The separation is deliberate.

- **Maturity is a lifecycle, not a tag**: seed → growing → mature → canonical is a promotion path with defined criteria. Pages are not born canonical. Forcing premature canonicalization produces false authority. Neglecting promotion produces orphaned seeds — pages that accumulated insights but never got distilled into actionable form.

- **The pipeline has increasing returns**: every evolved page creates new relationship edges back to its source concepts. Those edges increase source concept scores in subsequent scoring runs. A well-linked wiki evolves faster than a sparse one — the pipeline rewards prior investment in quality ingestion and cross-linking.

- **Prompt engineering is where pipeline intelligence lives**: the prompt builder assembles the candidate page, all pages it references, all pages that reference it, and domain context. A well-assembled prompt produces a canonical pattern page. A poorly assembled one produces a restatement. Builder quality scales with wiki density — another form of increasing returns.

- **The 6-layer architecture maps to Progressive Distillation**: raw files (Layer 0) → synthesized sources (Layer 1) → concepts (Layer 2) → lessons (Layer 4) → patterns (Layer 5) → decisions (Layer 6). Each layer is qualitatively different, not just compressed. See [[Progressive Distillation]] for the pattern that governs all six layers.

- **Three LLM backends for three operating contexts**: `--backend claude-code` writes a prompt queue for session execution (human-in-the-loop, highest quality); `--backend openai` with LocalAI routes lower-complexity evolution to free local inference; `--backend aicp` routes through the devops AI control platform for fleet-integrated generation. Backend selection is separate from evolution logic.

## Deep Analysis

### The 6-Layer Density Architecture

The wiki's six layers represent increasing levels of knowledge distillation. Each layer is a transformation, not a compression:

| Layer | Type | Maturity | What It Contains |
|-------|------|----------|-----------------|
| 0 | Raw files | — | Unprocessed transcripts, articles, notes in `raw/` |
| 1 | Source synthesis | seed | What the source says, direct evidence preserved |
| 2 | Concepts | seed → growing | Synthesized understanding, multi-source integration |
| 4 | Lessons | growing → mature | Validated insight — what was learned and why it holds |
| 5 | Patterns | mature | Structural template — reusable form that generalizes across instances |
| 6 | Decisions | canonical | Resolved choice — rationale, alternatives considered, consequences |

The gaps (no Layer 3) are intentional — the numbering reflects density tiers in the original PARA/Zettelkasten-influenced design, where the jump from concept to lesson represents a qualitative shift that warrants a tier gap. A lesson is not a dense concept; it is a validated principle with operational evidence behind it.

### The Six Scoring Signals

The `evolve --score` command computes a composite score using these deterministic signals, in approximate order of weight:

1. **Relationship count** — how many other pages this page references or is referenced by. High relationship density indicates a page that other knowledge depends on or builds from — a candidate for pattern or decision promotion.

2. **Cross-domain references** — how many of its relationships point to pages in different domains. Cross-domain pages are high-value evolution targets because they surface generalizable insights, not domain-specific observations.

3. **Source count** — how many distinct sources back the page. Multi-source concepts have higher epistemic weight and are closer to promotable lessons.

4. **Page age** — how long since creation. Pages that have existed for a while without promotion have had time to accumulate backlinks from new pages; revisiting them often reveals they qualify for promotion that wasn't clear at creation.

5. **Type weight** — pattern and lesson candidates score higher than raw concepts at the same relationship count, because their page type signals that evolution is the expected next step.

6. **Current maturity** — seed pages score higher than growing pages, which score higher than mature pages. This biases the scorer toward pages most in need of evolution, not pages already advanced.

Full implementation: `tools/pipeline.py evolve --score` with optional `--top N --json` for machine-readable output. See [[Knowledge Evolution Pipeline]] for signal weight details and the composite formula.

### The 8-Step Generation Loop

```
1. SCORE    → rank all eligible pages by composite score
2. SELECT   → choose top N candidates (human-reviewed or automated)
3. ASSEMBLE → prompt builder gathers candidate + all related pages + domain context
4. GENERATE → LLM backend produces evolved page content (lesson/pattern/decision type)
5. WRITE    → scaffolded page written to correct domain folder with full frontmatter
6. POST     → post-chain validates, rebuilds indexes, regenerates wikilinks
7. REVIEW   → human gate: verify maturity promotion before marking mature/canonical
8. LOOP     → re-score; newly added relationships shift neighbor scores
```

The ASSEMBLE step is where pipeline quality is highest and most variable. A candidate concept page with 12 strong relationships pointing to primary sources produces a context package that almost writes the lesson itself. A candidate with 3 thin relationships to other seed pages produces weak generation context. This is why [[Multi-Stage Ingestion Beats Single-Pass Processing]] is a prerequisite for effective evolution: the pipeline's inputs depend entirely on ingestion quality.

### The Four Maturity Levels and Promotion Criteria

**Seed** — freshly ingested or created; minimal cross-linking; may have a single source. No special requirements beyond valid frontmatter and a Summary. Seeds are expected to remain seeds until enough related content accumulates to make evolution meaningful.

**Growing** — has 3+ relationships, 2+ sources, has been referenced by at least one other page. Growing pages are visible in the scorer and eligible for evolution runs. Most pages live here for weeks before promotion.

**Mature** — has passed human review; the insight it captures has been validated against operational evidence; has a `derived_from` link to its source concepts. Mature pages are treated as reliable by the wiki's cross-reference tools and the LightRAG graph.

**Canonical** — the highest maturity tier; reserved for pages that have been tested against real implementation and have no known contradictions in the knowledge base. Canonical pages should be rare — premature canonicalization is a documented failure mode ([[Lesson: Schema Is the Real Product — Not the Content]]).

### The Three LLM Backends

**`--backend claude-code`** (session execution)
Writes a prompt queue to disk for human execution in a Claude Code session. The human reviews each prompt, can edit it, and executes at their discretion. Highest quality — the human can inspect and improve the assembled context before generation. Slowest — requires a human in the loop.

**`--backend openai`** (direct API, uses LocalAI when configured)
Calls an OpenAI-compatible API directly, producing pages without human review at the generation step. With LocalAI configured as the endpoint, this is zero-cost for seed → growing evolution. Review step still occurs after generation. Appropriate for high-volume, lower-stakes evolution runs.

**`--backend aicp`** (fleet-integrated)
Routes through the AICP inference platform, applying its complexity scorer and routing logic. High-complexity pages go to Claude; routine pages go to LocalAI. The AICP backend makes the evolution pipeline a first-class citizen of the fleet's inference budget management — evolution tasks compete for resources alongside agent tasks rather than running in a separate cost silo.

### Two Documented Failure Modes

The evolution pipeline documentation identifies two failure modes that must be actively prevented:

**Premature distillation** — promoting a page to pattern or canonical status before it has enough cross-domain evidence, source diversity, or relationship density to justify the authority that canonical tier confers. A single-source pattern page looks authoritative but is actually one person's observation of one implementation. When other agents or pages cite it as canonical, the authority claim is unsupported. The scorer guards against this by requiring minimum signal thresholds before a page is eligible for promotion.

**Distillation arrest** — seeds that accumulate enough relationships to qualify for evolution but never get promoted. These are the most insidious failure mode because the value is there (the page is cited, cross-linked, multi-sourced) but it remains locked in seed format — no distilled lesson, no structural template, no explicit decision rationale. Distillation arrest often results from high-scoring candidates that the human reviewer keeps deferring. The `--review` flag surfaces these explicitly: pages in growing maturity with scores above the promotion threshold that have not been acted on.

Both failure modes are addressed by the same mechanism: running the evolution pipeline regularly and acting on its output. A pipeline that runs but whose output is never reviewed is equivalent to no pipeline at all. The human-in-the-loop checkpoint between growing and mature is where both failure modes are caught or allowed to persist.

### Connection to the LLM Wiki Model

The evolution pipeline's output — mature patterns and canonical decisions — is exactly the content that makes the LightRAG knowledge graph valuable. Pattern pages create hub nodes in the graph: many concepts reference them, many lessons derive from them, and they appear as common intermediaries in graph traversal. When `kb_sync.py` parses the wiki's relationships into the LightRAG graph, promoted pages are the high-connectivity nodes that make semantic search and graph-enhanced retrieval return relevant results.

This connection means evolution quality directly affects fleet intelligence quality. A wiki with mostly seed-maturity pages produces a sparse, low-signal graph. A wiki with well-evolved patterns and decisions produces a dense graph that enables contextually grounded navigation. See [[Model: LLM Wiki]] for the full LightRAG integration model.

### Evolved Pages and Their Source Pages

A common question: when a concept page gets evolved into a lesson or pattern, should the source page be deleted, updated, or preserved?

The correct answer is preserve and mark. Evolved pages coexist with their source pages. The source concept page gets `status: stale` and a `derived_from` reference pointing to the evolved page. The evolved page has a `derived_from` field in its frontmatter listing the source concepts.

Why coexistence matters:

1. **The source page preserves the evidence layer**: the evolved lesson or pattern makes a generalized claim. The source concept page contains the specific evidence (data points, source citations, implementation details) that justifies the claim. Deleting the source page removes the evidence layer — the evolved page becomes an assertion without grounding.

2. **The graph needs both nodes**: LightRAG's knowledge graph gains value from the parent-child relationship between source concept and evolved page. Both nodes appear in graph traversal. The source page is the evidence node; the evolved page is the synthesis node. Queries can traverse from specific evidence to generalized insight or from generalized insight to supporting evidence.

3. **Stale marking is honest**: `status: stale` signals that the page has been superseded by a more mature synthesis, but does not delete the page's evidence value. A wiki visitor encountering a stale page is directed to the evolved version via the `derived_from` link — they get the navigation benefit without losing the option to examine the primary source.

The only case for removing a source page is if it is demonstrably wrong (not just superseded) and the wrongness would mislead someone who encounters it. In that case, the stale page should explicitly note the correction rather than being silently deleted.

### The Weekly Evolution Cadence

```
Weekly review chain:
  1. post              → validate, manifest, lint (catch decay since last run)
  2. review            → surface pages ready for maturity promotion
  3. gaps              → orphans, thin pages, open questions, weak domains
  4. crossref          → missing backlinks, comparison candidates, domain bridges

When evolution is queued:
  5. evolve --score --top 10   → rank candidates, review the list
  6. evolve --dry-run --top 3  → preview assembled context before generation
  7. Execute top candidates     → generate lessons/patterns/decisions
  8. post                       → validate new evolved pages, rebuild indexes
  9. gaps                       → re-run to see what promotions unlocked
```

This cadence is codified in `python3 -m tools.pipeline chain review`.

## Open Questions

- The 200-page threshold for LightRAG integration was set empirically — what specific graph density metric actually triggers the need for graph-enhanced retrieval vs pure index navigation?
- How should the scorer handle pages that were highly connected at creation (manually cross-linked during ingestion) vs pages that accumulated connections organically over time? Manual seeding could inflate scores artificially.
- Does the `--backend openai` / LocalAI path produce materially worse page quality than `--backend claude-code` for the same candidate? A systematic quality comparison would inform backend selection guidance.

## Relationships

- BUILDS ON: [[Knowledge Evolution Pipeline]]
- BUILDS ON: [[Progressive Distillation]]
- RELATES TO: [[Model: SFIF and Architecture]]
- RELATES TO: [[Model: Ecosystem Architecture]]
- RELATES TO: [[Model: LLM Wiki]]
- FEEDS INTO: [[Model: Automation and Pipelines]]
- ENABLES: [[Decision: Wiki-First with LightRAG Upgrade Path]]
- ENABLES: [[Decision: Local Model vs Cloud API for Routine Operations]]

## Backlinks

[[Knowledge Evolution Pipeline]]
[[Progressive Distillation]]
[[Model: SFIF and Architecture]]
[[Model: Ecosystem Architecture]]
[[Model: LLM Wiki]]
[[Model: Automation and Pipelines]]
[[Decision: Wiki-First with LightRAG Upgrade Path]]
[[Decision: Local Model vs Cloud API for Routine Operations]]
[[Model: NotebookLM]]
[[Model: Second Brain]]
