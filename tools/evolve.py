"""Evolution engine for the DevOps Solutions Research Wiki.

Scores existing pages to find candidates for higher-layer synthesis
(lessons, patterns, decisions), builds prompts, and delegates to LLM
backends for content generation.

Usage:
    python3 -m tools.evolve score [--top N] [--type TYPE] [--domain DOMAIN]
    python3 -m tools.evolve scaffold [--top N] [--type TYPE]
    python3 -m tools.evolve dry-run [--top N]
    python3 -m tools.evolve auto [--backend NAME] [--top N]
    python3 -m tools.evolve execute [--clear]
    python3 -m tools.evolve review
    python3 -m tools.evolve stale
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.common import (
    find_wiki_pages,
    get_project_root,
    load_config,
    parse_frontmatter,
    parse_sections,
    parse_relationships,
    word_count,
)
from tools.manifest import build_manifest


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Signal:
    """A scoring signal contributing to a candidate's total score."""
    name: str
    score: float  # 0.0 - 1.0
    detail: str


@dataclass
class Candidate:
    """An evolution candidate — a proposed new higher-layer page."""
    type: str           # "lesson", "pattern", "decision"
    title: str
    score: float        # 0.0 - 1.0 (aggregated weighted score)
    signals: List[Signal]
    source_pages: List[str]
    domain: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Signal weights — must sum to 1.0
SIGNAL_WEIGHTS: Dict[str, float] = {
    "tag_cooccurrence":         0.25,
    "cross_source_convergence": 0.25,
    "relationship_hub":         0.15,
    "domain_layer_gap":         0.15,
    "open_question_density":    0.10,
    "orphaned_references":      0.10,
}


# ---------------------------------------------------------------------------
# Scoring signal functions
# ---------------------------------------------------------------------------

def _signal_tag_cooccurrence(pages: List[Dict[str, Any]]) -> List["Candidate"]:
    """Find groups of 3+ pages sharing 2+ tags → pattern candidates."""
    weight = SIGNAL_WEIGHTS["tag_cooccurrence"]
    candidates: List[Candidate] = []

    # Build tag → pages index
    tag_to_pages: Dict[str, List[Dict[str, Any]]] = {}
    for page in pages:
        for tag in page.get("tags", []):
            tag_to_pages.setdefault(tag, []).append(page)

    # Find pairs of tags with 3+ shared pages
    tags = list(tag_to_pages.keys())
    seen_groups: Dict[frozenset, bool] = {}

    for i, t1 in enumerate(tags):
        for t2 in tags[i + 1:]:
            pages_t1 = set(p["title"] for p in tag_to_pages[t1])
            pages_t2 = set(p["title"] for p in tag_to_pages[t2])
            shared_titles = pages_t1 & pages_t2
            if len(shared_titles) >= 3:
                group_key = frozenset(shared_titles)
                if group_key in seen_groups:
                    continue
                seen_groups[group_key] = True

                shared_count = len(shared_titles)
                raw_score = min(shared_count / 5, 1.0) * weight

                # Determine domain from most common domain among source pages
                source_page_objs = [p for p in pages if p["title"] in shared_titles]
                domain = _most_common_domain(source_page_objs)

                title = f"Pattern: {t1.title()} + {t2.title()}"
                signal = Signal(
                    name="tag_cooccurrence",
                    score=raw_score,
                    detail=f"{shared_count} pages share tags '{t1}' and '{t2}': {', '.join(sorted(shared_titles)[:5])}",
                )
                candidates.append(Candidate(
                    type="pattern",
                    title=title,
                    score=raw_score,
                    signals=[signal],
                    source_pages=sorted(shared_titles),
                    domain=domain,
                ))

    return candidates


def _signal_cross_source_convergence(pages: List[Dict[str, Any]]) -> List["Candidate"]:
    """Source-synthesis pages referencing same concept pages → lesson candidates."""
    weight = SIGNAL_WEIGHTS["cross_source_convergence"]
    candidates: List[Candidate] = []

    source_pages = [p for p in pages if p.get("type") == "source-synthesis"]

    # Build concept → list of source-synthesis pages that reference it
    concept_to_sources: Dict[str, List[str]] = {}
    for sp in source_pages:
        for rel in sp.get("relationships", []):
            target = rel.get("target", "")
            if target:
                concept_to_sources.setdefault(target, []).append(sp["title"])

    for concept, sources in concept_to_sources.items():
        # Deduplicate
        sources = list(set(sources))
        if len(sources) < 2:
            continue

        source_count = len(sources)
        raw_score = min(source_count / 4, 1.0) * weight

        # Find the concept page for domain info
        concept_page_objs = [p for p in pages if p["title"] == concept]
        domain = _most_common_domain(concept_page_objs) if concept_page_objs else "cross-domain"

        signal = Signal(
            name="cross_source_convergence",
            score=raw_score,
            detail=f"{source_count} source-synthesis pages reference '{concept}': {', '.join(sorted(sources)[:4])}",
        )
        candidates.append(Candidate(
            type="lesson",
            title=f"Lesson: Convergence on {concept}",
            score=raw_score,
            signals=[signal],
            source_pages=sources + ([concept] if concept_page_objs else []),
            domain=domain,
        ))

    return candidates


def _signal_relationship_hub(pages: List[Dict[str, Any]]) -> List["Candidate"]:
    """Pages with 5+ inbound relationships → lesson candidates.

    Skip pages already at Layer 4+.
    """
    weight = SIGNAL_WEIGHTS["relationship_hub"]
    candidates: List[Candidate] = []

    # Build inbound relationship count (title → set of pages referencing it)
    inbound: Dict[str, List[str]] = {}
    for page in pages:
        for rel in page.get("relationships", []):
            target = rel.get("target", "")
            if target:
                inbound.setdefault(target, []).append(page["title"])

    title_to_page = {p["title"]: p for p in pages}

    for target_title, referrers in inbound.items():
        target_page = title_to_page.get(target_title)
        if target_page:
            # Skip pages already at Layer 4+
            layer = target_page.get("layer", "")
            try:
                if layer and int(str(layer)) >= 4:
                    continue
            except (ValueError, TypeError):
                pass

        inbound_count = len(referrers)
        if inbound_count < 5:
            continue

        raw_score = min(inbound_count / 10, 1.0) * weight

        domain = "cross-domain"
        if target_page:
            domain = target_page.get("domain", "cross-domain") or "cross-domain"

        signal = Signal(
            name="relationship_hub",
            score=raw_score,
            detail=f"'{target_title}' has {inbound_count} inbound relationships from: {', '.join(sorted(referrers)[:5])}",
        )
        candidates.append(Candidate(
            type="lesson",
            title=f"Lesson: Hub — {target_title}",
            score=raw_score,
            signals=[signal],
            source_pages=[target_title] + sorted(referrers),
            domain=domain,
        ))

    return candidates


def _signal_domain_layer_gap(pages: List[Dict[str, Any]]) -> List["Candidate"]:
    """Domains with 3+ Layer 1-2 pages but no Layer 4-6 → lesson candidates."""
    weight = SIGNAL_WEIGHTS["domain_layer_gap"]
    candidates: List[Candidate] = []

    # Group pages by domain
    domain_pages: Dict[str, List[Dict[str, Any]]] = {}
    for page in pages:
        domain = page.get("domain", "")
        if domain:
            domain_pages.setdefault(domain, []).append(page)

    for domain, dpages in domain_pages.items():
        low_layer_pages = []
        has_high_layer = False

        for p in dpages:
            layer = p.get("layer", "")
            try:
                layer_int = int(str(layer)) if layer else 0
            except (ValueError, TypeError):
                layer_int = 0

            if layer_int >= 4:
                has_high_layer = True
            elif layer_int in (1, 2) or layer_int == 0:
                # Layer 0 (unlayered) counts as base layer
                low_layer_pages.append(p)

        if has_high_layer:
            continue
        if len(low_layer_pages) < 3:
            continue

        low_count = len(low_layer_pages)
        raw_score = min(low_count / 8, 1.0) * weight

        source_titles = [p["title"] for p in low_layer_pages]
        signal = Signal(
            name="domain_layer_gap",
            score=raw_score,
            detail=f"Domain '{domain}' has {low_count} base-layer pages but no evolved pages (Layer 4+)",
        )
        candidates.append(Candidate(
            type="lesson",
            title=f"Lesson: Synthesize {domain.replace('-', ' ').title()} Knowledge",
            score=raw_score,
            signals=[signal],
            source_pages=source_titles[:10],
            domain=domain,
        ))

    return candidates


def _signal_open_question_density(pages: List[Dict[str, Any]],
                                  gaps: Optional[Dict[str, Any]] = None) -> List["Candidate"]:
    """Pages contributing 3+ open questions → decision candidates."""
    weight = SIGNAL_WEIGHTS["open_question_density"]
    candidates: List[Candidate] = []

    if not gaps:
        return candidates

    # Aggregate open questions per source page
    page_questions: Dict[str, List[str]] = {}
    for oq in gaps.get("open_questions", []):
        source = oq.get("source_page", "")
        question = oq.get("question", "")
        if source and question:
            page_questions.setdefault(source, []).append(question)

    for source_page_title, questions in page_questions.items():
        question_count = len(questions)
        if question_count < 3:
            continue

        raw_score = min(question_count / 6, 1.0) * weight

        # Find domain of the source page
        source_page_obj = next((p for p in pages if p["title"] == source_page_title), None)
        domain = source_page_obj.get("domain", "cross-domain") if source_page_obj else "cross-domain"

        signal = Signal(
            name="open_question_density",
            score=raw_score,
            detail=f"'{source_page_title}' has {question_count} open questions: {'; '.join(questions[:3])}",
        )
        candidates.append(Candidate(
            type="decision",
            title=f"Decision: Resolve Open Questions in {source_page_title}",
            score=raw_score,
            signals=[signal],
            source_pages=[source_page_title],
            domain=domain,
        ))

    return candidates


def _signal_orphaned_references(pages: List[Dict[str, Any]],
                                gaps: Optional[Dict[str, Any]] = None) -> List["Candidate"]:
    """Orphaned targets referenced by 2+ pages → lesson candidates."""
    weight = SIGNAL_WEIGHTS["orphaned_references"]
    candidates: List[Candidate] = []

    if not gaps:
        return candidates

    # Build orphaned target → referrers from manifest orphaned_refs
    # gaps doesn't directly have this but orphaned_targets does
    # We need to cross-reference with manifest data (use pages relationship data)
    orphaned_targets = set(gaps.get("orphaned_targets", []))

    if not orphaned_targets:
        return candidates

    # Count how many pages reference each orphaned target
    orphan_referrers: Dict[str, List[str]] = {}
    for page in pages:
        for rel in page.get("relationships", []):
            target = rel.get("target", "")
            # Strip parenthetical context
            bare_target = re.sub(r"\s*\([^)]*\)\s*$", "", target).strip()
            if bare_target in orphaned_targets:
                orphan_referrers.setdefault(bare_target, []).append(page["title"])

    for target, referrers in orphan_referrers.items():
        # Deduplicate
        referrers = list(set(referrers))
        referrer_count = len(referrers)
        if referrer_count < 2:
            continue

        raw_score = min(referrer_count / 4, 1.0) * weight

        # Determine domain from referrers
        referrer_pages = [p for p in pages if p["title"] in referrers]
        domain = _most_common_domain(referrer_pages)

        signal = Signal(
            name="orphaned_references",
            score=raw_score,
            detail=f"'{target}' is referenced by {referrer_count} pages but doesn't exist: {', '.join(sorted(referrers)[:4])}",
        )
        candidates.append(Candidate(
            type="lesson",
            title=f"Lesson: {target}",
            score=raw_score,
            signals=[signal],
            source_pages=sorted(referrers),
            domain=domain,
        ))

    return candidates


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _most_common_domain(pages: List[Dict[str, Any]]) -> str:
    """Return the most common domain among a list of pages."""
    if not pages:
        return "cross-domain"
    domain_counts: Dict[str, int] = {}
    for p in pages:
        d = p.get("domain", "")
        if d:
            domain_counts[d] = domain_counts.get(d, 0) + 1
    if not domain_counts:
        return "cross-domain"
    return max(domain_counts, key=lambda k: domain_counts[k])


def _merge_candidates(candidates: List[Candidate]) -> List[Candidate]:
    """Merge candidates with the same title, combining signals and recalculating score."""
    merged: Dict[str, Candidate] = {}

    for c in candidates:
        key = c.title.lower().strip()
        if key not in merged:
            merged[key] = Candidate(
                type=c.type,
                title=c.title,
                score=0.0,
                signals=list(c.signals),
                source_pages=list(c.source_pages),
                domain=c.domain,
            )
        else:
            existing = merged[key]
            # Add new signals
            existing_signal_names = {s.name for s in existing.signals}
            for sig in c.signals:
                if sig.name not in existing_signal_names:
                    existing.signals.append(sig)
            # Merge source pages
            existing_sources = set(existing.source_pages)
            for sp in c.source_pages:
                if sp not in existing_sources:
                    existing.source_pages.append(sp)
                    existing_sources.add(sp)
            # Use most specific domain (non cross-domain wins)
            if existing.domain == "cross-domain" and c.domain != "cross-domain":
                existing.domain = c.domain

    # Recalculate score as sum of weighted signals, capped at 1.0
    for c in merged.values():
        total = sum(s.score for s in c.signals)
        c.score = min(total, 1.0)

    return list(merged.values())


def _deduplicate(candidates: List[Candidate], pages: List[Dict[str, Any]]) -> List[Candidate]:
    """Skip candidates whose source_pages are 80%+ covered by existing Layer 4-6 pages.

    If an existing evolved page already derives from most of the same source pages,
    the candidate is redundant.
    """
    # Build derived_from sets for Layer 4-6 pages
    evolved_derived: List[set] = []
    for page in pages:
        layer = page.get("layer", "")
        try:
            layer_int = int(str(layer)) if layer else 0
        except (ValueError, TypeError):
            layer_int = 0
        if layer_int >= 4:
            df = set(page.get("derived_from", []) or [])
            if df:
                evolved_derived.append(df)

    filtered: List[Candidate] = []
    for candidate in candidates:
        source_set = set(candidate.source_pages)
        if not source_set:
            filtered.append(candidate)
            continue

        redundant = False
        for df_set in evolved_derived:
            if not df_set:
                continue
            overlap = len(source_set & df_set) / len(source_set)
            if overlap >= 0.80:
                redundant = True
                break

        if not redundant:
            filtered.append(candidate)

    return filtered


# ---------------------------------------------------------------------------
# Score aggregation
# ---------------------------------------------------------------------------

def score_candidates(
    project_root: Path,
    type_filter: Optional[str] = None,
    domain_filter: Optional[str] = None,
    top: Optional[int] = None,
) -> List[Candidate]:
    """Run all scoring signals and return ranked evolution candidates.

    Args:
        project_root: Path to project root.
        type_filter: If set, only return candidates of this type (lesson/pattern/decision).
        domain_filter: If set, only return candidates for this domain.
        top: If set, return only this many top candidates.

    Returns:
        Sorted list of Candidate objects (highest score first).
    """
    wiki_dir = project_root / "wiki"

    # Build manifest
    manifest = build_manifest(wiki_dir)
    pages = manifest["pages"]

    # Run gaps analysis (import here to avoid circular imports)
    from tools.pipeline import run_gaps
    gaps = run_gaps(project_root, verbose=False)

    # Collect all signal results
    all_candidates: List[Candidate] = []
    all_candidates.extend(_signal_tag_cooccurrence(pages))
    all_candidates.extend(_signal_cross_source_convergence(pages))
    all_candidates.extend(_signal_relationship_hub(pages))
    all_candidates.extend(_signal_domain_layer_gap(pages))
    all_candidates.extend(_signal_open_question_density(pages, gaps))
    all_candidates.extend(_signal_orphaned_references(pages, gaps))

    # Merge candidates with same title
    merged = _merge_candidates(all_candidates)

    # Deduplicate against existing evolved pages
    deduplicated = _deduplicate(merged, pages)

    # Apply filters
    result = deduplicated
    if type_filter:
        result = [c for c in result if c.type == type_filter]
    if domain_filter:
        result = [c for c in result if c.domain == domain_filter]

    # Sort by score descending
    result.sort(key=lambda c: c.score, reverse=True)

    if top is not None:
        result = result[:top]

    return result


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

def _read_page_by_title(title: str, wiki_dir: Path) -> Optional[Dict[str, Any]]:
    """Search wiki dir for a page with the given title.

    Returns dict with keys: title, path, summary, key_insights, deep_analysis,
    relationships, or None if not found.
    """
    for md_file in find_wiki_pages(wiki_dir):
        text = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        if meta.get("title", "").lower() == title.lower():
            sections = parse_sections(body)
            deep = sections.get("Deep Analysis", "")
            # Truncate Deep Analysis to ~500 words
            if word_count(deep) > 500:
                words = deep.split()
                deep = " ".join(words[:500]) + "..."
            return {
                "title": meta.get("title", title),
                "path": str(md_file.relative_to(wiki_dir)),
                "summary": sections.get("Summary", ""),
                "key_insights": sections.get("Key Insights", ""),
                "deep_analysis": deep,
                "relationships": sections.get("Relationships", ""),
            }
    return None


def _quality_requirements(page_type: str) -> str:
    """Return quality requirements string for a given page type."""
    base = (
        "- Frontmatter must be complete and valid YAML\n"
        "- Summary must be 2-3 sentences minimum\n"
        "- At least 1 relationship required\n"
        "- No placeholder text ({{...}} must be filled in)\n"
        "- Source provenance documented\n"
    )
    if page_type == "lesson":
        return base + (
            "- Context section: when/where this lesson applies\n"
            "- Insight section: min 50 words, stated plainly\n"
            "- Evidence section: specific examples from source pages\n"
            "- Applicability section: which domains benefit\n"
        )
    elif page_type == "pattern":
        return base + (
            "- Pattern Description: min 100 words, how to recognize it\n"
            "- Instances: 2+ specific examples from wiki pages\n"
            "- When To Apply and When Not To sections required\n"
            "- instances field in frontmatter with 2+ entries\n"
        )
    elif page_type == "decision":
        return base + (
            "- Decision section: clear statement of what to do\n"
            "- Alternatives: min 2 alternatives with rejection rationale\n"
            "- Rationale: min 100 words backed by evidence\n"
            "- Reversibility: how hard to undo\n"
            "- Dependencies: what this decision affects\n"
        )
    return base


def build_prompt(candidate: Candidate, project_root: Path) -> str:
    """Build a complete generation prompt for a candidate.

    Reads source pages, loads template, and assembles an LLM-ready prompt.

    Args:
        candidate: The evolution candidate to generate a page for.
        project_root: Path to project root.

    Returns:
        Complete prompt string.
    """
    wiki_dir = project_root / "wiki"
    template_dir = project_root / "config" / "templates"

    # Read source pages
    source_materials: List[str] = []
    for page_title in candidate.source_pages[:6]:  # cap at 6 sources
        page_data = _read_page_by_title(page_title, wiki_dir)
        if not page_data:
            source_materials.append(f"### {page_title}\n\n(Page not found in wiki)\n")
            continue
        material = f"### {page_data['title']}\n\n"
        if page_data["summary"]:
            material += f"**Summary:** {page_data['summary']}\n\n"
        if page_data["key_insights"]:
            material += f"**Key Insights:**\n{page_data['key_insights']}\n\n"
        if page_data["deep_analysis"]:
            material += f"**Deep Analysis:**\n{page_data['deep_analysis']}\n\n"
        if page_data["relationships"]:
            material += f"**Relationships:**\n{page_data['relationships']}\n\n"
        source_materials.append(material)

    # Load template
    template_path = template_dir / f"{candidate.type}.md"
    if template_path.exists():
        template_content = template_path.read_text(encoding="utf-8")
    else:
        template_content = f"(No template found for type: {candidate.type})"

    # Layer mapping
    layer_map = {"lesson": 4, "pattern": 5, "decision": 6}
    target_layer = layer_map.get(candidate.type, 4)

    # Build signals section
    signals_text = "\n".join(
        f"  - {s.name} (score={s.score:.3f}): {s.detail}"
        for s in candidate.signals
    )

    # Build source pages list
    source_page_list = "\n".join(f"  - {sp}" for sp in candidate.source_pages)

    # Quality requirements
    quality_req = _quality_requirements(candidate.type)

    # Derived-from frontmatter
    derived_from_yaml = "\n".join(
        f'  - "{sp}"' for sp in candidate.source_pages[:4]
    )

    prompt = f"""# Evolution Generation Task

## Target Page

- **Type:** {candidate.type}
- **Suggested Title:** {candidate.title}
- **Domain:** {candidate.domain}
- **Target Layer:** {target_layer}
- **Aggregate Score:** {candidate.score:.3f}

## Why This Page (Signals)

The following signals triggered this evolution candidate:

{signals_text}

## Source Pages

The following wiki pages are the evidence base for this new page:

{source_page_list}

---

## Source Material

{chr(10).join(source_materials)}

---

## Quality Requirements

{quality_req}

## Frontmatter Requirements

The generated page MUST have these frontmatter values:

```yaml
type: {candidate.type}
domain: {candidate.domain}
layer: {target_layer}
status: synthesized
confidence: medium
maturity: seed
derived_from:
{derived_from_yaml}
```

## Template Structure

Use this template as your skeleton:

{template_content}

---

## Instructions

1. Read all source material above carefully.
2. Synthesize the key insight, pattern, or decision that emerges from these pages.
3. Fill in the template structure completely — no placeholder text.
4. Title must accurately reflect the synthesized content (you may refine the suggested title).
5. Write the ## Relationships section with DERIVED FROM entries for each source page.
6. Add additional relationships (BUILDS ON, ENABLES, RELATES TO) as appropriate.
7. Ensure the page meets all quality requirements above.
8. Output ONLY the complete wiki page (frontmatter + body), nothing else.
"""
    return prompt


# ---------------------------------------------------------------------------
# LLM Backends
# ---------------------------------------------------------------------------

class LLMBackend:
    """Base class for LLM generation backends."""

    def generate(self, prompt: str, model: Optional[str] = None) -> str:
        """Generate content from prompt. Returns generated text or queue path."""
        raise NotImplementedError

    def is_available(self) -> bool:
        """Check if this backend is available."""
        return False


class ClaudeCodeBackend(LLMBackend):
    """Queue-based backend — writes .prompt.md files to wiki/.evolve-queue/.

    Claude Code will pick up and process these files in a follow-up session.
    The generate() method returns the path to the queued prompt file.
    """

    def __init__(self, queue_dir: Path):
        self.queue_dir = queue_dir
        self.queue_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, prompt: str, model: Optional[str] = None) -> str:
        """Write prompt to queue file. Returns queue file path."""
        # Extract target title from prompt
        title_match = re.search(r"\*\*Suggested Title:\*\*\s*(.+)", prompt)
        title = title_match.group(1).strip() if title_match else "unknown"
        slug = re.sub(r"[^a-z0-9-]", "-", title.lower())[:60].strip("-")

        score_match = re.search(r"\*\*Aggregate Score:\*\*\s*([\d.]+)", prompt)
        score = float(score_match.group(1)) if score_match else 0.0

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        filename = f"{timestamp}-{slug}.prompt.md"
        queue_path = self.queue_dir / filename

        frontmatter = f"""---
target: "{title}"
candidate_score: {score:.3f}
generated: "{datetime.now(timezone.utc).isoformat()}"
status: pending
---

"""
        queue_path.write_text(frontmatter + prompt, encoding="utf-8")
        return str(queue_path)

    def is_available(self) -> bool:
        return True


class OpenAIBackend(LLMBackend):
    """Calls a local or remote OpenAI-compatible API endpoint.

    Uses WIKI_LLM_ENDPOINT env var (default: http://localhost:8080/v1).
    Uses WIKI_LLM_MODEL env var for model selection.
    Timeout: 120s.
    """

    def __init__(self, endpoint: Optional[str] = None, model: Optional[str] = None):
        self.endpoint = endpoint or os.environ.get(
            "WIKI_LLM_ENDPOINT", "http://localhost:8080/v1"
        ).rstrip("/")
        self.model = model or os.environ.get("WIKI_LLM_MODEL", "gpt-4")

    def generate(self, prompt: str, model: Optional[str] = None) -> str:
        """Call chat completions endpoint. Returns generated text."""
        use_model = model or self.model
        url = f"{self.endpoint}/chat/completions"
        payload = json.dumps({
            "model": use_model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except urllib.error.URLError as e:
            return f"ERROR: {e}"
        except (KeyError, json.JSONDecodeError) as e:
            return f"ERROR: Unexpected response format: {e}"

    def is_available(self) -> bool:
        """Check /models endpoint for availability."""
        try:
            url = f"{self.endpoint}/models"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status == 200
        except Exception:
            return False


class AICPBackend(LLMBackend):
    """Calls AICP's LLM endpoint, falls back to OpenAIBackend on failure.

    Uses WIKI_AICP_ENDPOINT env var.
    """

    def __init__(self, endpoint: Optional[str] = None):
        self.endpoint = endpoint or os.environ.get(
            "WIKI_AICP_ENDPOINT", "http://localhost:8090"
        ).rstrip("/")
        self._fallback = OpenAIBackend()

    def generate(self, prompt: str, model: Optional[str] = None) -> str:
        """Call AICP endpoint, fall back to OpenAI backend on failure."""
        url = f"{self.endpoint}/v1/chat/completions"
        payload = json.dumps({
            "messages": [{"role": "user", "content": prompt}],
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except Exception:
            # Fall back to OpenAI backend
            return self._fallback.generate(prompt, model=model)

    def is_available(self) -> bool:
        """Check /health endpoint."""
        try:
            url = f"{self.endpoint}/health"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status == 200
        except Exception:
            return False


def get_backend(name: str, project_root: Path) -> LLMBackend:
    """Factory function to get an LLM backend by name.

    Args:
        name: "claude-code", "openai", "aicp"
        project_root: Project root path (used for queue dir).

    Returns:
        LLMBackend instance.
    """
    name = name.lower().strip()
    if name in ("claude-code", "claude", "queue"):
        queue_dir = project_root / "wiki" / ".evolve-queue"
        return ClaudeCodeBackend(queue_dir=queue_dir)
    elif name in ("openai", "local", "llm"):
        return OpenAIBackend()
    elif name in ("aicp",):
        return AICPBackend()
    else:
        # Default to claude-code queue
        queue_dir = project_root / "wiki" / ".evolve-queue"
        return ClaudeCodeBackend(queue_dir=queue_dir)


# ---------------------------------------------------------------------------
# Orchestrator helpers
# ---------------------------------------------------------------------------

def _print_candidates(candidates: List[Candidate], verbose: bool = True) -> None:
    """Print a formatted table of evolution candidates."""
    if not candidates:
        print("  No evolution candidates found.")
        return

    print(f"\n  {'#':<4} {'Score':<7} {'Type':<10} {'Domain':<25} {'Title'}")
    print(f"  {'-'*4} {'-'*7} {'-'*10} {'-'*25} {'-'*45}")
    for i, c in enumerate(candidates, 1):
        domain_short = (c.domain or "cross-domain")[:24]
        title_short = c.title[:55]
        print(f"  {i:<4} {c.score:<7.3f} {c.type:<10} {domain_short:<25} {title_short}")
        if verbose:
            for sig in c.signals:
                print(f"       {'':7} {'':10} {'':25}   ({sig.name}: {sig.score:.3f})")

    print(f"\n  Total: {len(candidates)} candidate(s)")


def _execute_queue(project_root: Path, clear: bool = False, verbose: bool = True) -> Dict[str, Any]:
    """List (and optionally clear) the evolution queue."""
    queue_dir = project_root / "wiki" / ".evolve-queue"

    if not queue_dir.exists():
        if verbose:
            print("  Queue directory does not exist (no items queued).")
        return {"queue_dir": str(queue_dir), "items": [], "cleared": False}

    queue_files = sorted(queue_dir.glob("*.prompt.md"))

    if verbose:
        print(f"\n  Evolution queue: {queue_dir.relative_to(project_root)}")
        print(f"  {len(queue_files)} item(s):")
        for qf in queue_files:
            # Read frontmatter for summary
            text = qf.read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(text)
            target = meta.get("target", qf.stem)
            score = meta.get("candidate_score", "?")
            status = meta.get("status", "pending")
            print(f"    [{status}] {target} (score={score}) — {qf.name}")

    items = [{"file": qf.name, "path": str(qf)} for qf in queue_files]

    if clear and queue_files:
        for qf in queue_files:
            qf.unlink()
        if verbose:
            print(f"\n  Cleared {len(queue_files)} item(s) from queue.")
        return {"queue_dir": str(queue_dir), "items": items, "cleared": True, "cleared_count": len(queue_files)}

    return {"queue_dir": str(queue_dir), "items": items, "cleared": False}


def review_seeds(project_root: Path, verbose: bool = True) -> Dict[str, Any]:
    """Find seed-maturity pages ready for promotion.

    A seed page is ready for promotion if:
    - maturity == "seed"
    - has derived_from entries
    - has at least one non-DERIVED-FROM relationship (indicates content beyond scaffolding)
    """
    wiki_dir = project_root / "wiki"
    manifest = build_manifest(wiki_dir)
    pages = manifest["pages"]

    ready = []
    for page in pages:
        if page.get("maturity") != "seed":
            continue
        derived = page.get("derived_from", []) or []
        if not derived:
            continue
        # Check for non-DERIVED-FROM relationships
        rels = page.get("relationships", [])
        non_derived = [r for r in rels if r.get("verb", "") != "DERIVED FROM"]
        if not non_derived:
            continue
        ready.append({
            "title": page["title"],
            "type": page.get("type", ""),
            "layer": page.get("layer", ""),
            "domain": page.get("domain", ""),
            "derived_from": derived,
            "path": page.get("path", ""),
        })

    if verbose:
        print(f"\n  Seed pages ready for promotion: {len(ready)}")
        for p in ready:
            print(f"    [{p['type']}] {p['title']} ({p['domain']})")
            print(f"      derived_from: {', '.join(p['derived_from'][:3])}")

    return {"ready_for_promotion": ready, "count": len(ready)}


def detect_stale(project_root: Path, verbose: bool = True) -> Dict[str, Any]:
    """Find evolved pages whose derived_from sources have been updated more recently.

    If a source page has a newer 'updated' date than the evolved page, the evolved
    page may be stale.
    """
    wiki_dir = project_root / "wiki"
    manifest = build_manifest(wiki_dir)
    pages = manifest["pages"]

    # Build title → updated map
    title_to_updated: Dict[str, str] = {
        p["title"]: p.get("updated", "") for p in pages
    }

    stale: List[Dict[str, Any]] = []

    for page in pages:
        layer = page.get("layer", "")
        try:
            layer_int = int(str(layer)) if layer else 0
        except (ValueError, TypeError):
            layer_int = 0

        if layer_int < 4:
            continue

        page_updated = page.get("updated", "")
        if not page_updated:
            continue

        derived = page.get("derived_from", []) or []
        newer_sources = []
        for source_title in derived:
            source_updated = title_to_updated.get(source_title, "")
            if source_updated and source_updated > page_updated:
                newer_sources.append({
                    "title": source_title,
                    "updated": source_updated,
                })

        if newer_sources:
            stale.append({
                "title": page["title"],
                "type": page.get("type", ""),
                "layer": layer,
                "updated": page_updated,
                "newer_sources": newer_sources,
                "path": page.get("path", ""),
            })

    if verbose:
        print(f"\n  Stale evolved pages: {len(stale)}")
        for p in stale:
            print(f"    [{p['type']}] {p['title']} (updated {p['updated']})")
            for ns in p["newer_sources"]:
                print(f"      source '{ns['title']}' updated {ns['updated']}")

    return {"stale_pages": stale, "count": len(stale)}


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def evolve(
    project_root: Path,
    mode: str = "score",
    backend_name: str = "claude-code",
    top: Optional[int] = 10,
    type_filter: Optional[str] = None,
    domain_filter: Optional[str] = None,
    clear_queue: bool = False,
    verbose: bool = True,
) -> Dict[str, Any]:
    """Main evolution orchestrator.

    Modes:
        score     — Score candidates and print ranked table.
        scaffold  — Score + scaffold top candidates via pipeline.scaffold_page.
        dry-run   — Score + print generated prompts (no files written).
        auto      — Score + scaffold + generate via LLM backend.
        execute   — List or clear the generation queue.
        review    — Find seed pages ready for promotion.
        stale     — Find evolved pages with stale sources.

    Args:
        project_root: Path to project root.
        mode: Orchestration mode (see above).
        backend_name: LLM backend to use for auto mode.
        top: Number of top candidates to process.
        type_filter: Only process candidates of this type.
        domain_filter: Only process candidates for this domain.
        clear_queue: In execute mode, also clear the queue.
        verbose: Print progress output.

    Returns:
        Dict with results.
    """
    result: Dict[str, Any] = {"mode": mode, "ok": True}

    # ------------------------------------------------------------------
    # execute mode — just manage the queue
    # ------------------------------------------------------------------
    if mode == "execute":
        queue_result = _execute_queue(project_root, clear=clear_queue, verbose=verbose)
        result["queue"] = queue_result
        return result

    # ------------------------------------------------------------------
    # review mode — find seeds ready for promotion
    # ------------------------------------------------------------------
    if mode == "review":
        review_result = review_seeds(project_root, verbose=verbose)
        result["review"] = review_result
        return result

    # ------------------------------------------------------------------
    # stale mode — find stale evolved pages
    # ------------------------------------------------------------------
    if mode == "stale":
        stale_result = detect_stale(project_root, verbose=verbose)
        result["stale"] = stale_result
        return result

    # ------------------------------------------------------------------
    # Score candidates (all other modes need this)
    # ------------------------------------------------------------------
    if verbose:
        print("  Scoring evolution candidates...")

    candidates = score_candidates(
        project_root,
        type_filter=type_filter,
        domain_filter=domain_filter,
        top=top,
    )
    result["candidates"] = [c.to_dict() for c in candidates]
    result["candidate_count"] = len(candidates)

    if mode == "score":
        _print_candidates(candidates, verbose=verbose)
        return result

    # ------------------------------------------------------------------
    # dry-run mode — print prompts
    # ------------------------------------------------------------------
    if mode == "dry-run":
        _print_candidates(candidates, verbose=verbose)
        print("\n" + "=" * 60)
        for c in candidates:
            print(f"\n--- PROMPT: {c.title} ---\n")
            prompt = build_prompt(c, project_root)
            print(prompt[:2000])  # Truncate for readability
            print("...")
        return result

    # ------------------------------------------------------------------
    # scaffold mode — create stub pages
    # ------------------------------------------------------------------
    if mode in ("scaffold", "auto"):
        from tools.pipeline import scaffold_page

        scaffolded = []
        for c in candidates:
            if verbose:
                print(f"  Scaffolding [{c.type}]: {c.title}")
            scaffold_result = scaffold_page(
                page_type=c.type,
                title=c.title,
                project_root=project_root,
                domain=c.domain,
                derived_from=c.source_pages[:4],
                verbose=verbose,
            )
            scaffolded.append({
                "title": c.title,
                "type": c.type,
                "scaffold": scaffold_result,
            })
        result["scaffolded"] = scaffolded

        if mode == "scaffold":
            return result

    # ------------------------------------------------------------------
    # auto mode — scaffold + generate via backend
    # ------------------------------------------------------------------
    if mode == "auto":
        backend = get_backend(backend_name, project_root)
        if verbose:
            available = backend.is_available()
            print(f"  Backend: {backend_name} (available={available})")

        generated = []
        for c in candidates:
            if verbose:
                print(f"  Generating [{c.type}]: {c.title}")
            prompt = build_prompt(c, project_root)
            output = backend.generate(prompt)
            generated.append({
                "title": c.title,
                "type": c.type,
                "output": output[:200] + "..." if len(output) > 200 else output,
            })

        result["generated"] = generated
        return result

    # Unknown mode
    result["ok"] = False
    result["error"] = f"Unknown mode: {mode}. Use: score, scaffold, dry-run, auto, execute, review, stale"
    return result


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point for the evolution engine."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Evolution engine — score and scaffold higher-layer wiki pages."
    )
    parser.add_argument(
        "mode",
        nargs="?",
        default="score",
        choices=["score", "scaffold", "dry-run", "auto", "execute", "review", "stale"],
        help="Operation mode (default: score)",
    )
    parser.add_argument(
        "--top", "-n",
        type=int,
        default=10,
        help="Number of top candidates to show/process (default: 10)",
    )
    parser.add_argument(
        "--type", "-t",
        dest="type_filter",
        choices=["lesson", "pattern", "decision"],
        default=None,
        help="Filter by candidate type",
    )
    parser.add_argument(
        "--domain", "-d",
        dest="domain_filter",
        default=None,
        help="Filter by domain",
    )
    parser.add_argument(
        "--backend", "-b",
        default="claude-code",
        help="LLM backend for auto mode: claude-code, openai, aicp (default: claude-code)",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        default=False,
        help="In execute mode, clear the queue after listing",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        default=False,
        help="Suppress verbose output",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Output result as JSON",
    )

    args = parser.parse_args()
    project_root = get_project_root()

    result = evolve(
        project_root=project_root,
        mode=args.mode,
        backend_name=args.backend,
        top=args.top,
        type_filter=args.type_filter,
        domain_filter=args.domain_filter,
        clear_queue=args.clear,
        verbose=not args.quiet,
    )

    if args.json:
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
