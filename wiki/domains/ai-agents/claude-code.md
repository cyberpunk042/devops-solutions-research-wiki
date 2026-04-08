---
title: "Claude Code"
type: concept
domain: ai-agents
status: synthesized
confidence: authoritative
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-shanraisshan-claude-code-best-practice
    type: documentation
    url: "https://github.com/shanraisshan/claude-code-best-practice"
    file: raw/articles/shanraisshanclaude-code-best-practice.md
    title: "Claude Code Best Practices"
    ingested: 2026-04-08
  - id: src-karpathy-claude-code-10x
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=7sInxhTDA7U"
    file: raw/transcripts/karpathy-claude-code-10x.txt
    title: "Andrej Karpathy Just 10x'd Everyone's Claude Code"
    ingested: 2026-04-08
  - id: src-token-hacks-claude-code
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=49V-5Ock8LU"
    file: raw/transcripts/18-claude-code-token-hacks-in-18-minutes.txt
    title: "18 Claude Code Token Hacks in 18 Minutes"
    ingested: 2026-04-08
tags: [claude-code, ai-agent, coding-agent, anthropic, skills, hooks, mcp, subagents, context-management, automation]
---

# Claude Code

## Summary

Claude Code is Anthropic's official CLI coding agent — a terminal-resident AI that reads, writes, and reasons about codebases. It operates through a tool-use loop where the model decides which tools to call (Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch, Agent, etc.) to accomplish user requests. Beyond basic code editing, it supports a rich extension ecosystem: Skills (SKILL.md instruction files), Hooks (shell commands triggered by events), MCP servers (external tool integration), subagents (parallel isolated workers), plans/todos (structured work tracking), and persistent memory. It is the execution engine behind the research wiki's ingestion pipeline, the backbone of each OpenFleet agent, and the primary human-to-AI interface for the entire 4-project ecosystem.

## Key Insights

- **Tool-use agent loop**: Claude Code is not a chatbot — it's an agent that iteratively decides which tools to invoke. Each response can chain multiple tool calls (Read → Edit → Bash → validate). The loop continues until the task is complete or the model yields to the user.

- **Three-tier extension system**: Commands (built-in slash commands like /help, /compact, /clear), Skills (SKILL.md files loaded into context — reusable, shareable knowledge), Hooks (shell scripts triggered before/after events like tool calls, model responses, notifications).

- **Context management is the critical skill**: The context window is finite. Effective use requires: CLAUDE.md project instructions (always loaded), compact (/compact to summarize and free context), subagents (isolated context for research tasks), targeted reads (specific line ranges, not whole files), and plan/todo tracking (externalized state).

- **Subagent parallelism**: The Agent tool spawns isolated workers that share the filesystem but not the conversation context. Use for: parallel research, independent file modifications, isolated testing. Each subagent gets a fresh context window, protecting the main conversation from context bloat.

- **MCP integration**: Model Context Protocol servers expose external tools to Claude Code. Any MCP server (database, API, custom tool) becomes available as a tool call. The research wiki's future architecture (backlog item 3) envisions MCP servers for wiki operations, NotebookLM, and Obsidian.

- **Hooks for automated behaviors**: Shell commands executed on events (pre-tool-call, post-tool-call, notification, etc.). Use for: linting on save, auto-formatting, custom notifications, git hooks integration. Unlike skills (which are instructions), hooks are executable actions.

- **Skills as transferable knowledge**: SKILL.md files teach Claude Code how to operate specific systems. The wiki-agent skill teaches ingestion, querying, linting, export. Skills are versionable, shareable, and composable. The agentskills.io ecosystem standardizes the format.

- **CLAUDE.md as project brain**: Loaded into every conversation. Defines conventions, schemas, tooling commands, quality gates. The research wiki's CLAUDE.md is the single source of truth for how the wiki system operates.

- **Persistent memory across sessions**: Memory files in `~/.claude/projects/` persist across conversations. Used to remember user preferences, project state, feedback, and references. Structured with frontmatter (name, description, type).

- **Plans and todos for structured work**: Plans decompose complex tasks into steps. Todos track progress within a session. Both externalize state from the context window, enabling work that spans beyond what fits in memory.

## Deep Analysis

### Role in the Ecosystem

Claude Code occupies a unique position — it is simultaneously:

1. **The research wiki's operator**: Every ingestion, validation, export, and quality check flows through Claude Code. The wiki-agent skill defines how Claude Code should process sources, create pages, and maintain quality.

2. **Each OpenFleet agent's runtime**: All 10 fleet agents are Claude Code instances connected through the OpenClaw gateway. SOUL.md and HEARTBEAT.md are essentially Claude Code skills that define agent identity and periodic tasks.

3. **The primary human interface**: The user interacts with the entire ecosystem through Claude Code conversations. Claude Code is the orchestration layer between human intent and system execution.

4. **Its own documentation subject**: The wiki documents Claude Code's features, best practices, and patterns — which Claude Code then uses to improve its own operation. This is a self-referential knowledge loop.

### Extension Comparison

| Mechanism | Loaded When | Scope | Format | Example |
|-----------|------------|-------|--------|---------|
| CLAUDE.md | Every conversation | Project-wide | Markdown | Schema, conventions, commands |
| Skills | Invoked by user or auto | Task-specific | SKILL.md | wiki-agent, notebooklm |
| Hooks | Event-triggered | Action-specific | Shell command | Pre-commit lint, format on save |
| MCP | Always available | Tool-specific | JSON-RPC server | Database access, API calls |
| Memory | Loaded per project | Cross-session | Markdown + frontmatter | User preferences, feedback |
| Subagents | Spawned on demand | Isolated task | Agent tool call | Parallel file research |

### The Self-Improving Pattern

The research wiki creates a feedback loop:
1. Claude Code ingests sources about Claude Code best practices
2. The wiki synthesizes these into concept pages (claude-code-best-practices, claude-code-context-management, etc.)
3. CLAUDE.md references these patterns as project conventions
4. Claude Code follows these conventions when operating the wiki
5. New sources about Claude Code patterns get ingested, enriching the cycle

## Open Questions

- What is the practical limit of concurrent subagents before performance degrades?
- Can Claude Code's context window expansion (1M context) eliminate the need for aggressive compaction strategies?
- How should skills be versioned and tested for breaking changes across Claude Code updates?
- What is the optimal split between CLAUDE.md instructions and skill files for project conventions?

## Relationships

- ENABLES: OpenFleet
- ENABLES: Wiki Ingestion Pipeline
- ENABLES: Claude Code Skills
- ENABLES: Claude Code Best Practices
- ENABLES: Claude Code Context Management
- RELATES TO: OpenClaw
- RELATES TO: AICP
- RELATES TO: Obsidian CLI
- RELATES TO: notebooklm-py CLI
- RELATES TO: LLM Wiki Pattern

## Backlinks

[[OpenFleet]]
[[Wiki Ingestion Pipeline]]
[[Claude Code Skills]]
[[Claude Code Best Practices]]
[[Claude Code Context Management]]
[[OpenClaw]]
[[AICP]]
[[Obsidian CLI]]
[[notebooklm-py CLI]]
[[LLM Wiki Pattern]]
[[Always Plan Before Executing]]
[[CLI Tools Beat MCP for Token Efficiency]]
[[Decision: MCP vs CLI for Tool Integration]]
[[Harness Engineering]]
[[Local LLM Quantization]]
[[MCP Integration Architecture]]
[[OpenArms]]
[[Plan Execute Review Cycle]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
[[Synthesis: Claude Code Harness Engineering]]
[[Synthesis: Superpowers Plugin — End of Vibe Coding (Full Tutorial)]]
[[devops-control-plane]]
