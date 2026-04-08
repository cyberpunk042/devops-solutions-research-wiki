"""Shared utilities for wiki tools.

Provides YAML frontmatter parsing, section extraction, relationship parsing,
and config file loading. Used by validate.py, manifest.py, lint.py, export.py,
and stats.py.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter from markdown text.

    Returns (metadata_dict, body_text). If no frontmatter found,
    returns ({}, full_text).
    """
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    yaml_str = parts[1].strip()
    body = parts[2].strip()

    if not yaml_str:
        return {}, body

    try:
        meta = yaml.safe_load(yaml_str)
        if not isinstance(meta, dict):
            return {}, text
        return meta, body
    except yaml.YAMLError:
        return {}, text


def parse_sections(body: str) -> Dict[str, str]:
    """Parse markdown body into {section_name: content} dict.

    Splits on ## headings. The heading text becomes the key,
    everything until the next ## becomes the value.
    """
    sections: Dict[str, str] = {}
    current_section = None
    current_lines: List[str] = []

    for line in body.split("\n"):
        match = re.match(r"^## (.+)$", line)
        if match:
            if current_section is not None:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = match.group(1).strip()
            current_lines = []
        elif current_section is not None:
            current_lines.append(line)

    if current_section is not None:
        sections[current_section] = "\n".join(current_lines).strip()

    return sections


_REL_PATTERN = re.compile(r"^-\s*([A-Z][A-Z /\-]+?):\s*(.+)$")


def parse_relationships(text: str) -> List[Dict[str, Any]]:
    """Parse ## Relationships section content into structured list.

    Each line like '- VERB: target1, target2 (context)' becomes:
    {"verb": "VERB", "targets": ["target1", "target2 (context)"], "raw": "..."}

    Comma splitting is smart: only splits on commas NOT inside parentheses.
    """
    rels: List[Dict[str, Any]] = []
    for line in text.split("\n"):
        line = line.strip()
        match = _REL_PATTERN.match(line)
        if match:
            verb = match.group(1).strip()
            targets_raw = match.group(2).strip()
            targets = _split_targets(targets_raw)
            rels.append({
                "verb": verb,
                "targets": targets,
                "raw": line,
            })
    return rels


def _split_targets(text: str) -> List[str]:
    """Split comma-separated targets, respecting parentheses."""
    targets: List[str] = []
    current: List[str] = []
    depth = 0

    for char in text:
        if char == "(":
            depth += 1
            current.append(char)
        elif char == ")":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            targets.append("".join(current).strip())
            current = []
        else:
            current.append(char)

    if current:
        targets.append("".join(current).strip())

    return [t for t in targets if t]


def load_config(path: Path) -> Optional[Dict[str, Any]]:
    """Load a YAML config file. Returns None if file doesn't exist."""
    if not path.exists():
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def find_wiki_pages(wiki_dir: Path) -> List[Path]:
    """Find all .md files in wiki/ excluding _index.md files."""
    pages = []
    for md_file in sorted(wiki_dir.rglob("*.md")):
        if md_file.name == "_index.md":
            continue
        pages.append(md_file)
    return pages


def find_all_wiki_files(wiki_dir: Path) -> List[Path]:
    """Find all .md files in wiki/ including _index.md files."""
    return sorted(wiki_dir.rglob("*.md"))


def get_project_root() -> Path:
    """Get the project root (directory containing CLAUDE.md or .git)."""
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / "CLAUDE.md").exists() or (parent / ".git").exists():
            return parent
    return current


def word_count(text: str) -> int:
    """Count words in text, stripping markdown formatting."""
    clean = re.sub(r"[#*_`\[\]\(\)]", "", text)
    return len(clean.split())


def detect_source_type(filename: str) -> str:
    """Detect source type from filename and extension.

    Returns a source_type enum value matching config/schema.yaml.
    """
    lower = filename.lower()
    ext = Path(filename).suffix.lower()

    if ext == ".pdf":
        return "paper"
    if ext in (".mp3", ".wav", ".ogg"):
        return "podcast-transcript"
    if "transcript" in lower:
        return "youtube-transcript"
    if ext in (".md", ".txt", ".html", ".htm"):
        if any(kw in lower for kw in ("note", "journal", "thought", "idea")):
            return "notes"
        return "article"
    return "article"


def rebuild_domain_index(domain_dir: Path, domain_name: str, description: str) -> str:
    """Rebuild a domain _index.md from its wiki pages.

    Scans all .md files in domain_dir (excluding _index.md),
    returns the regenerated _index.md content.
    """
    pages_info = []
    all_tags: list = []

    for md_file in sorted(domain_dir.glob("*.md")):
        if md_file.name == "_index.md":
            continue
        text = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        if not meta:
            continue
        title = meta.get("title", md_file.stem)
        sections = parse_sections(body)
        summary = sections.get("Summary", "").split(".")[0].strip()
        if len(summary) > 120:
            summary = summary[:117] + "..."
        pages_info.append({"file": md_file.name, "title": title, "summary": summary})
        for tag in meta.get("tags", []):
            all_tags.append(tag)

    lines = [
        f"# {domain_name.replace('-', ' ').title()}",
        "",
        description,
        "",
        "## Pages",
        "",
    ]

    if pages_info:
        for p in pages_info:
            lines.append(f"- [{p['title']}]({p['file']}) — {p['summary']}")
    else:
        lines.append("<!-- Pages added during ingestion -->")

    lines.extend(["", "## Tags", ""])
    if all_tags:
        tag_counts = {}
        for t in all_tags:
            tag_counts[t] = tag_counts.get(t, 0) + 1
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        lines.append(", ".join(f"`{t}`" for t, _ in sorted_tags[:20]))
    else:
        lines.append("<!-- Tag cloud generated during ingestion -->")

    return "\n".join(lines) + "\n"


def rebuild_layer_index(layer_dir: Path, layer_name: str, description: str) -> str:
    """Rebuild a layer _index.md (lessons/, patterns/, decisions/, spine/).

    Same logic as rebuild_domain_index but for non-domain directories.
    """
    return rebuild_domain_index(layer_dir, layer_name, description)
