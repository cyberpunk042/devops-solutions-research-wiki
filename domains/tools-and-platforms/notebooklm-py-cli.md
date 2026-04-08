---
title: "notebooklm-py CLI"
type: concept
domain: tools-and-platforms
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-notebooklm-py-official
    type: documentation
    url: "https://github.com/teng-lin/notebooklm-py"
    file: raw/articles/notebooklm-py-official-docs.md
    title: "notebooklm-py — Official Documentation"
    ingested: 2026-04-08
  - id: src-claude-world-notebooklm-skill
    type: documentation
    url: "https://github.com/claude-world/notebooklm-skill"
    file: raw/articles/claude-worldnotebooklm-skill.md
    title: "claude-world/notebooklm-skill"
    ingested: 2026-04-08
  - id: src-pleaseprompto-notebooklm-skill
    type: documentation
    url: "https://github.com/PleasePrompto/notebooklm-skill"
    file: raw/articles/pleasepromptonotebooklm-skill.md
    title: "PleasePrompto/notebooklm-skill"
    ingested: 2026-04-08
tags: [notebooklm, cli, python, api, automation, browser-automation, content-pipeline, agent-tools, google, research-tool]
---

# notebooklm-py CLI

## Summary

notebooklm-py is an unofficial Python package (9.5k GitHub stars, MIT licensed) that provides full programmatic access to Google NotebookLM via CLI, Python async API, and AI agent skill/MCP integration. It exposes capabilities beyond the web UI — batch artifact downloads, structured quiz/flashcard export (JSON/Markdown/HTML), mind map JSON extraction, data table CSV export, slide deck PPTX, individual slide revision, and programmatic sharing. The CLI covers notebook management, source ingestion (URLs, files, web research), chat with source-grounded Q&A, generation of 10 artifact types (audio, video, cinematic video, quizzes, flashcards, slides, infographics, mind maps, data tables, reports), and export/download of all artifacts. Authentication uses browser-based Google OAuth with local credential storage. The package integrates natively with Claude Code, Codex, and OpenClaw via `notebooklm skill install`.

## Key Insights

- **Full NotebookLM automation**: Every action available in the NotebookLM web UI — plus several that aren't — is accessible from the command line. Notebooks, sources, chat, artifact generation, downloads, sharing, and research are all scriptable.

- **10 artifact types, all downloadable**: Audio (MP3, 4 formats, 3 lengths, 50+ languages), video (MP4, 3 formats, 9 styles), cinematic video, quizzes, flashcards, slide decks (PDF/PPTX), infographics (PNG), mind maps (JSON), data tables (CSV), reports (PDF). Each has a `generate` and `download` command pair.

- **Async Python API**: The `NotebookLMClient` class uses async context managers with namespaced operations: `client.notebooks`, `client.sources`, `client.chat`, `client.artifacts`, `client.research`, `client.notes`, `client.sharing`. All methods are async, supporting concurrent operations.

- **Web research with auto-import**: `notebooklm source add-research "<query>"` triggers NotebookLM's web research agent to find and import relevant sources automatically — fast mode for quick results, deep mode for comprehensive research.

- **Source-grounded Q&A from terminal**: `notebooklm ask "<question>"` queries loaded sources with citations. Supports `--json` for structured output, `-s <id>` for source-specific queries, `--save-as-note` to persist answers as notebook notes.

- **Context-based workflow**: `notebooklm use <id>` sets the active notebook, and subsequent commands inherit it. Or use `-n/--notebook <id>` for explicit targeting — critical for parallel/automated workflows operating on multiple notebooks.

- **Multi-profile support**: `notebooklm profile create/switch` manages multiple Google accounts, enabling workflows that span personal and organizational NotebookLM instances.

- **Agent skill installation**: `notebooklm skill install` drops skill files into `~/.claude/skills/notebooklm` and `~/.agents/skills/notebooklm`. Also available via `npx skills add teng-lin/notebooklm-py`. The CLI includes `notebooklm agent show claude|codex` to print agent-specific instructions.

- **Browser automation underneath**: Uses Playwright/Patchright for browser automation since no official NotebookLM API exists. This means authentication requires a real browser session, and the package is vulnerable to NotebookLM web UI changes.

- **Structured exports fill a critical gap**: The web UI only shows artifacts inline. notebooklm-py enables downloading quizzes as JSON (parseable), flashcards as Markdown (ingestable), mind maps as JSON (graph data), and data tables as CSV (analyzable). These structured formats are what pipelines need.

## Deep Analysis

### Role in the Research Wiki Pipeline

notebooklm-py transforms NotebookLM from an interactive web tool into a programmable node in the research pipeline. The integration points for this project:

1. **Source mirroring**: Wiki sources ingested via `tools/ingest.py` can be simultaneously pushed to NotebookLM notebooks via `notebooklm source add`. This creates a parallel knowledge base where NotebookLM's Gemini-powered analysis complements the wiki's structured synthesis.

2. **Research amplification**: When gap analysis (`tools/lint.py`) identifies under-connected domains or missing concepts, `notebooklm source add-research "<topic>"` can automatically discover and import relevant sources. The deep research mode is particularly powerful for finding primary sources that simple web search misses.

3. **Cross-validation**: `notebooklm ask` can query sources with specific questions to validate wiki page claims. If the wiki says "X contradicts Y," NotebookLM can independently verify from the same sources. This is a second opinion from a different LLM (Gemini vs Claude).

4. **Content generation pipeline**: For the AICP and openfleet export targets, NotebookLM artifacts (slide decks, reports, audio overviews) could supplement wiki exports. A wiki page about "LLM Wiki Pattern" could also produce a NotebookLM audio overview for podcast distribution.

5. **Structured data extraction**: `notebooklm generate data-table` + `notebooklm download data-table ./file.csv` could extract structured comparisons from source material, feeding directly into wiki comparison pages.

### CLI Command Architecture

The CLI is organized hierarchically via Python Click:

| Group | Key Commands | Pipeline Value |
|-------|-------------|---------------|
| Notebooks | create, list, use, delete | Workspace management |
| Sources | add, add-research, list, fulltext | Ingestion pipeline |
| Chat | ask [--json] [--save-as-note] | Query + validation |
| Generate | audio, video, quiz, flashcards, slides, infographic, mind-map, data-table, report | Content production |
| Download | all artifact types in multiple formats | Export pipeline |
| Sharing | status, permissions | Collaboration |
| Agent | show, skill install/status | Integration setup |

### Python API for Pipeline Integration

The async API is the more powerful integration path for automated pipelines:

```python
async with await NotebookLMClient.from_storage() as client:
    # Create notebook per research topic
    nb = await client.notebooks.create("LLM Wiki Research")
    
    # Mirror wiki sources
    for url in wiki_source_urls:
        await client.sources.add_url(nb.id, url)
    
    # Generate artifacts
    await client.artifacts.generate_audio(nb.id)
    await client.artifacts.generate_mind_map(nb.id)
    
    # Download structured data
    await client.artifacts.download_mind_map(nb.id, "./mind-map.json")
    
    # Cross-validate
    result = await client.chat.ask(nb.id, 
        "What contradictions exist between these sources?")
```

### Risks and Constraints

- **No official API**: The entire package relies on browser automation and undocumented Google APIs. A NotebookLM web UI redesign could break everything. This is the single biggest risk for production pipelines.
- **Authentication friction**: Initial setup requires a real browser window for Google OAuth. CI/CD environments need the `NOTEBOOKLM_AUTH_JSON` environment variable workaround.
- **Rate limiting**: Heavy automated usage triggers Google's rate limits. The `--retry` flag with exponential backoff helps, but sustained high-volume pipelines need throttling.
- **Session state**: Browser automation sessions can expire, requiring re-authentication. Long-running daemons need session refresh logic.

## Open Questions

- What are the practical rate limits for automated NotebookLM usage before Google throttles or blocks the account?
- Can notebooklm-py's async API be wrapped as an MCP server for direct use in Claude Code conversations?
- How does the `add-research` deep mode compare to our `tools/ingest.py` + web search pipeline for source discovery?
- What is the quality/accuracy comparison between NotebookLM's source-grounded answers (Gemini) and the wiki's synthesized pages (Claude)?
- Can notebook metadata and source lists be synced bidirectionally with wiki/manifest.json?
- Will Google release an official NotebookLM API that makes browser automation unnecessary?

## Relationships

- BUILDS ON: NotebookLM
- EXTENDS: NotebookLM Skills
- ENABLES: AI-Driven Content Pipeline
- PARALLELS: Obsidian CLI
- RELATES TO: Claude Code Skills
- RELATES TO: Wiki Ingestion Pipeline
- RELATES TO: LLM Wiki Pattern
- ENABLES: Wiki Event-Driven Automation

## Backlinks

[[NotebookLM]]
[[NotebookLM Skills]]
[[AI-Driven Content Pipeline]]
[[Obsidian CLI]]
[[Claude Code Skills]]
[[Wiki Ingestion Pipeline]]
[[LLM Wiki Pattern]]
[[Wiki Event-Driven Automation]]
[[Claude Code]]
[[MCP Integration Architecture]]
[[Research Pipeline Orchestration]]
