"""Tests for tools/export.py — sister project export."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.export import transform_page, export_wiki
from tools.common import parse_frontmatter, load_config

FIXTURES = Path(__file__).resolve().parent / "fixtures"
EXPORT_PROFILES = Path(__file__).resolve().parent.parent / "config" / "export-profiles.yaml"


class TestTransformPage:
    def test_openfleet_strips_yaml_frontmatter(self):
        text = (FIXTURES / "valid-concept.md").read_text()
        profiles = load_config(EXPORT_PROFILES) or {}
        profile = profiles.get("openfleet", {})
        result = transform_page(text, profile)
        assert not result.startswith("---")
        assert "**Type:** Research" in result

    def test_openfleet_preserves_relationships(self):
        text = (FIXTURES / "valid-concept.md").read_text()
        profiles = load_config(EXPORT_PROFILES) or {}
        profile = profiles.get("openfleet", {})
        result = transform_page(text, profile)
        assert "## Relationships" in result
        assert "BUILDS ON" in result

    def test_openfleet_adds_source_project_header(self):
        text = (FIXTURES / "valid-concept.md").read_text()
        profiles = load_config(EXPORT_PROFILES) or {}
        profile = profiles.get("openfleet", {})
        result = transform_page(text, profile)
        assert "**Source Project:** devops-solutions-research-wiki" in result

    def test_aicp_converts_to_markdown_headers(self):
        text = (FIXTURES / "valid-concept.md").read_text()
        profiles = load_config(EXPORT_PROFILES) or {}
        profile = profiles.get("aicp", {})
        result = transform_page(text, profile)
        assert not result.startswith("---")
        assert "**Type:** Research Finding" in result
        assert "**Status:** RESEARCHED" in result

    def test_aicp_uses_condensed_resolution(self):
        text = (FIXTURES / "valid-concept.md").read_text()
        profiles = load_config(EXPORT_PROFILES) or {}
        profile = profiles.get("aicp", {})
        result = transform_page(text, profile)
        assert "## Summary" in result
        assert "## Key Insights" in result
        assert "## Deep Analysis" not in result
