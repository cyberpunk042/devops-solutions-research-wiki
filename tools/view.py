"""Wiki view — browse the knowledge tree.

Shows the wiki's structure as a navigable tree, not a flat dump.
Think of it as opening a manual: spine → models → domains → pages.

Usage:
    python3 -m tools.view                        # The full tree (10-second overview)
    python3 -m tools.view spine                  # Spine detail: models + standards
    python3 -m tools.view model methodology      # One model with its member pages
    python3 -m tools.view domain ai-agents       # One domain with pages + summaries
    python3 -m tools.view lessons                # All lessons grouped by type
    python3 -m tools.view decisions              # All decisions with their choices
    python3 -m tools.view search "context"       # Find pages matching a query
    python3 -m tools.view refs "Page Title"      # What connects to what

Cross-platform: runs on Linux, macOS, Windows via Python.
Shell shortcut: ./wiki (Linux/macOS) or wiki.cmd (Windows)
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
    page_path = root / "wiki" / page["path"]
    if not page_path.exists():
        return ""
    try:
        text = page_path.read_text(encoding="utf-8")
        _, body = parse_frontmatter(text)
        sections = parse_sections(body)
        summary = sections.get("Summary", "").strip().split("\n")[0]
        if len(summary) > max_len:
            summary = summary[:max_len - 3] + "..."
        return summary
    except Exception:
        return ""


def _get_targets(rel: Dict) -> List[str]:
    targets = rel.get("targets", [])
    if not targets and "target" in rel:
        targets = [rel["target"]]
    return targets


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_tree(manifest: Dict, root: Path):
    """The full tree — understand the wiki in 10 seconds."""
    pages = manifest["pages"]
    models = [p for p in pages if p.get("title", "").startswith("Model:")]
    standards = [p for p in pages if "Standards" in p.get("title", "") and "What Good" in p.get("title", "")]
    decisions = [p for p in pages if p.get("type") == "decision"]
    lessons = [p for p in pages if p.get("type") == "lesson"]
    patterns_list = [p for p in pages if p.get("type") == "pattern"]
    comparisons = [p for p in pages if p.get("type") == "comparison"]
    concepts = [p for p in pages if p.get("type") == "concept"]
    sources = [p for p in pages if p.get("type") == "source-synthesis"]
    overviews = [p for p in pages if p.get("type") == "domain-overview"]

    domain_counts = {}
    for p in pages:
        if p.get("type") == "concept" and p.get("path", "").startswith("domains/"):
            d = p.get("domain", "unknown")
            domain_counts[d] = domain_counts.get(d, 0) + 1

    stats = manifest.get("stats", {})
    total = stats.get("pages", len(pages))
    rels = stats.get("relationships", 0)

    print(f"""
RESEARCH WIKI ({total} pages, {rels} relationships)
│
├── SPINE
│   ├── Super-Model: Research Wiki as Ecosystem Intelligence Hub
│   ├── Model Registry (entry point)
│   ├── Adoption Guide
│   │""")

    print(f"│   ├── MODELS ({len(models)}) + STANDARDS ({len(standards)})")
    for m in sorted(models, key=lambda x: x.get("title", "")):
        name = m["title"].replace("Model: ", "")
        mat = m.get("maturity", "")
        std = None
        words = name.split()[:2]
        for s in standards:
            if any(w in s["title"] for w in words):
                std = "✓"
                break
        std_str = f" [standards: {std}]" if std else ""
        print(f"│   │   ├── {name} [{mat}]{std_str}")
    print("│   │")

    sorted_domains = sorted(domain_counts.keys())
    print(f"│   └── DOMAIN OVERVIEWS ({len(overviews)})")
    for i, d_name in enumerate(sorted_domains):
        c = domain_counts[d_name]
        connector = "└" if i == len(sorted_domains) - 1 else "├"
        print(f"│       {connector}── {d_name} ({c} concepts)")
    print("│")

    print(f"├── KNOWLEDGE LAYERS")
    print(f"│   ├── L6 Decisions ({len(decisions)})")
    print(f"│   ├── L5 Patterns ({len(patterns_list)})")
    print(f"│   ├── L4 Lessons ({len(lessons)})")
    print(f"│   ├── L3 Comparisons ({len(comparisons)})")
    print(f"│   ├── L2 Concepts ({len(concepts)} across {len(domain_counts)} domains)")
    print(f"│   └── L1 Sources ({len(sources)})")
    print("│")

    backlog = [p for p in pages if p.get("domain") == "backlog"]
    logs = [p for p in pages if p.get("type") == "note"]
    print(f"└── OPERATIONAL")
    print(f"    ├── Backlog ({len(backlog)} items)")
    print(f"    └── Log ({len(logs)} entries)")
    print()
    print("Drill down:  (python3 wiki.py <command>)")
    print("  spine              Models + standards detail")
    print("  model X            One model's member pages")
    print("  domain X           One domain's concept pages")
    print("  lessons            All lessons by category")
    print("  decisions          All decisions with summaries")
    print("  search \"X\"         Find pages matching a query")
    print("  refs \"X\"           Trace relationships for a page")
    print("  <anything else>    Search for it")


def cmd_spine(manifest: Dict, root: Path):
    """Spine detail: super-model, models, standards."""
    pages = manifest["pages"]
    models = sorted(
        [p for p in pages if p.get("title", "").startswith("Model:")],
        key=lambda x: x.get("title", ""),
    )
    standards_list = [p for p in pages if "Standards" in p.get("title", "") and "What Good" in p.get("title", "")]
    standards_map = {s["title"]: s for s in standards_list}

    # Super-model — match spine pages only (not log notes with "Super-Model" in title)
    print("\n=== SPINE ===\n")
    for p in pages:
        if "Super-Model" in p.get("title", "") and p.get("path", "").startswith("spine/"):
            s = _summary_for(p, root, 150)
            print(f"  ★ {p['title']}")
            if s:
                print(f"    {s}")
            print()
            break
    for p in pages:
        if p.get("title") == "Model Registry":
            print(f"  ★ Model Registry — entry point for all {len(models)} models")
            print()
            break
    for p in pages:
        if "Adoption Guide" in p.get("title", "") and p.get("path", "").startswith("spine/"):
            print(f"  ★ {p['title']}")
            print()
            break

    # Models
    print(f"  --- Models ({len(models)}) ---\n")
    for m in models:
        title = m["title"]
        name = title.replace("Model: ", "")
        mat = m.get("maturity", "")
        std = None
        words = name.split()[:2]
        for st in standards_map:
            if any(w in st for w in words):
                std = st
                break
        summary = _summary_for(m, root, 100)
        print(f"  {title} [{mat}]")
        if std:
            print(f"    Standards: {std}")
        if summary:
            print(f"    {summary}")
        print()


def cmd_model(manifest: Dict, root: Path, model_name: str):
    """One model with member pages and references."""
    pages = manifest["pages"]

    # No argument → list all models briefly
    if not model_name:
        return cmd_spine(manifest, root)

    # Find model — fuzzy match against Model: titles and spine pages
    model = None
    for p in pages:
        t = p.get("title", "")
        if model_name.lower() in t.lower() and (
            t.startswith("Model:") or ("Super-Model" in t and p.get("path", "").startswith("spine/"))
        ):
            model = p
            break

    if not model:
        print(f"Model not found: '{model_name}'")
        print("\nAvailable:")
        for p in sorted(pages, key=lambda x: x.get("title", "")):
            if p.get("title", "").startswith("Model:"):
                print(f"  {p['title']}")
        return

    title = model["title"]
    summary = _summary_for(model, root, 200)
    print(f"\n=== {title} ===\n")
    if summary:
        print(f"  {summary}\n")

    rels = model.get("relationships", [])
    if rels:
        print("  Relationships:")
        for r in rels:
            verb = r.get("verb", "")
            for t in _get_targets(r):
                print(f"    {verb}: {t}")
        print()

    inbound = []
    for p in pages:
        if p["title"] == title:
            continue
        for r in p.get("relationships", []):
            for t in _get_targets(r):
                if t == title:
                    inbound.append((p["title"], p.get("type", "")))
    if inbound:
        print(f"  Referenced by ({len(inbound)}):")
        for t, typ in sorted(set(inbound)):
            print(f"    [{typ}] {t}")


def cmd_domain(manifest: Dict, root: Path, domain: str, brief: bool = False):
    """One domain with concept pages."""
    all_domains = sorted(set(p.get("domain", "") for p in manifest["pages"] if p.get("type") == "concept"))
    if domain not in all_domains:
        matches = [d for d in all_domains if domain.lower() in d.lower()]
        if matches:
            domain = matches[0]
        else:
            print(f"Domain not found: '{domain}'")
            print(f"Available: {', '.join(all_domains)}")
            return

    concepts = [p for p in manifest["pages"] if p.get("domain") == domain and p.get("type") == "concept"]
    print(f"\n=== {domain} ({len(concepts)} concept pages) ===\n")
    for p in sorted(concepts, key=lambda x: x.get("title", "")):
        title = p.get("title", "")
        mat = p.get("maturity", "")
        if brief:
            print(f"  {title}" + (f" [{mat}]" if mat else ""))
        else:
            summary = _summary_for(p, root, 120)
            print(f"  {title}" + (f" [{mat}]" if mat else ""))
            if summary:
                print(f"    {summary}")
            print()


def cmd_lessons(manifest: Dict, root: Path):
    """All lessons grouped by category."""
    lessons = [p for p in manifest["pages"] if p.get("type") == "lesson"]
    failure = [l for l in lessons if "failure-lesson" in l.get("tags", [])]
    hub = [l for l in lessons if any(k in l.get("title", "") for k in ["Highest-Connected", "Bridge", "Foundational Domain"])]
    evolved = [l for l in lessons if any(k in l.get("title", "") for k in ["Speculation", "Hub, Not", "Framework, Not", "Systems, Not", "Preach", "Incompleteness"])]
    # Everything else
    seen = set(id(l) for group in [failure, hub, evolved] for l in group)
    other = [l for l in lessons if id(l) not in seen]

    print(f"\n=== LESSONS ({len(lessons)}) ===\n")
    for label, group in [("Failure Lessons", failure), ("Evolved from Directives", evolved),
                          ("Domain Hubs", hub), ("Other", other)]:
        if group:
            print(f"  --- {label} ({len(group)}) ---")
            for l in sorted(group, key=lambda x: x.get("title", "")):
                print(f"    {l['title']}")
            print()


def cmd_decisions(manifest: Dict, root: Path):
    """All decisions with summaries."""
    decisions = [p for p in manifest["pages"] if p.get("type") == "decision"]
    print(f"\n=== DECISIONS ({len(decisions)}) ===\n")
    for d in sorted(decisions, key=lambda x: x.get("title", "")):
        summary = _summary_for(d, root, 150)
        print(f"  {d['title']}")
        if summary:
            print(f"    {summary}")
        print()


def cmd_refs(manifest: Dict, root: Path, query: str):
    """Trace relationships."""
    target = None
    for p in manifest["pages"]:
        if query.lower() in p.get("title", "").lower():
            target = p
            break
    if not target:
        print(f"Page not found: '{query}'")
        return

    title = target["title"]
    print(f"\n=== {title} ===\n")

    rels = target.get("relationships", [])
    if rels:
        print(f"  Points to ({len(rels)}):")
        for r in rels:
            for t in _get_targets(r):
                print(f"    {r.get('verb', 'RELATES TO')}: {t}")

    inbound = []
    for p in manifest["pages"]:
        if p["title"] == title:
            continue
        for r in p.get("relationships", []):
            for t in _get_targets(r):
                if t == title:
                    inbound.append((p["title"], r.get("verb", "")))

    print(f"\n  Pointed to by ({len(inbound)}):")
    for src, verb in sorted(inbound):
        print(f"    {verb}: {src}")


def cmd_search(manifest: Dict, root: Path, query: str, filter_type: Optional[str] = None):
    """Search with ranked results."""
    results = []
    ql = query.lower()
    for p in manifest["pages"]:
        if filter_type and p.get("type") != filter_type:
            continue
        title = p.get("title", "").lower()
        tags = " ".join(p.get("tags", [])).lower()
        score = 0
        if ql in title:
            score += 3
        if ql in tags:
            score += 2
        if score == 0:
            pp = root / "wiki" / p["path"]
            if pp.exists():
                try:
                    if ql in pp.read_text(encoding="utf-8", errors="ignore").lower():
                        score = 1
                except Exception:
                    pass
        if score > 0:
            results.append((score, p))

    results.sort(key=lambda x: -x[0])
    filt = f" (type={filter_type})" if filter_type else ""
    print(f"\n=== Search: '{query}'{filt} — {len(results)} results ===\n")
    for _, p in results[:15]:
        summary = _summary_for(p, root, 100)
        print(f"  [{p.get('type','')}] {p.get('title','')}")
        if summary:
            print(f"    {summary}")
        print()
    if len(results) > 15:
        print(f"  ... +{len(results) - 15} more")


def main():
    parser = argparse.ArgumentParser(description="Browse the wiki knowledge tree")
    parser.add_argument("command", nargs="?", default="tree")
    parser.add_argument("argument", nargs="?", default=None)
    parser.add_argument("--brief", action="store_true")
    parser.add_argument("--type", dest="filter_type")
    args = parser.parse_args()

    root = get_project_root()
    manifest = load_manifest()

    cmds = {
        "tree": lambda: cmd_tree(manifest, root),
        "spine": lambda: cmd_spine(manifest, root),
        "models": lambda: cmd_spine(manifest, root),
        "model": lambda: cmd_model(manifest, root, args.argument or ""),
        "domain": lambda: cmd_domain(manifest, root, args.argument or "", brief=args.brief),
        "lessons": lambda: cmd_lessons(manifest, root),
        "decisions": lambda: cmd_decisions(manifest, root),
        "refs": lambda: cmd_refs(manifest, root, args.argument or ""),
        "search": lambda: cmd_search(manifest, root, args.argument or "", filter_type=args.filter_type),
    }

    fn = cmds.get(args.command)
    if fn:
        fn()
    else:
        # Unknown command → treat as search query
        query = args.command
        if args.argument:
            query = f"{args.command} {args.argument}"
        cmd_search(manifest, root, query, filter_type=args.filter_type)


if __name__ == "__main__":
    main()
