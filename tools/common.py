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
    """Split comma-separated targets, respecting parentheses and [[wikilinks]]."""
    targets: List[str] = []
    current: List[str] = []
    paren_depth = 0
    in_wikilink = False

    i = 0
    while i < len(text):
        # Track [[ ]] wikilink boundaries
        if text[i:i+2] == "[[":
            in_wikilink = True
            current.append("[")
            current.append("[")
            i += 2
            continue
        elif text[i:i+2] == "]]":
            in_wikilink = False
            current.append("]")
            current.append("]")
            i += 2
            continue
        elif text[i] == "(":
            paren_depth += 1
            current.append(text[i])
        elif text[i] == ")":
            paren_depth -= 1
            current.append(text[i])
        elif text[i] == "," and paren_depth == 0 and not in_wikilink:
            targets.append("".join(current).strip())
            current = []
        else:
            current.append(text[i])
        i += 1

    if current:
        targets.append("".join(current).strip())

    # Strip [[ ]] wikilink brackets from targets
    # Handles: [[Target]], [[Target]] (context note), [[Target, With Commas]]
    cleaned = []
    for t in targets:
        t = t.strip()
        # Extract target from [[...]] even if followed by (context)
        wl_match = re.match(r'\[\[(.+?)\]\]', t)
        if wl_match:
            t = wl_match.group(1).strip()
        cleaned.append(t)
    return [t for t in cleaned if t]


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

    Returns a source_type enum value matching config/wiki-schema.yaml.
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

    If the existing _index.md has curated content above ## Pages,
    that content is preserved. Only the ## Pages and ## Tags sections
    are regenerated.
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

    # Preserve curated content above ## Pages if it exists
    curated_header = ""
    index_path = domain_dir / "_index.md"
    if index_path.exists():
        existing = index_path.read_text(encoding="utf-8")
        pages_marker = "\n## Pages\n"
        if pages_marker in existing:
            curated_header = existing[:existing.index(pages_marker)]
        elif "\n## Pages" in existing:
            # Handle ## Pages without trailing newline
            idx = existing.index("\n## Pages")
            curated_header = existing[:idx]

    if curated_header.strip():
        # Use existing curated header
        lines = [curated_header.rstrip(), "", "## Pages", ""]
    else:
        # Generate default header
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


def rebuild_backlog_index(backlog_dir: Path) -> None:
    """Rebuild wiki/backlog/_index.md and wiki/backlog/tasks/_index.md.

    Scans epics/, modules/, and tasks/ for .md files (excluding _index.md).
    Reads frontmatter and rebuilds table-based indexes.
    """
    epics_dir = backlog_dir / "epics"
    tasks_dir = backlog_dir / "tasks"
    today = __import__("datetime").date.today().isoformat()

    # --- Collect epics ---
    epics = []
    if epics_dir.exists():
        for md_file in sorted(epics_dir.glob("*.md")):
            if md_file.name == "_index.md":
                continue
            text = md_file.read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(text)
            if not meta:
                continue
            # Derive ID from filename (e.g. E001-foo.md → E001)
            stem = md_file.stem
            epic_id = stem.split("-")[0].upper() if "-" in stem else stem.upper()
            epics.append({
                "id": epic_id,
                "title": meta.get("title", stem),
                "priority": meta.get("priority", ""),
                "status": meta.get("status", ""),
                "readiness": meta.get("readiness", ""),
            })

    # --- Collect tasks ---
    tasks = []
    if tasks_dir.exists():
        for md_file in sorted(tasks_dir.glob("*.md")):
            if md_file.name == "_index.md":
                continue
            text = md_file.read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(text)
            if not meta:
                continue
            stem = md_file.stem
            task_id = stem.split("-")[0].upper() if "-" in stem else stem.upper()
            tasks.append({
                "id": task_id,
                "title": meta.get("title", stem),
                "priority": meta.get("priority", ""),
                "status": meta.get("status", ""),
                "stage": meta.get("stage", ""),
                "readiness": meta.get("readiness", ""),
                "epic": meta.get("epic", ""),
            })

    # --- Rebuild wiki/backlog/_index.md ---
    # Build filename lookup for epics
    epic_files = {}
    if epics_dir.exists():
        for md_file in sorted(epics_dir.glob("*.md")):
            if md_file.name != "_index.md":
                text = md_file.read_text(encoding="utf-8")
                meta, _ = parse_frontmatter(text)
                if meta and meta.get("title"):
                    epic_files[meta["title"]] = md_file.name

    epic_rows = "\n".join(
        f"| {e['id']} | [{e['title']}](epics/{epic_files.get(e['title'], '')}) | {e['priority']} | {e['status']} | {e['readiness']} |"
        if e['title'] in epic_files else
        f"| {e['id']} | {e['title']} | {e['priority']} | {e['status']} | {e['readiness']} |"
        for e in epics
    ) or "<!-- No epics yet -->"

    backlog_index_content = f"""---
title: "Backlog"
type: index
domain: backlog
status: active
confidence: high
created: 2026-04-09
updated: {today}
sources: []
tags: [backlog, planning, epics, roadmap]
---

# Backlog

All planned work, organized by epics, modules, and tasks.

## Epics

| ID | Epic | Priority | Status | Readiness |
|----|------|----------|--------|-----------|
{epic_rows}

## Modules

See [modules/](modules/)

## Tasks

See [tasks/_index.md](tasks/_index.md)
"""
    backlog_index_path = backlog_dir / "_index.md"
    backlog_index_path.write_text(backlog_index_content, encoding="utf-8")

    # --- Rebuild wiki/backlog/tasks/_index.md ---
    # Build filename lookup for tasks
    task_files = {}
    if tasks_dir.exists():
        for md_file in sorted(tasks_dir.glob("*.md")):
            if md_file.name != "_index.md":
                text = md_file.read_text(encoding="utf-8")
                meta, _ = parse_frontmatter(text)
                if meta and meta.get("title"):
                    task_files[meta["title"]] = md_file.name

    task_rows = "\n".join(
        f"| {t['id']} | [{t['title']}]({task_files.get(t['title'], '')}) | {t['priority']} | {t['status']} | {t['stage']} | {t['readiness']} | {t['epic']} |"
        if t['title'] in task_files else
        f"| {t['id']} | {t['title']} | {t['priority']} | {t['status']} | {t['stage']} | {t['readiness']} | {t['epic']} |"
        for t in tasks
    ) or "<!-- No tasks yet -->"

    tasks_index_content = f"""---
title: "Tasks"
type: index
domain: backlog
status: active
confidence: high
created: 2026-04-09
updated: {today}
sources: []
tags: [backlog, tasks]
---

# Tasks

| ID | Task | Priority | Status | Stage | Readiness | Epic |
|----|------|----------|--------|-------|-----------|------|
{task_rows}
"""
    tasks_index_path = tasks_dir / "_index.md"
    tasks_index_path.write_text(tasks_index_content, encoding="utf-8")


def rebuild_log_index(log_dir: Path) -> None:
    """Rebuild wiki/log/_index.md with a chronological table of log entries.

    Scans log_dir for .md files (excluding _index.md). Reads frontmatter.
    Table columns: Date, Title, Type (note_type), Tags.
    """
    today = __import__("datetime").date.today().isoformat()

    entries = []
    for md_file in sorted(log_dir.glob("*.md"), reverse=True):
        if md_file.name == "_index.md":
            continue
        text = md_file.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        if not meta:
            continue
        date = str(meta.get("created", md_file.stem[:10] if len(md_file.stem) >= 10 else ""))
        title = meta.get("title", md_file.stem)
        note_type = meta.get("note_type", meta.get("type", ""))
        tags = meta.get("tags", [])
        tags_str = ", ".join(f"`{t}`" for t in tags) if tags else ""
        entries.append({
            "date": date,
            "title": title,
            "type": note_type,
            "tags": tags_str,
            "file": md_file.name,
        })

    rows = "\n".join(
        f"| {e['date']} | [{e['title']}]({e['file']}) | {e['type']} | {e['tags']} |"
        for e in entries
    ) or "<!-- No log entries yet -->"

    content = f"""---
title: "Log"
type: index
domain: log
status: active
confidence: high
created: 2026-04-09
updated: {today}
sources: []
tags: [log, directives, sessions]
---

# Log

Operator directives, session summaries, and task completion notes.

## Entries

| Date | Title | Type | Tags |
|------|-------|------|------|
{rows}
"""
    log_index_path = log_dir / "_index.md"
    log_index_path.write_text(content, encoding="utf-8")
