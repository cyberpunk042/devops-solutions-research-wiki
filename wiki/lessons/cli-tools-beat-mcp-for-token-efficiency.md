---
title: "CLI Tools Beat MCP for Token Efficiency"
type: lesson
domain: ai-agents
layer: 4
status: synthesized
confidence: high
maturity: growing
derived_from:
  - "Synthesis: Claude Code Accuracy Tips"
  - "Synthesis: Claude Code Harness Engineering"
  - "Claude Code"
  - "MCP Integration Architecture"
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-claude-code-accuracy-tips
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=D5bRTv6GhXk"
    title: "Claude Code Works Better When You Do This"
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    title: "Building Claude Code with Harness Engineering"
  - id: src-playwright-cli-vs-mcp
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=nN5R9DFYsXY"
    title: "Claude Code + Playwright CLI: Automate QA with Less Tokens"
tags: [cli, mcp, token-efficiency, skills, context-management, accuracy, tool-integration, agent-design]
---

# CLI Tools Beat MCP for Token Efficiency

## Summary

When integrating external tools into LLM-powered workflows, CLI tools paired with skill files consistently outperform MCP server integrations on token cost and output accuracy. MCP loads all registered tool schemas into the context window at session startup regardless of whether those tools will be used, while skill-based CLI tools inject instructions only when the relevant skill is invoked. The practical result is lower token consumption, fewer hallucinations from schema noise, and better accuracy — a tradeoff confirmed by independent practitioners and converging across multiple sources.

## Context

This lesson applies whenever you are deciding how to expose a capability to a Claude Code agent or any LLM-powered workflow:

- Choosing between building an MCP server vs. a CLI tool + SKILL.md to give Claude access to an external system (databases, APIs, wiki operations, Obsidian, NotebookLM)
- Designing agent architectures where multiple tools compete for context budget
- Debugging unexplained hallucinations or tool-call errors and looking for root causes beyond prompt quality
- Evaluating whether an existing MCP integration is worth its overhead for the frequency it is actually invoked
- Planning the MCP Integration Architecture evolution for the research wiki itself — where the tradeoff between discoverability and context cost is a live architectural decision

The tradeoff is most consequential in long-running sessions, multi-tool setups, and subagent pipelines where context pressure compounds across turns.

## Insight

MCP server integration is a convenient discovery mechanism — register a server once, and all its tools appear as native tool calls in any conversation. The cost of that convenience is that every registered MCP server loads its full JSON schema (tool names, parameter shapes, descriptions) into the context window at session initialization, before any tool has been called. In a single-tool setup this overhead is negligible. In a multi-server setup — even the research wiki's three planned MCP servers (wiki, NotebookLM, Obsidian) each with 6-8 tools — the cumulative schema payload consumes meaningful context budget on every single turn, regardless of relevance.

Skill-based CLI tools have the opposite loading profile. A SKILL.md file contains no schema overhead at rest. It only enters the context window when explicitly invoked — either by the user running a slash command or by the agent deciding the skill is relevant to the current task. Once loaded, the skill delivers targeted, prose-form instructions optimized for the model to read (not for a JSON-RPC parser to validate), then exits when the task is complete.

The accuracy implication is compounding: schema tokens from unused tools occupy space that could hold recent conversation turns or retrieved file content, pushing relevant history out of the window earlier. This is a form of context pollution — high-entropy tokens (JSON schema boilerplate) displacing lower-entropy, higher-signal tokens (actual task context). The Playwright CLI vs. MCP comparison referenced in the accuracy tips source produced a measurable result: the CLI approach was both cheaper and more accurate, not just one or the other.

The emerging practitioner consensus captured across multiple independent sources in 2026 is: use MCP when the tool needs to be callable from many different conversation contexts without setup, and use CLI+Skills when you control the agent's operating environment and want to minimize per-session overhead. For project-internal tooling — exactly the wiki's situation — CLI+Skills is the default winner.

## Evidence

**Playwright CLI vs. MCP direct comparison (src-claude-code-accuracy-tips):** A former Amazon/Microsoft senior AI engineer building BookZero.AI entirely with Claude Code ran a direct comparison between Playwright's MCP server and its CLI+Skills equivalent. The CLI was cheaper and more accurate. This is the most concrete single data point: same task, two integration modes, measurable difference in both cost and output quality.

**Playwright CLI vs. MCP mechanism video (src-playwright-cli-vs-mcp):** A dedicated comparison video provides the underlying mechanism with precise detail. MCP dumps the full accessibility tree into context after every single navigation step. CLI saves page state to a YAML file on disk and only loads it when Claude explicitly needs to find an element. In a 10-step QA test, MCP injects 10 full accessibility trees into the context window; CLI loads 2-3 targeted YAML snapshots on demand. The referenced "12x cost differential" in the accuracy tips source is substantiated by this mechanism: MCP's per-step context injection compounds across every action, while CLI's lazy-loading eliminates most of that overhead. The video also shows the accuracy trade-off clearly: CLI is more accurate for known-page tests (you know what fields and flows to expect), MCP retains an advantage for exploratory testing or unknown-page bug verification (where forced full-page visibility catches unexpected error states). This is the most mechanistically detailed evidence available.

**Microsoft officially recommends CLI over MCP for Playwright (src-playwright-cli-vs-mcp):** Playwright's creator (Microsoft) now recommends the CLI for AI agent integrations. The CLI also has 3x more features than the Playwright MCP server. This makes the CLI-over-MCP finding asymmetric — CLI wins on cost, accuracy for known tests, AND feature breadth. The tool's creator endorsing CLI over their own MCP server is a strong external validation signal.

**Google Trends signal (src-claude-code-accuracy-tips):** The accuracy tips source notes that Google Trends shows "CLI overtaking MCP" as a search trend in 2026. This is a weak signal individually but meaningful as confirmation that the practitioner community is converging on the same conclusion independently.

**Context loading mechanics (src-claude-code-accuracy-tips):** The source states explicitly: "CLI+Skills loads tool instructions only when relevant (skill loading is contextual), while MCP loads all tool schemas into context at startup." This is the mechanism, not just the observation.

**Harness engineering convergence (src-harness-engineering-article):** The harness engineering synthesis independently identifies the same pattern: "CLI over MCP is emerging consensus: Multiple sources now converge on CLI+Skills being more token-efficient and accurate than MCP for tool integration." The note explicitly flags a design implication: "consider a CLI+Skills alternative" for the research wiki's own MCP server.

**Claude Code extension comparison table (claude-code.md):** The Claude Code concept page documents the loading behavior of each extension type. MCP is listed as "Always available" — meaning always loaded — while Skills are "Invoked by user or auto" — meaning contextual. The table makes the tradeoff structural, not incidental.

**Context degradation curve (src-claude-code-accuracy-tips):** The same source documents that Claude Code accuracy drops significantly at 40% context usage and becomes unreliable at 60%+. Any mechanism that loads tokens into context at startup — before the task begins — consumes context budget that compounds this degradation curve sooner. MCP schema loading is a direct contributor to earlier context exhaustion in multi-tool setups.

## Applicability

**Domains where this lesson applies directly:**

- **AI agent design**: Any Claude Code project deciding how to expose tools. Default to CLI+Skills for project-internal tooling; reserve MCP for tools that need cross-project discoverability.
- **Research wiki architecture**: The three planned MCP servers (wiki, NotebookLM, Obsidian) are the right long-term target for discoverability and "Claude becomes replaceable" goals — but the cost is per-session schema overhead. The current CLI tool + SKILL.md approach (pipeline commands + wiki-agent skill) should be validated against the MCP target before migrating.
- **OpenFleet agent design**: Each fleet agent is a Claude Code instance. MCP servers registered fleet-wide would load their schemas into every agent's context, including agents that never use those tools. Skills distributed to specific agents are more targeted.
- **AICP and devops-control-plane**: Any future agent in the ecosystem faces the same tradeoff. Establish the CLI-first default now before MCP proliferates as the default integration pattern.

**When MCP is still the right choice:**

- Tools that need to be callable from many different, unrelated conversations without per-conversation setup (e.g., a company-wide database access tool)
- Tools used so frequently in a project that the skill-loading overhead (an extra invocation step) outweighs the schema overhead
- External tool ecosystems where MCP servers already exist and the integration cost of a CLI+Skills alternative is not justified
- Discoverability requirements — when the agent needs to autonomously discover what tools are available without being explicitly told

## Relationships

- DERIVED FROM: Synthesis: Claude Code Accuracy Tips
- DERIVED FROM: Synthesis: Claude Code Harness Engineering
- DERIVED FROM: Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens
- RELATES TO: Claude Code
- RELATES TO: MCP Integration Architecture
- RELATES TO: Claude Code Context Management
- RELATES TO: Claude Code Skills
- FEEDS INTO: MCP Integration Architecture
- CONTRADICTS: default assumption that MCP is the standard tool integration pattern

## Backlinks

[[Synthesis: Claude Code Accuracy Tips]]
[[Synthesis: Claude Code Harness Engineering]]
[[Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens]]
[[Claude Code]]
[[MCP Integration Architecture]]
[[Claude Code Context Management]]
[[Claude Code Skills]]
[[default assumption that MCP is the standard tool integration pattern]]
[[Context Management Is the Primary LLM Productivity Lever]]
[[Context-Aware Tool Loading]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
