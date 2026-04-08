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

After every ingestion, run: `python3 -m tools.pipeline post`

This executes all 5 steps automatically:
1. Rebuild affected _index.md files
2. Regenerate manifest.json
3. Validate all pages — errors block completion
4. Regenerate wikilinks via obsidian.py
5. Run lint checks and report summary

## Integration

This wiki feeds sister projects via file-based export:
- openfleet — LightRAG graph via ## Relationships (kb_sync.py compatible)
- AICP — docs/kb/ via export (tools/export.py)
- DSPD, control-plane — future

Export profiles defined in config/export-profiles.yaml.
Export transforms YAML frontmatter to markdown headers for compatibility.

## Tooling

### Pipeline (primary entry point)

- `python3 -m tools.pipeline post` — Run full post-ingestion chain (index → manifest → validate → obsidian → lint)
- `python3 -m tools.pipeline fetch URL [URL...]` — Fetch URLs into raw/
- `python3 -m tools.pipeline fetch --batch file.txt` — Batch fetch from URL list
- `python3 -m tools.pipeline fetch --topic "query"` — Queue a research topic
- `python3 -m tools.pipeline scan ../project/` — Scan local project, copy key docs to raw/
- `python3 -m tools.pipeline status` — Show raw files and wiki stats
- `python3 -m tools.pipeline run URL [URL...]` — Parallel fetch + post-chain in one command
- `python3 -m tools.pipeline gaps` — Gap analysis (orphans, thin pages, weak domains, open questions)
- `python3 -m tools.pipeline crossref` — Cross-reference analysis (missing backlinks, domain bridges, comparison candidates)
- `python3 -m tools.pipeline chain <name>` — Run a named chain (ingest, ingest-local, analyze, full, health)
- `python3 -m tools.pipeline chain --list` — List available chains

### Sync (WSL ↔ Windows)

- `python -m tools.sync` — One-shot sync wiki/ to Windows for Obsidian
- `python -m tools.sync --watch` — Watch daemon, auto-syncs on changes (bidirectional)
- `python -m tools.sync --watch --interval 10` — Custom watch interval
- `python -m tools.sync --reverse` — Sync from Windows back to WSL
- `python -m tools.sync --status` — Show sync config and last sync
- `python -m tools.sync --target /path` — Override target path
- Env: `WIKI_SYNC_TARGET` to override default, `WIN_USER` for Windows username

### Individual tools

- `python3 -m tools.validate` — Schema validation (exit 0 = clean, 1 = errors)
- `python3 -m tools.manifest -o wiki/manifest.json` — Regenerate manifest
- `python3 -m tools.lint [--report|--summary|--fix]` — Health checks
- `python3 -m tools.export [openfleet|aicp]` — Export for sister projects
- `python3 -m tools.stats [--json]` — Coverage & growth reporting
- `python3 -m tools.obsidian` — Regenerate [[wikilinks]] for Obsidian graph view
- `python3 -m tools.ingest URL [URL...]` — Fetch URLs (YouTube, GitHub, web) into raw/
- `python3 -m tools.ingest --list-raw` — List unprocessed raw files

## Setup

Cross-platform (Linux, macOS, Windows):

    python -m tools.setup              # Full setup (check + deps + obsidian config)
    python -m tools.setup --check      # Check environment
    python -m tools.setup --deps       # Install dependencies via uv + Python 3.11 venv
    python -m tools.setup --obsidian-config  # Configure Obsidian vault

Requires uv (https://docs.astral.sh/uv/). All tools run via `.venv/bin/python -m tools.<name>`.

## Conventions

- kebab-case filenames
- One concept per page
- Update existing pages rather than creating duplicates
- Domains grow organically — create new domain folders as needed
- _index.md in every domain folder, auto-maintained
- manifest.json regenerated after every wiki change
- raw/ files kept permanently for provenance
- Sources prefixed with src- in wiki/sources/
