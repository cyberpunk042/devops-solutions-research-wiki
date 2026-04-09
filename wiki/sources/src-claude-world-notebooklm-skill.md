---
title: "Synthesis: claude-world/notebooklm-skill"
type: source-synthesis
domain: tools-and-platforms
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-claude-world-notebooklm-skill
    type: documentation
    url: "https://github.com/claude-world/notebooklm-skill"
    file: raw/articles/claude-worldnotebooklm-skill.md
    title: "claude-world/notebooklm-skill"
    ingested: 2026-04-08
tags: [notebooklm, claude-code, mcp, content-pipeline, automation, python]
---

# Synthesis: claude-world/notebooklm-skill

## Summary

This repository provides a full-pipeline tool that connects trending topic discovery, NotebookLM deep research, Claude-powered content generation, and multi-platform publishing. It operates as either a Claude Code Skill (via SKILL.md) or a standalone MCP Server, built on the notebooklm-py v0.3.4 async Python library. The tool manages a four-phase workflow: source collection (URLs, PDFs, RSS, trending topics), NotebookLM research (notebook creation, source ingestion, question-asking, artifact generation), Claude content generation (articles, social posts, newsletters), and multi-platform publishing (blogs, Threads/X, newsletters). It supports 9 downloadable artifact types from NotebookLM including audio podcasts, video, slides, reports, quizzes, flashcards, mind maps, data tables, and study guides.

## Key Insights

- **End-to-end pipeline**: Unlike simpler NotebookLM integrations, this tool covers the full content lifecycle from source discovery through research, generation, and publishing, orchestrating four distinct phases into a single automated workflow.

- **Dual interface model**: The tool exposes 11 CLI commands and 13 MCP tools, meaning it works both as a Claude Code skill for direct use and as an MCP server compatible with Cursor, Gemini CLI, and any MCP-compatible client.

- **9 artifact types**: NotebookLM artifact generation covers audio (M4A), video (MP4), slides (PDF/PPTX), reports (Markdown), quizzes (JSON/Markdown/HTML), flashcards (JSON/Markdown/HTML), mind maps (JSON), infographics (PNG, no download), data tables (CSV), and study guides (Markdown). Most support language selection.

- **Trending topic integration**: The tool integrates with trend-pulse for real-time trending topic discovery from 7 sources, enabling automated research on currently trending subjects without manual topic selection.

- **Browser-based auth, no OAuth**: Authentication uses browser-based Google login via notebooklm-py, requiring no API keys, no OAuth Client ID, and no Google Cloud project setup. Sessions persist for weeks.

- **Pipeline workflows**: Five pre-built pipelines (research-to-article, research-to-social, trend-to-content, batch-digest, generate-all) cover common content creation patterns, each composing multiple steps into a single command.

- **Social publishing integration**: Integrates with threads-viral-agent for auto-publishing research-backed social posts, closing the loop from research to public distribution.

## Deep Analysis

This tool represents the most ambitious NotebookLM integration available, treating NotebookLM not as a query endpoint but as a research engine within a larger content production system. The four-phase architecture (collect, research, generate, publish) mirrors professional content workflows, with each phase handling a distinct concern.

The dual CLI/MCP architecture is a pragmatic design choice. CLI commands give direct control for scripting and automation, while the MCP server enables integration with the growing ecosystem of MCP-compatible AI tools. This positions the tool at the intersection of two trends: NotebookLM as a research platform and MCP as a tool interoperability protocol.

The video generation workflow (combining NotebookLM slides and podcasts into YouTube-ready MP4) shows the tool pushing beyond basic text generation into multimedia content production. This is enabled by NotebookLM's own artifact generation capabilities rather than custom media processing.

## Open Questions

- What are the rate limits when generating multiple artifact types from a single notebook? (Requires: empirical measurement under sustained load; the notebooklm-py CLI page documents `--retry` with exponential backoff as the mitigation but specifies no concrete per-artifact or per-session rate limit thresholds)
- How does the trend-pulse integration select which trending topics are worth researching? (Requires: external documentation on trend-pulse's topic scoring and filtering logic; the AI-Driven Content Pipeline page notes it discovers from "7 sources" but the selection criteria are not covered in any existing wiki page)

### Answered Open Questions

**Q: How reliable is the notebooklm-py browser automation for long-running batch workflows?**

Cross-referencing `notebooklm-py CLI` and `AI-Driven Content Pipeline`: the `notebooklm-py CLI` page documents the reliability risks directly: "No official API: The entire package relies on browser automation and undocumented Google APIs. A NotebookLM web UI redesign could break everything. This is the single biggest risk for production pipelines." It further identifies three specific failure modes for long-running batch workflows: (1) Rate limiting — "Heavy automated usage triggers Google's rate limits. The `--retry` flag with exponential backoff helps, but sustained high-volume pipelines need throttling"; (2) Authentication friction — "CI/CD environments need the `NOTEBOOKLM_AUTH_JSON` environment variable workaround"; (3) Session state — "Browser automation sessions can expire, requiring re-authentication. Long-running daemons need session refresh logic." The `AI-Driven Content Pipeline` page documents that failure handling operates at the granularity of individual artifact types (each is a separate CLI invocation), meaning a single artifact failure does not halt a batch — but session expiry mid-batch would. The `NotebookLM Skills` page confirms this is a shared vulnerability between both NotebookLM skill implementations: "Both projects face the same fundamental risk: dependency on browser automation for accessing NotebookLM. Neither uses an official API, making both vulnerable to changes in NotebookLM's web interface." For claude-world specifically, the async Python API's concurrent operations (`NotebookLMClient`) add session management complexity absent from single-query tools. Reliability for batch workflows is adequate for scheduled daily runs (as demonstrated by the presenter) but requires explicit session refresh logic and rate-limit throttling for production pipelines.

## Relationships

- DERIVED FROM: src-claude-world-notebooklm-skill
- FEEDS INTO: NotebookLM Skills
- EXTENDS: Claude Code Skills
- RELATES TO: NotebookLM

## Backlinks

[[src-claude-world-notebooklm-skill]]
[[NotebookLM Skills]]
[[Claude Code Skills]]
[[NotebookLM]]
[[NotebookLM as Grounded Research Engine Not Just Note Storage]]
