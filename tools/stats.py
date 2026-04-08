"""Wiki coverage and growth reporting.

Usage:
    python3 tools/stats.py             # Human-readable report
    python3 tools/stats.py --json      # JSON output
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict

from tools.common import get_project_root, load_config
from tools.manifest import build_manifest


def build_stats(wiki_dir: Path) -> Dict[str, Any]:
    """Build statistics from wiki content."""
    manifest = build_manifest(wiki_dir)
    pages = manifest["pages"]

    by_type = Counter(p["type"] for p in pages)
    by_domain = Counter(p["domain"] for p in pages)
    by_status = Counter(p["status"] for p in pages)
    by_confidence = Counter(p["confidence"] for p in pages)

    rel_counts = [(p["title"], len(p["relationships"])) for p in pages]
    rel_counts.sort(key=lambda x: x[1], reverse=True)
    avg_rels = sum(c for _, c in rel_counts) / max(len(rel_counts), 1)

    all_tags = []
    for p in pages:
        all_tags.extend(p.get("tags", []))
    tag_counts = Counter(all_tags).most_common(20)

    now = datetime.now()
    freshness = {"<7d": 0, "<30d": 0, "<90d": 0, ">90d": 0, "unknown": 0}
    for p in pages:
        updated = p.get("updated", "")
        if not updated:
            freshness["unknown"] += 1
            continue
        try:
            dt = datetime.strptime(updated[:10], "%Y-%m-%d")
            age = (now - dt).days
            if age < 7:
                freshness["<7d"] += 1
            elif age < 30:
                freshness["<30d"] += 1
            elif age < 90:
                freshness["<90d"] += 1
            else:
                freshness[">90d"] += 1
        except ValueError:
            freshness["unknown"] += 1

    domain_gaps = {}
    orphaned = manifest.get("orphaned_refs", [])
    orphan_by_referrer_domain = defaultdict(int)
    for o in orphaned:
        for ref_title in o["referenced_by"]:
            for p in pages:
                if p["title"] == ref_title:
                    orphan_by_referrer_domain[p["domain"]] += 1

    for domain, count in by_domain.items():
        total_rels = sum(len(p["relationships"]) for p in pages if p["domain"] == domain)
        orphan_count = orphan_by_referrer_domain.get(domain, 0)
        gap_score = orphan_count / max(total_rels, 1)
        domain_gaps[domain] = {
            "pages": count,
            "relationships": total_rels,
            "orphaned_refs": orphan_count,
            "gap_score": round(gap_score, 3),
        }

    by_layer = Counter()
    by_maturity = Counter()
    for p in pages:
        layer = p.get("layer")
        if layer is not None:
            by_layer[str(layer)] += 1
        mat = p.get("maturity")
        if mat:
            by_maturity[mat] += 1

    return {
        "total_pages": len(pages),
        "by_type": dict(by_type),
        "by_domain": dict(by_domain),
        "by_status": dict(by_status),
        "by_confidence": dict(by_confidence),
        "by_layer": dict(by_layer),
        "by_maturity": dict(by_maturity),
        "relationship_density": {
            "average_per_page": round(avg_rels, 1),
            "most_connected": rel_counts[:5] if rel_counts else [],
            "least_connected": rel_counts[-5:] if rel_counts else [],
        },
        "tag_cloud": tag_counts,
        "freshness": freshness,
        "domain_gaps": domain_gaps,
        "orphaned_refs_total": len(orphaned),
    }


def main():
    parser = argparse.ArgumentParser(description="Wiki coverage and growth report")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--wiki", help="Wiki directory path")
    args = parser.parse_args()

    root = get_project_root()
    wiki_dir = Path(args.wiki) if args.wiki else root / "wiki"

    stats = build_stats(wiki_dir)

    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        print("=== Wiki Stats ===")
        print(f"Total pages: {stats['total_pages']}")
        print(f"\nBy type: {json.dumps(stats['by_type'], indent=2)}")
        print(f"\nBy domain: {json.dumps(stats['by_domain'], indent=2)}")
        print(f"\nBy status: {json.dumps(stats['by_status'], indent=2)}")
        print(f"\nBy confidence: {json.dumps(stats['by_confidence'], indent=2)}")
        print(f"\nRelationship density: {stats['relationship_density']['average_per_page']} avg/page")
        if stats['relationship_density']['most_connected']:
            print(f"  Most connected: {stats['relationship_density']['most_connected'][:3]}")
        print(f"\nTop tags: {stats['tag_cloud'][:10]}")
        print(f"\nFreshness: {json.dumps(stats['freshness'], indent=2)}")
        print(f"\nOrphaned refs: {stats['orphaned_refs_total']}")
        if stats["by_layer"]:
            print(f"\nBy layer: {json.dumps(stats['by_layer'], indent=2)}")
        if stats["by_maturity"]:
            print(f"\nBy maturity: {json.dumps(stats['by_maturity'], indent=2)}")
        print(f"\nDomain gaps:")
        for d, g in stats["domain_gaps"].items():
            print(f"  {d}: {g['pages']} pages, gap score {g['gap_score']}")


if __name__ == "__main__":
    main()
