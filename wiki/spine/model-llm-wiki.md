---
title: "Model: LLM Wiki"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: authoritative
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources:
  - id: src-karpathy-llm-wiki-idea-file
    type: documentation
    file: raw/articles/karpathy-llm-wiki-idea-file.md
    title: "Karpathy LLM Wiki Idea File"
    ingested: 2026-04-08
tags: [llm-wiki, model, knowledge-system, repository-structure, schema, ingestion, evolution, standards]
---

# Model: LLM Wiki

## Summary

The LLM Wiki model defines how to build and operate a markdown-file wiki maintained by an LLM agent. It is not just a documentation tool — it is a structured knowledge system where the LLM ingests sources, synthesizes pages, cross-references relationships, evolves insights through density layers, and lints for quality — all automatically. The wiki compounds knowledge over time instead of decaying. This wiki project IS the reference implementation of this model. Any project in the ecosystem can adopt it by following the repository structure, schema, and pipeline standards defined here.

## Prerequisites

- Understanding of markdown and YAML frontmatter
- A project that needs persistent, structured knowledge (not just chat history)
- An LLM agent capable of file operations (Claude Code, OpenArms solo agent, or similar)

## Key Insights

- The wiki maintenance problem (wikis die because humans abandon upkeep) is structurally solved by making the LLM handle ALL mechanical operations
- Three core operations: Ingest (source → pages), Query (navigate via indexes), Lint (validate + cross-reference)
- The schema (`config/schema.yaml`) is the real product — content is regenerable, the schema that constrains it is not
- Knowledge layers (L1→L6) implement [[Progressive Distillation]] — each layer is denser and more actionable
- The repository structure below is the STANDARD for any project adopting this model
- Every operation is accessible from 4 interfaces: CLI, /commands, Skills, MCP

## Deep Analysis

### Core Principle

The wiki maintenance problem — wikis die because humans abandon maintenance — is solved by making the LLM responsible for ALL bookkeeping: index rebuilding, manifest regeneration, validation, wikilink updates, cross-referencing, and gap analysis. Humans provide direction and judgment. The LLM handles everything mechanical.

Three core operations (from Karpathy's original design):
1. **Ingest** — process any source (URL, file, paste) into structured wiki pages
2. **Query** — navigate the wiki via indexes and relationships (not vector search at this scale)
3. **Lint** — validate structure, detect orphans, flag stale content, surface contradictions

### Repository Structure Standard

```
project-root/
├── CLAUDE.md              # Agent instructions (the "brain config")
├── raw/                   # Unprocessed source material (permanent provenance)
│   ├── articles/          # Fetched web content, GitHub READMEs
│   ├── transcripts/       # YouTube/podcast transcripts
│   ├── notes/             # Legacy operator directives
│   └── dumps/             # Pasted content, research queues
├── wiki/                  # The wiki itself
│   ├── domains/           # L2 concept pages, organized by domain
│   │   ├── {domain-name}/ # One folder per domain
│   │   │   ├── _index.md  # Auto-maintained domain index
│   │   │   └── {page}.md  # One concept per page
│   ├── sources/           # L1 source-synthesis pages (src-*.md)
│   ├── comparisons/       # L3 structured comparison pages with matrices
│   ├── lessons/           # L4 codified experience (from evolution)
│   ├── patterns/          # L5 recurring cross-domain structures
│   ├── decisions/         # L6 actionable choice frameworks
│   ├── spine/             # Navigation: domain overviews, model guides, adoption guide
│   ├── backlog/           # PM: epics/, modules/, tasks/ with frontmatter state
│   ├── log/               # Operator directives, session logs, completion notes
│   ├── config/            # Methodology definition (methodology.yaml, agent-directive.md)
│   ├── manifest.json      # Auto-generated page index
│   └── index.md           # Wiki navigation entry point
├── tools/                 # Python pipeline tools
├── skills/                # Claude Code skill definitions
├── config/                # Schema, templates, export profiles
│   ├── schema.yaml        # Page validation schema
│   └── templates/         # Page scaffolding templates per type
├── .claude/
│   └── commands/          # Slash commands (/continue, /evolve, etc.)
└── docs/
    └── superpowers/       # Specs and plans (execution track)
```

### Knowledge Layer Architecture

| Layer | Directory | Type | What it contains | How it's created |
|-------|-----------|------|-----------------|-----------------|
| L0 | `raw/` | Raw sources | Unprocessed transcripts, articles, notes | `pipeline fetch` or manual drop |
| L1 | `wiki/sources/` | source-synthesis | Synthesized extraction from one source | Ingestion pipeline |
| L2 | `wiki/domains/` | concept | One concept per page, organized by domain | Ingestion + manual creation |
| L3 | `wiki/comparisons/` | comparison | Structured comparison with matrix table | Cross-reference analysis |
| L4 | `wiki/lessons/` | lesson | Codified experience with evidence | Evolution pipeline |
| L5 | `wiki/patterns/` | pattern | Recurring structure with 2+ instances | Evolution pipeline |
| L6 | `wiki/decisions/` | decision | Choice framework with alternatives + rationale | Evolution pipeline |
| Spine | `wiki/spine/` | various | Domain overviews, model guides, adoption guide | Manual curation |

Each layer is DENSER and MORE ACTIONABLE than the previous. Raw → synthesis → concept → comparison → lesson → pattern → decision. This IS the [[Progressive Distillation]] pattern applied to knowledge.

### Page Schema Standard

Every wiki page uses YAML frontmatter with required fields:

```yaml
---
title: "Page Title"           # Must match # Heading
type: concept                  # concept|source-synthesis|comparison|lesson|pattern|decision|...
domain: ai-agents              # Must match folder path
layer: 2                       # Knowledge layer (1-6, spine)
maturity: growing              # seed|growing|mature|canonical
status: synthesized            # raw|processing|synthesized|verified|stale
confidence: high               # low|medium|high|authoritative
created: 2026-04-09
updated: 2026-04-09
sources: []                    # Provenance: where this knowledge came from
tags: []                       # For cross-referencing and discovery
---
```

Additional fields for evolved pages (L4-L6):
- `derived_from: [list of source page titles]`
- `instances: [list for patterns]`
- `reversibility: easy|moderate|hard|irreversible` (for decisions)

Full schema: `config/schema.yaml`

### Page Section Standard

Every page follows this structure:

```markdown
# Title

## Summary          ← 2-3 sentences minimum, used as description
## Key Insights     ← Condensed takeaways
## Deep Analysis    ← Full depth (concept, comparison types)
## Open Questions   ← Gaps to fill, tagged with (Requires: ...)
## Relationships    ← [[wikilinks]] with ALL_CAPS verbs
## Backlinks        ← Auto-generated by obsidian.py
```

Evolved page types have additional required sections defined in `config/templates/`.

### Relationship Standard

Relationships use ALL_CAPS verbs, one per line, with [[wikilinks]]:

```markdown
## Relationships

- BUILDS ON: [[LLM Wiki Pattern]]
- ENABLES: [[Knowledge Evolution Pipeline]]
- RELATES TO: [[Second Brain Architecture]]
- DERIVED FROM: [[Synthesis: Karpathy's LLM Wiki Idea File]]
```

Supported verbs: BUILDS ON, ENABLES, COMPARES TO, CONTRADICTS, USED BY, RELATES TO, FEEDS INTO, DERIVED FROM, SUPERSEDES, IMPLEMENTS, EXTENDS, CONSTRAINS, PARALLELS, SYNTHESIZES

### Quality Gates

Every page must pass:
- Valid frontmatter per `config/schema.yaml`
- Summary ≥30 words
- At least 1 relationship (unless first in new domain)
- Title field matches # Heading
- Domain field matches folder path
- Source provenance (URL or file reference)
- No >70% concept overlap with existing pages

Validated by: `python3 -m tools.validate`

### Ingestion Workflow

```
Source arrives (URL, file, paste)
    ↓
pipeline fetch → saves to raw/
    ↓
Read FULL source (multiple offset reads for >200 lines)
    ↓
Verify depth: read actual INSTANCES not just descriptions (Layer 0 → Layer 1)
    ↓
Create source-synthesis page in wiki/sources/src-*.md
    ↓
Create/update concept pages in wiki/domains/
    ↓
pipeline post (6 steps):
  1. Rebuild domain + layer indexes
  2. Regenerate manifest.json
  3. Validate all pages
  4. Regenerate [[wikilinks]]
  5. Run lint checks
  6. Rebuild backlog/log indexes
```

### Evolution Workflow

```
pipeline evolve --score → rank candidates from 6 signals
    ↓
pipeline evolve --scaffold --top N → create page stubs from templates
    ↓
Fill pages with real content (this session or local model)
    ↓
pipeline post → validate
    ↓
pipeline evolve --review → check maturity promotions
```

Maturity lifecycle: `seed → growing → mature → canonical`
- seed: exists but unvalidated
- growing: human-reviewed, real derived_from, passes quality gates
- mature: cross-referenced by others, stable 30+ days
- canonical: authoritative reference, marked manually

### Pipeline Commands

| Command | What it does |
|---------|-------------|
| `pipeline post` | Full post-ingestion chain (6 steps) |
| `pipeline fetch URL` | Fetch source into raw/ |
| `pipeline evolve --score` | Rank evolution candidates |
| `pipeline evolve --scaffold --top N` | Scaffold top candidates |
| `pipeline evolve --review` | Check maturity promotions |
| `pipeline gaps` | Find orphans, thin pages, weak domains |
| `pipeline crossref` | Find missing backlinks, comparison candidates |
| `pipeline backlog` | Show project backlog state |
| `pipeline chain continue` | Resume mission (status → review → score → gaps) |
| `pipeline chain health` | Full health check |

### Interfaces (every operation at every level)

| Operation | CLI | /command | Skill | MCP |
|-----------|-----|---------|-------|-----|
| Resume | `pipeline chain continue` | `/continue` | `skills/continue/` | `wiki_continue` |
| Evolve | `pipeline evolve` | `/evolve` | `skills/evolve/` | `wiki_evolve` |
| Ingest | `pipeline fetch` | `/ingest` | `skills/wiki-agent/` | `wiki_fetch` |
| Review | `pipeline chain review` | `/review` | `skills/wiki-agent/` | `wiki_gaps` |
| Status | `pipeline status` | `/status` | — | `wiki_status` |
| Backlog | `pipeline backlog` | `/backlog` | — | `wiki_backlog` |

## How to Adopt This Model

1. Create the repository structure above
2. Copy `config/schema.yaml` → defines your page validation rules
3. Copy `config/templates/` → scaffolding templates per page type
4. Write your CLAUDE.md with the schema, conventions, and methodology rules
5. Start ingesting sources → the wiki grows from there
6. Run `pipeline post` after every change
7. Run `pipeline evolve --score` periodically to identify evolution candidates

Full guide: [[Adoption Guide — How to Use This Wiki's Standards]]

## Key Pages in This Model

| Page | Role |
|------|------|
| [[LLM Wiki Pattern]] | The foundational pattern (Karpathy's design) |
| [[Wiki Ingestion Pipeline]] | How sources become pages |
| [[Wiki Knowledge Graph]] | How relationships create a queryable graph |
| [[LLM Knowledge Linting]] | How quality is maintained automatically |
| [[Knowledge Evolution Pipeline]] | How pages evolve through density layers |
| [[Progressive Distillation]] | The pattern: raw → synthesis → lesson → pattern → decision |
| [[LLM Wiki vs RAG]] | When wiki navigation beats vector search |
| [[Decision: Wiki-First with LightRAG Upgrade Path]] | The scale decision |
| [[Second Brain Architecture]] | PKM theory (PARA, Zettelkasten) mapped to this wiki |
| [[Wiki Backlog Pattern]] | How the wiki tracks its own work |

## Lessons Learned (from building this wiki)

- [[LLM-Maintained Wikis Outperform Static Documentation]] — maintenance economics is the key
- [[Lesson: Schema Is the Real Product — Not the Content]] — the schema is more durable than any page
- [[Multi-Stage Ingestion Beats Single-Pass Processing]] — each pass discovers what the previous missed
- [[The Wiki Maintenance Problem Is Solved by LLM Automation]] — the 80-year gap from Memex to working implementation
- [[Never Synthesize from Descriptions Alone]] — read the THING, not the description of the thing
- [[Shallow Ingestion Is Systemic, Not Isolated]] — one quality defect = audit ALL similar artifacts
- [[Automated Knowledge Validation Prevents Silent Wiki Decay]] — without linting, wikis decay silently

## Outcomes

After studying this model you can:
- Set up a new LLM-maintained wiki from scratch following the repository structure
- Define a schema that enforces page quality
- Build an ingestion pipeline that processes any source type
- Understand why the schema document is more valuable than any individual page
- Run the evolution pipeline to generate higher-layer insights
- Know when to add LightRAG (at ~200 pages) and when to stay wiki-only

## Relationships

- FEEDS INTO: [[Model: Second Brain]]
- FEEDS INTO: [[Model Guide: Ecosystem Architecture]]
- ENABLES: [[Model Guide: Claude Code]]
- BUILDS ON: [[LLM Wiki Pattern]]
- BUILDS ON: [[Wiki Ingestion Pipeline]]
- BUILDS ON: [[Knowledge Evolution Pipeline]]
- RELATES TO: [[Model Guide: Methodology]]
- RELATES TO: [[Model: Knowledge Evolution]]

## Backlinks

[[[[Model: Second Brain]]]]
[[[[Model Guide: Ecosystem Architecture]]]]
[[[[Model Guide: Claude Code]]]]
[[[[LLM Wiki Pattern]]]]
[[[[Wiki Ingestion Pipeline]]]]
[[[[Knowledge Evolution Pipeline]]]]
[[[[Model Guide: Methodology]]]]
[[[[Model: Knowledge Evolution]]]]
