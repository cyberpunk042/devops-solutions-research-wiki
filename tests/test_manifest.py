"""Tests for tools/manifest.py — manifest.json builder."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.manifest import build_manifest

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class TestBuildManifest:
    def test_builds_from_fixtures(self):
        manifest = build_manifest(FIXTURES)
        assert "generated" in manifest
        assert "stats" in manifest
        assert "pages" in manifest
        assert "domains" in manifest
        assert "tags" in manifest
        assert manifest["stats"]["pages"] > 0

    def test_extracts_page_metadata(self):
        manifest = build_manifest(FIXTURES)
        pages_by_title = {p["title"]: p for p in manifest["pages"]}
        assert "Container Orchestration Patterns" in pages_by_title
        page = pages_by_title["Container Orchestration Patterns"]
        assert page["type"] == "concept"
        assert page["domain"] == "infrastructure"
        assert "kubernetes" in page["tags"]

    def test_extracts_relationships(self):
        manifest = build_manifest(FIXTURES)
        pages_by_title = {p["title"]: p for p in manifest["pages"]}
        page = pages_by_title["Container Orchestration Patterns"]
        verbs = [r["verb"] for r in page["relationships"]]
        assert "BUILDS ON" in verbs

    def test_builds_tag_index(self):
        manifest = build_manifest(FIXTURES)
        assert "kubernetes" in manifest["tags"]

    def test_builds_domain_index(self):
        manifest = build_manifest(FIXTURES)
        assert "infrastructure" in manifest["domains"]
        assert manifest["domains"]["infrastructure"]["page_count"] >= 1

    def test_finds_orphaned_refs(self):
        manifest = build_manifest(FIXTURES)
        orphan_targets = [o["target"] for o in manifest["orphaned_refs"]]
        assert "Docker Fundamentals" in orphan_targets
