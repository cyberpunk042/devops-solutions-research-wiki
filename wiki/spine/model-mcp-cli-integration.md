---
title: "Model Guide: MCP + CLI Integration"
type: learning-path
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: growing
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [mcp, cli, integration, model-guide, learning-path, token-efficiency, tool-integration, playwright, sandbox, spine]
---

# Model Guide: MCP + CLI Integration

## Summary

The MCP + CLI Integration model resolves one of the most consequential architectural decisions in LLM agent design: how to expose external tools to an agent without degrading its context window. MCP servers are powerful but always-on — they load all registered tool schemas at session startup, consuming context budget before any task-relevant token is written. CLI tools paired with skills load on demand, injecting targeted instructions only when the relevant capability is needed. The model documents when each approach is correct, the evidence base for the 12x token cost differential, and the sandbox pattern (context-mode) that achieves 98% context saving by running heavy operations in an isolated subagent.

## Prerequisites

- Understanding of Claude Code's context window constraint and the 40%/60%/80% degradation curve (see Model Guide: Claude Code)
- Familiarity with the concept of skill files (SKILL.md) as deferred-load instruction sets
- MCP protocol knowledge is helpful but not required — the model explains the relevant parts

## Sequence

### L1 — Primary Sources

- [[Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens]] — The Playwright CLI vs MCP comparison; 10-step QA test measuring token cost and accuracy for both approaches; origin of the CLI-beats-MCP finding
- `wiki/sources/src-harness-engineering-article.md` — The harness engineering model; origin of the context-mode sandbox pattern and the 98% context saving figure
- [[Synthesis: Claude Code Accuracy Tips]] — The accuracy tips source; origin of the degradation curve data; MCP schema noise as a documented failure mode

### L2 — Core Concepts

Read in this order:

1. **CLI Tools Beat MCP for Token Efficiency** ([[CLI Tools Beat MCP for Token Efficiency]]) — The core lesson: schema tokens from unused MCP tools displace task-relevant context; CLI+Skills loads nothing until invoked; the 12x cost differential is empirically validated. Start here.
2. **Context-Aware Tool Loading** ([[Context-Aware Tool Loading]]) — The pattern that explains WHY CLI wins: defer all tool schema loading until the agent actually needs it; eager loading accelerates movement along the degradation curve. Covers MCP vs CLI vs external knowledge bases uniformly.
3. **Decision: MCP vs CLI for Tool Integration** ([[Decision: MCP vs CLI for Tool Integration]]) — The resolved decision: CLI+Skills as default for project-internal operational tooling; MCP for external service bridges and cross-conversation discoverability. With full alternatives analysis.
4. **MCP Integration Architecture** (`wiki/domains/tools-and-platforms/mcp-integration-architecture.md`) — What MCP is, how it works, when it genuinely wins; the wiki's own MCP server (15 tools); scenarios where MCP's always-available property outweighs its cost.
5. **Harness Engineering** ([[Harness Engineering]]) — The context-mode pattern: an isolated subagent receives the heavy task, executes against a clean context window, and returns only the result to the parent session; achieves 98% context saving for operations like full codebase analysis.
6. **Playwright CLI vs MCP** ([[Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens]]) — Concrete case study: Playwright CLI writes full page accessibility data to YAML on disk, reads it into context only when Claude needs a specific element; MCP dumps the full accessibility tree after every navigation step.
7. **Playwright MCP Visual Testing** ([[Synthesis: Playwright MCP for Visual Development Testing]]) — The counter-case: when Playwright MCP IS the right choice; interactive visual development where always-available tool calls make the workflow faster.

### L3 — Comparisons

- **LLM Wiki vs RAG** ([[LLM Wiki vs RAG]]) — The same deferred-vs-eager loading decision applied to knowledge retrieval: index navigation vs vector embedding lookup.

### L4 — Lessons (Validated Insights)

- **CLI Tools Beat MCP for Token Efficiency** ([[CLI Tools Beat MCP for Token Efficiency]]) — Already the entry point above; re-read the Evidence section specifically for the 12x figure and the Google Trends adoption data.

### L5 — Patterns (Structural Templates)

- **Context-Aware Tool Loading** ([[Context-Aware Tool Loading]]) — The structural template; four instance implementations (Skills, Playwright CLI, NotebookLM, Context7) that all instantiate the same deferred-load principle.

### L6 — Decisions (Resolved Choices)

- **Decision: MCP vs CLI for Tool Integration** ([[Decision: MCP vs CLI for Tool Integration]]) — The resolved choice with full alternatives analysis; re-read the Consequences section for the concrete bindings (which tools go CLI, which go MCP in this ecosystem).

## Key Evidence Summary

For quick reference when making integration decisions:

- **12x token cost differential**: CLI+Skills vs MCP for the same Playwright operation (measured)
- **98% context saving**: Context-mode sandbox pattern (Harness Engineering; measured on full codebase analysis tasks)
- **Degradation thresholds**: 40% context fill = significant degradation; 60% = unreliable; 80% = bugs and hallucinations (Claude Code Accuracy Tips)
- **Google Trends**: CLI tooling overtaking MCP in adoption as practitioners discover the cost differential (2026 data)
- **Schema token pollution**: Each MCP server with 6-8 tools adds schema overhead to EVERY message, even those unrelated to that server's domain

## Outcomes

After completing this learning path you will understand:

- Why MCP's always-available property comes at the specific cost of context budget on every turn, not just when MCP tools are called
- The CLI+Skills deferred-load model: how SKILL.md files only enter the context window when invoked, and how `context: fork` further isolates execution
- When MCP genuinely wins: external services without native CLI, tools needing cross-conversation discoverability, interactive workflows benefiting from always-available tool calls
- The sandbox pattern for the most context-intensive operations: isolated subagent, clean window, result-only return
- How to apply the Context-Aware Tool Loading pattern uniformly across MCP servers, browser automation tools, external knowledge bases, and documentation fetchers
- The concrete integration bindings in this ecosystem: which tools are CLI, which are MCP, and why

## Relationships

- FEEDS INTO: [[Model Guide: Claude Code]]
- FEEDS INTO: [[Model Guide: Skills + Commands + Hooks]]
- BUILDS ON: [[CLI Tools Beat MCP for Token Efficiency]]
- BUILDS ON: [[Context-Aware Tool Loading]]
- BUILDS ON: [[Decision: MCP vs CLI for Tool Integration]]
- RELATES TO: [[Model Guide: Ecosystem Architecture]]
- RELATES TO: [[Harness Engineering]]

## Backlinks

[[Model Guide: Claude Code]]
[[Model Guide: Skills + Commands + Hooks]]
[[CLI Tools Beat MCP for Token Efficiency]]
[[Context-Aware Tool Loading]]
[[Decision: MCP vs CLI for Tool Integration]]
[[Model Guide: Ecosystem Architecture]]
[[Harness Engineering]]
[[Model: Claude Code]]
[[Model: Skills, Commands, and Hooks]]
