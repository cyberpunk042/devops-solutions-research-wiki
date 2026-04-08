---
title: "Context-Aware Tool Loading"
type: pattern
domain: ai-agents
layer: 5
status: synthesized
confidence: high
maturity: growing
derived_from:
  - "Synthesis: Claude Code Accuracy Tips"
  - "Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens"
  - "CLI Tools Beat MCP for Token Efficiency"
  - "Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py"
instances:
  - page: "Claude Code Skills"
    context: "Skills load their instruction content into the context window only when invoked via slash command or agent decision. MCP servers load all registered tool schemas at session startup regardless of whether those tools are ever called. The result is up to 12x token cost difference between the two integration modes."
  - page: "Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens"
    context: "Playwright CLI writes full page accessibility data to a YAML file on disk and reads it into context only when Claude needs to locate a specific element. The MCP server dumps the full accessibility tree into context after every single navigation step. In a 10-step QA test, MCP injects 10 full trees; CLI loads 2-3 targeted snapshots on demand."
  - page: "Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py"
    context: "All research, competitive analysis, and documentation lives in NotebookLM notebooks. Claude Code queries the external knowledge base via the notebooklm-py skill only when it needs a grounded answer, rather than loading all source documents into the context window at session start."
  - page: "Context7"
    context: "Fetches up-to-date, version-specific library documentation into context on demand as a fact-checking step after implementation. Docs are never pre-loaded; they enter the context window only when the user or agent explicitly invokes the Context7 skill for a specific library."
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-claude-code-accuracy-tips
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=D5bRTv6GhXk"
    title: "Claude Code Works Better When You Do This"
  - id: src-playwright-cli-vs-mcp
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=nN5R9DFYsXY"
    title: "Claude Code + Playwright CLI: Automate QA with Less Tokens"
  - id: src-notebooklm-claude-code-workflow
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=fV17ZkPBlAc"
    title: "This NotebookLM + Claude Code Workflow Is Insane"
tags: [context-management, token-efficiency, deferred-loading, skills, mcp, cli, tool-design, agent-architecture, accuracy, notebooklm, playwright, context7]
---

# Context-Aware Tool Loading

## Summary

Only load tool schemas, documentation, or external data into the context window when the agent actually needs them — never dump everything at session start. The mechanism is always deferred loading: information lives on disk, in an external service, or behind a CLI boundary until an explicit retrieval step pulls precisely what is relevant. Eager loading compounds as the context fills, degrading accuracy on everything else in the window. This pattern recurs identically across integration styles (MCP vs CLI+Skills), browser automation tools, external knowledge bases, and documentation fetchers — making it one of the most broadly applicable structural principles in LLM agent design.

## Pattern Description

Every LLM agent operates within a fixed context window. Tokens loaded at startup for "just in case" access — full tool schemas, complete accessibility trees, all documentation, entire knowledge bases — occupy context budget before the first task-relevant token has been written. As context fills, Claude Code accuracy drops measurably: high at 20% usage, significantly degraded at 40%, unreliable at 60%+, producing bugs and hallucinations at 80%. Any mechanism that pre-loads information at session initialization accelerates movement along this degradation curve.

The pattern that counters this is deferred loading: information is stored outside the context window (on disk as YAML, in an external knowledge base, behind a CLI boundary, in a documentation service) and retrieved only at the moment the agent determines it is necessary. The agent issues an explicit read, query, or fetch call, pulls a targeted subset of the available information, uses it for the immediate task, and does not carry it forward into subsequent turns unless required.

The key structural insight is that this pattern is not tool-specific — it is a recurring design decision. Every time you introduce a new information source into an agent workflow, you face the same binary: eager (load at startup, always available, always consuming context) vs. deferred (load on demand, narrowly scoped, context-clean). The eager approach optimizes for availability; the deferred approach optimizes for signal-to-noise ratio in the context window. Because accuracy is directly coupled to signal-to-noise ratio, deferred loading is the default-correct choice for any information source that is not required on every single turn.

The cost of getting this wrong compounds. Schema tokens from unused tools displace conversation history. Stale page trees from earlier navigation steps crowd out current task context. Pre-loaded documentation forces the model to attend to dozens of irrelevant API methods before finding the one it needs. Each individually small inefficiency multiplies across every turn in a long session, across every agent in a fleet, and across every call in a multi-step pipeline.

## Instances

### Skills vs. MCP: The Schema Loading Split

Claude Code supports two tool integration modes. MCP servers register their full JSON schema (tool names, parameter shapes, descriptions) into the context window at session initialization — before any tool has been called, before the agent knows what task it will perform. Skills (SKILL.md files) contain no schema at rest; they enter the context window only when explicitly invoked via slash command or agent decision, delivering targeted prose instructions and then exiting when the task completes.

The practical consequence is measurable. With multiple MCP servers registered, cumulative schema payload consumes meaningful context budget on every single turn regardless of relevance. The accuracy tips source documents this directly: "CLI+Skills loads tool instructions only when relevant (skill loading is contextual), while MCP loads all tool schemas into context at startup." Google Trends data from 2026 shows CLI search interest overtaking MCP as the practitioner community converges on this conclusion. The research wiki itself reflects this tradeoff: the three planned MCP servers (wiki, NotebookLM, Obsidian) deliver discoverability at the cost of per-session schema overhead that would be present even in conversations that never invoke those tools.

### Playwright CLI vs. MCP: The Accessibility Tree Problem

The Playwright browser automation comparison provides the most mechanistically detailed evidence for this pattern. The MCP integration dumps the full accessibility tree of the current page into Claude's context window after every single navigation step — after every click, every form fill, every page load. A 10-step QA test injects 10 full accessibility trees, including stale trees from pages the agent has already left.

The CLI integration takes the opposite approach: it writes the full page accessibility data to a YAML file on disk (the "sticky notes" metaphor from the source). Claude Code reads that file only when it needs to locate a specific element; it skips the read entirely when it already knows what action to take. In a 10-step test, CLI may load 2-3 targeted YAML snapshots. The token differential cited across sources is 12x. Microsoft (Playwright's creator) now officially recommends the CLI for AI agent use, and the CLI also has 3x more features than the MCP server — making the choice asymmetric: CLI wins on cost, accuracy for known-page tests, and feature breadth simultaneously.

The accuracy tradeoff is scenario-dependent: CLI is more accurate when the agent knows what to expect (known fields, known flows), while MCP's forced full-page visibility retains an advantage for exploratory testing on unknown pages. This maps directly onto the pattern's applicability conditions.

### NotebookLM as External Knowledge Base: Keeping Research Out of Context

The NotebookLM + Claude Code workflow demonstrates the pattern at the knowledge base level. Instead of loading all research documents, competitive analysis sources, and reference documentation into the session context at the start of each conversation, the entire knowledge corpus lives in NotebookLM notebooks (up to 300 sources per notebook, 250+ sources in the competitive analysis use case). Claude Code queries the external knowledge base via the `notebooklm-py` CLI skill only when it needs a grounded answer for a specific question.

The result is that a 35-competitor analysis with 250-300 source documents never enters the context window as raw material. Claude Code receives targeted, synthesized answers — a few sentences per query, configured via NotebookLM's "learning guide" persona for shorter, Claude-consumable responses. The research wiki follows the identical architecture: wiki pages live on disk and are retrieved via `wiki_search` and `wiki_read_page` on demand rather than pre-loaded into every conversation.

### Context7: On-Demand Documentation Fetching

Context7 (available as both MCP server and CLI+Skill) fetches up-to-date, version-specific library documentation into context on demand. The explicit use pattern is as a post-implementation fact-checking step: write the code first, then invoke Context7 to verify the implementation against current documentation for the specific library version in use. Docs are never pre-loaded; they enter the context window only when the agent or user explicitly requests documentation for a specific library.

This is the documentation layer's application of deferred loading. The alternative — loading all potentially relevant library docs at session start — would consume context budget on every turn for every library in a project's dependency graph, regardless of which library the current task touches.

## When To Apply

- Any information source used on fewer than ~80% of turns in a session: pre-loading the minority case penalizes every turn for the majority case.
- Multi-tool setups where several systems are registered: cumulative eager-loading overhead from N tools is additive; deferred loading keeps overhead at zero for unneeded tools.
- Long-running sessions, multi-step pipelines, and subagent workflows where context pressure compounds across turns.
- Known-workflow automation (QA scripts, research pipelines, batch processing) where the agent executes structured steps against predictable pages or data rather than exploring unknown territory.
- External knowledge bases larger than what a context window can hold: NotebookLM notebooks, wikis, documentation libraries, code repositories. Deferred loading is not optional here — it is the only viable approach.
- Any integration where you control the agent's operating environment and can design the retrieval step: project-internal tooling, custom CLI tools, skill files.

## When Not To

- Exploratory or discovery-mode tasks where the agent does not know in advance what information it will need: forcing explicit retrieval calls adds friction when the agent cannot predict what to retrieve. MCP's "always available" schema makes more sense when tool selection is unpredictable.
- Tools invoked on nearly every turn: the overhead of a deferred fetch on 95% of turns may exceed the savings from not pre-loading on the remaining 5%. Measure before optimizing.
- External services with high query latency where on-demand fetching creates unacceptable wait times in interactive workflows. Pre-fetching at session start may be the better UX tradeoff.
- When discoverability is a hard requirement: MCP's schema registration allows the agent to autonomously discover what tools exist without being explicitly told. If the agent needs to self-direct across an unknown toolset, eager loading is the only mechanism.
- Very short sessions (single-turn or two-turn) where context degradation cannot compound: the pattern's benefit scales with session length and tool count.

## Relationships

- DERIVED FROM: Synthesis: Claude Code Accuracy Tips
- DERIVED FROM: Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens
- DERIVED FROM: CLI Tools Beat MCP for Token Efficiency
- DERIVED FROM: Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py
- EXTENDS: CLI Tools Beat MCP for Token Efficiency
- RELATES TO: Claude Code Context Management
- RELATES TO: Claude Code Skills
- RELATES TO: MCP Integration Architecture
- RELATES TO: LLM Wiki Pattern
- CONTRADICTS: default assumption that registering all MCP tools at startup is cost-free
- FEEDS INTO: Research Pipeline Orchestration
- FEEDS INTO: Wiki Ingestion Pipeline

## Backlinks

[[Synthesis: Claude Code Accuracy Tips]]
[[Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens]]
[[CLI Tools Beat MCP for Token Efficiency]]
[[Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py]]
[[Claude Code Context Management]]
[[Claude Code Skills]]
[[MCP Integration Architecture]]
[[LLM Wiki Pattern]]
[[default assumption that registering all MCP tools at startup is cost-free]]
[[Research Pipeline Orchestration]]
[[Wiki Ingestion Pipeline]]
[[Cross-Domain Patterns]]
