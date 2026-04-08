"""Schema validation for wiki pages.

Validates YAML frontmatter against config/schema.yaml, checks required
sections per page type, and validates relationship verbs.

Usage:
    python3 tools/validate.py                    # Validate all wiki/ pages
    python3 tools/validate.py path/to/page.md    # Validate one page
    python3 tools/validate.py --json             # JSON output

Exit code: 0 if no errors, 1 if errors found.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from tools.common import (
    find_wiki_pages,
    get_project_root,
    load_config,
    parse_frontmatter,
    parse_relationships,
    parse_sections,
    word_count,
)


def validate_page(
    page_path: Path, schema_path: Path
) -> Dict[str, Any]:
    """Validate a single wiki page against schema.

    Returns {"file": str, "errors": [...], "warnings": [...]}.
    Each error/warning has "code", "message", and optional "field".
    """
    errors: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []
    result = {
        "file": str(page_path),
        "errors": errors,
        "warnings": warnings,
    }

    schema = load_config(schema_path)
    if schema is None:
        errors.append({"code": "schema_missing", "message": f"Schema not found: {schema_path}"})
        return result

    text = page_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    if not meta:
        errors.append({"code": "no_frontmatter", "message": "No YAML frontmatter found"})
        return result

    # Check required fields
    for field in schema.get("required_fields", []):
        if field not in meta:
            errors.append({
                "code": "missing_field",
                "message": f"Required field missing: {field}",
                "field": field,
            })
        elif meta[field] is None or meta[field] == "":
            errors.append({
                "code": "empty_field",
                "message": f"Required field is empty: {field}",
                "field": field,
            })

    # Check enum values
    enums = schema.get("enums", {})
    for field, allowed in enums.items():
        if field in meta and meta[field] not in allowed:
            errors.append({
                "code": "invalid_enum",
                "message": f"Invalid value for {field}: '{meta[field]}' (allowed: {allowed})",
                "field": field,
            })

    # Check sources
    sources = meta.get("sources", [])
    if isinstance(sources, list):
        src_required = schema.get("source_required_fields", [])
        src_needs_one = schema.get("source_needs_one_of", [])
        for i, src in enumerate(sources):
            if not isinstance(src, dict):
                errors.append({"code": "invalid_source", "message": f"Source {i} is not a dict"})
                continue
            for sf in src_required:
                if sf not in src:
                    errors.append({
                        "code": "source_missing_field",
                        "message": f"Source {i} missing required field: {sf}",
                    })
            if src_needs_one and not any(sf in src for sf in src_needs_one):
                errors.append({
                    "code": "source_missing_ref",
                    "message": f"Source {i} needs at least one of: {src_needs_one}",
                })
            if "type" in src and src["type"] not in enums.get("source_type", []):
                warnings.append({
                    "code": "invalid_source_type",
                    "message": f"Source {i} has unrecognized type: '{src['type']}'",
                })

    # Check required sections
    page_type = meta.get("type", "")
    required_secs = schema.get("required_sections", {}).get(page_type, [])
    sections = parse_sections(body)
    for sec in required_secs:
        if sec not in sections:
            errors.append({
                "code": "missing_section",
                "message": f"Required section missing for type '{page_type}': ## {sec}",
            })

    # Check title consistency
    title = meta.get("title", "")
    first_heading = None
    for line in body.split("\n"):
        if line.startswith("# ") and not line.startswith("## "):
            first_heading = line[2:].strip()
            break
    if title and first_heading and title != first_heading:
        warnings.append({
            "code": "title_mismatch",
            "message": f"Frontmatter title '{title}' != heading '{first_heading}'",
        })

    # Check relationships
    rel_text = sections.get("Relationships", "")
    if rel_text:
        rels = parse_relationships(rel_text)
        allowed_verbs = schema.get("relationship_verbs", [])
        for rel in rels:
            if rel["verb"] not in allowed_verbs:
                warnings.append({
                    "code": "invalid_verb",
                    "message": f"Unrecognized relationship verb: '{rel['verb']}'",
                })

    # Check summary word count
    summary = sections.get("Summary", "")
    if summary and word_count(summary) < 10:
        warnings.append({
            "code": "thin_summary",
            "message": f"Summary is very short ({word_count(summary)} words)",
        })

    return result


def validate_wiki(
    wiki_dir: Path, schema_path: Path
) -> List[Dict[str, Any]]:
    """Validate all .md files in a directory."""
    results = []
    for md_file in sorted(wiki_dir.rglob("*.md")):
        if md_file.name.startswith("_"):
            continue
        results.append(validate_page(md_file, schema_path))
    return results


def main():
    parser = argparse.ArgumentParser(description="Validate wiki pages against schema")
    parser.add_argument("path", nargs="?", help="Page or directory to validate")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--schema", help="Path to schema.yaml")
    args = parser.parse_args()

    root = get_project_root()
    schema_path = Path(args.schema) if args.schema else root / "config" / "schema.yaml"

    if args.path:
        target = Path(args.path)
        if target.is_file():
            results = [validate_page(target, schema_path)]
        else:
            results = validate_wiki(target, schema_path)
    else:
        results = validate_wiki(root / "wiki", schema_path)

    total_errors = sum(len(r["errors"]) for r in results)
    total_warnings = sum(len(r["warnings"]) for r in results)

    if args.json:
        print(json.dumps({"results": results, "total_errors": total_errors, "total_warnings": total_warnings}, indent=2))
    else:
        for r in results:
            if r["errors"] or r["warnings"]:
                print(f"\n{r['file']}:")
                for e in r["errors"]:
                    print(f"  ERROR [{e['code']}]: {e['message']}")
                for w in r["warnings"]:
                    print(f"  WARN  [{w['code']}]: {w['message']}")
        print(f"\n{'PASS' if total_errors == 0 else 'FAIL'}: {len(results)} files, {total_errors} errors, {total_warnings} warnings")

    sys.exit(0 if total_errors == 0 else 1)


if __name__ == "__main__":
    main()
