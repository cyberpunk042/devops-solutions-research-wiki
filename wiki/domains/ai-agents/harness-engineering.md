---
title: "Harness Engineering"
type: concept
domain: ai-agents
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    file: raw/articles/building-claude-code-harness-engineering.md
    title: "Building Claude Code with Harness Engineering"
    ingested: 2026-04-08
  - id: src-harness-engineering-github
    type: documentation
    url: "https://github.com/Chachamaru127/claude-code-harness"
    title: "claude-code-harness GitHub"
    ingested: 2026-04-08
  - id: src-claude-code-accuracy-tips
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=D5bRTv6GhXk"
    file: raw/transcripts/claude-code-works-better-when-you-do-this.txt
    title: "Claude Code Works Better When You Do This"
    ingested: 2026-04-08
tags: [harness-engineering, guardrails, plan-work-review, runtime-safety, agent-orchestration, claude-code, spec-driven, typescript]
---

# Harness Engineering

## Summary

Harness engineering is the practice of building structured control systems around LLM coding agents — moving beyond prompt engineering to runtime guardrails, quality validation, and rerunnable verification that keep development on a defined path. Anthropic's Claude Code implements this internally with a streaming agent loop, permission-governed tool dispatch, and context management layer. The community claude-code-harness project codifies the pattern as a 5-verb workflow (Setup → Plan → Work → Review → Release) with a TypeScript guardrail engine (13 rules) that enforces safety at execution time through hooks. The pattern is converging across multiple sources: the superpowers plugin, OpenFleet's deterministic orchestrator, and harness engineering all implement variants of the same Plan → Execute → Review cycle with runtime enforcement.

## Key Insights

- **Runtime enforcement, not prompt guidance**: The critical distinction is that harness guardrails operate at execution time through hooks, actually blocking dangerous operations (sudo, force-push, .env writes) before they happen. This is fundamentally different from instructions that the model may or may not follow.

- **The 5-verb workflow as universal pattern**: Setup → Plan → Work → Review → Release maps to every structured development approach in the ecosystem: superpowers (brainstorm → plan → execute → verify), OpenFleet (task creation → dispatch → execution → review → completion), and the research wiki's own ingestion pipeline (extract → analyze → synthesize → write → integrate).

- **13 guardrail rules (R01-R13)**: Denial rules (block sudo, .git/.env writes, force-push), Query rules (flag out-of-scope writes), Security rules (prevent --no-verify, direct main pushes), Post-execution checks (warn assertion tampering). These rules are TypeScript, not prompts — they execute as hooks with real enforcement.

- **CLI+Skills over MCP is emerging consensus**: Multiple sources converge: CLI tools with Skills (loaded contextually when relevant) are more token-efficient, more accurate, and cheaper than MCP servers (which load all tool schemas into context upfront). This is a significant architectural insight for any project exposing tools to LLM agents.

- **Planning discussion reduces rework**: The harness's Breezing mode adds Planner + Critic roles that review task quality before coding. ~5.5x token cost vs ~4x without discussion, but justified by reduced rework. Same principle as the wiki's "guided" ingestion mode — invest upfront in understanding to avoid downstream errors.

- **Agent teams with shared communication**: Beyond isolated subagents, both harness engineering and OpenFleet implement cross-agent communication channels. The harness uses hook-driven signals, OpenFleet uses IRC channels. Both solve the same problem: coordinating parallel workers.

## Deep Analysis

### The Harness Pattern Hierarchy

The ecosystem implements harness engineering at increasing levels of sophistication:

| Level | Implementation | Enforcement | Example |
|-------|---------------|-------------|---------|
| 0. Prompt guidance | CLAUDE.md, SKILL.md | Model compliance (hope) | Research wiki conventions |
| 1. Status monitoring | Context progress bar | Human intervention at threshold | "Claude Code Works Better" tips |
| 2. Workflow orchestration | superpowers, pipeline.py | Skill-enforced sequencing | This project's pipeline chains |
| 3. Runtime guardrails | Hooks, TypeScript engine | Execution-time blocking | claude-code-harness R01-R13 |
| 4. Deterministic orchestration | OpenFleet brain | Zero-LLM state machine | OpenFleet 30s cycle |

Each level adds stronger guarantees. This project currently operates at levels 0-2. The harness engineering pattern suggests level 3 (hook-based runtime guardrails) as the natural next step — before the eventual level 4 (deterministic orchestration).

### CLI vs MCP: Architectural Implications

The emerging CLI > MCP consensus has direct implications for the research wiki's MCP server (tools/mcp_server.py). The MCP server exposes 13 tools whose schemas load into every conversation. A CLI+Skills alternative would:
- Only load wiki tool instructions when the user invokes `/wiki-agent` skill
- Reduce baseline context overhead from ~2K tokens (MCP schemas) to near-zero
- Be inherently cross-platform (Python CLI works everywhere)

However, MCP has advantages for programmatic composition (chain/group/tree) that CLI lacks. The right answer may be both: MCP for pipeline orchestration, CLI+Skills for human conversations.

## Open Questions

- Should this project adopt the TypeScript guardrail engine for runtime safety, or implement equivalent rules in Python hooks?
- At what point does harness complexity become a net negative for productivity?
- Can the 13 guardrail rules be adapted to protect wiki operations (e.g., block deletion of pages with high connectivity)?
- How do harness engineering patterns change when the agent is running autonomously (OpenFleet) vs interactively (Claude Code)?

## Relationships

- EXTENDS: Claude Code Best Practices
- EXTENDS: Claude Code Skills
- BUILDS ON: Claude Code
- PARALLELS: OpenFleet
- RELATES TO: Research Pipeline Orchestration
- RELATES TO: MCP Integration Architecture
- RELATES TO: OpenClaw

## Backlinks

[[Claude Code Best Practices]]
[[Claude Code Skills]]
[[Claude Code]]
[[OpenFleet]]
[[Research Pipeline Orchestration]]
[[MCP Integration Architecture]]
[[OpenClaw]]
[[Always Plan Before Executing]]
[[Context Management Is the Primary LLM Productivity Lever]]
[[Plan Execute Review Cycle]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
[[Synthesis: Playwright MCP for Visual Development Testing]]
[[Synthesis: Superpowers Plugin — End of Vibe Coding (Full Tutorial)]]
