"""Wiki view and search CLI.

Query the wiki by type, domain, maturity, tag, or free text.
Browse pages with summaries. Trace relationships.

Usage:
    python3 -m tools.view                           # Overview dashboard
    python3 -m tools.view type lesson               # All lessons with summaries
    python3 -m tools.view type decision              # All decisions with choices
    python3 -m tools.view domain ai-agents           # Domain pages + state
    python3 -m tools.view domain ai-agents --brief   # Just titles
    python3 -m tools.view maturity canonical          # Pages at maturity level
    python3 -m tools.view tag harness-engineering    # Pages with tag
    python3 -m tools.view refs "Agent Orchestration" # What references / is referenced by
    python3 -m tools.view search "context management" # Free text search with summaries
    python3 -m tools.view search "hooks" --type lesson # Faceted search
    python3 -m tools.view models                     # All 15 models with standards
    python3 -m tools.view decisions                  # All decisions with choices
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.common import (
    get_project_root,
    parse_frontmatter,
    parse_sections,
)


def load_manifest() -> Dict[str, Any]:
    root = get_project_root()
    manifest_path = root / "wiki" / "manifest.json"
    if not manifest_path.exists():
        print("ERROR: manifest.json not found. Run: python3 -m tools.pipeline post")
        sys.exit(1)
    return json.load(open(manifest_path, encoding="utf-8"))


def _summary_for(page: Dict, root: Path, max_len: int = 120) -> str:
    """Get the Summary section content for a page."""
    page_path = root / "wiki" / page["path"]
    if not page_path.exists():
        return ""
    try:
        text = page_path.read_text(encoding="utf-8")
        _, body = parse_frontmatter(text)
        sections = parse_sections(body)
        summary = sections.get("Summary", "").strip()
        if len(summary) > max_len:
            summary = summary[:max_len - 3] + "..."
        return summary
    except Exception:
        return ""


def cmd_overview(manifest: Dict, root: Path):
    """Dashboard overview."""
    stats = manifest.get("stats", {})
    pages = manifest["pages"]

    print(f"\n=== Wiki Dashboard ===")
    print(f"Pages: {stats.get('pages', len(pages))}")
    print(f"Relationships: {stats.get('relationships', 0)}")
    print()

    # By type
    type_counts = {}
    for p in pages:
        t = p.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1
    print("By type:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {c:>3}  {t}")

    # By domain
    print("\nBy domain:")
    domain_counts = {}
    for p in pages:
        d = p.get("domain", "unknown")
        domain_counts[d] = domain_counts.get(d, 0) + 1
    for d, c in sorted(domain_counts.items(), key=lambda x: -x[1]):
        print(f"  {c:>3}  {d}")

    # By maturity
    print("\nBy maturity:")
    mat_counts = {}
    for p in pages:
        m = p.get("maturity", "") or "unset"
        mat_counts[m] = mat_counts.get(m, 0) + 1
    for m, c in sorted(mat_counts.items(), key=lambda x: -x[1]):
        print(f"  {c:>3}  {m}")


def cmd_type(manifest: Dict, root: Path, page_type: str, brief: bool = False):
    """List pages of a given type with summaries."""
    pages = [p for p in manifest["pages"] if p.get("type") == page_type]
    if not pages:
        print(f"No pages of type '{page_type}'")
        return

    print(f"\n=== {page_type} ({len(pages)} pages) ===\n")
    for p in sorted(pages, key=lambda x: x.get("title", "")):
        title = p.get("title", p.get("slug", ""))
        domain = p.get("domain", "")
        if brief:
            print(f"  [{domain}] {title}")
        else:
            summary = _summary_for(p, root, 150)
            print(f"  [{domain}] {title}")
            if summary:
                print(f"    {summary}")
            print()


def cmd_domain(manifest: Dict, root: Path, domain: str, brief: bool = False):
    """Show domain pages with state."""
    pages = [p for p in manifest["pages"] if p.get("domain") == domain]
    if not pages:
        print(f"No pages in domain '{domain}'")
        return

    print(f"\n=== {domain} ({len(pages)} pages) ===\n")

    # Group by type
    by_type = {}
    for p in pages:
        t = p.get("type", "unknown")
        by_type.setdefault(t, []).append(p)

    for t, ps in sorted(by_type.items()):
        print(f"  --- {t} ({len(ps)}) ---")
        for p in sorted(ps, key=lambda x: x.get("title", "")):
            title = p.get("title", "")
            maturity = p.get("maturity", "")
            if brief:
                print(f"    {title}" + (f" [{maturity}]" if maturity else ""))
            else:
                summary = _summary_for(p, root, 120)
                print(f"    {title}" + (f" [{maturity}]" if maturity else ""))
                if summary:
                    print(f"      {summary}")
                print()


def cmd_refs(manifest: Dict, root: Path, query: str):
    """Show what a page references and what references it."""
    # Find the page
    target = None
    for p in manifest["pages"]:
        if query.lower() in p.get("title", "").lower() or query.lower() in p.get("slug", "").lower():
            target = p
            break

    if not target:
        print(f"Page not found: '{query}'")
        return

    title = target["title"]
    print(f"\n=== References for: {title} ===\n")

    # Outbound
    rels = target.get("relationships", [])
    if rels:
        print(f"  Outbound ({len(rels)}):")
        for r in rels:
            verb = r.get("verb", "RELATES TO")
            # Handle both 'target' (singular) and 'targets' (list) formats
            targets = r.get("targets", [])
            if not targets and "target" in r:
                targets = [r["target"]]
            for t in targets:
                print(f"    {verb}: {t}")
    else:
        print("  Outbound: none")

    # Inbound
    inbound = []
    for p in manifest["pages"]:
        if p["title"] == title:
            continue
        for r in p.get("relationships", []):
            rel_targets = r.get("targets", [])
            if not rel_targets and "target" in r:
                rel_targets = [r["target"]]
            for t in rel_targets:
                if t == title:
                    inbound.append((p["title"], r.get("verb", "RELATES TO")))

    print(f"\n  Inbound ({len(inbound)}):")
    if inbound:
        for src, verb in sorted(inbound):
            print(f"    {verb}: {src}")
    else:
        print("    none")


def cmd_search(manifest: Dict, root: Path, query: str,
               filter_type: Optional[str] = None,
               filter_domain: Optional[str] = None):
    """Free text search with optional facets."""
    results = []
    ql = query.lower()

    for p in manifest["pages"]:
        # Check title, tags, domain
        title = p.get("title", "").lower()
        tags = " ".join(p.get("tags", [])).lower()
        domain = p.get("domain", "").lower()
        ptype = p.get("type", "")

        if filter_type and ptype != filter_type:
            continue
        if filter_domain and p.get("domain") != filter_domain:
            continue

        score = 0
        if ql in title:
            score += 3
        if ql in tags:
            score += 2
        if ql in domain:
            score += 1

        # Check page body if no metadata match
        if score == 0:
            page_path = root / "wiki" / p["path"]
            if page_path.exists():
                try:
                    text = page_path.read_text(encoding="utf-8", errors="ignore").lower()
                    if ql in text:
                        score = 1
                except Exception:
                    pass

        if score > 0:
            results.append((score, p))

    results.sort(key=lambda x: -x[0])

    filters = []
    if filter_type:
        filters.append(f"type={filter_type}")
    if filter_domain:
        filters.append(f"domain={filter_domain}")
    filter_str = f" ({', '.join(filters)})" if filters else ""

    print(f"\n=== Search: '{query}'{filter_str} — {len(results)} results ===\n")
    for score, p in results[:20]:
        title = p.get("title", "")
        domain = p.get("domain", "")
        ptype = p.get("type", "")
        summary = _summary_for(p, root, 120)
        print(f"  [{ptype}] [{domain}] {title}")
        if summary:
            print(f"    {summary}")
        print()

    if len(results) > 20:
        print(f"  ... and {len(results) - 20} more")


def cmd_models(manifest: Dict, root: Path):
    """Show all models with their standards pages."""
    models = [p for p in manifest["pages"] if p.get("title", "").startswith("Model:")]
    standards = {p["title"]: p for p in manifest["pages"] if "Standards" in p.get("title", "")}

    print(f"\n=== Models ({len(models)}) ===\n")
    for m in sorted(models, key=lambda x: x.get("title", "")):
        title = m["title"]
        maturity = m.get("maturity", "")
        # Find matching standards page
        std = None
        for st, sp in standards.items():
            if any(word in st for word in title.replace("Model: ", "").split()[:2]):
                std = st
                break

        print(f"  {title} [{maturity}]")
        if std:
            print(f"    Standards: {std}")
        summary = _summary_for(m, root, 120)
        if summary:
            print(f"    {summary}")
        print()


def cmd_decisions(manifest: Dict, root: Path):
    """Show all decisions with their choices."""
    decisions = [p for p in manifest["pages"] if p.get("type") == "decision"]

    print(f"\n=== Decisions ({len(decisions)}) ===\n")
    for d in sorted(decisions, key=lambda x: x.get("title", "")):
        title = d.get("title", "")
        summary = _summary_for(d, root, 150)
        print(f"  {title}")
        if summary:
            print(f"    {summary}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Wiki view and search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  (none)              Dashboard overview
  type <type>         List pages of a type (lesson, decision, pattern, concept, etc.)
  domain <domain>     Show domain pages grouped by type
  refs <title>        Show outbound and inbound relationships for a page
  search <query>      Free text search with summaries
  models              All models with standards pages
  decisions           All decisions with summaries

Options:
  --brief             Titles only, no summaries
  --type TYPE         Filter search by page type
  --domain DOMAIN     Filter search by domain
""",
    )
    parser.add_argument("command", nargs="?", default="overview",
                        help="Command: overview, type, domain, refs, search, models, decisions")
    parser.add_argument("argument", nargs="?", default=None,
                        help="Argument for the command (type name, domain name, search query, etc.)")
    parser.add_argument("--brief", action="store_true", help="Titles only")
    parser.add_argument("--type", dest="filter_type", help="Filter by page type")
    parser.add_argument("--domain", dest="filter_domain", help="Filter by domain")

    args = parser.parse_args()
    root = get_project_root()
    manifest = load_manifest()

    if args.command == "overview" or args.command is None:
        cmd_overview(manifest, root)
    elif args.command == "type":
        if not args.argument:
            print("Usage: python3 -m tools.view type <type>")
            sys.exit(1)
        cmd_type(manifest, root, args.argument, brief=args.brief)
    elif args.command == "domain":
        if not args.argument:
            print("Usage: python3 -m tools.view domain <domain>")
            sys.exit(1)
        cmd_domain(manifest, root, args.argument, brief=args.brief)
    elif args.command == "refs":
        if not args.argument:
            print("Usage: python3 -m tools.view refs <page-title>")
            sys.exit(1)
        cmd_refs(manifest, root, args.argument)
    elif args.command == "search":
        if not args.argument:
            print("Usage: python3 -m tools.view search <query>")
            sys.exit(1)
        cmd_search(manifest, root, args.argument,
                   filter_type=args.filter_type, filter_domain=args.filter_domain)
    elif args.command == "models":
        cmd_models(manifest, root)
    elif args.command == "decisions":
        cmd_decisions(manifest, root)
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
