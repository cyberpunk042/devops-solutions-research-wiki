"""Tests for tools/validate.py — schema enforcement."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.validate import validate_page, validate_wiki

FIXTURES = Path(__file__).resolve().parent / "fixtures"
SCHEMA = Path(__file__).resolve().parent / "fixtures" / "test-schema.yaml"


class TestValidatePage:
    def test_valid_concept_passes(self):
        result = validate_page(FIXTURES / "valid-concept.md", SCHEMA)
        assert result["errors"] == []

    def test_valid_source_synthesis_passes(self):
        result = validate_page(FIXTURES / "valid-source-synthesis.md", SCHEMA)
        assert result["errors"] == []

    def test_missing_fields_detected(self):
        result = validate_page(FIXTURES / "invalid-missing-fields.md", SCHEMA)
        errors = [e["code"] for e in result["errors"]]
        assert "missing_field" in errors

    def test_bad_verb_warned(self):
        result = validate_page(FIXTURES / "invalid-bad-verb.md", SCHEMA)
        warnings = [w["code"] for w in result["warnings"]]
        assert "invalid_verb" in warnings

    def test_missing_sections_detected(self):
        result = validate_page(FIXTURES / "invalid-missing-fields.md", SCHEMA)
        errors = [e["code"] for e in result["errors"]]
        assert "missing_section" in errors


class TestValidateWiki:
    def test_validates_fixtures_dir(self):
        results = validate_wiki(FIXTURES, SCHEMA)
        assert len(results) > 0
        all_errors = [e for r in results for e in r["errors"]]
        assert len(all_errors) > 0
