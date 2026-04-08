# Pipeline Automation — Design Spec

## Problem

After every ingestion or page edit, 6 manual commands must run:
1. Update _index.md files
2. `python3 -m tools.manifest -o wiki/manifest.json`
3. `python3 -m tools.validate`
4. `python3 -m tools.obsidian`
5. Flag stale pages
6. Report summary

Additionally, ingestion inputs (URLs, topics, local paths) require manual classification and routing. Batch operations (12 URLs at once) have no parallelism. There's no single entry point that handles "here's a list of things to research."

## Solution

`tools/pipeline.py` — a pipeline orchestrator that:
1. **Accepts any input type** (URLs, local paths, topic strings, raw file globs)
2. **Routes inputs** to the right handler (ingest.py for URLs, scan for local, web search for topics)
3. **Runs post-ingestion chain** as a single command (index → manifest → validate → obsidian → report)
4. **Supports batch execution** with parallel fetching
5. **Reports results** as structured JSON or human-readable summary

## Commands

```bash
# Post-ingestion chain (run after any wiki change)
python3 -m tools.pipeline post

# Fetch + queue for synthesis
python3 -m tools.pipeline fetch URL [URL...]
python3 -m tools.pipeline fetch --batch urls.txt
python3 -m tools.pipeline fetch --topic "LLM agent memory patterns"

# List what's ready for synthesis
python3 -m tools.pipeline status

# Full chain: fetch → report ready → (human/LLM synthesis) → post
python3 -m tools.pipeline run URL [URL...]
python3 -m tools.pipeline run --batch urls.txt

# Scan local project for documentation
python3 -m tools.pipeline scan ../openfleet/
```

## Architecture

```
pipeline.py
├── post_chain(wiki_dir)           → run all 6 post-ingestion steps
├── fetch_inputs(inputs, input_type)  → classify + fetch via ingest.py or web search
├── scan_project(project_path)     → extract docs/README/CLAUDE.md from local project
├── pipeline_status(raw_dir)       → list unprocessed raw files with metadata
├── run_pipeline(inputs, ...)      → fetch → status → post (synthesis is external)
└── CLI: post, fetch, status, run, scan
```

## Dependencies

- Reuses: tools/ingest.py (fetch), tools/manifest.py, tools/validate.py, tools/obsidian.py, tools/lint.py, tools/common.py
- New: tools/pipeline.py only
- No new packages required

## Post-Chain Steps (in order)

1. Rebuild affected _index.md files (via common.rebuild_domain_index)
2. Regenerate manifest.json
3. Run validate.py — collect errors
4. Run obsidian.py — regenerate wikilinks
5. Run lint.py — collect warnings
6. Print summary report (pages, relationships, errors, warnings)

## Input Classification

| Input | Detection | Handler |
|-------|-----------|---------|
| URL (http/https) | startswith http | ingest.py |
| Local path (exists) | os.path.exists | scan_project() |
| Raw file glob | glob match in raw/ | direct list |
| Topic string | everything else | WebSearch → ingest.py |

## Output

```json
{
  "fetched": [{"url": "...", "file": "...", "status": "ok"}],
  "ready_for_synthesis": ["raw/articles/foo.md", "raw/transcripts/bar.txt"],
  "post_chain": {
    "manifest_pages": 42,
    "validation_errors": 0,
    "validation_warnings": 1,
    "backlinks_updated": 5,
    "lint_issues": 3
  }
}
```
