---
title: "NotebookLM Skills"
type: concept
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
  - id: src-pleaseprompto-notebooklm-skill
    type: documentation
    url: "https://github.com/PleasePrompto/notebooklm-skill"
    file: raw/articles/pleasepromptonotebooklm-skill.md
    title: "PleasePrompto/notebooklm-skill"
    ingested: 2026-04-08
tags: [notebooklm, claude-code, skills, mcp, browser-automation, content-pipeline, source-grounded]
---

# NotebookLM Skills

## Summary

Two independent open-source projects bridge Google's NotebookLM with Claude Code through the skills system: claude-world/notebooklm-skill and PleasePrompto/notebooklm-skill. Despite sharing a name and target platform, they serve fundamentally different purposes and take different architectural approaches. The claude-world implementation is a full content production pipeline covering source discovery through research, AI content generation, and multi-platform publishing with dual CLI/MCP interfaces. The PleasePrompto implementation is a focused query tool that lets Claude Code ask NotebookLM source-grounded questions to reduce hallucinations during coding and research tasks. Both use browser automation for NotebookLM access (notebooklm-py and Patchright respectively) and both authenticate via browser-based Google login, but they diverge sharply in scope, architecture, and intended use case.

## Key Insights

- **Pipeline vs. query paradigm**: The claude-world skill orchestrates a four-phase content pipeline (collect sources, research via NotebookLM, generate content via Claude, publish to platforms). The PleasePrompto skill provides single-question Q&A against NotebookLM notebooks to get source-grounded answers for coding tasks. These are complementary rather than competing tools.

- **Dual interface vs. skill-only**: claude-world offers both a CLI (11 commands) and an MCP server (13 tools), working with Claude Code, Cursor, Gemini CLI, and any MCP client. PleasePrompto is a Claude Code skill only, with a companion MCP server as a separate repository (notebooklm-mcp in TypeScript).

- **Stateful vs. stateless sessions**: claude-world maintains notebook context across operations within a pipeline run. PleasePrompto uses a stateless model where each question opens a fresh browser, asks, retrieves, and closes. The stateless approach trades conversational context for reliability and simplicity.

- **Artifact generation vs. answer retrieval**: claude-world leverages NotebookLM's 9 artifact types (audio, video, slides, reports, quizzes, flashcards, mind maps, data tables, study guides). PleasePrompto retrieves text answers with citations and does not use artifact generation.

- **Anti-hallucination positioning**: PleasePrompto explicitly frames NotebookLM as superior to local RAG and direct document feeding for reducing hallucinations, providing a comparison table of approaches. claude-world does not emphasize hallucination reduction, focusing instead on content production throughput.

- **Library routing**: PleasePrompto includes a smart library management system where saved notebooks are tagged with metadata and Claude auto-selects the right notebook per question. claude-world manages notebooks programmatically as part of pipeline workflows.

- **Browser automation approaches**: Both rely on browser automation but use different libraries. claude-world uses notebooklm-py (pure async Python, no OAuth). PleasePrompto uses Patchright (Playwright-based) with human-like typing and interaction patterns for stealth.

- **Follow-up prompting pattern**: PleasePrompto compensates for its stateless model by appending "Is that ALL you need to know?" to each answer, prompting Claude to ask follow-up questions. This shifts multi-turn research from the browser session to Claude's conversation context.

## Deep Analysis

### Answered: Complementary Roles for Anti-Hallucination and Knowledge Compounding

PleasePrompto's anti-hallucination positioning creates an interesting bridge to the Agentic Search vs Vector Search debate. PleasePrompto treats NotebookLM as a grounded retrieval system (RAG-like) that is explicitly better than local RAG. Yet Karpathy critiques NotebookLM as a "retrieve-and-forget" system lacking compounding. The resolution: use NotebookLM for accuracy on specific questions, and the LLM Wiki for knowledge compounding over time. They serve complementary roles — NotebookLM provides ground-truth answers from specific sources; the wiki builds durable synthesized knowledge that accrues relationships and evolves over sessions. Neither replaces the other. The `src-notebooklm-claude-code-workflow` synthesis confirms this directly: "The wiki is the NotebookLM equivalent in the devops ecosystem — a grounded knowledge base that Claude Code queries to get project-specific answers." The difference is ownership and integration depth, not purpose.

### Answered: Structural Parallel Between Content Pipeline and Wiki Ingestion Pipeline

The claude-world pipeline skill's 4-phase architecture (collect sources, research via NotebookLM, generate content via Claude, publish to platforms) is structurally identical to the Wiki Ingestion Pipeline's stages (ingest, process, link, post-chain). Both are agent-orchestrated pipelines that transform raw sources into structured output. The difference is the output: wiki pages vs. content assets. This parallel is confirmed in `Skills Architecture Patterns`, which documents that the complexity spectrum for skills converges on "full pipeline skills" as the top tier — and notes that claude-world/notebooklm-skill is one such example. The `AI-Driven Content Pipeline` page explicitly maps the same three-layer architecture (intent → orchestration → generation) to both pipelines. A unified "ingest-then-publish" pattern is architecturally feasible: `notebooklm-py CLI` documents the integration point — "Sources ingested via tools/ingest.py can be simultaneously pushed to NotebookLM notebooks via notebooklm source add."

### Answered: Coexistence of Both Skills in the Same Environment

Cross-referencing `Skills Architecture Patterns`: the two NotebookLM skills use a **complementary composition** model, not a conflicting one. They target different use cases (pipeline production vs. ad-hoc queries) and do not overlap in their SKILL.md trigger descriptions. The `Skills Architecture Patterns` page documents this explicitly: "claude-world handles content production pipelines; PleasePrompto handles ad-hoc knowledge queries. Different use cases, same platform, no overlap." They can coexist because their trigger mechanisms are different — claude-world activates when the agent needs to build a content pipeline; PleasePrompto activates when the agent needs a source-grounded answer. The pablo-mano Obsidian CLI skill pattern (8+ agent platforms via system prompt paste) confirms that multiple SKILL.md files in the same environment work as long as their description fields are distinct enough for the model to select correctly.

### Answered: Feasibility of a Unified Skill

Cross-referencing `Skills Architecture Patterns` on composition: a unified skill combining PleasePrompto's query focus with claude-world's pipeline capabilities is technically feasible but architecturally undesirable. The `Skills Architecture Patterns` page identifies "context cost vs. capability breadth" as the central tension — "every loaded skill consumes context window tokens." A skill that bundled both 4-phase pipeline orchestration AND per-question query logic would be a full-pipeline skill (the most complex tier) that also needed to activate in lightweight query contexts. The correct solution is the existing complementary composition pattern: install both, let trigger descriptions route correctly. The `Context-Aware Tool Loading` pattern confirms: deferred loading (loading only the relevant skill for the current task) is the default-correct architecture. A merged skill would break context efficiency by loading pipeline machinery for simple queries.

### Answered: Practical Notebook Limit for PleasePrompto Library Routing

Cross-referencing `notebooklm-py CLI` and `Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py`: NotebookLM has a hard limit of 300 sources per notebook. At scale, the competitive analysis use case uses 2 notebooks for 35 competitors (~250 and ~136 sources respectively). For PleasePrompto's library routing, the practical limit is not determined by source count (PleasePrompto's notebooks are query-only, not source-heavy) but by the number of distinct notebooks in the library index. The `notebooklm-py CLI` page documents that the `notebooklm profile create/switch` commands support multi-profile isolation, which is the recommended architectural response to notebook sprawl. Reliability degrades when the metadata tags are ambiguous — when two notebooks have overlapping topic coverage and Claude must select between them. The `src-notebooklm-claude-code-workflow` synthesis recommends configuring NotebookLM's response format (persona: "learning guide", shorter responses) to reduce per-query token cost, which also helps library routing by keeping notebook descriptions compact and differentiable.

### Two Philosophies of NotebookLM Integration

The claude-world approach treats NotebookLM as a research engine within a larger production system. The mental model is: find topics, research them deeply, generate polished content, publish across platforms. This is a content creator's tool, optimized for throughput and breadth. The trending topic integration (via trend-pulse) and social publishing (via threads-viral-agent) extend the pipeline beyond NotebookLM itself into a full content automation system.

The PleasePrompto approach treats NotebookLM as a knowledge oracle for the coding agent. The mental model is: Claude needs accurate information from specific documents, so it asks NotebookLM instead of hallucinating or consuming tokens reading files directly. This is a developer's tool, optimized for answer accuracy and token efficiency. The comparison to local RAG is telling: the author positions NotebookLM as a zero-infrastructure alternative to vector databases and embedding pipelines.

The architectural differences follow from these different goals. A content pipeline needs to orchestrate multiple steps, manage artifacts, and push to external platforms, so claude-world builds a structured pipeline with CLI and MCP interfaces. A query tool needs to be simple and reliable for frequent ad-hoc questions, so PleasePrompto builds a stateless skill that opens, asks, and closes.

Both projects face the same fundamental risk: dependency on browser automation for accessing NotebookLM. Neither uses an official API (because none exists for NotebookLM), making both vulnerable to changes in NotebookLM's web interface. PleasePrompto explicitly acknowledges this risk with its stealth techniques and recommendation to use a dedicated Google account.

A practical user might reasonably install both: PleasePrompto for daily coding assistance with source-grounded answers, and claude-world for periodic content production runs where NotebookLM research feeds into published articles and social posts.

## Open Questions

- Will Google release an official NotebookLM API that would make browser automation unnecessary? (Requires: external announcement from Google; no existing wiki page covers this timeline)
- How do the browser automation approaches compare in reliability over weeks of use? (Requires: empirical longitudinal data from production deployments; no existing wiki page covers this)

## Relationships

- DERIVED FROM: src-claude-world-notebooklm-skill
- DERIVED FROM: src-pleaseprompto-notebooklm-skill
- EXTENDS: Claude Code Skills
- BUILDS ON: NotebookLM
- RELATES TO: Obsidian Skills Ecosystem
- RELATES TO: LLM Wiki Pattern
- ENABLES: AI-Driven Content Pipeline
- RELATES TO: Skills Architecture Patterns

## Backlinks

[[src-claude-world-notebooklm-skill]]
[[src-pleaseprompto-notebooklm-skill]]
[[Claude Code Skills]]
[[NotebookLM]]
[[Obsidian Skills Ecosystem]]
[[LLM Wiki Pattern]]
[[AI-Driven Content Pipeline]]
[[Skills Architecture Patterns]]
[[Agentic Search vs Vector Search]]
[[NotebookLM as Grounded Research Engine Not Just Note Storage]]
[[OpenClaw]]
[[Pattern: Skills + Notebooklm]]
[[Skill Specification Is the Key to Ecosystem Interoperability]]
[[Synthesis: PleasePrompto/notebooklm-skill]]
[[Synthesis: claude-world/notebooklm-skill]]
[[notebooklm-py CLI]]
