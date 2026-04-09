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

- What is the right quality threshold for auto-filing query answers — too low creates noise, too high loses valuable insights? (Requires: empirical calibration data from deployed wiki systems; no existing wiki page specifies a concrete threshold)
- How should session-end compression balance completeness against conciseness? (Requires: empirical data on compression quality at different length ratios; no existing wiki page covers this)

## Answered Open Questions

### Can event hooks be implemented purely through Claude Code skills and scheduling, or do they require custom infrastructure?

Cross-referencing `WSL2 Development Patterns` and `Research Pipeline Orchestration`: yes, event hooks can be implemented using current Claude Code capabilities without custom infrastructure. The `WSL2 Development Patterns` page documents the exact implementation: tools/watcher.py (change detection daemon deployed as a systemd user service) fires the post-chain whenever wiki/ changes are detected. This is the "on new source" hook in production form. The `Research Pipeline Orchestration` page documents the "on-schedule" hook implementation path: "Claude Code Scheduling's two modes (local cron vs. remote tasks)" provide the scheduling substrate. The six wiki event hooks map to existing primitives: (1) on new source → tools/watcher.py + post-chain; (2) on session start → CLAUDE.md context loading; (3) on session end → crystallization skill triggered by Stop hook; (4) on query → quality-gated filing via PostToolUse hook in Claude Code; (5) on memory write → contradiction check in the wiki-agent skill; (6) on schedule → systemd timer or Claude Code Scheduling. The `WSL2 Development Patterns` page confirms that the watcher service auto-restarts on failure via systemd, providing hook reliability without manual intervention.

### How does the auto-contradiction check scale as the wiki grows — does it need to read the entire wiki on every write?

Cross-referencing `Research Pipeline Orchestration` and `Agent Orchestration Patterns`: full-wiki reads on every write do not scale. The `Research Pipeline Orchestration` page documents the wiki's domain-indexed structure — each domain has an `_index.md` and manifest.json provides a full page inventory with metadata. This means contradiction checking can be scoped: when a new page is written to domain X, only load domain X's index and related domains' summaries (via manifest metadata) rather than the full wiki. The `Agent Orchestration Patterns` page documents the OpenFleet approach to scale: "behavioral security on new/changed tasks" (step 5 of the 12-step cycle) is performed only on delta items, not the full fleet state. The same pattern applies here — contradiction checking should be incremental (compare new content against the affected domain's pages and their stated relationships), not global. As the wiki grows, the manifest.json summary layer becomes increasingly important as the scalable contradiction-check index.

### What is the failure mode when an automated hook produces low-quality output — is there a rollback mechanism?

Cross-referencing `Agent Orchestration Patterns`: the correct failure response is the "review gate" pattern documented in agent orchestration. The `Agent Orchestration Patterns` page states: "a mandatory review gate prevents unreviewed outputs from propagating downstream." For automated wiki hooks, this maps to: (1) hooks write to a staging location (e.g., raw/auto-generated/) rather than directly into wiki/; (2) a validation step (tools/validate.py) acts as the review gate — outputs that fail validation are rejected and flagged, not committed; (3) quality scoring (the "on query" hook's quality threshold) acts as a pre-review filter. The `WSL2 Development Patterns` page documents that tools/watcher.py runs the post-chain (validate → manifest → lint) after every write — this is the existing rollback-adjacent mechanism: invalid pages are caught and reported before they can corrupt the graph. A full rollback (reverting automated writes) is available via git, since the wiki is a git repository — "wiki is just a git repo of markdown files" (Obsidian Knowledge Vault page). The combination of staging → validate → commit provides rollback without requiring a separate rollback mechanism.

### Answered: The Six Hooks Map to Claude Code Best Practices Hook Taxonomy

The hooks architecture for wiki event automation maps directly to Claude Code's PostToolUse, PreToolUse, and Stop hooks. The six wiki event hooks can be implemented as native Claude Code hooks without additional infrastructure: (1) "on new source" → PostToolUse hook fires after any file write to raw/; (2) "on session start" → CLAUDE.md pre-loads session context; (3) "on session end" → Stop hook triggers crystallization; (4) "on query" → PostToolUse hook on any query tool call evaluates quality score; (5) "on memory write" → PostToolUse hook on wiki page writes triggers contradiction check; (6) "on schedule" → Claude Code Scheduling's two modes (local cron via systemd timer as documented in `WSL2 Development Patterns`, or remote tasks). This creates a direct bridge between the ai-agents and automation domains — the wiki's event-driven maintenance is implementable as standard Claude Code harness configuration.

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
[[Decision: Polling vs Event-Driven Change Detection]]
[[Lesson: Automation Is the Bridge Between Knowledge and Action]]
[[Lesson: Knowledge Systems Is the Foundational Domain for the Entire Wiki]]
[[Multi-Stage Ingestion Beats Single-Pass Processing]]
[[Obsidian CLI]]
[[Plan Execute Review Cycle]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
[[notebooklm-py CLI]]
