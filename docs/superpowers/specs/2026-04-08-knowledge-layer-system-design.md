# Knowledge Layer System — Design Spec

## Problem

The wiki currently operates as a flat system: sources go in, concept pages come out, relationships connect them. But ingestion is not terminal — it should be the start of a knowledge evolution pipeline that produces structured lessons, patterns, principles, and decisions. There's no hierarchy of knowledge maturity, no strategic templates, no spine that defines what the vault's architecture should look like.

The user's directive: "These things ingest are not meant to be dump but to be smart and give birth to other layers, to evolutions of ideas and aggregations and filterings and orderings and annotatings and enriching."

## Solution

A layered knowledge architecture with 6 explicit layers, strategic spine pages, enforced templates, and per-layer quality gates. Each layer builds on the previous, creating a knowledge evolution pipeline from raw sources to actionable decisions.

## Knowledge Layers

```
Layer 0: Raw sources            → raw/ (transcripts, articles, papers, notes)
Layer 1: Source syntheses       → wiki/sources/ (what a source says)
Layer 2: Concepts               → wiki/domains/ (what we know about a topic)
Layer 3: Comparisons            → wiki/comparisons/ (how things relate/differ)
Layer 4: Lessons                → wiki/lessons/ (what we learned)
Layer 5: Patterns               → wiki/patterns/ (what recurs)
Layer 6: Decisions              → wiki/decisions/ (what to do)
Spine:   Strategic architecture → wiki/spine/ (how it all fits together)
```

Layers 0-3 exist today. Layers 4-6 and the spine are new.

## Directory Structure

```
wiki/
├── domains/                    # Layer 2 (existing)
├── sources/                    # Layer 1 (existing)
├── comparisons/                # Layer 3 (existing)
├── lessons/                    # Layer 4 (NEW)
│   ├── _index.md
│   └── {lesson-slug}.md
├── patterns/                   # Layer 5 (NEW)
│   ├── _index.md
│   └── {pattern-slug}.md
├── decisions/                  # Layer 6 (NEW)
│   ├── _index.md
│   └── {decision-slug}.md
├── spine/                      # Curator layer (NEW)
│   ├── _index.md
│   ├── domain-overviews/
│   │   └── {domain}-overview.md
│   ├── learning-paths/
│   │   └── {path-slug}.md
│   └── evolution-log/
│       └── {concept}-evolution.md
├── manifest.json
└── index.md
```

## New Page Types

### Lesson (Layer 4)

A single distilled insight synthesized from one or more source-derived pages.

```yaml
title: "Lesson title"
type: lesson
domain: ai-agents          # primary domain
layer: 4
status: synthesized
confidence: high
maturity: seed              # seed | growing | mature | canonical
derived_from:               # pages this lesson was extracted from
  - "Claude Code Best Practices"
  - "Harness Engineering"
created: 2026-04-08
updated: 2026-04-08
tags: [...]
```

Required sections:
- **Summary** — the lesson in 2-3 sentences
- **Context** — when/where this lesson applies
- **Insight** — the core learning, stated clearly (min 50 words)
- **Evidence** — specific examples/data from derived_from pages
- **Applicability** — domains, projects, situations where this applies
- **Relationships**

### Pattern (Layer 5)

A recurring structure observed across 2+ sources, concepts, or lessons.

```yaml
title: "Pattern name"
type: pattern
domain: cross-domain
layer: 5
status: synthesized
confidence: high
maturity: growing
derived_from:
  - "Lesson A"
  - "Lesson B"
  - "Concept C"
instances:                  # specific occurrences of this pattern
  - page: "OpenFleet"
    context: "Deterministic orchestrator implements Plan→Execute→Review"
  - page: "Harness Engineering"
    context: "5-verb workflow: Setup→Plan→Work→Review→Release"
created: 2026-04-08
updated: 2026-04-08
tags: [...]
```

Required sections:
- **Summary** — the pattern in 2-3 sentences
- **Pattern Description** — what it is, how to recognize it (min 100 words)
- **Instances** — 2+ specific examples from the wiki (with page references)
- **When To Apply** — conditions that make this pattern appropriate
- **When Not To** — anti-patterns, conditions where this fails
- **Relationships**

### Decision (Layer 6)

An actionable choice framework with explicit tradeoffs and rationale.

```yaml
title: "Decision: X vs Y"
type: decision
domain: tools-and-platforms
layer: 6
status: synthesized
confidence: high
maturity: mature
derived_from:
  - "Pattern A"
  - "Lesson B"
reversibility: easy         # easy | moderate | hard | irreversible
created: 2026-04-08
updated: 2026-04-08
tags: [...]
```

Required sections:
- **Summary** — the decision and its recommendation in 2-3 sentences
- **Decision** — clear statement of what to do
- **Alternatives** — what else was considered (min 2 alternatives)
- **Rationale** — why this choice, backed by evidence (min 100 words)
- **Reversibility** — how hard to undo, what changes if reversed
- **Dependencies** — what this decision affects downstream
- **Relationships**

### Domain Overview (Spine)

Strategic view of a domain's knowledge state.

```yaml
title: "AI Agents — Domain Overview"
type: domain-overview
domain: ai-agents
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-08
updated: 2026-04-08
tags: [...]
```

Required sections:
- **Summary** — domain scope and current state
- **State of Knowledge** — what we know well, what's thin
- **Maturity Map** — pages by maturity (seed → canonical)
- **Gaps** — what's missing, what to research next
- **Priorities** — ordered list of next research targets
- **Key Pages** — the essential reading for this domain
- **Relationships**

### Learning Path (Spine)

Ordered sequence of pages to achieve a learning goal.

```yaml
title: "Learning Path: Building an Agent Fleet"
type: learning-path
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-08
updated: 2026-04-08
tags: [...]
```

Required sections:
- **Summary** — what you'll learn and why
- **Prerequisites** — what to read/know first
- **Sequence** — ordered list of pages with brief annotation per step
- **Outcomes** — what you should understand after completing the path
- **Relationships**

### Evolution (Spine)

Timeline of how a concept or decision has changed.

```yaml
title: "Evolution: LLM Wiki Pattern"
type: evolution
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-08
updated: 2026-04-08
tags: [...]
```

Required sections:
- **Summary** — what evolved and the current state
- **Timeline** — chronological entries (date, event, significance)
- **Key Shifts** — turning points that changed direction
- **Current State** — where the concept stands now
- **Relationships**

## New Frontmatter Fields

Added to config/schema.yaml:

```yaml
optional_fields:
  - layer           # int: 1-6 or "spine"
  - derived_from    # list of page titles this was synthesized from
  - maturity        # seed | growing | mature | canonical
  - instances       # list of {page, context} for pattern pages
  - reversibility   # easy | moderate | hard | irreversible (decision pages)

enums:
  maturity:
    - seed          # just created, needs validation
    - growing       # validated, being enriched
    - mature        # stable, well-connected
    - canonical     # authoritative, reference-quality
  reversibility:
    - easy
    - moderate
    - hard
    - irreversible
```

## Templates

Each new page type gets a template in `config/templates/`:

```
config/templates/
├── lesson.md
├── pattern.md
├── decision.md
├── domain-overview.md
├── learning-path.md
└── evolution.md
```

Templates contain placeholder frontmatter + section headers + inline guidance comments. Used by:
- `tools/pipeline.py` when scaffolding new evolved pages
- Claude Code when creating pages manually
- `tools/validate.py` to verify section completeness

## Quality Gates per Layer

| Layer | Type | Min Summary | Min Content Section | Min Rels | Special |
|-------|------|------------|---------------------|----------|---------|
| 1 | source-synthesis | 30 words | — | 1 | needs source ref |
| 2 | concept | 30 words | 100w (Deep Analysis) | 1 | needs source ref |
| 3 | comparison | 30 words | 100w (Deep Analysis) | 2 | needs 2+ sources |
| 4 | lesson | 30 words | 50w (Insight) | 1 | needs derived_from |
| 5 | pattern | 50 words | 100w (Pattern Description) | 2 | needs 2+ instances |
| 6 | decision | 50 words | 100w (Rationale) | 2 | needs derived_from |
| spine | domain-overview | 50 words | — | 3 | — |
| spine | learning-path | 50 words | — | 3 | needs Sequence |
| spine | evolution | 50 words | — | 2 | needs Timeline |

## Tool Changes

### config/schema.yaml
- Add 6 new types to `enums.type`
- Add `required_sections` for each new type
- Add `optional_fields`: layer, derived_from, maturity, instances, reversibility
- Add `enums.maturity` and `enums.reversibility`

### tools/validate.py
- Validate new page types against new required_sections
- Validate `derived_from` references resolve to existing pages
- Validate `instances` references resolve for pattern pages
- Enforce per-layer quality gates (min content words per section)

### tools/manifest.py
- Index `layer`, `maturity`, `derived_from` in manifest
- Add `layers` section to manifest stats
- Track layer distribution and maturity distribution

### tools/pipeline.py
- New command: `pipeline scaffold <type> <title>` — create a page from template
- New chain: `evolve` — gaps → identify lesson candidates → scaffold → post
- New chain: `spine-refresh` — rebuild domain overviews from manifest + gaps

### tools/stats.py
- Report per-layer stats (pages, maturity distribution)
- Report evolution metrics (lessons per domain, pattern coverage)

### tools/common.py
- Add `rebuild_layer_index()` for lessons/, patterns/, decisions/, spine/

### tools/obsidian.py
- Graph color groups for new directories (lessons=green, patterns=blue, decisions=orange, spine=gold)

## Relationship to Existing Pages

Existing 48 pages are unmodified. They are Layer 1-3 content. The new layers reference them via `derived_from` and `DERIVED FROM` relationships. The spine pages reference everything.

The first evolved pages to create after implementation:
1. Domain overviews for each of the 7 domains (from gaps analysis data)
2. 3-5 lessons from the strongest cross-source insights already identified
3. 1-2 patterns (Plan→Execute→Review cycle, CLI>MCP trend)
4. 1 decision (MCP vs CLI+Skills for tool integration)

## Success Criteria

- All 6 new page types validated by tools/validate.py
- Templates in config/templates/ for each type
- `pipeline scaffold lesson "CLI vs MCP"` creates a valid page from template
- `pipeline chain evolve` identifies and scaffolds lesson candidates
- `pipeline chain health` reports layer distribution
- Manifest includes layer/maturity stats
- Obsidian graph shows colored layers
