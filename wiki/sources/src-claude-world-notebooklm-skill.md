---
title: "Synthesis: claude-world/notebooklm-skill"
type: source-synthesis
domain: tools-and-platforms
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-09
sources:
  - id: src-claude-world-notebooklm-skill
    type: documentation
    url: "https://github.com/claude-world/notebooklm-skill"
    file: raw/articles/claude-worldnotebooklm-skill.md
    title: "claude-world/notebooklm-skill"
    ingested: 2026-04-08
tags: [notebooklm, claude-code, mcp, content-pipeline, automation, python, trending-topics, artifact-generation, social-publishing, rss, batch, skill, mcp-server, trend-pulse, threads-viral-agent, uvx, pypi]
---

# Synthesis: claude-world/notebooklm-skill

## Summary

This repository provides a full-pipeline tool that connects trending topic discovery, NotebookLM deep research, Claude-powered content generation, and multi-platform publishing. It operates as either a Claude Code Skill (via SKILL.md) or a standalone MCP Server, built on the notebooklm-py v0.3.4 async Python library. The tool manages a four-phase workflow: source collection (URLs, PDFs, RSS, trending topics), NotebookLM research (notebook creation, source ingestion, question-asking, artifact generation), Claude content generation (articles, social posts, newsletters), and multi-platform publishing (blogs, Threads/X, newsletters). It supports 9 downloadable artifact types from NotebookLM including audio podcasts, video, slides, reports, quizzes, flashcards, mind maps, data tables, and study guides. Available via `uvx notebooklm-skill` (zero-install) or `pip install notebooklm-skill` from PyPI.

## Key Insights

- **End-to-end pipeline**: Unlike simpler NotebookLM integrations, this tool covers the full content lifecycle from source discovery through research, generation, and publishing, orchestrating four distinct phases into a single automated workflow. The README phrase is concise: "NotebookLM does the research, Claude writes the content."

- **Four-phase architecture with a branch**: Phase 1 (Collect: URLs, PDFs, RSS, trending topics) → Phase 2 (Research: notebook creation, source ingestion, question-asking, insight extraction) with a Phase 2b branch (Artifact generation: audio, video, slides, report, quiz, flashcards, mind map, infographic, data table, study guide) → Phase 3 (Generate: Claude content engine producing articles, social posts, newsletters) → Phase 4 (Publish: blog/CMS, Threads/X, newsletter, any platform).

- **Dual interface model**: The tool exposes 11 CLI commands and 13 MCP tools, meaning it works both as a Claude Code skill for direct use and as an MCP server compatible with Cursor, Gemini CLI, and any MCP-compatible client. The two interfaces map to the same underlying notebooklm-py library.

- **11 CLI commands**: `create` (notebook with URL/text sources), `list`, `delete`, `add-source` (URL, text, or file), `ask` (research question with citations), `summarize`, `generate` (artifact by type), `download`, `research` (deep web research), `podcast` (shortcut for `generate --type audio`), `qa` (shortcut for `generate --type quiz`).

- **13 MCP tools**: `nlm_create_notebook`, `nlm_list`, `nlm_delete`, `nlm_add_source`, `nlm_ask`, `nlm_summarize`, `nlm_generate`, `nlm_download`, `nlm_list_sources`, `nlm_list_artifacts`, `nlm_research`, `nlm_research_pipeline`, `nlm_trend_research`. The MCP server is started with `uvx --from notebooklm-skill notebooklm-mcp` or added to `.mcp.json`.

- **9 artifact types**: NotebookLM artifact generation covers Audio (M4A, AI-generated podcast), Video (MP4, video summary), Slides (PDF/PPTX), Report (Markdown), Quiz (JSON/Markdown/HTML), Flashcards (JSON/Markdown/HTML), Mind Map (JSON), Infographic (PNG — no download available), Data Table (CSV), Study Guide (Markdown). Most support language selection via `--lang` (e.g., `--lang zh-TW`); exceptions are quiz, flashcards, and mind map. Note: NotebookLM returns audio in MPEG-4 (M4A), not MP3.

- **5 pre-built pipeline workflows**: `research-to-article` (URLs → article draft: create notebook → 5 research questions → Claude article), `research-to-social` (URLs → social post: create notebook → summarize → platform-specific post), `trend-to-content` (geo+count → content per trend: fetch trends → create notebooks → research → draft), `batch-digest` (RSS URL → newsletter digest: fetch RSS → create notebook → digest + Q&A), `generate-all` (URLs → all artifact types: create notebook → generate all artifacts → download).

- **Slides + Podcast → YouTube video workflow**: A built-in multi-step workflow combines NotebookLM-generated slides (PDF) and podcast (M4A) into a YouTube-ready MP4 via a `make_video.sh` helper script. This demonstrates the tool pushing into multimedia content production without custom media processing infrastructure.

- **Trending topic integration**: Integrates with `trend-pulse` for real-time trending topic discovery from 7 sources, enabling automated research on currently trending subjects without manual topic selection. The `trend-to-content` pipeline and `nlm_trend_research` MCP tool operationalize this.

- **Browser-based auth, no OAuth**: Authentication uses browser-based Google login via notebooklm-py, requiring no API keys, no OAuth Client ID, and no Google Cloud project setup. One-time `uvx notebooklm login` opens Chromium; session is saved to `~/.notebooklm/storage_state.json` and typically lasts weeks. Subsequent calls use pure HTTP from the saved session.

- **Social publishing integration**: Integrates with `threads-viral-agent` for auto-publishing research-backed social posts, closing the loop from research to public distribution.

- **Installation paths**: Option A — `uvx notebooklm-skill` (zero install, recommended); Option B — `pip install notebooklm-skill`; Option C — install from source; Option D — one-line installer (`./install.sh`) that also installs Playwright and configures the Claude Code skill.

- **Claude Code Skill setup**: Two options — symlink via `./install.sh` (auto-updates with git pull) or manual copy of `SKILL.md`, scripts, and `requirements.txt` to `.claude/skills/notebooklm/`. Claude auto-detects the skill when prompts involve research, NotebookLM, or content creation.

- **MCP server setup**: Add `notebooklm-mcp` to `.mcp.json` using either `uvx --from notebooklm-skill notebooklm-mcp` (no install needed) or the `notebooklm-mcp` binary (if pip-installed). Works with Claude Code, Cursor, Gemini CLI, and any MCP-compatible client.

## Deep Analysis

This tool represents the most ambitious NotebookLM integration available, treating NotebookLM not as a query endpoint but as a research engine within a larger content production system. The four-phase architecture (collect, research, generate, publish) mirrors professional content workflows, with each phase handling a distinct concern.

The dual CLI/MCP architecture is a pragmatic design choice. CLI commands give direct control for scripting and automation, while the MCP server enables integration with the growing ecosystem of MCP-compatible AI tools. This positions the tool at the intersection of two trends: NotebookLM as a research platform and MCP as a tool interoperability protocol.

The video generation workflow (combining NotebookLM slides and podcasts into YouTube-ready MP4) shows the tool pushing beyond basic text generation into multimedia content production. This is enabled by NotebookLM's own artifact generation capabilities rather than custom media processing.

The two external integrations (trend-pulse and threads-viral-agent) represent deliberate ecosystem thinking: the tool is designed to be composed into larger automated pipelines rather than used in isolation. The `nlm_trend_research` MCP tool makes trend-to-content entirely autonomous — discover trending topics, research them in NotebookLM, generate content, and publish — without human intervention.

Compared to PleasePrompto/notebooklm-skill, this tool is oriented toward content production pipelines rather than document-grounded Q&A for code development. The stateful async Python API (`NotebookLMClient`) enables concurrent operations across phases, contrasting with PleasePrompto's deliberate stateless design.

The language-selection feature (`--lang zh-TW`) for most artifact types signals a multinational target audience — consistent with the repository providing a full Traditional Chinese README (`README.zh-TW.md`) and demo videos in both English and Traditional Chinese. This is practically relevant for non-English content workflows where artifact language and source language may differ.

The packaging choices (uvx zero-install as the recommended path, PyPI distribution, and a one-line `./install.sh` for skill+Playwright setup) reflect production maturity. The `uvx` path in particular means users can run `uvx notebooklm-skill --help` with no prior installation, significantly lowering the barrier to evaluating the tool.

## Open Questions

- What are the rate limits when generating multiple artifact types from a single notebook? (Requires: empirical measurement under sustained load; the notebooklm-py CLI page documents `--retry` with exponential backoff as the mitigation but specifies no concrete per-artifact or per-session rate limit thresholds)
- How does the trend-pulse integration select which trending topics are worth researching? (Requires: external documentation on trend-pulse's topic scoring and filtering logic; the tool notes discovery from "7 sources" but the selection and deduplication criteria are not documented in the raw file)

### Answered Open Questions

**Q: How reliable is the notebooklm-py browser automation for long-running batch workflows?**

Cross-referencing `notebooklm-py CLI` and `AI-Driven Content Pipeline`: the `notebooklm-py CLI` page documents the reliability risks directly: "No official API: The entire package relies on browser automation and undocumented Google APIs. A NotebookLM web UI redesign could break everything. This is the single biggest risk for production pipelines." It further identifies three specific failure modes for long-running batch workflows: (1) Rate limiting — "Heavy automated usage triggers Google's rate limits. The `--retry` flag with exponential backoff helps, but sustained high-volume pipelines need throttling"; (2) Authentication friction — "CI/CD environments need the `NOTEBOOKLM_AUTH_JSON` environment variable workaround"; (3) Session state — "Browser automation sessions can expire, requiring re-authentication. Long-running daemons need session refresh logic." The `AI-Driven Content Pipeline` page documents that failure handling operates at the granularity of individual artifact types (each is a separate CLI invocation), meaning a single artifact failure does not halt a batch — but session expiry mid-batch would. The `NotebookLM Skills` page confirms this is a shared vulnerability between both NotebookLM skill implementations: "Both projects face the same fundamental risk: dependency on browser automation for accessing NotebookLM. Neither uses an official API, making both vulnerable to changes in NotebookLM's web interface." For claude-world specifically, the async Python API's concurrent operations (`NotebookLMClient`) add session management complexity absent from single-query tools. Reliability for batch workflows is adequate for scheduled daily runs (as demonstrated by the presenter) but requires explicit session refresh logic and rate-limit throttling for production pipelines.

## Relationships

- DERIVED FROM: src-claude-world-notebooklm-skill
- FEEDS INTO: NotebookLM Skills
- EXTENDS: Claude Code Skills
- RELATES TO: NotebookLM
- COMPARES TO: src-pleaseprompto-notebooklm-skill

## Backlinks

[[src-claude-world-notebooklm-skill]]
[[NotebookLM Skills]]
[[Claude Code Skills]]
[[NotebookLM]]
[[src-pleaseprompto-notebooklm-skill]]
[[NotebookLM as Grounded Research Engine Not Just Note Storage]]
