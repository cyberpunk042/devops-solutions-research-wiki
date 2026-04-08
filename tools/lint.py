"""Wiki health checks CLI.

Checks for dead relationships, stale pages, thin content, orphan pages,
and domain health. Outputs structured JSON or human-readable reports.

Usage:
    python3 tools/lint.py                         # Human-readable summary
    python3 tools/lint.py --report                # JSON report
    python3 tools/lint.py --summary               # Human-readable summary
    python3 tools/lint.py --config path/to/config # Custom config
    python3 tools/lint.py --fix                   # Auto-fix where possible

Exit code: 0 if no issues, 1 if issues found.
"""

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from tools.common import (
    find_wiki_pages,
    get_project_root,
    load_config,
    parse_frontmatter,
    parse_relationships,
    parse_sections,
    word_count,
)


@dataclass
class LintConfig:
    stale_threshold_days: int
    min_summary_words: int
    min_deep_analysis_words: int
    min_relationships: int
    min_domain_pages: int
    min_cross_domain_rels: int
    similarity_threshold: float


def _collect_page_titles(pages: List[Path]) -> Set[str]:
    """Build a set of all page titles from frontmatter."""
    titles: Set[str] = set()
    for page in pages:
        try:
            text = page.read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(text)
            title = meta.get("title", "")
            if title:
                titles.add(title.strip())
            # Also add the stem as a fallback
            titles.add(page.stem)
        except Exception:
            pass
    return titles


def _strip_context(target: str) -> str:
    """Strip parenthetical context from a relationship target.

    e.g. 'Serverless Patterns (different trade-offs)' -> 'Serverless Patterns'
    """
    paren_idx = target.find("(")
    if paren_idx > 0:
        return target[:paren_idx].strip()
    return target.strip()


def _check_dead_relationships(
    pages: List[Path], known_titles: Set[str]
) -> List[Dict[str, str]]:
    """Find relationship targets that don't resolve to any known page title."""
    dead: List[Dict[str, str]] = []
    for page in pages:
        try:
            text = page.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(text)
            if not meta:
                continue
            source_title = meta.get("title", page.stem)
            sections = parse_sections(body)
            rel_text = sections.get("Relationships", "")
            if not rel_text:
                continue
            rels = parse_relationships(rel_text)
            for rel in rels:
                for target in rel["targets"]:
                    clean_target = _strip_context(target)
                    # Skip source IDs (start with src-)
                    if clean_target.startswith("src-"):
                        continue
                    if clean_target not in known_titles:
                        dead.append({
                            "source": source_title,
                            "verb": rel["verb"],
                            "target": clean_target,
                        })
        except Exception:
            pass
    return dead


def _check_stale_pages(
    pages: List[Path], threshold_days: int
) -> List[Dict[str, str]]:
    """Find pages not updated within threshold_days that aren't marked stale."""
    stale: List[Dict[str, str]] = []
    cutoff = date.today() - timedelta(days=threshold_days)
    for page in pages:
        try:
            text = page.read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(text)
            if not meta:
                continue
            status = meta.get("status", "")
            if status == "stale":
                continue
            updated = meta.get("updated")
            if updated is None:
                continue
            # updated may be a date object or string
            if isinstance(updated, str):
                try:
                    updated_date = date.fromisoformat(updated)
                except ValueError:
                    continue
            elif isinstance(updated, date):
                updated_date = updated
            else:
                continue
            if updated_date < cutoff:
                stale.append({
                    "title": meta.get("title", page.stem),
                    "updated": str(updated_date),
                })
        except Exception:
            pass
    return stale


def _check_thin_pages(
    pages: List[Path],
    min_summary_words: int,
    min_deep_analysis_words: int,
) -> List[Dict[str, Any]]:
    """Find pages with insufficient content in key sections."""
    thin: List[Dict[str, Any]] = []
    # Types that require Deep Analysis
    deep_analysis_types = {"concept", "deep-dive", "comparison"}
    for page in pages:
        try:
            text = page.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(text)
            if not meta:
                continue
            page_type = meta.get("type", "")
            title = meta.get("title", page.stem)
            sections = parse_sections(body)

            # Check Summary word count
            summary = sections.get("Summary", "")
            summary_wc = word_count(summary) if summary else 0
            if summary_wc < min_summary_words and summary_wc > 0:
                thin.append({
                    "title": title,
                    "type": page_type,
                    "issue": "thin_summary",
                    "summary_words": summary_wc,
                    "deep_analysis_words": None,
                })

            # Check Deep Analysis word count for relevant types
            if page_type in deep_analysis_types:
                deep = sections.get("Deep Analysis", "")
                deep_wc = word_count(deep) if deep else 0
                if deep_wc < min_deep_analysis_words:
                    thin.append({
                        "title": title,
                        "type": page_type,
                        "issue": "thin_deep_analysis",
                        "summary_words": summary_wc,
                        "deep_analysis_words": deep_wc,
                    })
        except Exception:
            pass
    return thin


def _check_orphan_pages(
    pages: List[Path], wiki_dir: Path
) -> List[str]:
    """Find pages not listed in any _index.md file."""
    # Collect all page filenames referenced in _index.md files
    referenced: Set[str] = set()
    for index_file in wiki_dir.rglob("_index.md"):
        try:
            content = index_file.read_text(encoding="utf-8")
            # Look for markdown link patterns like [Title](filename.md)
            import re
            for match in re.finditer(r"\[([^\]]+)\]\(([^)]+\.md)\)", content):
                linked_file = match.group(2)
                # Resolve relative to the index file's directory
                resolved = (index_file.parent / linked_file).resolve()
                referenced.add(str(resolved))
        except Exception:
            pass

    orphans: List[str] = []
    for page in pages:
        if str(page.resolve()) not in referenced:
            try:
                text = page.read_text(encoding="utf-8")
                meta, _ = parse_frontmatter(text)
                title = meta.get("title", page.stem) if meta else page.stem
                orphans.append(title)
            except Exception:
                orphans.append(page.stem)
    return orphans


def _check_domain_health(
    pages: List[Path],
    min_domain_pages: int,
    min_cross_domain_rels: int,
) -> List[Dict[str, Any]]:
    """Check domain-level health: page counts and cross-domain relationships."""
    # Group pages by domain
    domain_pages: Dict[str, List[Path]] = {}
    domain_titles: Dict[str, Set[str]] = {}

    for page in pages:
        try:
            text = page.read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(text)
            if not meta:
                continue
            domain = meta.get("domain", "unknown")
            title = meta.get("title", page.stem)
            domain_pages.setdefault(domain, []).append(page)
            domain_titles.setdefault(domain, set()).add(title)
        except Exception:
            pass

    # Build a global title->domain map
    title_to_domain: Dict[str, str] = {}
    for domain, titles in domain_titles.items():
        for t in titles:
            title_to_domain[t] = domain

    domain_health: List[Dict[str, Any]] = []
    for domain, dpages in domain_pages.items():
        issues: List[str] = []
        page_count = len(dpages)

        if page_count < min_domain_pages:
            issues.append(f"too_few_pages ({page_count} < {min_domain_pages})")

        # Count cross-domain relationships
        cross_domain_count = 0
        for page in dpages:
            try:
                text = page.read_text(encoding="utf-8")
                meta, body = parse_frontmatter(text)
                if not meta:
                    continue
                sections = parse_sections(body)
                rel_text = sections.get("Relationships", "")
                if not rel_text:
                    continue
                rels = parse_relationships(rel_text)
                for rel in rels:
                    for target in rel["targets"]:
                        clean = _strip_context(target)
                        if clean.startswith("src-"):
                            continue
                        target_domain = title_to_domain.get(clean)
                        if target_domain and target_domain != domain:
                            cross_domain_count += 1
            except Exception:
                pass

        if cross_domain_count < min_cross_domain_rels:
            issues.append(
                f"too_few_cross_domain_relationships ({cross_domain_count} < {min_cross_domain_rels})"
            )

        if issues:
            domain_health.append({
                "domain": domain,
                "page_count": page_count,
                "cross_domain_relationships": cross_domain_count,
                "issues": issues,
            })

    return domain_health


def lint_wiki(wiki_dir: Path, config: LintConfig) -> Dict[str, Any]:
    """Run all wiki health checks and return a structured report.

    Args:
        wiki_dir: Directory containing wiki markdown files.
        config: LintConfig with thresholds and limits.

    Returns:
        Dict with keys: orphan_pages, dead_relationships, stale_pages,
        thin_pages, domain_health, summary.
    """
    pages = []
    for md_file in sorted(wiki_dir.rglob("*.md")):
        if md_file.name == "_index.md":
            continue
        pages.append(md_file)

    known_titles = _collect_page_titles(pages)

    dead_relationships = _check_dead_relationships(pages, known_titles)
    stale_pages = _check_stale_pages(pages, config.stale_threshold_days)
    thin_pages = _check_thin_pages(
        pages,
        config.min_summary_words,
        config.min_deep_analysis_words,
    )
    orphan_pages = _check_orphan_pages(pages, wiki_dir)
    domain_health = _check_domain_health(
        pages,
        config.min_domain_pages,
        config.min_cross_domain_rels,
    )

    total_issues = (
        len(dead_relationships)
        + len(stale_pages)
        + len(thin_pages)
        + len(orphan_pages)
        + sum(len(d["issues"]) for d in domain_health)
    )

    return {
        "orphan_pages": orphan_pages,
        "dead_relationships": dead_relationships,
        "stale_pages": stale_pages,
        "thin_pages": thin_pages,
        "domain_health": domain_health,
        "summary": {
            "pages_scanned": len(pages),
            "total_issues": total_issues,
            "dead_relationships": len(dead_relationships),
            "stale_pages": len(stale_pages),
            "thin_pages": len(thin_pages),
            "orphan_pages": len(orphan_pages),
            "domain_health_issues": sum(len(d["issues"]) for d in domain_health),
        },
    }


def _config_from_quality_standards(path: Path) -> Optional[LintConfig]:
    """Load LintConfig from a quality-standards.yaml file."""
    data = load_config(path)
    if data is None:
        return None
    pq = data.get("page_quality", {})
    dh = data.get("domain_health", {})
    dd = data.get("duplicate_detection", {})
    return LintConfig(
        stale_threshold_days=pq.get("stale_threshold_days", 30),
        min_summary_words=pq.get("min_summary_words", 30),
        min_deep_analysis_words=pq.get("min_deep_analysis_words", 100),
        min_relationships=pq.get("min_relationships", 1),
        min_domain_pages=dh.get("min_pages", 3),
        min_cross_domain_rels=dh.get("min_cross_domain_relationships", 2),
        similarity_threshold=dd.get("similarity_threshold", 0.70),
    )


def _print_human_report(report: Dict[str, Any]) -> None:
    """Print a human-readable lint report."""
    s = report["summary"]
    print(f"\nWiki Lint Report")
    print(f"{'=' * 40}")
    print(f"Pages scanned:    {s['pages_scanned']}")
    print(f"Total issues:     {s['total_issues']}")
    print()

    if report["dead_relationships"]:
        print(f"Dead Relationships ({len(report['dead_relationships'])}):")
        for d in report["dead_relationships"]:
            print(f"  [{d['source']}] {d['verb']}: '{d['target']}' (not found)")
        print()

    if report["stale_pages"]:
        print(f"Stale Pages ({len(report['stale_pages'])}):")
        for p in report["stale_pages"]:
            print(f"  {p['title']} (updated: {p['updated']})")
        print()

    if report["thin_pages"]:
        print(f"Thin Pages ({len(report['thin_pages'])}):")
        for p in report["thin_pages"]:
            if p["issue"] == "thin_deep_analysis":
                print(f"  {p['title']} [{p['type']}]: Deep Analysis {p['deep_analysis_words']} words")
            else:
                print(f"  {p['title']} [{p['type']}]: Summary {p.get('summary_words', '?')} words")
        print()

    if report["orphan_pages"]:
        print(f"Orphan Pages ({len(report['orphan_pages'])}):")
        for title in report["orphan_pages"]:
            print(f"  {title}")
        print()

    if report["domain_health"]:
        print(f"Domain Health Issues ({len(report['domain_health'])}):")
        for d in report["domain_health"]:
            print(f"  {d['domain']} ({d['page_count']} pages):")
            for issue in d["issues"]:
                print(f"    - {issue}")
        print()

    status = "PASS" if s["total_issues"] == 0 else "FAIL"
    print(f"{status}: {s['total_issues']} issue(s) found")


def main():
    parser = argparse.ArgumentParser(description="Run wiki health checks")
    parser.add_argument(
        "--report",
        action="store_true",
        help="Output full JSON report",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Output human-readable summary (default)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to auto-fix issues where possible",
    )
    parser.add_argument(
        "--config",
        help="Path to quality-standards.yaml (default: config/quality-standards.yaml)",
    )
    parser.add_argument(
        "wiki_dir",
        nargs="?",
        help="Path to wiki directory (default: wiki/)",
    )
    args = parser.parse_args()

    root = get_project_root()

    config_path = Path(args.config) if args.config else root / "config" / "quality-standards.yaml"
    lint_config = _config_from_quality_standards(config_path)
    if lint_config is None:
        # Use sensible defaults if config is missing
        lint_config = LintConfig(
            stale_threshold_days=30,
            min_summary_words=30,
            min_deep_analysis_words=100,
            min_relationships=1,
            min_domain_pages=3,
            min_cross_domain_rels=2,
            similarity_threshold=0.70,
        )

    wiki_dir = Path(args.wiki_dir) if args.wiki_dir else root / "wiki"
    report = lint_wiki(wiki_dir, lint_config)

    if args.fix:
        print("Auto-fix is not yet implemented.", file=sys.stderr)

    if args.report:
        print(json.dumps(report, indent=2))
    else:
        # Default to human-readable summary
        _print_human_report(report)

    sys.exit(0 if report["summary"]["total_issues"] == 0 else 1)


if __name__ == "__main__":
    main()
