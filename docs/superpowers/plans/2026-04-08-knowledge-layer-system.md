# Knowledge Layer System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add layers 4-6 (lessons, patterns, decisions) and a strategic spine to the wiki, with templates, schema enforcement, pipeline scaffolding, and manifest indexing.

**Architecture:** Extend config/schema.yaml with 6 new page types and their validation rules. Create templates in config/templates/. Update tools (validate, manifest, pipeline, stats, common, obsidian) to handle new types. Scaffold directory structure. Create first evolved pages to prove the system works.

**Tech Stack:** Python 3.11, PyYAML, existing tool framework

---

### Task 1: Schema Extension

**Files:**
- Modify: `config/schema.yaml`
- Modify: `tests/fixtures/test-schema.yaml`

- [ ] **Step 1: Add new page types to schema.yaml enums.type**

Add to the `type` enum list in `config/schema.yaml`:

```yaml
  type:
    - concept
    - source-synthesis
    - comparison
    - reference
    - deep-dive
    - index
    - lesson
    - pattern
    - decision
    - domain-overview
    - learning-path
    - evolution
```

- [ ] **Step 2: Add new required_sections per type**

Add after the existing `index: []` entry:

```yaml
  lesson:
    - Summary
    - Context
    - Insight
    - Evidence
    - Applicability
    - Relationships
  pattern:
    - Summary
    - Pattern Description
    - Instances
    - When To Apply
    - When Not To
    - Relationships
  decision:
    - Summary
    - Decision
    - Alternatives
    - Rationale
    - Reversibility
    - Dependencies
    - Relationships
  domain-overview:
    - Summary
    - State of Knowledge
    - Maturity Map
    - Gaps
    - Priorities
    - Key Pages
    - Relationships
  learning-path:
    - Summary
    - Prerequisites
    - Sequence
    - Outcomes
    - Relationships
  evolution:
    - Summary
    - Timeline
    - Key Shifts
    - Current State
    - Relationships
```

- [ ] **Step 3: Add new optional fields and enums**

Add to `optional_fields`:

```yaml
optional_fields:
  - subdomain
  - aliases
  - complexity
  - resolution
  - layer
  - derived_from
  - maturity
  - instances
  - reversibility
```

Add new enums:

```yaml
  maturity:
    - seed
    - growing
    - mature
    - canonical
  reversibility:
    - easy
    - moderate
    - hard
    - irreversible
```

- [ ] **Step 4: Mirror changes to test-schema.yaml**

Apply the same additions to `tests/fixtures/test-schema.yaml`.

- [ ] **Step 5: Verify schema loads**

Run: `.venv/bin/python -c "from tools.common import load_config; s = load_config(__import__('pathlib').Path('config/schema.yaml')); print(f'Types: {len(s[\"enums\"][\"type\"])}'); print(f'Sections: {len(s[\"required_sections\"])}')"`

Expected: `Types: 12` and `Sections: 12`

- [ ] **Step 6: Commit**

```bash
git add config/schema.yaml tests/fixtures/test-schema.yaml
git commit -m "feat: extend schema with lesson, pattern, decision, spine page types"
```

---

### Task 2: Page Templates

**Files:**
- Create: `config/templates/lesson.md`
- Create: `config/templates/pattern.md`
- Create: `config/templates/decision.md`
- Create: `config/templates/domain-overview.md`
- Create: `config/templates/learning-path.md`
- Create: `config/templates/evolution.md`

- [ ] **Step 1: Create lesson template**

Create `config/templates/lesson.md`:

```markdown
---
title: "{{title}}"
type: lesson
domain: {{domain}}
layer: 4
status: synthesized
confidence: medium
maturity: seed
derived_from:
  - "{{derived_page_1}}"
created: {{date}}
updated: {{date}}
sources: []
tags: []
---

# {{title}}

## Summary

<!-- 2-3 sentences: the lesson stated clearly -->

## Context

<!-- When and where does this lesson apply? What situation triggers it? -->

## Insight

<!-- The core learning. Min 50 words. State it plainly. -->

## Evidence

<!-- Specific examples from derived_from pages. Quote or reference directly. -->

## Applicability

<!-- Which domains, projects, situations benefit from this lesson? -->

## Relationships

- DERIVED FROM: {{derived_page_1}}
```

- [ ] **Step 2: Create pattern template**

Create `config/templates/pattern.md`:

```markdown
---
title: "{{title}}"
type: pattern
domain: cross-domain
layer: 5
status: synthesized
confidence: medium
maturity: seed
derived_from:
  - "{{derived_page_1}}"
  - "{{derived_page_2}}"
instances:
  - page: "{{instance_1}}"
    context: "{{how_instance_1_shows_this_pattern}}"
  - page: "{{instance_2}}"
    context: "{{how_instance_2_shows_this_pattern}}"
created: {{date}}
updated: {{date}}
sources: []
tags: []
---

# {{title}}

## Summary

<!-- 2-3 sentences: what recurs and why it matters -->

## Pattern Description

<!-- What is this pattern? How do you recognize it? Min 100 words. -->

## Instances

<!-- 2+ specific examples from the wiki. Reference pages directly. -->

## When To Apply

<!-- Conditions that make this pattern appropriate -->

## When Not To

<!-- Anti-patterns, conditions where this fails or is counterproductive -->

## Relationships

- DERIVED FROM: {{derived_page_1}}
- DERIVED FROM: {{derived_page_2}}
```

- [ ] **Step 3: Create decision template**

Create `config/templates/decision.md`:

```markdown
---
title: "Decision: {{title}}"
type: decision
domain: {{domain}}
layer: 6
status: synthesized
confidence: medium
maturity: seed
derived_from:
  - "{{derived_page_1}}"
reversibility: moderate
created: {{date}}
updated: {{date}}
sources: []
tags: []
---

# Decision: {{title}}

## Summary

<!-- 2-3 sentences: the decision and recommendation -->

## Decision

<!-- Clear statement of what to do -->

## Alternatives

<!-- What else was considered. Min 2 alternatives with brief rationale for rejection. -->

## Rationale

<!-- Why this choice. Backed by evidence from derived_from pages. Min 100 words. -->

## Reversibility

<!-- How hard to undo. What changes downstream if reversed. -->

## Dependencies

<!-- What this decision affects. Other decisions, systems, or pages impacted. -->

## Relationships

- DERIVED FROM: {{derived_page_1}}
```

- [ ] **Step 4: Create domain-overview template**

Create `config/templates/domain-overview.md`:

```markdown
---
title: "{{domain_name}} — Domain Overview"
type: domain-overview
domain: {{domain}}
layer: spine
status: synthesized
confidence: medium
maturity: seed
created: {{date}}
updated: {{date}}
sources: []
tags: []
---

# {{domain_name}} — Domain Overview

## Summary

<!-- Domain scope and current knowledge state -->

## State of Knowledge

<!-- What we know well. What's thin. What's authoritative vs speculative. -->

## Maturity Map

<!-- Pages grouped by maturity: seed, growing, mature, canonical -->

## Gaps

<!-- What's missing. Topics mentioned but not covered. Open questions aggregated. -->

## Priorities

<!-- Ordered list of next research targets for this domain -->

## Key Pages

<!-- The essential reading list for this domain, in recommended order -->

## Relationships

- RELATES TO: {{related_domain_1}}
```

- [ ] **Step 5: Create learning-path template**

Create `config/templates/learning-path.md`:

```markdown
---
title: "Learning Path: {{title}}"
type: learning-path
layer: spine
status: synthesized
confidence: medium
maturity: seed
created: {{date}}
updated: {{date}}
sources: []
tags: []
---

# Learning Path: {{title}}

## Summary

<!-- What you'll learn and why it matters -->

## Prerequisites

<!-- What to read or know before starting this path -->

## Sequence

<!-- Ordered list of pages. Each entry: page title + 1-sentence annotation -->

## Outcomes

<!-- What you should understand after completing this path -->

## Relationships

- RELATES TO: {{related_page_1}}
```

- [ ] **Step 6: Create evolution template**

Create `config/templates/evolution.md`:

```markdown
---
title: "Evolution: {{concept}}"
type: evolution
layer: spine
status: synthesized
confidence: medium
maturity: seed
created: {{date}}
updated: {{date}}
sources: []
tags: []
---

# Evolution: {{concept}}

## Summary

<!-- What evolved and where it stands now -->

## Timeline

<!-- Chronological entries. Format: **YYYY-MM** — event (significance) -->

## Key Shifts

<!-- Turning points that changed direction or understanding -->

## Current State

<!-- Where this concept/decision stands today -->

## Relationships

- RELATES TO: {{related_page_1}}
```

- [ ] **Step 7: Commit**

```bash
git add config/templates/
git commit -m "feat: add page templates for lessons, patterns, decisions, spine"
```

---

### Task 3: Directory Scaffolding

**Files:**
- Create: `wiki/lessons/_index.md`
- Create: `wiki/patterns/_index.md`
- Create: `wiki/decisions/_index.md`
- Create: `wiki/spine/_index.md`
- Create: `wiki/spine/domain-overviews/.gitkeep`
- Create: `wiki/spine/learning-paths/.gitkeep`
- Create: `wiki/spine/evolution-log/.gitkeep`

- [ ] **Step 1: Create directory structure and index files**

```bash
mkdir -p wiki/lessons wiki/patterns wiki/decisions wiki/spine/domain-overviews wiki/spine/learning-paths wiki/spine/evolution-log
```

Create `wiki/lessons/_index.md`:

```markdown
# Lessons

Structured insights distilled from source-derived knowledge (Layer 4)

## Pages

<!-- Auto-maintained by pipeline -->

## Tags

<!-- Auto-maintained by pipeline -->
```

Create `wiki/patterns/_index.md`:

```markdown
# Patterns

Recurring structures observed across multiple sources and concepts (Layer 5)

## Pages

<!-- Auto-maintained by pipeline -->

## Tags

<!-- Auto-maintained by pipeline -->
```

Create `wiki/decisions/_index.md`:

```markdown
# Decisions

Actionable choice frameworks with explicit tradeoffs (Layer 6)

## Pages

<!-- Auto-maintained by pipeline -->

## Tags

<!-- Auto-maintained by pipeline -->
```

Create `wiki/spine/_index.md`:

```markdown
# Spine

Strategic architecture of the knowledge base — domain overviews, learning paths, evolution tracking

## Domain Overviews

<!-- Links to spine/domain-overviews/ pages -->

## Learning Paths

<!-- Links to spine/learning-paths/ pages -->

## Evolution Log

<!-- Links to spine/evolution-log/ pages -->
```

Create `.gitkeep` files in empty spine subdirectories.

- [ ] **Step 2: Commit**

```bash
git add wiki/lessons/ wiki/patterns/ wiki/decisions/ wiki/spine/
git commit -m "feat: scaffold knowledge layer directories (lessons, patterns, decisions, spine)"
```

---

### Task 4: Manifest Extension

**Files:**
- Modify: `tools/manifest.py:100-154`

- [ ] **Step 1: Add layer and maturity to page records**

In `build_manifest()`, after line 87 where `sources` is extracted, add:

```python
        layer = meta.get("layer", "")
        maturity = meta.get("maturity", "")
        derived_from = meta.get("derived_from", []) or []
```

Add these to the `page_record` dict after `"sources"`:

```python
            "layer": layer,
            "maturity": maturity,
            "derived_from": derived_from,
```

- [ ] **Step 2: Add layer and maturity stats**

After the existing `stats` dict (around line 154), add layer and maturity counting:

```python
    # Layer stats
    layer_counts: Dict[str, int] = {}
    maturity_counts: Dict[str, int] = {}
    for p in pages_meta:
        l = str(p.get("layer", ""))
        if l:
            layer_counts[l] = layer_counts.get(l, 0) + 1
        m = p.get("maturity", "")
        if m:
            maturity_counts[m] = maturity_counts.get(m, 0) + 1

    stats["layers"] = layer_counts
    stats["maturity"] = maturity_counts
```

- [ ] **Step 3: Verify manifest builds with new fields**

Run: `.venv/bin/python -m tools.manifest -o wiki/manifest.json`

Expected: manifest includes `layers` and `maturity` in stats (both empty for now since no pages have these fields yet).

- [ ] **Step 4: Commit**

```bash
git add tools/manifest.py
git commit -m "feat: manifest indexes layer and maturity fields"
```

---

### Task 5: Validate Extension

**Files:**
- Modify: `tools/validate.py:109-154`

- [ ] **Step 1: Add derived_from validation**

After the existing relationship checking (around line 144), add:

```python
    # Check derived_from references (for lesson/pattern/decision types)
    derived_types = {"lesson", "pattern", "decision"}
    if page_type in derived_types:
        derived_from = meta.get("derived_from", [])
        if not derived_from:
            warnings.append({
                "code": "missing_derived_from",
                "message": f"Type '{page_type}' should have derived_from field listing source pages",
            })

    # Check maturity enum if present
    maturity = meta.get("maturity")
    if maturity and maturity not in enums.get("maturity", []):
        errors.append({
            "code": "invalid_enum",
            "message": f"Invalid maturity value: '{maturity}' (allowed: {enums.get('maturity', [])})",
            "field": "maturity",
        })

    # Check reversibility enum if present
    reversibility = meta.get("reversibility")
    if reversibility and reversibility not in enums.get("reversibility", []):
        errors.append({
            "code": "invalid_enum",
            "message": f"Invalid reversibility value: '{reversibility}' (allowed: {enums.get('reversibility', [])})",
            "field": "reversibility",
        })
```

- [ ] **Step 2: Verify validation passes on existing pages**

Run: `.venv/bin/python -m tools.validate wiki/domains/`

Expected: `PASS: 27 files, 0 errors, 0 warnings`

- [ ] **Step 3: Commit**

```bash
git add tools/validate.py
git commit -m "feat: validate derived_from, maturity, reversibility for evolved page types"
```

---

### Task 6: Pipeline Scaffold Command

**Files:**
- Modify: `tools/pipeline.py`

- [ ] **Step 1: Add scaffold function**

Add after the existing integration step functions, before the `CHAINS` dict:

```python
def scaffold_page(page_type: str, title: str, project_root: Path,
                  domain: str = None, derived_from: List[str] = None,
                  verbose: bool = True) -> Dict[str, Any]:
    """Create a new page from template. Returns {ok, path, error}."""
    template_dir = project_root / "config" / "templates"
    template_path = template_dir / f"{page_type}.md"

    if not template_path.exists():
        return {"ok": False, "error": f"No template for type: {page_type}"}

    template = template_path.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "-").replace(":", "")[:80].strip("-")

    # Determine output directory
    type_dirs = {
        "lesson": "wiki/lessons",
        "pattern": "wiki/patterns",
        "decision": "wiki/decisions",
        "domain-overview": "wiki/spine/domain-overviews",
        "learning-path": "wiki/spine/learning-paths",
        "evolution": "wiki/spine/evolution-log",
    }
    out_dir = project_root / type_dirs.get(page_type, "wiki")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.md"

    if out_path.exists():
        return {"ok": False, "error": f"Page already exists: {out_path.relative_to(project_root)}"}

    # Fill template placeholders
    content = template
    content = content.replace("{{title}}", title)
    content = content.replace("{{date}}", today)
    content = content.replace("{{domain}}", domain or "cross-domain")
    content = content.replace("{{domain_name}}", (domain or "cross-domain").replace("-", " ").title())
    content = content.replace("{{concept}}", title)

    if derived_from:
        content = content.replace("{{derived_page_1}}", derived_from[0])
        if len(derived_from) > 1:
            content = content.replace("{{derived_page_2}}", derived_from[1])
    
    out_path.write_text(content, encoding="utf-8")

    if verbose:
        print(f"  Scaffolded: {out_path.relative_to(project_root)}")

    return {"ok": True, "path": str(out_path.relative_to(project_root))}
```

- [ ] **Step 2: Add scaffold CLI command**

Add `"scaffold"` to the `choices` list in the argument parser. Add handler:

```python
    elif args.command == "scaffold":
        if len(args.args) < 2:
            print("Usage: pipeline scaffold <type> <title> [--domain DOMAIN] [--derived PAGE1,PAGE2]")
            sys.exit(1)
        page_type = args.args[0]
        title = " ".join(args.args[1:])
        derived = args.batch.split(",") if args.batch else None
        result = scaffold_page(page_type, title, root,
                               domain=args.topic, derived_from=derived,
                               verbose=verbose)
        if args.json:
            print(json.dumps(result, indent=2))
        if not result["ok"]:
            print(f"ERROR: {result['error']}")
            sys.exit(1)
        sys.exit(0)
```

- [ ] **Step 3: Add evolve and spine-refresh chains**

Add to the `CHAINS` dict:

```python
    "evolve": {
        "description": "Gaps → scaffold lesson candidates → post-chain",
        "steps": ["gaps", "post"],
        "needs_input": False,
    },
    "spine-refresh": {
        "description": "Rebuild domain overviews → post-chain",
        "steps": ["post"],
        "needs_input": False,
    },
```

- [ ] **Step 4: Test scaffold command**

Run: `.venv/bin/python -m tools.pipeline scaffold lesson "CLI Tools Beat MCP for Token Efficiency" --topic ai-agents --batch "Harness Engineering,Claude Code Best Practices"`

Expected: Creates `wiki/lessons/cli-tools-beat-mcp-for-token-efficiency.md` from template with placeholders filled.

- [ ] **Step 5: Validate the scaffolded page**

Run: `.venv/bin/python -m tools.validate wiki/lessons/cli-tools-beat-mcp-for-token-efficiency.md`

Expected: Warnings about placeholder content but no errors on structure.

- [ ] **Step 6: Delete the test page (it was just a test)**

```bash
rm wiki/lessons/cli-tools-beat-mcp-for-token-efficiency.md
```

- [ ] **Step 7: Commit**

```bash
git add tools/pipeline.py
git commit -m "feat: pipeline scaffold command + evolve/spine-refresh chains"
```

---

### Task 7: Common Utilities Extension

**Files:**
- Modify: `tools/common.py`

- [ ] **Step 1: Add rebuild_layer_index function**

Add after `rebuild_domain_index()`:

```python
def rebuild_layer_index(layer_dir: Path, layer_name: str, description: str) -> str:
    """Rebuild a layer _index.md (lessons/, patterns/, decisions/, spine/).

    Same logic as rebuild_domain_index but for non-domain directories.
    """
    return rebuild_domain_index(layer_dir, layer_name, description)
```

- [ ] **Step 2: Commit**

```bash
git add tools/common.py
git commit -m "feat: add rebuild_layer_index utility"
```

---

### Task 8: Stats Extension

**Files:**
- Modify: `tools/stats.py`

- [ ] **Step 1: Add layer and maturity reporting**

In the `build_stats()` or main reporting section, add after existing stats output:

```python
    # Layer distribution
    layer_counts = {}
    maturity_counts = {}
    for page in pages:
        text = page.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        layer = str(meta.get("layer", ""))
        maturity = meta.get("maturity", "")
        if layer:
            layer_counts[layer] = layer_counts.get(layer, 0) + 1
        if maturity:
            maturity_counts[maturity] = maturity_counts.get(maturity, 0) + 1

    if layer_counts:
        print(f"\nBy layer: {json.dumps(layer_counts, indent=2)}")
    if maturity_counts:
        print(f"\nBy maturity: {json.dumps(maturity_counts, indent=2)}")
```

- [ ] **Step 2: Commit**

```bash
git add tools/stats.py
git commit -m "feat: stats reports layer and maturity distribution"
```

---

### Task 9: Obsidian Graph Colors

**Files:**
- Modify: `tools/setup.py` (the `configure_obsidian` function)

- [ ] **Step 1: Add color groups for new directories**

In `configure_obsidian()`, add to the `colorGroups` list in `graph_config`:

```python
            {"query": "path:lessons", "color": {"a": 1, "rgb": 3394611}},
            {"query": "path:patterns", "color": {"a": 1, "rgb": 3381759}},
            {"query": "path:decisions", "color": {"a": 1, "rgb": 16744448}},
            {"query": "path:spine", "color": {"a": 1, "rgb": 16766720}},
```

- [ ] **Step 2: Commit**

```bash
git add tools/setup.py
git commit -m "feat: obsidian graph colors for lessons/patterns/decisions/spine"
```

---

### Task 10: Update CLAUDE.md and Pipeline Post-Chain

**Files:**
- Modify: `CLAUDE.md`
- Modify: `tools/pipeline.py` (rebuild_all_indexes function)

- [ ] **Step 1: Update CLAUDE.md page types and layer descriptions**

Add after `Page types:` line:

```
Layer 1-3 (source-derived): concept, source-synthesis, comparison, reference, deep-dive, index
Layer 4-6 (evolved): lesson, pattern, decision
Spine: domain-overview, learning-path, evolution
```

Add new maturity lifecycle:

```
Maturity lifecycle: seed → growing → mature → canonical
```

Add scaffold command to pipeline section:

```
- `python -m tools.pipeline scaffold <type> <title>` — Create page from template
```

- [ ] **Step 2: Update post-chain to rebuild layer indexes**

In `rebuild_all_indexes()` in pipeline.py, add after the domain loop:

```python
    # Rebuild layer indexes (lessons, patterns, decisions)
    layer_dirs = {
        "lessons": "Structured insights distilled from source-derived knowledge (Layer 4)",
        "patterns": "Recurring structures observed across multiple sources and concepts (Layer 5)",
        "decisions": "Actionable choice frameworks with explicit tradeoffs (Layer 6)",
    }
    for layer_name, desc in layer_dirs.items():
        layer_dir = wiki_dir / layer_name
        if layer_dir.exists() and any(layer_dir.glob("*.md")):
            content = rebuild_domain_index(layer_dir, layer_name, desc)
            index_path = layer_dir / "_index.md"
            old = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
            if content != old:
                index_path.write_text(content, encoding="utf-8")
                updated += 1
```

- [ ] **Step 3: Run full health chain to verify**

Run: `.venv/bin/python -m tools.pipeline chain health`

Expected: PASS, no new errors.

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md tools/pipeline.py
git commit -m "feat: update CLAUDE.md and post-chain for knowledge layer system"
```

---

### Task 11: Create First Evolved Pages

**Files:**
- Create: 2-3 lesson pages in `wiki/lessons/`
- Create: 1 pattern page in `wiki/patterns/`
- Create: 1 decision page in `wiki/decisions/`

- [ ] **Step 1: Scaffold and fill first lesson — CLI over MCP**

Run: `.venv/bin/python -m tools.pipeline scaffold lesson "CLI Tools Beat MCP for Token Efficiency"`

Then fill in the scaffolded page with real content from the wiki's existing insights (Harness Engineering, Claude Code Accuracy Tips, Claude Code Best Practices all converge on this).

- [ ] **Step 2: Scaffold and fill second lesson — Plan Execute Review**

Run: `.venv/bin/python -m tools.pipeline scaffold lesson "Always Plan Before Executing"`

Fill from: Harness Engineering, OpenFleet, superpowers workflow, wiki-agent skill.

- [ ] **Step 3: Scaffold and fill pattern — Plan Execute Review Cycle**

Run: `.venv/bin/python -m tools.pipeline scaffold pattern "Plan Execute Review Cycle"`

Fill from: OpenFleet (deterministic brain), Harness Engineering (5-verb), superpowers (brainstorm→plan→execute→verify), wiki pipeline (extract→analyze→synthesize→write→integrate).

- [ ] **Step 4: Scaffold and fill decision — MCP vs CLI for Tool Integration**

Run: `.venv/bin/python -m tools.pipeline scaffold decision "MCP vs CLI for Tool Integration"`

Fill from: Harness Engineering CLI>MCP analysis, Claude Code Accuracy Tips, existing MCP server design.

- [ ] **Step 5: Run post-chain**

Run: `.venv/bin/python -m tools.pipeline chain publish`

Expected: indexes rebuilt (lessons, patterns, decisions should now have pages), manifest updated with layer/maturity stats, sync to Windows.

- [ ] **Step 6: Verify layer stats**

Run: `.venv/bin/python -m tools.stats`

Expected: `By layer: {"4": 2, "5": 1, "6": 1}` and `By maturity: {"seed": 4}`

- [ ] **Step 7: Commit**

```bash
git add wiki/lessons/ wiki/patterns/ wiki/decisions/
git commit -m "feat: first evolved pages — 2 lessons, 1 pattern, 1 decision"
```

---

### Task 12: Final Verification

- [ ] **Step 1: Full health chain**

Run: `.venv/bin/python -m tools.pipeline chain health`

Verify: 0 validation errors, layer stats present, no new dead relationships.

- [ ] **Step 2: Verify scaffold roundtrip**

Run: `.venv/bin/python -m tools.pipeline scaffold evolution "LLM Wiki Pattern"`

Verify: creates `wiki/spine/evolution-log/llm-wiki-pattern.md` from template.

```bash
rm wiki/spine/evolution-log/llm-wiki-pattern.md
```

- [ ] **Step 3: Update session artifact**

Update `docs/SESSION-2026-04-08.md` with Phase 7 knowledge layer system work.

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "feat: knowledge layer system — lessons, patterns, decisions, spine"
```
