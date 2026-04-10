# DevOps Solutions Research Wiki

A research-grade knowledge synthesis system and second brain. Central intelligence
spine for the devops ecosystem (openfleet, AICP, DSPD, devops-control-plane).

## What This Is

A monorepo containing:
- An interlinked wiki of synthesized knowledge across domains
- An ingestion pipeline that processes any source type into structured wiki pages
- Tooling for validation, linting, export, and integration with sister projects
- A skill that teaches Claude how to operate the entire system

**Start here:** `wiki/spine/model-registry.md` — lists all 15 named models with their
companion standards pages. Models are the primary knowledge containers.

## Project Structure

- `raw/` — Unprocessed source material (transcripts, articles, papers, notes, dumps)
- `wiki/` — Processed knowledge (domains/, sources/, comparisons/, lessons/, patterns/, decisions/, spine/, backlog/, log/, config/, index.md, manifest.json)
- `tools/` — Python utilities (lint, manifest, export, validate, stats)
- `skills/` — Claude skill definitions
- `config/` — Schema, domain registry, export profiles, quality standards
- `docs/` — Project documentation and specs

## Page Schema

Every wiki page uses YAML frontmatter with these required fields:

  title, type, domain, status, confidence, created, updated, sources, tags

Page types: concept, source-synthesis, comparison, reference, deep-dive, index,
  lesson, pattern, decision, domain-overview, learning-path, evolution

Optional fields for evolved pages: layer, derived_from, maturity, instances, reversibility

Maturity levels: seed, growing, mature, canonical

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

Evolved page types (lesson, pattern, decision) have additional required sections.
See config/templates/ for section structure. Scaffold via: `python3 -m tools.pipeline scaffold <type> <title>`

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
- Complete frontmatter with valid values per config/wiki-schema.yaml
- Summary (min 30 words)
- At least 1 relationship (unless first in new domain)
- Reachable from domain _index.md
- Source provenance (URL or file reference)
- No >70% concept overlap with existing pages (update instead of create)
- title field matches # Heading
- domain field matches folder path

## Post-Ingestion

After every ingestion, run: `python3 -m tools.pipeline post`

This executes all 6 steps automatically:
1. Rebuild affected _index.md files (including layer indexes)
2. Regenerate manifest.json (with layer/maturity stats)
3. Validate all pages — errors block completion
4. Regenerate wikilinks via obsidian.py
5. Run lint checks and report summary
6. Rebuild layer indexes (lessons/, patterns/, decisions/, spine/)

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
- `python3 -m tools.pipeline scaffold <type> <title>` — Create page from template
- `python3 -m tools.pipeline evolve --score` — Rank evolution candidates (deterministic)
- `python3 -m tools.pipeline evolve --score --top 5 --json` — Top 5 candidates as JSON
- `python3 -m tools.pipeline evolve --scaffold --top 3` — Scaffold top 3 candidates
- `python3 -m tools.pipeline evolve --dry-run --top 1` — Preview generation prompt
- `python3 -m tools.pipeline evolve --auto --backend openai` — Generate via local model
- `python3 -m tools.pipeline evolve --auto --backend claude-code` — Write prompt queue
- `python3 -m tools.pipeline evolve --execute` — List prompt queue for session execution
- `python3 -m tools.pipeline evolve --review` — List seed pages ready for maturity promotion
- `python3 -m tools.pipeline backlog` — Show backlog summary (epics, tasks, completion %)
- `python3 -m tools.pipeline backlog --epic E001` — Show epic detail with children
- `python3 -m tools.pipeline chain <name>` — Run a named chain (ingest, ingest-local, analyze, full, health, evolve, evolve-auto)
- `python3 -m tools.pipeline chain continue` — Resume mission (status → review → score → gaps → crossref)
- `python3 -m tools.pipeline chain review` — Weekly health check (post → review → gaps → crossref)
- `python3 -m tools.pipeline chain --list` — List available chains

### Skills (conversation interface)

Skills in `skills/` — invocable via natural language or slash commands:
- `wiki-agent` — Ingest sources, query knowledge, maintain quality, export
- `evolve` — Score candidates, scaffold, generate, review maturity, detect staleness
- `continue` — Resume the mission: run diagnostics, show state, present options

### MCP Server (native tools for any Claude Code conversation)

Registered in `.mcp.json` — auto-discovered by Claude Code.
17 tools: wiki_status, wiki_search, wiki_read_page, wiki_list_pages,
wiki_post, wiki_fetch, wiki_fetch_topic, wiki_scan_project,
wiki_gaps, wiki_crossref, wiki_sync, wiki_mirror_to_notebooklm,
wiki_integrations, wiki_continue, wiki_evolve, wiki_backlog, wiki_log.

Manual start: `.venv/bin/python -m tools.mcp_server`

### Watcher (change detection → auto-pipeline)

- `python -m tools.watcher` — One-shot: report changes since last check, trigger post-chain
- `python -m tools.watcher --watch` — Daemon: poll for changes, auto-run post-chain on wiki edits
- `python -m tools.watcher --watch --sync` — Also auto-sync to Windows on changes
- `python -m tools.watcher --watch --interval 5` — Custom poll interval
- `python -m tools.watcher --reset` — Reset change tracking baseline
- `python -m tools.watcher --no-post` — Report changes without running post-chain

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
    python -m tools.setup --services              # List available services
    python -m tools.setup --services wiki-sync    # Deploy sync daemon (WSL→Windows, auto-detect target)
    python -m tools.setup --services wiki-sync --target /mnt/c/Users/You/vault  # Custom target
    python -m tools.setup --services wiki-watcher # Deploy watcher daemon (auto post-chain)

Requires uv (https://docs.astral.sh/uv/). All tools run via `.venv/bin/python -m tools.<name>`.

## Agent Methodology — MANDATORY

You MUST follow this methodology in order. Skipping steps is a violation.

### Stage Gates

For ANY non-trivial work, progress through stages in order:

1. **DOCUMENT** — Understand first. Read existing code/pages. Log user directives verbatim in raw/notes/. Create/update wiki pages documenting what you learned. Do NOT write implementation code.
2. **DESIGN** — Decide. If the work needs a design, brainstorm with the user. Present options. Get approval. Do NOT skip to implementation.
3. **SCAFFOLD** — Create the skeleton only. Templates, directory structure, schema changes, empty files. Do NOT implement logic.
4. **IMPLEMENT** — Build on the scaffold. Follow the design. Run validation after.
5. **TEST** — Verify. Run `pipeline post`, validate, check results. Do NOT claim done without evidence.

### Rules

- **NEVER skip stages.** Document before design. Design before scaffold. Scaffold before implement.
- **NEVER write a spec without completing the brainstorm.** Brainstorm = ask questions → propose approaches → present design sections → get approval on EACH section. Only THEN write the spec.
- **NEVER rush.** If the user says "get started" or "process this," it means the CURRENT stage, not "skip to the end."
- **ALWAYS log user directives verbatim** in raw/notes/ BEFORE acting on them. This is core methodology.
- **ALWAYS read full files** before synthesizing. Check `wc -l` first. Use multiple offset reads for files >200 lines. Wiki page must be ≥0.25 ratio to raw file length.
- **ALWAYS verify depth.** When ingesting a source that DESCRIBES a format/tool/pattern, reading the description is Layer 0 (surface). You MUST examine a real INSTANCE of the thing (Layer 1) before synthesizing. A README about DESIGN.md files ≠ understanding DESIGN.md — download and read an actual one. A repo description ≠ understanding the code — read the actual files.
- **ALWAYS research before brainstorming.** Check existing wiki pages, ecosystem projects, and online sources FIRST. Then brainstorm.
- **TWO TRACKS coexist:**
  - Execution track (superpowers): brainstorm → spec → plan → sub-agent implementation. Lives in docs/superpowers/.
  - PM/observability track (backlog): epics → modules → tasks with stage gates. Lives in wiki/backlog/.
  - These are DIFFERENT concerns. Do not conflate them.

### Per-Scale Artifact Requirements

| Scale | Required Before Work |
|-------|---------------------|
| Epic | Directive log → research → spec → design → plan → per-module breakdown |
| Module | Design (or section of epic design) → plan → per-task breakdown |
| Task | Task description (from plan) → implement → verify |
| Hotfix | Nothing — fix, test, commit |

### Quality Gates

- Every wiki page: valid frontmatter, summary ≥30 words, ≥1 relationship, passes `pipeline post`
- Every evolved page: ≥0.25 ratio to source material length
- Every commit: describes WHAT changed and WHY
- Every stage transition: previous stage's artifacts exist and are committed

## Conventions

- kebab-case filenames
- One concept per page
- Update existing pages rather than creating duplicates
- Domains grow organically — create new domain folders as needed
- _index.md in every domain folder, auto-maintained
- manifest.json regenerated after every wiki change
- raw/ files kept permanently for provenance
- Sources prefixed with src- in wiki/sources/
