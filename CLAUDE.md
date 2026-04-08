# DevOps Solutions Research Wiki

A research-grade knowledge synthesis system and second brain. Central intelligence
spine for the devops ecosystem (openfleet, AICP, DSPD, devops-control-plane).

## What This Is

A monorepo containing:
- An interlinked wiki of synthesized knowledge across domains
- An ingestion pipeline that processes any source type into structured wiki pages
- Tooling for validation, linting, export, and integration with sister projects
- A skill that teaches Claude how to operate the entire system

## Project Structure

- `raw/` — Unprocessed source material (transcripts, articles, papers, notes, dumps)
- `wiki/` — Processed knowledge (domains/, sources/, comparisons/, index.md, manifest.json)
- `tools/` — Python utilities (lint, manifest, export, validate, stats)
- `skills/` — Claude skill definitions
- `config/` — Schema, domain registry, export profiles, quality standards
- `docs/` — Project documentation and specs

## Page Schema

Every wiki page uses YAML frontmatter with these required fields:

  title, type, domain, status, confidence, created, updated, sources, tags

Page types: concept, source-synthesis, comparison, reference, deep-dive, index

Status lifecycle: raw → processing → synthesized → verified → stale

Confidence levels: low, medium, high, authoritative

## Page Structure

Every page follows this section order:

  # Title
  ## Summary          ← minimal resolution (2-3 sentences min, used for LightRAG description)
  ## Key Insights     ← condensed resolution boundary
  ## Deep Analysis    ← full resolution (concept, comparison, deep-dive types)
  ## Open Questions   ← gaps to fill (optional but encouraged)
  ## Relationships    ← VERB: target format, one per line

## Relationship Conventions

Use ALL_CAPS verbs. One relationship per line. Comma-separated targets allowed.

  BUILDS ON, ENABLES, COMPARES TO, CONTRADICTS, USED BY,
  RELATES TO, FEEDS INTO, DERIVED FROM, SUPERSEDES, IMPLEMENTS, EXTENDS

Format: `- VERB: Target Name (optional context)`

Compatible with openfleet kb_sync.py regex: ^([A-Z][A-Z /\-]+?):\s*(.+)$

## Ingestion Modes

Three modes, user specifies or defaults to smart:

- `auto` — Process without stopping. Report summary after.
- `guided` — Show extraction plan. Wait for approval. Review each page.
- `smart` (default) — Auto when confident. Escalate when: new domain,
  contradictions, ambiguity, expert-level complexity, low-quality source.

## Ingestion Sources

Accept any of:
- Files dropped in raw/ (any subfolder)
- URLs (fetch via WebFetch, save to raw/, then process)
- Pasted content (save to raw/dumps/, then process)

## Quality Gates

Every page must have:
- Complete frontmatter with valid values per config/schema.yaml
- Summary (min 30 words)
- At least 1 relationship (unless first in new domain)
- Reachable from domain _index.md
- Source provenance (URL or file reference)
- No >70% concept overlap with existing pages (update instead of create)
- title field matches # Heading
- domain field matches folder path

## Post-Ingestion

After every ingestion:
1. Update affected _index.md files
2. Regenerate manifest.json via tools/manifest.py
3. Run tools/validate.py — errors block completion
4. Flag stale pages affected by new information
5. Report summary of changes

## Integration

This wiki feeds sister projects via file-based export:
- openfleet — LightRAG graph via ## Relationships (kb_sync.py compatible)
- AICP — docs/kb/ via export (tools/export.py)
- DSPD, control-plane — future

Export profiles defined in config/export-profiles.yaml.
Export transforms YAML frontmatter to markdown headers for compatibility.

## Tooling

- `python3 tools/validate.py` — Schema validation (exit 0 = clean, 1 = errors)
- `python3 tools/manifest.py` — Regenerate wiki/manifest.json
- `python3 tools/lint.py [--report|--summary|--fix]` — Health checks
- `python3 tools/export.py [openfleet|aicp]` — Export for sister projects
- `python3 tools/stats.py [--json]` — Coverage & growth reporting

## Conventions

- kebab-case filenames
- One concept per page
- Update existing pages rather than creating duplicates
- Domains grow organically — create new domain folders as needed
- _index.md in every domain folder, auto-maintained
- manifest.json regenerated after every wiki change
- raw/ files kept permanently for provenance
- Sources prefixed with src- in wiki/sources/
