---
title: "Synthesis: PleasePrompto/notebooklm-skill"
type: source-synthesis
domain: tools-and-platforms
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-09
sources:
  - id: src-pleaseprompto-notebooklm-skill
    type: documentation
    url: "https://github.com/PleasePrompto/notebooklm-skill"
    file: raw/articles/pleasepromptonotebooklm-skill.md
    title: "PleasePrompto/notebooklm-skill"
    ingested: 2026-04-08
tags: [notebooklm, claude-code, skill, source-grounded, browser-automation, python, patchright, anti-hallucination, library-management, stateless, rag-alternative, local-only, quick-start, mcp-alternative]
---

# Synthesis: PleasePrompto/notebooklm-skill

## Summary

This repository provides a Claude Code Skill that lets Claude directly query Google NotebookLM for source-grounded, citation-backed answers based exclusively on uploaded documents. The skill uses browser automation (Patchright, a Playwright-based stealth library) to open Chrome in a headless instance, submit questions, and return answers to Claude Code programmatically. It focuses on eliminating hallucinations by grounding all responses in user-uploaded documents rather than general training data. The skill operates in a stateless model where each question opens a fresh browser session, asks the question, retrieves the answer with a follow-up prompt ("Is that ALL you need to know?"), and closes. A library management system lets users save NotebookLM notebook links with tags and descriptions so Claude can auto-select the right notebook for each query. Works only with local Claude Code (not web UI). Companion to the TypeScript-based PleasePrompto/notebooklm-mcp which provides persistent sessions and multi-tool support.

## Key Insights

- **Anti-hallucination as primary value proposition**: The README explicitly compares this to feeding docs directly to Claude (high token cost, hallucinations), web search (unreliable sources), and local RAG (hours of setup, medium hallucinations), positioning NotebookLM as the superior option: minimal token cost, 5-minute setup, minimal hallucinations via source-grounded answers. The comparison table frames NotebookLM's "expert synthesis" by Gemini 2.5 as qualitatively different from embedding-based retrieval.

- **What makes NotebookLM superior to local RAG**: Pre-processed by Gemini (upload once, get instant knowledge), natural language Q&A (understanding and synthesis, not just retrieval), multi-source correlation (connects information across 50+ documents), citation-backed answers, and no infrastructure (no vector DBs, embeddings, or chunking strategies required).

- **Stateless session model**: Each question opens a fresh Chrome browser, asks the question, gets the answer, and closes immediately. This contrasts with the companion MCP server version which maintains persistent chat sessions. The tradeoff is simplicity and reliability versus conversational context within NotebookLM. Session data is stored locally at `~/.claude/skills/notebooklm/data/browser_state/`.

- **Follow-up prompting pattern**: Each answer includes "Is that ALL you need to know?" to prompt Claude to ask comprehensive follow-up questions, compensating for the lack of persistent sessions by encouraging multi-query research within a single user interaction. This shifts multi-turn conversation burden from the browser session to Claude's own conversation context.

- **Smart library management**: Users can save NotebookLM notebooks with metadata (name, topics, tags). Claude auto-selects the appropriate notebook based on the user's question. This creates a persistent knowledge routing layer on top of ephemeral query sessions. Library is stored at `~/.claude/skills/notebooklm/data/library.json`. Two addition modes: Smart Add (Claude queries the notebook to auto-discover content) or Manual Add.

- **Installation in 3 steps**: (1) `mkdir -p ~/.claude/skills`, (2) `git clone https://github.com/PleasePrompto/notebooklm-skill notebooklm` into that directory, (3) open Claude Code and say "What are my skills?". On first use, the skill auto-creates an isolated Python `.venv`, installs all dependencies including Google Chrome (not Chromium), and sets up browser automation. Everything stays contained in the skill folder.

- **Why Chrome, not Chromium**: The skill uses real Chrome (not Chromium) for cross-platform reliability, consistent browser fingerprinting, and better anti-detection with Google services. This is the explicit design choice versus Chromium-based alternatives.

- **Local-only architectural constraint**: The skill works only with local Claude Code installations, not the web UI, because the web UI runs skills in a sandbox without network access required for browser automation. This is a fundamental constraint — not a bug.

- **Human-like automation**: Uses Patchright (a Playwright-based stealth library) with realistic typing speeds, natural delays, and mouse movements to avoid detection by Google services. The author explicitly acknowledges the gray area: "probably fine, but better safe than sorry" — recommends using a dedicated Google account for automation.

- **Directory structure**: `~/.claude/skills/notebooklm/SKILL.md` (instructions for Claude), `scripts/ask_question.py` (query NotebookLM), `scripts/notebook_manager.py` (library management), `scripts/auth_manager.py` (Google authentication), `.venv/` (auto-created isolated Python environment), `data/` (local notebook library — contains `library.json`, `auth_info.json`, `browser_state/`; auto-excluded from git).

- **Common commands** (natural language interface):
  - "Set up NotebookLM authentication" → opens Chrome for Google login
  - "Add [link] to my NotebookLM library" → saves notebook with metadata
  - "Show my NotebookLM notebooks" → lists all saved notebooks
  - "Ask my API docs about [topic]" → queries the relevant notebook
  - "Use the React notebook" → sets active notebook
  - "Clear NotebookLM data" → fresh start (keeps library)

- **Real-world examples from README**: Workshop manual query (Suzuki GSR 600: DOT 4 brake fluid, SAE 10W-40 oil, 100 N·m rear axle torque — sourced from uploaded manual, no hallucination); n8n workflow building from uploaded n8n notebook (working workflow on first try, no hallucinated APIs).

- **Limitations documented explicitly**: Skill-specific: local Claude Code only (no web UI), no session persistence, no follow-up context ("can't reference the previous answer"). NotebookLM-specific: rate limits on free tier, manual document upload required, notebooks must be shared publicly to be accessible by the automation.

- **Companion MCP server**: PleasePrompto/notebooklm-mcp is a TypeScript-based MCP server version. Key differences: persistent chat sessions vs. fresh browser per question; works with Claude Code + Codex + Cursor vs. Claude Code only; npm package vs. git clone; TypeScript vs. Python. Both use Patchright for browser automation. The decision table: use skill for quick Claude Code integration; use MCP server for persistent sessions or multi-tool support.

- **Dependencies**: `patchright==1.55.2` (browser automation), `python-dotenv==1.0.0` (environment configuration). Auto-installed on first use.

- **Security posture**: Chrome runs locally, credentials never leave the machine. The `data/` directory is auto-excluded from git. Recommendation: use a dedicated Google account for automation rather than primary account.

## Deep Analysis

This skill takes a fundamentally different approach from claude-world/notebooklm-skill. While claude-world builds a content production pipeline (research to article to publishing), PleasePrompto focuses on a single, focused use case: letting Claude Code query NotebookLM as a knowledge source to produce better, grounded code and answers.

The stateless architecture is a deliberate design choice that trades capability for reliability. By not maintaining browser sessions, the skill avoids the complexity of session management, timeouts, and state corruption. Each query is independent and self-contained. The follow-up prompting pattern ("Is that ALL you need to know?") is a clever workaround that shifts the multi-turn conversation burden from the browser session to Claude's own conversation context.

The comparison table in the README (feeding docs to Claude vs web search vs local RAG vs NotebookLM) frames NotebookLM as a superior alternative to local RAG for document-grounded Q&A. This positioning is noteworthy: it suggests that for use cases where the document corpus fits within NotebookLM's limits, the effort of setting up local RAG infrastructure may be unnecessary.

The library management feature adds a layer of intelligence absent from simpler integrations. By maintaining metadata about which notebooks contain what topics, the skill creates a routing mechanism that automatically directs questions to the right knowledge source. This is analogous to a manual version of the routing step in agentic RAG architectures.

The problem framing in the README — "massive token consumption", "hallucinations", "manual copy-paste dance" — maps directly to three real pain points in AI-assisted development. The solution addresses all three: NotebookLM answers are token-efficient (one call returns a synthesized answer), source-grounded (no hallucination), and programmatic (no copy-paste).

## Open Questions

- How does Google's detection of automated browser usage affect long-term reliability? (Requires: empirical longitudinal data from production deployments; the notebooklm-py CLI page documents "No official API: entire package relies on browser automation" as the single biggest risk, and PleasePrompto uses stealth techniques, but no wiki page quantifies actual detection rates over time)
- What is the performance overhead of opening and closing a Chrome instance for every question? (Requires: empirical timing data from real usage; no existing wiki page covers per-query browser startup latency for Patchright-based automation)

### Answered Open Questions

**Q: How does the stateless model perform for complex multi-step research that benefits from conversational context?**

Cross-referencing `NotebookLM Skills` and `notebooklm-py CLI`: the `NotebookLM Skills` page documents the tradeoff explicitly in its Key Insights section: "Stateful vs. stateless sessions: claude-world maintains notebook context across operations within a pipeline run. PleasePrompto uses a stateless model where each question opens a fresh browser, asks, retrieves, and closes. The stateless approach trades conversational context for reliability and simplicity." The `NotebookLM Skills` page further documents the follow-up prompting pattern as the architectural workaround: "PleasePrompto compensates for its stateless model by appending 'Is that ALL you need to know?' to each answer, prompting Claude to ask follow-up questions. This shifts multi-turn research from the browser session to Claude's conversation context." For complex multi-step research, this means the stateless model is adequate as long as Claude's own conversation context accumulates the research findings across multiple independent queries — the browser session carries no state, but Claude's context window does. The `notebooklm-py CLI` page confirms that session state management is a real risk for long-running operations ("Browser automation sessions can expire, requiring re-authentication"), which reinforces the stateless design as a reliability choice at the cost of conversational continuity within NotebookLM itself.

**Q: What are the practical limits of the library routing mechanism when a user has dozens of notebooks?**

Cross-referencing `NotebookLM Skills`: the `NotebookLM Skills` page addresses this directly in its Answered section: "For PleasePrompto's library routing, the practical limit is not determined by source count... but by the number of distinct notebooks in the library index. Reliability degrades when the metadata tags are ambiguous — when two notebooks have overlapping topic coverage and Claude must select between them." The page further documents the mitigation: "The `notebooklm profile create/switch` commands support multi-profile isolation, which is the recommended architectural response to notebook sprawl." The `notebooklm-py CLI` page confirms that NotebookLM has a 300-source limit per notebook, and large-scale research requires multi-notebook architectures. The `NotebookLM Skills` page notes that "the `src-notebooklm-claude-code-workflow` synthesis recommends configuring NotebookLM's response format... to reduce per-query token cost, which also helps library routing by keeping notebook descriptions compact and differentiable." Practical guidance from wiki cross-references: the routing degrades at the point where notebook topic descriptions overlap significantly — the solution is to make descriptions as distinct as possible and use profile isolation to partition sprawl by domain.

## Relationships

- DERIVED FROM: src-pleaseprompto-notebooklm-skill
- FEEDS INTO: NotebookLM Skills
- EXTENDS: Claude Code Skills
- RELATES TO: NotebookLM
- COMPARES TO: src-claude-world-notebooklm-skill

## Backlinks

[[src-pleaseprompto-notebooklm-skill]]
[[NotebookLM Skills]]
[[Claude Code Skills]]
[[NotebookLM]]
[[src-claude-world-notebooklm-skill]]
