"""Pipeline orchestrator for the DevOps Solutions Research Wiki.

Chains wiki tools into automated pipelines with support for chain (sequential),
group (parallel), and tree (branch/merge) operations.

Usage:
    python3 -m tools.pipeline post                    # Run post-ingestion chain
    python3 -m tools.pipeline fetch URL [URL...]      # Fetch URLs into raw/
    python3 -m tools.pipeline fetch --batch urls.txt  # Batch fetch from file
    python3 -m tools.pipeline fetch --topic "query"   # Web search → fetch
    python3 -m tools.pipeline scan ../project/        # Scan local project docs
    python3 -m tools.pipeline status                  # List raw files ready for synthesis
    python3 -m tools.pipeline run URL [URL...]        # Fetch + post-chain
    python3 -m tools.pipeline run --batch urls.txt    # Batch fetch + post-chain
    python3 -m tools.pipeline chain <name>            # Run a named chain
    python3 -m tools.pipeline chain --list            # List available chains
    python3 -m tools.pipeline gaps                    # Run gap analysis pipeline
    python3 -m tools.pipeline crossref                # Run cross-reference analysis
"""

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from tools.common import (
    find_wiki_pages,
    get_project_root,
    load_config,
    parse_frontmatter,
    parse_sections,
    parse_relationships,
    rebuild_domain_index,
    rebuild_layer_index,
    word_count,
)
from tools.ingest import ingest_url, list_raw
from tools.manifest import build_manifest
from tools.validate import validate_page
from tools.lint import lint_wiki, LintConfig
from tools.integrations import obsidian, notebooklm, status_report as integrations_status


# ---------------------------------------------------------------------------
# Post-ingestion chain
# ---------------------------------------------------------------------------

def rebuild_all_indexes(wiki_dir: Path, config_path: Path) -> int:
    """Rebuild all domain _index.md files. Returns count of domains updated."""
    domains_dir = wiki_dir / "domains"
    if not domains_dir.exists():
        return 0

    domains_config = load_config(config_path)
    domain_descriptions = {}
    if domains_config and "domains" in domains_config:
        for name, info in domains_config["domains"].items():
            domain_descriptions[name] = info.get("description", "")

    updated = 0
    for domain_dir in sorted(domains_dir.iterdir()):
        if not domain_dir.is_dir():
            continue
        name = domain_dir.name
        desc = domain_descriptions.get(name, "")
        content = rebuild_domain_index(domain_dir, name, desc)
        index_path = domain_dir / "_index.md"
        old = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
        if content != old:
            index_path.write_text(content, encoding="utf-8")
            updated += 1

    return updated


def run_manifest(wiki_dir: Path, output_path: Path) -> Dict[str, Any]:
    """Build manifest and write to file. Returns manifest data."""
    manifest = build_manifest(wiki_dir)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, default=str)
    return manifest


def run_validate(wiki_dir: Path, schema_path: Path) -> Dict[str, Any]:
    """Validate all wiki pages. Returns {errors: int, warnings: int, details: [...]}."""
    pages = find_wiki_pages(wiki_dir)
    all_errors = 0
    all_warnings = 0
    details = []

    # Skip known non-wiki files (navigation pages without frontmatter)
    skip_names = {"index.md"}

    for page in pages:
        if page.name in skip_names and page.parent == wiki_dir:
            continue
        result = validate_page(page, schema_path)
        errors = result.get("errors", [])
        warnings = result.get("warnings", [])
        if errors or warnings:
            details.append(result)
        all_errors += len(errors)
        all_warnings += len(warnings)

    return {"errors": all_errors, "warnings": all_warnings, "details": details}


def run_obsidian(project_root: Path) -> Dict[str, Any]:
    """Run obsidian.py to regenerate backlinks. Returns {updated: int, unchanged: int}."""
    result = subprocess.run(
        [sys.executable, "-m", "tools.obsidian"],
        capture_output=True, text=True, cwd=project_root,
    )
    output = result.stdout + result.stderr

    updated = 0
    unchanged = 0
    for line in output.splitlines():
        if "updated" in line.lower() and "unchanged" in line.lower():
            parts = line.split(",")
            for part in parts:
                part = part.strip()
                if "updated" in part:
                    try:
                        updated = int(part.split()[1] if part[0].isalpha() else part.split()[0])
                    except (IndexError, ValueError):
                        pass
                if "unchanged" in part:
                    try:
                        unchanged = int(part.split()[0])
                    except (IndexError, ValueError):
                        pass
            break

    return {"updated": updated, "unchanged": unchanged, "output": output.strip()}


def run_lint(wiki_dir: Path) -> Dict[str, Any]:
    """Run lint checks. Returns summary dict."""
    config = LintConfig(
        stale_threshold_days=30,
        min_summary_words=30,
        min_deep_analysis_words=100,
        min_relationships=1,
        min_domain_pages=3,
        min_cross_domain_rels=2,
        similarity_threshold=0.70,
    )
    report = lint_wiki(wiki_dir, config)
    return {
        "dead_relationships": len(report.get("dead_relationships", [])),
        "orphan_pages": len(report.get("orphan_pages", [])),
        "stale_pages": len(report.get("stale_pages", [])),
        "thin_pages": len(report.get("thin_pages", [])),
        "domain_issues": len(report.get("domain_health", [])),
        "total_issues": report.get("summary", {}).get("total_issues", 0),
    }


def post_chain(project_root: Path, verbose: bool = True) -> Dict[str, Any]:
    """Run the full post-ingestion chain. Returns structured report."""
    wiki_dir = project_root / "wiki"
    config_dir = project_root / "config"
    schema_path = config_dir / "schema.yaml"
    domains_config = config_dir / "domains.yaml"
    manifest_path = wiki_dir / "manifest.json"

    report: Dict[str, Any] = {"steps": {}, "success": True}

    # Step 1: Rebuild indexes (domain + layer)
    if verbose:
        print("  [1/6] Rebuilding domain indexes...")
    indexes_updated = rebuild_all_indexes(wiki_dir, domains_config)

    # Rebuild layer indexes
    layer_dirs = {
        "lessons": "Structured insights synthesized from sources",
        "patterns": "Recurring structures observed across sources",
        "decisions": "Actionable choice frameworks with tradeoffs",
        "spine": "Strategic architecture and domain overviews",
    }
    for layer_name, desc in layer_dirs.items():
        layer_dir = wiki_dir / layer_name
        if layer_dir.exists():
            content = rebuild_layer_index(layer_dir, layer_name, desc)
            idx = layer_dir / "_index.md"
            old = idx.read_text(encoding="utf-8") if idx.exists() else ""
            if content != old:
                idx.write_text(content, encoding="utf-8")
                indexes_updated += 1
    report["steps"]["indexes"] = {"updated": indexes_updated}

    # Step 2: Regenerate manifest
    if verbose:
        print("  [2/6] Regenerating manifest.json...")
    manifest = run_manifest(wiki_dir, manifest_path)
    pages = manifest.get("stats", {}).get("pages", 0)
    rels = manifest.get("stats", {}).get("relationships", 0)
    report["steps"]["manifest"] = {"pages": pages, "relationships": rels}

    # Step 3: Validate
    if verbose:
        print("  [3/6] Validating pages...")
    validation = run_validate(wiki_dir, schema_path)
    report["steps"]["validate"] = validation
    if validation["errors"] > 0:
        report["success"] = False

    # Step 4: Regenerate wikilinks
    if verbose:
        print("  [4/6] Regenerating wikilinks...")
    obsidian = run_obsidian(project_root)
    report["steps"]["obsidian"] = {
        "updated": obsidian["updated"],
        "unchanged": obsidian["unchanged"],
    }

    # Step 5: Lint
    if verbose:
        print("  [5/6] Running lint checks...")
    lint = run_lint(wiki_dir)
    report["steps"]["lint"] = lint

    return report


# ---------------------------------------------------------------------------
# Fetch pipeline
# ---------------------------------------------------------------------------

def fetch_urls(urls: List[str], project_root: Path, verbose: bool = True) -> List[Dict[str, Any]]:
    """Fetch multiple URLs into raw/. Returns list of results."""
    results = []
    for i, url in enumerate(urls, 1):
        if verbose:
            print(f"  [{i}/{len(urls)}] {url}")
        result = ingest_url(url, project_root)
        if verbose:
            status = result["status"]
            if status == "fetched":
                print(f"    → {result['file']}")
            elif status == "skipped":
                print(f"    → SKIP (exists)")
            else:
                print(f"    → ERROR: {result.get('error', 'unknown')}")
        results.append(result)
    return results


def fetch_topic(topic: str, project_root: Path, verbose: bool = True) -> List[Dict[str, Any]]:
    """Search web for topic, fetch top results into raw/. Returns results."""
    if verbose:
        print(f"  Searching: {topic}")

    # Use WebSearch-style approach via subprocess
    # For now, save the topic as a research note in raw/dumps/
    slug = topic.lower().replace(" ", "-")[:60]
    dump_dir = project_root / "raw" / "dumps"
    dump_dir.mkdir(parents=True, exist_ok=True)
    dump_file = dump_dir / f"topic-{slug}.md"

    if not dump_file.exists():
        content = (
            f"# Research Topic: {topic}\n\n"
            f"Queued: {datetime.now().isoformat()[:10]}\n"
            f"Status: pending\n\n"
            f"## Instructions\n\n"
            f"Research this topic online and create wiki pages from findings.\n"
            f"Use WebSearch and WebFetch to gather sources.\n"
        )
        dump_file.write_text(content, encoding="utf-8")
        if verbose:
            print(f"    → Queued: {dump_file.relative_to(project_root)}")
        return [{"topic": topic, "status": "queued", "file": str(dump_file.relative_to(project_root))}]
    else:
        if verbose:
            print(f"    → Already queued")
        return [{"topic": topic, "status": "skipped", "file": str(dump_file.relative_to(project_root))}]


def scan_project(project_path: Path, project_root: Path, verbose: bool = True) -> List[Dict[str, Any]]:
    """Scan a local project and copy key docs to raw/. Returns results."""
    project_path = project_path.resolve()
    if not project_path.exists():
        return [{"path": str(project_path), "status": "error", "error": "Path does not exist"}]

    project_name = project_path.name
    results = []

    # Key files to look for
    key_files = ["README.md", "CLAUDE.md", "AGENTS.md", "docs/architecture.md", "docs/ARCHITECTURE.md"]

    raw_dir = project_root / "raw" / "articles"
    raw_dir.mkdir(parents=True, exist_ok=True)

    for rel_path in key_files:
        src = project_path / rel_path
        if src.exists():
            slug = f"{project_name}-{rel_path.replace('/', '-').replace('.md', '').lower()}"
            dst = raw_dir / f"{slug}.md"

            if dst.exists():
                results.append({
                    "source": str(src),
                    "status": "skipped",
                    "file": str(dst.relative_to(project_root)),
                })
                if verbose:
                    print(f"    SKIP: {rel_path} (already saved)")
                continue

            content = src.read_text(encoding="utf-8", errors="ignore")
            header = (
                f"# {project_name} — {rel_path}\n\n"
                f"Source: {src}\n"
                f"Ingested: {datetime.now().isoformat()[:10]}\n"
                f"Type: documentation\n\n---\n\n"
            )
            dst.write_text(header + content, encoding="utf-8")
            results.append({
                "source": str(src),
                "status": "fetched",
                "file": str(dst.relative_to(project_root)),
            })
            if verbose:
                print(f"    OK: {rel_path} → {dst.relative_to(project_root)}")

    if not results:
        if verbose:
            print(f"    No key docs found in {project_path}")
        results.append({"path": str(project_path), "status": "empty", "error": "No key docs found"})

    return results


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def pipeline_status(project_root: Path) -> Dict[str, Any]:
    """Report what's in raw/ and wiki stats."""
    raw_files = list_raw(project_root)
    wiki_dir = project_root / "wiki"
    pages = find_wiki_pages(wiki_dir)

    # Group raw files by type
    by_type: Dict[str, int] = {}
    for f in raw_files:
        t = f["type"]
        by_type[t] = by_type.get(t, 0) + 1

    return {
        "raw_files": len(raw_files),
        "raw_by_type": by_type,
        "wiki_pages": len(pages),
        "raw_details": raw_files,
    }


# ---------------------------------------------------------------------------
# Group execution (parallel)
# ---------------------------------------------------------------------------

def group_fetch(urls: List[str], project_root: Path, max_workers: int = 4,
                verbose: bool = True) -> List[Dict[str, Any]]:
    """Fetch multiple URLs in parallel. Returns list of results."""
    results: List[Dict[str, Any]] = []
    if verbose:
        print(f"  Fetching {len(urls)} URL(s) in parallel (max {max_workers} workers)...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(ingest_url, url, project_root): url
            for url in urls
        }
        for future in as_completed(futures):
            url = futures[future]
            try:
                result = future.result()
            except Exception as e:
                result = {"url": url, "status": "error", "error": str(e),
                          "file": None, "title": None}
            results.append(result)
            if verbose:
                status = result["status"]
                if status == "fetched":
                    print(f"    OK: {result.get('title', url)[:60]}")
                elif status == "skipped":
                    print(f"    SKIP: {url[:60]}")
                else:
                    print(f"    ERROR: {url[:40]} — {result.get('error', '')[:40]}")

    return results


def group_scan(paths: List[str], project_root: Path,
               verbose: bool = True) -> List[Dict[str, Any]]:
    """Scan multiple local projects in parallel. Returns list of results."""
    all_results: List[Dict[str, Any]] = []
    if verbose:
        print(f"  Scanning {len(paths)} project(s)...")

    for path_str in paths:
        path = Path(path_str).resolve()
        if verbose:
            print(f"  [{path.name}]")
        results = scan_project(path, project_root, verbose=verbose)
        all_results.extend(results)

    return all_results


# ---------------------------------------------------------------------------
# Gap analysis pipeline
# ---------------------------------------------------------------------------

def run_gaps(project_root: Path, verbose: bool = True) -> Dict[str, Any]:
    """Analyze the wiki for gaps: thin pages, missing targets, weak domains."""
    wiki_dir = project_root / "wiki"
    manifest_path = wiki_dir / "manifest.json"

    # Ensure manifest is current
    manifest = build_manifest(wiki_dir)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, default=str)

    report: Dict[str, Any] = {
        "orphaned_targets": [],
        "thin_pages": [],
        "weak_domains": [],
        "open_questions": [],
        "disconnected_pages": [],
    }

    all_titles = {p["title"] for p in manifest["pages"]}

    # 1. Orphaned relationship targets (pages referenced but don't exist)
    for ref in manifest.get("orphaned_refs", []):
        target = ref["target"]
        # Skip src- refs (source IDs, not page titles)
        if target.startswith("src-"):
            continue
        # Skip slug-vs-title mismatches (lowercase version of existing title)
        if any(t.lower().replace(" ", "-") == target.lower().replace(" ", "-") for t in all_titles):
            continue
        report["orphaned_targets"].append(target)

    # 2. Thin pages (concepts/comparisons with short Deep Analysis)
    for page_data in manifest["pages"]:
        ptype = page_data.get("type", "")
        if ptype not in ("concept", "comparison", "deep-dive"):
            continue
        page_path = wiki_dir / page_data.get("path", "")
        if not page_path.exists():
            continue
        text = page_path.read_text(encoding="utf-8")
        _, body = parse_frontmatter(text)
        sections = parse_sections(body)
        deep = sections.get("Deep Analysis", "")
        if word_count(deep) < 100:
            report["thin_pages"].append({
                "title": page_data["title"],
                "deep_analysis_words": word_count(deep),
                "path": page_data.get("path", ""),
            })

    # 3. Weak domains (few pages or low relationship density)
    for dname, dinfo in manifest.get("domains", {}).items():
        page_count = dinfo.get("page_count", 0)
        rel_count = dinfo.get("relationship_count", 0)
        density = rel_count / max(page_count, 1)
        if page_count < 3 or density < 3.0:
            report["weak_domains"].append({
                "domain": dname,
                "pages": page_count,
                "relationships": rel_count,
                "density": round(density, 1),
            })

    # 4. Aggregate Open Questions across all pages
    for page_data in manifest["pages"]:
        page_path = wiki_dir / page_data.get("path", "")
        if not page_path.exists():
            continue
        text = page_path.read_text(encoding="utf-8")
        _, body = parse_frontmatter(text)
        sections = parse_sections(body)
        oq = sections.get("Open Questions", "")
        if oq.strip():
            questions = [l.strip().lstrip("- ") for l in oq.splitlines()
                         if l.strip().startswith("-")]
            for q in questions:
                report["open_questions"].append({
                    "question": q,
                    "source_page": page_data["title"],
                })

    # 5. Disconnected pages (< 2 outgoing relationships)
    for page_data in manifest["pages"]:
        rels = page_data.get("relationships", [])
        if len(rels) < 2 and page_data.get("type") != "source-synthesis":
            report["disconnected_pages"].append({
                "title": page_data["title"],
                "relationships": len(rels),
            })

    if verbose:
        print(f"  Gap Analysis:")
        print(f"    Orphaned targets:   {len(report['orphaned_targets'])}")
        print(f"    Thin pages:         {len(report['thin_pages'])}")
        print(f"    Weak domains:       {len(report['weak_domains'])}")
        print(f"    Open questions:     {len(report['open_questions'])}")
        print(f"    Disconnected pages: {len(report['disconnected_pages'])}")

        if report["orphaned_targets"]:
            print(f"\n  Missing pages (create these):")
            for t in report["orphaned_targets"]:
                print(f"    - {t}")

        if report["thin_pages"]:
            print(f"\n  Thin pages (deepen these):")
            for t in report["thin_pages"]:
                print(f"    - {t['title']} ({t['deep_analysis_words']} words)")

        if report["weak_domains"]:
            print(f"\n  Weak domains (expand these):")
            for d in report["weak_domains"]:
                print(f"    - {d['domain']}: {d['pages']} pages, density {d['density']}")

    return report


# ---------------------------------------------------------------------------
# Cross-reference analysis pipeline
# ---------------------------------------------------------------------------

def run_crossref(project_root: Path, verbose: bool = True) -> Dict[str, Any]:
    """Analyze relationships for missing cross-references and patterns."""
    wiki_dir = project_root / "wiki"
    manifest_path = wiki_dir / "manifest.json"

    manifest = build_manifest(wiki_dir)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, default=str)

    report: Dict[str, Any] = {
        "missing_backlinks": [],
        "domain_bridges": [],
        "potential_comparisons": [],
        "relationship_stats": {},
    }

    # Build adjacency: page → set of pages it references
    title_to_page = {p["title"]: p for p in manifest["pages"]}
    outgoing: Dict[str, set] = {}
    for page_data in manifest["pages"]:
        title = page_data["title"]
        targets = set()
        for rel in page_data.get("relationships", []):
            for t in rel.get("targets", []):
                targets.add(t)
        outgoing[title] = targets

    # 1. Missing backlinks: A references B but B doesn't reference A
    for title, targets in outgoing.items():
        for target in targets:
            if target in outgoing and title not in outgoing[target]:
                # Target exists as a page but doesn't link back
                report["missing_backlinks"].append({
                    "from": title,
                    "to": target,
                })

    # 2. Domain bridges: pages with relationships crossing domains
    domain_connections: Dict[str, Dict[str, int]] = {}
    for page_data in manifest["pages"]:
        src_domain = page_data.get("domain", "")
        for rel in page_data.get("relationships", []):
            for target_name in rel.get("targets", []):
                target_page = title_to_page.get(target_name)
                if target_page:
                    dst_domain = target_page.get("domain", "")
                    if src_domain and dst_domain and src_domain != dst_domain:
                        key = tuple(sorted([src_domain, dst_domain]))
                        bridge_key = f"{key[0]} <-> {key[1]}"
                        domain_connections.setdefault(bridge_key, {"count": 0, "pages": set()})
                        domain_connections[bridge_key]["count"] += 1
                        domain_connections[bridge_key]["pages"].add(page_data["title"])

    for bridge, info in sorted(domain_connections.items(), key=lambda x: x[1]["count"], reverse=True):
        report["domain_bridges"].append({
            "bridge": bridge,
            "relationship_count": info["count"],
            "bridging_pages": len(info["pages"]),
        })

    # 3. Potential comparisons: pages in different domains with shared tags
    for i, p1 in enumerate(manifest["pages"]):
        for p2 in manifest["pages"][i + 1:]:
            if p1.get("domain") == p2.get("domain"):
                continue
            if p1.get("type") == "source-synthesis" or p2.get("type") == "source-synthesis":
                continue
            tags1 = set(p1.get("tags", []))
            tags2 = set(p2.get("tags", []))
            shared = tags1 & tags2
            if len(shared) >= 3:
                report["potential_comparisons"].append({
                    "page_a": p1["title"],
                    "page_b": p2["title"],
                    "shared_tags": sorted(shared),
                    "overlap": len(shared),
                })

    report["potential_comparisons"].sort(key=lambda x: x["overlap"], reverse=True)

    # 4. Relationship verb distribution
    verb_counts: Dict[str, int] = {}
    for page_data in manifest["pages"]:
        for rel in page_data.get("relationships", []):
            verb = rel.get("verb", "UNKNOWN")
            verb_counts[verb] = verb_counts.get(verb, 0) + 1
    report["relationship_stats"] = dict(sorted(verb_counts.items(), key=lambda x: x[1], reverse=True))

    if verbose:
        print(f"  Cross-Reference Analysis:")
        print(f"    Missing backlinks:      {len(report['missing_backlinks'])}")
        print(f"    Domain bridges:         {len(report['domain_bridges'])}")
        print(f"    Potential comparisons:  {len(report['potential_comparisons'])}")

        if report["domain_bridges"]:
            print(f"\n  Domain bridges (strongest connections):")
            for b in report["domain_bridges"][:5]:
                print(f"    {b['bridge']}: {b['relationship_count']} rels across {b['bridging_pages']} pages")

        if report["potential_comparisons"][:5]:
            print(f"\n  Comparison candidates (shared tags):")
            for c in report["potential_comparisons"][:5]:
                print(f"    {c['page_a']} vs {c['page_b']} ({c['overlap']} shared tags)")

        print(f"\n  Relationship verbs:")
        for verb, count in list(report["relationship_stats"].items())[:10]:
            print(f"    {verb}: {count}")

    return report


# ---------------------------------------------------------------------------
# Integration steps (notebooklm, obsidian, sync)
# ---------------------------------------------------------------------------

def run_mirror(project_root: Path, notebook_name: str = None,
               verbose: bool = True) -> Dict[str, Any]:
    """Mirror wiki source URLs to a NotebookLM notebook."""
    if not notebooklm.is_available():
        return {"ok": False, "error": "notebooklm-py not available", "skipped": True}

    wiki_dir = project_root / "wiki"
    manifest_path = wiki_dir / "manifest.json"
    if not manifest_path.exists():
        return {"ok": False, "error": "No manifest.json — run post-chain first"}

    manifest = json.loads(manifest_path.read_text())

    # Collect unique source URLs from all pages
    source_urls = set()
    for page in manifest.get("pages", []):
        meta_path = wiki_dir / page.get("path", "")
        if not meta_path.exists():
            continue
        text = meta_path.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        for src in meta.get("sources", []):
            url = src.get("url")
            if url:
                source_urls.add(url)

    if not source_urls:
        return {"ok": True, "sources_added": 0, "note": "No source URLs found"}

    # Create or use notebook
    nb_name = notebook_name or "Research Wiki Sources"
    if verbose:
        print(f"  Mirroring {len(source_urls)} source URLs to NotebookLM notebook '{nb_name}'...")

    result = notebooklm.create_notebook(nb_name)
    if not result["ok"] and "already exists" not in result.get("stderr", ""):
        # Try to continue — notebook might already exist
        pass

    added = 0
    errors = 0
    for url in sorted(source_urls):
        if verbose:
            print(f"    + {url[:70]}")
        add_result = notebooklm.add_source(url)
        if add_result["ok"]:
            added += 1
        else:
            errors += 1
            if verbose:
                print(f"      ERROR: {add_result.get('error', add_result.get('stderr', ''))[:60]}")

    return {"ok": True, "sources_added": added, "errors": errors, "total": len(source_urls)}


def run_nlm_research(topic: str, project_root: Path,
                     verbose: bool = True) -> Dict[str, Any]:
    """Use NotebookLM's research agent to find sources for a topic."""
    if not notebooklm.is_available():
        return {"ok": False, "error": "notebooklm-py not available", "skipped": True}

    if verbose:
        print(f"  Researching via NotebookLM: {topic}")

    result = notebooklm.add_research(topic)
    if verbose:
        if result["ok"]:
            print(f"    Research started — sources will be auto-imported")
        else:
            print(f"    ERROR: {result.get('error', result.get('stderr', ''))[:80]}")

    return result


def run_nlm_ask(question: str, project_root: Path,
                verbose: bool = True) -> Dict[str, Any]:
    """Ask NotebookLM a question against its sources (cross-validation)."""
    if not notebooklm.is_available():
        return {"ok": False, "error": "notebooklm-py not available", "skipped": True}

    if verbose:
        print(f"  Asking NotebookLM: {question}")

    result = notebooklm.ask(question, json_output=True)
    if verbose:
        if result["ok"]:
            # Print first 200 chars of answer
            answer = result.get("stdout", "")[:200]
            print(f"    {answer}")
        else:
            print(f"    ERROR: {result.get('error', result.get('stderr', ''))[:80]}")

    return result


def run_sync_step(project_root: Path, verbose: bool = True) -> Dict[str, Any]:
    """Run sync to Windows as a pipeline step."""
    from tools.sync import get_sync_config, run_sync, save_sync_state

    config = get_sync_config(project_root)
    if not config["target"]:
        return {"ok": False, "error": "No sync target configured", "skipped": True}

    if verbose:
        print(f"  Syncing to {config['target']}...")

    result = run_sync(config, verbose=False)
    save_sync_state(project_root, result)

    if verbose:
        status = "OK" if result["ok"] else "FAILED"
        print(f"    Sync {status} ({result.get('files_changed', '?')} files)")

    return result


# ---------------------------------------------------------------------------
# Scaffold command
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Named chains (predefined pipeline sequences)
# ---------------------------------------------------------------------------

CHAINS: Dict[str, Dict[str, Any]] = {
    "ingest": {
        "description": "Fetch URLs → post-chain",
        "steps": ["fetch", "post"],
        "needs_input": True,
    },
    "ingest-local": {
        "description": "Scan local projects → post-chain",
        "steps": ["scan", "post"],
        "needs_input": True,
    },
    "analyze": {
        "description": "Gap analysis → cross-reference → post-chain",
        "steps": ["gaps", "crossref", "post"],
        "needs_input": False,
    },
    "full": {
        "description": "Fetch → post → gaps → crossref → sync (complete pipeline)",
        "steps": ["fetch", "post", "gaps", "crossref", "sync"],
        "needs_input": True,
    },
    "health": {
        "description": "Post-chain → gaps → crossref (wiki health check)",
        "steps": ["post", "gaps", "crossref"],
        "needs_input": False,
    },
    "publish": {
        "description": "Post-chain → sync to Windows (make Obsidian-ready)",
        "steps": ["post", "sync"],
        "needs_input": False,
    },
    "mirror": {
        "description": "Push wiki source URLs to NotebookLM notebook",
        "steps": ["mirror"],
        "needs_input": False,
    },
    "research": {
        "description": "NotebookLM research → fetch results → post-chain",
        "steps": ["nlm-research", "post"],
        "needs_input": True,
    },
    "deep": {
        "description": "Gaps → crossref → mirror → sync (full analysis + integration)",
        "steps": ["gaps", "crossref", "mirror", "post", "sync"],
        "needs_input": False,
    },
    "evolve": {
        "description": "Score candidates → scaffold top N → post-chain",
        "steps": ["evolve-score", "post"],
        "needs_input": False,
    },
    "evolve-auto": {
        "description": "Score → scaffold → generate (local model) → post-chain",
        "steps": ["evolve-auto", "post"],
        "needs_input": False,
    },
    "spine-refresh": {
        "description": "Score domain-overview candidates → generate → post-chain",
        "steps": ["evolve-spine", "post"],
        "needs_input": False,
    },
}


def run_chain(chain_name: str, project_root: Path, inputs: List[str] = None,
              batch_file: str = None, verbose: bool = True) -> Dict[str, Any]:
    """Execute a named chain of pipeline steps."""
    if chain_name not in CHAINS:
        return {"error": f"Unknown chain: {chain_name}. Available: {', '.join(CHAINS.keys())}"}

    chain = CHAINS[chain_name]
    results: Dict[str, Any] = {"chain": chain_name, "steps": {}}

    if verbose:
        print(f"Running chain: {chain_name} ({chain['description']})")

    # Collect URLs if needed
    urls = list(inputs or [])
    if batch_file:
        bf = Path(batch_file)
        if bf.exists():
            for line in bf.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    urls.append(line)

    for step_name in chain["steps"]:
        if verbose:
            print(f"\n--- Step: {step_name} ---")

        if step_name == "fetch":
            if urls:
                step_result = group_fetch(urls, project_root, verbose=verbose)
            else:
                step_result = {"skipped": "no URLs provided"}
            results["steps"]["fetch"] = step_result

        elif step_name == "scan":
            if urls:
                step_result = group_scan(urls, project_root, verbose=verbose)
            else:
                step_result = {"skipped": "no paths provided"}
            results["steps"]["scan"] = step_result

        elif step_name == "post":
            step_result = post_chain(project_root, verbose=verbose)
            results["steps"]["post"] = step_result

        elif step_name == "gaps":
            step_result = run_gaps(project_root, verbose=verbose)
            results["steps"]["gaps"] = step_result

        elif step_name == "crossref":
            step_result = run_crossref(project_root, verbose=verbose)
            results["steps"]["crossref"] = step_result

        elif step_name == "mirror":
            step_result = run_mirror(project_root, verbose=verbose)
            results["steps"]["mirror"] = step_result

        elif step_name == "nlm-research":
            # Uses first input arg as the research topic
            topic = urls[0] if urls else None
            if topic:
                step_result = run_nlm_research(topic, project_root, verbose=verbose)
            else:
                step_result = {"ok": False, "error": "No topic provided"}
            results["steps"]["nlm-research"] = step_result

        elif step_name == "nlm-ask":
            question = urls[0] if urls else None
            if question:
                step_result = run_nlm_ask(question, project_root, verbose=verbose)
            else:
                step_result = {"ok": False, "error": "No question provided"}
            results["steps"]["nlm-ask"] = step_result

        elif step_name == "sync":
            step_result = run_sync_step(project_root, verbose=verbose)
            results["steps"]["sync"] = step_result

        elif step_name == "evolve-score":
            from tools.evolve import evolve as run_evolve
            step_result = run_evolve(project_root, mode="scaffold", top=5, verbose=verbose)
            results["steps"]["evolve-score"] = step_result

        elif step_name == "evolve-auto":
            from tools.evolve import evolve as run_evolve
            step_result = run_evolve(project_root, mode="auto", backend_name="openai", top=5, verbose=verbose)
            results["steps"]["evolve-auto"] = step_result

        elif step_name == "evolve-spine":
            from tools.evolve import evolve as run_evolve
            step_result = run_evolve(project_root, mode="auto", type_filter="domain-overview",
                                     backend_name="openai", top=7, verbose=verbose)
            results["steps"]["evolve-spine"] = step_result

    return results


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def print_post_report(report: Dict[str, Any]):
    """Print a human-readable post-chain report."""
    steps = report["steps"]
    m = steps.get("manifest", {})
    v = steps.get("validate", {})
    o = steps.get("obsidian", {})
    l = steps.get("lint", {})
    idx = steps.get("indexes", {})

    print("\n  ┌─────────────────────────────────────┐")
    print("  │       Post-Ingestion Report          │")
    print("  ├─────────────────────────────────────┤")
    print(f"  │  Indexes rebuilt:  {idx.get('updated', 0):>15} │")
    print(f"  │  Pages:            {m.get('pages', 0):>15} │")
    print(f"  │  Relationships:    {m.get('relationships', 0):>15} │")
    print(f"  │  Validation errors:{v.get('errors', 0):>15} │")
    print(f"  │  Backlinks updated:{o.get('updated', 0):>15} │")
    print(f"  │  Lint issues:      {l.get('total_issues', 0):>15} │")
    print("  └─────────────────────────────────────┘")

    if v.get("errors", 0) > 0:
        print("\n  ⚠ Validation errors found:")
        for d in v.get("details", []):
            for e in d.get("errors", []):
                print(f"    {d['file']}: {e}")

    status = "PASS" if report["success"] else "FAIL"
    print(f"\n  Status: {status}")


def print_fetch_report(results: List[Dict[str, Any]]):
    """Print a human-readable fetch report."""
    fetched = sum(1 for r in results if r.get("status") == "fetched")
    skipped = sum(1 for r in results if r.get("status") == "skipped")
    errors = sum(1 for r in results if r.get("status") == "error")
    queued = sum(1 for r in results if r.get("status") == "queued")

    parts = []
    if fetched:
        parts.append(f"{fetched} fetched")
    if skipped:
        parts.append(f"{skipped} skipped")
    if queued:
        parts.append(f"{queued} queued")
    if errors:
        parts.append(f"{errors} errors")
    print(f"\n  Fetch: {', '.join(parts)}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Pipeline orchestrator for the research wiki",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  post                  Run post-ingestion chain (index → manifest → validate → obsidian → lint)
  fetch URL [URL...]    Fetch URLs into raw/
  fetch --batch FILE    Fetch URLs from a file (one per line)
  fetch --topic QUERY   Queue a research topic
  scan PATH             Scan local project and copy key docs to raw/
  status                Show raw files and wiki stats
  run URL [URL...]      Fetch + post-chain
  run --batch FILE      Batch fetch + post-chain
""",
    )
    parser.add_argument("command",
                        choices=["post", "fetch", "scan", "status", "run",
                                 "chain", "gaps", "crossref", "integrations",
                                 "scaffold", "evolve"],
                        help="Pipeline command")
    parser.add_argument("args", nargs="*", help="Command arguments (URLs, paths, chain name, etc.)")
    parser.add_argument("--batch", help="File containing URLs (one per line)")
    parser.add_argument("--topic", help="Research topic to queue")
    parser.add_argument("--list", action="store_true", help="List available chains")
    parser.add_argument("--parallel", "-p", type=int, default=4,
                        help="Max parallel workers for group operations (default: 4)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--quiet", "-q", action="store_true", help="Minimal output")

    args, _extra = parser.parse_known_args()
    # Merge unrecognised flags into args.args so sub-commands (e.g. evolve) can
    # re-parse them with their own ArgumentParser.
    if _extra:
        args.args = list(args.args) + _extra
    root = get_project_root()
    verbose = not args.quiet and not args.json

    if args.command == "post":
        if verbose:
            print("Running post-ingestion chain...")
        report = post_chain(root, verbose=verbose)
        if args.json:
            print(json.dumps(report, indent=2, default=str))
        elif verbose:
            print_post_report(report)
        sys.exit(0 if report["success"] else 1)

    elif args.command == "fetch":
        urls = list(args.args)
        results = []

        if args.batch:
            batch_file = Path(args.batch)
            if batch_file.exists():
                for line in batch_file.read_text().splitlines():
                    line = line.strip()
                    if line and not line.startswith("#"):
                        urls.append(line)

        if args.topic:
            if verbose:
                print(f"Queueing topic: {args.topic}")
            results.extend(fetch_topic(args.topic, root, verbose=verbose))

        if urls:
            if verbose:
                print(f"Fetching {len(urls)} URL(s)...")
            results.extend(fetch_urls(urls, root, verbose=verbose))

        if not urls and not args.topic:
            print("Nothing to fetch. Provide URLs, --batch, or --topic.")
            sys.exit(1)

        if args.json:
            print(json.dumps(results, indent=2, default=str))
        elif verbose:
            print_fetch_report(results)

    elif args.command == "scan":
        if not args.args:
            print("Provide a project path to scan.")
            sys.exit(1)
        for path_str in args.args:
            path = Path(path_str)
            if verbose:
                print(f"Scanning: {path}")
            results = scan_project(path, root, verbose=verbose)
            if args.json:
                print(json.dumps(results, indent=2, default=str))

    elif args.command == "status":
        status = pipeline_status(root)
        if args.json:
            print(json.dumps(status, indent=2, default=str))
        else:
            print(f"Raw files: {status['raw_files']}")
            for t, c in sorted(status["raw_by_type"].items()):
                print(f"  {t}: {c}")
            print(f"Wiki pages: {status['wiki_pages']}")

    elif args.command == "run":
        urls = list(args.args)
        all_results: List[Dict[str, Any]] = []

        if args.batch:
            batch_file = Path(args.batch)
            if batch_file.exists():
                for line in batch_file.read_text().splitlines():
                    line = line.strip()
                    if line and not line.startswith("#"):
                        urls.append(line)

        if args.topic:
            if verbose:
                print(f"Queueing topic: {args.topic}")
            all_results.extend(fetch_topic(args.topic, root, verbose=verbose))

        if urls:
            if verbose:
                print(f"Fetching {len(urls)} URL(s) in parallel...")
            all_results.extend(group_fetch(urls, root, max_workers=args.parallel, verbose=verbose))

        if verbose:
            print_fetch_report(all_results)

        # Now run post-chain
        if verbose:
            print("\nRunning post-ingestion chain...")
        report = post_chain(root, verbose=verbose)

        if args.json:
            print(json.dumps({"fetch": all_results, "post": report}, indent=2, default=str))
        elif verbose:
            print_post_report(report)

        sys.exit(0 if report["success"] else 1)

    elif args.command == "chain":
        if args.list:
            print("Available chains:")
            for name, info in CHAINS.items():
                needs = " (needs input)" if info["needs_input"] else ""
                print(f"  {name:15s} — {info['description']}{needs}")
            sys.exit(0)

        chain_name = args.args[0] if args.args else None
        if not chain_name:
            print("Provide a chain name. Use --list to see available chains.")
            sys.exit(1)

        inputs = args.args[1:] if len(args.args) > 1 else []
        result = run_chain(chain_name, root, inputs=inputs,
                           batch_file=args.batch, verbose=verbose)

        if args.json:
            print(json.dumps(result, indent=2, default=str))
        sys.exit(0)

    elif args.command == "gaps":
        report = run_gaps(root, verbose=verbose)
        if args.json:
            print(json.dumps(report, indent=2, default=str))
        sys.exit(0)

    elif args.command == "crossref":
        report = run_crossref(root, verbose=verbose)
        if args.json:
            print(json.dumps(report, indent=2, default=str))
        sys.exit(0)

    elif args.command == "integrations":
        report = integrations_status()
        if args.json:
            print(json.dumps(report, indent=2, default=str))
        else:
            for name, info in report.items():
                installed = "YES" if info["installed"] else "NO"
                responsive = "YES" if info["responsive"] else "NO"
                print(f"  {name:15s}  installed={installed:3s}  responsive={responsive:3s}  {info['note']}")
        sys.exit(0)

    elif args.command == "scaffold":
        if len(args.args) < 2:
            print("Usage: pipeline scaffold <type> <title> [--topic DOMAIN] [--batch DERIVED1,DERIVED2]")
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

    elif args.command == "evolve":
        from tools.evolve import evolve as run_evolve
        import argparse as _argparse
        sub = _argparse.ArgumentParser(prog="pipeline evolve", add_help=False)
        sub.add_argument("--score", action="store_true")
        sub.add_argument("--scaffold", action="store_true")
        sub.add_argument("--auto", action="store_true")
        sub.add_argument("--dry-run", action="store_true", dest="dry_run")
        sub.add_argument("--execute", action="store_true")
        sub.add_argument("--review", action="store_true")
        sub.add_argument("--stale", action="store_true")
        sub.add_argument("--backend", default=os.environ.get("WIKI_EVOLVE_BACKEND", "claude-code"))
        sub.add_argument("--top", type=int, default=int(os.environ.get("WIKI_EVOLVE_TOP", 10)))
        sub.add_argument("--type", dest="etype")
        sub.add_argument("--domain")
        sub.add_argument("--clear", action="store_true")
        sub_args = sub.parse_args(args.args)

        # Determine mode from first true flag (score is default)
        if sub_args.stale:
            mode = "stale"
        elif sub_args.review:
            mode = "review"
        elif sub_args.execute:
            mode = "execute"
        elif sub_args.dry_run:
            mode = "dry-run"
        elif sub_args.auto:
            mode = "auto"
        elif sub_args.scaffold:
            mode = "scaffold"
        else:
            mode = "score"

        result = run_evolve(
            project_root=root,
            mode=mode,
            backend_name=sub_args.backend,
            top=sub_args.top,
            type_filter=sub_args.etype,
            domain_filter=sub_args.domain,
            clear_queue=sub_args.clear,
            verbose=verbose,
        )
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        sys.exit(0)


if __name__ == "__main__":
    main()
