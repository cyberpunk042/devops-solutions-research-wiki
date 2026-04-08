# Setup Scripts + Obsidian + NotebookLM — Design Specification

**Date:** 2026-04-08
**Status:** Draft
**Author:** jfortin + Claude Code
**Depends on:** `docs/superpowers/specs/2026-04-08-research-wiki-design.md`

---

## 1. Overview

### 1.1 What This Is

A modular setup script system that installs, configures, and wires together:
- **Obsidian** as the visual frontend for the wiki (graph view, backlinks, navigation)
- **NotebookLM** prep for future querying and multimedia summaries
- **Sister project export** directories for openfleet and AICP
- **Python dependencies** and system packages

Plus a new `tools/obsidian.py` that bridges the wiki's `## Relationships` format to Obsidian's `[[wikilinks]]` for graph view.

### 1.2 What This Is NOT

- Not Obsidian theming/styling (future iteration)
- Not a full NotebookLM automation pipeline (future — this is prep only)
- Not a replacement for the existing tooling (additive)

### 1.3 Goals

- One command (`./scripts/setup.sh --all`) to go from zero to working wiki vault
- Modular sub-scripts that run independently
- Obsidian graph view shows the full relationship graph with domain-colored nodes
- Sister project export paths verified and ready
- NotebookLM tooling prepped for future activation

---

## 2. Scripts Architecture

### 2.1 File Structure

```
scripts/
├── setup.sh                     # Master orchestrator
├── lib.sh                       # Shared functions
├── install-deps.sh              # Python + system deps
├── install-obsidian.sh          # Obsidian .deb download + install
├── configure-obsidian.sh        # wiki/.obsidian/ vault config
├── configure-exports.sh         # Sister project export dir setup
└── setup-notebooklm.sh          # notebooklm-py install + auth stub

tools/
└── obsidian.py                  # Wikilink generator (NEW)
```

### 2.2 `scripts/lib.sh` — Shared Functions

Sourced by all sub-scripts. Provides:

```bash
# Logging
log_info "message"               # Green [INFO] prefix
log_warn "message"               # Yellow [WARN] prefix
log_error "message"              # Red [ERROR] prefix

# Checks
check_command "binary"           # Verify command exists, log result
check_dpkg "package"             # Verify .deb package installed
check_dir "path" "label"         # Verify directory exists, warn if not

# Interaction
confirm_action "prompt"          # y/n prompt, returns 0/1. Skipped with --yes flag.

# Constants
PROJECT_ROOT                     # Auto-detected from script location (parent of scripts/)
WIKI_DIR="${PROJECT_ROOT}/wiki"
CONFIG_DIR="${PROJECT_ROOT}/config"
```

### 2.3 `scripts/setup.sh` — Master Orchestrator

```bash
Usage: ./scripts/setup.sh [OPTIONS]

Options:
  --all           Run everything
  --deps          Install Python + system dependencies
  --obsidian      Install Obsidian + configure vault + generate wikilinks
  --exports       Configure sister project export directories
  --notebooklm    Install notebooklm-py + create stub skill
  --yes           Skip confirmation prompts
  -h, --help      Show usage

With no flags: interactive mode — asks what to install.
```

Execution order when `--all`:
1. `install-deps.sh`
2. `install-obsidian.sh`
3. `configure-obsidian.sh` (includes running `tools/obsidian.py`)
4. `configure-exports.sh`
5. `setup-notebooklm.sh`

### 2.4 Sub-Script Conventions

Every sub-script:
- Sources `lib.sh` as its first action: `source "$(dirname "$0")/lib.sh"`
- Is idempotent (safe to re-run, checks before acting)
- Can run standalone: `./scripts/install-obsidian.sh`
- Exits 0 on success, 1 on failure
- Uses `log_info/warn/error` for all output
- Does NOT `set -e` globally (handles errors per-command for better logging)

---

## 3. Obsidian Integration

### 3.1 `scripts/install-obsidian.sh`

```
1. Check if obsidian is already installed (dpkg -l | grep obsidian)
   → If installed: log_info, skip, exit 0
2. Download .deb from GitHub releases
   → Version pinned via OBSIDIAN_VERSION env var (default: 1.12.7)
   → URL: https://github.com/obsidianmd/obsidian-releases/releases/download/v${OBSIDIAN_VERSION}/obsidian_${OBSIDIAN_VERSION}_amd64.deb
   → Download to /tmp/obsidian_${OBSIDIAN_VERSION}.deb
3. Install with sudo dpkg -i
4. Fix missing deps: sudo apt-get install -f -y
5. Verify: check_command obsidian
```

### 3.2 `scripts/configure-obsidian.sh`

Creates `wiki/.obsidian/` configuration. The vault root is `wiki/` (not the project root) so raw/, tools/, config/ stay out of the vault.

**Files created:**

#### `wiki/.obsidian/app.json`
```json
{
  "vimMode": false,
  "strictLineBreaks": true,
  "showFrontmatter": true,
  "foldHeading": true,
  "foldIndent": true,
  "defaultViewMode": "preview"
}
```

#### `wiki/.obsidian/appearance.json`
```json
{
  "theme": "obsidian",
  "translucency": false,
  "baseFontSize": 16
}
```

#### `wiki/.obsidian/core-plugins.json`
Enables: `graph`, `backlink`, `tag-pane`, `outgoing-links`, `search`, `file-explorer`, `page-preview`.

#### `wiki/.obsidian/graph.json`
Graph view settings with domain-based color groups:

```json
{
  "collapse-filter": false,
  "search": "",
  "showTags": false,
  "showAttachments": false,
  "hideUnresolved": false,
  "showOrphans": true,
  "collapse-color-groups": false,
  "colorGroups": [
    {"query": "path:domains/ai-agents", "color": {"a": 1, "rgb": 4886754}},
    {"query": "path:domains/knowledge-systems", "color": {"a": 1, "rgb": 2470655}},
    {"query": "path:domains/automation", "color": {"a": 1, "rgb": 16750848}},
    {"query": "path:domains/tools-and-platforms", "color": {"a": 1, "rgb": 8388352}},
    {"query": "path:sources", "color": {"a": 1, "rgb": 10066329}}
  ],
  "collapse-display": false,
  "lineSizeMultiplier": 1,
  "nodeSizeMultiplier": 1,
  "textFadeMultiplier": 0,
  "centerStrength": 0.5,
  "repelStrength": 10,
  "linkStrength": 1,
  "linkDistance": 250
}
```

Domain colors (rgb values are decimal):
- ai-agents: steel blue (4886754 = #4A86C2)
- knowledge-systems: sky blue (2470655 = #25ADFF)
- automation: orange (16750848 = #FFA500)
- tools-and-platforms: olive (8388352 = #800780)
- sources: gray (10066329 = #999999)

#### Final step
Runs `python3 tools/obsidian.py` to generate `## Backlinks` sections in all wiki pages.

### 3.3 `tools/obsidian.py` — Wikilink Generator

Bridges `## Relationships` (openfleet-compatible plain text) to `[[wikilinks]]` (Obsidian graph view).

**How it works:**
1. Reads `wiki/manifest.json` to build title → path lookup
2. For each wiki page:
   a. Parses `## Relationships` to get targets
   b. Also finds pages that reference THIS page (incoming links from manifest)
   c. Resolves targets to page titles where possible
   d. Generates a `## Backlinks` section with `[[Page Title]]` links
   e. Writes the section at the bottom of the page (after `## Relationships`)
3. If `## Backlinks` already exists, replaces it (idempotent)

**Output format in a page:**

```markdown
## Relationships

- DERIVED FROM: src-karpathy-claude-code-10x
- COMPARES TO: LLM Wiki vs RAG
- ENABLES: Wiki Ingestion Pipeline

## Backlinks

[[Synthesis - Karpathy LLM Wiki Method via Claude Code]]
[[LLM Wiki vs RAG]]
[[Wiki Ingestion Pipeline]]
[[LLM Knowledge Linting]]
[[Obsidian Knowledge Vault]]
```

**Title matching logic:**
- Direct match: relationship target == page title → `[[Page Title]]`
- Slug match: relationship target matches page filename stem (kebab-case) → resolve to full title
- Source match: `DERIVED FROM: src-xxx` → find source-synthesis page with that source ID → `[[Source Title]]`
- Unresolved: target not found → `[[Target Name]]` (Obsidian shows as unresolved link — useful for gap visibility)

**CLI:**
```bash
python3 tools/obsidian.py                  # Generate/update backlinks in all pages
python3 tools/obsidian.py --check          # Dry-run, report changes
python3 tools/obsidian.py --clean          # Remove all ## Backlinks sections
python3 tools/obsidian.py --wiki path/     # Custom wiki dir
```

**Integration with existing workflow:**
- Added to wiki-agent skill post-ingestion: after `tools/manifest.py`, run `tools/obsidian.py`
- Added to CLAUDE.md tooling section

---

## 4. Sister Project Export Wiring

### 4.1 `scripts/configure-exports.sh`

```
1. Detect sister projects:
   OPENFLEET_DIR="${PROJECT_ROOT}/../openfleet"
   AICP_DIR="${PROJECT_ROOT}/../devops-expert-local-ai"

2. For each:
   → Check if dir exists (warn if not, don't fail)
   → Create export target dir if project exists:
     openfleet: docs/knowledge-map/kb/research-wiki/
     AICP: docs/kb/research-wiki/

3. Dry-run both exports:
   python3 tools/export.py openfleet --dry
   python3 tools/export.py aicp --dry

4. Report results
```

Non-destructive. Only creates empty directories and validates the pipeline.

---

## 5. NotebookLM Prep

### 5.1 `scripts/setup-notebooklm.sh`

```
1. Attempt to install notebooklm-py:
   pip3 install notebooklm-py
   → If fails: log_warn with manual install instructions (GitHub URL)

2. Check for existing auth:
   → If ~/.notebooklm/credentials.json exists: log_info "authenticated"
   → If not: log_warn with instructions to run 'notebooklm auth'

3. Create stub skill if not present:
   → skills/notebooklm/skill.md with status "Not yet configured"
   → Lists setup steps and planned capabilities
```

The stub skill documents what the full NotebookLM skill will do once the user configures auth and obtains the full skill (from Jay's community or custom-built).

---

## 6. Updated Project Files

### 6.1 CLAUDE.md Addition

Add to the Tooling section:
```
- `python3 tools/obsidian.py` — Regenerate [[wikilinks]] for Obsidian graph view
```

Add to Post-Ingestion:
```
6. Regenerate wikilinks via tools/obsidian.py
```

### 6.2 Wiki-Agent Skill Update

Add `tools/obsidian.py` to the post-ingestion steps in `skills/wiki-agent/skill.md`:
```
Post-ingestion (every time):
1. Update affected _index.md files
2. Run: python3 tools/manifest.py
3. Run: python3 tools/validate.py
4. Run: python3 tools/obsidian.py
5. Flag stale pages needing review
6. Report summary
```

### 6.3 `.gitignore` Addition

```
# Obsidian workspace (user-specific, not portable)
wiki/.obsidian/workspace.json
wiki/.obsidian/workspace-mobile.json
```

The rest of `.obsidian/` IS committed (app.json, graph.json, etc. are project settings).

---

## 7. Dependencies

### System
- `wget` — for downloading Obsidian .deb
- `sudo` — for dpkg install

### Python (no new pip deps)
- `tools/obsidian.py` uses only `tools.common` + standard library (json, pathlib, re)

### Optional
- `notebooklm-py` — installed by setup-notebooklm.sh, not required for core functionality
