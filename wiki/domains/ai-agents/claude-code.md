---
title: "Claude Code"
type: concept
layer: 2
maturity: growing
domain: ai-agents
status: synthesized
confidence: authoritative
created: 2026-04-08
updated: 2026-04-10
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

> [!info] Extension system reference card
>
> | Layer | Mechanism | Loading Behavior | Best For |
> |-------|-----------|-----------------|----------|
> | **Commands** | Built-in slash commands | Always available | Navigation, session control (/help, /compact, /clear) |
> | **Skills** | SKILL.md instruction files | On-demand (invoked or auto-detected) | Reusable workflows, transferable knowledge |
> | **Hooks** | Shell scripts on events | Event-triggered (pre/post tool calls) | Automated behaviors, stage-gate enforcement |
> | **MCP** | External tool servers | Schema loaded at session start | Cross-conversation tool discoverability |
> | **Subagents** | Isolated parallel workers | Fresh context per spawn | Parallel research, independent tasks |

> [!tip] Claude Code is an agent loop, not a chatbot
> It iteratively decides which tools to invoke — Read → Edit → Bash → validate in a single response. The loop continues until the task is complete. The tool-use pattern makes it the execution engine behind the wiki, each OpenFleet agent, and the primary human-to-AI interface for the ecosystem.

**Context management is the critical skill.** The context window is finite. CLAUDE.md (always loaded, <200 lines), /compact at 60%, subagents (isolated context), targeted reads (line ranges, not whole files), plans/todos (externalized state).

**CLAUDE.md is the project brain.** Loaded every conversation. Defines conventions, schemas, tooling, quality gates. The research wiki's CLAUDE.md is the single source of truth for the entire system.

**Persistent memory across sessions.** Files in `~/.claude/projects/` survive conversations — user preferences, project state, feedback, references. Structured with frontmatter.

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

- Can Claude Code's context window expansion (1M context) eliminate the need for aggressive compaction strategies? (Requires: external research on 1M context degradation curve vs. compaction cost tradeoffs; the accuracy tips source documents the 40%/60%/80% degradation curve for standard context windows but does not address 1M context behavior)

### Answered Open Questions

**Q: What is the practical limit of concurrent subagents before performance degrades?**

Cross-referencing `Claude Code Best Practices` and `Agent Orchestration Patterns`: the limit is not a fixed number but is governed by two constraints. First, the `Agent Orchestration Patterns` page documents that OpenFleet caps at 2 dispatches per 30-second cycle to "prevent runaway parallel execution" — this is the production-validated upper bound for an autonomous fleet with 10 agents. Second, the `Claude Code Best Practices` page notes that subagents each receive "fresh context windows" and share the filesystem. The practical constraint is filesystem contention (concurrent writes to the same files cause race conditions) and cost (each subagent is a full context window). The `Context-Aware Tool Loading` pattern page confirms that the degradation curve is per-agent (each agent's accuracy degrades at 40%/60%/80% context fill), not cumulative. Therefore, 2-4 concurrent subagents on independent tasks is the empirically validated safe range; beyond that, filesystem coordination overhead and parallel cost begin to exceed the parallelism benefit.

**Q: How should skills be versioned and tested for breaking changes across Claude Code updates?**

Cross-referencing `Claude Code Skills` and `Claude Code Best Practices`: skill versioning follows a maturity-based approach, not semantic versioning. The `Claude Code Skills` page documents that skills exist on a "complexity spectrum: seed skill is a single SKILL.md; a mature production skill is a folder with SKILL.md + references/ + scripts/ + examples/." The `Claude Code Best Practices` page states that skills should include a "Gotchas section for known failure points" — this is where breaking-change history accumulates. The `Context-Aware Tool Loading` pattern page documents that `context: fork` for skill execution isolates skill instructions in a sub-agent context, meaning a breaking change in one skill cannot affect other skills' execution. The practical versioning approach from existing wiki knowledge: use git commits on the skill folder for version history, test skills by running them in `context: fork` isolation against a known input, and document breaking changes in the Gotchas section rather than through a formal semver process. The `Claude Code Skills` page also notes: "Can skills reference or compose other skills? — formal skill-to-skill composition is not yet documented, so dependency version conflicts are not yet a concern."

**Q: What is the optimal split between CLAUDE.md instructions and skill files for project conventions?**

Cross-referencing `Claude Code Best Practices` and `Context-Aware Tool Loading`: the split is determined by frequency of use and scope. The `Claude Code Best Practices` page states the rule explicitly: "CLAUDE.md is an index, not an encyclopedia. Keep it under 200 lines. Treat it as a routing table that tells Claude where to find detailed information, not as the detailed information itself. Every message re-reads the entire CLAUDE.md, so bloat compounds across every interaction." The `Context-Aware Tool Loading` pattern page provides the decision rule: "any information source used on fewer than ~80% of turns in a session should be deferred." Applied to the CLAUDE.md vs skill split: global conventions used on every turn belong in CLAUDE.md (schema, commands, quality gates); task-specific procedures used only when performing that task (ingestion, export, evolution) belong in skill files loaded on demand. The research wiki's current implementation follows this: CLAUDE.md defines schema and commands; `wiki-agent`, `evolve`, and `continue` skills contain the detailed operational procedures. This matches the `Claude Code Best Practices` rule that CLAUDE.md "acts as a routing table" to skills.

## Relationships

- ENABLES: [[OpenFleet]]
- ENABLES: [[Wiki Ingestion Pipeline]]
- ENABLES: [[Claude Code Skills]]
- ENABLES: [[Claude Code Best Practices]]
- ENABLES: [[Claude Code Context Management]]
- RELATES TO: [[OpenClaw]]
- RELATES TO: [[AICP]]
- RELATES TO: [[Obsidian CLI]]
- RELATES TO: [[notebooklm-py CLI]]
- RELATES TO: [[LLM Wiki Pattern]]

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
[[Claude Code Slash Commands (artemgetmann)]]
[[Decision: MCP vs CLI for Tool Integration]]
[[Harness Engineering]]
[[Hooks Lifecycle Architecture]]
[[Local LLM Quantization]]
[[MCP Integration Architecture]]
[[Model: Claude Code]]
[[OpenArms]]
[[Pattern: Skills + Claude-Code]]
[[Pattern: Skills + Mcp]]
[[Plan Execute Review Cycle]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
[[Synthesis: Claude Code Harness Engineering]]
[[Synthesis: Context Mode — MCP Sandbox for Context Saving]]
[[Synthesis: Superpowers Plugin — End of Vibe Coding (Full Tutorial)]]
[[devops-control-plane]]
