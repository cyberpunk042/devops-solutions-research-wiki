"""Manifest JSON builder for the DevOps Solutions Research Wiki.

Scans all wiki .md files (excluding _index.md), extracts frontmatter
and relationships, and emits a machine-readable graph index with:
  - page list with metadata and relationships
  - domain index (page_count, relationship_count)
  - tag index (tag -> [page slugs])
  - orphaned reference detection
  - summary stats
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set

# Allow running as a script directly (python tools/manifest.py)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.common import (
    find_wiki_pages,
    get_project_root,
    parse_frontmatter,
    parse_relationships,
    parse_sections,
)

# Strip trailing parenthetical context for orphan-detection title matching.
# e.g. "Serverless Patterns (different trade-offs)" -> "Serverless Patterns"
_PAREN_SUFFIX = re.compile(r"\s*\([^)]*\)\s*$")


def _strip_context(target: str) -> str:
    """Remove trailing parenthetical context from a relationship target."""
    return _PAREN_SUFFIX.sub("", target).strip()


def _page_slug(path: Path, wiki_dir: Path) -> str:
    """Return a slash-separated relative path string (without .md extension)."""
    try:
        rel = path.relative_to(wiki_dir)
    except ValueError:
        rel = path
    return str(rel.with_suffix(""))


def build_manifest(wiki_dir: Path) -> Dict[str, Any]:
    """Scan wiki_dir for .md pages and build the manifest dictionary.

    Args:
        wiki_dir: Root directory to search for wiki pages.

    Returns:
        Manifest dict with generated timestamp, stats, pages list,
        domain index, tag index, and orphaned_refs list.
    """
    pages_meta: List[Dict[str, Any]] = []
    all_titles: Set[str] = set()
    domain_data: Dict[str, Dict[str, int]] = {}
    tag_index: Dict[str, List[str]] = {}

    # First pass: collect all page titles for orphan detection
    md_files = find_wiki_pages(wiki_dir)
    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        title = meta.get("title", "")
        if title:
            all_titles.add(title)

    # Second pass: build full page records
    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)

        title = meta.get("title", md_file.stem)
        page_type = meta.get("type", "")
        domain = meta.get("domain", "")
        tags = meta.get("tags", []) or []
        status = meta.get("status", "")
        confidence = meta.get("confidence", "")
        created = str(meta.get("created", ""))
        updated = str(meta.get("updated", ""))
        sources = meta.get("sources", []) or []
        slug = _page_slug(md_file, wiki_dir)

        # Parse relationships from ## Relationships section
        sections = parse_sections(body)
        rel_text = sections.get("Relationships", "")
        raw_rels = parse_relationships(rel_text)

        relationships: List[Dict[str, Any]] = []
        for rel in raw_rels:
            for target in rel["targets"]:
                relationships.append({"verb": rel["verb"], "target": target})

        page_record: Dict[str, Any] = {
            "path": str(md_file.relative_to(wiki_dir)),
            "slug": slug,
            "title": title,
            "type": page_type,
            "domain": domain,
            "status": status,
            "confidence": confidence,
            "created": created,
            "updated": updated,
            "tags": tags,
            "sources": sources,
            "relationships": relationships,
        }
        pages_meta.append(page_record)

        # Update domain index
        if domain:
            if domain not in domain_data:
                domain_data[domain] = {"page_count": 0, "relationship_count": 0}
            domain_data[domain]["page_count"] += 1
            domain_data[domain]["relationship_count"] += len(relationships)

        # Update tag index
        for tag in tags:
            tag_index.setdefault(tag, []).append(slug)

    # Orphaned reference detection
    # A ref is orphaned if no page title matches the stripped target
    orphan_map: Dict[str, List[str]] = {}  # target -> list of referencing page titles
    for page in pages_meta:
        for rel in page["relationships"]:
            bare_target = _strip_context(rel["target"])
            if bare_target and bare_target not in all_titles:
                orphan_map.setdefault(bare_target, []).append(page["title"])

    orphaned_refs = [
        {"target": target, "referenced_by": referrers}
        for target, referrers in sorted(orphan_map.items())
    ]

    # Stats
    total_relationships = sum(len(p["relationships"]) for p in pages_meta)
    concept_pages = [p for p in pages_meta if p["type"] == "concept"]
    source_pages = [p for p in pages_meta if p["type"] == "source-synthesis"]
    comparison_pages = [p for p in pages_meta if p["type"] == "comparison"]

    stats: Dict[str, int] = {
        "pages": len(pages_meta),
        "domains": len(domain_data),
        "sources": len(source_pages),
        "comparisons": len(comparison_pages),
        "relationships": total_relationships,
        "tags_unique": len(tag_index),
    }

    return {
        "generated": datetime.now(timezone.utc).isoformat(),
        "stats": stats,
        "pages": pages_meta,
        "domains": domain_data,
        "tags": tag_index,
        "orphaned_refs": orphaned_refs,
    }


def main() -> None:
    """CLI entry point for manifest builder."""
    parser = argparse.ArgumentParser(
        description="Build manifest.json from wiki .md files."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Wiki directory to scan (default: wiki/ under project root)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file path (default: stdout)",
    )
    args = parser.parse_args()

    if args.path:
        wiki_dir = Path(args.path).resolve()
    else:
        wiki_dir = get_project_root() / "wiki"

    if not wiki_dir.exists():
        print(f"Error: directory not found: {wiki_dir}", file=sys.stderr)
        sys.exit(1)

    manifest = build_manifest(wiki_dir)
    output_json = json.dumps(manifest, indent=2, default=str)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_json, encoding="utf-8")
        print(
            f"Manifest written to {out_path} ({manifest['stats']['pages']} pages)",
            file=sys.stderr,
        )
    else:
        print(output_json)


if __name__ == "__main__":
    main()
