---
title: "PARA Methodology"
type: concept
layer: 2
maturity: growing
domain: knowledge-systems
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-second-brain-research
    type: article
    file: raw/articles/second-brain-pkm-research.md
    title: "Second Brain / PKM Research"
    ingested: 2026-04-08
  - id: src-zettelkasten-basb
    type: article
    url: "https://zettelkasten.de/posts/building-a-second-brain-and-zettelkasten/"
    title: "Combining Zettelkasten and Building a Second Brain"
    ingested: 2026-04-08
tags: [para, pkm, second-brain, tiago-forte, projects, areas, resources, archives, code-workflow, progressive-summarization, knowledge-management, action-oriented]
---

# PARA Methodology

## Summary

PARA is Tiago Forte's action-oriented personal knowledge management framework that organizes all information into four buckets — Projects (active, outcome-bound), Areas (ongoing responsibilities), Resources (reference material), and Archives (inactive items) — and pairs them with the CODE workflow (Capture, Organize, Distill, Express) and progressive summarization to move material from raw capture toward usable knowledge. Where Zettelkasten optimizes for idea density and connection discovery, PARA optimizes for retrieval speed in service of active work. This wiki maps directly onto PARA: raw/ is Capture, wiki/domains/ is Areas, wiki/sources/ is Resources, and the evolution pipeline's maturity promotion is progressive summarization implemented as code.

## Key Insights

- **Action drives organization, not taxonomy**: PARA buckets are defined by actionability, not subject matter. A book about machine learning can live in Projects (currently reading for a deliverable), Areas (relevant to an ongoing ML responsibility), Resources (reference, not active), or Archives (read and no longer relevant). The same material belongs in different buckets at different lifecycle stages. This means PARA is not a taxonomy — it is an activity-relative filing system.

- **Projects are the defining category**: PARA's most important distinction is between Projects and Areas. A Project has a specific outcome and a deadline. An Area is an ongoing responsibility with no terminal state. Misclassifying Areas as Projects (treating "infrastructure reliability" as a Project) leads to perpetual "projects" that never complete. Misclassifying Projects as Areas leads to un-owned work with no delivery accountability.

- **Progressive summarization is the distillation layer**: Forte's progressive summarization technique layers highlighting over multiple passes — read and highlight key passages; bold the most critical highlights; write a one-paragraph executive summary. The goal is to make future retrieval fast: the summary is actionable in 30 seconds; the highlighted text is actionable in 2 minutes; the full source is available for deep reference. This is the same layered structure this wiki uses in ## Summary → ## Key Insights → ## Deep Analysis.

- **CODE workflow closes the loop**: Capture (get everything out of your head and into a trusted system) → Organize (move to the right PARA bucket) → Distill (progressive summarization to reduce to essential value) → Express (use the knowledge to produce something). CODE is a workflow, not a structure — it describes how information moves through the system, not where it lives.

- **Archives are the secret to a healthy system**: Most PKM systems fail because people fear archiving. PARA treats archiving as a first-class operation, not a concession. Inactive projects, completed responsibilities, and consumed resources belong in Archives — where they are retrievable but do not clutter the active view. A clean active layer (Projects + Areas) is what makes the system feel fast.

- **PARA's weakness is what Zettelkasten fills**: PARA manages the lifecycle of information resources but does not process them into permanent knowledge. A book in Resources is still just a book — PARA gives it a bucket, not a place in your thinking. Zettelkasten fills this gap: Resources are the input; permanent notes linked to the Zettelkasten network are the output.

## Deep Analysis

### The Four Buckets

**Projects** — Short-horizon, outcome-bound, has a deadline:
- Specific deliverable: "Deploy monitoring stack for production by Q2"
- Narrowly defined scope
- Once complete, the project moves to Archives
- Rule of thumb: if you cannot describe when it will be done, it is not a Project

**Areas** — Ongoing responsibilities with no end date:
- "Infrastructure reliability", "Team knowledge management", "Security posture"
- Requires maintenance and attention indefinitely
- Associated with a role or identity (you are responsible for this area)
- Rule of thumb: if it ends when you change jobs or roles, it was an Area

**Resources** — Reference material collected for potential future use:
- Saved articles, books, research, tool documentation
- No current activation — just "might be useful"
- Organized by topic, not by project or responsibility
- Rule of thumb: if someone else might benefit from it, it is a Resource

**Archives** — Inactive items from the above three:
- Completed projects
- No-longer-relevant areas
- Consumed or outdated resources
- Archives are not deleted — they are available for search but do not appear in active views

### The CODE Workflow

The CODE workflow is how information moves through the system:

1. **Capture**: Get anything potentially useful into the system immediately. Quantity over quality at this stage — capture everything, sort nothing. The raw/ directory in this wiki is the capture layer.

2. **Organize**: Move captured items to their PARA bucket as quickly as possible. No deep processing at this stage — just filing. The goal is to clear the capture queue and get material into its correct context.

3. **Distill**: Process items toward their essential value. Progressive summarization happens here. Extract the key insight. Write the permanent note. Reduce to what will be useful 2 years from now, not just today.

4. **Express**: Use the distilled knowledge to produce something: a document, a decision, a recommendation, a system change. Expression is the test of whether knowledge was actually internalized. This wiki's `decisions/` and `wiki/spine/` layers are the expression layer.

### Progressive Summarization in Detail

Progressive summarization is a layered reading technique designed for future retrieval:

| Pass | Action | Reading time |
|------|--------|-------------|
| 1 — Capture | Save the full source (note, article, transcript) | — |
| 2 — Highlight | Bold or highlight the most important 10-20% | 5-10 minutes |
| 3 — Bold highlights | Bold the most essential 5-10% of the highlighted material | 2-3 minutes |
| 4 — Executive summary | Write a 1-3 sentence summary in your own words | 1 minute |

The layers accumulate — the full text is always preserved below the summary. This means the system adapts to retrieval context: quick decision → read the summary; detailed reference → read the highlighted text; deep research → read the full source.

This wiki maps progressive summarization directly onto its page structure:
- `## Summary` = executive summary (pass 4)
- `## Key Insights` = bolded highlights (pass 3)
- `## Deep Analysis` = highlighted material (pass 2)
- Source file in `raw/` = full capture (pass 1)

### How This Wiki Maps to PARA

| PARA Element | This Wiki's Implementation |
|---|---|
| Projects | `wiki/decisions/` — bound decisions with specific outcomes |
| Areas | `wiki/domains/*/` — ongoing knowledge domains (ai-agents, knowledge-systems, etc.) |
| Resources | `wiki/sources/` — synthesized individual source pages |
| Archives | Pages with `status: stale`; superseded entries with `SUPERSEDES` relationship |
| Capture (CODE) | `raw/` — all source material, kept permanently for provenance |
| Organize (CODE) | Ingestion pipeline routes to correct domain; frontmatter assigns type/domain |
| Distill (CODE) | `## Summary` + `## Key Insights` + evolution pipeline maturity promotion |
| Express (CODE) | Export pipeline → openfleet, AICP; decisions/; spine/ cross-cutting synthesis |

### PARA vs. Zettelkasten: Complementary Layers

The two methodologies solve different problems:

| Dimension | PARA | Zettelkasten |
|-----------|------|-------------|
| Primary question | "Where does this live? Is it active?" | "What does this connect to? What does it mean?" |
| Organization unit | Bucket (project/area/resource/archive) | Note with links |
| Navigation model | Folder hierarchy | Graph traversal |
| Processing output | Highlighted/summarized source | Permanent linked note in your own words |
| Strength | Action orientation, fast retrieval, lifecycle management | Deep synthesis, connection discovery, emergent insight |
| Weakness | Does not extract ideas from sources | No lifecycle management, no project tracking |

The recommended hybrid: PARA manages what lives outside the Zettelkasten (active projects, resource filing, archiving). Zettelkasten processes the most valuable materials into permanent linked knowledge. Every project completion is an opportunity to feed project-specific insights back into the Zettelkasten as new permanent notes.

## Open Questions

- What is the right trigger for moving a wiki domain from "Areas" to "Archives" status — inactivity threshold, explicit decision, or relevance scoring? (Requires: a curator decision on archiving policy; the pipeline gaps command can surface domains with no recently updated pages as candidates, but the promotion trigger itself is a policy decision not resolved by existing wiki pages)

### Answered Open Questions

**Q: Should `decisions/` be a sub-layer of Projects (each decision was a project) or Areas (ongoing decision framework)?**

Cross-referencing `Second Brain Architecture` and `Knowledge Evolution Pipeline`: `decisions/` maps most precisely to Projects in PARA, not Areas. The `Second Brain Architecture` page documents the wiki's PARA mapping explicitly: "Project notes (PARA) → `wiki/spine/` — cross-cutting synthesis; `decisions/`." A Project in PARA "has a specific outcome and a deadline" — each decision page represents a bounded deliberation with a resolved outcome (the decision itself). The `PARA Methodology` page reinforces: "if you cannot describe when it will be done, it is not a Project" — decisions are done when the decision is made. Once made, the decision page moves to a reference role (Areas or Resources) rather than an active project. The `Knowledge Evolution Pipeline` page maps `wiki/decisions/` to the "Expression" phase of the CODE workflow — decisions are the output of distillation, not the container for ongoing work. The practical answer: `decisions/` is the Projects layer during deliberation, and becomes Resources (archived decisions, consulted for reference) after the decision is made. The `status: verified` frontmatter field marks the transition from active project to archived reference.

**Q: How should the CODE workflow's Express phase be operationalized for this wiki — beyond export profiles, what constitutes "expression" for a knowledge system?**

Cross-referencing `Second Brain Architecture` and `Knowledge Evolution Pipeline`: expression has three operationalized forms in this wiki, beyond the documented export profiles. First, the `Second Brain Architecture` page maps the Express phase to "Export pipeline → openfleet, AICP; `decisions/` layer" — meaning export to sister projects is the primary expression mechanism. Second, the `Knowledge Evolution Pipeline` page's outer loop identifies the research phase as a form of expression: identifying gaps → queuing new sources → fetching → ingesting is the wiki "expressing" its understanding into research priorities. Third, the `PARA Methodology` page notes: "Expression is the test of whether knowledge was actually internalized" — for a knowledge system, the equivalent test is whether synthesized knowledge changes behavior in the ecosystem (an OpenFleet agent making better decisions because the wiki's LightRAG graph has been updated, or a sprint decision informed by a canonical pattern page). Expression for a knowledge system is: (1) export to consuming systems, (2) decisions that change ecosystem behavior, and (3) wiki-informed research priorities that drive new ingestion.

**Q: Is progressive summarization best implemented as page sections, or should separate summary artifacts exist per domain (FAQ pages as Forte's "executive summary" layer)?**

Cross-referencing `Second Brain Architecture` and `Zettelkasten Methodology`: both layers are valuable but serve different audiences and use cases. The `Second Brain Architecture` page identifies this directly as a gap: "Systematic FAQs per domain — PARA's progressive summarization produces 'executive summaries' at each layer. This wiki has `## Summary` sections per page, but no domain-level distillation artifacts." The `Zettelkasten Methodology` page confirms that the `domain-overview` page type is the correct structural answer: it requires `## Summary`, `## State of Knowledge`, `## Maturity Map`, `## Gaps`, and `## Priorities` sections — this is a domain-level progressive summarization artifact, not a page-level one. The `Second Brain Architecture` page explicitly recommends these belong in `wiki/domains/*/faq.md` files or as a `domain-overview` page type. The synthesis answer: page-level sections (`## Summary` + `## Key Insights` + `## Deep Analysis`) implement progressive summarization at the concept level (Forte's "layered notes"); `domain-overview` pages implement it at the domain level (Forte's "executive summary" layer for an entire subject area). Both are needed; `domain-overview` pages are the more urgently missing layer since per-page sections are already implemented.

## Relationships

- BUILDS ON: [[Second Brain Architecture]]
- COMPARES TO: [[Zettelkasten Methodology]]
- IMPLEMENTS: [[Memory Lifecycle Management]]
- RELATES TO: [[Wiki Ingestion Pipeline]]
- RELATES TO: [[Knowledge Evolution Pipeline]]
- FEEDS INTO: [[Research Pipeline Orchestration]]
- RELATES TO: [[LLM Wiki Pattern]]

## Backlinks

[[Second Brain Architecture]]
[[Zettelkasten Methodology]]
[[Memory Lifecycle Management]]
[[Wiki Ingestion Pipeline]]
[[Knowledge Evolution Pipeline]]
[[Research Pipeline Orchestration]]
[[LLM Wiki Pattern]]
[[Cross-Domain Patterns]]
[[Model: Second Brain]]
[[Progressive Distillation]]
