"""Export wiki pages to sister projects.

Config-driven via config/export-profiles.yaml. Supports openfleet (LightRAG)
and aicp (LocalAI Collections) targets. The transform_page() function handles
all profiles uniformly — type/status mapping, metadata injection, resolution
filtering.

Usage:
    python3 tools/export.py openfleet [--dry] [--wiki path] [--profiles path]
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.common import (
    find_wiki_pages,
    get_project_root,
    load_config,
    parse_frontmatter,
    parse_sections,
)

# Confidence ordering for filter comparisons
_CONFIDENCE_ORDER = ["low", "medium", "high", "authoritative"]
# Status ordering for filter comparisons
_STATUS_ORDER = ["raw", "processing", "synthesized", "verified"]

# Which sections to include per resolution level (None = all)
_RESOLUTION_SECTIONS: Dict[str, Optional[List[str]]] = {
    "full": None,
    "condensed": ["Summary", "Key Insights", "Relationships"],
    "minimal": ["Summary", "Relationships"],
}


def transform_page(text: str, profile: Dict[str, Any]) -> str:
    """Transform a wiki page according to the given export profile.

    Steps:
    1. Parse YAML frontmatter
    2. Map type and status via profile transforms
    3. Build metadata header lines from add_metadata config
    4. Apply resolution filter to body sections
    5. Return transformed markdown (no YAML frontmatter)
    """
    meta, body = parse_frontmatter(text)
    transforms = profile.get("transforms", {})

    # --- Type and status mapping ---
    page_type = meta.get("type", "")
    type_map = transforms.get("type_map") or {}
    type_mapped = type_map.get(page_type, page_type)

    page_status = meta.get("status", "")
    status_map = transforms.get("status_map") or {}
    status_mapped = status_map.get(page_status, page_status)

    # Collect source URLs for template substitution
    sources = meta.get("sources") or []
    source_urls = ", ".join(
        s.get("url", "") for s in sources if isinstance(s, dict) and s.get("url")
    )

    updated = str(meta.get("updated", meta.get("created", "")))

    # --- Template variable resolver ---
    def _resolve(value: str) -> str:
        return (
            value
            .replace("{type_mapped}", type_mapped)
            .replace("{status_mapped}", status_mapped)
            .replace("{updated}", updated)
            .replace("{source_urls}", source_urls)
        )

    # --- Build metadata header block ---
    add_metadata = transforms.get("add_metadata") or []
    metadata_lines: List[str] = []
    for entry in add_metadata:
        key = entry.get("key", "")
        value = _resolve(entry.get("value", ""))
        if value:
            metadata_lines.append(f"**{key}:** {value}")

    # --- Apply resolution filter to body sections ---
    resolution = transforms.get("resolution", "full")
    allowed_sections = _RESOLUTION_SECTIONS.get(resolution, None)

    if allowed_sections is not None:
        sections = parse_sections(body)
        filtered_parts: List[str] = []
        for section_name in allowed_sections:
            if section_name in sections:
                filtered_parts.append(f"## {section_name}\n\n{sections[section_name]}")
        body = "\n\n".join(filtered_parts)

    # --- Assemble final output ---
    parts: List[str] = []

    if metadata_lines:
        parts.append("\n".join(metadata_lines))

    if body.strip():
        parts.append(body.strip())

    return "\n\n".join(parts)


def _passes_filters(meta: Dict[str, Any], filters: Dict[str, Any]) -> bool:
    """Return True if page metadata satisfies all export filter criteria.

    Checks:
    - min_confidence: page confidence >= filter threshold
    - min_status: page status >= filter threshold
    - domains: page domain must be in allowed list (if list non-empty)
    - exclude_domains: page domain must NOT be in exclusion list
    """
    if not filters:
        return True

    confidence = meta.get("confidence", "low")
    min_confidence = filters.get("min_confidence")
    if min_confidence:
        conf_idx = _CONFIDENCE_ORDER.index(confidence) if confidence in _CONFIDENCE_ORDER else -1
        min_idx = _CONFIDENCE_ORDER.index(min_confidence) if min_confidence in _CONFIDENCE_ORDER else 0
        if conf_idx < min_idx:
            return False

    status = meta.get("status", "raw")
    min_status = filters.get("min_status")
    if min_status:
        stat_idx = _STATUS_ORDER.index(status) if status in _STATUS_ORDER else -1
        min_idx = _STATUS_ORDER.index(min_status) if min_status in _STATUS_ORDER else 0
        if stat_idx < min_idx:
            return False

    domain = meta.get("domain", "")
    allowed_domains = filters.get("domains") or []
    if allowed_domains and domain not in allowed_domains:
        return False

    exclude_domains = filters.get("exclude_domains") or []
    if exclude_domains and domain in exclude_domains:
        return False

    return True


def export_wiki(
    wiki_dir: Path,
    profile_name: str,
    profiles_path: Path,
    dry_run: bool = False,
) -> List[Dict[str, Any]]:
    """Export wiki pages matching the given profile's filters.

    Returns a list of result dicts with keys: path, status, output_path.
    Status is one of: exported, skipped, error.
    """
    profiles = load_config(profiles_path) or {}
    profile = profiles.get(profile_name)
    if not profile:
        raise ValueError(f"Export profile '{profile_name}' not found in {profiles_path}")

    filters = profile.get("filters", {})
    output_dir_str = profile.get("output_dir", "")

    # Resolve output dir relative to wiki_dir's parent (project root)
    project_root = wiki_dir.parent if wiki_dir.name == "wiki" else wiki_dir
    output_dir = (project_root / output_dir_str).resolve() if output_dir_str else None

    pages = find_wiki_pages(wiki_dir)
    results: List[Dict[str, Any]] = []

    for page_path in pages:
        try:
            text = page_path.read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(text)

            if not _passes_filters(meta, filters):
                results.append({"path": page_path, "status": "skipped", "output_path": None})
                continue

            transformed = transform_page(text, profile)

            if output_dir and not dry_run:
                # Mirror the relative structure under the output dir
                rel = page_path.relative_to(wiki_dir)
                out_path = output_dir / rel
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(transformed, encoding="utf-8")
            else:
                out_path = output_dir / page_path.relative_to(wiki_dir) if output_dir else None

            results.append({"path": page_path, "status": "exported", "output_path": out_path})

        except Exception as exc:  # noqa: BLE001
            results.append({"path": page_path, "status": "error", "output_path": None, "error": str(exc)})

    return results


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Export wiki pages to a sister project.")
    parser.add_argument("profile", help="Export profile name (e.g. openfleet, aicp)")
    parser.add_argument("--dry", action="store_true", help="Dry run — do not write files")
    parser.add_argument("--wiki", default=None, help="Path to wiki directory")
    parser.add_argument("--profiles", default=None, help="Path to export-profiles.yaml")
    args = parser.parse_args()

    project_root = get_project_root()
    wiki_dir = Path(args.wiki) if args.wiki else project_root / "wiki"
    profiles_path = Path(args.profiles) if args.profiles else project_root / "config" / "export-profiles.yaml"

    results = export_wiki(wiki_dir, args.profile, profiles_path, dry_run=args.dry)

    exported = [r for r in results if r["status"] == "exported"]
    skipped = [r for r in results if r["status"] == "skipped"]
    errors = [r for r in results if r["status"] == "error"]

    print(f"Export profile: {args.profile} {'(dry run)' if args.dry else ''}")
    print(f"  Exported: {len(exported)}")
    print(f"  Skipped:  {len(skipped)}")
    print(f"  Errors:   {len(errors)}")

    for r in errors:
        print(f"  ERROR {r['path']}: {r.get('error', '')}")

    if args.dry:
        for r in exported:
            print(f"  [dry] would write: {r['output_path']}")


if __name__ == "__main__":
    main()
