---
title: "Wiki Ingestion Pipeline"
type: concept
domain: knowledge-systems
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-karpathy-claude-code-10x
    type: youtube-transcript
    file: raw/transcripts/karpathy-claude-code-10x.txt
    title: "Andrej Karpathy Just 10x'd Everyone's Claude Code"
    ingested: 2026-04-08
  - id: src-karpathy-llm-wiki-idea-file
    type: documentation
    url: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
    file: raw/articles/karpathy-llm-wiki-idea-file.md
    title: "Karpathy LLM Wiki Idea File"
    ingested: 2026-04-08
  - id: src-llm-wiki-v2-agentmemory
    type: documentation
    url: "https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2"
    file: raw/articles/llm-wiki-v2-extending-karpathys-llm-wiki-pattern-with-lessons-from-building-agen.md
    title: "LLM Wiki v2 -- Extending Karpathy's LLM Wiki Pattern with Lessons from Building Agentmemory"
    ingested: 2026-04-08
tags: [ingestion, pipeline, claude-code, wiki, markdown, data-processing, workflow, entity-extraction, event-driven]
---

# Wiki Ingestion Pipeline

## Summary

The wiki ingestion pipeline is the workflow by which raw source documents are transformed into structured, interlinked wiki pages by Claude Code. The process has distinct phases: data ingest (placing raw documents into the `raw/` folder), processing (Claude Code reads the source, asks clarifying questions, then generates multiple wiki pages with relationships), and linking (the index is updated, cross-references are created, and the operation is logged). The pipeline handles diverse source types including PDFs, web articles, and transcript batches, and adapts its output granularity based on source complexity — a single article may produce anywhere from 5 to 25 wiki pages.

## Key Insights

- **Three-phase workflow**: (1) Drop raw source into the `raw/` folder, (2) tell Claude Code to ingest it, (3) Claude Code reads, asks questions, generates wiki pages, updates the index, and logs the operation.
- **Clarifying questions phase**: After reading a source, Claude Code asks the user about emphasis, focus areas, desired granularity, and the project's overall purpose. This shapes how it structures the output.
- **Adaptive page generation**: The LLM decides how many pages to create based on content density. The AI 2027 article produced 23 wiki pages including 1 source page, 6 person pages, 5 organization pages, 1 AI systems page, multiple concept pages, and an analysis page.
- **Batch ingestion**: The presenter ingested 36 YouTube transcripts in a single batch, which took about 14 minutes. Individual article ingestion takes roughly 10 minutes depending on length and complexity.
- **Web clipper as intake mechanism**: The Obsidian Web Clipper extension allows one-click capture of web articles directly into the `raw/` folder, reducing friction in the intake step.
- **Automatic relationship discovery**: Claude Code does not just summarize — it identifies entities, concepts, and their relationships, then creates explicit interlinks between pages. The human does no manual relationship building.
- **Index and log maintenance**: Every ingestion operation updates the master index (adding new entries for tools, techniques, concepts, people, comparisons) and appends to the log (operation history for auditability).
- **Project context matters**: Telling Claude Code the purpose of the vault (research project vs. personal second brain vs. YouTube archive) changes how it structures and categorizes the output.
- **Interactive vs. batch modes (from primary source)**: Karpathy describes two ingestion styles: interactive ("I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize") and batch ("you could also batch-ingest many sources at once with less supervision"). The right workflow depends on user preference and is documented in the schema.
- **Entity extraction during ingestion (from v2)**: The LLM Wiki v2 document argues that ingestion should go beyond prose summaries to extract structured entities (people, projects, libraries, concepts) with typed attributes and relationships. This enables graph-based queries that catch connections prose summaries miss.
- **Event-driven auto-ingestion (from v2)**: Rather than requiring the user to manually trigger ingestion, a "new source" event hook should auto-ingest, extract entities, update the graph, and update the index. The human remains in the loop for curation but is freed from remembering to trigger processing.
- **Privacy filtering on ingest (from v2)**: Before anything reaches the wiki, sensitive data (API keys, tokens, passwords, PII) should be automatically stripped. This should be a standard ingestion step, not something the user remembers to do manually.

## Deep Analysis

The ingestion pipeline is the core engine of the LLM Wiki pattern. Its effectiveness comes from treating document processing not as a chunking problem (as in RAG) but as a comprehension and organization problem. Claude Code reads the full source, understands it holistically, and then makes editorial decisions about how to decompose it into wiki pages.

This is a fundamentally different approach from RAG chunking, where documents are mechanically split at fixed token boundaries or paragraph breaks. The LLM's chunking is semantic — it groups related information into coherent pages based on conceptual boundaries, creates pages for entities and concepts that deserve their own entries, and links everything together.

The clarifying questions phase is an underappreciated design element. By asking the user about their goals and focus, the pipeline customizes its output to the user's actual needs rather than producing generic summaries. This interactive step is what makes the same pipeline work for both a YouTube transcript archive and a personal second brain — the structure emerges from the conversation, not from a rigid template.

The batch ingestion capability demonstrates that the pipeline scales linearly with source count. 36 transcripts in 14 minutes suggests roughly 23 seconds per transcript for a batch operation, which is significantly faster than the 10-minute single-article ingestion — likely because batch mode reduces the per-source overhead of index updates and question-asking.

A key architectural decision is that the raw source is preserved in the `raw/` folder even after ingestion. This means you can re-ingest sources with different parameters, audit the wiki against its sources, or migrate to a different system later without losing original data.

## Open Questions

- How does ingestion quality vary across source types (structured PDF vs. rambling transcript vs. dense technical paper)? (Requires: empirical benchmarking across source types; the `Rework Prevention` page notes that smart mode escalates for "low-quality source" cases, but no quantitative quality data across source types is documented in existing wiki pages)

### Answered Open Questions

**Q: Can the pipeline be run in fully non-interactive mode for automated ingestion (skipping the clarifying questions)?**

Cross-referencing `Rework Prevention` and `Research Pipeline Orchestration`: yes — `auto` mode is the fully non-interactive ingestion mode. The `Rework Prevention` page documents all three ingestion modes: "auto mode: No gates. Appropriate only for high-confidence, low-complexity sources where rework risk is low and throughput is valued. The `post` chain's validation step (exit code 1 on errors) is the only hard gate in auto mode." The `Research Pipeline Orchestration` page confirms the vision: "Extract pages (Claude Code manual) → Needs skill-driven automation" and documents `pipeline run URL [URL...]` as the "Parallel fetch + post-chain in one command" — this is the closest current implementation of fully automated end-to-end ingestion. The three-mode system (auto/guided/smart) means non-interactive operation is already supported by design; the user selects `auto` or the pipeline defaults to `smart` which only asks questions when risk is high. For fully automated pipeline operation (e.g., scheduled overnight ingestion of a URL list), `auto` mode with `pipeline run --batch urls.txt` is the correct invocation.

**Q: How does the pipeline handle updates to a previously ingested source — does it diff and update, or re-create from scratch?**

Cross-referencing `Knowledge Evolution Pipeline` and `Rework Prevention`: the current model is re-create from scratch using the evolution pipeline's `derived_from` + `status: stale` mechanism, not diff-and-patch. The `Knowledge Evolution Pipeline` page documents the update mechanism: "The original page is preserved (or marked `status: stale`) and the promoted page carries a `derived_from` frontmatter field pointing back." The `Rework Prevention` page notes: "The raw source is preserved in the `raw/` folder even after ingestion. This means you can re-ingest sources with different parameters." The practical update workflow: re-ingest the updated source (or new version of a source) and the pipeline creates new pages; the curator then marks the old pages `status: stale` and adds `SUPERSEDES` relationships from new to old. A true diff-and-update mechanism (detecting changes between ingestion runs and patching only modified sections) is not implemented in existing wiki tooling — the `Knowledge Evolution Pipeline` page's `--review` flag is the closest human gate for deciding whether a re-ingested version should supersede an existing page.

**Q: Is there a way to prioritize which raw documents to ingest next based on the wiki's current gaps?**

Cross-referencing `Knowledge Evolution Pipeline` and `Research Pipeline Orchestration`: yes — `pipeline gaps` is the gap analysis tool that identifies what to ingest next. The `Knowledge Evolution Pipeline` page documents the outer loop: "3. Gaps: Run `pipeline gaps` to find orphans, thin pages, missing backlinks, and under-covered domains. 4. Research: Queue new sources to fill identified gaps." The `Research Pipeline Orchestration` page describes a `DEEPENING` pipeline type: "lint_report → identify_thin → research_gaps → enrich → validate → integrate" — this is the automated version of gap-driven ingestion prioritization. For raw files already in `raw/`, `tools/pipeline status` shows unprocessed raw files, and `pipeline gaps` identifies which domains are thin. Cross-referencing these two outputs gives a priority queue: ingest raw files that address the weakest domains first. The `pipeline chain continue` command (`status → review → score → gaps → crossref`) surfaces this priority information in one operation.

**Q: Could the pipeline be triggered automatically when a new file appears in the `raw/` folder?**

Cross-referencing `Knowledge Evolution Pipeline` and `WSL2 Development Patterns`: yes — this is explicitly described in the LLM Wiki v2 source as "event-driven auto-ingestion" and the infrastructure to implement it already exists. The `Wiki Ingestion Pipeline` Key Insights section (from v2) states: "Rather than requiring the user to manually trigger ingestion, a 'new source' event hook should auto-ingest, extract entities, update the graph, and update the index. The human remains in the loop for curation but is freed from remembering to trigger processing." The `WSL2 Development Patterns` page documents `tools/watcher.py` which already watches the `wiki/` folder for changes and triggers the post-chain. Extending `watcher.py` to also watch `raw/` for new files (which land on the Linux filesystem where inotify is reliable) and trigger `pipeline run` in `auto` or `smart` mode is a direct implementation of the v2 vision. The `Research Pipeline Orchestration` page calls this the `ONLINE RESEARCH` pipeline triggered by "new source" events. The technical components exist; the missing piece is extending the watcher's watched paths from `wiki/` to also include `raw/`.

## Relationships

- DERIVED FROM: src-karpathy-claude-code-10x
- DERIVED FROM: src-karpathy-llm-wiki-idea-file
- DERIVED FROM: src-llm-wiki-v2-agentmemory
- IMPLEMENTS: LLM Wiki Pattern
- USED BY: Obsidian Knowledge Vault
- FEEDS INTO: LLM Knowledge Linting
- FEEDS INTO: Wiki Knowledge Graph
- EXTENDS: Research Pipeline Orchestration
- RELATES TO: notebooklm-py CLI
- RELATES TO: Obsidian CLI
- RELATES TO: Wiki Event-Driven Automation
- PARALLELS: AI-Driven Content Pipeline
- CONSTRAINED BY: Claude Code Context Management

## Backlinks

[[src-karpathy-claude-code-10x]]
[[src-karpathy-llm-wiki-idea-file]]
[[src-llm-wiki-v2-agentmemory]]
[[LLM Wiki Pattern]]
[[Obsidian Knowledge Vault]]
[[LLM Knowledge Linting]]
[[Wiki Knowledge Graph]]
[[Research Pipeline Orchestration]]
[[notebooklm-py CLI]]
[[Obsidian CLI]]
[[Wiki Event-Driven Automation]]
[[AI-Driven Content Pipeline]]
[[Claude Code Context Management]]
[[Claude Code]]
[[Claude Code Best Practices]]
[[Context-Aware Tool Loading]]
[[Decision: MCP vs CLI for Tool Integration]]
[[Decision: Obsidian vs NotebookLM as Knowledge Interface]]
[[Knowledge Evolution Pipeline]]
[[LLM Wiki vs RAG]]
[[LLM-Maintained Wikis Outperform Static Documentation]]
[[Lesson: Schema Is the Real Product — Not the Content]]
[[LightRAG]]
[[MCP Integration Architecture]]
[[Memory Lifecycle Management]]
[[Multi-Stage Ingestion Beats Single-Pass Processing]]
[[Obsidian as Knowledge Infrastructure Not Just Note-Taking]]
[[PARA Methodology]]
[[Per-Role Command Architecture]]
[[Plan Execute Review Cycle]]
[[Rework Prevention]]
[[Second Brain Architecture]]
[[Synthesis: Context Mode — MCP Sandbox for Context Saving]]
[[Synthesis: Karpathy LLM Wiki Method via Claude Code]]
[[Synthesis: Karpathy's LLM Wiki Idea File]]
[[Synthesis: LLM Wiki v2 -- Extending Karpathy's Pattern with Agentmemory Lessons]]
[[Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py]]
[[Synthesis: Obsidian + Claude Code Second Brain Setup]]
[[WSL2 Development Patterns]]
[[Zettelkasten Methodology]]
[[devops-control-plane]]
