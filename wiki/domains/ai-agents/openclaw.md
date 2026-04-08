---
title: "OpenClaw"
type: concept
domain: ai-agents
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-openclaw-docs
    type: documentation
    url: "https://github.com/anthropics/claude-code"
    title: "OpenClaw — Agent Framework Documentation"
    ingested: 2026-04-08
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — OpenClaw Usage"
    ingested: 2026-04-08
tags: [openclaw, agent-framework, gateway, brain, memory, skills, heartbeat, mission-control, multi-agent, messaging]
---

# OpenClaw

## Summary

OpenClaw is an open-source (MIT), local-first AI agent framework (352k+ GitHub stars) that runs persistent AI assistants on your own devices, connected through 24+ messaging channels. It wraps a core agent loop in a persistent daemon (Gateway at ws://127.0.0.1:18789) with five components: Gateway (WebSocket daemon, auth, channel management), Brain (ReAct reasoning engine, 10-stage agent loop), Memory (plain Markdown on disk — daily notes + curated MEMORY.md), Skills (hierarchical plugin system via SKILL.md), and Heartbeat (periodic autonomous task execution). OpenFleet builds on OpenClaw as its execution substrate, deploying 10 agent instances through a single gateway with Mission Control as the governance dashboard.

## Key Insights

- **Five-component architecture**: Gateway (WS daemon, channel routing, auth) → Brain (ReAct loop, tool execution) → Memory (Markdown files, human-readable) → Skills (SKILL.md plugins, hierarchical loading) → Heartbeat (periodic turns, cost optimization).

- **10-stage agent loop**: (1) Entry & session resolution → (2) Agent command execution → (3) Context & workspace preparation → (4) Prompt assembly with token limits → (5) Serialized execution per session → (6) Model inference → (7) Tool execution & streaming → (8) Reply assembly & suppression → (9) Compaction & retries → (10) Persistence with write locks.

- **Bootstrap context files**: SOUL.md (persona, boundaries, tone — the "character sheet"), AGENTS.md (procedural rules, workflows — the "what to do"), TOOLS.md (tool guidance), BOOTSTRAP.md (first-run init, auto-deleted), IDENTITY.md (naming/characteristics), USER.md (user profile).

- **24+ messaging channels**: WhatsApp (Baileys), Telegram (grammY), Slack (Bolt), Discord (discord.js), Google Chat, Signal, iMessage (BlueBubbles), IRC, MS Teams, Matrix, Feishu, LINE, Mattermost, and more.

- **Plugin hooks system**: before_model_resolve, before_prompt_build, before_tool_call, after_tool_call, tool_result_persist, before_compaction, after_compaction. This enables extension without modifying core.

- **Multi-agent in single gateway**: Each agent gets its own identity, workspace, memory, and channel bindings. Isolated and independently configurable. OpenFleet deploys 10 agents this way.

- **Mission Control**: Centralized governance dashboard (TypeScript/React frontend, Python backend, Docker Compose). Hierarchical work orchestration (orgs → board groups → boards → tasks → tags), agent lifecycle, approval-driven governance, decision trails, gateway management. 3.6k stars, MIT licensed.

- **Heartbeat for autonomous operation**: Default 30-minute interval. Uses HEARTBEAT.md as task checklist. Supports active hours, per-agent config, task blocks. isolatedSession and lightContext modes for cost optimization — silent heartbeats for idle agents save 70% cost.

- **Memory is just files**: Daily notes in `memory/YYYY-MM-DD.md`, curated into `MEMORY.md`. Users can read and edit directly. No hidden state, no vector database — just Markdown.

## Deep Analysis

### How OpenFleet Uses OpenClaw

OpenFleet is not a fork but a deployment pattern. It uses OpenClaw's multi-agent gateway with customizations:

1. **Agent identity**: Each of the 10 agents has SOUL.md defining its role (architect, software-engineer, qa-engineer, etc.) and HEARTBEAT.md with role-specific periodic tasks.

2. **Gateway as execution substrate**: The gateway at ws://18789 manages all 10 agent sessions. The deterministic orchestrator dispatches tasks to agents by sending messages through the gateway.

3. **Mission Control as ops board**: The fleet's task board, approval system, and activity log. Agents report status, fleet-ops reviews work, humans approve through MC.

4. **Skills as agent capabilities**: Each agent has a curated skill set installed via `scripts/setup-agent-tools.sh`. Skills define what tools and knowledge each role has access to.

5. **IRC as real-time bus**: 10 IRC channels (#fleet, #alerts, #reviews, #sprint, #agents, #security, #human, #builds, #memory, #plane) provide observable, persistent event streams.

### OpenClaw vs Other Agent Frameworks

| Aspect | OpenClaw | LangChain Agents | AutoGPT |
|--------|----------|-----------------|---------|
| Persistence | Markdown files, human-readable | Vector DB, opaque | JSON files |
| Multi-agent | Native (single gateway) | Requires LangGraph | Custom orchestration |
| Channels | 24+ messaging platforms | Code-only | Web UI only |
| Cost control | Heartbeat optimization, silent mode | Token tracking | No built-in |
| Governance | Mission Control, approvals | None built-in | None built-in |

## Open Questions

- What is the performance overhead of running 10 agents through a single gateway vs distributed gateways?
- Can OpenClaw's plugin hook system be used to integrate the research wiki as a knowledge source for all agents?
- How does session serialization handle burst dispatch from the orchestrator (multiple tasks in one cycle)?

## Relationships

- USED BY: OpenFleet
- ENABLES: Claude Code Skills
- RELATES TO: AICP
- RELATES TO: Obsidian Skills Ecosystem
- RELATES TO: NotebookLM Skills
- ENABLES: LLM Knowledge Linting

## Backlinks

[[OpenFleet]]
[[Claude Code Skills]]
[[AICP]]
[[Obsidian Skills Ecosystem]]
[[NotebookLM Skills]]
[[LLM Knowledge Linting]]
[[AI-Driven Content Pipeline]]
[[Claude Code]]
[[Harness Engineering]]
[[Local LLM Quantization]]
[[Plane]]
[[Synthesis: Claude Code Accuracy Tips]]
[[Synthesis: Claude Code Harness Engineering]]
[[Synthesis: Gemma 4 + SearXNG for Free Private OpenClaw]]
