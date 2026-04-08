"""Tests for tools/lint.py — wiki health checks."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.lint import lint_wiki, LintConfig

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class TestLintWiki:
    def test_detects_dead_relationships(self):
        config = LintConfig(stale_threshold_days=30, min_summary_words=30,
                            min_deep_analysis_words=100, min_relationships=1,
                            min_domain_pages=3, min_cross_domain_rels=2,
                            similarity_threshold=0.70)
        report = lint_wiki(FIXTURES, config)
        assert len(report["dead_relationships"]) > 0

    def test_returns_structured_report(self):
        config = LintConfig(stale_threshold_days=30, min_summary_words=30,
                            min_deep_analysis_words=100, min_relationships=1,
                            min_domain_pages=3, min_cross_domain_rels=2,
                            similarity_threshold=0.70)
        report = lint_wiki(FIXTURES, config)
        assert "orphan_pages" in report
        assert "dead_relationships" in report
        assert "stale_pages" in report
        assert "thin_pages" in report
        assert "domain_health" in report
        assert "summary" in report
