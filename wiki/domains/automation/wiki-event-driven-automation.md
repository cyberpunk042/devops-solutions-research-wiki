---
title: "Wiki Event-Driven Automation"
type: concept
domain: automation
status: synthesized
confidence: medium
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-llm-wiki-v2-agentmemory
    type: documentation
    url: "https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2"
    file: raw/articles/llm-wiki-v2-extending-karpathys-llm-wiki-pattern-with-lessons-from-building-agen.md
    title: "LLM Wiki v2 -- Extending Karpathy's LLM Wiki Pattern with Lessons from Building Agentmemory"
    ingested: 2026-04-08
  - id: src-obsidian-claude-code-second-brain
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=Y2rpFa43jTo"
    file: raw/transcripts/obsidian-claude-code-the-second-brain-setup-that-actually-works.txt
    title: "Obsidian + Claude Code: The Second Brain Setup That Actually Works"
    ingested: 2026-04-08
tags: [automation, event-driven, hooks, auto-ingest, auto-lint, wiki-maintenance, crystallization]
---

# Wiki Event-Driven Automation

## Summary

Wiki Event-Driven Automation is the pattern of replacing manual wiki operations (ingest, lint, query filing) with automated hooks that fire in response to specific events. Proposed in the LLM Wiki v2 document as the biggest practical gap in Karpathy's original pattern, it defines six trigger points: on new source (auto-ingest and entity extraction), on session start (load relevant context), on session end (compress and file insights), on query (auto-file quality answers exceeding a threshold), on memory write (check for contradictions), and on schedule (periodic lint, consolidation, retention decay). The Obsidian + Claude Code second brain video provides a concrete implementation of this pattern through its "onboard projects" skill, which automates multi-source data collection and structured filing. The goal is to keep the human focused on curation and strategic direction while automating all bookkeeping.

## Key Insights

- **Six core automation hooks**: (1) On new source -- auto-ingest, extract entities, update graph and index. (2) On session start -- load relevant context from the wiki. (3) On session end -- compress session into observations, file insights. (4) On query -- assess whether the answer is worth filing back (quality score above threshold). (5) On memory write -- check for contradictions with existing knowledge, trigger supersession. (6) On schedule -- periodic lint, consolidation between memory tiers, retention decay.

- **Crystallization as automated distillation**: A completed chain of work (research thread, debugging session, analysis) should be automatically distilled into a structured digest: what was the question, what was found, what entities were involved, what lessons emerged. This digest becomes a first-class wiki page and its lessons strengthen existing knowledge. Explorations become sources, just like articles or papers.

- **Quality-gated auto-filing**: Not every query answer deserves wiki permanence. A quality scoring mechanism determines which answers cross the threshold for automatic filing. This prevents the wiki from being cluttered with trivial Q&A while ensuring valuable analyses are preserved.

- **Contradiction detection on write**: Every time new content is written to the wiki, it should be automatically checked against existing knowledge for contradictions. When conflicts are found, the system triggers supersession workflow rather than silently creating inconsistencies.

- **Practical implementation via Claude Code skills**: The Obsidian + Claude Code video demonstrates a concrete version of this automation through custom skills that automate ingestion from Gmail, local files, and user-pasted content into structured Obsidian folders -- showing that event-driven wiki automation is achievable with current Claude Code capabilities.

- **Obsidian Git auto-commit as a passive hook**: The Obsidian Git plugin's auto-commit feature (committing changes at configurable intervals) is a simple example of event-driven automation -- file changes trigger version control operations without manual intervention.

## Deep Analysis

This concept represents the maturation path from Karpathy's manual-first approach to a fully automated knowledge management system. Karpathy explicitly prefers interactive ingestion: "Personally I prefer to ingest sources one at a time and stay involved." The event-driven approach respects this preference while removing the burden of remembering to perform maintenance operations -- lint runs automatically on schedule, contradictions are flagged on write rather than discovered later, and session insights are captured without manual filing.

The crystallization mechanism is particularly valuable because it captures a class of knowledge that is otherwise lost. When a user spends 30 minutes with the LLM exploring a question, the intermediate reasoning, dead ends, and final conclusions all exist in the chat history but vanish when the session closes. Automatic crystallization preserves the conclusions and key reasoning in a structured format, making explorations compound in the knowledge base.

The six-hook architecture maps naturally to existing Claude Code capabilities. On-schedule hooks map to Claude Code Scheduling (local cron or remote tasks). Skill-triggered automation (like the "onboard projects" skill) demonstrates on-new-source hooks. The session start/end hooks could be implemented through Claude Code's workspace context loading. Quality-gated filing and contradiction detection require additional LLM processing but are straightforward prompt engineering tasks.

The connection between this concept and the AI-Driven Content Pipeline is direct: both represent automation patterns where Claude Code acts as an orchestration layer. The content pipeline automates research-to-output workflows; event-driven wiki automation automates knowledge-maintenance workflows. Both remove the human from routine operations while keeping them in the strategic loop.

## Open Questions

- What is the right quality threshold for auto-filing query answers -- too low creates noise, too high loses valuable insights?
- How should session-end compression balance completeness against conciseness?
- Can event hooks be implemented purely through Claude Code skills and scheduling, or do they require custom infrastructure?
- How does the auto-contradiction check scale as the wiki grows -- does it need to read the entire wiki on every write?
- What is the failure mode when an automated hook produces low-quality output -- is there a rollback mechanism?
- Cross-source insight: The hooks architecture here maps directly to Claude Code Best Practices' hook taxonomy (PostToolUse, PreToolUse, Stop hooks). The six wiki event hooks could be implemented as Claude Code hooks, creating a direct bridge between the ai-agents and automation domains. The "on-schedule" hook maps to Claude Code Scheduling's two modes (local cron vs. remote tasks).

## Relationships

- DERIVED FROM: src-llm-wiki-v2-agentmemory
- DERIVED FROM: src-obsidian-claude-code-second-brain
- EXTENDS: LLM Wiki Pattern
- EXTENDS: Wiki Ingestion Pipeline
- BUILDS ON: Claude Code Skills
- BUILDS ON: Claude Code Scheduling
- ENABLES: Memory Lifecycle Management
- ENABLES: LLM Knowledge Linting
- RELATES TO: AI-Driven Content Pipeline
- FEEDS INTO: MCP Integration Architecture
- FEEDS INTO: Research Pipeline Orchestration
- RELATES TO: Claude Code Best Practices

## Backlinks

[[src-llm-wiki-v2-agentmemory]]
[[src-obsidian-claude-code-second-brain]]
[[LLM Wiki Pattern]]
[[Wiki Ingestion Pipeline]]
[[Claude Code Skills]]
[[Claude Code Scheduling]]
[[Memory Lifecycle Management]]
[[LLM Knowledge Linting]]
[[AI-Driven Content Pipeline]]
[[MCP Integration Architecture]]
[[Research Pipeline Orchestration]]
[[Claude Code Best Practices]]
[[Agent Orchestration Patterns]]
[[Multi-Stage Ingestion Beats Single-Pass Processing]]
[[Obsidian CLI]]
[[Plan Execute Review Cycle]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
[[notebooklm-py CLI]]
