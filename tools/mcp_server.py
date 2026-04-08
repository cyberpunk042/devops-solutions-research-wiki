"""Wiki MCP Server — exposes wiki operations as native Claude Code tools.

Any Claude Code conversation in this project can query, ingest, validate,
and analyze the wiki through MCP tool calls instead of running CLI commands.

Run: python -m tools.mcp_server
Or via .mcp.json in project root (stdio transport).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from tools.common import (
    find_wiki_pages,
    get_project_root,
    load_config,
    parse_frontmatter,
    parse_sections,
    word_count,
)
from tools.manifest import build_manifest
from tools.pipeline import (
    post_chain,
    run_gaps,
    run_crossref,
    run_mirror,
    run_sync_step,
    fetch_urls,
    fetch_topic,
    scan_project,
    group_fetch,
    pipeline_status,
)
from tools.integrations import (
    obsidian,
    notebooklm,
    status_report as integrations_status,
)

# ---------------------------------------------------------------------------
# Server setup
# ---------------------------------------------------------------------------

server = FastMCP(
    name="research-wiki",
    instructions=(
        "Research wiki operations. Use these tools to query, ingest, validate, "
        "and analyze the wiki knowledge base. Run wiki_status first to understand "
        "the current state."
    ),
)

ROOT = get_project_root()
WIKI_DIR = ROOT / "wiki"
CONFIG_DIR = ROOT / "config"


# ---------------------------------------------------------------------------
# Query tools
# ---------------------------------------------------------------------------

@server.tool()
def wiki_status() -> str:
    """Get current wiki stats: page count, raw files, domain breakdown."""
    status = pipeline_status(ROOT)
    # Add domain breakdown
    manifest_path = WIKI_DIR / "manifest.json"
    domains = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        for dname, dinfo in manifest.get("domains", {}).items():
            domains[dname] = dinfo.get("page_count", 0)

    return json.dumps({
        "wiki_pages": status["wiki_pages"],
        "raw_files": status["raw_files"],
        "raw_by_type": status["raw_by_type"],
        "domains": domains,
    }, indent=2)


@server.tool()
def wiki_search(query: str) -> str:
    """Search wiki pages for a query string. Returns matching file paths and titles."""
    results = []
    for page in find_wiki_pages(WIKI_DIR):
        text = page.read_text(encoding="utf-8", errors="ignore")
        if query.lower() in text.lower():
            meta, _ = parse_frontmatter(text)
            results.append({
                "title": meta.get("title", page.stem),
                "path": str(page.relative_to(ROOT)),
                "domain": meta.get("domain", ""),
                "type": meta.get("type", ""),
            })

    return json.dumps({"query": query, "matches": len(results), "results": results}, indent=2)


@server.tool()
def wiki_read_page(page_path: str) -> str:
    """Read a wiki page by its path (e.g., 'wiki/domains/ai-agents/openfleet.md')."""
    full_path = ROOT / page_path
    if not full_path.exists():
        return json.dumps({"error": f"Page not found: {page_path}"})

    text = full_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    sections = parse_sections(body)

    return json.dumps({
        "path": page_path,
        "frontmatter": meta,
        "sections": {k: v[:500] + "..." if len(v) > 500 else v for k, v in sections.items()},
    }, indent=2, default=str)


@server.tool()
def wiki_list_pages(domain: str = None) -> str:
    """List all wiki pages, optionally filtered by domain."""
    pages = []
    for page in find_wiki_pages(WIKI_DIR):
        text = page.read_text(encoding="utf-8", errors="ignore")
        meta, _ = parse_frontmatter(text)
        if not meta:
            continue
        if domain and meta.get("domain") != domain:
            continue
        pages.append({
            "title": meta.get("title", page.stem),
            "path": str(page.relative_to(ROOT)),
            "domain": meta.get("domain", ""),
            "type": meta.get("type", ""),
            "status": meta.get("status", ""),
            "confidence": meta.get("confidence", ""),
        })

    return json.dumps({"count": len(pages), "pages": pages}, indent=2)


# ---------------------------------------------------------------------------
# Pipeline tools
# ---------------------------------------------------------------------------

@server.tool()
def wiki_post() -> str:
    """Run the post-ingestion chain: rebuild indexes, manifest, validate, wikilinks, lint."""
    report = post_chain(ROOT, verbose=False)
    return json.dumps(report, indent=2, default=str)


@server.tool()
def wiki_fetch(urls: str) -> str:
    """Fetch one or more URLs into raw/ for processing. Comma-separated."""
    url_list = [u.strip() for u in urls.split(",") if u.strip()]
    results = group_fetch(url_list, ROOT, verbose=False)
    return json.dumps(results, indent=2, default=str)


@server.tool()
def wiki_fetch_topic(topic: str) -> str:
    """Queue a research topic for processing."""
    results = fetch_topic(topic, ROOT, verbose=False)
    return json.dumps(results, indent=2, default=str)


@server.tool()
def wiki_scan_project(project_path: str) -> str:
    """Scan a local project and copy key docs to raw/."""
    results = scan_project(Path(project_path), ROOT, verbose=False)
    return json.dumps(results, indent=2, default=str)


# ---------------------------------------------------------------------------
# Analysis tools
# ---------------------------------------------------------------------------

@server.tool()
def wiki_gaps() -> str:
    """Run gap analysis: orphaned targets, thin pages, weak domains, open questions."""
    report = run_gaps(ROOT, verbose=False)
    # Trim open_questions to top 20 for context efficiency
    if len(report.get("open_questions", [])) > 20:
        report["open_questions"] = report["open_questions"][:20]
        report["open_questions_total"] = len(report["open_questions"])
    return json.dumps(report, indent=2, default=str)


@server.tool()
def wiki_crossref() -> str:
    """Run cross-reference analysis: missing backlinks, domain bridges, comparison candidates."""
    report = run_crossref(ROOT, verbose=False)
    return json.dumps(report, indent=2, default=str)


# ---------------------------------------------------------------------------
# Integration tools
# ---------------------------------------------------------------------------

@server.tool()
def wiki_sync() -> str:
    """Sync wiki to Windows for Obsidian."""
    result = run_sync_step(ROOT, verbose=False)
    return json.dumps(result, indent=2, default=str)


@server.tool()
def wiki_mirror_to_notebooklm(notebook_name: str = "Research Wiki Sources") -> str:
    """Push wiki source URLs to a NotebookLM notebook."""
    result = run_mirror(ROOT, notebook_name=notebook_name, verbose=False)
    return json.dumps(result, indent=2, default=str)


@server.tool()
def wiki_integrations() -> str:
    """Check availability of external integrations (Obsidian CLI, notebooklm-py)."""
    report = integrations_status()
    return json.dumps(report, indent=2, default=str)


@server.tool()
def wiki_continue() -> str:
    """Resume the wiki mission. Runs: post-chain, evolve review, evolve score, gaps, crossref. Returns full mission state."""
    root = get_project_root()
    report = {}

    # Post-chain
    post_result = post_chain(root, verbose=False)
    report["post"] = {
        "pages": post_result["steps"].get("manifest", {}).get("pages", 0),
        "relationships": post_result["steps"].get("manifest", {}).get("relationships", 0),
        "validation_errors": post_result["steps"].get("validate", {}).get("errors", 0),
    }

    # Evolve review
    from tools.evolve import review_seeds, detect_stale, score_candidates
    review = review_seeds(root, verbose=False)
    stale = detect_stale(root, verbose=False)
    report["review"] = {
        "promotable": len(review.get("promotable", [])),
        "stale": len(stale.get("stale", [])),
    }

    # Score candidates
    candidates = score_candidates(root, top=10)
    report["candidates"] = [
        {"title": c.title, "type": c.type, "score": round(c.score, 3)}
        for c in candidates
    ]

    # Gaps
    gaps = run_gaps(root, verbose=False)
    report["gaps"] = {
        "orphaned_targets": len(gaps.get("orphaned_targets", [])),
        "thin_pages": len(gaps.get("thin_pages", [])),
        "weak_domains": len(gaps.get("weak_domains", [])),
        "open_questions": len(gaps.get("open_questions", [])),
    }

    # Crossref
    crossref = run_crossref(root, verbose=False)
    report["crossref"] = {
        "missing_backlinks": len(crossref.get("missing_backlinks", [])),
        "potential_comparisons": len(crossref.get("potential_comparisons", [])),
    }

    return json.dumps(report, indent=2, default=str)


@server.tool()
def wiki_evolve(mode: str = "score", top: int = 10, type_filter: str = None) -> str:
    """Run the evolution pipeline. Modes: score, scaffold, dry-run, review, stale."""
    from tools.evolve import evolve as run_evolve
    root = get_project_root()
    result = run_evolve(root, mode=mode, top=top, type_filter=type_filter, verbose=False)
    return json.dumps(result, indent=2, default=str)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main():
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
